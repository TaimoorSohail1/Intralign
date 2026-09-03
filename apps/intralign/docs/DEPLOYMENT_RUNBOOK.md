# OSLO Release 1 — Staging Deployment Runbook

**Status:** Staging deploy prep (DTM-0041). Binds to: Deployment Governance §2–7,
Runtime Environment Constraint Profile, **DL-054** (Supabase / Neo4j / Redis;
Heroku / Vercel; app runs **native**, only backing services dockerised),
DL-069 / ADR-0007 (internal `gemma4` LLM, native runtime).

> **PRODUCTION DEPLOY IS OWNER-ONLY.** Per Deployment Governance §1/§3/§9 and
> `apps/intralign/CLAUDE.md`, an autonomous agent may operate through **Dev** and **propose**
> Staging; **Staging→Production is human-gated** (tagged release, owner-approved).
> This runbook covers local + Staging bring-up. It commits **no secret** — every
> credential is injected from the platform secret store (Heroku config vars /
> Vercel env / Supabase) per environment. `.env.example` holds **placeholders only**.

---

## 0. Topology (what runs where)

| Component | Runs | DL-054 class |
|---|---|---|
| Backend (FastAPI / uvicorn) | **native** — Heroku `web` dyno | app, native |
| Frontend (Vite SPA) | **native** — Vercel static build + rewrites | app, native |
| Supabase (Postgres + GoTrue/Auth + RLS + pgvector + Storage) | dockerised — Supabase CLI locally (`supabase start`); hosted Supabase project for Staging | backing service |
| Neo4j (knowledge graph) | dockerised — `docker compose` locally; managed instance for Staging | backing service |
| Redis (sessions/cache/streams) | dockerised — `docker compose` locally; managed instance for Staging | backing service |
| OTLP collector + Grafana (otel-lgtm) | dockerised, **opt-in profile** locally; owner-provisioned Grafana for Staging | observability |

The LLM runtime (internal `gemma4`, OpenAI-compatible endpoint) runs **natively /
NOT dockerised** (DL-069). PR CI leaves `OSLO_LLM_LIVE` unset (offline fixtures);
a live leg requires `OSLO_LLM_LIVE=1` + a reachable `OSLO_LLM_BASE_URL`.

---

## 1. Environment configuration

1. Copy the template and fill **real** values locally (never commit `.env`):
   ```bash
   cd apps/intralign
   cp .env.example .env
   ```
2. Every variable the code reads is documented in `.env.example`. The reads are:

   | Var | Read by | Notes |
   |---|---|---|
   | `SUPABASE_URL` | `services/persistence/client.py` | local: `supabase status`; Staging: hosted project URL |
   | `SUPABASE_SERVICE_ROLE_KEY` | `services/persistence/client.py` | **secret** — platform store only |
   | `SUPABASE_JWT_SECRET` | `platform/auth.py` | **secret** — GoTrue HS256 signing secret; verifies caller tokens |
   | `SUPABASE_DB_URL` | `orchestration/checkpointer.py` | durable LangGraph checkpointer + migrations |
   | `OSLO_LLM_BASE_URL` / `OSLO_LLM_MODEL` / `OSLO_LLM_API_KEY` / `OSLO_LLM_LIVE` | `services/llm_provider/` | internal gemma4 runtime; `OSLO_LLM_LIVE=1` only for live legs |
   | `LLM_PRIMARY_PROVIDER` / `LLM_FALLBACK_PROVIDER` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | `services/llm_provider/` | fallback disabled by default; keys are **secret**, optional |
   | `OTEL_EXPORTER_OTLP_ENDPOINT` / `OTEL_SERVICE_NAME` | `services/observability/setup.py` | degrades to a warning when unset |
   | `LANGSMITH_TRACING` / `LANGSMITH_ENDPOINT` / `LANGSMITH_API_KEY` / `LANGSMITH_PROJECT` | `services/observability/langsmith_linkage.py` | LangSmith complement; key is **secret** |
   | `NEO4J_URI` / `NEO4J_USER` / `NEO4J_PASSWORD` | persistence (Neo4j) | password is **secret** |
   | `REDIS_URL` | orchestration (Phase-II-A) | — |
   | Calibration Defaults (`REPLAY_*`, `CONFIDENCE_*`, `DRIFT_*`, `RETENTION_*`) | config | tunable, not architecture |

3. **Staging / Production secret injection** (Deployment Governance §7):
   - Heroku: `heroku config:set SUPABASE_SERVICE_ROLE_KEY=… SUPABASE_JWT_SECRET=… …`
     (per-environment app; least privilege). Never echo or commit the values.
   - Vercel: set the same public/non-secret build vars in Project → Settings → Environment Variables.
   - Supabase: the hosted project holds its own Auth secret + DB credentials.

---

## 2. Bring up the backing services (local)

DL-054: only backing services are dockerised. Supabase is brought up by its **own
CLI**, the other two by `docker compose`.

```bash
cd apps/intralign

# (a) Supabase stack (Postgres + GoTrue + Storage + pgvector). Applies the
#     migrations (§3) and the seed in one shot:
supabase start          # first run pulls images; prints URL + anon/service keys + JWT secret
supabase status         # copy SUPABASE_URL / keys / "JWT secret" into .env

# (b) Neo4j + Redis (and, opt-in, the otel-lgtm observability stack):
docker compose up -d                       # neo4j + redis
docker compose --profile observability up -d   # + otel-lgtm (Grafana :3000, OTLP :4317)
```

Ports are non-default to avoid colliding with another local Supabase stack on this
machine (`supabase/config.toml`: API 54331, DB 54332, Studio 54333). Align
`SUPABASE_URL` / `SUPABASE_DB_URL` in `.env` with `supabase status`.

---

## 3. Migration order (forward-only, additive — Deployment Governance §5)

Migrations are applied in **timestamp order**. `supabase start` / `supabase db
reset` apply the whole `supabase/migrations/` directory automatically; against a
remote/Staging DB use `supabase db push`. The canonical order is:

1. `20260612090000_canonical_append_only_tables.sql` — canonical epistemic store
   (attested_assertion / cognition_history_record / user_acceptance_record /
   history_record); **append-only** (REVOKE UPDATE/DELETE + BEFORE-trigger).
2. `20260612090100_derived_projection_tables.sql` — `derived.*_current`
   projections (rebuildable; the materializer's read surface).
3. `20260612100000_intake_artifact_candidate.sql` — intake artifact / candidate.
4. `20260617120000_chr_output_kind_wave_s.sql` — additive CHR `output_kind`
   widening (wave-S; allowlisted CHECK widening, append-only-preserving).
5. `20260626120000_platform_tables.sql` — **DTM-0031** platform tables (project /
   analysis_run / notification); mutable, workspace-scoped, RLS-enabled.
6. `20260626130000_custom_access_token_hook.sql` — **DTM-0041** Supabase
   custom-access-token hook + `workspace_membership` map (mints
   `app_metadata.workspace_id` + `role`; no secret).

Then the **local-only** `supabase/seed.sql` (the append-only test probe; applied
by `supabase db reset`, never in Staging/Production).

> **Canonical migrations are READ-ONLY here** — DTM-0041 does not alter them; it
> only applies them and adds the two additive platform migrations (5 + 6).
> Canonical-data migrations require explicit owner approval + a verified backup
> (Deployment Governance §5/§9) — out of scope for this slice.

### Enabling the access-token hook on Staging

Locally the hook is wired by `supabase/config.toml`
(`[auth.hook.custom_access_token] enabled = true`). On a **hosted** Supabase
project, after `supabase db push` applies migration 6, enable the same hook in the
Dashboard → Authentication → Hooks → *Custom Access Token*, pointing at
`public.custom_access_token_hook`. Seed `public.workspace_membership`
(user_id → workspace_id + role) for each user via owner/admin provisioning —
the backend verifier fails **closed** if a user has no membership row.

---

## 4. Bring up the app (native)

```bash
# Backend (Heroku web dyno locally = uvicorn):
cd apps/intralign
.venv/bin/uvicorn backend.api.app:app --host 0.0.0.0 --port 8000
#   /health -> {"status":"ok"};  /openapi.json -> the schema the frontend client is generated from.

# Frontend (Vercel build locally = vite):
cd apps/intralign/frontend
npm install
npm run dev      # http://localhost:5173 ; vite proxies /v1,/health,/openapi.json -> :8000
# or a production build:
npm run build    # -> dist/  (what Vercel serves)
```

How the app connects: the backend reads `SUPABASE_*` (persistence + durable
checkpointer), `NEO4J_*`, `REDIS_URL`, `OSLO_LLM_*`, `OTEL_*` from the environment.
The frontend's generated axios client uses **relative** URLs (`/v1`, `/health`,
`/openapi.json`); locally vite's proxy forwards them to the backend, and on Vercel
the `frontend/vercel.json` **rewrites** forward them to the Heroku backend origin.

---

## 5. Deploy to Staging (agent **proposes**; owner approves — Deployment Governance §3)

1. Land the change on `main` via reviewed PR with all CI gates green
   (build · contract-traceability · positive+negative tests · gate-4 invariants ·
   gate-5 observability · gate-6 secret-scan · human review).
2. **Backend → Heroku** (Staging app): set config vars (§1.3), then deploy `main`.
   The `Procfile` `web` process starts uvicorn on `$PORT`. Apply migrations as a
   gated step (`supabase db push` against the Staging DB — §3), **not** ad-hoc.
3. **Frontend → Vercel** (Staging project): set the backend origin in
   `frontend/vercel.json` rewrites (replace `OSLO-BACKEND-PLACEHOLDER.example.com`
   with the Heroku Staging hostname) **or** define the rewrites at the Vercel
   project level. Deploy `main`; Vercel runs `npm run build` → `dist/`.
4. Verify: `GET https://<staging-frontend>/health` → `ok`; a sign-in mints
   `app_metadata.workspace_id`+`role`; create a project → trigger analysis →
   `GET /v1/projects/{id}/findings` returns live `derived.*_current` data.

> **Staging uses synthetic / anonymized data only — never raw production canonical
> data** (Deployment Governance §3). Staging stores + secrets are isolated from
> Production.

## 6. Production (OWNER-ONLY — not performed by the agent)

Production deploy is a human-approved, tagged-release action with a retained prior
tag for rollback (Deployment Governance §6). The agent **STOPS** at the
Staging→Production boundary, at any canonical-data migration, at any new
secret/credential, and at any CI-gate failure (§9). Nothing in this slice promotes
a release tag or deploys to Production.

---

## 7. Live end-to-end leg (the DTM-0030/0031 materializer check)

With the stack up + migrations applied:

```bash
cd apps/intralign
# (offline by default) trigger a deep pass and read the materialized surface:
#   create project -> POST analysis trigger -> submit_trigger runs the deep pass
#   inline (Supabase-Postgres checkpointer) -> materializer upserts derived.*_current
#   -> GET /v1/projects/{id}/findings returns live data.
# A live LLM leg additionally needs:  OSLO_LLM_LIVE=1  + a reachable OSLO_LLM_BASE_URL.
```

See §7 of the worker report in
`docs/deep-tasks/release1-completion-deep-task/deep-task-0041.md` for whether the
live leg was exercised in this environment.

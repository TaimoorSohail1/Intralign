# DTM-0041 — Env binding / staging deploy prep (config, compose, hooks)

**Status:** In progress — OWNER-APPROVED (staging deploy prep) 2026-06-26 · **Module:** DTM-0041 ·
**Phase:** Completion (last) · **Contract:** Deployment Governance §2–7 + Runtime Env + DL-054 ·
**Depends:** all prior slices. **Branch:** `feat/release1-completion`. **Production deploy stays
OWNER-ONLY** (this slice prepares Dev/Staging config + proposes Staging; it does NOT deploy to
Production).

## Goal / observable behavior

The app can be stood up locally and on staging. Audit what Phase I already set up, then complete the
**deployment binding** artifacts: docker-compose for the backing services (Supabase/Neo4j/Redis —
DL-054: only backing services dockerised, the app runs native), the Heroku/Vercel binding (Procfile/
`vercel.json`/build config), the complete `.env.example` (every env var documented, **placeholders
only — no secret**), the **Supabase custom-access-token hook** that mints `workspace_id`+`role` into
`app_metadata` (the DTM-0036 deployment requirement), and a staging runbook. The materializer +
live e2e (flagged across DTM-0030/0031) can then run against a real local stack.

## Source docs / constraints

- Deployment Governance §2 (branches), §3 (Dev/Staging/Prod separation — **Claude autonomous through
  Dev, proposes Staging, Production human-only**), §4 (CI gates), §5 (migration discipline), §7 (no
  secret in repo — secrets via platform store). Runtime Env (Supabase/Neo4j/Redis; Heroku/Vercel;
  native app, dockerised backing services) + DL-054. `code/CLAUDE.md` "Human approval REQUIRED:
  production deploy" + STOP #4/#6. DL-069/ADR-0007 (gemma LLM — `OSLO_LLM_BASE_URL` env).
- Code AUDIT: existing `docker-compose*.yml`, `Procfile`, `vercel.json`, `.env.example`,
  `code/supabase/` (migrations + config), `.github/workflows/app-ci.yml` (the gates), the
  `services/persistence/client.py` + `services/llm_provider` env vars, any Phase-I infra docs.

## Locked decisions (do not re-derive)

- **OWNER-APPROVED for Dev/Staging; Production is owner-only** — prepare compose/config/Procfile/
  vercel/hook/runbook + propose staging. **Do NOT deploy to Production**, do NOT add a real secret,
  do NOT promote a release tag.
- **No secret committed (gate-6)** — `.env.example` placeholders only; document the var names + where
  the secret is injected (Heroku config vars / Vercel env / Supabase). The custom-access-token hook
  is SQL/config (no secret).
- **Backing services dockerised, app native** (DL-054) — compose covers Supabase(Postgres+GoTrue+
  Storage+pgvector)/Neo4j/Redis; the backend/frontend run native (uvicorn/vite; Heroku/Vercel).
- **Additive** — audit + complete; do not duplicate working Phase-I infra. No canonical migration
  change. Apply the existing migrations to the local stack (the platform-table migration DTM-0031 +
  the canonical/derived ones) — document the order.

## Owned files / boundaries

- **OWN:** `code/docker-compose*.yml` · `code/Procfile` / `code/backend/Procfile` · `code/frontend/
  vercel.json` · `code/.env.example` (completeness) · `code/supabase/` config + the custom-access-
  token hook (SQL/config) · a `code/docs/DEPLOYMENT_RUNBOOK.md` (staging) · CI tweaks if needed for
  staging. 
- **READ-ONLY:** the application code (cognition/api/frontend), the canonical migrations (apply,
  don't alter), the governance docs.

## Packages / refactors — none new (infra config only).

## Implementation instructions

1. **Audit** (report): what deploy/infra config exists (compose, Procfile, vercel, env, supabase
   config, CI) vs missing.
2. Complete the missing binding: compose (backing services), Procfile (web = uvicorn + a worker dyno
   for durable runs if needed), `vercel.json` (frontend build + the API proxy/rewrite to the backend),
   `.env.example` (every var, placeholders), the Supabase custom-access-token hook (mint
   workspace_id+role into app_metadata — DTM-0036), the staging runbook (migration order, env setup,
   how to bring it up).
3. If possible, bring up the local stack + apply migrations + run the live e2e leg that DTM-0030/0031
   flagged (materializer → read surface shows live data); report the result (or why it couldn't run
   here).

## Verify (paste exact commands + results)

- `docker compose config` (validate the compose) if docker is available; else lint by inspection.
- `cd code && .venv/bin/pytest tests/positive tests/negative -q` (no regression — config-only should
  not affect tests) + ruff + gate-4 + gate-5. The frontend `npm run build`.
- **gate-6: confirm no secret committed** (only placeholders in `.env.example`; the hook has no
  secret). State this explicitly.

## Manual checks (EM / owner)

- `docker compose up` brings up Supabase/Neo4j/Redis; the backend (native) connects; migrations
  apply; the seeded/real flow works; staging deploy follows the runbook. **Production deploy is the
  owner's tagged-release action — NOT done here.**

## Done criteria

- Deployment binding complete: compose (backing services), Procfile, vercel.json, full `.env.example`
  (no secret), the Supabase custom-access-token hook, the staging runbook; CI gates incl. gate-6
  green; no secret committed; **production deploy left to the owner**. PR cites Deployment Governance.
  **Last completion slice — Release 1 deployable to staging.**

## Worker report

**Status: Ready for review.** Config-only deploy binding; no application/cognition code
changed; **no secret committed; production left to the owner.** Stack verified live.

### AUDIT — existing vs missing (before this slice)

| Artifact | State | Action |
|---|---|---|
| `code/docker-compose.yml` | **EXISTS** — Neo4j 5 + Redis 7 + opt-in `otel-lgtm` profile; Supabase via CLI (DL-054 correct: only backing services dockerised, app native) | left as-is (no duplication) |
| `code/.env.example` | **EXISTS** — already complete + placeholder-only; covers every code env read (`SUPABASE_URL/SERVICE_ROLE_KEY/JWT_SECRET/DB_URL`, `OSLO_LLM_BASE_URL/MODEL/API_KEY/LIVE`, `OPENAI/ANTHROPIC`, `OTEL_*`, `LANGSMITH_*`, `NEO4J_*`, `REDIS_URL`, Calibration Defaults) | verified by grep of `os.environ.get` sites; no change needed |
| `code/supabase/config.toml` + 5 migrations + `seed.sql` | **EXISTS** | added hook migration (6th) + enabled the hook block |
| `code/Procfile` | **MISSING** | **created** |
| `code/frontend/vercel.json` | **MISSING** | **created** |
| Supabase custom-access-token hook (SQL + config) | **MISSING** (config block was commented out; no SQL fn; no membership map) | **created** (migration 6 + config enable) |
| `code/docs/DEPLOYMENT_RUNBOOK.md` | **MISSING** | **created** |
| `.github/workflows/app-ci.yml` (gate-6 CI) | **ABSENT** — no `.github/workflows/` dir in repo at all | **NOT created** — net-new CI pipeline is out of this config-binding scope; the gate scripts themselves (`ci/gate_invariants.py` gate-4, `ci/gate_observability.py` gate-5) + ruff + pytest are present and green locally. Flagged for the EM/owner. |

### Artifacts built

- **`code/Procfile`** — `web: uvicorn backend.api.app:app --host 0.0.0.0 --port ${PORT:-8000}`. Durable LangGraph runs execute **inline on the web dyno** (the command routers call `runner.submit_trigger` synchronously through the Supabase-Postgres checkpointer), so a single web dyno suffices for R1. A `worker` dyno is documented as a Phase-II-A scaling follow-up (needs the Redis cross-dyno coalescing guard already flagged in `runner.py`/`deps.py`) — not enabled. A commented `release:` (`supabase db push`) documents the gated migration step without enabling ad-hoc Production migration.
- **`code/frontend/vercel.json`** — `framework: vite`, build → `dist/`; rewrites forward the generated client's **relative** `/v1`, `/health`, `/openapi.json` to a placeholder backend origin (`OSLO-BACKEND-PLACEHOLDER.example.com`, owner replaces per-env — Vercel does not interpolate env vars in rewrite destinations), plus an SPA catch-all → `index.html`. No secret (public hostname only).
- **`code/supabase/migrations/20260626130000_custom_access_token_hook.sql`** — additive PLATFORM migration: `public.workspace_membership` (user_id → workspace_id + role) map + `public.custom_access_token_hook(jsonb)` (SECURITY DEFINER, `search_path=''`) that merges `workspace_id`+`role` into `app_metadata` — exactly the shape `backend/platform/auth.py` reads (`role` with `prefer_metadata=True`). No-membership → passthrough (backend fails closed). `EXECUTE` granted to `supabase_auth_admin`, revoked from `anon/authenticated/public`; RLS-enabled map (default-deny). **No secret** — the JWT signing secret is never referenced (GoTrue signs after the hook). Touches no canonical table → gate-4 passes.
- **`code/supabase/config.toml`** — enabled `[auth.hook.custom_access_token]` → `pg-functions://postgres/public/custom_access_token_hook` (+7/-3, comment-documented).
- **`code/docs/DEPLOYMENT_RUNBOOK.md`** — staging runbook: topology table (what's native vs dockerised per DL-054), env setup + the full var→reader table, backing-services bring-up (`supabase start` + `docker compose up`), **migration order** (below), the hosted-Supabase hook-enable step + membership seeding, native app bring-up + how it connects, the Staging deploy proposal (agent proposes, owner approves), and an explicit **Production = owner-only** STOP section.

### Migration order (forward-only, additive)

1. `20260612090000_canonical_append_only_tables.sql` (canonical; append-only)
2. `20260612090100_derived_projection_tables.sql` (`derived.*_current`)
3. `20260612100000_intake_artifact_candidate.sql`
4. `20260617120000_chr_output_kind_wave_s.sql`
5. `20260626120000_platform_tables.sql` (DTM-0031 platform tables)
6. `20260626130000_custom_access_token_hook.sql` (**DTM-0041**, new)
… then local-only `seed.sql` (append-only test probe; never Staging/Prod).

### Live e2e result (ran here — docker + Supabase CLI both available)

`supabase db reset` applied **all 6 migrations in order** + seed cleanly (the new hook migration applied 6th). Against the real local stack (Supabase 54331/Postgres 54332, Neo4j, Redis):

- **Hook verified live:** inserted a `workspace_membership` row → `custom_access_token_hook` returned `app_metadata = {"role":"admin","provider":"email","workspace_id":"2222…"}` (preserves existing metadata); no-membership user → claims unchanged (passthrough). Grants: `supabase_auth_admin` has EXECUTE; `anon`/`authenticated` do not.
- **Read surface present:** all 8 `derived.*_current` projection tables + all platform tables (`project`/`analysis_run`/`notification`/`workspace_membership`/`artifact`) + 5 canonical append-only triggers exist in the live DB.
- **Live e2e suites: 10 passed** (`test_intake_live`, `test_b2_live_chain_e2e` — admit→infer→evaluate <60s + recompute-supersedes, `test_full_loop_live` — intake→admission→recompute receipt, `test_artifact_append_only_live` — DB rejects UPDATE on `artifact`). This is the materializer/read-model live leg DTM-0030/0031 flagged, proven against real Supabase Postgres + Storage (body in `artifacts` bucket, rows in Postgres).

### Verify (exact commands + results)

- `docker compose config` → **COMPOSE VALID**.
- `cd code && .venv/bin/pytest tests/positive tests/negative -q` → **746 passed, 65 skipped** (no regression; OTLP trace-export warning is a harmless teardown with no live collector).
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS** (no canonical-table mutation in the new migration).
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS**.
- `cd frontend && npm run build` → **built `dist/` OK** (tsc + vite; only the pre-existing chunk-size advisory).
- Live: `supabase db reset` (6 migrations + seed) OK; 4 live e2e files → **10 passed**.

### Secret statement (explicit)

**No secret committed.** `.env.example` is placeholders-only; the hook migration + config are SQL/config with no secret (the JWT signing secret is read from `SUPABASE_JWT_SECRET` env at runtime, never embedded). `.env` is gitignored (`git check-ignore` confirms). The local Supabase demo keys used for the live run are the well-known default local keys, used in the terminal session only and never written to any file. Secret-scan of all new/changed files → **no secret-shaped value**. **Production deploy / release tag is left entirely to the owner** — this slice prepares Dev/Staging config and proposes Staging only (Deployment Governance §1/§3/§9).

### Working tree

Changed: `code/supabase/config.toml`. New: `code/Procfile`, `code/frontend/vercel.json`, `code/supabase/migrations/20260626130000_custom_access_token_hook.sql`, `code/docs/DEPLOYMENT_RUNBOOK.md`. No unrelated working-tree change touched. Not committed (per instruction; stage if green).

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Deployment binding complete: `Procfile` (web=uvicorn; durable runs inline; worker dyno documented),
  `frontend/vercel.json` (vite build + `/v1` rewrite + SPA), the Supabase custom-access-token hook
  (migration `20260626130000` + config enable — mints `workspace_id`+`role` into `app_metadata`,
  closing the DTM-0036 deployment requirement), `docs/DEPLOYMENT_RUNBOOK.md`. docker-compose +
  `.env.example` already existed (Phase I) — verified, not duplicated.

Verification (EM re-ran + worker ran live): `.venv/bin/pytest` → **746 passed, 65 skipped** (no
regression — config-only). ruff clean; gate-4 PASS (hook migration touches NO canonical table —
confirmed); gate-5 PASS. frontend `npm run build` OK. **Live (worker had docker + Supabase CLI):**
all 6 migrations applied in order; the auth hook proven live (membership → app_metadata claims); the
**DTM-0030/0031 materializer→read-surface live e2e leg PASSED (10 live tests)** against real Supabase
— the live legs flagged across the completion phase are now exercised.

No secret committed (`.env.example` placeholders; hook is SQL/config; `.env` gitignored). **Production
deploy / release tag left entirely to the owner** (Deployment Governance §1 — human-only).

Remaining risks / flagged:
- **No `.github/workflows/` directory exists in the repo** — the gate SCRIPTS (gate-4/5) + ruff +
  pytest are present and green, but the GitHub Actions pipeline YAML that runs them (incl. the gate-6
  secret-scan/npm-audit job) is absent. Authoring it is a net-new CI task for the owner/EM (out of
  this config-binding scope).
- Worker dyno (cross-dyno run coalescing via Redis) is a Phase-II-A scaling follow-up — single web
  dyno suffices for R1.

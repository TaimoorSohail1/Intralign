# DTM-0003 — Local environment verified end-to-end + observability bring-up

**Status:** Approved · **Module:** DTM-0003 · **Phase:** I · **Contract:** none (Phase-I infra; label `phase-1-infra`) · **Depends:** DTM-0002

## Goal / observable behavior

On a clean machine: `supabase start` + `docker compose up -d` bring all backing services
healthy; `uvicorn backend.api.app:app` boots; `GET /health` returns 200; an OpenTelemetry
trace from that request is **visible in the local observability stack**; Orval generates
the frontend client from the live `/openapi.json`.

## Source docs / constraints

- Stack + native-run rule: env profile §6/§7 (amended per DL-054); `code/README.md` bring-up.
- Observability mandate: `00_owner/build_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` (Level 1 operational first).
- LangSmith = config-only in Phase I (decisions A3): env keys + wiring point, no self-hosted instance yet.

## Locked decisions

- Local observability (CONFIRMED): `grafana/otel-lgtm` dev container in `docker-compose.yml` under `profiles: ["observability"]` (dev-only; staging swaps in owner-provisioned Grafana via the same OTLP endpoint env var).
- OTel SDK wiring in `backend/services/observability/`: FastAPI auto-instrumentation + OTLP exporter from `.env` (`OTEL_EXPORTER_OTLP_ENDPOINT`).
- No domain events yet — operational traces only (governed-output events are DTM-0006).

## Owned files

- `backend/services/observability/**`, `docker-compose.yml` (add profile block only), `code/README.md` (verified-commands update), `frontend/src/api/` (generated output only).
- Read-only: migrations, responsibilities, orchestration.

## Packages / refactors

- Approved additions if needed: `opentelemetry-instrumentation-fastapi`, `opentelemetry-exporter-otlp`. Stop-and-ask for anything else. No refactors.

## Implementation instructions

1. Wire OTel tracer provider + FastAPI instrumentation behind `services/observability/setup.py`, called from `api/app.py`.
2. Add the `otel-lgtm` compose profile.
3. Verify the full bring-up sequence; fix only environment/wiring issues found (no scope growth).
4. Run `npm run api:gen`; commit nothing under `src/api/generated` (gitignored) — record that it succeeds.
5. Update `code/README.md` to the exact verified commands.

## Test plan

- Automated: smoke tests extended — app boots with observability enabled/disabled (env-driven); health 200 both ways (negative: bad OTLP endpoint must not crash the app — degrade, log).
- Manual (EM): see a `/health` trace in local Grafana; all containers healthy; `supabase status` green.

## Done criteria

- Clean-machine bring-up reproduces from README alone; trace visible; api:gen works; tests green.

## Worker report

**Worker:** fresh worker, 2026-06-12.

### Built

- `backend/services/observability/setup.py` — `configure_observability(app) -> bool`:
  enabled only when `OTEL_EXPORTER_OTLP_ENDPOINT` is set; service name from
  `OTEL_SERVICE_NAME` (default `oslo-backend`); TracerProvider + `BatchSpanProcessor` +
  OTLP gRPC exporter + `FastAPIInstrumentor.instrument_app`. Degrades gracefully on:
  unset endpoint (warning, returns False), missing OTel packages (`ImportError` →
  warning), unreachable endpoint (best-effort 0.5 s socket probe → warning, but still
  wires the exporter — it retries in the background), any wiring exception (warning).
  Never raises.
- `backend/api/app.py` — minimal call-site edit: one import + `configure_observability(app)`.
- `pyproject.toml` — two approved deps only: `opentelemetry-instrumentation-fastapi>=0.46b0`,
  `opentelemetry-exporter-otlp>=1.25`.
- `docker-compose.yml` — one new service `otel-lgtm` (`grafana/otel-lgtm`,
  `profiles: ["observability"]`, ports 4317/4318/3000, named volume `otel_lgtm_data:/data`)
  + the volume declaration. Nothing else touched.
- Tests: `tests/positive/observability_setup/test_observability_enabled.py` (boots with
  observability enabled, `/health` 200) and
  `tests/negative/observability_setup/test_observability_degrades.py` (endpoint unset →
  warning + 200; dead port `127.0.0.1:59999` → warning + 200, no crash). Placed under
  `observability_setup/` because `observability/` is reserved for DTM-0006.
- `README.md` — bring-up updated to the exact verified commands incl.
  `--profile observability`, Grafana URL, and the DL-054 shifted-Supabase-ports note.

### Verification (real outputs)

1. `docker compose --profile observability up -d` →
   `code-otel-lgtm-1  Up (healthy)` (also neo4j, redis healthy; image ships its own healthcheck).
2. `/tmp/oslo-ci-venv/bin/pip install -e ".[dev]"` → `Successfully installed …
   opentelemetry-exporter-otlp-1.42.1 … opentelemetry-instrumentation-fastapi-0.63b1 …`
   (see flag 2 below for one transitive resolver warning).
3. `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 OTEL_SERVICE_NAME=oslo-backend
   /tmp/oslo-ci-venv/bin/python -m uvicorn backend.api.app:app --port 8000` →
   `curl http://localhost:8000/health` → **HTTP 200** `{"status":"ok"}`.
4. Trace in Grafana/Tempo:
   `curl "http://localhost:3000/api/datasources"` → Tempo datasource uid `tempo`;
   `curl ".../api/datasources/proxy/uid/tempo/api/search?tags=service.name%3Doslo-backend"` →
   **traceID `5e994ea57f07c35bf3ee3d03ce3d67e2`**, `rootServiceName: oslo-backend`,
   `rootTraceName: GET /health`, durationMs 6.
5. `cd frontend && OPENAPI_URL=http://localhost:8000/openapi.json npm run api:gen` →
   `🎉 oslo - Your OpenAPI spec has been converted into ready to use orval!`
   (output in `frontend/src/api/generated/`, not committed — but see flag 1).
6. uvicorn stopped; otel-lgtm + supabase left RUNNING. `supabase status` green
   (API `http://127.0.0.1:54331`, DB `127.0.0.1:54332` — shifted ports per DL-054 note).
7. Full suite: `pytest tests/positive tests/negative` (with `SUPABASE_URL`/
   `SUPABASE_SERVICE_ROLE_KEY` from `supabase status`) → **84 passed**.
   `ruff check .` → **All checks passed!**

### Deviations / flags (EM action needed)

1. **`.gitignore` bug found — NOT fixed (file not in owned set; edit was blocked).**
   `code/.gitignore` line `src/api/generated/` contains an internal slash → anchored to
   `code/`, so it does **not** match `frontend/src/api/generated/`; `git status` shows
   `?? code/frontend/src/api/`. One-line fix for the EM:
   `src/api/generated/` → `frontend/src/api/generated/`. Generated output left on disk
   (untracked), nothing staged/committed.
2. pip resolver warning (pre-existing transitive chain, not caused by the two approved
   deps' identity but by their latest versions): `mistralai 2.4.9 requires
   opentelemetry-semantic-conventions<0.61, but you have 0.63b1`. Runtime unaffected
   (app boots, traces export, 84 tests green); mistralai is an unused pydantic-ai extra
   in Phase I. EM may pin instrumentation `<0.61` if a clean resolver graph is wanted.
3. `OPENAPI_URL` env var in the documented api:gen command is currently inert —
   `frontend/orval.config.ts` hardcodes `http://localhost:8000/openapi.json` (same URL).
   Noted only; frontend config not in owned set.

## Engineering-manager review notes

**Review 1 (2026-06-12):** `setup.py` reviewed — clean env-driven wiring, every failure
path degrades to a warning (never raises), reachability probe warn-only, DTM-0006
boundary respected (operational traces only). `app.py` edit minimal (import + one call).
Compose addition scoped to one profiled service. Scope clean. Worker flags: (1) `.gitignore`
anchor bug — **fixed by EM** (`frontend/src/api/generated/`), verified generated client no
longer untracked; (2) mistralai transitive resolver warning — accepted (unused extra,
runtime green); revisit if pydantic-ai is upgraded; (3) inert `OPENAPI_URL` in README
command — cosmetic, orval.config.ts hardcodes the same URL; cleanup with a later frontend task.

## Approved by engineering manager

Status: Approved

Executive summary:
- Local environment is verified end-to-end: Supabase + Neo4j + Redis + otel-lgtm healthy;
  backend boots natively with env-driven OTel (FastAPI auto-instrumentation → OTLP →
  Tempo/Grafana); Orval generates the client from live `/openapi.json`. Phase I exit-gate
  items 1, 2, and 6 (local) demonstrated.

Verification (EM-run, independent):
- Tempo search API returned multiple `oslo-backend` / `GET /health` traces (e.g.
  `1693f144ac9a2cac23735d15c9b614ad`); worker's trace `5e994ea57f07c35bf3ee3d03ce3d67e2`.
- `pytest tests/positive tests/negative` (live Supabase env) → **84 passed**.
- `ruff check .` → All checks passed.
- App boots with OTEL env unset → warning + `/health` 200 (graceful degradation).

Manual test plan:
- `docker compose --profile observability up -d`; run uvicorn with the README env; hit
  `/health`; open http://localhost:3000 → Explore → Tempo → search service `oslo-backend`.

Remaining risks:
- Two-axis replay hook lands with DTM-0006 (the kickoff DoD item is split: trace ✅ now,
  replay hook with Wave A — by design, replay needs CHRs to exist).
- mistralai resolver warning accepted (see review notes).

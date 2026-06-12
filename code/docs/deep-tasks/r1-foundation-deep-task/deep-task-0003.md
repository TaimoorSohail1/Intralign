# DTM-0003 — Local environment verified end-to-end + observability bring-up

**Status:** Not started · **Module:** DTM-0003 · **Phase:** I · **Contract:** none (Phase-I infra; label `phase-1-infra`) · **Depends:** DTM-0002

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

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_

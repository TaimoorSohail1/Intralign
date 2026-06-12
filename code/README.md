# OSLO Release 1 — Application (`code/`)

Monorepo for the OSLO application: a Python cognition backend + a React frontend.
Build rules: see [`CLAUDE.md`](./CLAUDE.md). Authoritative canon lives in the
knowledge-base zones (`00_owner/`, `30_engineering/`, `20_handoff/`).

> **Governance note:** placing app code here is a monorepo override of the ratified
> default (a separate owner-owned `oslo` repo). It should be recorded as a decision/ADR
> and ratified by the owner. Stack is bound by **DL-054**.

## Stack (DL-054)

- **Backend:** Python · FastAPI (transport) · Pydantic / Pydantic AI · LangGraph (orchestration)
- **Frontend:** React · Vite · MUI · TanStack · Orval (client generated from the backend OpenAPI)
- **Stores:** Supabase (Postgres + Auth/GoTrue + RLS + pgvector + Storage) · Neo4j · Redis
- **Observability:** OpenTelemetry → Grafana · LangSmith (complement)

## Local bring-up (Phase I) — verified commands

```bash
cp .env.example .env            # fill from owner-provided secrets; never commit .env

# 1. Supabase (Postgres + Auth + pgvector + Storage) — via the Supabase CLI
supabase start                  # then: supabase status → copy URL + keys into .env
# NOTE (DL-054): use the ports `supabase status` PRINTS, not the CLI defaults — on this
# machine they are shifted (API http://127.0.0.1:54331, DB 127.0.0.1:54332).

# 2. The other backing services (Neo4j + Redis) + local observability (dev-only)
docker compose --profile observability up -d
#   otel-lgtm = OTLP collector (4317 gRPC / 4318 HTTP) + Grafana UI at http://localhost:3000
#   omit `--profile observability` to run without the observability stack

# 3. Backend (native) — Python project is rooted at code/
pip install -e ".[dev]"
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 OTEL_SERVICE_NAME=oslo-backend \
  uvicorn backend.api.app:app --reload
# /health → 200; the trace appears in Grafana (http://localhost:3000) under Tempo,
# service `oslo-backend`. Unset OTEL_EXPORTER_OTLP_ENDPOINT → app still boots (warns).

# 4. Frontend (native) — backend must be serving /openapi.json first
cd frontend && npm install && npm run api:gen && npm run dev
```

Phase I is **done** only when the Definition of Done in
`30_engineering/implementation/Phase_I_Foundation_and_Environment/IMPLEMENTATION_PLAN.md`
holds (stores healthy, CI gates fail correctly, canonical stores append-only, Staging up).

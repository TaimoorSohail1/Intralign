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

## Local bring-up (Phase I)

```bash
cp .env.example .env            # fill from owner-provided secrets; never commit .env

# 1. Supabase (Postgres + Auth + pgvector + Storage) — via the Supabase CLI
supabase start                  # writes local URL + keys into .env

# 2. The other backing services
docker compose up -d            # Neo4j + Redis; confirm health

# 3. Backend (native) — Python project is rooted at code/
pip install -e ".[dev]" && uvicorn backend.api.app:app --reload

# 4. Frontend (native)
cd frontend && npm install && npm run api:gen && npm run dev
```

Phase I is **done** only when the Definition of Done in
`30_engineering/implementation/Phase_I_Foundation_and_Environment/IMPLEMENTATION_PLAN.md`
holds (stores healthy, CI gates fail correctly, canonical stores append-only, Staging up).

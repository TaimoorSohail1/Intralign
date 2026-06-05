# Phase I — Foundation & Environment

**Sequence:** First. Unblocks all later phases. · **Status:** Not started · **Owner gate:** required before Phase II.
**Maps to:** Onboarding Runbook Phase 1 · the deferred build-time step (task #121) · Deployment Governance.

## Goal
Stand up the ratified environment and the enforcement scaffolding so that autonomous, contract-driven coding can begin safely. No product behavior is built in this phase — it makes the building *possible and governed*.

## Scope (this phase)
- Local Dev stack (Docker): Postgres, Neo4j, MongoDB, Qdrant, Redis.
- LangGraph application skeleton organized by the responsibility code-tree (`AGENTS.md`).
- CI pipeline implementing the Deployment Governance gate sequence (incl. the epistemic-invariant gate).
- Physical schema + environment-profile R1–R5 binding to the Logical Data Model (Attested vs Derived stores; append-only canonical tables).
- Staging provisioned (Heroku/Vercel) with synthetic data; per-environment secrets; observability (OTel→Grafana). Production locked.

## Depends on
- Phase 0 owner setup complete (GitHub Pro + protected `main`; cloud accounts; access).

## Build steps
1. Seed app repo from `03_architecture/engineering/starter_kit/` (compose, `.env`, CI workflow, `AGENTS.md`+`CLAUDE.md`).
2. `docker compose up` — all five datastores healthy.
3. Scaffold `/backend/responsibilities/...`, `/services`, `/shared`, `/frontend`, `/tests` per the code-tree.
4. Wire CI gates; confirm each can **fail** the build.
5. Bind canonical/derived schema; provision Staging + secrets; stand up observability.

## Expected outcomes (definition of done)
- ✅ `docker compose up` brings up all five stores; health checks green.
- ✅ App skeleton compiles/runs; module layout mirrors the responsibility code-tree (no `/authority` module).
- ✅ CI runs on a PR and **blocks** on a forced failure in each gate (build, contract-traceability, tests, invariant, observability, security).
- ✅ Canonical stores exist as **append-only** (Attested/CHR/UAR/PlanFact); derived projection stores separate.
- ✅ Staging deploys from green `main` with synthetic data; Production exists but is locked/empty.
- ✅ A trace + a sample two-axis-replay hook land in Grafana.

## Invariants established here
Canonical/derived store **separation**; canonical **append-only**; **no Authority module**; secrets never committed; production human-gated.

## Testing focus
Infrastructure smoke tests + the CI gates themselves (prove they fail correctly). No domain tests yet.

## Exit gate (owner-approved before Phase II)
Environment reproducible from the repo; CI enforces gates; schema bound and append-only; Staging live, Production locked.

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

## Context manifest — what you need in the repo to implement this phase

> Links only; nothing is copied here. The files below are authoritative in their own locations — if a plan and a source differ, the **source wins**.

### Phase-specific (Foundation)
- **Starter kit (seed the app repo):** `03_architecture/engineering/starter_kit/` (`docker-compose.yml`, `.env.example`, `ci-pipeline.yml`, `AGENTS.md`, `README.md`)
- **Environment binding:** `03_architecture/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` (+ `…/RUNTIME_ENVIRONMENT_PROFILE_DL043_RECONCILIATION_001.md`)
- **Schema source:** `03_architecture/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- **Pipeline/gates:** `01_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md`
- **Code-tree:** `03_architecture/engineering/starter_kit/AGENTS.md` (§ code-tree)

### Always-required (every phase)
- **Agent rules:** `03_architecture/engineering/starter_kit/AGENTS.md` · `01_governance/CLAUDE_CODE_IMPLEMENTATION_CONSTRAINTS_V1.md`
- **Canonical architecture:** `03_architecture/specifications/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`
- **Models:** `03_architecture/runtime_models/RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `…/RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1.md` · `…/RELEASE_1_LOGICAL_DATA_MODEL_V1.md`
- **Standards:** `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` · `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md`
- **Numeric config:** `03_architecture/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md`
- **Ratified scope:** `01_governance/decisions/decision_log.md` (DL-043, DL-044)
- **Testing:** `02_product/specs/testing_fixtures/RELEASE_1_TESTING_STRATEGY_V1.md` · `…/DETERMINISM_CALIBRATION_NOTE_001.md` (test authoring + determinism tiers; pair with each contract's QA section)
- **Observability:** `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` + this wave's **OBS contract** (inside the wave package above — events · audit · two-axis replay · drift/trust signals). Every governed output must emit and be replayable.

## Depends on
- Phase 0 owner setup complete (GitHub Pro + protected `main`; cloud accounts; access).

## Build steps
1. Seed app repo from `03_architecture/engineering/starter_kit/` (compose, `.env`, CI workflow, `CLAUDE.md`+`AGENTS.md`).
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

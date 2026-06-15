# Deep-task decisions — R1 Foundation (Phase I) + Wave A 00R (Phase II start)

**Scope:** complete Phase I (Foundation & Environment) exit gate, then begin Phase II with
the first ratified contract, IC-WA-00R (Recompute & Stale Backbone).
**EM model:** one fresh worker per task; sequential; review → fix → verify → approve.

## Source-of-truth docs (binding; cite, don't copy)

| Concern | Path |
|---|---|
| Phase I plan + DoD | `30_engineering/implementation/Phase_I_Foundation_and_Environment/IMPLEMENTATION_PLAN.md` |
| Day-one checklist | `30_engineering/implementation/Phase_I_Foundation_and_Environment/PHASE_1_BUILD_KICKOFF_PACKET.md` |
| First contract | `20_handoff/contracts/WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` (IC/QA/OBS-WA-00R) |
| Stack binding | `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` (amended per DL-054) |
| Logical data model | `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` (canonical §2; derived §3) |
| Data model (entities) | `30_engineering/data/RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md` |
| Gate sequence | `00_owner/build_governance/DEPLOYMENT_GOVERNANCE_SPECIFICATION_V1.md` + starter-kit `ci-pipeline.yml` |
| Calibration numbers | `30_engineering/environment/RELEASE_1_CALIBRATION_DEFAULTS_V1.md` (mirrored in `code/.env.example`) |
| App build rules | `code/CLAUDE.md` · `code/CONTEXT.md` · `code/docs/adr/0001..0003` |
| Anti-assumption | `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md` — escalate gaps, never invent |

## Repo facts

- Monorepo override (ADR-0001, *proposed*): app lives in `code/` of the knowledge base; `code/` is currently **untracked** (never committed).
- Skeleton scaffolded + py_compile-clean: `backend/{api,orchestration,responsibilities,platform,services,contracts}`, root `shared/`, `tests/{positive,negative}`, frontend (React/Vite/MUI/TanStack/Orval). No `/authority`.
- Existing repo CI: `.github/workflows/doc-integrity.yml` (docs gate) — must not be disturbed.
- Backing stores per DL-054: Supabase via CLI (not compose), compose = Neo4j + Redis only.
- Nothing has been run: no `pip install`, no `supabase start`, no `docker compose up` yet.

## Locked implementation decisions

1. **Branch:** one branch for the whole sequence: `feat/phase1-wavea-00r`. Commits per task, PR at sequence end (or per owner direction).
2. **App CI** = new `.github/workflows/app-ci.yml`, path-filtered `code/**`, 6-gate sequence (build · contract-traceability · tests pos+neg · epistemic-invariant · observability · security). Gates 1,2,3,4,6 real in Phase I; gate 5 scaffold until 00R lands real events (then DTM-0006 upgrades it).
3. **Gate-2 exemption (CONFIRMED by user, 2026-06-12):** PRs labeled `phase-1-infra` bypass the contract-id requirement until the owner closes Phase I; label retired at Phase I exit. Everything else must cite a valid `IC-*` id.
4. **Canonical schema** (Supabase migrations, LDM §2): `attested_assertion` (single table, `attesting_source` discriminator; Plan Fact = user-attested row per LDM §2.4), `cognition_history_record`, `user_acceptance_record`, `history_record`. **Append-only enforced in Postgres itself**: `REVOKE UPDATE, DELETE` + `BEFORE UPDATE OR DELETE` trigger raising exception (belt and braces; not just app discipline).
5. **Derived projections** in separate tables (schema `derived`), rebuildable; FK lineage to CHR ids.
6. **00R chain stages are injected, not implemented**: Infer/Evaluate/Advise don't exist until Waves B/C. The backbone re-runs a registered chain; Phase II-A registers no-op pass-through stages clearly marked as Wave B/C placeholders. Backbone itself produces no cognition (IC-WA-00R A4.3).
7. **DTOs/entities:** `shared/entities.py` binds fields from Data Model v1.2 only as needed per task — no invented fields.
8. **Epistemic-invariant gate (gate 4) static checks:** forbidden tokens (`GovernanceDecision`, `Authority`, banned glossary synonyms) in `code/backend` + `code/shared`; no `/authority` dir; migration linter — no `UPDATE/DELETE/DROP TABLE/ALTER` statements against canonical tables in new migrations.

## Assumptions (escalate if wrong)

- A1. Owner accepts deep-task/CI/migration work as `phase-1-infra` (no IC contract covers foundation).
- A2. Worker machines have Docker + Supabase CLI available; if not, tasks record exact commands as manual checks and the EM runs them.
- A3. LangSmith is config-only in Phase I (env keys, wiring point); a self-hosted instance is owner-provisioned later.

## Owner gates

- **Phase II (Wave A 00R) start AUTHORIZED by owner, 2026-06-12** (DL-044 condition 2).
  Phase I items 3 (live red-proof) and 5 (Staging) remain open in parallel — owner to
  provide Heroku/Vercel accounts + push/PR for live CI.
- Wave A 001/002 deep-tasks to be authored after 00R approval (plan against real code).

## Open conflicts / blocked items

- **Staging (Heroku/Vercel) + Production lock** — blocked on owner Day-0 accounts (kickoff §1). PARKED: not a worker task; exit-gate item 5 needs owner action. Phase I owner sign-off will be partial until then.
- **Grafana trace DoD item 6 (RESOLVED — user confirmed, 2026-06-12):** local Docker Grafana via the `grafana/otel-lgtm` container, compose `profiles: ["observability"]`, dev-only. Staging Grafana later swaps in via the same `OTEL_EXPORTER_OTLP_ENDPOINT`.
- **ADR-0001 ratification** — still `proposed`; owner decision outstanding.

## Package approvals

- Approved (already in pyproject/package.json): fastapi, uvicorn, pydantic, pydantic-ai, langgraph, supabase, neo4j, redis, opentelemetry-sdk, langsmith; react, vite, mui, tanstack, orval, axios.
- Approved dev/CI additions: pytest(-asyncio), ruff, mypy; gitleaks (CI action), pip-audit. **Anything else = stop and ask** (ratified-stack rule).

## Refactor approvals

- None pre-approved. Workers must not restructure folders (tree is ADR-locked).

# DRAFT Decision-Log Entry — ENV-REV-001 (for owner ratification)

**Status:** 🟡 **DRAFT — non-canonical — awaiting owner ratification.** Not a decision-log entry until the owner authors/ratifies it into `00_owner/decisions/decision_log.md`.
**Prepared by:** AI contributor (recommendation generation only — Authority Constraint). **Date:** 2026-06-10
**Framework 001 stage:** Decision (Review = `ENV_REV_001_REVIEW_001.md`).

> AI may not ratify, reject, supersede, or adopt canon. This is proposed text for the owner to edit and enact. Assign the next `DL-0xx` number on ratification.

---

## Proposed entry

**DL-0xx — Revised Phase 1 Foundation environment binding (ENV-REV-001): ratify with conditions**

**Decision.** Ratify the environment-binding revision in `REVISED_PHASE_1_FOUNDATION_STACK_PROPOSAL.md` (ENV-REV-001) as the Release 1 environment binding, amending `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1`, **subject to the four conditions below.** Platform architecture (DL-043) is unchanged; this is an implementation/environment binding only.

**What is ratified (intent).**
- Consolidate relational + auth + vector + object storage onto **Supabase** (Postgres + Auth/GoTrue + pgvector + Storage), local via the Supabase CLI.
- **Remove MongoDB** (roles → Supabase Storage + Postgres `jsonb`) and **remove Qdrant** (→ pgvector).
- Keep **Neo4j** (graph) and **Redis** (cache/sessions/streams).
- **LangGraph** orchestration with a **Postgres checkpointer** for durable, resumable Fast/Deep-Pass runs.
- **Pydantic AI + OSS adapter** behind the canon-mandated `/services/llm_provider` interface (OpenAI primary / Anthropic fallback, structured outputs, streaming).
- **LangSmith** (self-hosted) added for run/trace/cost observability.
- App code runs **natively** (not Dockerized); only backing services are Dockerized. (Already permitted by Profile §6 "containerized or platform-native.")
- Hosting unchanged: Heroku + Vercel.

**Conditions of ratification.**
1. **Observability is additive, not a replacement.** LangSmith **complements** OpenTelemetry → Grafana for runs/traces/cost; it does **not** retire the mandated service-health, queue/event-stream monitoring, two-axis derivation replay, governed-output event emission, drift/trust signals, or retention. CI gate-5 (Observability) remains satisfied at the app level (governed-output events + `CognitionHistoryRecord` recording provider/model/version + LangSmith run linkage).
2. **Audit retention remains owner-pending (OPEN_TBD C1).** Any "≥1-year audit" figure is a proposed default, not a ratified requirement, until reconciled against compliance.
3. **LLM adapter must preserve Profile §5 controls** — workload-based routing matrix, usage quotas, and model-consumption auditability — and the provider/routing choice is approved here per `starter_kit/CLAUDE.md` (human approval required).
4. **Terminology fix.** ENV-REV-001 to refer to the profile as "owner-provided (pending DL-043 reconciliation)," not "ratified."

**Triggered canon changes (each via branch → PR → green doc-integrity gate → owner merge; never main).**
- Amend `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` (§2 DB matrix, §5 LLM, §7 observability) per the above.
- Update the Database Ownership Matrix and `RELEASE_1_LOGICAL_DATA_MODEL_V1.2` physical-binding notes (remove Mongo/Qdrant → Supabase Storage / pgvector).
- Update starter-kit templates (`docker-compose.dev.yml`, `.env`, `ci.yml` gate-5 wording) — **blocked until the app repo / starter kit exists** (build-realization → app-repo relocation parked).
- Reconcile the sibling `ORIENT_PHASE` stage matrix (Mongo/Qdrant → revised bindings).
- Changelog entry (Framework 001 final stage).

**Not in scope of this decision.** Master Spec §8 ↔ State Model recommendation-action reconciliation; the Template / Guided Intake scope ruling — both tracked separately.

**Traceability.** Review: `90_research/design_artifacts/ENV_REV_001_REVIEW_001.md`. Proposal: `90_research/design_artifacts/REVISED_PHASE_1_FOUNDATION_STACK_PROPOSAL.md`. Profile: `30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md`.

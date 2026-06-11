# Runtime Environment Constraint Profile v1

**Document Type:** Runtime Environment Constraint Profile (environment-binding anchor) · **Status:** **Owner-Provided (2026-06-04) — pending DL-043 reconciliation; amended per DL-054 (2026-06-10) — pending owner merge of the DL-054 PR** · **Date:** 2026-06-04
**Role:** This is the artifact DL-043 and all Wave contracts deferred environment binding to. It defines **implementation boundaries and runtime expectations** — it does **not** alter the platform architecture. **Reconciliation against ratified DL-043 is recorded separately** (`RUNTIME_ENVIRONMENT_PROFILE_DL043_RECONCILIATION_001.md`); where this profile's terminology conflicts with the Cognitive Responsibility Architecture / Epistemic State Model, the reconciliation governs and the conflicts are routed to the owner.

> **Guiding principle (owner):** these constraints define implementation boundaries and runtime expectations; they provide a consistent engineering framework for operational, governance, scalability, and maintainability objectives. Architecture (DL-043) is unchanged.

> **🟡 DL-054 amendment (2026-06-10) — applies on merge of the DL-054 PR.** This profile is amended for the revised Phase 1 foundation environment binding (ENV-REV-001): consolidate relational + auth + vector + object storage onto **Supabase** (Postgres + Auth/GoTrue + pgvector + Storage); **remove MongoDB and Qdrant**; add **LangSmith** as an observability **complement** (not a replacement) to OpenTelemetry → Grafana; app code runs **natively** (only backing services Dockerized). Changes appear inline in **§2 (Database Ownership Matrix), §5 (LLM Provider Strategy), §7 (Observability)** below, each marked *Amended per DL-054*. **Platform architecture (DL-043) is unchanged.** Conditions 1–4 of DL-054 apply.

---

## 1. LangGraph Usage Constraints

**Graph architecture:** multiple **domain-specific graphs** with **reusable subgraphs**; avoid a single monolithic graph (maintainability, scalability, testing); shared workflows as reusable subgraphs.
**Graph type:** **StateGraph** preferred; **MessageGraph** only for lightweight conversational workflows without state persistence.
**Human-in-the-loop:** approval checkpoints supported for governance decisions, scope modifications, high-impact recommendations, administrative overrides; human intervention **configurable at the workflow level**. *(See reconciliation §R3 — in R1 the in-product human step is **user acceptance capture**, not OSLO governance; governance HITL is Future.)*
**Persistence & checkpointing:** long-running workflows must support **checkpointing and resumability**; state recoverable after interruption/deploy/failure; execution history auditable.

## 2. Database Ownership Matrix

| Data Type | System of Record |
|---|---|
| Organizations | Supabase Postgres |
| Users | Supabase Postgres |
| Projects | Supabase Postgres |
| Requirements | Supabase Postgres |
| Findings (Derived projection) | Supabase Postgres · canonical = Cognition History Record |
| Issues (Derived projection) | Supabase Postgres · canonical = Cognition History Record |
| Recommendations (Derived projection) | Supabase Postgres · canonical = Cognition History Record |
| Cognition History Records (canonical, append-only) | Supabase Postgres |
| User Acceptance Records (canonical, append-only) | Supabase Postgres |
| Governance Decisions (out of R1 — Authority inactive) | Supabase Postgres |
| Workflow Metadata | Supabase Postgres |
| Documents & Unstructured Content (artifact bodies) | Supabase Storage |
| Derived snapshots / projection blobs (CHR `output_payload`) | Supabase Postgres `jsonb` (large blobs → Supabase Storage) |
| Knowledge Graph Relationships | Neo4j |
| Semantic Embeddings | Supabase pgvector |
| Runtime Sessions | Redis |
| Cache Layer | Redis |
| Event Buffers | Redis |

**Ownership principle:** each entity has a **single authoritative source of truth**; secondary stores are **derived representations**, not primary ownership.

> *(Reconciliation §R2: under DL-043, Findings/Issues/Recommendations are **Derived (non-canonical, recomputable)**; their **Cognition History Records** are the canonical Attested facts. The matrix's "system of record" for these should bind the **Cognition History Record** as canonical and the live Derived projection as a recomputable representation. **Governance Decisions** are **out of R1** (Authority inactive). The matrix omits **Cognition History Record** and **User Acceptance Record** — both must be added as the canonical, append-only stores.)*

> **Amended per DL-054 (2026-06-10):** relational provider = **Supabase Postgres** (local via the Supabase CLI); identity/authz = **Supabase Auth (GoTrue) + RLS** + app-level Org/Project authorization; artifact bodies → **Supabase Storage**, snapshots/projections → Postgres **`jsonb`**; embeddings → **Supabase pgvector**. **MongoDB and Qdrant are removed.** Cognition History Records and User Acceptance Records are now listed as canonical append-only stores (DL-043 reconciliation §R2 enacted). Single-source-of-truth principle unchanged; platform architecture (DL-043) unchanged.

## 3. Event Architecture

**Style:** hybrid — **request/response** for user-facing operations; **event-driven** for background processing.
**Redis usage:** **Streams** for workflow orchestration / async processing; **Pub/Sub** for lightweight notifications / transient events; **caching** for hot runtime data.
**Event categories:** project updates, workflow completions, recommendation generation, embedding refresh, knowledge-graph sync, notification delivery, audit/governance actions. *(Reconciliation: "governance actions" in R1 = integrity-clearance + user-acceptance + recompute events; not OSLO Governance Decisions.)*

## 4. Authentication & Authorization Model

**Tenant model:** multi-tenant. **Hierarchy:** Platform → Organization → Project → Resources.
**RBAC roles:** Platform Administrator · Organization Administrator · Project Manager · Contributor · Viewer.
**Permission inheritance:** Org Admins inherit access to all org projects; project-level permissions may override; **all authorization decisions centrally enforced**.

> *(Reconciliation §R4: this is **access control** — Category E **commodity infrastructure** (Classification Decision 001), **distinct from the Authority/exposure plane** (cognitive governance, deferred). "Authorization decisions" here = identity/permission, **not** OSLO Governance Decisions. No conflict, but the terms must stay separate.)*

## 5. LLM Provider Strategy

**Primary:** OpenAI. **Fallback:** Anthropic Claude.
**Routing by workload:** Complex Reasoning → Premium Reasoning Models · Structured Extraction / Classification / Summarization → Cost-Optimized Models · Agent Workflows → Premium Reasoning Models.
**Abstraction:** all LLM interactions through a **provider abstraction layer** (no vendor lock-in).
**Cost controls:** token monitoring · model routing policies · usage quotas · model-consumption auditability.

> *(Reconciliation: the **model/rule version** captured in every Cognition History Record (DL-043) must include the provider+model identity, so two-axis replay's derivation tier — semantic for AI-assisted — is reproducible per model version.)*

> **Amended per DL-054 (2026-06-10):** the provider abstraction layer is realized as **Pydantic AI + an open-source provider adapter** behind the `/services/llm_provider` interface (OpenAI primary / Anthropic fallback; structured-output validation against contract schemas with retry-on-mismatch; standard streaming). The **workload-based routing, usage quotas, and model-consumption auditability above are preserved** in the adapter (DL-054 condition 3). Provider/routing choice approved per `starter_kit/CLAUDE.md` (human approval required). No `/authority` module.

## 6. Deployment Constraints

**Hosting:** **Heroku** for backend services / workers / operational workloads; **Vercel** for frontend / edge web; remain platform-agnostic where practical.
**Environments:** Development → Staging → Production.
**Requirements:** containerized or platform-native deploys; automated CI/CD; environment-specific config; **secure secrets management**; zero-downtime where feasible; clear frontend (Vercel) / backend (Heroku) separation.

## 7. Observability Expectations

**Telemetry:** **OpenTelemetry** (distributed tracing) · **Grafana** (dashboards/monitoring).
**Logging:** centralized structured logging · correlation IDs across services · workflow-level execution tracing.
**Replay & auditability:** agent execution replay · workflow execution history retention · governance decision audit trails · user action audit logs.
**Monitoring:** service health · workflow execution · queue/event-stream · LLM usage & latency.
**Retention:** operational logs ≥ **90 days**; audit logs per compliance/governance.

> **Amended per DL-054 (2026-06-10):** **LangSmith (self-hosted) is added as a complement, not a replacement** — it covers LLM/agent run + trace + per-run token/cost (a strong fit for cost governance, DL-048). **OpenTelemetry → Grafana is retained** for service-health, queue/event-stream monitoring, and retention; the **two-axis derivation replay, governed-output event emission, and drift/trust signals remain app-level** (Cognition History Record + the determinism harness). CI gate-5 (Observability) is satisfied by governed-output events + a `CognitionHistoryRecord` recording provider/model/version + its LangSmith run id (DL-054 condition 1). **Audit-log retention remains an owner-pending value (OPEN_TBD C1)** — any "≥1-year" figure is a proposed default, not a ratified requirement (DL-054 condition 2).

> *(Reconciliation §R5: map to DL-043 observability — "agent execution replay" = **two-axis replay** (record-exact + derivation-by-determinism); "governance decision audit trails" → **Cognition History Records + integrity-clearance audit** (no Governance Decisions in R1); "user action audit logs" → **User Acceptance Records + intake provenance**. **Outcome Drift** monitored as a product feature, distinct from determinism-drift trust failures.)*

---

## Open Calibration Residual (DL-043 Condition 4 — still owner-pending)

This profile provides infrastructure but **not** the numeric tolerances: **determinism replay tolerances, drift thresholds, confidence-band cutoffs, and tier boundaries** remain an owner-supplied calibration input required before the affected outputs are implemented. (Retention is specified — 90 days ops — the tolerances are not.)

---

*This Runtime Environment Constraint Profile records the owner-provided environment binding — LangGraph (domain-specific StateGraphs with reusable subgraphs, workflow-level human-in-the-loop, checkpointing/resumability), the database ownership matrix (PostgreSQL relational system-of-record, MongoDB documents, Neo4j knowledge graph, Qdrant embeddings, Redis sessions/cache/event-buffers), a hybrid event architecture (request/response for user-facing, Redis Streams/Pub-Sub for background), a multi-tenant Platform→Organization→Project→Resources RBAC model with central enforcement, an LLM provider strategy (OpenAI primary, Anthropic fallback, provider abstraction, workload-based routing, cost controls), deployment constraints (Heroku backend, Vercel frontend, Dev→Staging→Prod, CI/CD, secrets management, zero-downtime), and observability expectations (OpenTelemetry, Grafana, structured logging with correlation IDs, agent/workflow replay, 90-day operational retention). It is the environment-binding anchor that DL-043 and the Wave contracts deferred to, defining implementation boundaries without altering the platform architecture; it is reconciled against ratified DL-043 separately (Findings/Issues/Recommendations are Derived with Cognition History Records as the canonical store; Governance Decisions are out of Release 1; RBAC access control is distinct from the deferred Authority/exposure plane; observability terms map to two-axis replay and integrity/acceptance audit), and the numeric determinism/drift/band calibration remains an open owner-supplied residual.*

**Runtime Environment Constraint Profile v1 recorded.**

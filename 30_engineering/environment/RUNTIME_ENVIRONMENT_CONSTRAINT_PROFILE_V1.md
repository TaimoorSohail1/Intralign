# Runtime Environment Constraint Profile v1

**Document Type:** Runtime Environment Constraint Profile (environment-binding anchor) · **Status:** **Owner-Provided (2026-06-04) — pending DL-043 reconciliation** · **Date:** 2026-06-04
**Role:** This is the artifact DL-043 and all Wave contracts deferred environment binding to. It defines **implementation boundaries and runtime expectations** — it does **not** alter the platform architecture. **Reconciliation against ratified DL-043 is recorded separately** (`RUNTIME_ENVIRONMENT_PROFILE_DL043_RECONCILIATION_001.md`); where this profile's terminology conflicts with the Cognitive Responsibility Architecture / Epistemic State Model, the reconciliation governs and the conflicts are routed to the owner.

> **Guiding principle (owner):** these constraints define implementation boundaries and runtime expectations; they provide a consistent engineering framework for operational, governance, scalability, and maintainability objectives. Architecture (DL-043) is unchanged.

---

## 1. LangGraph Usage Constraints

**Graph architecture:** multiple **domain-specific graphs** with **reusable subgraphs**; avoid a single monolithic graph (maintainability, scalability, testing); shared workflows as reusable subgraphs.
**Graph type:** **StateGraph** preferred; **MessageGraph** only for lightweight conversational workflows without state persistence.
**Human-in-the-loop:** approval checkpoints supported for governance decisions, scope modifications, high-impact recommendations, administrative overrides; human intervention **configurable at the workflow level**. *(See reconciliation §R3 — in R1 the in-product human step is **user acceptance capture**, not OSLO governance; governance HITL is Future.)*
**Persistence & checkpointing:** long-running workflows must support **checkpointing and resumability**; state recoverable after interruption/deploy/failure; execution history auditable.

## 2. Database Ownership Matrix

| Data Type | System of Record |
|---|---|
| Organizations | PostgreSQL |
| Users | PostgreSQL |
| Projects | PostgreSQL |
| Requirements | PostgreSQL |
| Findings | PostgreSQL |
| Issues | PostgreSQL |
| Recommendations | PostgreSQL |
| Governance Decisions | PostgreSQL |
| Workflow Metadata | PostgreSQL |
| Documents & Unstructured Content | MongoDB |
| Knowledge Graph Relationships | Neo4j |
| Semantic Embeddings | Qdrant |
| Runtime Sessions | Redis |
| Cache Layer | Redis |
| Event Buffers | Redis |

**Ownership principle:** each entity has a **single authoritative source of truth**; secondary stores are **derived representations**, not primary ownership.

> *(Reconciliation §R2: under DL-043, Findings/Issues/Recommendations are **Derived (non-canonical, recomputable)**; their **Cognition History Records** are the canonical Attested facts. The matrix's "system of record" for these should bind the **Cognition History Record** as canonical and the live Derived projection as a recomputable representation. **Governance Decisions** are **out of R1** (Authority inactive). The matrix omits **Cognition History Record** and **User Acceptance Record** — both must be added as the canonical, append-only stores.)*

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

> *(Reconciliation §R5: map to DL-043 observability — "agent execution replay" = **two-axis replay** (record-exact + derivation-by-determinism); "governance decision audit trails" → **Cognition History Records + integrity-clearance audit** (no Governance Decisions in R1); "user action audit logs" → **User Acceptance Records + intake provenance**. **Outcome Drift** monitored as a product feature, distinct from determinism-drift trust failures.)*

---

## Open Calibration Residual (DL-043 Condition 4 — still owner-pending)

This profile provides infrastructure but **not** the numeric tolerances: **determinism replay tolerances, drift thresholds, confidence-band cutoffs, and tier boundaries** remain an owner-supplied calibration input required before the affected outputs are implemented. (Retention is specified — 90 days ops — the tolerances are not.)

---

*This Runtime Environment Constraint Profile records the owner-provided environment binding — LangGraph (domain-specific StateGraphs with reusable subgraphs, workflow-level human-in-the-loop, checkpointing/resumability), the database ownership matrix (PostgreSQL relational system-of-record, MongoDB documents, Neo4j knowledge graph, Qdrant embeddings, Redis sessions/cache/event-buffers), a hybrid event architecture (request/response for user-facing, Redis Streams/Pub-Sub for background), a multi-tenant Platform→Organization→Project→Resources RBAC model with central enforcement, an LLM provider strategy (OpenAI primary, Anthropic fallback, provider abstraction, workload-based routing, cost controls), deployment constraints (Heroku backend, Vercel frontend, Dev→Staging→Prod, CI/CD, secrets management, zero-downtime), and observability expectations (OpenTelemetry, Grafana, structured logging with correlation IDs, agent/workflow replay, 90-day operational retention). It is the environment-binding anchor that DL-043 and the Wave contracts deferred to, defining implementation boundaries without altering the platform architecture; it is reconciled against ratified DL-043 separately (Findings/Issues/Recommendations are Derived with Cognition History Records as the canonical store; Governance Decisions are out of Release 1; RBAC access control is distinct from the deferred Authority/exposure plane; observability terms map to two-axis replay and integrity/acceptance audit), and the numeric determinism/drift/band calibration remains an open owner-supplied residual.*

**Runtime Environment Constraint Profile v1 recorded.**

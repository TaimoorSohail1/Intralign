# Runtime Environment Profile — DL-043 Reconciliation 001

**Document Type:** Environment-Binding Reconciliation Review (governance) · **Status:** **Draft · Pending Owner Decision** · **Date:** 2026-06-04
**Reconciles:** `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` (owner-provided) **against** ratified **DL-043** (Cognitive Responsibility Architecture · Epistemic State Model · Derived Cognition Lifecycle · Integrity-not-Authority · User Acceptance Recording · Application/Platform Classification).

> **Mode:** independent reconciliation — the Environment Profile is welcome and unblocks coding, but a few items use **pre-DL-043 vocabulary** (governance decisions, Findings/Issues/Recs as "system of record") that conflict with the ratified epistemic model. I flag these and **route them to the owner**, rather than silently re-binding. **No architecture change.** Per `CLAUDE.md`, owner ratifies.

---

## 0A. Owner Decisions Log (confirmed 2026-06-04)

- **R1 — confirmed.** In R1 the human step = **user-acceptance capture** (record the decision), **not** OSLO governance approval. **Plus owner clarification:** a user **confirmation** also creates a **user-attested plan fact** (the confirmed content becomes canonical, attributed to the user) — factual *in the plan*, not an OSLO world-truth claim. (Recorded in `USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001.md` §0.1.)
- **R2 — confirmed (Option A).** Canonical store = **append-only dated receipts** (Cognition History Records + User Acceptance Records + Attested Assertions incl. user-confirmed plan facts) in PostgreSQL; **live Findings/Issues/Recommendations = recomputable representations** (current-view cache, not system of record); **Governance Decisions removed** from the R1 matrix.
- **R3 — confirmed (rename).** The event category **"governance actions"** is renamed to the real R1 events: **integrity-clearance ("document checked & saved")**, **user-confirmation ("user accepted/edited")**, and **recompute ("OSLO re-ran analysis")**. *Owner note: apply this reclassification at the appropriate implementation time (event-model environment binding), not retroactively rewritten everywhere now.* Tracked for application.
- **R4 — confirmed (separate).** Multi-tenant **RBAC (logins/roles: Platform/Org/Project/Contributor/Viewer)** is **ordinary commodity app work** (Category E) — built in R1, kept **distinct** from the OSLO **Authority/exposure** plane (deciding what's true / what to hide), which stays **out of R1**. "Authorization" in the auth sense ≠ OSLO Governance Decision.
- **R5 — confirmed (term mapping).** Observability terms map to real R1 records: "governance decision audit trails" → **Cognition History Records + integrity-clearance logs**; "agent execution replay" → **two-axis replay** (record-exact + derivation-by-determinism); "user action audit logs" → **User-confirmation receipts**. **Outcome Drift** monitored as a **product feature**, kept distinct from determinism-drift trust failures. *(Adjacent open item, not blocking: audit-log **retention duration** "per compliance" — to be set alongside the numeric calibration.)*
- **CALIBRATION — open.** Numeric determinism/drift/confidence-band tolerances (and audit-log retention duration) remain owner-supplied; owner to provide values **or** approve safe defaults. *(Pending.)*

**Status: R1–R5 all owner-confirmed (2026-06-04). Environment Profile adoptable with reconciliations applied at env-binding (task #121). Only the numeric calibration residual remains open.**

## 0. Headline

**The Environment Profile is conformant and adoptable — with four reconciliations and one standing residual.** The infrastructure choices (LangGraph StateGraphs, Postgres/Mongo/Neo4j/Qdrant/Redis, hybrid events, multi-tenant RBAC, OpenAI-primary/Anthropic-fallback with provider abstraction, Heroku/Vercel, OTel/Grafana) are **compatible with DL-043** and sound. The conflicts are **terminological, not structural** — they stem from the Profile predating DL-043's "Integrity, not Authority" and "Canonical = Attested" ratifications. None blocks adoption; each needs an owner-confirmed mapping before the contracts are environment-bound.

## R1 — Human-in-the-Loop: "governance" vs "user acceptance"

**Profile (§1):** HITL approval for *governance decisions, scope modifications, high-impact recommendations, administrative overrides.*
**DL-043:** OSLO performs **no interpretation acceptance / governance** in R1 (Authority plane inactive). The in-product human step is **user acceptance capture** (User Acceptance Record) — the user *accepts/rejects/defers* a recommendation; OSLO **records**, never gates.
**Reconciliation:** In R1, map the HITL checkpoint on **"high-impact recommendations"** to **user-acceptance capture** (Perceive → User Acceptance Record), **not** an OSLO governance approval. **"Governance decisions" and "administrative overrides"** HITL are **Future (Outcome Governance)** — keep the LangGraph capability available but **inactive in R1**. *Owner decision:* confirm R1 HITL = user-acceptance capture only.

## R2 — Database Ownership Matrix: Derived vs Canonical (the substantive one)

**Profile (§2):** Findings, Issues, Recommendations, **Governance Decisions** listed as **PostgreSQL "System of Record."**
**DL-043:** Findings/Issues/Recommendations are **Derived Cognition — non-canonical, recomputable.** The **canonical** Attested facts are their **Cognition History Records** (OSLO-self-attested, append-only). **Governance Decisions are out of R1.** The matrix **omits** Cognition History Record and User Acceptance Record — the actual canonical stores.
**Reconciliation (proposed binding):**

| DL-043 object | Epistemic state | Proposed store |
|---|---|---|
| **Cognition History Record** (Finding/Issue/Confidence/CAF/Outcome/Recommendation/Clarification emissions) | **Attested — canonical** | **PostgreSQL** (append-only system of record) |
| **User Acceptance Record** (version-pinned) | **Attested — canonical** | **PostgreSQL** (append-only) |
| **Attested Assertions** (Canonical Fact + attested Assumption/Constraint/Dependency) | **Attested — canonical** | **PostgreSQL** (+ **Neo4j** for relationship/dependency graph) |
| **Live Findings / Issues / Recommendations / Confidence / CAF / Outcome Confidence** | **Derived — non-canonical (recomputable)** | **recomputable projection** — Postgres "current view" cache and/or **Redis**; **never the canonical record** |
| **Governance Decisions** | **Future (out of R1)** | **none in R1** |

**Key correction:** the **"single source of truth"** for cognition is the **Cognition History Record**, not the live Derived projection. The live projection is a **derived representation** (exactly the Profile's own "secondary stores are derived representations" principle — applied to cognition). *Owner decision:* confirm this binding; remove Governance Decisions from the R1 matrix; add the two record types.

## R3 — Event Architecture / "governance actions"

**Profile (§3):** event category "audit and governance actions."
**DL-043:** R1 has no Governance Decisions; the equivalent governed-event stream is **integrity-clearance events** (admission), **user-acceptance events**, and **recompute/emission events** (Cognition History appends).
**Reconciliation:** rename/scope the R1 "governance actions" event category to **integrity + acceptance + recompute events**. Redis Streams for the recompute/emission orchestration is a good fit (matches 00R's append-on-recompute). *Owner decision:* confirm scoping.

## R4 — Auth/RBAC vs the Authority plane (keep distinct)

**Profile (§4):** multi-tenant RBAC; "all authorization decisions centrally enforced."
**DL-043 / Classification 001:** RBAC = **Category E commodity access control** — *distinct from* the **Authority/exposure plane** (cognitive governance, deferred). "Authorization" here = **identity/permission**, not OSLO Governance Decision.
**Reconciliation:** **No conflict** — but the terms must not be conflated. RBAC governs *who can see/act in the app*; the (deferred) Authority plane would govern *what cognitive output is exposed/suppressed*. R1 ships RBAC; R1 does **not** ship Authority exposure. *Owner decision:* acknowledge the distinction (no contract needed for RBAC — commodity).

## R5 — Observability term mapping

**Profile (§7):** "agent execution replay," "governance decision audit trails," "user action audit logs."
**DL-043 mapping:**
- "agent execution replay" → **two-axis replay** (record-exact for every Cognition History Record; derivation exact-if-rule / semantic-if-AI). Provider+model identity (from §5) must be captured in each record for derivation replay.
- "governance decision audit trails" → **Cognition History Records + integrity-clearance audit** (no Governance Decisions in R1).
- "user action audit logs" → **User Acceptance Records + intake provenance.**
- **Outcome Drift** is a **product feature** (surfaced via the Cognition History stream); determinism-drift / confidence-inflation are **trust failures** — keep distinct in dashboards. *Owner decision:* confirm mapping for the OTel/Grafana instrumentation.

## Standing Residual — Numeric Calibration (DL-043 Condition 4)

The Profile supplies **retention** (90 days ops) but **not** the **determinism replay tolerances, drift thresholds, confidence-band cutoffs, or tier boundaries.** These remain an **owner-supplied input** required before the affected outputs are implemented. *Owner action:* provide the numeric calibration set.

---

## Readiness Impact

With the Environment Profile provided and these reconciliations confirmed, the **last Critical gate from the Autonomous Development Readiness Audit is closed**: environment binding now exists. Remaining before autonomous coding: **(1)** owner confirmation of R1–R5 mappings; **(2)** the numeric calibration set; **(3)** environment-bound versions of the contracts (the architecture-level triads bind to this Profile); **(4)** the Claude Code coding constraints + code-tree convention (in progress in the handoff plan). The project moves from **NOT READY (environment missing)** toward **READY WITH CONTROLS.**

> ### Proposed Owner Resolution
> Adopt the Runtime Environment Constraint Profile v1 as the canonical environment-binding anchor, **subject to five reconciliations:** **(R1)** R1 HITL = user-acceptance capture (governance/override HITL = Future, inactive); **(R2)** canonical store = **Cognition History Record + User Acceptance Record + Attested Assertions** (Postgres append-only; Neo4j for the dependency graph); live Findings/Issues/Recommendations are **Derived recomputable representations** (not system of record); **Governance Decisions removed from the R1 matrix**; **(R3)** "governance actions" events rescoped to integrity/acceptance/recompute; **(R4)** RBAC access control acknowledged as commodity, **distinct from the deferred Authority plane**; **(R5)** observability terms mapped to two-axis replay + integrity/acceptance audit, Outcome-Drift-as-feature. **Standing residual:** supply the numeric determinism/drift/band calibration before implementation. No architecture change; conflicts are terminological and routed to the owner.

---

*This reconciliation reviews the owner-provided Runtime Environment Constraint Profile against ratified DL-043 and finds it conformant and adoptable with four terminological reconciliations and one standing residual: the profile's infrastructure (LangGraph StateGraphs, Postgres/Mongo/Neo4j/Qdrant/Redis, hybrid events, multi-tenant RBAC, OpenAI-primary/Anthropic-fallback with abstraction, Heroku/Vercel, OpenTelemetry/Grafana) is compatible with the architecture, but its pre-DL-043 vocabulary conflicts where it (R1) frames human-in-the-loop as governance approval rather than R1 user-acceptance capture, (R2) lists Findings/Issues/Recommendations as PostgreSQL system-of-record though they are Derived and recomputable while their canonical Cognition History Records — and the omitted User Acceptance Records — are the true append-only system of record, and lists Governance Decisions which are out of Release 1, (R3) names a "governance actions" event category that in R1 is integrity/acceptance/recompute events, (R4) uses "authorization" for RBAC access control which must stay distinct from the deferred Authority/exposure plane, and (R5) uses observability terms that map to two-axis replay and integrity/acceptance audit with Outcome Drift as a product feature; the numeric determinism/drift/band calibration remains an owner-supplied residual. It proposes an owner resolution adopting the profile subject to these five reconciliations, closes the last Critical environment gate from the readiness audit, and routes all terminological conflicts to the owner without altering the architecture.*

**Runtime Environment Profile — DL-043 Reconciliation 001 complete.**

# Release 1 Runtime Behavior Model v1

**Document Type:** Runtime Behavior Model (architecture-concept; governance) · **Status:** **Updated under DL-043 (2026-06-04)** · **Date:** 2026-06-04
**Consistent with (assumed accepted):** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` · `RELEASE_1_RUNTIME_OWNERSHIP_UPDATE_SPECIFICATION_V1.md` · `RELEASE_1_CONTRACT_INVENTORY_V1.md` · `RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md` · `GOV_ARCH_001_CANONICAL_ARCHITECTURE_GOVERNANCE_REVIEW.md`.

> **Mode:** **behavior only** — defines *what happens* (events, causality, recompute, governance interventions, state transitions, observability). **Does not** define APIs, schemas, tables, workflow/graph nodes, queues, implementation, languages, infrastructure, or deployment (those belong to Runtime Environment Specs / implementation contracts). **Does not** revisit ownership or redesign the architecture; **introduces no new** responsibility/domain/engine/object/layer/service/governance concept. **Invariants preserved:** *cognition generates; Authority governs; Render formats; only reanalysis (recompute) changes assessment; Adapt is emergent, not a responsibility.* **Intend is provisional** (R1: the declared outcome is a Retained Canonical Fact used as drift reference). **Per `CLAUDE.md`, owner ratifies.**

---

## 1. Runtime Event Catalog

*(Event · Producing Responsibility · Consuming Responsibility · Trigger Source · Recompute Impact · Governance Impact · Observability)*

| Event | Producer | Consumer | Trigger | Recompute | Governance | Obs |
|---|---|---|---|---|---|---|
| Artifact Uploaded | Perceive | Retain | user | → promotion → analysis | promotion **authorize** | Yes |
| Context Signal Received | Perceive | Act/Perceive | external signal | may trigger recompute | none | Yes |
| Promotion Candidate Ready | Perceive | Authority/Retain | normalization complete | — | **authorize** (promotion) | Yes |
| Knowledge Promoted / Versioned | Retain | Infer | authorized promotion / edit | **cascading recompute** | authorized | Yes (audit) |
| Finding Detected | Infer | Evaluate, Disclose | analysis pass | derived (this pass) | **exposure** | Yes (generation) |
| Finding Superseded | Infer | Evaluate | recompute re-derivation | derived | exposure | Yes |
| Issue Generated | Evaluate | Authority, Advise, Disclose | Findings ready | derived | **exposure / disposition** | Yes |
| CAF Assessed | Evaluate | Evaluate (aggregate), Disclose | Issues ready | derived | exposure | Yes |
| Outcome Confidence Computed | Evaluate | Disclose | CAF + drivers ready | derived | exposure | Yes |
| Recommendation Generated | Advise | Authority, Disclose | Issue/Finding ready (constrained by Authority) | derived | **exposure (+ authorize if action)** | **Yes (generation)** |
| Clarification Requested | Advise | Authority, Disclose | ambiguity blocking understanding | derived | **exposure** | **Yes (generation)** |
| Clarification Answered | Perceive | Retain → recompute | user | **triggers recompute** | none | Yes |
| Recommendation Accepted | (user-state) | Recommendation record | user | **none** (info-change only) | none | Yes |
| Recommendation Rejected | (user-state) | Recommendation record | user | none | none | Yes |
| Recommendation Deferred | (user-state) | Recommendation record | user | none | none | Yes |
| Recommendation Implemented (info changed) | Perceive (re-intake) | Retain → recompute | user updates info | **triggers recompute** | none | Yes |
| Governance Decision Recorded | Authority | Disclose, Act | governed object ready | **is governance** | n/a | **Yes (core audit)** |
| Disclosure Rendered | Disclose (+ Render) | user | governed (exposed) output | none | post-exposure | light |
| Notification Raised | Disclose | user | awareness event | none (presentation) | **exposure / timing** | Yes |
| Notification Read / Dismissed | (user-state) | Notification record | user | none | none | light |
| Artifact Modified / Saved | Perceive (re-intake) | Retain → stale | user edit | **marks stale → trigger** | none | Yes |
| Stale Detected | Perceive (change-detection) | Act/Disclose | content changed since analysis | **enables reanalysis** | none | Yes |
| Reanalysis Triggered | Act | Adapt (loop) | user / auto / signal | **recompute (by definition)** | none | Yes |
| Recompute Completed | Adapt (emergent) | Disclose | loop finished | n/a | exposure of new outputs | Yes |
| Recompute Failed | Adapt (emergent) | Disclose | loop error | retains last-known-good | none | Yes |
| State Transition Occurred | Adapt (emergent) | Disclose | analysis/stale/reanalysis change | n/a | none | Yes |

*(Catalog is comprehensive for Release 1; actuation/Coordinate/Learn events are Future, excluded.)*

### 1A. DL-043 Behavior Amendments (authoritative — supersede conflicting catalog rows)

The catalog above predates DL-043's "Integrity, not Authority" and Derived-Cognition-Lifecycle ratification. Where it conflicts, the following govern:

- **Admission is integrity-gated, not Authority-gated.** `Artifact Uploaded` / `Promotion Candidate Ready` → admission proceeds on **promotion-readiness + integrity** (attribution/idempotency/evidence-chain), **no Authority "authorize" step in R1.** The "authorize/exposure/disposition" Governance columns are **inactive in R1** (Authority plane specified, not running).
- **`Governance Decision Recorded` → Future/excluded in R1** (alongside actuation/Coordinate/Learn). No Governance Decision object is produced in R1.
- **Every cognition emission appends a Cognition History Record (Attested, append-only).** `Finding Detected`, `Issue Generated`, `CAF Assessed`, `Outcome Confidence Computed`, `Recommendation Generated`, `Clarification Requested`, and each **recompute** emit a new **Cognition History Record**; **recompute appends, never overwrites.** Live cognition is a recomputable projection; only its emission records are canonical.
- **`Recommendation Accepted` (and acceptance of any item) → appends a User Acceptance Record** (user-attested, canonical, append-only), **captured by Perceive**, **version-pinned** to the accepted item's Cognition History Record. It remains *info-change only* (no recompute by itself) and **never** marks the item true/approved/canonical-as-truth. (Replaces the prior `(user-state)` framing for Accept/Reject/Defer with an attested record.)
- **New event — `Acceptance-Impact Assessed`:** Producer **Infer + Evaluate**; Consumer **Disclose**; Trigger = recompute/drift affecting an item that has a User Acceptance Record; Recompute = **derived** (recomputable); Governance = none; Obs = **Yes**. Raises an Acceptance-Impact finding ("a decision you accepted has drifted"). Derived, non-governance.
- **Two-axis replay (per the Lifecycle decision):** the **record** of any emission/acceptance is **exactly replayable** (Attested); the **derivation** is exact-if-rule / semantic-if-AI.

*(No new responsibility introduced; all amendments map to existing Perceive/Retain/Infer/Evaluate/Advise/Disclose owners.)*

## 2. Responsibility Interaction Model

**Canonical forward flow (cognition generates; Authority governs across it):**
```text
Perceive → Retain → [Intend ref] → Infer → Evaluate → Advise → [Authority govern] → Disclose → Act
```

| Responsibility | Inputs | Outputs | Produces events | Consumes events |
|---|---|---|---|---|
| **Perceive** | user/artifact/signals | normalized candidates; stale/change signals | Artifact Uploaded, Signal Received, Stale Detected, Clarification Answered (capture), Artifact Modified | (external) |
| **Retain** | authorized promotions | canonical knowledge, history | Knowledge Promoted/Versioned | Promotion Candidate Ready, Clarification Answered |
| **Intend** *(provisional)* | declared outcome (Canonical Fact) | maintained reference for drift | — *(R1: reference only)* | Knowledge Promoted |
| **Infer** | canonical knowledge | Findings | Finding Detected/Superseded | Knowledge Promoted, Recompute Triggered |
| **Evaluate** | Findings, knowledge, Intend ref | Issues, severity/confidence/CAF/reliability, Outcome Confidence | Issue Generated, CAF Assessed, Outcome Confidence Computed | Finding Detected, Recompute Triggered |
| **Advise** | Issues/Findings, Authority constraints | Recommendations, Clarification Requests | Recommendation Generated, Clarification Requested | Issue Generated |
| **Authority** *(cross-cutting)* | every stage's outputs; posture/tier/policy | Governance Decisions (expose/suppress/defer/block/authorize) | Governance Decision Recorded | Promotion Candidate, Finding/Issue/Recommendation/Clarification ready |
| **Disclose** | governed outputs | meaning-preserving disclosure (rendered) | Disclosure Rendered, Notification Raised, State Transition (presentation) | Governance Decision Recorded, Recompute Completed |
| **Act** | authorized actions; signals/mutations | recompute triggers (R1) | Reanalysis Triggered | Stale Detected, Clarification Answered, Knowledge Versioned |

**Feedback loops (all close via Perceive→recompute):**
- **L1 — Adapt loop (core):** Act (Reanalysis Triggered) → Adapt → Infer → Evaluate → Advise → Authority → Disclose. *(Adapt emergent.)*
- **L2 — Clarification loop:** Clarification Answered → Perceive → Retain → recompute (L1).
- **L3 — Implementation loop:** Recommendation Implemented (info change) → Perceive → Retain → recompute (L1).
- **L4 — Edit loop:** Artifact Modified → Perceive (Stale Detected) → reanalysis → recompute (L1).
- **L5 — Signal loop:** Context Signal Received → Act/Perceive → recompute (L1).

## 3. Runtime Trigger Matrix

| Event | Initiating Trigger | Affected Objects | Affected Responsibilities | Recompute Required? |
|---|---|---|---|---|
| Artifact Uploaded | user | Artifact, Promotion Candidate | Perceive→Retain→(loop) | **Yes** (initial analysis) |
| Knowledge Promoted/Versioned | authorization / edit | Canonical Fact, Project Artifact | Retain→Infer→… | **Yes (cascading)** |
| Clarification Answered | user | Clarification, Canonical Fact | Perceive→Retain→loop | **Yes** |
| Artifact Modified | user | Project Artifact | Perceive→stale | **Yes (on reanalysis)** |
| Context Signal Received | external | Context Signal | Perceive/Act | **Maybe** (if material) |
| Recommendation Accepted/Rejected/Deferred | user | Recommendation (user-state) | (record) | **No** |
| Recommendation Implemented | user (info change) | Canonical Fact | Perceive→loop | **Yes** |
| Governance Decision Recorded | object ready | Governance Decision | Authority→Disclose | **No** |
| Reanalysis Triggered | user/auto/signal | Findings/Issues/Recs/Confidence | Adapt loop | **Yes (by definition)** |
| Notification Read/Dismissed | user | Notification | (record) | **No** |

## 4. Recompute Model

**Recompute (the Adapt loop re-running Infer→Evaluate→Advise) occurs when project *information* changes**, never from presentation or user-state-only actions.

- **Triggers recompute:** **artifact modification** (edit→stale→reanalysis); **clarification response** (new information); **knowledge mutation** (authorized promotion/version); **material external signal**; **stale-state reanalysis**.
- **Does NOT trigger recompute:** **recommendation accept/reject/defer** (user-state only — *acceptance ≠ information change*); **governance decisions** (govern exposure, not assessment); **disclosure/notification/read** (presentation); **navigation**.
- **Scope:** recompute is **cascading by default** — a knowledge change re-derives the dependent chain **Finding → Issue → CAF/Outcome-Confidence → Recommendation/Clarification**; partial/local scoping is an optimization concept, not a behavioral guarantee (the **behavioral contract is full re-derivation of dependents**).
- **Emergence:** **Adapt is emergent** — it is the loop re-running on a trigger; it is **owned by no responsibility**. Trigger detection belongs to **Perceive** (stale/signal) and **Act** (reanalysis trigger). Recompute Completed/Failed are events; failure **retains last-known-good**.
- **Invariant:** **only recompute changes Finding/Issue/Recommendation/Confidence content.** All other interactions are non-mutating.

## 5. Governance Intervention Model

The **Authority Plane** intervenes at defined gates (constrains inputs; governs outputs; **generates nothing**):

| Gate | Triggering Event | Governed Object | Governance Action |
|---|---|---|---|
| **Before promotion** | Promotion Candidate Ready | Artifact/Canonical Fact | **Authorize** (admit to canonical knowledge) |
| **Before generation** (input constraint) | Issue ready (pre-Advise) | candidate space | **Constrain** (posture/tier bound which candidates may be generated) |
| **After generation** | Finding/Issue/Recommendation/Clarification Generated | the generated object | **Expose / Suppress / Defer / Block** |
| **Before disclosure** | governed output → Disclose | Card/View/Notification | **Expose decision gates** what Disclose may show (+ timing) |
| **Before actuation** *(Future)* | authorized action | execution | **Authorize** (R1: recompute is always-on/ungoverned; actuation posture-gated/disabled) |

**Clarity:** governance acts **before generation** (constrains candidate space), **after generation / before disclosure** (exposure disposition), and **before actuation** (authorization, future). It **never generates** Findings/Issues/Recommendations/Clarifications. Recompute is **ungoverned** (always-on, posture-invariant).

## 6. Lifecycle Transition Model

*(per object: states · transition triggers · producing · consuming · emitted events — authoritative source: Runtime Object Model §4)*

- **Finding** — states `detected→acknowledged→addressed→closed` (`→reopened`; any`→superseded`). *Triggers:* analysis/recompute (detect/supersede/close); user (acknowledge/address). *Producer:* Infer. *Consumer:* Evaluate/Advise/Disclose. *Events:* Finding Detected/Superseded.
- **Issue** — `detected→(exposed|deferred|suppressed)→resolved` (`→superseded`). *Triggers:* Evaluate (detect); Authority (expose/defer/suppress); recompute (resolve/supersede). *Producer:* Evaluate. *Consumer:* Authority/Advise/Disclose. *Events:* Issue Generated.
- **Recommendation** — `generated→(accepted|rejected|deferred)→implemented` (`→superseded`). *Triggers:* Advise (generate); user (accept/reject/defer); info-change→recompute (supersede). *Producer:* Advise. *Consumer:* Authority/Disclose. *Events:* Recommendation Generated/Accepted/Rejected/Deferred/Implemented.
- **Clarification Request** — `generated→(answered|dismissed)→consumed` (`→superseded`). *Triggers:* Advise (generate); user (answer/dismiss); answer→recompute. *Producer:* Advise. *Consumer:* Authority/Disclose; Perceive (answer). *Events:* Clarification Requested/Answered.
- **Governance Decision** — `pending→decided(expose|suppress|defer|block|authorize)` (`→superseded`). *Triggers:* governed-object-ready; new decision (supersede). *Producer:* Authority. *Consumer:* Disclose/Act. *Events:* Governance Decision Recorded.

All transitions **append-only**; prior states retained; assessment content changes **only via recompute**.

## 7. Observability Model

*(per event: audit · metric · trace · replay; three observability classes)*

- **Operational observability** — intake success/failure; recompute latency; state-transition timing; notification routing. *(metric + trace; light audit.)*
- **Governance observability** — every **Governance Decision Recorded** (expose/suppress/defer/block/authorize) and promotion authorization. *(full **audit** + trace; replay of the decision.)*
- **Cognitive observability** — **Finding/Issue/Recommendation/Clarification generation events** + Outcome-Confidence computation. *(audit + trace + **replay**: deterministic re-derivation under a pinned baseline — Findings/Issues are derived and must be replayable; recommendation/clarification generation observed for adoption/answer signals.)*

| Event class | Audit | Metric | Trace | Replay |
|---|---|---|---|---|
| Intake / state / recompute (operational) | light | Yes | Yes | recompute replay |
| Governance decisions | **Yes** | Yes | Yes | **Yes** |
| Cognitive generation (Finding/Issue/Rec/Clarification/Confidence) | Yes | Yes | Yes | **Yes (deterministic)** |

Minimum: **state transitions, recompute triggers, governance decisions, recommendation-generation, clarification-generation** are observable (consistent with Contract Inventory §5 / Object Model §7).

## 8. Release 1 Consistency Review

Validated against the Runtime Object Model, Ownership Inventory, and Cognitive Responsibility Architecture:
- **Critical conflicts:** **None.**
- **Major conflicts:** **None.**
- **Minor clarifications:**
  - **M-1.** **Recommendation accept/reject/defer triggers NO recompute** (user-state only); only an **information change** (implement/answer/edit) triggers recompute — preserves *only reanalysis changes assessment*. (Behavioral clarification; consistent with the Recommendation lifecycle.)
  - **M-2.** **Recompute scope is cascading** (full re-derivation of dependents) as the **behavioral contract**; local/partial scoping is an implementation optimization, not a behavioral guarantee.
  - **M-3.** **Intend is provisional** — drift/alignment behavior uses the **Retained declared outcome** as reference in R1; no standalone Intend behavior is specified.
  - **M-4.** **Governance is ungoverned-recompute** — recompute always-on/posture-invariant; governance intervenes at exposure/authorization gates, not on recompute.
- No conflict resolved silently; the above are documented clarifications, not defects, and **none changes ownership, objects, or the architecture.**

## 9. Readiness Assessment

**B — Ready with Minor Clarifications.**

- **Behavioral Completeness Score: 92 / 100** — events, interactions, triggers, recompute, governance gates, lifecycles, and observability are defined for all Release 1 cognition + presentation behavior; −8 for the Minor clarifications (recompute scope; accept-no-recompute; Intend provisional) and excluded Future behavior (actuation/Coordinate/Learn).
- **Observability Readiness Score: 90 / 100** — operational/governance/cognitive observability and replay are specified; −10 for calibration of determinism/replay scope (pinned-baseline tolerance — carried RR-2).
- **Contract Generation Readiness Score: 92 / 100** — behavior is sufficient to generate Implementation/QA/Observability contracts without inventing concepts; −8 for the Minor clarifications + assumed-pending core ratification.

## 10. Recommended Next Artifact

With **architecture, ownership, object model, and behavior model complete**, the next artifact is the **`RELEASE_1_CONTRACT_GENERATION_PLAN_V1.md`** — the dependency-first sequencing that produces **one coordinated contract set (Implementation + QA + Observability) per backlog story** (per `CONTRACT_GENERATION_FRAMEWORK_V1.md`), where each set now references: the **owning responsibility** (Contract Inventory), the **object** (Object Model), and the **behavior** (this model — events, recompute, governance gates, observability). First sets: the foundational behavioral chain (Perceive intake → Infer Finding → Evaluate Issue → Advise Recommendation → Authority governance → Disclose), deferring Future behavior (actuation, Coordinate, Learn, Intend depth).

*(This completes the architecture-side foundation — what exists, who owns it, what happens. The Contract Generation Plan transitions from foundation to the coordinated contract sets that precede implementation contracts and Runtime Environment Specs.)*

---

*This Release 1 Runtime Behavior Model defines what happens at runtime — consistent with the accepted architecture, ownership, and object model — without drifting into implementation. It provides a comprehensive runtime event catalog (intake, knowledge promotion, finding/issue/recommendation/clarification generation, governance decisions, recommendation user-states, recompute and state-transition events) with producers/consumers/triggers/recompute/governance/observability; a responsibility interaction model (Perceive→Retain→[Intend]→Infer→Evaluate→Advise→[Authority]→Disclose→Act) with five feedback loops all closing via Perceive→recompute; a runtime trigger matrix; a recompute model preserving Adapt-as-emergent and the invariant that only information change (artifact edit, clarification answer, knowledge mutation, signal, stale reanalysis) recomputes assessment while recommendation accept/reject/defer and governance/presentation do not, with cascading re-derivation as the behavioral contract; a governance intervention model with gates before promotion, before generation (input constraint), after generation/before disclosure (expose/suppress/defer/block), and before actuation (authorize, future), where Authority generates nothing and recompute is ungoverned; lifecycle transition models for Findings/Issues/Recommendations/Clarifications/Governance Decisions; and an observability model across operational, governance, and cognitive classes including deterministic replay. A consistency review finds no Critical/Major conflicts and four Minor clarifications (accept-no-recompute; cascading scope; Intend provisional; recompute ungoverned), and assesses the model Ready with Minor Clarifications (Behavioral 92, Observability 90, Contract Readiness 92), recommending the Contract Generation Plan as the next artifact. It defines no APIs, schemas, workflow/graph nodes, queues, implementation, infrastructure, or deployment.*

**Release 1 Runtime Behavior Model v1 complete.**


---

## DL-047 Behavior Additions (ratified 2026-06-04)

- **Claim Extracted** (Perceive) — evidence → evidence-attested assertions (source-attributed).
- **Planning Artifact Generated / Regenerated** (Infer) — Derived; appends CHR; recompute-supersedes.
- **Understanding State Changed** (Evaluate) — Initial→…→Mature; only via recompute.
- **False-Confidence Flagged** (Evaluate) — high confidence on weak understanding.
- **Chat Exchange** (Disclose) — non-canonical; may trigger Deep Pass via Advise.
- **Stakeholder Response Submitted** (Perceive) — becomes evidence → triggers Deep Pass.
- **Suggested Fix Offered** (Advise) — application observed as a user artifact edit + recompute (no autonomous write).

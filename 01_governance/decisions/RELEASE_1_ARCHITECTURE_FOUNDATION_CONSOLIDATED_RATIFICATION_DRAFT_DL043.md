# DL-043 (DRAFT) — Release 1 Architecture & Epistemic Foundation — Consolidated Ratification

**Status of this file:** **RATIFIED WITH CONDITIONS — 2026-06-04.** This serves as the **disposition document** for **DL-043**, which is recorded in `01_governance/decisions/decision_log.md` and authorized by **CHG-049**. The owner ratified constituents A–J as a single act. Conditions of record are listed below (notably the numeric-calibration owner input, Condition 4). Downstream artifact revisions are authorized as Resulting Actions and are execution-pending.

> **Owner-directed Clarification (2026-06-04) — Plan-Fact.** Constituent (G) is clarified: a **user confirmation** (accept a recommendation, direct edit, or other commitment) creates a **user-attested Attested Assertion of the confirmed content — a *plan fact*** (canonical, attributed to the user), in addition to the acceptance-event record. A confirmed item is **factual in the plan** but is **not** an OSLO claim of **world-truth** (OSLO never certifies real-world correctness; Acceptance-Impact may still flag later conflict). One-way flow holds: OSLO does not promote its Derived recommendation; the **user authors** the new canonical fact. Recorded in `USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001.md` §0.1 and `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001.md` §2. *(Clarifies, does not alter, the seven (G) invariants — invariant 1 "user acceptance does not make content true" is read as **world-true**; plan-factual commitment by the user remains canonical.)*

> **Note on form.** The owner directed a **single consolidated entry, ratified as one act.** It is presented as one DL-043 with ten enumerated constituent decisions (A–J). If Framework 001A later requires discrete identifiers, the owner may split A–J into DL-043 … DL-052; the content is structured to allow either, but the owner's instruction is **ratify as one act.**

---

## Proposed Entry

### DL-043 — Release 1 Architecture & Epistemic Foundation (Consolidated)

- **Date Recorded:** *(owner to set on ratification; drafted 2026-06-04)*
- **Layer:** Implementation Spec (Architecture) — with cross-checks to Doctrine/Constitution (see *Doctrine Consistency*).
- **Source:** Convergent architecture investigation, documents:
  - `03_architecture/ACTIVE_ARCHITECTURE_RECONCILIATION_DECISION_001.md`
  - `03_architecture/ACTIVE_ARCHITECTURE_RECONCILIATION_RECOMMENDATION_001.md`
  - `03_architecture/ACTIVE_ARCHITECTURE_INTERPRETATION_ACCEPTANCE_ANALYSIS_001.md`
  - `03_architecture/CANONICALIZATION_CONTROL_CHALLENGE_REVIEW_001.md`
  - `03_architecture/RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001.md`
  - `03_architecture/DERIVED_COGNITION_LIFECYCLE_DECISION_001.md`
  - `03_architecture/USER_ACCEPTANCE_EVENT_IMPACT_ANALYSIS_001.md` *(constituent G)*
  - `01_governance/AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md`
  - `01_governance/QA_GOVERNANCE_SPECIFICATION_V1.md` *(constituent H)*
  - `01_governance/OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` *(constituent I)*
  - `01_governance/RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001.md` *(constituent J)*
  - `03_architecture/OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md`; `GOV_ARCH_001_CANONICAL_ARCHITECTURE_GOVERNANCE_REVIEW.md`

- **Decision:** The following ten constituent decisions are ratified together, as a single act, as the Release 1 architecture and epistemic foundation:

  - **(A) Canonical Architectural Representation.** Adopt the **Cognitive Responsibility Architecture** as OSLO's canonical architectural representation (responsibility-primary). Retain the layer model as a **secondary dependency-ordering view.** **Re-home (do not retire)** the governed layer-engineering artifacts (`03_architecture/{components, governance_layer, judgement_layer, runtime_architecture}`) and the integrity contracts as the implementation-detail backing of their owning responsibilities. This resolves ESC-0.

  - **(B) Release 1 Authority Scope — "Integrity, not Authority."** **Defer Authority-as-governance entirely from Release 1.** Reclassify the R1 "promotion" control as an **integrity control** owned by **Perceive** (promotion-readiness) + **Retain** (provenance / idempotency / append-only / evidence-chain), and the R1 "exposure" control as **epistemic-safety disclosure** owned by **Disclose.** The **Authority plane is specified but has no active engine in Release 1.** Outcome/Agent Governance (acceptance, disposition, policy suppression, execution authorization) remains Future.

  - **(C) Epistemic Boundary Invariant; no Canonicalization Control responsibility.** Adopt the **Epistemic Boundary Invariant** (persistence ≠ acceptance; only attributed, re-derivable assertions are canonical; interpretation is never auto-accepted; ambiguity is surfaced, not resolved). **Reject** elevating "Canonicalization Control" to an architectural responsibility — it is either already-owned invariant behavior or, if given discretion, deferred Authority.

  - **(D) Release 1 Epistemic State Model.** Adopt: **Canonical = Attested Assertions** (source-attributed + re-derivable without OSLO inference); **Derived Understanding** = OSLO-generated interpretation (**non-canonical, recomputable**); **Accepted** = deferred to the user/Future, absent in R1. Adopt the single binary epistemic label **Attested | Derived**, **superseding** the prior "Grounded / Candidate" proposal.

  - **(E) Derived Cognition Lifecycle.** Adopt: all cognition (Findings, Issues, Recommendations, Clarifications, Confidence, Reliability, CAF, Outcome Confidence, Alignment/Feasibility/Risk) is **Derived** (non-canonical, recomputable, owned by Infer/Evaluate/Advise). Each emission appends an **Attested, self-attested Cognition History Record** to Retain (immutable, append-only). **Two-axis replay:** record replay = exact for all (audit); derivation replay = exact-if-rule / semantic-if-AI. Drift is preserved via append-only emission history and computed as a **Derived** analysis over it. **Recompute appends history; it never overwrites.**

  - **(F) Autonomous Implementation Control System.** Ratify the control system as the governing operating rules for autonomous development: artifact precedence hierarchy, Claude Code MAY/MUST-NOT rules, the escalation matrix, the implementation readiness gate, and the drift register.

  - **(G) User Acceptance Recording & Reconciliation (additive; non-governance).** Release 1 records and reasons over **user** acceptance events as **attested project history**. A user may accept an interpretation, recommendation, assumption, clarification, or assessment; OSLO **records** that event and **may later reason** over it to detect drift. Specifically:
    - **New user-attested sub-class of Attested Assertion.** Attestation sources are now **evidence-attested**, **OSLO-self-attested** (Cognition History Records), and **user-attested** (acceptance events). All are canonical *as facts about who asserted/did what*, never as truth claims.
    - **New object — User Acceptance Record** (user-attested, append-only): who · when · what was accepted **version-pinned** to the relevant **Cognition History Record** (for Derived items) or attestation id (for Attested items) · optional rationale. **Decoupled** from the accepted item, which (if Derived) stays recomputable. Distinct from — and must not be conflated with — the deferred Disposition / Accepted-Understanding governance objects.
    - **New Derived Cognition type — Acceptance-Impact (Reconciliation) Assessment** (Infer + Evaluate): compares a version-pinned acceptance against current understanding and flags drift affecting a previously accepted decision. Recomputable; emits Cognition History Records; never deletes prior.
    - **Ownership (no Authority engine):** Perceive captures the acceptance action · Retain records it (append-only, user-attested) · Infer/Evaluate reconcile · Disclose surfaces. The **Authority plane remains inactive**; **Package 003 and Wave D remain removed.**
    - **Preserved invariants (acceptance ≠ governance):**
      1. User acceptance does **not** make the accepted content **true**.
      2. User acceptance does **not** make the accepted content **canonical as truth** (the accepted interpretation stays Derived; only the *acceptance event* is canonical, as a user-attested fact).
      3. User acceptance does **not** activate **Authority**.
      4. A **User Acceptance Record is not a Governance Decision** — it records that a user accepted something, not that OSLO determined it true, correct, organizationally approved, or permanently valid.
      5. User acceptance is **append-only project history**.
      6. OSLO **may** compare current understanding against prior user acceptance, but that comparison is **Derived Cognition** (Acceptance-Impact Assessment).
      7. Any future **OSLO-level** acceptance, approval, override, or execution authorization remains **Outcome Governance** and is **out of Release 1**.

  - **(H) QA Governance.** Ratify `QA_GOVERNANCE_SPECIFICATION_V1.md` (Approved-with-Modifications) as the governing QA framework: mandatory positive **and** negative validation per governable output; the Critical/Major/Minor failure-classification model; tiered determinism resolving GAP-1 (exact replay for Governance Decisions + rule-derived outputs; semantic/band/set replay for AI-assisted findings, confidence, recommendations). Determinism is governed at the **governable-output level**. *(Numeric tolerance values are an owner-calibration residual — Condition 4.)*

  - **(I) Observability Governance.** Ratify `OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` (Approved-with-Modifications) as the governing observability framework: governed-event/cognitive-event visibility, auditability, the two-axis replay model (record-exact / derivation-by-determinism), and the **drift distinction** — Outcome Drift is OSLO's product feature (surfaced, never failed), whereas determinism drift / confidence inflation / governance drift are trust failures. *(Numeric drift/tier thresholds are an owner-calibration residual — Condition 4.)*

  - **(J) Application / Platform Capability Classification.** Ratify `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001.md`: classify every Release 1 capability as A (cognitive core), B (cognitive presentation), C (platform shell), D (human interaction), E (commodity infrastructure), or F (deferred); **no governance-grade contracts** for Category C/E/F; the proposed P1–P5 platform-governance track is **not** created; access control stays distinct from Authority exposure. **As amended by constituent (G):** Category-D disposition is **user-acceptance attestation + reconciliation**, not an OSLO Governance Decision.

- **Rationale:** The architecture investigation converged: the apparent layer-vs-responsibility conflict was a settled representation question plus one genuine scope question; first-principles analysis showed R1 "Authority" decomposes into integrity (Perceive/Retain) and disclosure-safety (Disclose), with epistemic acceptance deferred to the user — so no governance plane is required in R1. The epistemic model (Canonical = Attested) and the cognition lifecycle (interpretation Derived; emission Attested) together preserve uncertainty and the full history of understanding-change **without** canonicalizing any interpretation, satisfying the anti-false-certainty doctrine structurally. The cost-of-being-wrong is asymmetric in favor of deferral (governance, if later needed, is added additively over a clean integrity/disclosure foundation). Constituent **(G)** demonstrates this asymmetry in practice: the owner's required capability — recording and reasoning over **user** acceptance — slots in **additively** as user-attested attestation (integrity) plus reconciliation (Derived Cognition), **without** activating Authority, resurrecting Pkg 003/Wave D, or reworking the integrity foundation. Ratifying the set as a package clears ESC-0 and gives every downstream contract and the Runtime Environment Constraint Profile a single canonical target.

- **Disposition:** *(owner to record — Accepted / Accepted with Conditions / Deferred / Returned for Revision)*

- **Conditions (proposed):**
  1. **Refined foundational assumption (owner-confirmed).** *"Release 1 assumes OSLO never performs interpretation acceptance. Acceptance remains a human responsibility. OSLO may record and reason over user acceptance events as attested project history."* OSLO-level acceptance (deciding an interpretation is organizational truth) remains the deferred **Outcome Governance**; **user** acceptance recording + reconciliation is **in** Release 1 per constituent (G), strictly as attestation + Derived Cognition (no Authority engine). *(This refines, and is confirmed by, the owner — it does not reopen B/C/D.)*
  2. **Doctrine consistency confirmed** (see below) — Implementation-tier; must not be read as superseding Doctrine/Constitution.
  3. Downstream artifact revisions (below) are authorized as Resulting Actions, not as separate doctrine.
  4. **Numeric calibration residual (owner-supplied input).** Constituents (H)/(I) ratify the QA/Observability *frameworks* and their determinism/drift *models*; the concrete **numeric tolerances** (determinism replay tolerances, drift thresholds, confidence-band cutoffs, tier boundaries) remain an **owner-supplied calibration input**, to be provided before the affected outputs are implemented. Ratification of the frameworks does not depend on the numbers; implementation does.

- **Supersedes:**
  - The **layer-as-primary representation** of `OSLO_ARCHITECTURE_BASELINE_V1.md` (demoted to secondary view; not deleted).
  - The **"Grounded / Candidate"** labeling proposal (superseded by **Attested / Derived**).
  - The in-flight contract assumption of **Authority-in-R1** (Pkg 003-as-governance and Wave D as R1 scope) — superseded by constituent (B).
  - Does **not** supersede any Doctrine/Constitution decision (DL-001…DL-028 grandfathered; DL-029…DL-042 ratified). Reconciles, does not modify, the open conflict noted at **DL-004**.

- **Doctrine Consistency (cross-check, not supersession):**
  - **DL-003 (Dynamic Epistemic Synthesis)** — consistent: Derived Cognition is recomputable synthesis; canonical history preserves its evolution.
  - **DL-004 (Five Epistemic Object Types: Facts, Inferences, Assumptions, Recommendations, Conflicts)** — consistent/refining: Facts = Attested; Inferences/Recommendations/Conflicts = Derived; Assumptions = Attested-if-stated / Derived-if-inferred. This is an **epistemic-state overlay** on DL-004's types, **not** a replacement. (Note: DL-004 records an open conflict with the component spec; this entry does **not** resolve that conflict and defers it to existing backlog.)
  - **DL-006 (Anti-False-Certainty)** — directly supported: uncertainty remains structurally inspectable (Derived label + confidence + conflict; Disclose obligation).
  - **DL-007 (Human Judgment Authoritative)** — directly supported and **reinforced by constituent (G)**: epistemic acceptance is the user's, and Release 1 now explicitly records those human acceptance decisions as attested project history (without OSLO asserting their truth).

- **Affected Artifacts:**
  - **Revise:** `WAVE_A_CONTRACT_PACKAGE_002_CANONICAL_KNOWLEDGE_RETENTION.md` — integrity-gated admission; add **Cognition History Record** (Attested, append-only, recompute-appends-never-overwrites); add **User Acceptance Record** (**user-attested**, append-only, version-pinned to a Cognition History Record or accepted-item attestation; decoupled from the accepted item); encode Canonical = Attested (incl. evidence-/OSLO-/user-attested sub-classes), persistence ≠ canonicalization, one-way flow, **acceptance-recording ≠ truth-assertion**; inferred assumptions/constraints/dependencies are Derived.
  - **Rescope:** `RELEASE_1_CONTRACT_INVENTORY_V1.md`, `RELEASE_1_CONTRACT_GENERATION_PLAN_V1.md`, `RELEASE_1_CAPABILITY_COVERAGE_REVIEW_V1.md`, `RELEASE_1_RUNTIME_OBJECT_MODEL_V1.md`, `RELEASE_1_RUNTIME_BEHAVIOR_MODEL_V1.md` — remove Authority-as-R1; Governance Decision = Future. Add the **User Acceptance Record** object, the **user-attested** attestation sub-class, and the **Acceptance-Impact (Reconciliation) Assessment** Derived type.
  - **Update (constituent G):** `RELEASE_1_EPISTEMIC_STATE_MODEL_DECISION_001.md` — note Attested includes a **user-attested** sub-class. `DERIVED_COGNITION_LIFECYCLE_DECISION_001.md` — add **Acceptance-Impact Assessment** to the Derived catalog. `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001.md` — **reclassify R1 disposition** (issue/recommendation/clarification/resolution) as **user-acceptance attestation + reconciliation**, **not** an OSLO Governance Decision / Wave D.
  - **Add to contract roadmap:** a **User Acceptance & Reconciliation** package (non-governance; spans Perceive capture → Retain user-attested record → Infer/Evaluate reconciliation → Disclose), **sequenced after** the Derived-cognition/Cognition-History packages it consumes. Distinct from the deferred Authority work.
  - **Drop from R1:** Wave A Contract Package 003 (Authority-as-governance) and Wave D (Authority/Exposure) — integrity substance folds into Perceive/Retain; disclosure into Disclose. **(Unchanged by constituent G — user acceptance is not these.)**
  - **Re-home:** governed layer-engineering dirs + integrity contracts under owning responsibilities.
  - **Adopt as canonical:** `OSLO_COGNITIVE_RESPONSIBILITY_ARCHITECTURE_SPECIFICATION_V1.md` (representation); `AUTONOMOUS_IMPLEMENTATION_CONTROL_SYSTEM_V1.md` (operating rules); `QA_GOVERNANCE_SPECIFICATION_V1.md` (constituent H); `OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1.md` (constituent I); `RELEASE_1_APPLICATION_PLATFORM_CLASSIFICATION_DECISION_001.md` (constituent J).
  - **Unaffected:** Doctrine, Constitution, ontology registry, canonical definitions (except the DL-004 overlay note), CLAUDE.md.

- **Resulting Actions:**
  1. Mark ESC-0 (active-architecture conflict) **Closed.**
  2. Execute the artifact revisions/rescopes/drops above.
  3. Add the **Epistemic Boundary Invariant + Attested/Derived labeling + Cognition History Record** as the mandatory pre-Wave-A clarification (one invariant + one label + one Attested record type; no new package, no new owner).
  4. Register constituent **(G)**: the **User Acceptance Record** object (user-attested, append-only, version-pinned), the **user-attested** attestation sub-class, and the **Acceptance-Impact Assessment** Derived type, with the seven preserved acceptance-≠-governance invariants. Confirm the **Authority plane stays inactive** and **Pkg 003/Wave D stay removed**.
  5. Register constituents **(H) QA Governance**, **(I) Observability Governance**, and **(J) Application/Platform Classification** as ratified frameworks/decision; record the **numeric calibration residual** (Condition 4) as an open owner-input, not a blocker to ratification.
  6. Authorize the **Runtime Environment Constraint Profile** as the next artifact (the single remaining hard gate to coding).
  7. Record the corresponding changelog entry (CHG-NNN) and any disposition document(s).
  8. GOV-ARCH-001 ratified as part of constituent (A).

- **Status:** **Proposed — Pending Owner Ratification.** *(On ratification: Ratified / Ratified with Conditions per owner. Owner instruction: ratify A–J as a single act.)*

---

## Owner Ratification Checklist (for convenience)

- [ ] Confirm Condition 1 (OSLO performs no interpretation acceptance; user acceptance is recorded as attested history) against product intent.
- [ ] Confirm constituent (G) invariants (acceptance ≠ truth / ≠ canonical-as-truth / ≠ Authority / append-only / comparison-is-Derived / OSLO-acceptance stays Future).
- [ ] Confirm constituents (H) QA Governance, (I) Observability Governance, (J) Application/Platform Classification — and that the numeric calibration values (Condition 4) are an owner-input, not a ratification blocker.
- [ ] Confirm Doctrine consistency (DL-003/004/006/007) — or route any conflict to backlog.
- [ ] Ratify A–J as a **single act** (owner instruction); split into DL-043…DL-052 only if Framework 001A later requires discrete IDs.
- [ ] Set Disposition + Date + Status; move entry into `decision_log.md`.
- [ ] Record changelog (CHG-NNN); create disposition document(s) per Framework 001A.
- [ ] Supply numeric calibration values (determinism/drift/band tolerances) before the affected outputs are implemented.
- [ ] Authorize Runtime Environment Constraint Profile as next artifact.

---

*This draft consolidates the converged Release 1 architecture and epistemic foundation into a single proposed decision-log entry (DL-043) with seven constituent decisions — Cognitive Responsibility representation; Integrity-not-Authority R1 scope; the Epistemic Boundary Invariant with rejection of a Canonicalization Control responsibility; the Epistemic State Model (Canonical = Attested, Derived non-canonical, Accepted deferred, Attested/Derived labels superseding Grounded/Candidate); the Derived Cognition Lifecycle (live recomputable cognition, Attested self-attested Cognition History Records, two-axis replay, snapshot-based drift); ratification of the Autonomous Implementation Control System; User Acceptance Recording & Reconciliation (a user-attested sub-class of Attested Assertion, the version-pinned User Acceptance Record object, and the Acceptance-Impact Assessment Derived type — additive and non-governance, preserving that user acceptance never makes content true, canonical-as-truth, or active Authority, while OSLO-level acceptance/approval/override/execution remains deferred Outcome Governance); ratification of QA Governance (mandatory positive+negative validation, failure classification, tiered determinism); ratification of Observability Governance (governed/cognitive-event visibility, two-axis replay, Outcome-Drift-as-feature vs trust-failure drift); and ratification of the Application/Platform Capability Classification (Categories A–F; no governance contracts for C/E/F; no P1–P5 platform track). It records rationale, the refined falsifiable product-intent condition, the numeric-calibration residual as an owner input, supersessions (layer-as-primary representation, Grounded/Candidate, Authority-in-R1), explicit Doctrine consistency cross-checks (DL-003/004/006/007 — refining, not superseding), affected-artifact revisions/rescopes/drops/additions, and resulting actions (close ESC-0, revise Package 002, register constituents G/H/I/J, authorize the Runtime Environment Constraint Profile as the next gate). Per the owner's instruction it is to be ratified as a single act (A–J). It is a proposed entry only, adopts nothing, and is routed to the owner for ratification per CLAUDE.md.*

**DL-043 (DRAFT) — Consolidated Ratification entry prepared. Pending Owner Ratification.**

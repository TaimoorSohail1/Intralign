# QA Governance Specification v1

**Document Type:** Governance Specification · **Status:** **Ratified with Conditions under DL-043 (2026-06-04)** · **Date:** 2026-05-31
**Authoritative inputs (accepted; not redesigned):** OSLO Cognitive Responsibility Architecture Specification · Runtime Ownership Update Specification · Contract Inventory · Runtime Object Model · Runtime Behavior Model · Contract Generation Plan · Runtime Environment Constraint Profile.

> **Mode:** independent governance authority — **challenge assumptions; identify gaps; do not rubber-stamp.** Defines **only**: how correctness is determined · what must be validated · what constitutes a release gate · how regressions are handled · how conformance is measured. **No** implementation, test frameworks, tooling, databases, APIs, infrastructure, deployment, or coding. **No** new responsibilities/objects/domains/engines/services/layers/planes/governance/runtime concepts. **Per `CLAUDE.md`, owner ratifies.**

---

## 1. Purpose

QA Governance defines **how OSLO determines that an increment is correct enough to be trusted and released.** It governs **what must be validated, the gates that must pass, how regressions are handled, and how conformance is measured** — not how tests are built.

**Why QA exists:** a built increment is **not yet a trusted increment.** Validation is the gate between *implemented* and *trusted*; without it, an increment cannot be shown to honor its contract, its ownership, or the architecture's invariants.

**Relationships:**
- **Architecture Governance** decides *what is correct structurally* (responsibilities, ownership, objects, behavior, invariants).
- **Contract Governance** decides *what each increment must do* (Implementation/QA/Observability contracts per story).
- **QA Governance** (this document) decides *whether the increment does it* — validation **before** trust/release.
- **Observability Governance** decides *whether it succeeds in reality* — validation **after** release (Validated ≠ Successful).

QA sits **between Contract and Observability:** contracts define expectations, QA validates them pre-release, observability validates outcomes post-release. QA is **architecturally independent of implementation** (the implementer does not validate itself).

## 2. QA Governance Principles

- **Behavior before implementation** — validation targets behavior (events/recompute/governance/state), not technology.
- **Contracts before testing** — every validation traces to a contract's acceptance/fail-condition/invariant; QA invents no requirements.
- **Ownership traceability** — every validated output traces to **one owning responsibility**.
- **No orphan behavior** — every behavior/event has an owner to validate against.
- **Positive *and* negative validation are both required** — prove required behavior present **and** forbidden behavior absent. *A validation set without negative validation is invalid.*
- **Deterministic validation** — cognitive outputs are validated by **deterministic re-derivation** under a pinned baseline (the substitute for ground truth — §8).
- **Governance visibility** — every governed object's exposure/authorization is observable and auditable, and QA validates that it is.
- **Regression protection** — previously-approved behavior/conformance/invariants are preserved across change.
- **Validate derivation, not verdict** — QA validates that a Finding/Issue/Recommendation is *well-formed, traceable, deterministic, and governed*, **not** that it is "true" or "best" (§8).
- **Humans approve** — QA produces evidence and a pass/fail recommendation; the owner/human approves release.

## 3. QA Validation Hierarchy

Five validation layers, **dependency-ordered** (each presupposes the layer above):

1. **Object Validation** — validate object **existence**, **ownership** (one responsibility), **lifecycle** (creation/supersession/archival), **state transitions** (legal states/terminals per Object Model §4). *Foundation: an object must be well-formed before its behavior is meaningful.*
2. **Behavior Validation** — validate **event generation**, **recompute behavior** (only information change recomputes; cascading), **governance intervention** (gates fire), **state transitions** (Behavior Model). *Presupposes valid objects.*
3. **Governance Validation** — validate **authority decisions** (expose/suppress/defer/block), **exposure decisions**, **authorization decisions**; that Authority **generates nothing** and acts at defined gates. *Presupposes valid behavior.*
4. **Contract Validation** — validate **Implementation** (acceptance present), **QA** (positive + negative tests present and passing), **Observability** (events/audit/replay present) contract conformance for the increment. *Spans the above.*
5. **Regression Validation** — validate that **previously-approved behavior/conformance/invariants remain valid** after change (§7). *Continuous; runs on every change.*

**Dependency rule:** a layer's failures **block** the layers below it (an ownership defect at Object Validation invalidates downstream behavior/governance validation).

## 4. Failure Classification Model

| Severity | Meaning | Examples | Release Impact | Escalation |
|---|---|---|---|---|
| **Critical** | Violates architecture invariant, ownership, or authority | orphan/duplicate ownership; **unauthorized generation** (Authority generating; Advise authorizing); **assessment changed outside recompute**; **Recommendation opened outside Finding context**; **Confidence as project health/score**; **stale presented as current**; mutable history; governed object **not observable** | **Blocks release (and the whole gate)** | **Owner-ratified reconciliation** (never resolved in code) |
| **Major** | Breaks a contract requirement or determinism | **missing negative validation**; **regression failure**; non-deterministic re-derivation beyond tolerance; missing observability for a governed object; missing applicable invariant binding | **Blocks the affected capability** | QA lead + owner if invariant-adjacent |
| **Minor** | Quality/clarity issue, no invariant breach | object-classification ambiguity; presentation calibration; documentation gap | **Does not block; tracked** | QA lead |
| **Informational** | Advisory note / improvement | observation; future-hardening suggestion | None | record |

**Rule:** **any Critical fails the release gate; any Major fails the capability gate.** Minor/Informational are tracked, not gating.

## 5. Release Gate Model

A capability/release **passes the gate** only when **all** hold (objective):
- **G-1.** **No Critical failures.**
- **No ownership violations** — every output one owner; no orphan; no duplicate.
- **No governance violations** — Authority generates nothing; gates fire; no unauthorized generation; only-recompute-changes-assessment.
- **No observability violations** — every governed object's exposure/authorization + every cognitive generation event is observable/auditable.
- **No orphan outputs** — every behavior/event traces to an owning responsibility.
- **Contract conformance** — Implementation + QA (positive **and** negative) + Observability contracts pass.
- **Regression passes** — prior-approved behavior/conformance/invariants preserved.
- **Invariants verified** — Recommendation-only-in-Finding-context; Confidence-never-health; stale-never-current; history-append-only; Resolution-Paths-presentation-only; cognition-generates/Authority-governs.

A capability ships **only** when its gate passes; a **Critical anywhere** fails the **release**.

## 6. Conformance Validation Rules

Architecture-level conformance checks (QA validates these for every increment):
- **QG-1.** **Every output has exactly one owning responsibility** (Inventory).
- **QG-2.** **No responsibility overlap / duplicate ownership** (cross-cutting Authority/Disclose are interactions, not co-ownership).
- **QG-3.** **No orphan behavior** — every event/behavior has an owner.
- **QG-4.** **No unauthorized generation** — only **Advise** generates candidate responses; **Authority generates nothing**; Infer/Evaluate/Disclose/Act generate no recommendations.
- **QG-5.** **Only recompute changes assessment** — no non-recompute interaction alters Finding/Issue/Recommendation/Confidence content.
- **QG-6.** **Every state transition is testable** — legal states/terminals defined and reachable; append-only.
- **QG-7.** **Every governed object is observable** — exposure/authorization + cognitive generation events emit observability.
- **QG-8.** **Reliability→Evaluate; MRI→Disclose; Resolution-Paths presentation-only (no object); Recommendation only in Finding context.**
- **QG-9.** **Confidence = trust in understanding** — reliability-qualified, never bare, never project health/readiness/probability/score.
- **QG-10.** **Cognitive outputs are deterministically re-derivable** under a pinned baseline (within tolerance — §8/§10 gap).
- **QG-11.** **Positive and negative validation both present** for every contract; fail conditions tested as negatives.
- **QG-12.** **No new responsibility/object/engine/governance concept** introduced by an increment (classify-before-specify).

## 7. Regression Governance

- **Regression requirements:** every change **re-validates** that previously-approved **behavior, contract conformance, invariants, routing/context (e.g., Recommendation-only-in-Finding), and state behavior** still hold.
- **Behavior preservation:** approved event/recompute/governance behavior is preserved unless explicitly superseded.
- **Contract preservation:** an increment may not silently weaken a prior contract's acceptance/negatives/invariants.
- **Ownership preservation:** an increment may not move ownership between responsibilities (that requires owner-ratified architecture change).
- **Supersession rule:** approved behavior may be superseded **only** via **owner-ratified reconciliation**, **append-only** (prior retained), with **full re-validation** of the superseding behavior and its regression surface. **No silent supersession; no in-code conflict resolution.**

## 8. Cognitive Validation Model

**OSLO is not a CRUD system, and QA cannot validate the *verdict* of a cognitive output** — there is no ground-truth "correct Finding" or "best Recommendation," and Recommendations are advisory by doctrine. Therefore cognitive validation targets **well-formedness, traceability, determinism, and governance-conformance** — *the derivation, not the verdict:*

| Object | What QA validates (NOT "is it correct/best") |
|---|---|
| **Finding** | descriptive (not prescriptive); **evidence-traceable** (no opaque finding); correctly typed; **deterministically re-derivable**; governed for exposure |
| **Issue** | severity/confidence/CAF/reliability **derived from Findings** (traceable); epistemic state labeled; **deterministic**; governed |
| **Recommendation** | **advisory**; **anchored to a Finding/Issue**; **governable** (Authority exposes/authorizes); **never authorizes/executes**; alternatives = multiple recommendations; **no Resolution-Path object** — *not* "is it the right action" |
| **Clarification** | a **candidate response** (information request); **feeds reanalysis**; governed exposure; not an action |
| **Governance Decision** | a valid expose/suppress/defer/block/authorize; **append-only**; **audited**; **generates nothing** |
| **Outcome Confidence** | **reliability-qualified, never bare**; **never project health/score**; **derived from CAF**; **deterministic** |

**Core principle:** **determinism is the substitute for ground truth.** A cognitive output is "correct" for QA purposes if, under a **pinned baseline** (config × fixture × model version), it is **deterministically re-derivable, evidence-traceable, correctly governed, and invariant-compliant.** QA validates **the chain of derivation and governance**, not the truth of the conclusion. *(The acceptable determinism **tolerance** is an open calibration gap — §10.)*

## 9. QA Readiness Framework

Dimensions (0–100; **ready ≥ 85**; conditionally-ready 70–84; not-ready < 70). A capability is QA-ready when **all** dimensions ≥ 85:

| Dimension | Validates | Current |
|---|---|---|
| **Ownership readiness** | one owner per output; no orphan/duplicate | 96 |
| **Object readiness** | objects/lifecycle/states well-formed | 93 |
| **Behavior readiness** | events/recompute/governance/state defined & testable | 92 |
| **Governance readiness** | authority decisions valid, audited, generate-nothing | 92 |
| **Observability readiness** | governed objects + cognitive events observable; replay | 90 |
| **Implementation readiness** | per-increment: contract triad approved | **gated** (per wave) |

**Scoring guidance:** a dimension scores by **conformance-rule pass-rate** (QG-1…12) for the capability; Implementation readiness is **0 until** the increment's contract triad is approved (Contract Generation Plan). **Release gate = all non-implementation dimensions ≥ 85 + the increment's contract triad approved + no Critical/Major.**

## 10. Final Governance Recommendation

**Readiness assessment:** QA Governance is **defined and ratifiable**; the validation hierarchy, failure model, release gates, conformance rules, regression governance, and the cognitive-validation model are complete and consistent with the accepted foundation. Current dimension scores are at/above threshold (Ownership 96 · Object 93 · Behavior 92 · Governance 92 · Observability 90).

**Remaining gaps (challenge findings):**
- **GAP-1 (Major, carried RR-2) — determinism tolerance unset.** Cognitive validation rests on **deterministic re-derivation under a pinned baseline (QG-10/§8)**, but the **acceptable tolerance** (semantic-equivalence bounds over governable outputs) is **not yet calibrated**. *Impact:* cognitive QA cannot finalize pass/fail thresholds for Findings/Issues/Confidence until set. *Recommendation:* owner/calibration decision before cognitive-capability gates finalize; presentation/governance QA unaffected.
- **GAP-2 (Minor) — object-classification clarifications** (attributes-vs-objects; types) carried from the Object Model; resolve inline.
- **GAP-3 (Minor) — calibration/tier values** (RR-1) gate threshold tests for tier-related capabilities only.

None blocks ratification of the QA Governance **model**; GAP-1 gates **finalization of cognitive-capability pass/fail thresholds**, not the governance model itself.

**Recommended next artifact:** **`OBSERVABILITY_GOVERNANCE_SPECIFICATION_V1`** — the post-release counterpart to QA Governance, defining how runtime observation governs whether validated increments **succeed in reality** (events, audit, metrics, traces, replay, governance visibility), completing the **Architecture → Contract → QA → Observability** governance chain.

---

*This QA Governance Specification defines OSLO's canonical model for determining correctness before release — what must be validated, the release gates, regression handling, and conformance measurement — at governance level only, with no implementation, frameworks, or tooling. It situates QA Governance between Contract Governance (what each increment must do) and Observability Governance (whether it succeeds in reality), and establishes principles (behavior before implementation; contracts before testing; ownership traceability; positive-and-negative validation both required; deterministic validation; validate derivation not verdict; humans approve). It defines a five-layer dependency-ordered validation hierarchy (Object → Behavior → Governance → Contract → Regression), a four-level failure classification (Critical/Major/Minor/Informational) with release impact and escalation, an objective release-gate model (no Critical; no ownership/governance/observability violations; no orphan outputs; contract and regression conformance; invariants verified), twelve architecture-level conformance rules (QG-1…12), regression governance (preserve behavior/contracts/invariants/ownership; supersede only via owner-ratified, append-only, re-validated change), and a cognitive validation model that — recognizing OSLO is not a CRUD system and has no ground-truth verdict for Findings/Issues/Recommendations — validates well-formedness, evidence-traceability, deterministic re-derivation under a pinned baseline, and governance-conformance rather than the truth or optimality of conclusions. It provides a QA readiness framework with scored dimensions, assesses the model ratifiable with one Major carried gap (determinism tolerance, RR-2, which must be calibrated before cognitive-capability pass/fail thresholds finalize) and minor carried clarifications, and recommends the Observability Governance Specification as the next artifact to complete the Architecture → Contract → QA → Observability governance chain.*

**QA Governance Specification v1 complete.**

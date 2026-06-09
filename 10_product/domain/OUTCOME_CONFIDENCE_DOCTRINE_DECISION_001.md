# Outcome Confidence Doctrine Decision 001

**Type:** Founder Decision Document (establishes doctrine — not discovery, not calibration, not implementation)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Converts into explicit doctrine:** `OUTCOME_CONFIDENCE_DOCTRINE_DISCOVERY_V1.md` (incl. its Founder Annotation) + `CAF_CONFIDENCE_CALIBRATION_DECISION_WORKBOOK_V1.md`
**Consistent with (not modified):** CAF Assessment Model · CAF Scoring Model · Reliability Model · Confidence Model · Planning Intelligence Spec · Analysis Engine Spec.

> **Governance status.** This is the **Decision** artifact for Release 1 Outcome Confidence doctrine. It records founder-approved positions and is intended for entry into the decision log per the governance lifecycle (Backlog → Proposal → Review → **Decision** → Repository Change → Changelog). It introduces **no formula, scoring, weighting, percentage, threshold, probability model, implementation, or UI design**, resolves **no calibration question**, creates **no future architecture**, and **modifies no existing model**. It establishes **meaning, not measurement.**

---

## Section 1 — Decision Purpose

This decision exists because Release 1 cannot proceed to calibration (scales, synthesis method, scoring) until the **meaning** of Outcome Confidence is explicitly and authoritatively fixed. The Doctrine Discovery established what the repository already implies; the Calibration Workbook enumerated what remains open. This document is the founder's act of **accepting, clarifying, and making explicit** the doctrine those documents surfaced — so that engineers, product designers, and future doctrine authors share one authoritative meaning before any number is chosen.

**This document establishes meaning, not measurement.** Every measurement question (how confidence is scored, scaled, or synthesized) remains deferred to calibration (Section 12).

---

## Section 2 — Canonical Definition

**Outcome Confidence (Release 1) — canonical definition:**

> **Outcome Confidence is a measure of confidence in the integrity and trustworthiness of OSLO's current understanding of project reality.**

It distinguishes two ideas and commits to one:

- **Confidence in understanding** — how much the current understanding of project reality can be trusted. **← This is what Release 1 Outcome Confidence represents.**
- **Confidence in outcome achievement** — the likelihood that the intended outcome will be achieved. **← This is explicitly *not* what Release 1 Outcome Confidence represents.**

**Release 1 Outcome Confidence represents confidence-in-understanding.** Any outcome-achievement / likelihood construct is out of scope for Release 1 (Section 10).

*Grounding:* `CONFIDENCE_MODEL_V1.md` §2/§5; `OSLO_RELEASE_1_MASTER_SPEC.md` §21; Founder Annotation §F.1.

---

## Section 3 — What Outcome Confidence Is

Doctrine statements (Release 1):

- **Outcome Confidence is** confidence in the integrity and trustworthiness of OSLO's current understanding of project reality.
- **Outcome Confidence is** a single, summarized, **explainable** signal a person can act on.
- **Outcome Confidence is** **derived** — it consolidates the CAF assessment and qualifies it by Assessment Reliability.
- **Outcome Confidence represents** *how much we should trust what OSLO currently understands*, given the available evidence.
- **Outcome Confidence communicates**, to a project leader, the **trustworthiness of the understanding** on which decisions are being made — and, by its reliability qualifier, how well-supported that judgment is.
- **Outcome Confidence is** **always accompanied by its basis** (the CAF dimensions and the reliability that account for the signal and its last change); it is never a bare number.

---

## Section 4 — What Outcome Confidence Is Not

Doctrine statements (Release 1):

- **Outcome Confidence is not a probability.**
- **Outcome Confidence is not a prediction or forecast.**
- **Outcome Confidence is not a likelihood of outcome achievement or success.**
- **Outcome Confidence is not certainty or a guarantee.**
- **Outcome Confidence is not a risk score.**
- **Outcome Confidence is not project health or project status.**
- **Outcome Confidence is not execution status or readiness.**
- **Outcome Confidence is not document completeness or task completion.**
- **Outcome Confidence is not acceptance** (an understanding may be accepted at any confidence; high confidence is not itself acceptance).

*Grounding:* `OSLO_RELEASE_1_MASTER_SPEC.md` §21; `CONFIDENCE_MODEL_V1.md` §5; `CAF_SCORING_MODEL_V1.md` §3; `GOVERNANCE_MODEL_V1.md` §9; `ACCEPTED_UNDERSTANDING_MODEL_V1.md` §10.

---

## Section 5 — Relationship to CAF

Doctrine:

- **CAF is the primary assessment.** CAF assesses the integrity of understanding across three dimensions: Clarity, Alignment, Feasibility.
- **Confidence is a downstream summary of CAF.** It consolidates CAF; it does not perform its own independent assessment of project reality.
- **Clarity, Alignment, and Feasibility are independent and co-equal assessment targets.** No dimension depends on another; **there is no doctrinal hierarchy or ordering** among them (no Clarity→Alignment→Feasibility precedence).
- **Confidence consumes CAF; it never replaces or overrides it.** Confidence never alters a CAF dimension and never feeds back into CAF.
- **Everything upstream of CAF reaches Confidence only through CAF** (evidence, inference, findings, impact assessment).

**Ambiguity resolved.** Whether the confidence *summary* treats the three dimensions identically or distinguishes among them is a **calibration** question (deferred, Section 12). At the **doctrine** level it is fixed that: the dimensions are independent and co-equal in standing; the consolidation must respect meaningful weakness in any dimension; **no dimension may be ignored, and none may dominate the signal by default** (constrained aggregation). *Grounding:* `CONFIDENCE_MODEL_V1.md` §3/§7; `CAF_ASSESSMENT_MODEL_V1.md` §3.

---

## Section 6 — Relationship to Reliability

Doctrine:

- **Reliability qualifies confidence; it does not replace CAF.** Reliability never changes a CAF dimension's assessed strength; it changes how much of that strength is expressed in the confidence signal.
- **Reliability measures the supportability of the assessment** — how trustworthy the CAF assessment is given observable evidence — not project quality and not OSLO's quality.
- **Reliability is determined independently of CAF**, from Coverage, Evidence Availability, and Assessability; it is **not** directly determined by findings.
- **Reliability ties confidence to evidence.** Because reliability depends on the observable evidence surface, **confidence can change as evidence changes even when CAF is unchanged** — broader coverage or more available evidence can raise confidence in an unchanged understanding.
- **A high CAF assessment over a thin evidence surface yields a more cautious confidence signal** than the same assessment over a well-covered surface.

*Grounding:* `RELIABILITY_MODEL_V1.md` §2–§8; `CONFIDENCE_MODEL_V1.md` §4/§8.

---

## Section 7 — Confidence Evolution Doctrine

Doctrine:

- **Confidence changes only when CAF or Reliability changes**, and CAF/Reliability change only through new evidence, new/changed findings, or a changed evidence surface. Confidence does not drift on its own.
- **Confidence is expected to evolve.** A project's understanding matures as evidence and user action accumulate; the signal is meant to move with it, not to be set once.
- **Confidence is versioned by supersession.** Each analysis run produces a new confidence state that **supersedes** the prior; superseded states are **retained, never deleted**.
- **Confidence history is preserved and explainable.** The supersession chain *is* the confidence history; every change is attributable to a CAF change, a reliability change, or both.
- **Confidence rising** reflects strengthened understanding (findings addressed, ambiguity reduced, conflicts resolved) and/or improved reliability (broader coverage, more evidence).
- **Confidence falling** reflects weakened or newly-qualified understanding (new or worsened findings) and/or reduced reliability.

*Grounding:* `CONFIDENCE_MODEL_V1.md` §10; `RELEASE_1_DATA_MODEL_SPECIFICATION_V1.1.md` §10; `RELEASE_1_STATE_MODEL_SPECIFICATION_V1.md` §8; `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` §14.

---

## Section 8 — Deep Analysis Doctrine

**Authoritative doctrine.**

- **Why Deep Analysis can reduce confidence.** Deep Analysis enriches understanding and discovers what the fast orientation could not see — additional claims, deeper assumptions, and especially **contradictions**. Surfacing a previously-hidden finding adds a reducing contribution to a CAF dimension, which can lower confidence. The conflict was already present; Deep Analysis merely made it visible.
- **Why this is not a failure.** A confidence drop after Deep Analysis means OSLO now understands the project **more truthfully**, not that the project got worse or that OSLO performed poorly. **Deep Analysis improves understanding; it does not manufacture certainty.** A lower-but-better-supported signal is a *more honest* signal — and Deep Analysis typically raises reliability even when the headline level falls.
- **What users should understand when this occurs.** A post-Deep decrease is a signal that **real issues were found that were worth finding** — it is the system earning trust by surfacing problems early, not losing trust. The right response is to act on the newly-surfaced findings and recommendations, not to distrust the analysis.
- **Confidence is not monotonic in project quality.** Because confidence tracks understanding integrity and supportability — *not* project quality — **confidence may fall while the project plan itself is improving.** This is expected and correct.

*Grounding:* `PLANNING_INTELLIGENCE_SPECIFICATION_V1.md` §14/§17; `RELEASE_1_ANALYSIS_ENGINE_SPECIFICATION_V1.md` §10; `CAF_SCORING_MODEL_V1.md` §4; Doctrine Discovery Q10/Q17/Q18.

---

## Section 9 — Representation Doctrine

**Conflict addressed (Doctrine Discovery contradiction C-A):** the repository asserts confidence "is not a probability" yet represents it as a bounded numeric signal, and `OSLO_CAPABILITY_MATRIX_V2.md` §22 g15 flags that nothing prevents users from reading it as one.

**Doctrine-level resolution (no formulas, no thresholds, no UI design):**

- **Outcome Confidence is a qualitative-first signal.** Its primary expression is a **state band** (a qualitative level) **always paired with its reliability qualifier**. A confidence signal is never presented as a level alone.
- **Any numeric index is subordinate and supportive, never primary, and never a percentage or probability.** A bare number is not a complete confidence signal — consistent with the CAF representation triple *(index, band, reliability)*, where "a bare number is never a complete CAF score."
- **Outcome Confidence must never be presented or labeled as a probability, likelihood, percentage chance, or odds of success.** Presentation that invites a probabilistic reading is doctrinally prohibited in Release 1.
- **Every confidence signal is presented with its basis.** The user must be able to see *why* the signal sits where it does (CAF dimensions + reliability) and *what last changed it*.
- **Confidence band vocabulary is to be unified** on a single canonical set (the Master Spec / Data Model band vocabulary: Very Low, Low, Moderate, High, Very High), to remove the label inconsistency noted in Doctrine Discovery (C-B). *(This is a terminology-unification doctrine decision; the actual reconciliation of any model example text that uses "Medium" is referred to governance, not performed here.)*

*This section gives doctrine-level guidance only. The band boundaries, the index range, and how the UI renders any of this are calibration/implementation, deferred.*

---

## Section 10 — Future Evolution Boundary

**Founder intent recorded:**

- **Release 1 Outcome Confidence remains confidence-in-understanding** and is not presented as probability.
- **Future versions of OSLO may gain access** to execution, resource, financial, market/competitive, compliance/regulatory, customer-adoption, operational, and external-environmental evidence sources.
- **Future probabilistic outcome-achievement models may become possible** once such evidence exists.

Two future directions were tabled:

- **Option A — Separate Signals.** Outcome Confidence remains confidence-in-understanding; a distinct future **Outcome Probability** signal represents likelihood of outcome achievement.
- **Option B — Expanded Outcome Confidence.** Outcome Confidence broadens over time into a combined understanding-plus-likelihood construct.

**Recommendation: Option A (separate signals).**

**Rationale.** (1) **Conceptual clarity** — the entire existing doctrine is built on confidence meaning *trust in understanding*; Option B would gradually redefine an established term, creating ambiguity about what any historical or current confidence value meant. (2) **Non-disruption** — Option A adds a new signal without altering the meaning, history, or behavior of the existing one; Option B mutates a canonical concept and would force re-interpretation of prior confidence states. (3) **Honest separation** — understanding quality and outcome likelihood are genuinely different questions (the repository already separates *understanding* from *outcome*); keeping them as separate signals preserves that honesty. (4) **Governed evolution** — Option A is additive and reviewable in isolation; Option B "changes the meaning currently established in the repository" and would require a heavier doctrinal rewrite.

**Boundary decision.** Any outcome-achievement / probabilistic construct (including the term **Outcome Probability**) is a **separate future architectural and doctrinal decision**. It is **out of scope for Release 1**, must **not alter Release 1 behavior**, and the term **Outcome Probability is not adopted into Release 1 canonical terminology** (recorded as future-only). *Grounding:* Founder Annotation §F.2/§F.3.

---

## Section 11 — Founder Decisions

| # | Doctrine area | Approved position | Reasoning |
|---|---|---|---|
| D1 | **Meaning** | Outcome Confidence = confidence in the integrity/trustworthiness of current understanding of project reality (confidence-in-understanding) | Consistent across Confidence Model, Master Spec, founder intent |
| D2 | **Scope commitment** | Release 1 represents confidence-in-understanding, **not** outcome achievement | Release 1 evidence is planning-domain only |
| D3 | **Exclusions** | Not probability/prediction/certainty/risk/health/readiness/completeness/acceptance | Repeated explicit exclusions; preserves epistemology |
| D4 | **CAF primacy** | CAF is primary; Confidence is a downstream summary that consumes, never replaces, CAF | Confidence Model §3 |
| D5 | **Dimension standing** | Clarity, Alignment, Feasibility are independent and **co-equal**; no doctrinal ordering | CAF Assessment §3; no repository evidence for hierarchy |
| D6 | **Aggregation principle** | Constrained aggregation: no dimension ignored, none dominant by default; weakness must be felt | Confidence Model §7 |
| D7 | **Reliability role** | Reliability **qualifies** confidence; never replaces CAF; determined from coverage/evidence/assessability, not findings | Reliability Model; Confidence Model §4 |
| D8 | **Evidence linkage** | Confidence can change on reliability alone as evidence/coverage change, with CAF unchanged | Confidence Model §8 |
| D9 | **Evolution** | Confidence is expected to evolve; versioned by supersession; history retained | Confidence Model §10; Data/State models |
| D10 | **Deep Analysis** | A Deep-Analysis confidence drop is honest improvement of understanding, **not a failure**; confidence may fall while the plan improves | Planning Intelligence §17; CAF Scoring §4 |
| D11 | **Representation** | Qualitative-first (band + reliability qualifier), basis always shown; numeric index subordinate; **never presented as probability/percentage** | Resolves C-A at doctrine level |
| D12 | **Band vocabulary** | Unify confidence bands on Very Low / Low / Moderate / High / Very High | Resolves C-B label inconsistency |
| D13 | **Future boundary** | Release 1 stays confidence-in-understanding; outcome-achievement is a separate future decision | Founder Annotation |
| D14 | **Future direction** | **Option A** (separate future *Outcome Probability* signal) recommended over Option B | Conceptual clarity + non-disruption + governed evolution |
| D15 | **Future terminology** | "Outcome Probability" is future-only; **not** adopted into Release 1 terminology | Prevents premature terminology drift |

### Conflicts identified and resolved
- **C-A (meaning vs representation).** *Conflict:* "not a probability" vs a bounded numeric signal readable as one. *Resolution:* D11 — qualitative-first, reliability-qualified, basis-accompanied, probability-presentation prohibited (doctrine). *Residual:* the *operationalization* (how the UI enforces this) is implementation, deferred.
- **C-B (label inconsistency).** *Conflict:* Reliability uses High/Moderate/Low; Confidence/CAF use Very Low…Very High; a stray "Medium" appears in Confidence Model examples. *Resolution:* D12 — unify confidence bands on the five-band set; refer model-text reconciliation to governance (not edited here).
- **Founder intent vs repository:** *no conflict found.* Founder intent (R1 = understanding; future may expand) is consistent with the repository; it makes the implicit explicit and adds a governed future boundary.

---

## Section 12 — Implications for Calibration

**Doctrine decisions resolved here (meaning fixed):**
- The **meaning** of Outcome Confidence and its exclusions (D1–D3).
- CAF primacy, dimension independence/co-equal standing, constrained-aggregation principle (D4–D6).
- Reliability's qualifying role and evidence linkage (D7–D8).
- Evolution/supersession doctrine (D9).
- Deep-Analysis-can-reduce-confidence-and-that-is-not-failure (D10).
- Representation **principles** and band **vocabulary** (D11–D12).
- Future boundary + direction (D13–D15).

**Calibration decisions still deferred (measurement — unchanged by this doctrine):**
- **CAL-CONF-1** — the CAF+Reliability → Confidence **synthesis method** (formula-free realization). *Meaning fixed; method open.*
- **CAL-CAF-2 / CAL-REL-1 / CAL-CONF-2** — the **scales/band boundaries** for CAF, Reliability, Confidence. *Vocabulary fixed (D12); boundary values open.*
- **CAL-REL-2** — the qualitative policy by which Coverage/Evidence/Assessability determine a reliability level.
- **CAL-CONF-3/4/5** — the specific quantitative reaction of confidence to ambiguity/assumptions/conflicts. *Direction fixed (reducing via CAF); magnitudes open.*
- **CAL-CAF-3** — finding-type → dimension-impact assignment magnitudes.
- **CAL-SEV-1/2/3** — severity basis/escalation/visibility.
- **CAL-DET-1/3** — determinism tolerance / acceptable variation.
- **CAL-FD-1…5** — Fast/Deep scope, deferral, recompute cadence.
- **Representation operationalization** (C-A residual) — how the UI prevents probabilistic misreading (implementation).

This doctrine **unblocks** calibration by fixing meaning; it **does not** answer any calibration item.

---

## Section 13 — Final Doctrine Summary

Concise statements, suitable for later promotion into a canonical doctrine repository (Release 1):

1. Outcome Confidence measures trust in OSLO's current understanding of project reality.
2. Outcome Confidence is confidence in understanding, not confidence in outcome achievement.
3. Outcome Confidence is not a probability, prediction, certainty, risk score, project health, readiness, or acceptance.
4. Outcome Confidence is derived from CAF and Reliability — and from nothing else.
5. CAF is the primary assessment; Confidence summarizes CAF and never replaces or overrides it.
6. Clarity, Alignment, and Feasibility are independent and co-equal; no dimension ranks above another.
7. The confidence summary must respect meaningful weakness in any dimension: none ignored, none dominant by default.
8. Reliability qualifies confidence; it never alters a CAF dimension.
9. Reliability measures supportability of the assessment, determined from coverage, evidence availability, and assessability — not from findings.
10. Confidence can change as evidence changes even when understanding is unchanged.
11. Confidence is expected to evolve; each value supersedes the prior, and history is preserved.
12. Confidence may decrease as understanding improves — a more honest signal, not a failure.
13. Deep Analysis improves understanding, not certainty; a post-Deep confidence drop means real issues were surfaced.
14. Outcome Confidence is qualitative-first, always shown with its reliability qualifier and its basis, and never presented as a probability or percentage.
15. Release 1 Outcome Confidence remains confidence-in-understanding; any future outcome-achievement signal is a separate, governed decision (Option A), and "Outcome Probability" is future-only terminology.

---

*This document establishes Release 1 Outcome Confidence doctrine (meaning), defers all measurement to calibration, introduces no formulas/scores/weights/thresholds/probability/UI, creates no future architecture, and modifies no existing model. Recorded as the Decision artifact pending entry into the decision log under the governance lifecycle.*

**Outcome Confidence Doctrine Decision 001 complete.**

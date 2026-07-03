# Outcome Confidence Calibration Decision 001

**Type:** Founder Calibration-Decision Document (settles calibration **principles** — not arithmetic)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Follows / consistent with (authoritative, not modified):** `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_DOCTRINE_DISCOVERY_V1.md` · `CAF_CONFIDENCE_CALIBRATION_DECISION_WORKBOOK_V1.md`
**Models consumed (not modified):** CAF Assessment · CAF Scoring · Reliability · Confidence · Planning Intelligence · Analysis Engine.
**Revision:** 2026-05-31 — targeted governance-safe revision applied (approved patch set): added **Calibration Invariants** (P-1), **determinism provenance notes** (P-4), and an **Understanding-Stability boundary note** (P-5). CAL-CAF-1 and CAL-REL-1 unchanged (rejected). No founder decision reopened. See `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001_GOVERNANCE_REVIEW.md`.

> **What this document is.** Meaning is already settled (Decision 001 / Interpretation 001 / Leadership 001). This document settles the **calibration principles** future models and implementations must obey. It establishes **which existing principle governs** each open calibration item; it does **not** create formulas, equations, weights, percentages, thresholds, scoring algorithms, or code, and it introduces **no** probability, outcome prediction, governance, or future architecture. Concrete numeric values (ranges, boundaries, tolerances) are deferred to the future v2 models (Deliverable 5).
>
> **Binding doctrine (all calibration must conform).** Outcome Confidence communicates **trust in OSLO's current understanding of project reality**. It is **not** probability, prediction, project health, readiness, certainty, or outcome likelihood. **No calibration may violate this.**
>
> **Status note.** Positions below are **recommended founder decisions**, captured for ratification under the governance lifecycle; AI does not self-ratify.

---

## Deliverable 1 — Calibration Decision Analysis

*Per item: question · repository evidence · doctrine constraints · recommended decision (principle) · risks · alternatives considered. No arithmetic is specified.*

### CAL-CAF-1 — Equal vs differentiated treatment of Clarity/Alignment/Feasibility
- **Question.** Are the three dimensions treated alike or distinctly in the confidence summary?
- **Evidence.** CAF Assessment §3 (dimensions independent, co-equal); Confidence Model §7 (constrained aggregation: none ignored, none dominant by default).
- **Doctrine constraints.** No hierarchy/ordering (Decision 001 D5); no weights permitted.
- **Recommended decision.** **Equal in standing** — no dimension is privileged or weighted — **with contextual expression via constrained aggregation** (a weak dimension constrains the signal; it is not averaged away). I.e., *equal importance, contextual effect.*
- **Risks.** Misreading "equal" as "simple average." Mitigation: pair with the constrained-aggregation principle (CAL-CONF-1).
- **Alternatives.** (B) Differentiated weighting — **rejected** (introduces weights/hierarchy, violates independence). (C) Contextual weighting — **subsumed**: contextual *effect* is already delivered by constrained aggregation without changing standing.

### CAL-CAF-2 — CAF assessed-level scale
- **Question.** How is each dimension's level expressed?
- **Evidence.** CAF Scoring §3 (representation triple: index + band + reliability; bands Very Low…Very High).
- **Doctrine constraints.** Qualitative-first; index never a probability/percentage (Decision 001 D11).
- **Recommended decision.** Adopt the **representation form** — qualitative **state band** (Very Low/Low/Moderate/High/Very High) as primary, with any index subordinate and always reliability-qualified. **Numeric range/boundaries deferred to CAF Scoring v2.**
- **Risks.** Boundary values undefined until v2. Acceptable (form fixed, values deferred).
- **Alternatives.** A bare numeric scale — rejected (violates qualitative-first).

### CAL-CAF-3 — Finding-type → dimension-impact assignment basis
- **Question.** Which findings move which dimensions, and how strongly?
- **Evidence.** CAF Scoring §4/§5 (locality + magnitude governed by the finding's **Impact Assessment**, never by finding type).
- **Doctrine constraints.** Findings reach confidence only through CAF; type is a label, not a coefficient.
- **Recommended decision.** **Assignment and magnitude are governed by each finding's Impact Assessment** (significance, affected dimensions, evidence support, scope) — **not** by finding type. Adopt as principle; **magnitudes deferred** to CAF Scoring v2.
- **Risks.** Requires Impact Assessment to be well-defined operationally (v2).
- **Alternatives.** Type-coefficient mapping — rejected (contradicts CAF Scoring §4).

### CAL-REL-1 — Reliability scale definition
- **Question.** Levels/labels for reliability.
- **Evidence.** Reliability Model (qualitative High/Moderate/Low usage); §12 (numeric expression = calibration).
- **Doctrine constraints.** Reliability is a qualifier, distinct from CAF/confidence bands.
- **Recommended decision.** Adopt **qualitative reliability levels (High / Moderate / Low)** as the form; reliability remains a **qualifier** carried alongside confidence, not a band of its own. **Boundaries deferred** to Reliability v2.
- **Risks.** Label-set difference vs 5 confidence bands. Mitigation: reliability is explicitly a *qualifier*, so a different granularity is acceptable and intended.
- **Alternatives.** Mirror the 5-band set — rejected (over-precises a qualifier).

### CAL-REL-2 — How Coverage/Evidence Availability/Assessability determine a reliability level
- **Question.** The (non-arithmetic) determination policy.
- **Evidence.** Reliability Model §6–§9 (three inputs; assessability gates; determined independently of CAF/findings).
- **Doctrine constraints.** No formula; reliability not influenced by findings.
- **Recommended decision.** Adopt the **principle**: all three inputs are considered, **none ignored**; **low assessability constrains reliability regardless** of coverage/evidence; reliability is read from the evidence-surface conditions, not from findings. **Combination arithmetic deferred** to Reliability v2.
- **Risks.** Qualitative policy may need examples for consistency (v2).
- **Alternatives.** Single-input proxy (e.g., coverage only) — rejected (Reliability Model fixes three inputs).

### CAL-REL-3 — Reliability display/visibility
- **Question.** How/where reliability is shown.
- **Evidence.** CAF Scoring §3; Representation doctrine (Decision 001 D11); Interpretation §8.
- **Doctrine constraints.** Confidence never shown bare; basis always available.
- **Recommended decision.** Adopt the principle: **reliability is always presented together with confidence** (a confidence state is never displayed without its reliability qualifier). **UI specifics deferred** (implementation, not calibration).
- **Risks.** None at doctrine level.
- **Alternatives.** Reliability hidden/secondary — rejected (violates always-paired principle).

### CAL-REL-4 — How reliability qualifies confidence
- **Question.** The qualification policy (no weights).
- **Evidence.** Reliability Model §4; Confidence Model §4/§8.
- **Doctrine constraints.** Qualifies, never replaces; can move confidence with CAF unchanged.
- **Recommended decision.** Adopt: reliability **qualifies the expression of CAF strength** — low reliability *holds the signal back*, high reliability *lets it express more fully* — and **never alters a CAF dimension**. Confidence may move on reliability alone. **Degree deferred** to Confidence v2.
- **Risks.** Degree undefined until v2.
- **Alternatives.** Reliability as an additive term/weight — rejected (would make it a co-score, not a qualifier).

### CAL-CONF-1 — CAF + Reliability → Confidence synthesis method
- **Question.** How CAF and reliability conceptually synthesize.
- **Evidence.** Confidence Model §6 (consolidate-then-qualify), §7 (constrained aggregation: between an average and a minimum; no simple averaging; no weakest-link domination).
- **Doctrine constraints.** No formula; meaning fixed (Decision 001 §5/§6).
- **Recommended decision.** Adopt **"consolidate-then-qualify via constrained aggregation"** as the synthesis principle: (1) consolidate the three CAF dimensions into one understanding-strength signal that **reflects strengths, materially reflects weaknesses, and lives between an average and a minimum** (no dimension ignored or dominant by default); (2) **qualify** that consolidated strength by reliability. **The arithmetic realization is deferred to Confidence Model v2.**
- **Risks.** "Between an average and a minimum" must be realized carefully in v2 to avoid implicit weighting. Mitigation: v2 must preserve §7 properties.
- **Alternatives.** Simple average — rejected (lets strength offset weakness). Weakest-link/minimum — rejected (collapses to one dimension). Weighted sum — rejected (introduces weights/hierarchy).

### CAL-CONF-2 — Confidence band set / mapping to states
- **Question.** Bands and their mapping.
- **Evidence.** CAF Scoring §3; Master Spec §3; Decision 001 D12.
- **Doctrine constraints.** Unify on one vocabulary; never a probability.
- **Recommended decision.** Adopt **five bands — Very Low / Low / Moderate / High / Very High** — as the canonical confidence-state vocabulary, mapped to OSLO's confidence states. **Boundaries deferred.**
- **Risks.** Stray "Medium" wording in some example text (C-B) needs reconciliation (governance, not here).
- **Alternatives.** 3-band or numeric-only — rejected (3 loses resolution; numeric-only violates qualitative-first).

### CAL-CONF-3 — What reduces confidence
- **Question.** Conditions that lower the signal.
- **Evidence.** CAF Scoring §4 (finding presence reduces integrity); Reliability Model §7–§9 (thin coverage/evidence/assessability).
- **Doctrine constraints.** Direction only; via CAF/Reliability.
- **Recommended decision.** Adopt the **direction principle**: confidence falls when CAF strength falls (new/worsened findings via their Impact Assessment) and/or reliability falls (reduced coverage/evidence/assessability). **Magnitudes deferred.**
- **Risks.** None at principle level.
- **Alternatives.** Direct finding→confidence reduction — rejected (must route through CAF).

### CAL-CONF-4 — What increases confidence
- **Question.** Conditions that raise the signal.
- **Evidence.** CAF Scoring §4 (resolution withdraws reducing contribution); Confidence Model §8 (reliability can raise on its own).
- **Recommended decision.** Adopt: confidence rises when CAF strengthens (findings addressed; ambiguity/assumption/conflict resolved) and/or reliability rises (broader coverage, more evidence). **Magnitudes deferred.**
- **Risks.** None at principle level.
- **Alternatives.** Confidence rises only with CAF — rejected (reliability-alone rise is doctrine, Confidence Model §8).

### CAL-CONF-5 — Reaction to ambiguity / assumptions / conflicts
- **Question.** How each class influences the summary.
- **Evidence.** Planning Intelligence §12–§14 (ambiguity→Clarity; assumptions→underpinned dimension; conflict→Alignment); CAF Scoring §4 (magnitude via Impact Assessment).
- **Recommended decision.** Adopt: each acts **through CAF on its affected dimension(s)**, with magnitude from its Impact Assessment — **not** equally and **not** by type. Same channel, different dimensions/magnitudes; **no direct reliability effect**. **Magnitudes deferred.**
- **Risks.** None at principle level.
- **Alternatives.** Uniform reaction by type — rejected (CAF Scoring §4).

### CAL-SEV-1 — Severity assignment basis
- **Question.** What makes a finding Warning / Moderate / Critical.
- **Evidence.** Finding Model / CAF Scoring §5 (Impact Assessment: significance, scope).
- **Doctrine constraints.** No score/threshold; descriptive.
- **Recommended decision.** Adopt: **severity expresses the significance and scope of a finding's impact on understanding integrity, qualitatively** — Critical = severe/pervasive impact on understanding; Moderate = meaningful but bounded; Warning = minor/localized. **It is a meaning, not a score; thresholds deferred.**
- **Risks.** Consistency needs examples (v2).
- **Alternatives.** Type-based severity — rejected (severity is impact-based, not type-based).

### CAL-SEV-2 — Severity escalation/change basis
- **Question.** Does severity change over runs/supersession?
- **Evidence.** CAF Scoring §5 (re-assessing impact changes effect without the finding changing); supersession doctrine.
- **Recommended decision.** Adopt: **severity may change only when a finding's Impact Assessment changes** (e.g., new evidence alters significance/scope), never on a timer; changes follow supersession (history retained). **No escalation formula.**
- **Risks.** None at principle level.
- **Alternatives.** Time-based escalation — rejected (not event-driven).

### CAL-SEV-3 — Severity visibility / surfacing
- **Question.** How severity surfaces; what is "top."
- **Evidence.** UI Spec §7/§9 (top findings by severity); Interpretation/Leadership (meaning only).
- **Recommended decision.** Adopt: **severity orders attention** — higher-severity findings surface first ("top") — as a **meaning/ordering principle**; exact surfacing rules are UI/implementation, deferred.
- **Risks.** None at doctrine level.
- **Alternatives.** Flat presentation — rejected (loses the attention signal severity exists to provide).

> **Provenance note (P-4).** CAL-DET-1…CAL-DET-5 are **implementation-derived** — the governable-output set, the replay/reconstruction contract, and the bounded-equivalence framing originate in the **Analysis Engine Specification §15/§16** and **Testing Strategy §6/§15**. The underlying *principle* (Outcome Confidence must be deterministic with respect to understanding) is **doctrine-aligned**. Content is retained unchanged; this note only distinguishes origin (doctrine-derived vs implementation-derived).

### CAL-DET-1 — Bounded-equivalence tolerance (governable outputs)
- **Question.** What must match for "same input = same output."
- **Evidence.** Engine §15 (bounded equivalence over governable outputs); Testing §6.
- **Doctrine constraints.** Deterministic w.r.t. understanding under pinned config.
- **Recommended decision.** Adopt the principle: **bounded equivalence is defined over the governable outputs** — the **finding-type set, recommendation set, confidence band, and reliability qualifier** must be equivalent for the same inputs and pinned configuration. **The tolerance value is deferred** to the determinism calibration (Testing/Engine v-next).
- **Risks.** Value undefined blocks numeric test pass/fail (tracked).
- **Alternatives.** Bit-exact equality — rejected (infeasible for LLM-bearing stages); free variation — rejected (breaks determinism).

### CAL-DET-2 — Replayability expectations
- **Question.** What must reconstruct exactly.
- **Evidence.** Engine §16; Testing §7; State/Event models (supersession, append-only log).
- **Recommended decision.** Adopt: **replay of the event log must reconstruct persisted state exactly** (runs, CAF/confidence states, finding/recommendation statuses and their supersession chains), with external side effects suppressed. Replay is **exact reconstruction**, distinct from live re-execution (CAL-DET-1).
- **Risks.** None at principle level.
- **Alternatives.** Approximate replay — rejected (undermines audit/history).

### CAL-DET-3 — Acceptable variation (semantic vs bit-exact)
- **Question.** Nature of permitted variation.
- **Evidence.** Engine §15.
- **Recommended decision.** Adopt **bounded semantic equivalence** (not bit-exact): incidental phrasing may differ, but the **governable outputs (per CAL-DET-1) must be equivalent** under pinned config. **Tolerance band deferred.**
- **Risks.** Requires a defined tolerance (DET-1).
- **Alternatives.** Bit-exact — rejected.

### CAL-DET-4 — Model-version change policy vs determinism
- **Question.** How config/model changes interact with determinism.
- **Evidence.** Engine §15 (configuration recorded per run; pinned config).
- **Recommended decision.** Adopt: determinism is guaranteed **only within a pinned model configuration**; a **model-version change establishes a new determinism baseline** and is **not** itself a regression. Each run records its configuration so changes are attributable. **Re-baseline procedure deferred to ops.**
- **Risks.** Requires disciplined config pinning/recording.
- **Alternatives.** Cross-version determinism — rejected (infeasible).

### CAL-DET-5 — Regression-testing expectations
- **Question.** What is a determinism regression.
- **Evidence.** Testing §6/§15.
- **Recommended decision.** Adopt: a **determinism regression** = a change in governable outputs, **under the same pinned configuration**, beyond the bounded-equivalence tolerance. Determinism is a **release gate**; cross-version changes are baseline updates, not regressions. **Tolerance value deferred (DET-1).**
- **Risks.** Gate depends on the deferred tolerance.
- **Alternatives.** Treat any change as regression — rejected (would fail on legitimate version updates).

---

## Deliverable 2 — Recommended Calibration Doctrine

### CAF Treatment
**Recommendation: A — Equally (co-equal standing), with contextual *expression* via constrained aggregation.** Clarity, Alignment, and Feasibility carry **equal standing** — none is weighted, ranked, or privileged — consistent with their independence (CAF Assessment §3). Their *effect* on the confidence signal is **contextual**: a materially weak dimension constrains the signal (it is not averaged away), and no dimension dominates by default (Confidence Model §7). This is *equal importance, contextual effect* — **no formulas, weights, or percentages**.

### Reliability Treatment
**Operationally, Reliability means the supportability of the CAF assessment** given the observable evidence surface — read from **Coverage, Evidence Availability, and Assessability**, independently of CAF and of findings (Reliability Model §6). **Reliability qualifies confidence** by governing **how fully the consolidated CAF strength is expressed**: low reliability holds the signal back; high reliability lets it express more fully; reliability **never alters a CAF dimension** and can move confidence even when CAF is unchanged. Low assessability constrains reliability regardless of the other two. **No arithmetic, no scoring** — a qualification principle only.

### Confidence Synthesis
**CAF and Reliability synthesize by consolidate-then-qualify:** first **consolidate** the three co-equal CAF dimensions into a single understanding-strength signal that reflects strengths and weaknesses and sits **between an average and a minimum** (no simple averaging, no weakest-link domination, none ignored, none dominant by default); then **qualify** that consolidated strength by reliability. The result is the summarized Outcome Confidence signal. **This is the conceptual method; the arithmetic realization is for Confidence Model v2 and must preserve these properties.** No formulas/percentages/calculations here.

### Severity Doctrine
**Severity expresses, qualitatively, the significance and scope of a finding's impact on understanding integrity** (drawn from its Impact Assessment, CAF Scoring §5):
- **Critical** — severe and/or pervasive impact on the understanding.
- **Moderate** — meaningful but bounded impact.
- **Warning** — minor and/or localized impact.

Severity is **a meaning, not a score**; it changes only when a finding's Impact Assessment changes; it **orders attention** (which findings surface first). **No thresholds, no scoring.**

### Determinism Doctrine
**"Same input = same output" means bounded *semantic* equivalence over governable outputs under a pinned model configuration** — the finding-type set, recommendation set, confidence band, and reliability qualifier must be equivalent (not bit-exact) for identical inputs. **Replayability** means the event log reconstructs persisted state **exactly** (distinct from live re-execution). **Model-version changes** establish a **new baseline**, not a regression. A **regression** is a governable-output change under the *same* configuration beyond tolerance. **Principles only; the tolerance value and procedures are deferred to implementation.**

> **Provenance note (P-4).** The determinism *principle* (deterministic with respect to understanding) is **doctrine-aligned**; the **governable-output set**, the **replay/reconstruction** contract, and the **bounded-equivalence** framing are **implementation-derived** from the **Analysis Engine Specification §15/§16** and **Testing Strategy §6/§15**. Distinguished here for provenance; content unchanged.

### Calibration Invariants  〔added per approved P-1〕

These are **invariants**, not new decisions, scores, or dimensions — they make explicit constraints already implied throughout the doctrine stack. Every future model and implementation (including Confidence Model v2) must preserve them.

**Confidence Stability Invariant.** Outcome Confidence may not change unless **CAF changes** or **Reliability changes**. Confidence has **no independent source of movement**. *(Invariant, not a formula. Grounding: Confidence Model §10; no-change → no-recompute, Event Model §15 / Engine §14.)*

**Explainability / Attribution Invariant.** Every confidence state must remain explainable through **CAF, Reliability, Findings, Recommendation history, and Confidence supersession history**. Confidence **may never become an opaque signal**. *(Invariant, not a UI requirement. Grounding: Confidence Model §10; CAF Scoring §3.)*

**Reliability Non-Collapse Invariant.** Reliability **qualifies** confidence; it **does not independently replace CAF**. Low Reliability **may constrain** confidence expression, but Low Reliability **alone must not automatically collapse** confidence to the lowest state. *(Invariant, not a scoring rule. Grounding: Confidence Model §8, Example B — High CAF + Low Reliability → Moderate, not the floor.)*

> **Boundary note — Understanding Stability (per approved P-5).** "Stable vs stabilizing understanding" is recognized by **Leadership Doctrine §9 as an interpretive concept only**. Stability **currently remains interpretation-only**; it is **not part of Outcome Confidence calibration**. No `CAL-CONF-6`, and **no stability model, metric, or signal** is introduced. **Future doctrine would be required** before stability could become a calibrated construct. *(This is the interpretive volatility/stability concept; it is distinct from the **Confidence Stability Invariant** above, which is the grounded behavioral rule that confidence does not move without a CAF or reliability change.)*

---

## Deliverable 3 — Founder Decision Matrix

| Decision | Recommended choice | Reasoning | Impact |
|---|---|---|---|
| CAL-CAF-1 | Equal standing + constrained-aggregation effect | Independence + no-weights doctrine | Confidence synthesis, CAF UX |
| CAL-CAF-2 | Qualitative band form; range deferred | Qualitative-first (D11) | CAF Scoring v2, UI |
| CAL-CAF-3 | Impact-Assessment-governed; not type | CAF Scoring §4/§5 | CAF Scoring v2 |
| CAL-REL-1 | Qualitative High/Moderate/Low qualifier | Reliability Model usage | Reliability v2, UI |
| CAL-REL-2 | All three inputs; assessability gates; no formula | Reliability Model §6–§9 | Reliability v2 |
| CAL-REL-3 | Always shown with confidence | Representation doctrine | UI |
| CAL-REL-4 | Qualifies expression; never replaces | Reliability/Confidence models | Confidence v2 |
| CAL-CONF-1 | Consolidate-then-qualify via constrained aggregation | Confidence Model §6/§7 | Confidence v2 (critical) |
| CAL-CONF-2 | Five bands (Very Low…Very High); boundaries deferred | D12 | Confidence v2, UI, Tests |
| CAL-CONF-3 | Direction: falls on CAF/reliability decline | CAF Scoring §4; Reliability §7–§9 | Confidence v2 |
| CAL-CONF-4 | Direction: rises on CAF/reliability gain | CAF Scoring §4; Confidence §8 | Confidence v2 |
| CAL-CONF-5 | Via CAF on affected dimension; not by type | Planning Intel §12–§14 | Confidence v2 |
| CAL-SEV-1 | Qualitative significance/scope of impact | CAF Scoring §5 | CAF Scoring v2, UI, Tests |
| CAL-SEV-2 | Changes only on Impact-Assessment change | CAF Scoring §5; supersession | Engine, UI |
| CAL-SEV-3 | Orders attention (top findings) | UI Spec §7/§9 | UI |
| CAL-DET-1 | Bounded equivalence over governable outputs; tolerance deferred | Engine §15 | Tests (gate), Engine |
| CAL-DET-2 | Exact state reconstruction on replay | Engine §16 | Tests, Engine |
| CAL-DET-3 | Bounded semantic (not bit-exact) | Engine §15 | Tests, Engine |
| CAL-DET-4 | Per-config; version change = new baseline | Engine §15 | Ops, Tests |
| CAL-DET-5 | Regression = same-config governable-output change beyond tolerance | Testing §6/§15 | Tests (gate) |
| **INV-1** Confidence Stability *(invariant)* | Confidence moves only on CAF or Reliability change; no independent movement | Confidence §10; no-change→no-recompute | Confidence v2, Tests |
| **INV-2** Explainability/Attribution *(invariant)* | Every state explainable via CAF/Reliability/Findings/Recommendation history/supersession; never opaque | Confidence §10; CAF Scoring §3 | Confidence v2, UI, Tests |
| **INV-3** Reliability Non-Collapse *(invariant)* | Low reliability may constrain, must not alone collapse to lowest state | Confidence §8 (Example B) | Confidence v2 |

*All decision entries are recommended founder decisions pending ratification. INV-1…INV-3 are **invariants** (constraints already implied by the doctrine stack), not new decisions, scores, or calibration dimensions.*

---

## Deliverable 4 — Calibration Dependency Map

Which decisions must be finalized before each downstream artifact:

- **Confidence Model v2** ← **CAL-CONF-1** (synthesis), CAL-CONF-2 (bands), CAL-CAF-1 (treatment), CAL-REL-1/2/4 (reliability role + determination), CAL-CONF-3/4/5 (reaction direction). *Blocking core.*
- **CAF Scoring implementation (v2)** ← CAL-CAF-2 (scale), CAL-CAF-3 (assignment), CAL-SEV-1/2 (severity), CAL-REL-2 (coverage→reliability qualifier).
- **Analysis Engine implementation** ← all of the above **plus** CAL-DET-1/2/3/4 (determinism + replay + version policy). *(Fast/Deep scope items CAL-FD-* live in the Fast-pass workbook, out of this document's set.)*
- **Testing Strategy implementation** ← CAL-DET-1/3/5 (tolerance + regression gate), CAL-CONF-1/2 (to assert behavior/bands), CAL-SEV-1 (severity tests).

**Critical chain:** CAL-CONF-1 → Confidence Model v2 → Analysis Engine confidence stage → Testing determinism/behavior gates. Resolve **CAL-CONF-1, CAL-CAF-1, CAL-REL-1/2, CAL-CONF-2, and CAL-DET-1/3** first.

---

## Deliverable 5 — Implementation Guidance

Recommended future artifacts to create **after** this calibration doctrine is ratified (not created here):

1. **Confidence Model v2** — realizes the consolidate-then-qualify synthesis and band boundaries, **preserving** the constrained-aggregation properties (CAL-CONF-1/2; CAL-CAF-1; CAL-REL-4). *Highest priority — critical chain.*
2. **CAF Scoring Model v2** — realizes the CAF index scale, Impact-Assessment-driven assignment/magnitude, and severity expression (CAL-CAF-2/3; CAL-SEV-1/2).
3. **Reliability Model v2** — realizes the reliability level scale and the (non-formula) determination policy from Coverage/Evidence/Assessability (CAL-REL-1/2). *Create only if v2 calibration requires more than the current model states; otherwise a calibration appendix may suffice.*
4. **Determinism Calibration note (Engine/Testing)** — fixes the bounded-equivalence tolerance and regression-gate definition (CAL-DET-1/3/5).

Each v2 artifact **must obey this calibration doctrine and the upstream meaning doctrine**; none may redefine meaning, introduce probability, or alter the confidence-in-understanding definition. **Do not create these here.**

---

*This document settles Release 1 Outcome Confidence calibration **principles**, conforms to the settled meaning doctrine, and defers all numeric calibration to future v2 artifacts. It introduces no formulas, weights, percentages, thresholds, scoring, probability, governance, or future architecture, and modifies no model. Recorded as the calibration-decision artifact pending ratification under the governance lifecycle.*

**Outcome Confidence Calibration Decision 001 complete.**

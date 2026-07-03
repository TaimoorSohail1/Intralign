# Determinism Calibration Note 001

**Type:** Calibration note — determinism **principles** (no numeric values); supplies the guidance the Confidence subsystem defers to
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits beneath (authoritative — implements, must not modify):** `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md` · `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md` · `RELEASE_1_CONFIDENCE_SUBSYSTEM_TEST_SPECIFICATION.md` · `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md`
**Consistent with:** Analysis Engine §15/§16 · Testing Strategy §6/§15 · State/Event/Data v1.1 models. **Stack position:** `OUTCOME_CONFIDENCE_STACK_INDEX.md` (calibration support for L4).

> **Non-negotiable.** This note establishes the **governing principles** for determinism, bounded equivalence, replay validation, regression interpretation, and baseline management. It introduces **no numeric tolerances, percentages, thresholds, formulas, scoring, or implementation details**, creates **no** new doctrine/entities/states/events/dimensions/calibration arithmetic, and **modifies no** Confidence/CAF/Reliability meaning. **Wherever a numeric value would normally be required, it states "Deferred to future calibration."** All rules are **objective and structurally testable** (Recommendation A); subjective terms ("reasonable", "minimal", "acceptable") are avoided.

---

## 1. Purpose

Determinism calibration exists to make the Confidence subsystem's behavior **verifiable and regression-detectable** despite the analysis engine containing LLM-bearing stages. Without a determinism principle, "same input → same output" is untestable: there is no agreed answer to *which* outputs must match, *against what* they are compared, or *when* a difference is a defect versus an expected baseline update. This note fixes those **principles** — equivalence over governable outputs, replay as reconstruction, and regression evaluated only within a baseline — so the test and fixture specifications have a stable basis. It supplies the **principle**; the **tolerance value** itself is **Deferred to future calibration**.

---

## 2. Scope

**In scope:**
- **Equivalence evaluation** — what determinism is assessed against (governable outputs).
- **Replay validation** — reconstruction of persisted state, distinct from live execution.
- **Regression interpretation** — what a regression is, within a baseline.
- **Baseline management** — what a baseline is and how changes to it are treated.

**Out of scope:**
- **Numeric tolerances / thresholds / percentages** — Deferred to future calibration.
- **Implementation techniques** — how determinism is achieved (seeding, caching, infra).
- **Model internals** — engine/model mechanics.
- **Infrastructure concerns** — transport, storage, scaling.

---

## 3. Determinism Definition

Determinism is evaluated **against governable outputs**, not raw model internals. The **governable output set** (used throughout the stack) is:

- **finding-type set**
- **recommendation set**
- **confidence band**
- **reliability qualifier**

Determinism asks whether, for the same input under the same baseline, **these governable outputs remain equivalent** — **not** whether internal representations, intermediate text, or token-level details are identical. **No additional governable outputs are invented here.**

> **Provenance note (Recommendation B).** The governable output set is **implementation-derived** — it originates in the **Analysis Engine Specification §15/§16** and **Testing Strategy §6/§15**, not from founder meaning-doctrine. It is **not new doctrine**; this note adopts it unchanged and only governs how determinism is evaluated against it.

---

## 4. Bounded Equivalence Principle

- **Exact identity is not required.** Determinism does not demand bit-exact or token-exact reproduction (infeasible for LLM-bearing stages).
- **Equivalence is the governing concept.** Determinism is satisfied when the **governable outputs are equivalent** for the same input under the same baseline — incidental phrasing or internal detail may differ.
- **Determinism concerns the governable outputs only** — the finding-type set, recommendation set, confidence band, and reliability qualifier (Section 3).

**The actual equivalence tolerance is Deferred to future calibration.** This note fixes *that* equivalence is bounded and *over which outputs*; it fixes **no** numeric bound.

---

## 5. Replay Principle

**Replay = reconstruction of persisted state from the event log.**

Replay is **NOT**:
- **re-analysis** — it does not analyze inputs again;
- **re-execution** — it does not run the engine/models again;
- **re-running models** — it invokes no LLM or scoring;
- **side-effecting** — it emits no external effects (e.g., notifications).

> **Replay vs Re-Execution boundary (Recommendation C — made explicit).** **Replay reconstructs. Replay does not think. Replay does not re-analyze. Replay does not emit side effects.** Replay rebuilds the *already-persisted* CAF/Reliability/Confidence states and their supersession chains exactly, from the append-only event log. **Live execution** (a fresh analysis run) is the *only* place new states are computed; determinism (Section 4) governs *live execution*, while replay governs *reconstruction*. The two are evaluated separately and must never be conflated.

Replay exists so that history/audit is reconstructable **exactly** without recomputation, and so that explainability and lineage survive independently of model behavior. This remains consistent with the Replay tests (Subsystem Test Spec §11, REPLAY-T1…T6).

---

## 6. Baseline Principle

A **baseline** consists of:
- **pinned configuration** (the run/engine settings),
- **fixture version** (the exact fixture inputs), and
- **model version** (the model used).

**Determinism and regression evaluation occur only against a baseline.** A determinism or regression result is meaningful **only** relative to a fixed (configuration × fixture × model) triple. Comparing outputs produced under **different** baselines is not a determinism evaluation.

> **Baseline discipline (Recommendation D).** A change to **any** baseline component — **configuration, fixture, or model** — establishes a **new baseline**. Regression interpretation **requires baseline consistency**: only outputs produced under the **same** baseline may be compared for regression.

---

## 7. Model Version Principle

**A model-version change creates a new baseline; it is not automatically a regression** (formalizing Calibration CAL-DET-4).

**Why.** Determinism is guaranteed only *within* a pinned configuration (which includes the model version). A different model version is a **different baseline**, so a difference in governable outputs across model versions is an **expected baseline change**, not a defect. Treating cross-version differences as regressions would make every legitimate model update fail — which is incoherent. Cross-version change is therefore **recorded as a baseline update**, while regression is reserved for **within-baseline** departures (Section 8).

---

## 8. Regression Interpretation Principle

**Regression = governable outputs departing from bounded equivalence within the same baseline** (formalizing Calibration CAL-DET-5).

- **Within a baseline:** if the governable outputs for the same input cease to be equivalent (beyond the deferred tolerance), that is a **regression** — a defect and a release blocker.
- **Across baselines:** a difference is **not** a regression; it is a **baseline update** (Sections 6–7), recorded as such.

Changes within a baseline and changes across baselines are therefore **evaluated differently**. **No tolerance value is defined here** — the bound that separates "equivalent" from "departed" is **Deferred to future calibration.**

---

## 9. Fixture Stability Principle

Aligned with `RELEASE_1_CONFIDENCE_FIXTURE_LIBRARY_SPECIFICATION.md` (§8/§11) and its ratified refinements:

- **Active fixtures create baselines.** An Active fixture version is part of the baseline triple (Section 6).
- **Fixture changes create new baselines.** Editing fixture inputs changes the baseline; the change is a **new fixture version**, never an in-place edit.
- **Fixture edits must not invalidate historical determinism results.** Because prior results are tied to the prior fixture version, superseding a fixture **preserves** the interpretability of results produced against it.
- **Fixture supersession preserves interpretability of prior test results.** The append-only fixture lifecycle (Draft → Approved → Active → Deprecated → Retired) keeps every version retrievable, so any past determinism/regression result remains meaningful relative to its own baseline.

This makes fixture stability a **precondition** for sound determinism evaluation: without a pinned fixture version, a real regression cannot be distinguished from a fixture change.

---

## 10. Determinism Integrity Rules

*Objective, structurally testable. Each realizes existing doctrine/calibration; none is new doctrine, and none uses a numeric criterion.*

- DT-1. Determinism is evaluated **against the governable output set** (finding-type set, recommendation set, confidence band, reliability qualifier) — never against raw internals.
- DT-2. Determinism requires **bounded equivalence** of governable outputs for the same input under the same baseline (tolerance Deferred).
- DT-3. **Replay must reconstruct persisted state** from the event log **without** re-analysis, re-execution, or side effects.
- DT-4. Replay and live execution are **evaluated separately**; replay is never used to assert live-execution determinism, nor vice-versa.
- DT-5. A **baseline** is the (pinned configuration × fixture version × model version) triple; determinism/regression are evaluated **only** within a baseline.
- DT-6. A **model-version change creates a new baseline**; a cross-version output difference is **not** a regression.
- DT-7. A **fixture-version change creates a new baseline**; fixture changes are append-only (new version), never in-place edits.
- DT-8. A **configuration change creates a new baseline.**
- DT-9. **Regression requires baseline consistency** — only same-baseline outputs may be compared; a regression is a within-baseline departure from bounded equivalence.
- DT-10. Every baseline component MUST be **recorded** with each run so determinism/regression results are attributable to a specific baseline.

---

## 11. Conformance Requirements

Structural conformance for implementations and test suites (**no percentages, no thresholds, no pass-rate language**):

- **C-1.** The implementation **records** the full baseline triple (configuration, fixture version, model version) for every run (DT-5/DT-10).
- **C-2.** Determinism evaluation compares **only** the governable output set, **only** within a single baseline (DT-1/DT-5).
- **C-3.** Replay reconstructs persisted CAF/Reliability/Confidence states and supersession chains **exactly**, with **no** recomputation and **no** side effects (DT-3; REPLAY-T1…T6).
- **C-4.** The suite **distinguishes** replay results from live-execution determinism results (DT-4).
- **C-5.** A model, fixture, or configuration change is **registered as a new baseline**, not flagged as a regression (DT-6/DT-7/DT-8).
- **C-6.** A within-baseline departure of governable outputs from bounded equivalence is **flagged as a regression** (DT-9) — a release blocker (per Subsystem Test Spec §14).
- **C-7.** Fixture changes are applied as **new versions** (append-only), preserving prior results' interpretability (DT-7; Fixture Library §9/§11).
- **C-8.** Every determinism/regression result is **attributable** to a specific recorded baseline (DT-10).

Conformance is **structural and all-or-nothing on these rules**; the numeric tolerance that C-6 ultimately compares against is **Deferred to future calibration**.

---

## 12. Deferred Items

Explicitly **Deferred to future calibration** (this note creates none of them):
- **Equivalence tolerance value** — the bound separating "equivalent" from "departed" (Sections 4, 8).
- **Determinism thresholds** — any numeric determinism criterion.
- **Regression thresholds** — the numeric bound for a within-baseline regression.
- **Replay tolerances** — none assumed; replay is exact reconstruction, but any operational allowance is Deferred.

A **future calibration artifact may define these values.** When it does, it must conform to the principles in this note (governable-output equivalence, replay-as-reconstruction, baseline discipline) and may **not** alter any meaning doctrine or model invariant above it in the stack.

---

*This note establishes the determinism, bounded-equivalence, replay, regression, and baseline **principles** the Confidence subsystem defers to. It introduces no numeric values, no new doctrine/entities/states/events/dimensions, and no implementation detail; it keeps every rule objective and structurally testable; and it defers all tolerances to future calibration. It is the governing reference for how determinism and regression are interpreted across the Confidence stack.*

**Determinism Calibration Note 001 complete.**

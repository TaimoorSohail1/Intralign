# Release 1 Confidence Subsystem Test Specification

**Type:** Testing & validation artifact (implements the models/doctrine; creates none)
**Status:** Active Release 1 · **Date:** 2026-05-31
**Sits below (authoritative — implements, must not modify):** `OUTCOME_CONFIDENCE_DOCTRINE_DECISION_001.md` · `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_LEADERSHIP_DOCTRINE_001.md` · `OUTCOME_CONFIDENCE_CALIBRATION_DECISION_001.md` · `CONFIDENCE_MODEL_V2.md` · `CAF_SCORING_MODEL_V2.md` · `RELIABILITY_MODEL_V2.md`
**Consistent with:** `RELEASE_1_TESTING_STRATEGY_V1.md` · Analysis Engine · State/Event/Data v1.1 models. **Stack position:** `OUTCOME_CONFIDENCE_STACK_INDEX.md` (validation of L4).

> **Non-negotiable.** This document **validates** doctrine; it does **not** create doctrine, calibration, formulas, thresholds, weights, percentages, probability models, or governance behavior, and it **modifies no** CAF/Reliability/Confidence doctrine. Determinism tolerance values are **"Deferred to Determinism Calibration Note."** Conformance is **structural**, never a pass-rate percentage. **Testing validates doctrine; testing never redefines doctrine.**

---

## 1. Purpose

This document is the **authoritative testing reference** for the CAF → Reliability → Confidence subsystem. It defines **what must be tested, why, what constitutes success and failure, which invariants must never be violated**, and the required regression, replay, and explainability tests — so that an implementation can be certified to behave **exactly as the doctrine and the v2 models define**.

---

## 2. Scope

**Tested:** the behavior of `CAFState`, Reliability (as carried on per-run states), and `ConfidenceState` and their relationships — representation, conformance to the v2 models' Integrity Rules (CR-*, RR-*, IR-*), cross-model invariants (INV-1/2/3), Fast/Deep behavior, history/supersession, replay, explainability, and determinism *structure*.

**Explicitly not tested here (out of scope / owned elsewhere):** numeric calibration values (band/scale boundaries, magnitudes, tolerance), UI rendering, governance, probability/outcome constructs (none exist), the analysis engine's extraction stages (covered by engine tests), and severity numerics. These are **Deferred** (Section 17) or owned by other suites.

---

## 3. Subsystem Under Test

```text
Findings ─(Impact Assessment)─▶ CAF Scoring v2 ──┐
                                                  ├─▶ Confidence v2 (consolidate-then-qualify) ─▶ ConfidenceState
Coverage / Evidence / Assessability ─▶ Reliability v2 ──┘
```

- **CAF Scoring v2** — produces the three independent, co-equal dimension assessments (Clarity, Alignment, Feasibility); findings act on CAF only, locally, sized by Impact Assessment (not type).
- **Reliability v2** — produces the High/Moderate/Low qualifier from Coverage/Evidence Availability/Assessability, independently of CAF and findings; qualifies confidence, never replaces it.
- **Confidence v2** — consolidate-then-qualify; produces the `ConfidenceState` (band + reliability qualifier + basis), superseded over time.
- **Relationships under test:** CAF → Confidence; Reliability → Confidence; **CAF ≠ Reliability ≠ Confidence**; one-directional (no feedback).

---

## 4. Test Categories

| Category | Validates | Primary source rules |
|---|---|---|
| **CAF Tests** (§5) | CAF conformance | CR-1…CR-14 |
| **Reliability Tests** (§6) | Reliability conformance | RR-1…RR-10 |
| **Confidence Tests** (§7) | Confidence conformance | IR-1…IR-17 |
| **Cross-Model Tests** (§8) | INV-1/2/3 + boundaries | Calibration Invariants |
| **History Tests** (§10) | append-only/supersession | CR-14, RR-10, IR-14 |
| **Replay Tests** (§11) | reconstruction vs live | IR-15; Engine §16 |
| **Explainability Tests** (§12) | basis reconstruction | IR-12, CR-13, RR-9 |
| **Fast vs Deep Tests** (§9) | provisional/supersede/decline | Confidence v2 §11; CAF v2 §12 |
| **Determinism Tests** (§13) | equivalent governable outputs | IR-/Engine §15 (tolerance Deferred) |
| **Regression Tests** (§14) | release gate | Engine §15; Testing §15 |

---

## 5. CAF Conformance Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **CAF-T1** Dimension independence | A change confined to one dimension's findings moves only that dimension | Other dimensions unchanged | Any non-affected dimension moves (violates CR-2/CR-5) |
| **CAF-T2** Co-equality / no weighting | No dimension is privileged or ranked in CAF representation | Three dimensions represented with equal standing | Evidence of fixed hierarchy/weighting (CR-3) |
| **CAF-T3** Finding locality | A finding contributes only to its Impact-Assessment-declared dimensions | Contribution confined to affected dimensions | Contribution to a non-affected dimension (CR-5) |
| **CAF-T4** Type-is-not-coefficient | Two same-type findings with different Impact Assessments produce different contributions | Magnitude tracks Impact Assessment, not type | Magnitude determined by type (CR-4/CR-7) |
| **CAF-T5** Impact-Assessment control | Re-assessing a finding's impact changes the dimension without the finding changing | Dimension moves on impact re-assessment | Dimension unchanged, or finding forced to change (CR-8) |
| **CAF-T6** Evidence/finding-driven movement only | CAF recomputes only on evidence or finding/Impact change | No movement on time, Reliability, or Confidence | CAF moves with no evidence/finding change (CR-9) |
| **CAF-T7** No confidence feedback | Changing Confidence never alters CAF | CAF invariant under Confidence changes | CAF moves due to Confidence (CR-11) |
| **CAF-T8** Reducing direction | A finding's presence reduces integrity; resolution raises it | Direction always reducing; rise via resolution/evidence | A finding's presence raises integrity (CR-6) |

---

## 6. Reliability Conformance Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **REL-T1** Independence from CAF | Reliability determined without reference to CAF strength | Reliability set from surface conditions only | Reliability derived from CAF (RR-2) |
| **REL-T2** Independence from findings | Findings (incl. severity) do not move reliability | Reliability invariant under finding/severity changes | Reliability moves on a finding/severity change (RR-2/RR-8) |
| **REL-T3** Assessability gating | Low assessability constrains reliability regardless of coverage/evidence | Reliability constrained when assessability is low | High reliability despite low assessability (RR-6) |
| **REL-T4** Qualifier-only | Reliability never alters CAF and never acts as a score | CAF unchanged by reliability; reliability carried as qualifier | Reliability alters CAF or appears as a co-score (RR-3/RR-5) |
| **REL-T5** Non-collapse | Strong CAF + Low reliability does not yield lowest confidence from reliability alone | Confidence held above floor (e.g., Moderate) | Reliability alone collapses to Very Low (RR-7) |
| **REL-T6** Moves while CAF unchanged | Adding coverage/evidence raises reliability with CAF identical | Reliability rises, CAF unchanged | Reliability cannot move without CAF, or CAF forced to move (RR-8 / Example C) |

---

## 7. Confidence Conformance Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **CONF-T1** Consolidate-then-qualify | Confidence derives from consolidated CAF then qualified by reliability | Band reflects consolidation (between average and minimum) + qualification | Simple average, weakest-link domination, or a dimension ignored (IR-3/IR-4) |
| **CONF-T2** Stability invariant | Confidence does not change unless CAF or reliability changes | No movement absent a CAF/reliability change | Band changes with no CAF/reliability change (IR-10) |
| **CONF-T3** Explainability invariant | Every confidence state exposes its full basis | Basis available without recomputation | Any opaque/unexplainable state (IR-12) |
| **CONF-T4** Reliability qualification | Same CAF, different reliability → different confidence expression | Lower reliability holds the band back (bounded) | Reliability ignored, or collapses signal (IR-7/IR-8) |
| **CONF-T5** Movement attribution | Every transition is attributable to CAF and/or reliability change | Change attribution present and correct | Transition unattributable (IR-11) |
| **CONF-T6** Supersession | A new confidence state supersedes and retains the prior | Supersession pointer set; prior retained | Overwrite/deletion of prior state (IR-14) |
| **CONF-T7** Representation | Confidence carries band + reliability qualifier + basis | Never a bare value; never labeled probability/health/readiness | Bare band, or probability/health framing (IR-1/IR-16/IR-17) |

---

## 8. Cross-Model Invariant Tests

| ID | Invariant | Test objective | Failure condition |
|---|---|---|---|
| **INV-T1** | **Confidence Stability** — confidence may not move unless CAF or Reliability changes | Drive scenarios with no CAF/reliability change; confidence must be stable | Any confidence movement without a CAF/reliability change |
| **INV-T2** | **Explainability** — every confidence state is explainable | Inspect every produced state for full basis (CAF + reliability + findings + recommendation history + supersession) | Any state missing a required basis component |
| **INV-T3** | **Reliability Non-Collapse** — low reliability alone cannot collapse strong CAF to lowest confidence | Strong CAF + Low reliability fixture; confidence must stay above floor | Confidence reaches Very Low from reliability alone |
| **INV-T4** | **One-directional boundary** (doctrine-supported) — Confidence/Reliability never alter CAF; Reliability never replaces Confidence | Mutate Confidence/Reliability; CAF must be invariant; reliability must remain a qualifier | CAF moves, or reliability acts as a second confidence score |
| **INV-T5** | **Meaning boundary** (doctrine-supported) — confidence is trust-in-understanding, never probability/health/readiness | Inspect representation/labels across states | Any probability/health/readiness semantics present |

---

## 9. Fast vs Deep Analysis Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **FD-T1** Fast is provisional | Fast confidence is produced as initial/non-final; Alignment/Feasibility carry lower per-dimension reliability | Fast `ConfidenceState` flagged non-final; project `oriented` | Fast confidence treated/stored as final |
| **FD-T2** Deep supersedes Fast | A Deep run's confidence supersedes the Fast confidence; prior retained | Supersession chain Fast → Deep | Fast confidence overwritten or not superseded |
| **FD-T3** Deep may rise | Fixture where Deep resolves ambiguity/adds coverage → confidence rises | Band/expression increases with attribution | No rise where understanding strengthened |
| **FD-T4** Deep may fall | Fixture where Deep discovers a contradiction → CAF weakens → confidence falls | Band decreases, attributed to the new finding via CAF | Confidence fails to fall, or fall attributed to non-CAF cause |
| **FD-T5** Decrease-with-improvement | Deep run that improves understanding yet lowers confidence (contradiction surfaced) | Confidence decreases; understanding demonstrably deeper; not flagged as deterioration | Decrease treated as error/deterioration (violates doctrine) |
| **FD-T6** History preserved | After Deep supersession, the Fast confidence remains in history | Both states reconstructable | Prior state lost |

**Explicit scenario (FD-T5):** a project whose Fast orientation shows High confidence; a Deep run performs contradiction discovery, surfacing a Conflict finding (Alignment) whose Impact Assessment lowers CAF; the recalculated confidence drops to Moderate at **higher** reliability. *Expected:* supersession recorded, decrease attributed to the new finding via CAF, Fast state retained, no deterioration semantics. *Pass* iff all hold.

---

## 10. History and Supersession Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **HIST-T1** CAF history | Each reassessment supersedes prior `CAFState`; chain retained | Append-only CAF chain | Overwrite/loss of a prior `CAFState` (CR-14) |
| **HIST-T2** Reliability history | Reliability (on per-run states) supersedes via the chain; retained | Reliability chain reconstructable, distinct from CAF chain | Overwrite, or reliability chain forced to track CAF (RR-10) |
| **HIST-T3** Confidence history | Each recalculation supersedes prior `ConfidenceState`; retained | Append-only confidence chain | Overwrite/loss of a prior `ConfidenceState` (IR-14) |
| **HIST-T4** No overwrite | No history-bearing state is mutated in place | All change via supersession pointers | Any in-place mutation of a prior state |

---

## 11. Replayability Tests

Replay = **exact reconstruction of persisted state from the event log**, distinct from **live re-execution** (Confidence v2 C-4; Engine §16).

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **REPLAY-T1** Historical reconstruction | Replaying the event log reproduces persisted CAF/Reliability/Confidence states exactly | Reconstructed state == original (side effects suppressed) | Any divergence in persisted state |
| **REPLAY-T2** Supersession reconstruction | All supersession chains rebuild identically | Chains identical | Chain order/links differ |
| **REPLAY-T3** Confidence lineage | The confidence chain + change attributions reconstruct | Lineage identical | Missing/incorrect attribution |
| **REPLAY-T4** Reliability lineage | The reliability chain reconstructs (on per-run states) | Lineage identical | Divergence |
| **REPLAY-T5** CAF lineage | The CAF chain + contributing findings/impact assessments reconstruct | Lineage identical | Divergence |
| **REPLAY-T6** Replay ≠ live | Replay does not re-execute the model or emit external side effects | Reconstruction only | Replay re-runs analysis or re-emits notifications |

---

## 12. Explainability Tests

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **EXPL-T1** CAF basis | Reconstruct each dimension's assessment + contributing findings + impact assessments | Full CAF basis available without recomputation | Any missing component (CR-13) |
| **EXPL-T2** Reliability basis | Reconstruct coverage/evidence/assessability basis + independence statement | Full reliability basis available | Missing component / no independence statement (RR-9) |
| **EXPL-T3** Confidence basis | Reconstruct CAF basis + reliability basis + cause-of-level | Full confidence basis available | Any missing component (IR-12) |
| **EXPL-T4** Contributing findings | Each affected dimension traces to its findings | Findings resolvable | Untraceable contribution |
| **EXPL-T5** Impact assessments | Each contribution traces to its Impact Assessment | Impact Assessment resolvable | Untraceable magnitude/locality |
| **EXPL-T6** Change attribution | Every state change traces to its cause (CAF and/or reliability) | Attribution present | Unattributable change |
| **EXPL-T7** Opaque-state rejection | Any state lacking a required basis component fails | Opaque state rejected as defect | Opaque state accepted |

---

## 13. Determinism Tests

Validate that, for the **same input under the same pinned configuration**, the **governable outputs are equivalent** — the **finding-type set, recommendation set, confidence band, and reliability qualifier** (Engine §15; Confidence v2 C-4).

| ID | Objective | Expected behavior | Failure condition |
|---|---|---|---|
| **DET-T1** Same-input equivalence | Re-run identical inputs under pinned config | Governable outputs equivalent | Governable outputs differ beyond tolerance |
| **DET-T2** No-change → no-recompute | Re-trigger with unchanged understanding | No new state fabricated | New state produced without a CAF/reliability change |
| **DET-T3** Config pinning | Outputs evaluated against the recorded configuration | Determinism assessed per pinned config | Determinism asserted across differing configs |

> **Tolerance:** the bounded-equivalence **tolerance value is "Deferred to Determinism Calibration Note."** These tests are **structurally defined now**; their numeric pass/fail bound is supplied by that calibration artifact. **No tolerance value is created here.**

---

## 14. Regression Test Requirements

- **What constitutes a regression.** A change in **governable outputs under the same pinned configuration** beyond the (deferred) bounded-equivalence tolerance. A **model-version change is a new baseline, not a regression** (Engine §15; Calibration CAL-DET-4/5).
- **Must be tested before release (gate).** The full CAF (§5), Reliability (§6), Confidence (§7), Cross-Model Invariant (§8), History (§10), Replay (§11), and Explainability (§12) suites must pass, plus the determinism structural suite (§13, tolerance deferred). Any invariant violation (INV-T1/2/3) is a **hard release blocker**.
- **Per-fix regression.** Every fixed defect adds a regression test pinned to the invariant/rule it violated.
- **Baseline discipline.** Regression is evaluated only within a pinned configuration; baseline updates are recorded, not counted as regressions.

---

## 15. Test Fixture Requirements

Required fixture **classes** (definitions only — no actual fixtures created here):

- **Ambiguity fixtures** — exercise Clarity-reducing findings (ambiguity/missing information).
- **Assumption fixtures** — exercise assumption findings and their dimension impact.
- **Conflict fixtures** — exercise contradiction discovery and Alignment-reducing findings (drive FD-T4/T5).
- **Coverage fixtures** — vary the breadth of the observable surface (drive REL-T1/T6).
- **Evidence fixtures** — vary evidence availability (drive reliability movement with CAF unchanged).
- **Assessability fixtures** — vary assessability to exercise gating (REL-T3) and non-collapse (REL-T5/INV-T3).
- **Fast/Deep fixtures** — paired fast-then-deep inputs that produce both rises and falls (drive §9), checksum-pinned for determinism/replay.

Fixtures must be **deterministic and configuration-pinned** so determinism/replay tests are stable.

---

## 16. Conformance Requirements

The subsystem is **certified** when **all** of the following hold (structural — **no percentages, no pass-rate thresholds**):

- **CR-1.** All CAF Integrity Rules (CR-1…CR-14) pass (§5).
- **CR-2.** All Reliability Integrity Rules (RR-1…RR-10) pass (§6).
- **CR-3.** All Confidence Integrity Rules (IR-1…IR-17) pass (§7).
- **CR-4.** All Cross-Model Invariants (INV-T1…T5) pass — **zero** violations (hard gate).
- **CR-5.** Fast/Deep behavior (§9), including decrease-with-improvement, passes.
- **CR-6.** History/supersession (§10) and Replay (§11) pass — exact reconstruction; no overwrite.
- **CR-7.** Explainability (§12) passes — **no opaque state** exists.
- **CR-8.** Determinism **structural** suite (§13) passes (tolerance deferred).

Certification is **all-or-nothing on the invariants**: any INV violation, any opaque state, or any unattributable confidence change **fails certification** regardless of other results.

---

## 17. Deferred Items

Explicitly **Deferred to future calibration artifacts** (not created or assumed here):

- **Determinism tolerance / bounded-equivalence bound** → **Determinism Calibration Note**.
- **Band/scale boundaries** (CAF, Reliability, Confidence) → the respective v2 calibration appendices.
- **Calibration arithmetic** (synthesis "between an average and a minimum"; reliability combination; contribution magnitude) → v2 calibration.
- **Scoring values / severity numerics** → CAF Scoring v2 calibration.

These deferrals affect **numeric pass/fail bounds only**; all **structural** tests and invariants in this specification are defined and enforceable now.

---

## Critical Requirement — restated

This specification proves that **CAF + Reliability → Confidence behaves exactly as doctrine defines**: CAF supplies independent, co-equal dimension assessments; Reliability qualifies (never replaces, never collapses, never alters CAF); Confidence consolidates-then-qualifies, is stable, attributable, explainable, and superseding. **Testing validates this doctrine; testing never redefines it.**

**Release 1 Confidence Subsystem Test Specification complete.**

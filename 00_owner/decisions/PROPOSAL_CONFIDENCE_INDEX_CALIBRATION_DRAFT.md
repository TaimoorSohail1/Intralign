# PROPOSAL — Outcome Confidence Index Calibration (Measurement)

> **DRAFT for owner ratification (Framework 001).** Engineering proposes realization; the **owner ratifies** policy intent. Route: Backlog → **Proposal (this)** → Review → Decision → Change → Changelog. This resolves **OPEN_TBD D1** (bounded-equivalence tolerance) and the associated index scale/threshold TBDs. It does **not** modify the Confidence *meaning* (Interpretation Doctrine) — it supplies the *measurement* that doctrine deferred.

- **Date:** 2026-07-01 · **Status:** Proposed (owner direction 2026-07-01) · **Class:** B (measurement / calibration realization)
- **Layer:** `30_engineering` realization proposing values for `00_owner` owner-TBD registers (D1); lands as a Calibration spec + owner confirmations in `OPEN_TBD_REGISTER`. **Non-doctrinal** — meaning is unchanged.
- **Grounded in:** `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001` (Meaning fixed; Measurement deferred — §"Meaning vs Measurement"), canonical band vocabulary **Very Low · Low · Moderate · High · Very High** (Decision 001 / D12), `OPEN_TBD_REGISTER` **D1** (bounded-equivalence ±7 / same-band — *proposed, owner to confirm*), Confidence Model · CAF Assessment Model · Reliability Model (composition inputs), DL-046 (Fast/Deep passes emit Confidence), Testing §20.1 (non-determinism bound). Companion to `PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT.md` (the number now ships **clean**, so calibration is on the critical path).

## Why now

The Interpretation Doctrine states calibration must **follow** meaning: *"a number means nothing until its meaning is fixed."* Meaning is now fixed (bands + interpretation ratified). And the presentation decision (2026-07-01) makes the numeric index a **clean, focal, user-facing** figure — so its scale, band thresholds, stability, and equivalence tolerance can no longer stay TBD without risking exactly the misreads the doctrine warns of. Calibration is the missing measurement layer.

## What this proposal fixes (the open TBDs)

1. **Index scale** — the numeric range and its meaning.
2. **Band thresholds** — how the scale maps to the five canonical bands.
3. **Bounded-equivalence tolerance** (D1) — how much two runs on identical inputs may differ.
4. **Materiality / stability** — what counts as a *real* change (so the UI never dramatizes noise), plus boundary hysteresis.
5. **Composition constraints** — how CAF + reliability compose into the index, expressed as invariants (not a formula to ratify).
6. **Validation harness** — how the above are tested in CI.

> **Anti-Assumption compliance:** every numeric below is **PROPOSED — owner to confirm**. The **structure and harness** are the deliverable; the pass/fail numbers activate only on owner ratification. No threshold is treated as canon until ratified.

## Proposal

### 1. Scale
Adopt a **0–100 integer index** as the internal measurement, presented to users as the focal number. 0–100 is a display/interpretation scale, **not** a probability or percentage of success (Interpretation Doctrine). The **named band remains the authoritative unit of magnitude**; the integer is a finer readout *within* the ratified band vocabulary.

### 2. Band scheme & thresholds (OWNER-SET 2026-07-01)

Resolves the **3-band vs 5-band inconsistency**: the v0 formula doc used a 3-band scheme (0–49 / 50–74 / 75–100), while Master Spec §20 + Data Model + the Interpretation Doctrine use **5 bands**. **Adopt 5 bands**, reconciled by **preserving the v0's pressure-tested 50 and 75 edges** and subdividing the extremes:

| Band | Index range | Notes |
|---|---|---|
| **Very Low** | 0–34 | Immature / thinly-supported understanding |
| **Low** | 35–49 | Usable only with heavy caution |
| **Moderate** | 50–74 | Partial, qualified trust |
| **High** | 75–89 | Dependable enough to reason and plan with |
| **Very High** | 90–100 | As trustworthy as OSLO currently represents (never certainty) |

Plus the existing **±3 band-edge guard**. Grounded in a v0-formula simulation (2026-07-01): a single **material** weakness lands ~74 (top of Moderate); minor/moderate issues land High; all-dimensions-material floors at 45 (Low) — so the edges separate the doctrine's meanings against the formula's actual behavior. Edges refine from the interpretation-alignment suite; the 50/75 anchors are inherited from the v0 pressure-test.

### 2a. Magnitude defaults (OWNER-SET 2026-07-01 — R1 provisional, refine from data)
Adopt the v0 pressure-tested defaults as the R1 starting values, all marked *calibrate from real cohorts*: **impact table** trivial 0.03 / minor 0.08 / moderate 0.18 / significant 0.35 / material 0.55; **power-mean `p = −0.5`**; **floor `ε = 5`**. Watch-item (from v0 §7): small-finding stacking compounds multiplicatively — refine the impact table against real finding-count distributions; **change magnitudes only, never the structure**.

### 3. Bounded-equivalence tolerance (resolves D1)
Confirm **±7 / same-band** as the non-determinism bound: two analysis runs on **identical inputs** must yield indices within **±7 of each other AND resolve to the same band**. This is the governable-output equivalence contract for AI non-determinism (Testing §20.1). If runs disagree beyond this, it is a **defect**, not a confidence change.

### 4. Materiality & stability (ties presentation to measurement)
- **Material change rule:** a change is surfaced/animated as a real movement only if it **crosses a band boundary** OR **exceeds the ±7 tolerance** *and* is **cause-bound** (attributable to a finding resolved, evidence added, reanalysis discovery). Sub-tolerance drift is **not** shown as a change — this is what lets the number ship clean without misleading.
- **Boundary hysteresis (PROPOSED):** apply a **2-point** hysteresis at band edges (must move ≥2 past a threshold to re-label) to prevent flicker between adjacent bands.
- **Both directions:** the index may fall; a post-Deep fall is framed as *improved understanding, not a worse project* (Interpretation Doctrine).

### 5. Composition invariants (constraints, not a ratified formula)
The index is computed from the CAF dimensions and qualified by reliability. Rather than ratify a formula, ratify **invariants** the computation must satisfy:
- **Monotonic in CAF** — improving any dimension without weakening another must not lower the index.
- **Reliability qualifies, never inflates** — low reliability can **hold back** the index (false-confidence guard: high CAF + low reliability → index held down and flagged), and reliability alone never pushes the index above what CAF supports.
- **Independence** — reliability components (Coverage / Evidence availability / Assessability) are computed independently of CAF (they qualify it; they are not findings-driven).
- **Cause-traceable** — every index delta must be attributable to a named cause (for the change explanation and audit trail).

### 6. Validation harness (the structural deliverable)
- **Equivalence test:** N repeated runs on fixed fixtures assert ±7 / same-band (§3). Wired into CI as a gate; pass/fail threshold set on ratification.
- **Monotonicity test:** synthetic CAF perturbations assert the monotonic + reliability-qualifies invariants (§5).
- **Threshold/hysteresis test:** boundary fixtures assert correct band labelling and no flicker (§2, §4).
- **Interpretation-alignment set:** an owner/expert-labelled scenario suite (band-level labels only) validates that computed bands match human judgement — calibrating thresholds against meaning, not the reverse.

## Conditions (binding if ratified)

1. **Meaning is upstream** — calibration may set measurement but must never alter the ratified band meanings or the "not probability / not health" invariants.
2. **Band is authoritative** — where integer and band could diverge in interpretation, the band governs; the integer never implies precision the tolerance can't support.
3. **Tolerance is a contract** — beyond-tolerance non-determinism is a defect, gated in CI.
4. **No sub-tolerance theatre** — the UI does not present within-tolerance drift as change (aligns with the presentation proposal, Condition 2).
5. **Proposed numbers require ratification** — thresholds (§2), ±7 (§3), and 2-point hysteresis (§4) are candidate values; owner confirms in `OPEN_TBD_REGISTER` (D1 + a new index-scale/threshold entry).
6. **Recompute discipline** — the index changes only on reanalysis / state change (event-driven), consistent with the recompute doctrine.

## Dependencies

Confidence Model (composition), CAF Assessment Model, Reliability Model (inputs); Interpretation Doctrine (meaning, upstream); OPEN_TBD D1 (this resolves it) + a new scale/threshold TBD; Testing §20.1 (non-determinism); DL-046 (passes emit Confidence); `PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT` (consumes the clean, calibrated number). Perf/NFR (calibration must not breach the <60s Time-to-First-MRI ceiling).

## Concerns

- **Threshold sensitivity** — band widths materially shape user perception; the interpretation-alignment set (§6) must drive them, or the numbers will feel arbitrary. Recommend owner review of the labelled scenario suite before confirming §2.
- **±7 vs narrow bands** — if any ratified band is narrower than the tolerance, same-run values could straddle it; §2's widths keep every band ≥ tolerance, but owner changes to widths must preserve this.
- **Composition transparency** — ratifying invariants (not a formula) keeps flexibility but means the exact computation stays engineering-owned; the "how this is calculated" affordance must stay truthful to whatever formula realizes the invariants.
- **Calibration drift over time** — model changes can shift the mapping; the equivalence + alignment suites must run as regression gates, not one-time.

## Recommendation

**Accept the structure and harness; ratify the proposed numbers after reviewing the interpretation-alignment suite.** The measurement layer is now correctly sequenced (meaning first), and the clean user-facing number makes it necessary. Adopt §1 (0–100), §3 (±7/same-band, resolving D1), §4–§6 as the calibration contract; treat §2 thresholds and the 2-point hysteresis as candidate values pending the labelled-scenario review. Owner ratifies; on ratification it lands as a Calibration spec + D1/threshold confirmations with a Changelog record.

## Provenance

Owner direction 2026-07-01: with the confidence number now focal and shipping clean, calibration moves onto the critical path. AI drafted the measurement proposal, sequenced it behind the (already-ratified) interpretation meaning, resolved D1, and surfaced threshold-sensitivity and tolerance-vs-band-width risks (Framework 001A — analysis / recommendation). Candidate numbers are marked proposed per the Anti-Assumption Build Protocol. The **owner ratifies.**

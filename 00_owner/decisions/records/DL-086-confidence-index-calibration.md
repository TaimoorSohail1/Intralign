# DL-086 — Outcome Confidence index calibration (measurement) — 5-band scheme + v0 defaults

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** B (measurement/calibration realization; non-doctrinal — meaning unchanged)

- **Source:** Owner direction 2026-07-01/02. Proposal: `00_owner/decisions/PROPOSAL_CONFIDENCE_INDEX_CALIBRATION_DRAFT.md`; Review: `RATIFICATION_REVIEWS_001A.md` §2. Resolves `OPEN_TBD` D1 (±7/same-band) + workbook CAL-CONF-2 (band set) + CAL-DET-1; confirms F1 (v0 formula) for R1. Grounded in the Confidence Interpretation Doctrine (measurement follows meaning), canonical bands (Decision 001 D12), Master Spec §20, Testing §20.1, `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md`.
- **Layer:** `30_engineering` measurement realization + `00_owner` OPEN_TBD confirmations (D1/F1). Non-doctrinal (meaning unchanged).

## Decision
Ratify the Confidence measurement contract for R1:

- **Scale:** 0–100 integer index (display/interpretation; never probability/health). The **band remains the authoritative unit of magnitude**.
- **Band scheme (owner-set):** **5 bands**, resolving the v0 3-band vs Master Spec §20 5-band inconsistency by **preserving the v0's pressure-tested 50 & 75 edges and subdividing the extremes** — **Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100**, with the ±3 band-edge guard.
- **Magnitude defaults (owner-set, R1-provisional — refine from data):** impact table trivial 0.03 / minor 0.08 / moderate 0.18 / significant 0.35 / material 0.55; power-mean **p = −0.5**; floor **ε = 5**. Structure is doctrine-fixed; only magnitudes recalibrate (watch-item: small-finding multiplicative stacking).
- **Determinism tolerance (owner-set, provisional):** **±7 / same-band**; measured to confirm once the pipeline runs.
- **Materiality/hysteresis, composition invariants, CI harness:** per the proposal.

## Conditions
Per proposal Conditions 1–6: meaning upstream (doctrine unchanged); band is the authoritative unit; the tolerance is a CI-gated contract; sub-tolerance drift is not surfaced as change; the R1-provisional numbers recalibrate against real cohorts + the interpretation-alignment suite without a structure change; recompute is event-driven.

## Supersedes / Amends
Resolves `OPEN_TBD` D1 (+ workbook CAL-CONF-2 / CAL-DET-1); confirms F1 (v0 formula ratified for R1); **amends `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` §3** to the 5-band scheme (was 3-band 0–49/50–74/75–100). No prior decision superseded.

## Provenance
AI-drafted at owner direction; sequenced behind ratified meaning; band edges grounded in a v0-formula simulation and anchored to the pressure-tested 50/75 breakpoints; candidate numbers adopted as R1-provisional per the Anti-Assumption Build Protocol. Owner ratifies; effect on canon at owner merge via the Founder Console. Numbered at landing (DL-065).

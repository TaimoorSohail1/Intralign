# DL-097 — Canonical CAF-dimension maturity band vocabulary (RB-038)

- **Date:** 2026-07-08 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner ratification 2026-07-09 of the CAF-dimension band set (chosen from options presented). Proposal: `00_owner/decisions/PROPOSAL_CAF_DIMENSION_BAND_VOCABULARY_DRAFT.md` (RB-038). Resolves the open item in **DL-096** (Overview redesign). Grounded in `CAF_ASSESSMENT_MODEL_V1`, `CONFIDENCE_MODEL_V1` (Confidence bands Low/Moderate/High), CAF-01, and DL-087 (user-facing presentation-label mechanism).
- **Layer:** `00_owner` (Canonical Glossary) with `10_product` (CAF Assessment Model + Overview/Confidence presentation) reference. Presentation-only.

## Decision (ratifiable text)

Adopt a canonical **four-step CAF-dimension maturity band vocabulary**, ordered low→high, applied per CAF dimension (Clarity, Alignment, Feasibility):

**Limited · Forming · Solid · Strong**

This is the source of truth for the per-dimension band labels the user reads. It resolves the placeholder-vocabulary open item in DL-096.

## Conditions

- **Maturity ramp, not health.** Consistent with `Visual Design §1.2` (neutral maturity ramp; never red=bad/green=good). The band conveys understanding maturity, not project health.
- **Distinct axis.** The CAF-dimension band (a per-dimension input maturity) is **not** the same vocabulary as the overall **Confidence band** (Low/Moderate/High — the consolidated output), the **Understanding State** (AE-04: Initial→Partial→Refined→Validated→Mature), or the **MRI Understanding States** (MRI-03). This decision names one axis and does not merge or alter the others.
- **OWNER/CALIBRATION ITEM (open — do not assume):** the **band→CAF-score thresholds** (which numeric score = Limited vs Forming vs Solid vs Strong) are **not** ratified here. This record ratifies the **four band names and their order** only. Thresholds are an owner/calibration decision and must not be invented (Anti-Assumption Protocol).
- **Presentation-only.** CAF-01 already computes the per-dimension assessments; this names the presentation bands (DL-087 pattern). No scoring, model, or contract change.

## Realization (landed with the decision)

Add the canonical CAF-dimension band set to the `CANONICAL_GLOSSARY`; reference it in `CAF_ASSESSMENT_MODEL_V1` and the Overview/Confidence presentation specs. The v-next prototype (`oslo_r1_experience_mockup_v4.html`) already uses these bands.

## Supersedes / Amends

Adds a canonical definition to the `CANONICAL_GLOSSARY`; referenced by the CAF Assessment Model and the Confidence/Overview presentation. Resolves the DL-096 open item. No model, scoring, doctrine, or object superseded.

## Provenance

Owner-directed 2026-07-09: canon did not fix a per-dimension CAF band vocabulary, so AI surveyed canon, confirmed the gap, presented three coherent ramp options with a recommendation, and the **owner selected `Limited · Forming · Solid · Strong`** — surfacing the band→score thresholds as an explicit owner/calibration item rather than resolving it. **AI recommended; the owner ratifies.** Number assigned at landing (DL-065); effect on canon at owner merge.

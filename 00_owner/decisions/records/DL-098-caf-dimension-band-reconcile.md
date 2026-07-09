# DL-098 — Reconcile CAF-dimension bands to the DL-086 5-band scheme (supersedes DL-097) (RB-039)

- **Date:** 2026-07-09 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Conflict found 2026-07-09 during the DL-097 threshold work: DL-097's 4-band CAF-dimension vocabulary collides with the ratified DL-086 scoring scheme. Proposal: `00_owner/decisions/PROPOSAL_CAF_DIMENSION_BAND_RECONCILE_DL086_DRAFT.md` (RB-039). Grounded in **DL-086** and `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` (§1 per-dimension 0–100; §3 5-band scheme).
- **Layer:** `00_owner` (decision) with `10_product/experience` + `product-design` (Overview/Confidence presentation) realization. Presentation-only.

## Decision (ratifiable text)

**CAF dimensions (Clarity, Alignment, Feasibility) use the ratified DL-086 5-band scheme** — **Very Low 0–34 · Low 35–49 · Moderate 50–74 · High 75–89 · Very High 90–100** (with the ±3 band-edge guard) — the same authoritative band unit as the Confidence index. **DL-097's 4-band vocabulary (Limited · Forming · Solid · Strong) is superseded and retired.** The DL-097 "band→score thresholds" open item is **closed**: DL-086 already owns the edges.

## Conditions

- **No new thresholds.** DL-086's per-dimension 0–100 edges apply directly; no calibration is introduced here.
- **Stage narrative unchanged.** "Understanding is forming" is the confidence **stage** (CONF-05), separate from the band; it stays.
- **Maturity, not health.** The 5-band is a neutral maturity ramp (DL-086; Visual §1.2). The amber "limit" flag on the weakest dimension is retained (attention, not health color).
- **Presentation-only.** DL-086's formula/scoring/calibration unchanged; no model, scoring, or contract change.

## Realization (landed with the decision)

Confirm `CAF_CONFIDENCE_V0_SCORING_FORMULA_V1 §3` states dimension bands use the 5-band scheme (already implied); relabel dimensions in the Overview/Confidence presentation and the `oslo_r1_experience_mockup_v4.html` prototype (Strong/Forming/Limited → the 5-band words: e.g. Clarity **High** · Alignment **Moderate** · Feasibility **Very Low**). No glossary removal needed (DL-097's entry was never added).

## Supersedes / Amends

**Supersedes DL-097** (the 4-band CAF-dimension vocabulary) and its RB-038 outcome. Confirms (does not change) DL-086 and the v0 scoring formula. No doctrine, model, or scoring superseded.

## Provenance

While teeing up the DL-097 band→score thresholds, AI surfaced that DL-097 conflicts with the earlier-ratified DL-086 scoring scheme — a conflict DL-097's analysis missed by not reading the scoring formula spec (an incomplete read at DL-097 draft time). AI flagged the conflict, presented reconciliation options, and the **owner selected adopting the single DL-086 5-band scheme** (Option B). **AI recommended; the owner ratifies.** Number assigned at landing (DL-065); effect on canon at owner merge.

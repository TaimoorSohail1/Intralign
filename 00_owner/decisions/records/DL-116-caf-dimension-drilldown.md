# DL-116 — CAF drill-down — quantify the drivers, never the dimension (adds a finding-type field)

- **Date:** 2026-07-16 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

# DL-PENDING — CAF "What's driving it" becomes a drill-down: quantify the DRIVERS, never the dimension (adds a canonical finding-type field)

**Class:** A (product design + a data-model addition) · **Framework 001A** (AI drafts; **owner ratifies**; numbered at land per DL-065)
**Decided by:** Idris (Founder) · **Drafted:** 2026-07-15 · Grill record: **Enhancement #3** (intermediate release).

## Problem
The Overview "What's driving it" CAF panel showed only the three dimensions as five-band maturity ramps (Clarity / Alignment / Feasibility) with no way to see *what supports each band*. Users had no quantifiable insight into the level below the dimension.

## Decision (recommended — owner ratifies)
The panel becomes a **drill-down** that quantifies the **drivers** of each dimension's band. **The band stays a band — there is NO numeric score/percentage on a dimension.** This upholds **D176b** (the dimensions are bands, not percentages) and **D183b** (the bounded numeric index was deleted because a number under the confidence/CAF label reads as a forbidden "probability of hitting your outcome" forecast). Only the *drivers* are quantified.

- **Level 1** (a dimension expanded): **Rests on** — grounded vs inferred count (evidence vs inference); **Held back by** — open issues impacting the dimension, by severity; **To lift it** — the specific limiter.
- **Level 2** ("What kind of problem?"): the dimension's open issues grouped by **canonical CAF finding type**, each routing to the existing Issue panel.
- **Conforms to CAF_ASSESSMENT_MODEL_V1 §5** — *CAF is determined by the interaction of evidence and findings* — the drill-down exposes exactly those determinants (evidence/inference strengthens; findings reduce), never a manufactured score. **§8** — Level 2 uses the ratified seven-type finding taxonomy (Missing Information · Ambiguity · Assumption · Inference · Conflict · Constraint · Coverage Gap).

## Data-model addition (the one owner-ratified item)
Each issue/finding gains a **canonical finding type** field (`ftype`, one of the §8 seven types) so Level 2 can group by type. In the prototype the 9 demo issues are tagged **illustratively** (marked owner-confirmable in code). For real issues, OSLO assigns the finding type during Impact Assessment (§9); **the owner ratifies that the taxonomy mapping is applied as intended.** No new object — a field on the existing Finding.

## Doctrine inside the confidence card (D003 / D175 / D176a)
The card is a neutral maturity zone: ramps, band words, and driver numbers stay **neutral**; the cool accent appears **only on interactive controls** (chevron, "Details" pill, "What kind?" chip). "critical" is carried by **weight**, not red — severity colour lives in the Issue panel the rows route to.

## Affordance (owner-selected)
The "middle" treatment: subtitle "click a dimension to see what's behind it"; a persistent disclosure chevron ▸/▾ and an always-visible outlined **"Details ▾"** pill on every row (flips to "Hide ▴"); rows stay flat (no card chrome); the Attention-map route remains via the footer link.

## Guards (executable — `window._S10`)
`_assertCafDrilldownHasNoDimensionScore` (no %, no /100, no index on a band — checked on markup + DOM) · `_assertCafDrilldownDriversComputed` (grounded/inferred + severity + finding-type counts computed from state and internally consistent — the per-dimension type and severity counts each sum to the open-issue count). Live self-check **144/144, 0 pageerrors**; existing CAF-bands / neutrality guards unchanged.

## Governance
Route via `dl-land` (owner ratifies; numbered at land per DL-065). The **`ftype` field + its taxonomy mapping** is the canonical touch the owner ratifies; the drill-down UI is product-authored realization. Slices 3 (Overview) & 10 reopened + re-signed off 2026-07-15. AI recommends; only the owner ratifies.

## Provenance
Owner request 2026-07-15 (from the "What's driving it" panel — wanting quantifiable insight below each dimension). Design converged via mockups (lens comparison → hybrid; affordance study → "middle"). Built + verified; owner "lock it in" 2026-07-15.

### Sources
- [CAF_ASSESSMENT_MODEL_V1.md](computer:///Users/macuser/GitHub/oslo-knowledge-base/10_product/domain/CAF_ASSESSMENT_MODEL_V1.md) — §5 (evidence × findings), §8 (finding taxonomy), §9 (Impact Assessment).

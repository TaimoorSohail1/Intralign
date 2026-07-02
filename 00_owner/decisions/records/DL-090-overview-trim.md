# DL-090 — Overview cognitive-load trim + Attention-map as its own surface (amends DL-088)

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (product experience / presentation; non-doctrinal)

- **Source:** Owner direction 2026-07-02 (Overview cognitive-load iteration). Reference of record: `product-design/oslo_r1_experience_mockup_v2.html`. Grounded in DL-088 (Overview §Q — amended here), DL-085 (§P), the Panel Model, `MRI_EXPERIENCE_SPECIFICATION_V1`, `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1`.
- **Layer:** `10_product/experience` (Overview · MRI · Global-Nav). Presentation-only; non-doctrinal.

## Decision
Trim the Project Overview to reduce cognitive load. The Overview presents: **Confidence → a compact "What's driving it" CAF driver-glance → the confidence trend → Start here → Progress → (quiet) project summary.** Removed from the Overview:
- **Reliability component breakdown** — its headline stays on the confidence line; the Coverage/Evidence/Assessability detail folds into the "how this is calculated" explainer.
- **Recommendations summary** — Panel Model: recommendations live only inside a Finding; "Start here" carries the next action.
- **Attention heatmap** — relocated to its **own "Attention map" (MRI) left-rail surface** (the canonical MRI Workspace per Global-Nav), not embedded in the Overview.

CAF driver chips are **qualitative** (level only; per-dimension 0–100 numbers move to drill-in). Amends DL-088 §Q (does not reverse it). Presentation-only — Confidence doctrine, Panel Model, and advisory-only are unchanged.

## Conditions
Presentation-only (no epistemic invariant, object/state model, or contract change); Confidence never bare (band + reliability remain on the confidence line); Panel Model preserved (no orphan recommendation surface); MRI/heatmap stays qualitative (no scores/ranks); the prototype is the reference of record; visual baselines `02-overview` (updated) + `07-attention-map` (new) regenerated to match (#92).

## Supersedes / Amends
Amends `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` (§R — trims the §Q detail-stack), `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1` (Attention-map as its own left-rail surface), `MRI_EXPERIENCE_SPECIFICATION_V1` (reached via its own surface, not embedded in Overview). DL-088 amended, not reversed.

## Provenance
Owner-directed Overview cognitive-load pass; AI analyzed redundancy (Reliability / Recommendations / heatmap duplicated other surfaces), proposed the trim + Attention-map relocation, and benchmarked against readiness-score dashboards (Framework 001A). Owner ratifies; effect on canon at owner merge. Numbered at landing (DL-065).

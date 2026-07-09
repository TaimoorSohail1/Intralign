# DL-096 — Overview surface redesign: confidence-led, low-cognitive-load (RB-037)

- **Date:** 2026-07-08 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner-directed UX refinement, 2026-07-08. Proposal: `00_owner/decisions/PROPOSAL_OVERVIEW_REDESIGN_DRAFT.md` (RB-037). Visual reference of record: `product-design/oslo_r1_overview_redesign_mockup.html`. Grounded in `RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1 §1.2` (neutral maturity ramp; orange = action accent), `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1`, `CONFIDENCE_MODEL_V1`, CAF-01, CONF-05, MRI-06, DL-046, DL-095.
- **Layer:** `10_product/experience` (Overview surface + Confidence presentation) with `10_product` Visual-token usage. Presentation-only; non-doctrinal.

## Decision (ratifiable text)

Adopt the **redesigned Overview surface** per the reference mockup, presentation-only. One focal signal per section; the rest encoded visually; narration behind progressive disclosure.

1. **Confidence section.** The maturity score (value + band) is the single focal read; reliability is a one-line qualifier; change-since-last-run is a quiet trend line. The three CAF dimensions render as **neutral maturity bars** with an always-visible **band word** and **hover/tap detail**; the **lowest dimension carries the single amber attention flag**. Causal narration lives behind a **"Why"** disclosure (auto-opened once after a material user-initiated change, collapsed and sunset thereafter). **Removed:** the ring gauge, the green "your change moved the read" box, and the persistent `Current` / `From OSLO` pills.
2. **Aligned lower sections.** Start here, Progress, and More adopt one grammar: eyebrow + descriptor, dot-and-label chips, neutral tracks with right-aligned counts.
3. **Color discipline.** One meaning per accent — **amber = action/attention, green = good state**, confidence/CAF on the **neutral maturity ramp** — strengthening `Visual §1.2` conformance by removing the green-as-health delta.

## Conditions

- **Presentation-only.** No change to the Confidence Model, CAF Model, scoring, contracts, or object model. CAF band values are already produced by CAF-01; this surfaces them.
- **OWNER-DECISION ITEM (open — do not assume):** the **per-dimension CAF band vocabulary** (placeholder `Strong / Moderate / Limited` in the mockup) must be the **canonical CAF band set**; the owner ratifies the exact vocabulary before the surface is built (Anti-Assumption Protocol).
- **Accessibility.** The band word is the always-visible value; hover/tap only adds detail (touch/keyboard/screen-reader parity).
- **Trend reconciliation.** "Understanding over runs" renders the lightweight understanding timeline (MRI-06) and reconciles with Confidence Stages (CONF-05) and Initial/Extended labels (DL-046) — no new object.
- **Why auto-open** is scoped to material user-initiated change (not every Deep Pass recompute, AE-03) and sunsets.
- **Staleness** is surfaced conditionally but must always present stale understanding as previous/stale (never as current) now that the `Current` pill is removed.

## Realization (landed with the decision)

Amend `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` (Overview layout + Confidence/Start-here/Progress/More sections) and confirm token usage against `RELEASE_1_VISUAL_DESIGN_AND_BRANDING_SPECIFICATION_V1 §1.2`; update the Overview surface in the prototype (v-next). Engineering surfaces per-dimension CAF bands and the hover/tap + Why disclosure layers. Realization timing per owner; folds into the Overview/Issues vertical slice.

## Supersedes / Amends

Amends the Project Overview screen spec and the Confidence presentation; confirms (does not change) Visual §1.2. No doctrine, model, scoring, or object superseded. The green "your change moved the read" delta and the ring gauge are retired from the Overview presentation.

## Provenance

Owner-directed UX iteration 2026-07-08 (confidence panel too prose-heavy / unclear focus). AI proposed data-viz motifs, iterated to the locked leaner design with the owner, and drafted this record — surfacing the CAF band vocabulary as an explicit owner-decision item rather than resolving it. **AI drafted and recommended; the owner ratifies.** Number assigned at landing (DL-065); effect on canon at owner merge.

# PROPOSAL — R1 UX-Surface Reconciliation (prototype-as-baseline)

> **DRAFT for owner ratification (Framework 001).** AI-drafted at owner direction; AI analyzes/recommends, the **owner ratifies**. Route: Backlog → Proposal (this) → Review (Framework 001A, see `RATIFICATION_REVIEWS_001A.md`) → Decision (`DL-PENDING-ux-surface-reconciliation.md`) → spec changes → Changelog. One canon PR in flight (DL-065); branch → PR → green doc-integrity gate → owner merge; never main.

- **Date:** 2026-07-01 · **Status:** Proposed · **Class:** A (product experience / presentation)
- **Layer:** `10_product/experience` (+ `UI_SCREEN_INVENTORY`). **Non-doctrinal** — no epistemic invariant, object model, or advisory-only stance changes.
- **Grounded in:** the ratified R1 experience specs; the interactive prototype `oslo_r1_experience_mockup_v2.html` (owner-authored UX intent); `DESIGN_RECONCILIATION_CHANGESET.md`; `UI_BACKEND_INTEGRATION_MAP.md`. Companion to the confidence-presentation, confidence-calibration, and strategic-chain/positioning proposals.

## Problem

The ratified R1 UX under-delivered largely because it was **under-specified**. The owner authored a high-fidelity, executable prototype to define the intended UX precisely. The prototype is now the intended baseline, but several of its surfaces **diverge from the current experience specs**, and a stale screen-inventory entry conflicts with the ratified Panel Model. Those divergences must be reconciled into canon so the developer builds exactly the prototype, and so the specs stop drifting from intent.

## Proposal

Adopt the **prototype as the authoritative R1 UX baseline** and update the affected experience specs to match it. Specifically:

1. **Project Overview hierarchy (updates `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1`).** Re-sequence the Overview to *Confidence → single "Start here" next-action → progress → (Explore details: CAF · Reliability · Attention)*. The redundant at-a-glance CAF strip is demoted into Explore details (it duplicated the CAF card). Confidence remains reliability-qualified and never bare. Adds a **progress readout** of countable governed objects (findings resolved/open by severity; see confidence-presentation proposal Track 2 for the anti-gamification framing).
2. **Findings as a destination (updates `FINDING_PRESENTATION_SPECIFICATION_V1`; reconciles `GLOBAL_NAV`).** The **Findings list** is a **center-pane workspace** (the canonical "Findings Workspace", `UI_SCREEN_INVENTORY` #8), reachable from the left rail — *consistent with History and Overview*. The **finding detail remains a contextual Panel** (`FINDING_PANEL_SPEC`, unchanged). Adds **Dimension / Severity / Section filters** and a **Group-by (Dimension | Section)** control; default grouping stays Dimension (findings map to the CAF dimensions that drive Confidence).
3. **History as a center pane (updates `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1`).** History is presented as a **center pane** reachable from the left rail, rather than a full-screen overlay — while remaining a **secondary, append-only, read-only** surface (no restore/rollback; viewing changes no assessment).
4. **Application shell / navigation (updates `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1`).** Declutter the top bar (Findings and History move to the **left rail**; the feature tour moves to Settings → Help; the OSLO-panel toggle moves to the **panel edge**). Add a **command palette (⌘K)** and a header search affordance for jump-to navigation and actions — recognition-over-recall for repeat use.
5. **Panel-Model cleanup (updates `UI_SCREEN_INVENTORY`).** **Retire the stale standalone "Recommendation Workspace" (#9).** Recommendations exist **only** inside a Finding (selection = Selected Path in finding context); there is no orphan recommendation surface. This ratifies what the prototype already does and aligns the inventory with `RECOMMENDATION_PANEL_SPEC` and `GLOBAL_NAV`.
6. **Adaptive teaching (updates `HELP_AND_SUPPORT_EXPERIENCE_SPECIFICATION_V1`).** Teaching/coach copy **sunsets by interaction/proficiency** (fades once learned), re-enableable from Settings → Help. Status/feedback copy is exempt.

## Scope decision requested (owner)
- **Command palette (⌘K)** — include in R1 or defer to R2? It has **no backend dependency** and is built. Recommendation: **include** (low cost, high repeat-use fluency).

## Conditions (binding if ratified)
1. **Presentation-only.** No epistemic invariant, object/state model, event/API contract, or advisory-only stance is altered by this proposal.
2. **Panel Model preserved.** Finding and Recommendation **detail** remain contextual panels; only the findings **list** is a destination. No orphan recommendation surface.
3. **Confidence doctrine preserved.** Overview keeps Confidence reliability-qualified and never bare; the number/band presentation is governed by the confidence-presentation + calibration proposals (this proposal does not restate them).
4. **History stays read-only/secondary.** Center-pane presentation does not add actions, restore, or decision-record framing.
5. **Fidelity is enforceable.** "Built exactly as designed" is verified by the visual-regression + acceptance layer in the build repo (screenshot diffs vs the prototype, wired to the doc-integrity gate), not by judgment.
6. **Prototype is the reference of record** for these surfaces; spec text is updated to match it, and the prototype is versioned alongside the specs.

## Concerns
- **Findings-as-destination vs "contextual panel" language** in `GLOBAL_NAV` — mitigated by Condition 2 (list = destination; detail = panel) and by the existing `UI_SCREEN_INVENTORY #8`; owner attention warranted so the nav spec's language is updated cleanly.
- **History prominence** — elevating to a left-rail pane could read as "primary"; Condition 4 keeps it secondary/read-only.
- **Command palette scope** — a genuine scope addition; owner decides include/defer.
- **Spec breadth** — this touches six specs; recommend landing as **one reconciliation PR** (per DL-065 one-in-flight) with the spec edits batched, to keep the change atomic and reviewable.

## Dependencies
`DESIGN_RECONCILIATION_CHANGESET.md` (D5, D6, D8, D10, D11, D12, D15, D19); `UI_BACKEND_INTEGRATION_MAP.md` (findings read/query params, history feed gap G3); confidence-presentation + calibration proposals (Overview confidence behavior); strategic-chain/positioning proposal (plain-language labels used across these surfaces).

## Recommendation
**Accept-in-substance with Conditions 1–6**, command palette **included** in R1. The changes are presentation-level, largely already Panel-Model-aligned, and directly resolve the under-specification that motivated the prototype. Owner ratifies; on ratification the six experience specs + screen inventory update in one reconciliation PR with a Changelog record and a DL-065 decision record.

## Provenance
Owner direction 2026-07-01 to implement the latest prototype exactly and ready it for the developer. AI produced the change-set and integration map, identified the divergences and the stale screen-inventory entry, and drafted this reconciliation (Framework 001A — analysis / conflict identification / recommendation). The **owner ratifies.** Numbered at landing under DL-065.

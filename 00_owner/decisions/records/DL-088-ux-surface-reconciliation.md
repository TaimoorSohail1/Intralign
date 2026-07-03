# DL-088 — R1 UX-surface reconciliation (prototype-as-baseline)

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (product experience / presentation; non-doctrinal)

- **Source:** Owner direction 2026-07-01/02. Proposal: `00_owner/decisions/PROPOSAL_UX_SURFACE_RECONCILIATION_DRAFT.md`; Review: `RATIFICATION_REVIEWS_001A.md` §4. Grounded in the ratified experience specs, the prototype `product-design/oslo_r1_experience_mockup_v2.html`, `DESIGN_RECONCILIATION_CHANGESET.md`, `UI_BACKEND_INTEGRATION_MAP.md`.
- **Layer:** `10_product/experience` (5 specs) + `UI_SCREEN_INVENTORY`. Presentation-only; non-structural.

## Decision
Adopt the prototype as the authoritative R1 UX baseline and update the affected specs: Overview re-sequenced (**Confidence → Start here → progress → Explore details**; the at-a-glance CAF triad demoted into Explore details); **Findings list = center-pane workspace** (finding detail stays a contextual Panel) with **Dimension / Severity / Section filters + Group-by (Dimension | Section)**; **History = center pane** (secondary, read-only); **shell decluttered** (panel-edge OSLO-panel toggle; Findings/History to the left rail; tour to Settings → Help); **teaching sunsets by proficiency**; **retire the stale "Recommendation Workspace" (#9)** (Panel Model — recommendations exist only inside a Finding). **Command palette (⌘K) DEFERRED to R2.** *(Conditions 1–6 per the proposal.)*

## Conditions
Per proposal Conditions 1–6: presentation-only (no epistemic invariant, object/state model, event/API contract, or advisory-only change); **Panel Model preserved** (list = destination, detail = contextual panel; no orphan recommendation surface); Confidence doctrine preserved (governed by DL-085/DL-086); History stays read-only/secondary; fidelity enforced by the visual-regression + acceptance gate; the prototype is the reference of record.

## Supersedes / Amends
Adds ratified-update addenda to `PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1` (§Q), `FINDING_PRESENTATION_SPECIFICATION_V1` (§O), `GLOBAL_NAVIGATION_AND_APPLICATION_SHELL_SPECIFICATION_V1` (§U), `HISTORY_AND_TIMELINE_SURFACE_SPECIFICATION_V1` (§U), `HELP_AND_SUPPORT_EXPERIENCE_SPECIFICATION_V1` (§R); corrects `UI_SCREEN_INVENTORY` (#9 Recommendation Workspace retired). Command palette → R2 backlog. Additive; no prior decision superseded.

## Provenance
AI produced the change-set + integration map, identified the divergences and the stale screen-inventory entry, and drafted the reconciliation (Framework 001A). Owner ratifies; command-palette scope (R2) and clarification scope (R1, separate contract) recorded by owner 2026-07-02. Numbered at landing (DL-065).

# R1 UX Acceptance Criteria (per surface)

> Makes "built exactly as designed" **verifiable**, not trusted. Two gates per surface: **(A) visual** — the built surface matches the committed baseline within `diffThreshold` (see `surfaces.json`); and **(B) structural/behavioral** — the objective checks below, each traceable to a ratified decision (DL-085…089) and to the UI↔backend binding. A surface passes only if **both** gates pass. Baselines are captured from `product-design/oslo_r1_experience_mockup_v2.html` (reference of record). Date: 2026-07-02.

## Global (apply to every surface)
- **Confidence never bare** — wherever Confidence appears it shows band + reliability qualifier; never health/probability framing (DL-085; Interpretation Doctrine).
- **Neutral confidence ramp** — no health-color (red/green) on Confidence/CAF; severity color only on findings (DL-085/086).
- **No ⌘K command palette in R1** — deferred to R2 (DL-088). Its presence is a failure.
- **Advisory-only** — no execution/governance/auto-apply affordance anywhere (DL-043/047).
- **Only reanalysis changes assessment** — no UI action mutates CAF/Reliability/Confidence or closes a finding without a run.

## 01 — Onboarding / intake
- Single primary CTA ("See where I stand"); **one-line** sub-headline (DL-088 C4); "Explore a sample" fast path present.
- No account/creation gates before value (DL-073 ingestion-first).

## 02 — Overview
- **Number-focal Confidence**: the 0–100 index is the visual hero; band + reliability are secondary qualifiers beside it (DL-085; bound to `GET /projects/{pid}/confidence`).
- **5-band** labels only (Very Low / Low / Moderate / High / Very High) (DL-086).
- Sequence: **Confidence → single "Start here" action → Progress readout → Explore details (CAF · Reliability · Attention)** (DL-088); at-a-glance CAF triad lives inside Explore details, not the hero.
- Cause-bound change: a change to the index shows its cause and can move up or down (DL-085; `confidence_recalculated` carries the driving finding — Integration-Map G5).
- Work-ledger counts attested objects only (findings resolved/open by severity); never a second number (DL-085).

## 03 — Findings (center-pane workspace)
- Findings **list is a center pane** (left-rail destination), not a slide-over (DL-088; `GET /projects/{pid}/findings`).
- Filters: **Dimension · Severity · Section**; **Group-by (Dimension | Section)**, default Dimension (DL-088).
- Cards show **title · severity · location · status** only; type/evidence-count/paths in the detail (DL-088 C3).

## 04 — Finding detail (contextual panel)
- Opens as a **contextual panel** over its surface (Panel Model; DL-088).
- Canonical order: header → summary → **evidence → …→ recommendations** (evidence before recommendations) → history → reanalysis (FINDING_PANEL_SPEC).
- Acknowledge / select-path / resolve are distinct; resolution closes only via reanalysis.
- **Clarification answerable in-panel** (DL-089, Option B) → `POST /projects/{pid}/clarification-answers`; answering marks analysis stale, changes no assessment by itself.
- No orphan recommendation surface; recommendations live only here (DL-088; "Recommendation Workspace" retired).

## 05 — Plan section / artifact
- Format by layer: **Understanding = prose**, **Execution = structured tables** (DL-088 / artifact rule).
- Inline weakness spans link to findings; **weakness stepper reads "Jump to weakness · k of N"** (DL-088 C7).
- Edit → autosave → event-driven reanalysis (no manual Reanalyze button); recompute per the stale backbone.

## 06 — History (center pane)
- **Center pane**, secondary, **append-only, read-only** — no restore/rollback/actions (DL-088; HISTORY_SURFACE).
- Prior/current/superseded labels correct; viewing changes nothing.

## 07 — Attention map (its own surface)
- Reached from the **left rail** ("Attention map"), not embedded in the Overview (DL-090; GLOBAL_NAV §V, MRI §S).
- Heatmap cell with 2+ findings opens the **filtered Findings list** (not a single finding); single-finding cell opens that finding's panel.

## 08 — Confidence explainer (the "how this is calculated" popover)
- Opened from the top-bar **Confidence pill**; shows the CAF dimension breakdown **and** the **Reliability basis** — Coverage, Evidence availability, Assessability (DL-085; DL-090 relocation target).
- Reliability is presented as a **qualifier** of Confidence, **determined independently** of Clarity/Alignment/Feasibility — not a fourth dimension and not findings-derived (Interpretation Doctrine; DL-085).
- The reliability components are **not** rendered on the Overview (DL-090 trim) — they live only here and are bound to the reliability read on `GET /projects/{pid}/confidence`.

## Notes for the implementer
- Run visual gate in a **fixed container** (viewport 1440×960, reduced-motion, srgb) so diffs are deterministic; mask genuinely dynamic regions (timestamps) via Playwright `mask` if needed.
- The numeric Confidence value is produced by the **v0 formula** (`30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md`); thresholds are the ratified 5-band map (DL-086). Sub-±7 jitter must not render as a change.

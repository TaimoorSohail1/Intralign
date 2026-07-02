# DL-085 — User-facing Confidence movement & quantified progress presentation

- **Date:** 2026-07-02 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A (Confidence presentation; non-doctrinal — meaning unchanged)

- **Source:** Owner direction 2026-07-01. Proposal: `00_owner/decisions/PROPOSAL_CONFIDENCE_PROGRESS_PRESENTATION_DRAFT.md`; Review: `RATIFICATION_REVIEWS_001A.md` §1. Grounded in `OUTCOME_CONFIDENCE_INTERPRETATION_DOCTRINE_001` (change is cause-based; read with basis; may fall), Master Spec §20 (numeric 0–100 + band both sanctioned), `OPEN_TBD` D1/F1, DL-043 (advisory-only).
- **Layer:** `10_product/experience` (Overview / MRI Confidence presentation) + Confidence Interpretation Doctrine presentation surface. Non-structural (meaning unchanged).

## Decision
Ratify the user-facing Confidence presentation posture: the numeric index is **focal and moves cause-bound** (both directions), **never bare** (always with its band + reliability qualifier), shown **clean** (no "illustrative" caveat in production; a "how this is calculated" affordance instead), with a **quantified work-ledger** of countable governed objects (findings resolved/open by severity) alongside. **No gamification** (no points/streaks; never a score to chase). Numeric 0–100 is already sanctioned (Master Spec §20); this decision governs its *presentation*, not its existence. *(Conditions 1–7 per the proposal.)*

## Conditions
Per proposal Conditions 1–7: never shown bare (band + reliability + cause always present); no permanent on-screen caveat (production shows the number clean; the "illustrative" label is a mockup artifact removed on calibration); downward movement rendered legible and non-alarming; no gamification; Confidence/CAF keep the neutral (non health-color) ramp; the work-ledger counts only attested/governed objects and never restates the signal as a second number; sub-tolerance jitter is not surfaced as change (ties to the Calibration decision).

## Supersedes / Amends
Amends the Confidence-presentation surface of `10_product/experience/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` and `MRI_EXPERIENCE_SPECIFICATION_V1.md`, and adds a presentation addendum to the Outcome Confidence Interpretation Doctrine surface. No prior decision superseded. (Spec-text realization lands on this branch alongside this record.)

## Provenance
AI-drafted at owner direction; surfaced the probability-misread, sub-band-noise, and honest-decrease risks and the two-track (signal + work-ledger) resolution (Framework 001A — analysis / recommendation). The **owner ratifies**; effect on canon occurs at owner merge via the Founder Console. Numbered at landing under DL-065.

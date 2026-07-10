# DL-100 — Reliability qualifier — finalize copy + confirm CONF-06 trigger reuse (closes RB-040)

- **Date:** 2026-07-10 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision
Ratify the final user-facing copy for the Reliability qualifier established by DL-099 (presentation-only; no model, threshold, or invariant change):

- **Quiet-by-default badge** — maps to the Reliability level `R ∈ {High, Moderate, Low}` (Reliability Model v2; v0 Scoring §3): **R = High → "Solid read"** · **R = Moderate → "Partial read"** · **R = Low → "Thin read"**.
- **Loud / divergence message** (shown only when the false-confidence state is present): **"This reads strong, but on thin evidence — treat as provisional."** The message spells out evidence explicitly so the warning is unambiguous.

## Confirmation (DL-099 Review threshold-ownership condition)
The "loud" divergence state renders **exactly when the existing CONF-06 false-confidence flag is raised** — band ∈ {High, Very High} ∧ `R = Low` (per `30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md` §3; 5-band scheme per DL-086; flag per DL-047). It reuses that single source of truth and introduces **no new, separately-tuned threshold**. Any change to the trigger condition is a calibration (Class B) matter for the scoring/calibration surface, not this decision.

## Supersedes / Amends
Finalizes the "copy TBD" placeholder in the DL-099 realization: amends the Reliability-qualifier copy in `10_product/experience/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` §S and `10_product/experience/MRI_EXPERIENCE_SPECIFICATION_V1.md` §T. **Closes RB-040.** Companion to DL-099 / DL-085. No prior decision superseded; no meaning/model change.

## Provenance
RB-040 (owner-directed 2026-07-10). Owner selected the copy 2026-07-10 — quiet badge uses the "read-solidity" wording; the loud message spells out evidence explicitly. CONF-06 reuse verified against v0 Scoring §3 / DL-086 / DL-047. AI analyzed/drafted under Framework 001A; the owner ratifies. Effect on canon occurs at owner merge.

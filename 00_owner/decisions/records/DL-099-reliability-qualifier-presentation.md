# DL-099 — Reliability qualifier presentation — single quiet-by-default state (loud on CONF-06 divergence)

- **Date:** 2026-07-10 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

## Decision
Ratify the user-facing Reliability presentation posture: the three Reliability components (Coverage · Evidence availability · Assessability) compose into a single user-facing "read-solidity" qualifier that is **quiet by default** and **prominent only on divergence** — the high-CAF-on-low-reliability case, i.e. the existing **CONF-06 false-confidence flag**. Full three-component detail remains available **on demand** via the "how this is calculated" affordance. The qualifier is always a **qualifier of the one Confidence index** (never a second number), satisfies the reliability leg of DL-085 "never bare," and uses the **neutral (non health-color) ramp** except where the false-confidence flag intentionally draws attention. Reliability Model V1, its components, the **Independence** and **"qualifies-never-inflates"** invariants, and the false-confidence flag logic are **unchanged** (presentation-only). Companion to DL-085.

## Conditions
Per proposal Conditions 1–7: (1) one displayed state — the three components are never surfaced as three standing readouts; full detail on demand only; (2) quiet by default when reliability is adequate and consistent with CAF; (3) loud on divergence, carrying the plain-language provisional message, divergence-triggered not continuous; (4) never a second number; (5) never bare — band + reliability qualifier + cause always present (DL-085); (6) model unchanged — no change to components, invariants, or flag logic; (7) neutral ramp retained except for the intentional false-confidence flag. Binding threshold-ownership condition (from Review): the "diverged" (loud) trigger reuses the existing CONF-06 false-confidence flag — no new, separately-tuned threshold; any new threshold is a calibration (Class B) item.

## Supersedes / Amends
Amends the Reliability-presentation surface of `10_product/experience/PROJECT_OVERVIEW_SCREEN_SPECIFICATION_V1.md` and `MRI_EXPERIENCE_SPECIFICATION_V1.md`; companion to DL-085. No prior decision superseded. (Spec-text realization lands alongside this record.)

## Provenance
Proposal: `00_owner/decisions/PROPOSAL_RELIABILITY_QUALIFIER_PRESENTATION_DRAFT.md` (PR #132, Framework 001). Review (001A) posted on #132. Owner ratified 2026-07-10. AI analyzed/drafted under Framework 001A; the owner ratifies. Effect on canon occurs at owner merge.

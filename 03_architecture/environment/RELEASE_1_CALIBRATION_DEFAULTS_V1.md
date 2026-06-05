# Release 1 Calibration Defaults v1

**Document Type:** Calibration Parameter Defaults (numeric dials) · **Status:** **Adopted as operative defaults under DL-044 constituent C — 2026-06-04 (tunable; owner may retune any value without a new Decision)** · **Date:** 2026-06-04
**Satisfies:** DL-043 Condition 4 (numeric determinism/drift/band calibration) and the Environment-Profile R5 retention residual — provisionally, with **safe conservative defaults** the owner can tune later. **These are dials, not architecture:** changing any value changes behavior sensitivity, not the model. Per `CLAUDE.md`, the owner ratifies.

> **Why defaults now:** they unblock implementation without forcing premature precision. Every value is **conservative** (errs toward *surfacing* a concern rather than hiding it, consistent with OSLO's anti-false-certainty doctrine) and **independently tunable**. Engineering should treat these as configuration, not constants.

---

## 1. Determinism / Replay Tolerances

*(How close a re-run must match the record to count as conformant — per the two-axis replay model.)*

| Output class | Replay tier | Default tolerance |
|---|---|---|
| **Record replay** (any Cognition History / Acceptance / Attested record) | **exact** | **0** — byte/value-identical; any difference is a Critical trust failure |
| **Rule / formula-derived** (CAF formula step, structural findings, rule confidence) | **exact** | **0** — identical given same inputs + rule version |
| **AI-assisted numeric** (confidence, reliability, outcome confidence) | **band-semantic** | **± 7 points** on a 0–100 scale **and** same band (below) — within tolerance = conformant |
| **AI-assisted textual** (findings, issues, recommendations, clarifications) | **semantic** | **semantic-equivalence** (same finding identity / same recommendation intent); wording may differ |
| **Set-level** (which findings/issues exist) | **set** | **≥ 90%** overlap of stable identities across replay; new/dropped beyond that flags review |

## 2. Confidence Bands (0–100)

*(Where "low / medium / high" start and stop. Used for display and for band-semantic replay stability.)*

| Band | Range | Meaning |
|---|---|---|
| **Low** | **0–49** | understanding is weak/contested — surface prominently |
| **Medium** | **50–74** | partial understanding — usable with caution |
| **High** | **75–100** | well-grounded understanding |

- **Band-edge guard:** a value within **± 3 points of a band boundary** is treated as the **lower** band for display (conservative — never overstate confidence).
- Confidence = **trust in understanding, never project health** (preserved).

## 3. Drift Thresholds

*(How much a value must move before OSLO flags it. Outcome Drift is surfaced as a **feature**; these thresholds decide when it's worth the user's attention.)*

| Drift type | Default trigger | Treatment |
|---|---|---|
| **Outcome / Confidence drift** (a score moved between emissions) | **≥ 10 points** change **or** a **band change** | **surfaced** to user (product feature — "understanding shifted; here's why") |
| **Acceptance-Impact drift** (a value behind a *user-accepted* item moved) | **≥ 10 points** or **band change** vs. the version-pinned acceptance | **surfaced as an Acceptance-Impact alert** ("a decision you confirmed is affected") |
| **Determinism drift** (replay exceeded §1 tolerance) | **any** exceedance | **trust failure** (not a feature) — Critical/Major per QA & Observability Governance |
| **Confidence inflation** (confidence rises without new grounding evidence) | rise **≥ 10 points** with no new Attested input | **trust-failure flag** for investigation |

*(Outcome/Acceptance drift = product signal. Determinism drift / inflation = trust failure. Kept distinct on dashboards per R5.)*

## 4. Retention Durations

| Log / record class | Default retention |
|---|---|
| **Operational logs** (service/runtime telemetry) | **90 days** (per Environment Profile) |
| **Canonical records** (Attested Assertions · Cognition History Records · User Acceptance Records / plan facts) | **retained for project lifetime + 1 year** (append-only; never deleted while the project is active) — these are the system of record |
| **Audit receipts** (integrity-clearance, user-action) | **≥ 1 year** default; **owner to confirm against any compliance regime** (the "per compliance" residual) |

## 5. Status & Tuning

- **All values above are owner-review-pending defaults.** They are **configuration**, surfaced for ops to adjust per environment; none changes the architecture or any contract's structure.
- **Tuning guidance:** lower thresholds = more sensitive (more flags, fewer missed shifts); raise = quieter. Defaults lean **sensitive** by design (surface over suppress).
- **Open for owner:** confirm the **± 7 / 10-point** sensitivities, the **75/50** band edges, and the **audit retention vs. compliance** duration.

---

*This document provides conservative, owner-review-pending numeric defaults satisfying DL-043 Condition 4 and the Environment-Profile retention residual: determinism/replay tolerances (exact for records and rule/formula outputs; ±7 points and same-band for AI-assisted numeric; semantic-equivalence for AI-assisted text; ≥90% set overlap), confidence bands (0–49 low / 50–74 medium / 75–100 high, with a ±3-point conservative band-edge guard), drift thresholds (≥10 points or a band change to surface Outcome/Acceptance drift as a product feature; any replay-tolerance exceedance or unexplained ≥10-point confidence rise as a trust failure), and retention durations (90-day operational logs; project-lifetime+1-year canonical records; ≥1-year audit receipts pending compliance confirmation). All values are tunable configuration that leans toward surfacing over suppressing, change no architecture or contract structure, and are routed to the owner for review.*

**Release 1 Calibration Defaults v1 — proposed, owner-review pending.**

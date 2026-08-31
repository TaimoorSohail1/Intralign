# Evaluate computes on the v0 CAF/Confidence formula, version-pinned; calibration deferred

The CAF/Confidence/Reliability **v2 models** fix the meaning, structure, properties, and
bands of the scores but deliberately defer the **aggregation arithmetic** to "future
calibration". Without a formula, the Evaluate slice cannot produce the 0–100 confidence the
MRI needs. The **v0 provisional formula** (`30_engineering/scoring/CAF_CONFIDENCE_V0_SCORING_FORMULA_V1.md`)
supplies arithmetic that provably satisfies the ratified doctrine (co-equal dimensions,
"between an average and a minimum" via power-mean p≤1 with an ε floor, multiplicative
per-finding impact, reliability as a separate qualifier — never multiplied in).

We adopt v0 for Release 1 build and test. Its `rule_version` is **pinned into the
determinism baseline** so rule-arithmetic replays **exact** (AI-derived inputs to the
formula remain ±7/band per ADR-0004). We **scaffold the calibration harness** but add **no
hard numeric pass/fail thresholds** — the calibrated `p` / `ε` / impact-magnitude table
(Calibration §4h) and thresholds stay deferred, set by the owner from real data. This is
exactly the `ANTI_ASSUMPTION_BUILD_PROTOCOL` rule: build the structure and scaffold the
metric; do not invent the numbers.

## Status

accepted — owner ratifies v0 for R1 build/test, 2026-06-16. The **canonical** formula
remains an owner-calibration decision (Open-TBD F1); v0 unblocks build until then.

## Considered Options

- **Wait for an owner-calibrated formula** — rejected: stalls the entire Evaluate output
  (Confidence / CAF / Outcome Confidence), the core of Wave B.
- **Adopt v0, pin version, scaffold calibration, defer numbers (chosen)** — unblocks build
  while keeping the calibrated values an explicit, deferred owner decision; consistent with
  Open-TBD F1, which now states R1 needs a v0 to compute/test against.

## Consequences

- v0 parameters live in Calibration Defaults §4h and are **owner-review-pending**; changing
  them bumps the `rule_version` and therefore the determinism baseline (a new baseline, not
  a regression — DT-6).
- v0 introduces **no new** dimension, finding, entity, state, probability, or
  project-health concept — it realises deferred arithmetic only. Confidence stays banded,
  reliability-qualified, "trust in understanding, never project health" (negative tests
  enforce).
- The calibration harness records the inputs needed to fit `p`/`ε`/impact magnitudes later,
  but asserts no threshold until the owner sets one.
- False-Confidence Detection (CONF-06) is built against v0 outputs (flag high confidence on
  weak understanding; mandatory QA negative).

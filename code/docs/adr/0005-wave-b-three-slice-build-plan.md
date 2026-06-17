# Wave B is built as three sequential slices: Synthesis → Infer → Evaluate

Phase III / Wave B (Understanding) spans three ratified contracts:
`IC/QA/OBS-WS-SYNTH` (synthesis engine, DL-047), `IC/QA/OBS-WB-INFER` (Finding), and
`IC/QA/OBS-WB-EVAL` (Issue / Confidence / Reliability / CAF / Outcome Confidence). The
Wave B `IMPLEMENTATION_PLAN` sequences Infer then Evaluate; DL-047 requires the Synthesis
Engine built **with/before** Wave B because Findings need a synthesized planning model to
analyse.

We build these as **three sequential deep-task slices, one contract each**, one fresh
worker per slice, reviewed and approved before the next begins — the same discipline that
carried Wave A (DTM-0001…0008). Synthesis lands first (it produces the
`SynthesizedPlanningModel` + `PlanningArtifact`s that Infer reads), then Infer (Findings
from Attested content), then Evaluate (scores the Findings).

This is the first wave where AI enters the codebase, so each slice also carries its first
real `llm_provider` wiring and recorded-model-response fixtures (ADR-0004), and its scoring
math (ADR-0006, the Evaluate slice).

## Status

accepted — owner direction, 2026-06-16. Coding starts only after per-wave owner
authorization (DL-044 condition 2) and the readiness gate.

## Considered Options

- **Two slices (Synthesis+Infer combined, Evaluate second)** — rejected: a larger first
  slice mixing two contracts, harder to review, weaker traceability.
- **Three slices, one contract each (chosen)** — most reviewable; clean contract→slice
  traceability; synthesis available before Findings depend on it.

## Consequences

- Slice order is a hard dependency chain: WS-SYNTH → WB-INFER → WB-EVAL. A slice is not
  started until the prior slice is approved.
- Each slice is vertical and independently verifiable, carries positive AND negative suites
  (the "confidence-as-health" and "Derived-as-Attested" prohibitions are mandatory
  negatives), emits its OBS events, and appends CHRs via the existing 00R backbone.
- Both Fast Pass (synchronous, &lt;60s Time-to-First-MRI orientation) and Deep Pass (async,
  via the 00R graph) are exercised within the slices; emissions carry `mode` +
  `confidence_stage` (Orientation → Expanded → Validated) as attributes (DL-046).
- The `infer`/`evaluate` responsibility stubs and the `stage_infer`/`stage_evaluate`
  placeholders in `orchestration/graphs/deep_pass.py` are replaced with real
  implementations registered via `orchestration.register_stage()`.
- Detailed slice scope, test mapping, and DoD live in
  `code/docs/deep-tasks/waveb-understanding-deep-task/deep-task-plan.md`.

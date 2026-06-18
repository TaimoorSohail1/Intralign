"""Evaluate — assessment. Sole producer of Confidence / CAFAssessment / Issue (Derived).

Public surface (DTM-0011 / Wave B; IC-WB-EVAL):

- ``EvaluateEngine`` / ``EvaluationResult`` — severity → Issue + the v0
  CAF/Confidence/Reliability/OutcomeConfidence assessment (scoring is EXACT
  under the pinned ``CAF_RULE_VERSION``).
- ``run_evaluate_stage`` / ``build_evaluate_stage`` — the injected ``evaluate``
  stage (CHR per value via ``ctx.chr_repo``; events; recompute supersedes).
- ``scoring`` / ``config`` — the v0 arithmetic + the Calibration §4h dials.
- ``CalibrationRecorder`` — the calibration-harness scaffold (records inputs to
  fit ``p``/``ε``/the impact table; asserts NO numeric threshold — Anti-Assumption).
"""

from backend.responsibilities.evaluate.calibration import (
    CalibrationRecorder,
    CalibrationSample,
)
from backend.responsibilities.evaluate.engine import EvaluateEngine, EvaluationResult
from backend.responsibilities.evaluate.scoring import (
    CAF_RULE_VERSION,
    band_for,
    per_dimension_index,
    power_mean,
)
from backend.responsibilities.evaluate.stage import (
    OUTPUT_KIND_CAF,
    OUTPUT_KIND_CONFIDENCE,
    OUTPUT_KIND_ISSUE,
    OUTPUT_KIND_OUTCOME_CONFIDENCE,
    OUTPUT_KIND_RELIABILITY,
    build_evaluate_stage,
    run_evaluate_stage,
)

__all__ = [
    "CAF_RULE_VERSION",
    "OUTPUT_KIND_CAF",
    "OUTPUT_KIND_CONFIDENCE",
    "OUTPUT_KIND_ISSUE",
    "OUTPUT_KIND_OUTCOME_CONFIDENCE",
    "OUTPUT_KIND_RELIABILITY",
    "CalibrationRecorder",
    "CalibrationSample",
    "EvaluateEngine",
    "EvaluationResult",
    "band_for",
    "build_evaluate_stage",
    "per_dimension_index",
    "power_mean",
    "run_evaluate_stage",
]

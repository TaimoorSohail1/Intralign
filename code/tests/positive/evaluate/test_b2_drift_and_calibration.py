"""QA-WB-EVAL B2 — drift surfaced (≥10 pts or band change) + the calibration
harness scaffold (records inputs to fit p/ε/impact; asserts NO numeric threshold).
"""

from __future__ import annotations

from backend.responsibilities.evaluate.calibration import CalibrationRecorder
from backend.responsibilities.evaluate.config import (
    DIMENSION_FLOOR_EPSILON,
    IMPACT_MAGNITUDE_TABLE,
    POWER_MEAN_EXPONENT,
)
from backend.responsibilities.evaluate.scoring import band_for
from tests.positive.evaluate.helpers import (
    PROJECT,
    conflict,
    engine,
    risk,
    synthesized_model,
)

# Calibration §3 — Outcome/Confidence drift surfaces at ≥10 points OR a band change.
_DRIFT_POINTS = 10.0


def _drift_surfaced(before: float, after: float) -> bool:
    return abs(before - after) >= _DRIFT_POINTS or band_for(before) != band_for(after)


def test_b2_confidence_drop_of_at_least_10_points_is_drift() -> None:
    eng = engine()
    strong = eng.assess(project_id=PROJECT, findings=[], model=synthesized_model())
    weak = eng.assess(
        project_id=PROJECT, findings=[conflict(), risk()], model=synthesized_model()
    )
    delta = strong.outcome_confidence.index - weak.outcome_confidence.index
    assert delta >= _DRIFT_POINTS
    assert _drift_surfaced(strong.outcome_confidence.index, weak.outcome_confidence.index)


def test_b2_band_change_is_drift_even_under_10_points() -> None:
    # A small index move that crosses a band boundary still surfaces as drift.
    assert band_for(78.0) != band_for(74.0)        # high vs medium (a band change)
    assert _drift_surfaced(78.0, 74.0)             # surfaced despite < 10 pts


# ---- calibration harness scaffold (Anti-Assumption: NO numeric threshold) ----


def test_b2_calibration_recorder_records_inputs_without_judging() -> None:
    recorder = CalibrationRecorder()
    eng = engine()
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    impacts = {
        "feasibility": [IMPACT_MAGNITUDE_TABLE["significant"]],
    }
    sample = recorder.record(
        project_id=PROJECT,
        dimension_indices={d.dimension: d.index for d in result.caf.dimensions()},
        dimension_impacts=impacts,
        outcome_index=result.outcome_confidence.index,
        outcome_band=result.outcome_confidence.band,
        reliability=result.reliability.level,
        label="envelope-fixture",
    )
    assert sample.rule_version == "wb-eval-caf-v0"
    assert recorder.samples == [sample]
    # The recorder makes NO pass/fail judgement (no threshold attribute exists).
    assert not hasattr(sample, "passed")
    assert not hasattr(recorder, "threshold")


def test_b2_calibration_recorder_serializes_for_owner_fitting() -> None:
    recorder = CalibrationRecorder()
    recorder.record(
        project_id=PROJECT, dimension_indices={"clarity": 100.0},
        dimension_impacts={"clarity": []}, outcome_index=100.0,
        outcome_band="high", reliability="high",
    )
    jsonl = recorder.to_jsonl()
    assert '"rule_version": "wb-eval-caf-v0"' in jsonl
    assert '"outcome_index": 100.0' in jsonl


def test_b2_v0_parameters_are_config_dials_not_hardcoded_thresholds() -> None:
    """The v0 params live in config (Calibration §4h) — tunable, not asserted gates."""
    assert POWER_MEAN_EXPONENT == -0.5
    assert DIMENSION_FLOOR_EPSILON == 5.0
    assert IMPACT_MAGNITUDE_TABLE["material"] == 0.55
    # No test anywhere asserts "score must be >= X" — the threshold is owner-TBD (F1).

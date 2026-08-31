"""QA-WB-EVAL B2 — determinism: the v0 rule arithmetic replays EXACT under the
pinned ``CAF_RULE_VERSION``; AI-derived input jitter stays within ±7 & same band.
"""

from __future__ import annotations

from backend.responsibilities.evaluate.config import IMPACT_MAGNITUDE_TABLE
from backend.responsibilities.evaluate.scoring import (
    CAF_RULE_VERSION,
    band_for,
    per_dimension_index,
    power_mean,
)
from tests.positive.evaluate.helpers import (
    PROJECT,
    coverage_gap,
    engine,
    risk,
    synthesized_model,
)


def test_b2_rule_version_is_pinned() -> None:
    assert CAF_RULE_VERSION == "wb-eval-caf-v0"


def test_b2_identical_inputs_replay_exact_index_and_band() -> None:
    """Same findings + model + rule version → byte-identical index (exact tier)."""
    findings = [coverage_gap(), risk()]
    model = synthesized_model()
    a = engine().assess(project_id=PROJECT, findings=findings, model=model)
    b = engine().assess(project_id=PROJECT, findings=findings, model=model)
    assert a.outcome_confidence.index == b.outcome_confidence.index
    assert a.outcome_confidence.band == b.outcome_confidence.band
    assert a.caf.clarity.index == b.caf.clarity.index
    assert a.caf.feasibility.index == b.caf.feasibility.index
    # The rule version is stamped on every value (the determinism baseline).
    assert a.outcome_confidence.model_or_rule_version == CAF_RULE_VERSION
    assert a.confidence.model_or_rule_version == CAF_RULE_VERSION


def test_b2_per_dimension_arithmetic_is_exact() -> None:
    # The Π reduction is exact given the same impacts.
    impacts = [IMPACT_MAGNITUDE_TABLE["moderate"], IMPACT_MAGNITUDE_TABLE["minor"]]
    assert per_dimension_index(impacts) == per_dimension_index(impacts)


def test_b2_ai_impact_jitter_stays_within_band_and_pm7() -> None:
    """A small impact-sizing jitter (AI tier) stays ±7 and same band (DT tolerance)."""
    base = per_dimension_index([IMPACT_MAGNITUDE_TABLE["minor"]])
    # Simulate the AI sizing landing one notch lighter (trivial) — band-semantic.
    jittered = per_dimension_index([IMPACT_MAGNITUDE_TABLE["trivial"]])
    assert abs(base - jittered) <= 7.0  # within the ±7 numeric tolerance
    assert band_for(base) == band_for(jittered)  # same band (band-semantic)


def test_b2_power_mean_is_symmetric_in_the_dimensions() -> None:
    # Co-equal dims: the aggregate is invariant to dimension order (no weights).
    assert power_mean([80, 60, 40]) == power_mean([40, 80, 60])

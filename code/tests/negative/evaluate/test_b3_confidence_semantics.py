"""QA-WB-EVAL B3 — Confidence is trust in UNDERSTANDING, never project health
*(Critical)* + CONF-06 false-confidence-without-a-flag *(negative)*.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from backend.responsibilities.evaluate import engine as engine_mod
from shared.epistemic import Confidence, OutcomeConfidence
from tests.positive.evaluate.helpers import PROJECT, engine, risk, synthesized_model


def test_b3_confidence_shape_forbids_a_health_or_probability_field() -> None:
    """Confidence is NEVER project health/probability/score (the shape forbids it)."""
    for forbidden in ("project_health", "health", "probability", "readiness", "score"):
        with pytest.raises(ValidationError):
            Confidence(
                project_id=PROJECT, index=80.0, band="high",
                reliability_qualifier="high", basis=("b",),
                model_or_rule_version="wb-eval-caf-v0", mode="fast",
                **{forbidden: 0.9},  # extra='forbid' rejects it
            )


def test_b3_outcome_confidence_shape_forbids_a_health_field() -> None:
    for forbidden in ("project_health", "probability", "readiness", "score"):
        with pytest.raises(ValidationError):
            OutcomeConfidence(
                project_id=PROJECT, index=80.0, band="high",
                reliability_qualifier="high", basis=("b",),
                model_or_rule_version="wb-eval-caf-v0", mode="fast",
                **{forbidden: 0.9},
            )


def test_b3_engine_never_renders_confidence_as_a_project_health_number() -> None:
    """The produced Confidence surfaces a BAND + basis — never a health/probability field."""
    result = engine().assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    dumped = result.confidence.model_dump()
    # No project-health / probability / readiness / score key leaks into the value.
    for forbidden in ("project_health", "health", "probability", "readiness", "score"):
        assert forbidden not in dumped
    # The user-facing value is the BAND; it reduces to its basis (not a bare number).
    assert result.confidence.band in ("low", "medium", "high")
    assert result.confidence.basis


def test_b3_false_confidence_is_never_silently_dropped_conf06() -> None:
    """CONF-06 — a high band on low reliability MUST raise the flag (not be hidden)."""
    result = engine().assess(
        project_id=PROJECT, findings=[], model=synthesized_model(n_assumptions=5)
    )
    # The dangerous 4th state exists here (high band + low reliability)...
    assert result.outcome_confidence.band == "high"
    assert result.reliability.level == "low"
    # ...and the flag is RAISED — a high-confidence-over-weak-understanding value
    # without the flag would be the rejected negative.
    assert result.outcome_confidence.false_confidence_flagged is True


def test_b3_reliability_is_not_multiplied_into_the_confidence_number() -> None:
    """Reliability qualifies; it never enters the arithmetic (Non-Collapse)."""
    src = inspect.getsource(engine_mod)
    # The band is computed from the INDEX only; reliability is attached alongside.
    assert "band_for(outcome_index)" in src
    # Two runs, identical CAF, different reliability → identical index (proven in
    # positive too; re-asserted here as the negative of "reliability changed it").
    strong = engine().assess(
        project_id=PROJECT, findings=[risk()], model=synthesized_model(n_assumptions=0)
    )
    weak = engine().assess(
        project_id=PROJECT, findings=[risk()], model=synthesized_model(n_assumptions=5)
    )
    assert strong.outcome_confidence.index == weak.outcome_confidence.index

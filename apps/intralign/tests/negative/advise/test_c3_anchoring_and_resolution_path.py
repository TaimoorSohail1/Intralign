"""QA-WC-ADVISE C2 (negative) — anchoring is mandatory; Resolution Paths are
presentation-only (no standalone object).

- standalone / unanchored Recommendation rejected (Major) — structurally
  impossible (the ``anchor`` field is required + non-empty) AND a model that
  returns an unanchored item is DROPPED by the engine (never admitted).
- a standalone Resolution-Path OBJECT rejected (Major) — Advise builds NO such
  object; alternatives persist as MULTIPLE Recommendations.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from backend.responsibilities.advise import engine as engine_mod
from backend.responsibilities.advise import stage as stage_mod
from shared.epistemic import Recommendation
from tests.positive.advise.helpers import (
    COVERAGE_GAP_ID,
    PROJECT,
    advise_engine,
    coverage_gap,
)


def test_c3_standalone_recommendation_is_structurally_impossible() -> None:
    """Major — a Recommendation with NO anchor is rejected at construction."""
    with pytest.raises(ValidationError):
        Recommendation(
            project_id=PROJECT, recommendation_id="r",
            recommendation_type="suggested_action",
            summary="x", model_or_rule_version="wc-advise-v0", mode="fast",
            # no anchor → required field missing
        )


def test_c3_empty_anchor_recommendation_is_rejected() -> None:
    """Major — an empty-string anchor is rejected (min_length=1)."""
    with pytest.raises(ValidationError):
        Recommendation(
            project_id=PROJECT, recommendation_id="r",
            recommendation_type="suggested_action", anchor="",
            summary="x", model_or_rule_version="wc-advise-v0", mode="fast",
        )


def test_c3_model_returned_unanchored_recommendation_is_dropped() -> None:
    """Major — a model recommendation whose anchor resolves to nothing is DROPPED.

    The engine only admits a Recommendation whose anchor is one of the real
    Finding/Issue ids it was given; an unanchored/wrong-anchor item never becomes
    a standalone Recommendation.
    """
    engine, _ = advise_engine(step_to_key={"recommendation": "recommendation_unanchored"})
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap()])
    # The recommendation pass's only item anchors to "nonexistent-id" → dropped:
    # NO suggested_action/candidate_improvement is admitted. (DTM-0015's separate
    # 'validation' pass anchors legitimately and is additive — not from this pass.)
    c1 = [r for r in result.recommendations
          if r.recommendation_type in ("suggested_action", "candidate_improvement")]
    assert c1 == []
    # Every admitted recommendation is still anchored to a REAL id (never standalone).
    assert all(r.anchor == COVERAGE_GAP_ID for r in result.recommendations)


def test_c3_advise_builds_no_standalone_resolution_path_object() -> None:
    """Major — Resolution Paths are presentation-only; Advise builds NO object.

    There is no ResolutionPath type and the advise modules never construct one;
    alternatives are MULTIPLE Recommendations (proven in the positive suite).
    """
    import shared.epistemic as epistemic

    assert not hasattr(epistemic, "ResolutionPath")
    assert "ResolutionPath" not in getattr(epistemic, "CANONICAL_OUTPUTS", ())
    for mod in (engine_mod, stage_mod):
        src = inspect.getsource(mod)
        assert "ResolutionPath" not in src
        assert "resolution_path" not in src.lower() or "no standalone" in src.lower()


def test_c3_multiple_alternatives_are_separate_recommendations_not_one_object() -> None:
    """The alternatives the fixture returns are distinct Recommendations, not merged."""
    engine, _ = advise_engine()
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap()])
    # Each is its own Recommendation object with its own id — never a single
    # path object holding a list of options.
    ids = [r.recommendation_id for r in result.recommendations]
    assert len(ids) == len(set(ids))  # distinct objects
    assert all(isinstance(r, Recommendation) for r in result.recommendations)

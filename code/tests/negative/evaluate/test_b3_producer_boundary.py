"""QA-WB-EVAL B3 — Evaluate's producer boundary (forbidden behaviors).

Evaluate is the SINGLE producer of Issue / Severity / Confidence / Reliability /
CAF / OutcomeConfidence ONLY. It must NOT generate Findings (Infer's) or
recommendations/clarifications (Advise's), and must not write canonical /
promote to Attested. These are negative-PROVEN structurally (the engine exports
no such producer; the shapes forbid the fields).
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from backend.responsibilities import evaluate as evaluate_pkg
from backend.responsibilities.evaluate import engine as engine_mod
from shared.epistemic import EpistemicState, Issue
from tests.positive.evaluate.helpers import PROJECT, coverage_gap, engine, risk, synthesized_model


def test_b3_evaluate_exports_no_finding_or_recommendation_producer() -> None:
    """Evaluate does NOT generate Findings (Infer) or Recommendations (Advise)."""
    public = set(evaluate_pkg.__all__)
    for forbidden in ("FindingEngine", "derive", "Recommendation", "ClarificationRequest",
                      "SuggestedFix", "Advise"):
        assert forbidden not in public
    src = inspect.getsource(engine_mod)
    # The engine never constructs a Finding / Recommendation / Clarification.
    assert "Finding(" not in src       # it READS Findings; it never builds one
    assert "Recommendation(" not in src
    assert "ClarificationRequest(" not in src


def test_b3_evaluate_outputs_are_all_derived_never_attested() -> None:
    result = engine().assess(
        project_id=PROJECT, findings=[coverage_gap(), risk()], model=synthesized_model()
    )
    for value in (result.confidence, result.reliability, result.caf,
                  result.outcome_confidence, *result.issues):
        assert value.epistemic_state == EpistemicState.DERIVED
        assert not value.is_canonical


def test_b3_value_cannot_be_constructed_as_attested() -> None:
    """The Derived layer NEVER writes to the canonical store as Attested (rule #2)."""
    with pytest.raises(ValidationError):
        Issue(
            project_id=PROJECT, issue_id="i", finding_id="f", finding_type="gap",
            severity="moderate", summary="x", evidence_anchors=("a",),
            model_or_rule_version="wb-eval-caf-v0", mode="fast",
            epistemic_state=EpistemicState.ATTESTED_OSLO,  # forbidden
        )


def test_b3_issue_carries_no_recommendation_or_resolution_field() -> None:
    """An Issue has NO recommendation/clarification/resolution field (Advise's)."""
    with pytest.raises(ValidationError):
        Issue(
            project_id=PROJECT, issue_id="i", finding_id="f", finding_type="gap",
            severity="moderate", summary="x", evidence_anchors=("a",),
            model_or_rule_version="wb-eval-caf-v0", mode="fast",
            recommendation="do the thing",  # extra='forbid' rejects it
        )


def test_b3_evaluate_does_not_accept_an_interpretation_as_truth() -> None:
    """No acceptance: Evaluate exposes no accept/confirm/attest method (user-owned)."""
    methods = {name for name, _ in inspect.getmembers(engine().__class__, inspect.isfunction)}
    for forbidden in ("accept", "confirm", "attest", "promote", "resolve_conflict"):
        assert forbidden not in methods

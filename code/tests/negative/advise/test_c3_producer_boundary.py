"""QA-WC-ADVISE C2 (negative) — Advise's producer boundary (forbidden behaviors).

Advise is the SINGLE producer of Recommendation + ClarificationRequest ONLY. It
must NOT evaluate/score (Evaluate's), generate Findings (Infer's), write canonical
/ promote to Attested, govern/authorize/execute, or ACCEPT its own output
(acceptance is the user's — DL-055; Wave U). These are negative-PROVEN
structurally: the engine/stage export no such producer and the shapes forbid the
fields. (Advise proposes, never disposes.)

Failure classification: Critical — Advise governs/authorizes/executes or
self-accepts; writes canonical. Major — unanchored recommendation;
Resolution-Path-as-object.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from backend.responsibilities import advise as advise_pkg
from backend.responsibilities.advise import engine as engine_mod
from backend.responsibilities.advise import stage as stage_mod
from shared.epistemic import ClarificationRequest, EpistemicState, Recommendation


def test_c3_advise_exports_no_evaluate_accept_or_execute_producer() -> None:
    """Advise does NOT score/evaluate, accept, govern, authorize, or execute."""
    public = set(advise_pkg.__all__)
    for forbidden in (
        "EvaluateEngine", "FindingEngine", "Issue", "Confidence", "CAFAssessment",
        "accept", "approve", "govern", "authorize", "execute", "apply",
        "UserAcceptanceRecord", "Authority",
    ):
        assert forbidden not in public


def test_c3_advise_modules_never_score_govern_execute_or_self_accept() -> None:
    """No source-level evaluating/governing/executing/self-accepting in advise."""
    for mod in (engine_mod, stage_mod):
        src = inspect.getsource(mod)
        # Advise reads Findings/Issues; it never CONSTRUCTS an assessment value…
        assert "Issue(" not in src
        assert "Confidence(" not in src
        assert "CAFAssessment(" not in src
        assert "OutcomeConfidence(" not in src
        # …nor a Finding (Infer's)…
        assert "Finding(" not in src
        # …and exposes no accept/approve/govern/authorize/execute producer.
        for forbidden in (
            "def accept", "def approve", "def govern", "def authorize",
            "def execute", "def apply_fix", "def self_accept",
        ):
            assert forbidden not in src


def test_c3_advise_engine_exposes_no_acceptance_or_execution_method() -> None:
    from backend.responsibilities.advise.engine import AdviseEngine

    methods = {
        name for name, _ in inspect.getmembers(AdviseEngine, inspect.isfunction)
    }
    for forbidden in (
        "accept", "approve", "confirm", "attest", "promote", "govern",
        "authorize", "execute", "apply", "resolve_conflict", "score", "evaluate",
    ):
        assert forbidden not in methods


def test_c3_recommendation_outputs_are_all_derived_never_attested() -> None:
    from tests.positive.advise.helpers import PROJECT, coverage_gap, advise_engine

    engine, _ = advise_engine()
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap()])
    for rec in result.recommendations:
        assert rec.epistemic_state == EpistemicState.DERIVED
        assert not rec.is_canonical


def test_c3_recommendation_cannot_be_constructed_as_attested() -> None:
    """The Derived layer NEVER writes Advise output to canonical as Attested (rule #2)."""
    with pytest.raises(ValidationError):
        Recommendation(
            project_id="p", recommendation_id="r", recommendation_type="suggested_action",
            anchor="finding-1", summary="x", model_or_rule_version="wc-advise-v0",
            mode="fast",
            epistemic_state=EpistemicState.ATTESTED_OSLO,  # forbidden
        )


def test_c3_advise_self_accept_is_structurally_impossible() -> None:
    """CRITICAL — Advise cannot mark its own Recommendation accepted (DL-055).

    The Recommendation ``state`` is pinned to ``generated``; any acceptance state
    out of Advise is rejected at construction (acceptance is the user's, Wave U).
    """
    with pytest.raises(ValidationError):
        Recommendation(
            project_id="p", recommendation_id="r", recommendation_type="suggested_action",
            anchor="finding-1", summary="x", model_or_rule_version="wc-advise-v0",
            mode="fast", state="accepted",  # forbidden — Advise emits 'generated' only
        )


def test_c3_recommendation_carries_no_severity_score_or_accept_field() -> None:
    """CRITICAL/Major — a Recommendation has NO severity/score (Evaluate's) nor
    accept/execute field (the user's / Future)."""
    for bad_field in ("severity", "score", "confidence", "accepted", "executed",
                      "resolution_path"):
        with pytest.raises(ValidationError):
            Recommendation(
                project_id="p", recommendation_id="r",
                recommendation_type="suggested_action", anchor="finding-1",
                summary="x", model_or_rule_version="wc-advise-v0", mode="fast",
                **{bad_field: "nope"},  # extra='forbid' rejects it
            )


def test_c3_clarification_carries_no_answer_or_acceptance_field() -> None:
    for bad_field in ("answer", "severity", "accepted", "resolution"):
        with pytest.raises(ValidationError):
            ClarificationRequest(
                project_id="p", clarification_id="c", anchor="finding-1",
                question="why?", model_or_rule_version="wc-advise-v0", mode="fast",
                **{bad_field: "nope"},
            )

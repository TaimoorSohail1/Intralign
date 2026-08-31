"""Recorded-fixture harness self-test for the WB-INFER Finding fixture (ADR-0004).

NOT a "replay" (reserved — event-log reconstruction that does not re-run the
LLM; CONTEXT.md Register). It lives under tests/replay/ only because that is the
determinism-harness home, and it proves the DTM-0010 Finding derivation runs
ENTIRELY on recorded responses — PR CI makes ZERO provider calls. The two-axis
discipline (OBS-WB-INFER): record-exact for the model's recorded output;
derivation semantic for AI Findings, exact for rule-structural gaps/conflicts.
"""

from __future__ import annotations

import sys

from backend.responsibilities.infer.finding import FindingEngine
from backend.services.llm_provider import LLMProvider, live_calls_enabled
from shared.epistemic import SynthesizedPlanningModel
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    load_fixture,
    response_key_directive,
)

_PROJECT = "11111111-1111-1111-1111-111111111111"
_IDS = ["assertion-0", "assertion-1", "assertion-2", "assertion-3"]


def _model() -> SynthesizedPlanningModel:
    return SynthesizedPlanningModel(
        project_id=_PROJECT, model_version="ws-synth-llm-v0",
        intent_summary="Ship billing.", scope_summary="Deliver billing.",
        derived_from_assertions=tuple(_IDS), mode="fast",
    )


def test_wb_infer_fixture_carries_a_baseline_stamp() -> None:
    fixture = load_fixture("wb_infer_v0")
    assert fixture.model_version
    assert fixture.config
    assert "risk" in fixture.responses
    assert "alignment" in fixture.responses


def test_finding_derivation_runs_entirely_on_recorded_responses() -> None:
    """The AI Finding passes serve recorded output — zero live provider calls."""
    session = build_recorded_model("wb_infer_v0")
    provider = LLMProvider(recorded_model=session.model())
    engine = FindingEngine(provider=provider, prompt_suffix_for=response_key_directive)
    before = set(sys.modules)
    result = engine.derive(
        project_id=_PROJECT, assertions=[], assertion_ids=_IDS,
        model=_model(), declared_outcome="Deliver billing.", outcome_anchor="outcome-ref",
    )
    # The two AI passes (alignment + risk) were served by the fixture, not a provider.
    assert session.call_count == 2
    assert set(session.served_keys) == {"alignment", "risk"}
    # Record-exact axis: the recorded risk Findings are present, anchored.
    assert any(f.finding_type == "risk" for f in result.findings)
    # Exercising the harness imported no provider SDK.
    newly = set(sys.modules) - before
    assert not any(
        m.startswith(("pydantic_ai.models.openai", "pydantic_ai.models.anthropic"))
        for m in newly
    )


def test_pr_ci_never_enables_live_calls() -> None:
    assert not live_calls_enabled()

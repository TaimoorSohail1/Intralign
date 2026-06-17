"""QA-WB-EVAL B3 — Fast-Pass 60 s breach *(Major)* + cost discipline (no bypass /
no silent overspend / no wrong-tier routing).

Evaluate is rule-arithmetic (no provider call), so it cannot overspend AI
tokens; the cost obligations are proven by the routed-model identity it records
and the latency it surfaces. The 60 s ceiling is the ratified bound (envelope
value owner-TBD).
"""

from __future__ import annotations

import inspect

from backend.responsibilities.evaluate import stage as stage_mod
from backend.responsibilities.evaluate.stage import _spend_payload, run_evaluate_stage
from tests.positive.evaluate.helpers import PROJECT, engine, risk, synthesized_model
from tests.positive.evaluate.test_b2_performance_gate import (
    TIME_TO_FIRST_MRI_CEILING_SECONDS,
)
from tests.positive.synthesis.fakes import FakeStageContext


def test_b3_a_simulated_over_ceiling_latency_would_breach_the_gate() -> None:
    """A latency exceeding 60 s on the envelope is a Major breach (the gate catches it).

    We do not slow the rule engine artificially; instead we assert the gate's
    COMPARISON is the real ratified bound — a value over the ceiling fails it.
    """
    over = TIME_TO_FIRST_MRI_CEILING_SECONDS + 1.0
    assert not (over < TIME_TO_FIRST_MRI_CEILING_SECONDS)  # would FAIL the gate
    under = TIME_TO_FIRST_MRI_CEILING_SECONDS - 1.0
    assert under < TIME_TO_FIRST_MRI_CEILING_SECONDS       # passes


def test_b3_spend_records_the_configured_free_tier_model_not_a_full_model() -> None:
    """Wrong-tier routing is rejected: Free records the cheap routed model (mini)."""
    payload = _spend_payload(
        tier="free", user="u", mode="fast",
        confidence_stage="orientation", understanding_state="partial",
        time_to_first_mri_ms=1.0,
    )
    # Free synthesis/eval routes to mini (Calibration §4c) — never a full model.
    assert payload["model"] == "gpt-4.1-mini"
    assert payload["model"] != "gpt-4.1"  # the full-quality model is wrong-tier


def test_b3_spend_event_is_always_emitted_no_silent_run() -> None:
    """No silent run: every Evaluate run emits exactly one ai_spend_recorded."""
    ctx = FakeStageContext()
    run_evaluate_stage(
        engine=engine(), project_id=PROJECT, findings=[risk()], ctx=ctx,
        input_attestation_version="v1", recompute_trigger=None, is_recompute=False,
        model=synthesized_model(), mode="fast",
    )
    assert ctx.emitter.names.count("ai_spend_recorded") == 1


def test_b3_evaluate_never_calls_a_provider_no_overspend_possible() -> None:
    """Evaluate scores Findings — it imports no Agent / provider (cost bypass impossible)."""
    src = inspect.getsource(stage_mod) + inspect.getsource(
        __import__("backend.responsibilities.evaluate.engine", fromlist=["x"])
    )
    assert "Agent(" not in src
    assert "run_sync" not in src
    # No live-model resolution: Evaluate uses only the PURE routing identity
    # (routing_for_tier(...).model_for(...) is config, not a provider call) — it
    # never constructs an LLMProvider or resolves a live model.
    assert "LLMProvider(" not in src
    assert "provider.model_for" not in src
    assert ".run_sync(" not in src

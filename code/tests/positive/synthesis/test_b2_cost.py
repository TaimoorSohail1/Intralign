"""QA-WS-SYNTH / DL-048 B2 (cost governance) — Free-tier within budget, and a
graceful over-budget degrade that emits ``ai_spend_recorded``.

Free-tier Fast per-run cap is 150,000 tokens (Calibration §4c). A normal
recorded run stays well under it and defers nothing. An over-budget recorded run
(large recorded token counts) synthesizes a PARTIAL model + the artifacts that
fit, DEFERS the rest (never silent overspend, never runaway), and EMITS the
spend event with the over-budget trust signal. All offline (recorded fixtures).
"""

from __future__ import annotations

from backend.responsibilities.infer.stage import run_synthesis_stage
from backend.services.llm_provider import RunBudget, budget_for_tier
from shared.epistemic import PLANNING_ARTIFACT_TYPES
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import (
    PROJECT,
    sample_drafts,
    synthesis_engine,
)

FREE_FAST_CAP = 150_000


def _ids() -> list[str]:
    return [f"assertion-{i}" for i in range(4)]


def test_b2_free_fast_per_run_cap_matches_calibration_4c() -> None:
    """The enforced cap is the §4c Free Fast per-run budget (config, not magic)."""
    assert budget_for_tier("free").per_run_cap("fast") == FREE_FAST_CAP


def test_b2_free_tier_run_stays_within_budget_and_defers_nothing() -> None:
    engine, _ = synthesis_engine()  # the normal (small-token) recorded fixture
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert not result.degraded
    assert result.deferred_artifact_types == ()
    assert len(result.artifacts) == len(PLANNING_ARTIFACT_TYPES)
    # The recorded run is well under the Free Fast cap.
    assert result.spend_payload["tokens_in"] + result.spend_payload["tokens_out"] < (
        FREE_FAST_CAP
    )
    assert result.spend_payload["over_budget"] is False


def test_b2_over_budget_degrades_to_partial_and_defers_the_rest() -> None:
    """DL-048 — partial model from highest-priority evidence + defer (no overspend)."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert result.degraded is True
    # Some artifacts were produced; the remainder were DEFERRED, not overspent.
    assert 0 < len(result.artifacts) < len(PLANNING_ARTIFACT_TYPES)
    assert result.deferred_artifact_types
    assert (
        len(result.artifacts) + len(result.deferred_artifact_types)
        == len(PLANNING_ARTIFACT_TYPES)
    )
    # The model itself is still produced (a partial orientation), with assumptions.
    assert result.model.intent_summary


def test_b2_over_budget_emits_ai_spend_recorded_with_the_trust_signal() -> None:
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    ctx = FakeStageContext()
    run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(),
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
    )
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    payload = spend[0]
    # The DL-048 fields are present (tokens/cost/tier/user/mode/model).
    for field in ("tokens_in", "tokens_out", "est_cost", "tier", "user", "mode", "model"):
        assert field in payload
    assert payload["tier"] == "free"
    assert payload["mode"] == "fast"
    # Over-budget is a TRUST SIGNAL, not just a metric (DL-048 OBS).
    assert payload["over_budget"] is True
    assert payload["degraded"] is True


def test_b2_spend_event_records_real_token_counts_from_the_fixture() -> None:
    """The recorded usage flows into the budget accounting (est_cost from §4c basis)."""
    engine, _ = synthesis_engine()
    budget = RunBudget.for_run(tier="free", mode="fast")
    result = engine.synthesize_and_generate(
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(),
        budget=budget,
    )
    # tokens_in/out are the SUM of the recorded per-call usage (synthesis + 7 gen).
    assert budget.tokens_in == 400 + 7 * 120
    assert budget.tokens_out == 220 + 7 * 60
    assert result.spend_payload["est_cost"] >= 0.0

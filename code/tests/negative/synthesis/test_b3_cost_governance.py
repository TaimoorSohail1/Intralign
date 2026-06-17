"""QA-WS-SYNTH / DL-048 B3 — the cost-governance Critical negatives.

DL-048 forbids: budget bypass, runaway regeneration, silent overspend, and
wrong-tier routing. Each is a test:

- over-budget NEVER silently overspends — it stops and defers (the engine asks
  ``can_afford`` before each call and degrades on False);
- the budget can NEVER report under-cap once spend has reached the cap;
- Free-tier routing is honored — synthesis/generation route to the §4c mini
  model, NOT a full-quality model (wrong-tier routing);
- the spend event always surfaces over-budget as a trust signal (no silent run).
"""

from __future__ import annotations

from backend.services.llm_provider import (
    DEFAULT_INTERNAL_MODEL,
    LLMProvider,
    ModelRef,
    RunBudget,
    internal_model_id,
    routing_for_tier,
)
from shared.epistemic import PLANNING_ARTIFACT_TYPES
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine


def _ids() -> list[str]:
    return [f"a{i}" for i in range(4)]


def test_b3_over_budget_never_silently_overspends() -> None:
    """CRITICAL (silent overspend) — recorded spend never exceeds the cap unbounded."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    budget = RunBudget.for_run(tier="free", mode="fast")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids(),
        budget=budget,
    )
    # It DEGRADED instead of generating all seven — the defer is the proof.
    assert result.degraded is True
    assert result.deferred_artifact_types
    # The engine stopped BEFORE generating every artifact (no runaway regeneration).
    assert len(result.artifacts) < len(PLANNING_ARTIFACT_TYPES)


def test_b3_budget_cannot_report_affordable_once_the_cap_is_reached() -> None:
    """CRITICAL (budget bypass) — can_afford is False once spend hits the cap."""
    budget = RunBudget(tier="free", mode="fast", cap=1000)
    budget.record(tokens_in=600, tokens_out=400, model="gpt-4.1-mini")  # exactly at cap
    assert budget.over_budget is True
    assert budget.can_afford(1) is False
    assert budget.can_afford(0) is False  # even a zero-token call is refused over-cap


def test_b3_runaway_regeneration_is_bounded_by_the_cap() -> None:
    """CRITICAL (runaway) — the loop cannot generate past the per-run cap."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    budget = RunBudget.for_run(tier="free", mode="fast")
    engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids(),
        budget=budget,
    )
    # Total recorded spend never blows far past the cap (it stops at the boundary).
    assert budget.spent <= budget.cap + 60_000  # one last in-flight call, then stop


def test_b3_free_tier_routes_synthesis_to_internal_not_a_full_model() -> None:
    """CRITICAL (wrong-tier routing) — primary routing is internal gemma (DL-059).

    Post-DL-059 the PRIMARY model behind the seam is the internal gemma on the
    local Llama runtime; Free resolves to it for every stage. An external
    full-quality model (gpt-4.1) is still NOT what Free routes to (wrong-tier).
    """
    gemma = internal_model_id()
    assert gemma == DEFAULT_INTERNAL_MODEL  # env default is gemma4
    routing = routing_for_tier("free")
    assert routing.synthesis == ModelRef("internal", gemma)
    assert routing.generation == ModelRef("internal", gemma)
    assert routing.extraction == ModelRef("internal", gemma)
    # A full-quality external model is NOT what Free synthesis routes to.
    assert routing.synthesis.model != "gpt-4.1"
    assert routing.synthesis.provider != "openai"
    provider = LLMProvider()
    assert provider.resolve(tier="free", stage="synthesis").provider == "internal"
    assert provider.resolve(tier="free", stage="synthesis").model_name == gemma
    assert provider.resolve(tier="free", stage="extraction").model_name == gemma


def test_b3_over_budget_run_cannot_emit_a_clean_spend_signal() -> None:
    """CRITICAL — the spend payload must mark over_budget; it can't hide overspend."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert result.spend_payload["over_budget"] is True
    assert result.spend_payload["degraded"] is True

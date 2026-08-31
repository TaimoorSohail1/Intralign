"""QA-WB-INFER B2 (DL-046/DL-048) — Fast Pass orientation-sufficient + cost-gov.

Fast Pass produces orientation-sufficient Findings (the rule-structural set) and
NEVER blocks; the AI passes run within the per-run token budget. Over-budget
DEFERS the AI Findings (graceful degradation) — the rule-structural Findings are
still produced — rather than overspending (DL-048). The Deep Pass (00R async)
expands; the user is never blocked on it.
"""

from __future__ import annotations

from backend.services.llm_provider import RunBudget, internal_model_id
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    PROJECT,
    finding_engine,
    sample_drafts,
    synthesized_model,
)


def _derive(engine, *, budget=None):
    return engine.derive(
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS,
        model=synthesized_model(),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
        budget=budget,
    )


def test_b2_fast_pass_is_orientation_sufficient_and_not_degraded_within_budget() -> None:
    engine, _ = finding_engine(mode="fast")
    result = _derive(engine)
    assert not result.degraded
    # Orientation-sufficient: at least the rule-structural Findings are present.
    assert result.of_type("gap")
    assert result.of_type("conflict")


def test_b2_over_budget_defers_ai_findings_keeping_rule_structural_ones() -> None:
    """DL-048 — a tiny budget defers the AI passes (degraded) but never overspends;
    the rule-structural orientation Findings are still produced (Fast not blocked)."""
    engine, session = finding_engine(mode="fast")
    tiny = RunBudget(tier="free", mode="fast", cap=1)  # nothing affordable
    result = _derive(engine, budget=tiny)
    assert result.degraded  # the AI passes were deferred, not overspent
    assert session.call_count == 0  # no model call at all under a zero-room budget
    # Rule-structural Findings (coverage/SMART gaps + conflicts) still derived.
    assert result.of_type("gap")
    assert result.of_type("conflict")
    assert not result.of_type("risk")  # the risk (AI) pass was deferred


def test_b2_spend_payload_records_degraded_and_mode() -> None:
    engine, _ = finding_engine(mode="fast")
    tiny = RunBudget(tier="free", mode="fast", cap=1)
    result = _derive(engine, budget=tiny)
    assert result.spend_payload["degraded"] is True
    assert result.spend_payload["mode"] == "fast"
    assert "tokens_in" in result.spend_payload


def test_b2_free_tier_routes_finding_passes_to_the_internal_primary() -> None:
    """DL-069 — Free routes synthesis to the internal gemma primary, not a full model."""
    engine, _ = finding_engine(tier="free")
    resolved = engine.provider.resolve(tier="free", stage="synthesis")
    assert resolved.provider == "internal"
    assert resolved.model_name == internal_model_id()
    assert resolved.model_name != "gpt-4.1"

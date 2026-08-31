"""QA-WS-SYNTH B2 (Infer synthesis) — a Derived SynthesizedPlanningModel with
every gap-filling assumption EXPLICITLY flagged (A3.3; A4.4 no silent gap-fill).

Synthesis turns the Attested drafts into OSLO's recomputable interpretation:
Derived (``epistemic_state=derived``), lineage-bearing (the assertion ids it
derived from), and carrying its flagged assumptions as Derived — never as
evidence-attested fact. Driven offline by a recorded fixture.
"""

from __future__ import annotations

from shared.epistemic import EpistemicState, FlaggedAssumption
from tests.positive.synthesis.helpers import (
    PROJECT,
    sample_drafts,
    synthesis_engine,
)


def _ids(n: int) -> list[str]:
    return [f"assertion-{i}" for i in range(n)]


def test_b2_synthesis_produces_a_derived_planning_model() -> None:
    engine, _ = synthesis_engine()
    drafts = sample_drafts()
    ids = _ids(len(drafts))
    from backend.services.llm_provider import RunBudget

    model = engine.synthesize_model(
        project_id=PROJECT,
        assertions=drafts,
        assertion_ids=ids,
        budget=RunBudget.for_run(tier="free", mode="fast"),
    )
    assert model.epistemic_state == EpistemicState.DERIVED
    assert model.is_canonical is False  # Derived is never canonical (hard rule #2)
    assert model.project_id == PROJECT
    assert model.intent_summary and model.scope_summary
    # Lineage back to the Attested assertions it derived from.
    assert set(model.derived_from_assertions) == set(ids)


def test_b2_synthesis_flags_every_gap_filling_assumption_explicitly() -> None:
    """A4.4 — inferred assumptions are surfaced as Derived, with the gap covered."""
    engine, _ = synthesis_engine()
    result = engine.synthesize_and_generate(
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(4),
    )
    assumptions = result.model.flagged_assumptions
    assert assumptions, "the recorded synthesis fills gaps -> must flag them"
    for a in assumptions:
        assert isinstance(a, FlaggedAssumption)
        # Each assumption is PINNED Derived and records the gap it covers (audit).
        assert a.epistemic_state == EpistemicState.DERIVED
        assert a.statement
        assert a.covers_gap


def test_b2_synthesis_runs_offline_on_a_recorded_fixture() -> None:
    engine, session = synthesis_engine()
    engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids(4)
    )
    # The synthesis step + 7 generations are all recorded responses (zero live).
    assert session.call_count == 8
    assert session.served_keys[0] == "synthesis"

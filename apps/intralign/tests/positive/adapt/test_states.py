"""DTM-0005 positive adapt suite — cognition state machine (IC-WA-00R A3.6/A7; QA B2.3).

States are EXACTLY ``analyzing | current | stale | reanalyzing | failed``; every
legal transition emits a ``state_transition_occurred`` event through the event
seam (A6) and returns the StateTransitionEvent record. Pure — never skips.
"""

from __future__ import annotations

from backend.responsibilities.adapt.states import (
    LEGAL_TRANSITIONS,
    CognitionState,
    CognitionStateMachine,
    StateTransitionEvent,
)
from backend.services.observability.events import CollectingEventEmitter

_PROJECT = "33333333-3333-3333-3333-333333333333"


def test_states_are_exactly_the_contract_five() -> None:
    """A3.6 — analyzing | current | stale | reanalyzing | failed, nothing else."""
    assert sorted(s.value for s in CognitionState) == sorted(
        ["analyzing", "current", "stale", "reanalyzing", "failed"]
    )


def test_b2_3_full_success_cycle_emits_each_transition() -> None:
    """B2.3 / A7 — Current -> Stale -> Reanalyzing -> Current', all evented."""
    emitter = CollectingEventEmitter()
    machine = CognitionStateMachine(
        project_id=_PROJECT, state=CognitionState.CURRENT, emitter=emitter
    )

    events = [
        machine.transition(CognitionState.STALE, run_id="run-1"),
        machine.transition(CognitionState.REANALYZING, run_id="run-1"),
        machine.transition(CognitionState.CURRENT, run_id="run-1"),
    ]

    assert machine.state is CognitionState.CURRENT
    assert [(e.from_state, e.to_state) for e in events] == [
        (CognitionState.CURRENT, CognitionState.STALE),
        (CognitionState.STALE, CognitionState.REANALYZING),
        (CognitionState.REANALYZING, CognitionState.CURRENT),
    ]
    # Every transition went through the event seam (A6), in order.
    assert emitter.names == ["state_transition_occurred"] * 3
    assert [
        (p["from_state"], p["to_state"]) for _, p in emitter.events
    ] == [("current", "stale"), ("stale", "reanalyzing"), ("reanalyzing", "current")]


def test_b2_3_failure_branch_reanalyzing_to_failed() -> None:
    """B2.3 / A7 — Reanalyzing -> Failed is legal and evented."""
    emitter = CollectingEventEmitter()
    machine = CognitionStateMachine(
        project_id=_PROJECT, state=CognitionState.REANALYZING, emitter=emitter
    )
    event = machine.transition(CognitionState.FAILED, reason="chain failure")
    assert machine.state is CognitionState.FAILED
    assert isinstance(event, StateTransitionEvent)
    assert event.reason == "chain failure"
    assert emitter.names == ["state_transition_occurred"]


def test_first_analysis_path_analyzing_to_current() -> None:
    """A3.6 — analyzing is the first-analysis state; it completes to current."""
    machine = CognitionStateMachine(project_id=_PROJECT, state=CognitionState.ANALYZING)
    machine.transition(CognitionState.CURRENT)
    assert machine.state is CognitionState.CURRENT


def test_failed_recovers_via_stale_on_new_trigger() -> None:
    """Failed retains last-known-good; a NEW trigger re-marks stale (A7 cycle)."""
    machine = CognitionStateMachine(project_id=_PROJECT, state=CognitionState.FAILED)
    machine.transition(CognitionState.STALE, reason="new trigger after failure")
    assert machine.state is CognitionState.STALE


def test_transition_event_record_fields() -> None:
    """A6 — the StateTransitionEvent record carries project/run/time metadata."""
    emitter = CollectingEventEmitter()
    machine = CognitionStateMachine(
        project_id=_PROJECT, state=CognitionState.CURRENT, emitter=emitter
    )
    event = machine.transition(CognitionState.STALE, run_id="run-9", reason="promotion")
    assert event.project_id == _PROJECT
    assert event.run_id == "run-9"
    assert event.reason == "promotion"
    assert event.occurred_at is not None
    name, payload = emitter.events[0]
    assert name == "state_transition_occurred"
    assert payload["project_id"] == _PROJECT
    assert payload["run_id"] == "run-9"


def test_legal_transition_table_is_exactly_a7() -> None:
    """The legal-transition table encodes A7 and nothing more."""
    assert LEGAL_TRANSITIONS == {
        CognitionState.ANALYZING: frozenset(
            {CognitionState.CURRENT, CognitionState.FAILED}
        ),
        CognitionState.CURRENT: frozenset({CognitionState.STALE}),
        CognitionState.STALE: frozenset({CognitionState.REANALYZING}),
        CognitionState.REANALYZING: frozenset(
            {CognitionState.CURRENT, CognitionState.FAILED}
        ),
        CognitionState.FAILED: frozenset({CognitionState.STALE}),
    }

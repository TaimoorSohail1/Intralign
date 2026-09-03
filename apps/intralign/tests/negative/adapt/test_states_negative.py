"""DTM-0005 negative adapt suite — illegal state transitions rejected (IC-WA-00R A7).

Only the A7 transitions are legal; anything else raises and leaves the machine
unmoved with NO event emitted (an illegal move never reaches the event seam).
Pure — never skips.
"""

from __future__ import annotations

import pytest

from backend.responsibilities.adapt.states import (
    CognitionState,
    CognitionStateMachine,
    IllegalStateTransitionError,
)
from backend.services.observability.events import CollectingEventEmitter

_PROJECT = "55555555-5555-5555-5555-555555555555"

_ILLEGAL = [
    # Recompute cannot be skipped: stale must pass through reanalyzing.
    (CognitionState.STALE, CognitionState.CURRENT),
    # A run cannot start without being marked stale first.
    (CognitionState.CURRENT, CognitionState.REANALYZING),
    # Failed never silently becomes current — last-known-good stays until a NEW
    # trigger re-marks stale and a recompute succeeds.
    (CognitionState.FAILED, CognitionState.CURRENT),
    (CognitionState.FAILED, CognitionState.REANALYZING),
    # No backwards moves.
    (CognitionState.REANALYZING, CognitionState.STALE),
    (CognitionState.CURRENT, CognitionState.ANALYZING),
    # Failure is a run outcome, not an idle-state move.
    (CognitionState.CURRENT, CognitionState.FAILED),
    (CognitionState.STALE, CognitionState.FAILED),
    # Self-transitions are not transitions.
    (CognitionState.CURRENT, CognitionState.CURRENT),
    (CognitionState.REANALYZING, CognitionState.REANALYZING),
]


@pytest.mark.parametrize(("start", "target"), _ILLEGAL)
def test_b2_3_illegal_transition_rejected(
    start: CognitionState, target: CognitionState
) -> None:
    """A7 — an illegal transition raises; state unmoved; nothing emitted."""
    emitter = CollectingEventEmitter()
    machine = CognitionStateMachine(project_id=_PROJECT, state=start, emitter=emitter)
    with pytest.raises(IllegalStateTransitionError):
        machine.transition(target)
    assert machine.state is start
    assert emitter.events == []


def test_unknown_state_value_rejected() -> None:
    """A3.6 — the five contract states are the whole vocabulary."""
    with pytest.raises(ValueError):
        CognitionState("superseded")

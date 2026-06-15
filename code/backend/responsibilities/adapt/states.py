"""Cognition state machine — the legal A7 lifecycle (IC-WA-00R A3.6/A7; QA B2.3).

States are EXACTLY ``analyzing | current | stale | reanalyzing | failed``.
Legal moves (A7):

    analyzing   -> current | failed          (first analysis)
    current     -> stale                     (input/knowledge change)
    stale       -> reanalyzing               (recompute started)
    reanalyzing -> current' | failed         (success / failure)
    failed      -> stale                     (a NEW trigger re-marks stale;
                                              last-known-good retained meanwhile)

Anything else raises :class:`IllegalStateTransitionError` and emits nothing.
Every legal transition produces a :class:`StateTransitionEvent` record and emits
``state_transition_occurred`` through the event seam (A6) — a callback protocol,
never printing; transport is DTM-0006.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field

from backend.services.observability.events import EventEmitter


class CognitionState(str, Enum):
    """A3.6 — the five cognition states, exactly."""

    ANALYZING = "analyzing"
    CURRENT = "current"
    STALE = "stale"
    REANALYZING = "reanalyzing"
    FAILED = "failed"


# A7 legal-transition table. failed -> stale: failure retains last-known-good
# until a NEW information-changing trigger re-marks the project stale.
LEGAL_TRANSITIONS: dict[CognitionState, frozenset[CognitionState]] = {
    CognitionState.ANALYZING: frozenset({CognitionState.CURRENT, CognitionState.FAILED}),
    CognitionState.CURRENT: frozenset({CognitionState.STALE}),
    CognitionState.STALE: frozenset({CognitionState.REANALYZING}),
    CognitionState.REANALYZING: frozenset(
        {CognitionState.CURRENT, CognitionState.FAILED}
    ),
    CognitionState.FAILED: frozenset({CognitionState.STALE}),
}


class IllegalStateTransitionError(Exception):
    """Raised on any move outside the A7 table; the machine does not move."""


class StateTransitionEvent(BaseModel):
    """The State Transition Event record (IC-WA-00R primary object; A6)."""

    project_id: str
    from_state: CognitionState
    to_state: CognitionState
    run_id: str | None = None
    reason: str | None = None
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CognitionStateMachine:
    """Per-project cognition state with A7-legal transitions only.

    Each successful transition returns the event record and emits it through
    the seam (``state_transition_occurred``); an illegal transition raises
    before anything is emitted.
    """

    def __init__(
        self,
        project_id: str,
        state: CognitionState = CognitionState.CURRENT,
        emitter: EventEmitter | None = None,
    ) -> None:
        self._project_id = project_id
        self._state = CognitionState(state)
        self._emitter = emitter

    @property
    def state(self) -> CognitionState:
        return self._state

    def transition(
        self,
        to_state: CognitionState,
        *,
        run_id: str | None = None,
        reason: str | None = None,
    ) -> StateTransitionEvent:
        """Move to ``to_state`` if legal per A7; emit and return the event record."""
        target = CognitionState(to_state)
        if target not in LEGAL_TRANSITIONS[self._state]:
            raise IllegalStateTransitionError(
                f"illegal cognition state transition {self._state.value!r} -> "
                f"{target.value!r} for project {self._project_id} — legal targets: "
                f"{sorted(s.value for s in LEGAL_TRANSITIONS[self._state])} (A7)"
            )
        event = StateTransitionEvent(
            project_id=self._project_id,
            from_state=self._state,
            to_state=target,
            run_id=run_id,
            reason=reason,
        )
        self._state = target
        if self._emitter is not None:
            self._emitter.emit(
                "state_transition_occurred",
                {
                    "project_id": event.project_id,
                    "from_state": event.from_state.value,
                    "to_state": event.to_state.value,
                    "run_id": event.run_id,
                    "reason": event.reason,
                    "occurred_at": event.occurred_at.isoformat(),
                },
            )
        return event

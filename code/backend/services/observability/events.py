"""Event seam for the recompute backbone (IC-WA-00R A6) — dispatcher protocol only.

The backbone emits its seven contract events through this seam; transport is
deliberately NOT decided here (open NFR). Full observability wiring — OTel spans,
LangSmith linkage, governed-output event transport — is DTM-0006; this module
stays a thin internal dispatcher so DTM-0006 can swap the emitter without
touching the backbone.

The event vocabulary is EXACTLY the IC-WA-00R A6 list. An unknown name is a
programming error and is rejected loudly — events are contract surface, not
free-form logging.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

# IC-WA-00R A6 — the seven backbone events, exactly.
EVENT_NAMES: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

_EVENT_NAME_SET: frozenset[str] = frozenset(EVENT_NAMES)


class UnknownEventError(ValueError):
    """Raised when an event name outside the IC-WA-00R A6 vocabulary is emitted."""


@runtime_checkable
class EventEmitter(Protocol):
    """The seam the backbone emits through (callback protocol, not a transport)."""

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Dispatch one A6 event with its payload."""
        ...  # pragma: no cover - protocol


class CollectingEventEmitter:
    """Default emitter: validates names and collects events in order.

    Serves tests and local runs until DTM-0006 binds a real transport.
    """

    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        if event_name not in _EVENT_NAME_SET:
            raise UnknownEventError(
                f"unknown backbone event {event_name!r} — the vocabulary is "
                f"exactly IC-WA-00R A6: {', '.join(EVENT_NAMES)}"
            )
        self.events.append((event_name, dict(payload)))

    @property
    def names(self) -> list[str]:
        """Event names in emission order (assertion convenience)."""
        return [name for name, _ in self.events]

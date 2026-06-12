"""Event seam for the Wave A contracts — dispatcher protocol only.

The backbone (IC-WA-00R A6) and artifact intake (IC-WA-001 A6) emit their
contract events through this seam; transport is deliberately NOT decided here
(open NFR). Full observability wiring — OTel spans, LangSmith linkage, governed
output event transport — is DTM-0006's ``ObservedEventEmitter`` decorator; this
module stays a thin internal dispatcher so the emitter can be swapped without
touching the responsibilities.

The vocabulary is pinned PER CONTRACT (deep-task decision #1, DTM-0007):

- ``EVENT_NAMES_WA00R`` — EXACTLY the seven IC-WA-00R A6 names, in contract order.
- ``EVENT_NAMES_WA001`` — EXACTLY the eight IC-WA-001 A6 names, in contract
  order. ``stale_detected`` belongs to the WA00R set and is referenced, never
  duplicated (IC-WA-001 A6 "Artifact Modified / Stale Detected").
- ``EVENT_NAMES`` — the union (concatenation) the emitters accept; kept as the
  back-compat alias for existing consumers.

An unknown name is a programming error and is rejected loudly — events are
contract surface, not free-form logging.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

# IC-WA-00R A6 — the seven backbone events, exactly.
EVENT_NAMES_WA00R: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

# IC-WA-001 A6 — the eight intake events, exactly (OBS-WA-001 C2).
# stale_detected is NOT repeated here — it is already pinned in the WA00R set.
EVENT_NAMES_WA001: tuple[str, ...] = (
    "artifact_received",
    "artifact_normalizing",
    "artifact_normalized",
    "promotion_candidate_ready",
    "promotion_readiness_failed",
    "user_acceptance_captured",
    "context_signal_received",
    "artifact_modified",
)

# Union vocabulary accepted by emitters (back-compat alias for consumers).
EVENT_NAMES: tuple[str, ...] = EVENT_NAMES_WA00R + EVENT_NAMES_WA001

_EVENT_NAME_SET: frozenset[str] = frozenset(EVENT_NAMES)


class UnknownEventError(ValueError):
    """Raised when an event name outside the contract vocabularies is emitted."""


@runtime_checkable
class EventEmitter(Protocol):
    """The seam responsibilities emit through (callback protocol, not a transport)."""

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Dispatch one contract event with its payload."""
        ...  # pragma: no cover - protocol


class CollectingEventEmitter:
    """Default emitter: validates names and collects events in order.

    Serves tests and local runs until a real external transport is bound.
    """

    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def emit(self, event_name: str, payload: Mapping[str, Any]) -> None:
        if event_name not in _EVENT_NAME_SET:
            raise UnknownEventError(
                f"unknown contract event {event_name!r} — the vocabulary is "
                f"exactly IC-WA-00R A6 + IC-WA-001 A6: {', '.join(EVENT_NAMES)}"
            )
        self.events.append((event_name, dict(payload)))

    @property
    def names(self) -> list[str]:
        """Event names in emission order (assertion convenience)."""
        return [name for name, _ in self.events]

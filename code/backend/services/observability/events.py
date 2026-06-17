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
- ``EVENT_NAMES_WA002`` — EXACTLY the five IC-WA-002 A6 names, in contract
  order (DTM-0008; OBS-WA-002 C2 == A6).
- ``EVENT_NAMES_WS`` — EXACTLY the four IC/OBS-WS-SYNTH A6 names (DTM-0009;
  decision #9), in contract order.
- ``EVENT_NAMES_WB_INFER`` — EXACTLY the two IC/OBS-WB-INFER A6 names (DTM-0010;
  decision #9), in contract order.
- ``EVENT_NAMES_COST`` — the single shared DL-048 spend event
  (``ai_spend_recorded``), introduced in DTM-0009 and reused by Wave B.
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

# IC-WA-002 A6 — the five retention events, exactly (OBS-WA-002 C2).
EVENT_NAMES_WA002: tuple[str, ...] = (
    "knowledge_promoted",
    "knowledge_versioned",
    "knowledge_superseded",
    "knowledge_archived",
    "knowledge_mutation_recorded",
)

# IC/OBS-WS-SYNTH A6 — the four synthesis-engine events, exactly (decision #9).
# Pinned verbatim against OBS-WS-SYNTH §3 / A6 ("Claim Extracted", "Planning
# Artifact Generated/Regenerated", "Synthesized Model Updated"). The
# per-emission ``cognition_history_record_appended`` is reused from the WA00R
# set (never duplicated). DTM-0009 / Wave S.
EVENT_NAMES_WS: tuple[str, ...] = (
    "claim_extracted",
    "planning_artifact_generated",
    "planning_artifact_regenerated",
    "synthesized_model_updated",
)

# IC/OBS-WB-INFER A6 — the two Finding events, exactly (decision #9; DTM-0010).
# Pinned verbatim against OBS-WB-INFER §1.3 / A6 ("Finding Detected/Superseded";
# C2 == A6). The per-emission ``cognition_history_record_appended`` is reused
# from the WA00R set (never duplicated). Wave B / Infer.
EVENT_NAMES_WB_INFER: tuple[str, ...] = (
    "finding_detected",
    "finding_superseded",
)

# DL-048 cost-governance — the single shared spend event (decision #9),
# introduced in DTM-0009 and reused by Wave B. "AI Spend Recorded" (OBS §3).
EVENT_NAMES_COST: tuple[str, ...] = ("ai_spend_recorded",)

# Union vocabulary accepted by emitters (back-compat alias for consumers).
EVENT_NAMES: tuple[str, ...] = (
    EVENT_NAMES_WA00R
    + EVENT_NAMES_WA001
    + EVENT_NAMES_WA002
    + EVENT_NAMES_WS
    + EVENT_NAMES_WB_INFER
    + EVENT_NAMES_COST
)

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
                "exactly IC-WA-00R A6 + IC-WA-001 A6 + IC-WA-002 A6 + "
                "IC-WS-SYNTH A6 + IC-WB-INFER A6 + DL-048 cost: "
                f"{', '.join(EVENT_NAMES)}"
            )
        self.events.append((event_name, dict(payload)))

    @property
    def names(self) -> list[str]:
        """Event names in emission order (assertion convenience)."""
        return [name for name, _ in self.events]

"""User-acceptance CAPTURE (DTM-0007; IC-WA-001 A3.5) — capture, never accept.

Perceive records WHAT the user did (item + the specific version pin + action)
and hands it off; Retain creates the User Acceptance Record (DTM-0008). This
module writes NO row, marks nothing true/approved/organizational-truth, and
performs no interpretation — capture is info-change only and triggers no
recompute by itself (A9; B3.4).

``version_pin`` is MANDATORY (QA-WA-001 B4 Major: "acceptance captured without
version reference") — a capture without the exact emission/version accepted is
rejected before anything is emitted.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from backend.services.observability.events import CollectingEventEmitter, EventEmitter

AcceptanceActionName = Literal["accept", "reject", "defer", "direct_edit"]


class VersionPinMissingError(ValueError):
    """B4-Major guard: an acceptance action without its version pin is rejected."""


class AcceptanceCapture(BaseModel):
    """The handoff object: who acted, on what item, at which pinned version.

    Field shape feeds the LDM §2.4 User Acceptance Record that RETAIN will
    write (DTM-0008). Frozen + closed (``extra='forbid'``): it cannot grow a
    truth/approval marker and cannot be mutated after capture.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str
    target_kind: str = Field(..., description="recommendation | finding | … (LDM §2.4)")
    version_pin: str = Field(
        ..., description="the EXACT emission/version accepted (CHR/assertion id)"
    )
    action: AcceptanceActionName
    project_id: str | None = None
    captured_at: datetime
    # Wave U (DTM-0016): for a ``direct_edit`` the user authors content directly —
    # this carries that confirmed edit content so Retain can record the plan fact
    # from it (no recommendation to derive from). For accept/reject/defer it is
    # ``None`` (an accept's plan-fact content comes from the pinned CHR, a data
    # read; reject/defer write no plan fact). It is the user's words, NEVER a
    # truth/approval marker.
    edit_content: str | None = Field(
        default=None,
        description="direct_edit only: the user-authored confirmed content (plan fact source).",
    )


def capture_acceptance(
    action_input: AcceptanceCapture | Mapping[str, Any],
    *,
    emitter: EventEmitter | None = None,
) -> AcceptanceCapture:
    """Capture one user-acceptance action; emit its event; return the handoff.

    Capture only: the user's action is recorded as ATTRIBUTION (who/what/
    which-version/when), not as truth — Perceive accepts nothing (A4.4).

    Raises:
        VersionPinMissingError: no/empty ``version_pin`` (B4 Major) — rejected
            before any event is emitted.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    fields = (
        dict(action_input)
        if isinstance(action_input, Mapping)
        else action_input.model_dump()
    )
    pin = fields.get("version_pin")
    if pin is None or not str(pin).strip():
        raise VersionPinMissingError(
            "acceptance capture rejected — version_pin is mandatory: the "
            "capture must name the specific emission/version accepted "
            "(IC-WA-001 A3.5; QA-WA-001 B4 Major)"
        )
    capture = AcceptanceCapture(
        **{**fields, "captured_at": fields.get("captured_at") or datetime.now(UTC)}
    )
    seam.emit(
        "user_acceptance_captured",
        {
            # C3 acceptance audit: the accepted item + version reference.
            "user_id": capture.user_id,
            "target_kind": capture.target_kind,
            "version_pin": capture.version_pin,
            "action": capture.action,
            "project_id": capture.project_id,
            "captured_at": capture.captured_at.isoformat(),
        },
    )
    return capture

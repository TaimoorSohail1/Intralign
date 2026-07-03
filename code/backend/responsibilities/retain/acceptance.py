"""User Acceptance Record creation (DTM-0008; IC-WA-002 DL-043 §B+; decision #9).

``record_acceptance`` turns the Perceive handoff (``AcceptanceCapture``,
DTM-0007) into the canonical, user-attested ``user_acceptance_record`` row —
"User U, at time T, took action A on item I at version_pin V". It records a
HUMAN DECISION, nothing more (DL-043 amendment 4):

- **acceptance-recording != truth-assertion** — the UAR row carries action /
  target / version_pin attribution ONLY; no field marks the accepted item
  true, approved, canonical-as-truth, or permanently valid, and the accepted
  item itself is never touched (decoupled — it stays recomputable if Derived).
- **version_pin is MANDATORY** (QA B4 Major / B+ negative 4): a capture
  without the exact emission/version accepted is rejected with
  :class:`AcceptanceRecordingError` before anything is written.
- **No event is emitted here.** Acceptance is an information change, not a
  knowledge mutation: the capture's own event (``user_acceptance_captured``)
  already fired in Perceive (IC-WA-001 A6), and OBS-WA-002 names no
  acceptance event of Retain's — the UAR write appends history only
  (``acceptance-recorded``). This module therefore takes no emitter at all.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from backend.responsibilities.perceive.acceptance_capture import AcceptanceCapture
from backend.responsibilities.retain.admission import RetentionStore


class AcceptanceRecordingError(ValueError):
    """B4-Major guard: a UAR without its mandatory fields is rejected."""


class AcceptanceRecordResult(BaseModel):
    """What one acceptance recording produced: the UAR row + its history entry."""

    uar_id: str
    record: dict
    history_id: str


def record_acceptance(
    capture: AcceptanceCapture | Mapping[str, Any],
    *,
    project_id: str,
    store: RetentionStore,
) -> AcceptanceRecordResult:
    """Write the User Acceptance Record for one captured acceptance action.

    INSERTS one ``user_acceptance_record`` row (version-pinned, decoupled,
    user-attested) and appends one ``acceptance-recorded`` history entry.
    Marks nothing true/approved; mutates nothing; emits nothing (the capture
    event already fired in Perceive — see module docstring).

    Raises:
        AcceptanceRecordingError: missing/empty ``version_pin`` (B4 Major /
            B+ negative 4) or missing ``project_id`` — rejected before any
            write.
    """
    fields = (
        dict(capture)
        if isinstance(capture, Mapping)
        else capture.model_dump()
    )
    pin = fields.get("version_pin")
    if pin is None or not str(pin).strip():
        raise AcceptanceRecordingError(
            "acceptance recording rejected — version_pin is mandatory: a User "
            "Acceptance Record must pin the exact emission/version accepted "
            "(DL-043; IC-WA-002 §B+ negative 4; QA B4 Major)"
        )
    if not str(project_id).strip():
        raise AcceptanceRecordingError(
            "acceptance recording rejected — project_id is mandatory: the UAR "
            "is a canonical project record (LDM §1 universal fields)"
        )

    user_id = str(fields["user_id"])
    captured_at = fields.get("captured_at")
    confirmed_at = (
        captured_at.isoformat() if hasattr(captured_at, "isoformat") else captured_at
    )
    row: dict[str, Any] = {
        "user_id": user_id,
        "action": str(fields["action"]),
        "target_kind": str(fields["target_kind"]),
        "version_pin": str(pin),
        "project_id": str(project_id),
        "created_by": user_id,
        "epistemic_state": "attested-user",
        "version": 1,
        "provenance_ref": {
            "capture_event": "user_acceptance_captured",  # fired in Perceive
            "user_id": user_id,
            "version_pin": str(pin),
            "captured_at": confirmed_at,
        },
    }
    if confirmed_at is not None:
        row["confirmed_at"] = confirmed_at
    persisted = dict(store.insert_acceptance(row))

    entry = store.insert_history(
        {
            "event_type": "acceptance-recorded",
            "subject_ref": {
                "uar_id": str(persisted["uar_id"]),
                "version_pin": str(pin),
                "target_kind": str(fields["target_kind"]),
                "action": str(fields["action"]),
            },
            "actor": user_id,
            "project_id": str(project_id),
            "created_by": user_id,
            "epistemic_state": "attested-user",
            "provenance_ref": dict(persisted["provenance_ref"]),
        }
    )

    return AcceptanceRecordResult(
        uar_id=str(persisted["uar_id"]),
        record=persisted,
        history_id=str(entry["history_id"]),
    )

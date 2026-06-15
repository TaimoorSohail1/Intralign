"""Archival as a history event (DTM-0008; IC-WA-002 A3.8/A4.8; decision #6).

Archival destroys NOTHING: ``archive_assertion`` mutates no row and deletes no
row — it appends ONE ``history_record`` entry (``event_type='archived'``) and
emits ``knowledge_archived`` + ``knowledge_mutation_recorded``. The
``attested_assertion`` row stays fully intact, versioned, and auditable
(A3.8 preserved-not-destroyed; A7: Archived is terminal-for-activity, never
deletion — the object remains in the version chain and History).

Active/archived STATUS IS DERIVED from history (no schema change, no status
column — decision #6): ``is_archived`` reads the assertion's history entries;
the latest ``'archived'`` event wins. An explicit unarchive is OUT of scope in
R1 — no ``unarchived`` event type exists in the LDM §2.5 vocabulary, so once
archived an assertion stays archived (any later knowledge change is a NEW
version row, not a resurrection of the archived one).
"""

from __future__ import annotations

from pydantic import BaseModel

from backend.responsibilities.retain.admission import RetentionStore
from backend.services.observability.events import CollectingEventEmitter, EventEmitter


class AssertionNotFoundError(ValueError):
    """Archival must name an existing assertion — nothing exists to archive."""


class ArchivalResult(BaseModel):
    """What one archival produced: the appended history entry (no row changed)."""

    assertion_id: str
    history_id: str
    reason: str
    actor: str


def archive_assertion(
    assertion_id: str,
    *,
    reason: str,
    actor: str,
    store: RetentionStore,
    emitter: EventEmitter | None = None,
) -> ArchivalResult:
    """Archive an assertion WITHOUT destruction: one history entry, two events.

    No UPDATE, no DELETE, no row written to ``attested_assertion`` — the only
    write is the append-only ``history_record`` entry. The assertion row
    remains present, versioned, and auditable afterwards (A3.8; QA B2.7).

    Raises:
        AssertionNotFoundError: ``assertion_id`` does not resolve — rejected
            BEFORE any write or event.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    row = store.get_assertion(str(assertion_id))
    if row is None:
        raise AssertionNotFoundError(
            f"archival rejected — assertion {assertion_id!r} does not exist "
            "(IC-WA-002 A3.8: archival preserves existing knowledge)"
        )

    subject_id = str(row["assertion_id"])
    project_id = str(row["project_id"])
    entry = store.insert_history(
        {
            "event_type": "archived",
            "subject_ref": {
                "assertion_id": subject_id,
                "version": int(row["version"]),
                "reason": reason,
            },
            "actor": actor,
            "project_id": project_id,
            "created_by": actor,
            "epistemic_state": str(row["epistemic_state"]),
            "provenance_ref": dict(row["provenance_ref"]),
        }
    )

    audit = {
        "project_id": project_id,
        "assertion_id": subject_id,
        "reason": reason,
        "actor": actor,
    }
    seam.emit("knowledge_archived", audit)
    seam.emit("knowledge_mutation_recorded", {**audit, "mutation": "archival"})

    return ArchivalResult(
        assertion_id=subject_id,
        history_id=str(entry["history_id"]),
        reason=reason,
        actor=actor,
    )


def is_archived(assertion_id: str, *, store: RetentionStore) -> bool:
    """Derive archived status from history — the latest ``archived`` event wins.

    No status column exists (decision #6); the answer is read from the
    append-only history alone. No unarchive event type exists in R1, so any
    recorded ``archived`` entry means the assertion is archived.
    """
    events = store.history_for_assertion(str(assertion_id))
    return any(e.get("event_type") == "archived" for e in events)

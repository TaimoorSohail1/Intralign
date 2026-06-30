"""Archival + unarchival as history events (DTM-0008; IC-WA-002 A3.8/A4.8; decision #6).

Archival destroys NOTHING: ``archive_assertion`` mutates no row and deletes no
row — it appends ONE ``history_record`` entry (``event_type='archived'``) and
emits ``knowledge_archived`` + ``knowledge_mutation_recorded``. The
``attested_assertion`` row stays fully intact, versioned, and auditable
(A3.8 preserved-not-destroyed; A7: Archived is terminal-for-activity, never
deletion — the object remains in the version chain and History).

**Unarchive is reversible in R1 (DL-058; UP-3 affirmed; RB-025).** ``unarchive_assertion``
is symmetric and equally non-destructive: it appends ONE ``history_record``
entry (``event_type='unarchived'`` — LDM §2.5 vocabulary) and emits
``knowledge_unarchived`` + ``knowledge_mutation_recorded``. No row is mutated or
deleted; reversal is itself an append-only event, so the full lifecycle stays
auditable from history alone.

Active/archived STATUS IS DERIVED from history (no schema change, no status
column — decision #6): ``is_archived`` reads the assertion's ordered history
entries (oldest-first) and the **latest** of ``'archived'`` / ``'unarchived'``
wins. So an archive can be reversed, and a later re-archive flips status back —
each transition a distinct, ordered, append-only event.
"""

from __future__ import annotations

from pydantic import BaseModel

from backend.responsibilities.retain.admission import RetentionStore
from backend.services.observability.events import CollectingEventEmitter, EventEmitter


class AssertionNotFoundError(ValueError):
    """Archival must name an existing assertion — nothing exists to archive."""


class NotArchivedError(ValueError):
    """Unarchive must reverse an ACTIVE archive — there is nothing to reverse."""


class ArchivalResult(BaseModel):
    """What one archival produced: the appended history entry (no row changed)."""

    assertion_id: str
    history_id: str
    reason: str
    actor: str


class UnarchivalResult(BaseModel):
    """What one unarchival produced: the appended reversal entry (no row changed)."""

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


def unarchive_assertion(
    assertion_id: str,
    *,
    reason: str,
    actor: str,
    store: RetentionStore,
    emitter: EventEmitter | None = None,
) -> UnarchivalResult:
    """Reverse an archive WITHOUT destruction: one history entry, two events (DL-058).

    Symmetric to ``archive_assertion``: no UPDATE, no DELETE — the only write is
    the append-only ``history_record`` reversal entry (``event_type='unarchived'``).
    Status is re-derived from history; the latest of archived/unarchived wins.

    Raises:
        AssertionNotFoundError: ``assertion_id`` does not resolve — rejected
            BEFORE any write or event.
        NotArchivedError: the assertion is not currently archived — there is
            nothing to reverse; rejected BEFORE any write or event (no spurious
            ``unarchived`` event is ever appended).
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    row = store.get_assertion(str(assertion_id))
    if row is None:
        raise AssertionNotFoundError(
            f"unarchive rejected — assertion {assertion_id!r} does not exist "
            "(IC-WA-002 A3.8: reversal preserves existing knowledge)"
        )
    if not is_archived(str(assertion_id), store=store):
        raise NotArchivedError(
            f"unarchive rejected — assertion {assertion_id!r} is not archived "
            "(nothing to reverse; reversal is append-only and never spurious)"
        )

    subject_id = str(row["assertion_id"])
    project_id = str(row["project_id"])
    entry = store.insert_history(
        {
            "event_type": "unarchived",
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
    seam.emit("knowledge_unarchived", audit)
    seam.emit("knowledge_mutation_recorded", {**audit, "mutation": "unarchival"})

    return UnarchivalResult(
        assertion_id=subject_id,
        history_id=str(entry["history_id"]),
        reason=reason,
        actor=actor,
    )


def is_archived(assertion_id: str, *, store: RetentionStore) -> bool:
    """Derive archived status from ordered history — latest archive/unarchive wins.

    No status column exists (decision #6); the answer is read from the
    append-only history alone. History is returned oldest-first (the real store
    orders by ``at`` then ``created_at``; the in-memory store preserves insert
    order), so the LAST ``archived``/``unarchived`` transition is authoritative:
    archive → archived; a later unarchive → active; a later re-archive → archived.
    """
    archived = False
    for e in store.history_for_assertion(str(assertion_id)):
        event_type = e.get("event_type")
        if event_type == "archived":
            archived = True
        elif event_type == "unarchived":
            archived = False
    return archived

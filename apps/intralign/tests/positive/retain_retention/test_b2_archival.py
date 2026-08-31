"""QA-WA-002 B2.7 — archival without destruction (pure; decision #6).

Archival appends ONE ``archived`` history entry and emits its events; the
assertion row is untouched (no mutation, no deletion) and active/archived
status is DERIVED from history alone.
"""

from __future__ import annotations

import pytest

from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.archival import (
    AssertionNotFoundError,
    archive_assertion,
    is_archived,
)
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate


def _admitted(store) -> dict:
    candidate = store.seed_candidate(ready_candidate())
    result = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    return store.get_assertion(result.assertion_ids[0])


def test_b2_7_archival_appends_history_and_emits_events() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    row = _admitted(store)

    result = archive_assertion(
        row["assertion_id"],
        reason="superseded project scope",
        actor="user-42",
        store=store,
        emitter=emitter,
    )

    archived_entries = [
        h
        for h in store.history_for_assertion(row["assertion_id"])
        if h["event_type"] == "archived"
    ]
    assert len(archived_entries) == 1
    entry = archived_entries[0]
    assert entry["history_id"] == result.history_id
    assert entry["subject_ref"]["reason"] == "superseded project scope"
    assert entry["actor"] == "user-42"
    assert emitter.names == ["knowledge_archived", "knowledge_mutation_recorded"]
    assert emitter.events[0][1]["assertion_id"] == row["assertion_id"]


def test_b2_7_archived_row_remains_fully_intact_and_auditable() -> None:
    """A3.8 — preserved, not destroyed: the row after archival == before."""
    store = InMemoryRetentionStore()
    row = _admitted(store)
    before = dict(row)

    archive_assertion(
        row["assertion_id"], reason="stale", actor="user-42", store=store,
        emitter=CollectingEventEmitter(),
    )

    after = store.get_assertion(row["assertion_id"])
    assert after == before  # no field changed — archival wrote NO row mutation
    assert len(store.assertions) == 1  # nothing deleted
    # Provenance still present and auditable (A4.10).
    assert after["provenance_ref"]["integrity_clearance"]


def test_b2_7_status_is_derived_from_history() -> None:
    store = InMemoryRetentionStore()
    row = _admitted(store)
    assert is_archived(row["assertion_id"], store=store) is False
    archive_assertion(
        row["assertion_id"], reason="stale", actor="user-42", store=store,
        emitter=CollectingEventEmitter(),
    )
    assert is_archived(row["assertion_id"], store=store) is True


def test_archiving_a_missing_assertion_is_rejected_before_any_write() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    with pytest.raises(AssertionNotFoundError):
        archive_assertion(
            "00000000-0000-0000-0000-000000000000",
            reason="stale",
            actor="user-42",
            store=store,
            emitter=emitter,
        )
    assert store.history == []
    assert emitter.events == []

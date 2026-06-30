"""QA-WA-002 — unarchive (archive reversal) without destruction (RB-025 / DL-058).

Symmetric to archival (B2.7): unarchive appends ONE ``unarchived`` history entry
and emits its events; the assertion row is untouched (no mutation, no deletion);
active/archived status is DERIVED from the ordered history — the latest of
``archived`` / ``unarchived`` wins, so an archive can be reversed and a later
re-archive flips status back. Reversal is itself append-only (UP-3 affirmed).
"""

from __future__ import annotations

import pytest

from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.archival import (
    AssertionNotFoundError,
    NotArchivedError,
    archive_assertion,
    is_archived,
    unarchive_assertion,
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


def _archive(store, assertion_id: str) -> None:
    archive_assertion(
        assertion_id, reason="stale", actor="user-42", store=store,
        emitter=CollectingEventEmitter(),
    )


def test_unarchive_appends_reversal_history_and_emits_events() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    row = _admitted(store)
    _archive(store, row["assertion_id"])

    result = unarchive_assertion(
        row["assertion_id"], reason="back in scope", actor="user-42",
        store=store, emitter=emitter,
    )

    unarchived = [
        h for h in store.history_for_assertion(row["assertion_id"])
        if h["event_type"] == "unarchived"
    ]
    assert len(unarchived) == 1
    entry = unarchived[0]
    assert entry["history_id"] == result.history_id
    assert entry["subject_ref"]["reason"] == "back in scope"
    assert entry["actor"] == "user-42"
    assert emitter.names == ["knowledge_unarchived", "knowledge_mutation_recorded"]
    assert emitter.events[1][1]["mutation"] == "unarchival"


def test_unarchive_flips_derived_status_back_to_active() -> None:
    store = InMemoryRetentionStore()
    row = _admitted(store)
    _archive(store, row["assertion_id"])
    assert is_archived(row["assertion_id"], store=store) is True

    unarchive_assertion(
        row["assertion_id"], reason="back in scope", actor="user-42",
        store=store, emitter=CollectingEventEmitter(),
    )
    assert is_archived(row["assertion_id"], store=store) is False


def test_unarchive_is_non_destructive_row_intact() -> None:
    """The assertion row after unarchive == before — reversal writes NO row mutation."""
    store = InMemoryRetentionStore()
    row = _admitted(store)
    before = dict(row)
    _archive(store, row["assertion_id"])

    unarchive_assertion(
        row["assertion_id"], reason="back in scope", actor="user-42",
        store=store, emitter=CollectingEventEmitter(),
    )

    after = store.get_assertion(row["assertion_id"])
    assert after == before  # no field changed
    assert len(store.assertions) == 1  # nothing deleted


def test_re_archive_after_unarchive_flips_status_back_latest_wins() -> None:
    store = InMemoryRetentionStore()
    row = _admitted(store)
    _archive(store, row["assertion_id"])
    unarchive_assertion(
        row["assertion_id"], reason="back", actor="u", store=store,
        emitter=CollectingEventEmitter(),
    )
    assert is_archived(row["assertion_id"], store=store) is False

    _archive(store, row["assertion_id"])  # latest transition wins
    assert is_archived(row["assertion_id"], store=store) is True


def test_unarchiving_a_missing_assertion_is_rejected_before_any_write() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    with pytest.raises(AssertionNotFoundError):
        unarchive_assertion(
            "00000000-0000-0000-0000-000000000000",
            reason="x", actor="u", store=store, emitter=emitter,
        )
    assert store.history == []
    assert emitter.events == []


def test_unarchiving_a_non_archived_assertion_is_rejected_no_spurious_event() -> None:
    """Nothing to reverse — NotArchivedError, and NO unarchived event is appended."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    row = _admitted(store)  # admitted but never archived
    history_before = list(store.history)

    with pytest.raises(NotArchivedError):
        unarchive_assertion(
            row["assertion_id"], reason="x", actor="u", store=store, emitter=emitter,
        )

    assert store.history == history_before  # no reversal entry appended
    assert emitter.events == []
    assert is_archived(row["assertion_id"], store=store) is False

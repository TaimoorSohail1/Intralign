"""QA-WA-002 §B+ positive 3 — User Acceptance Record creation (pure; decision #9).

A captured acceptance action (DTM-0007 handoff) becomes a version-pinned,
user-attested ``user_acceptance_record`` row plus one ``acceptance-recorded``
history entry — decoupled from the accepted item, which is never touched.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from backend.responsibilities.perceive.acceptance_capture import capture_acceptance
from backend.responsibilities.retain.acceptance import record_acceptance
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore

USER = str(uuid.uuid4())
PIN = str(uuid.uuid4())
PROJECT = str(uuid.uuid4())


def _capture():
    return capture_acceptance(
        {
            "user_id": USER,
            "target_kind": "recommendation",
            "version_pin": PIN,
            "action": "accept",
            "project_id": PROJECT,
        },
        emitter=CollectingEventEmitter(),
    )


def test_b_plus_3_uar_row_is_version_pinned_and_user_attested() -> None:
    store = InMemoryRetentionStore()
    result = record_acceptance(_capture(), project_id=PROJECT, store=store)

    row = store.get_acceptance(result.uar_id)
    assert row["user_id"] == USER
    assert row["action"] == "accept"
    assert row["target_kind"] == "recommendation"
    assert row["version_pin"] == PIN  # pinned to the EXACT accepted version
    assert row["project_id"] == PROJECT
    assert row["epistemic_state"] == "attested-user"
    assert row["created_by"] == USER
    # Provenance names the Perceive capture event that preceded this write.
    assert row["provenance_ref"]["capture_event"] == "user_acceptance_captured"
    assert row["provenance_ref"]["version_pin"] == PIN


def test_b_plus_3_acceptance_recorded_history_entry_appended() -> None:
    store = InMemoryRetentionStore()
    result = record_acceptance(_capture(), project_id=PROJECT, store=store)

    entries = [h for h in store.history if h["event_type"] == "acceptance-recorded"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["history_id"] == result.history_id
    assert entry["subject_ref"]["uar_id"] == result.uar_id
    assert entry["subject_ref"]["version_pin"] == PIN
    assert entry["actor"] == USER
    assert entry["epistemic_state"] == "attested-user"


def test_uar_write_touches_only_its_two_tables() -> None:
    """Decoupled (DL-043): the accepted item is never touched by recording."""
    store = InMemoryRetentionStore()
    record_acceptance(_capture(), project_id=PROJECT, store=store)
    assert store.tables_written == ["user_acceptance_record", "history_record"]
    assert store.assertions == []  # no attested_assertion written or changed


def test_b_plus_3_uar_row_inserts_into_the_real_table_live() -> None:
    """LIVE — the UAR row shape satisfies the real DTM-0002 table (uuid pins,
    action CHECK, attested-user pin) and replays record-exact after insert."""
    import os

    try:
        from supabase import create_client
    except ImportError:  # pragma: no cover - CI venv without supabase-py
        create_client = None  # type: ignore[assignment]
    import pytest

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if create_client is None or not url or not key:
        pytest.skip(
            "local Supabase stack not configured — set SUPABASE_URL and "
            "SUPABASE_SERVICE_ROLE_KEY from `supabase status`"
        )
    from backend.services.persistence.retention_store import SupabaseRetentionStore

    store = SupabaseRetentionStore(create_client(url, key))
    result = record_acceptance(_capture(), project_id=PROJECT, store=store)
    row = store.get_acceptance(result.uar_id)
    assert row is not None
    assert row["version_pin"] == PIN
    assert row["action"] == "accept"
    assert row["epistemic_state"] == "attested-user"
    # Record-exact (C+): the re-read row is the stored fact, verbatim.
    assert store.get_acceptance(result.uar_id) == row


def test_capture_timestamp_is_preserved_as_confirmed_at() -> None:
    store = InMemoryRetentionStore()
    when = datetime(2026, 6, 12, 9, 30, tzinfo=UTC)
    capture = capture_acceptance(
        {
            "user_id": USER,
            "target_kind": "finding",
            "version_pin": PIN,
            "action": "defer",
            "captured_at": when,
        },
        emitter=CollectingEventEmitter(),
    )
    result = record_acceptance(capture, project_id=PROJECT, store=store)
    assert store.get_acceptance(result.uar_id)["confirmed_at"] == when.isoformat()

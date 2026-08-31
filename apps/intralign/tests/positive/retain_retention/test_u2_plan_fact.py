"""QA-WU-ACCEPT U2 positive — Plan-Fact recording (DTM-0016; IC-WU-ACCEPT U1.2).

On a user CONFIRM (accept / direct-edit) the acceptance path records TWO
canonical items, append-only: the version-pinned ``UserAcceptanceRecord`` AND a
user-attested **plan fact** (an ``attested_assertion`` row, ``attesting_source =
user``, ``epistemic_state = attested-user``) holding the confirmed content as
"factual in the plan, attributed to the user". On reject / defer the UAR records
the action but NO plan fact is written. The path emits
``user_acceptance_record_appended`` (always) + ``plan_fact_recorded`` (confirm
only). The USER authors the plan fact — OSLO never self-accepts (hard rule #5).
"""

from __future__ import annotations

import uuid

from backend.responsibilities.perceive.acceptance_capture import capture_acceptance
from backend.responsibilities.retain.acceptance import record_acceptance
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import (
    InMemoryChrReader,
    InMemoryRetentionStore,
)

USER = str(uuid.uuid4())
PIN = str(uuid.uuid4())
PROJECT = str(uuid.uuid4())
ACCEPTED_CONTENT = "Adopt the two-phase rollout milestone plan."


def _capture(action: str = "accept", *, edit_content: str | None = None):
    fields = {
        "user_id": USER,
        "target_kind": "recommendation",
        "version_pin": PIN,
        "action": action,
        "project_id": PROJECT,
    }
    if edit_content is not None:
        fields["edit_content"] = edit_content
    return capture_acceptance(fields, emitter=CollectingEventEmitter())


def _reader() -> InMemoryChrReader:
    """A CHR reader pinned to PIN — the accepted recommendation's payload."""
    reader = InMemoryChrReader()
    reader.seed(PIN, {"summary": ACCEPTED_CONTENT})
    return reader


# --- accept -> UAR + plan fact -------------------------------------------------


def test_u2_accept_writes_both_the_uar_and_a_plan_fact() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    result = record_acceptance(
        _capture("accept"),
        project_id=PROJECT,
        store=store,
        emitter=emitter,
        chr_reader=_reader(),
    )
    # (a) the UAR row (version-pinned, user-attested) — unchanged Wave-A shape.
    uar = store.get_acceptance(result.uar_id)
    assert uar["action"] == "accept"
    assert uar["version_pin"] == PIN
    assert uar["epistemic_state"] == "attested-user"
    # (b) the plan fact — a user-attested attested_assertion row.
    assert result.plan_fact_id is not None
    plan_fact = store.get_assertion(result.plan_fact_id)
    assert plan_fact["epistemic_state"] == "attested-user"
    assert plan_fact["attesting_source"] == USER  # the USER is the source
    assert plan_fact["created_by"] == USER
    assert plan_fact["proposition"] == ACCEPTED_CONTENT  # confirmed content
    assert plan_fact["content_type"] == "fact"
    assert plan_fact["project_id"] == PROJECT


def test_u2_accept_plan_fact_is_version_pinned_to_the_accepted_emission() -> None:
    store = InMemoryRetentionStore()
    result = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    # The plan fact's provenance pins the exact accepted version + the user.
    prov = plan_fact["provenance_ref"]
    assert prov["version_pin"] == PIN
    assert prov["user_id"] == USER
    assert prov["action"] == "accept"
    assert prov["capture_event"] == "user_acceptance_captured"
    # The source_ref also carries the version reference (audit lineage).
    assert plan_fact["source_ref"]["version_pin"] == PIN


def test_u2_accept_plan_fact_content_is_a_data_read_of_the_pinned_chr() -> None:
    """The accepted content comes from the pinned CHR payload — a data read, no
    LLM. The accepted Derived recommendation STAYS Derived (OSLO never promotes
    it); the USER's confirmation authors the plan fact (hard rule #5)."""
    store = InMemoryRetentionStore()
    reader = InMemoryChrReader()
    reader.seed(PIN, {"summary": "Confirm the staffing assumption.", "state": "generated"})
    result = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=reader
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    assert plan_fact["proposition"] == "Confirm the staffing assumption."
    # The plan fact is NOT the recommendation: it is a fresh attested-user row,
    # not the Derived emission, and carries no recommendation 'state' field.
    assert "state" not in plan_fact


# --- direct_edit -> plan fact from the edit content (no recommendation) --------


def test_u2_direct_edit_writes_plan_fact_from_edit_content_without_a_recommendation() -> None:
    """A direct edit authors content directly — a plan fact is written from the
    capture's edit_content even with NO recommendation/CHR to derive from."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    edited = "Ship the API gateway in sprint 4 (user-authored)."
    result = record_acceptance(
        _capture("direct_edit", edit_content=edited),
        project_id=PROJECT,
        store=store,
        emitter=emitter,
        chr_reader=None,  # no recommendation needed for a direct edit
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    assert plan_fact["proposition"] == edited
    assert plan_fact["attesting_source"] == USER
    assert plan_fact["epistemic_state"] == "attested-user"
    assert plan_fact["provenance_ref"]["action"] == "direct_edit"
    # The UAR still recorded the direct_edit action.
    assert store.get_acceptance(result.uar_id)["action"] == "direct_edit"


# --- reject / defer -> UAR only, NO plan fact ----------------------------------


def test_u2_reject_records_the_uar_but_no_plan_fact() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    result = record_acceptance(
        _capture("reject"), project_id=PROJECT, store=store, emitter=emitter
    )
    assert store.get_acceptance(result.uar_id)["action"] == "reject"
    assert result.plan_fact_id is None
    assert result.plan_fact is None
    assert store.assertions == []  # nothing confirmed as factual
    # Only the UAR's two tables were touched — no attested_assertion.
    assert store.tables_written == ["user_acceptance_record", "history_record"]


def test_u2_defer_records_the_uar_but_no_plan_fact() -> None:
    store = InMemoryRetentionStore()
    result = record_acceptance(_capture("defer"), project_id=PROJECT, store=store)
    assert store.get_acceptance(result.uar_id)["action"] == "defer"
    assert result.plan_fact_id is None
    assert store.assertions == []


# --- events --------------------------------------------------------------------


def test_u2_accept_emits_uar_appended_then_plan_fact_recorded() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    record_acceptance(
        _capture("accept"),
        project_id=PROJECT,
        store=store,
        emitter=emitter,
        chr_reader=_reader(),
    )
    assert emitter.names == [
        "user_acceptance_record_appended",
        "plan_fact_recorded",
    ]
    # The plan-fact event carries the user attribution + the version-pin (C3 audit).
    plan_evt = emitter.events[1][1]
    assert plan_evt["attested_by_user"] == USER
    assert plan_evt["version_pin"] == PIN
    assert plan_evt["content_type"] == "fact"
    # The UAR event carries the acceptance->emission linkage (version reference).
    uar_evt = emitter.events[0][1]
    assert uar_evt["version_pin"] == PIN
    assert uar_evt["action"] == "accept"


def test_u2_direct_edit_emits_both_events() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    record_acceptance(
        _capture("direct_edit", edit_content="x."),
        project_id=PROJECT,
        store=store,
        emitter=emitter,
    )
    assert emitter.names == [
        "user_acceptance_record_appended",
        "plan_fact_recorded",
    ]


def test_u2_reject_emits_only_the_uar_event_not_plan_fact_recorded() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    record_acceptance(
        _capture("reject"), project_id=PROJECT, store=store, emitter=emitter
    )
    assert emitter.names == ["user_acceptance_record_appended"]
    assert "plan_fact_recorded" not in emitter.names


# --- append-only ---------------------------------------------------------------


def test_u2_two_accepts_append_two_distinct_plan_facts_never_overwrite() -> None:
    """Append-only: a second confirm writes a NEW plan-fact row; the first is
    untouched (no overwrite, no supersedes_id)."""
    store = InMemoryRetentionStore()
    r1 = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    r2 = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    assert r1.plan_fact_id != r2.plan_fact_id
    assert len(store.assertions) == 2  # two distinct rows
    # The plan fact is a fresh row — never a supersession of a prior one.
    for row in store.assertions:
        assert row["supersedes_id"] is None


def test_u2_plan_fact_history_entry_is_appended() -> None:
    """The plan-fact write appends its own audit entry. It reuses the admitted
    ``acceptance-recorded`` event_type (no migration; the history CHECK admits no
    ``plan-fact-recorded``), discriminated by ``subject_ref.record == 'plan_fact'``
    and the assertion_id."""
    store = InMemoryRetentionStore()
    result = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    entries = [
        h
        for h in store.history
        if h["event_type"] == "acceptance-recorded"
        and h["subject_ref"].get("record") == "plan_fact"
    ]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["subject_ref"]["assertion_id"] == result.plan_fact_id
    assert entry["subject_ref"]["uar_id"] == result.uar_id
    assert entry["actor"] == USER
    assert entry["epistemic_state"] == "attested-user"
    # The accept appended exactly two history entries: the UAR's + the plan fact's.
    acc_entries = [h for h in store.history if h["event_type"] == "acceptance-recorded"]
    assert len(acc_entries) == 2


# --- live ----------------------------------------------------------------------


def test_u2_plan_fact_inserts_into_the_real_attested_assertion_table_live() -> None:
    """LIVE — the plan-fact row satisfies the real attested_assertion table
    (attested-user CHECK admits it; no migration) and replays record-exact."""
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
    result = record_acceptance(
        _capture("accept"), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    plan_fact = store.get_assertion(result.plan_fact_id)
    assert plan_fact is not None
    assert plan_fact["epistemic_state"] == "attested-user"
    assert plan_fact["attesting_source"] == USER
    assert plan_fact["proposition"] == ACCEPTED_CONTENT
    # Record-exact (C+): the re-read row is the stored fact, verbatim.
    assert store.get_assertion(result.plan_fact_id) == plan_fact

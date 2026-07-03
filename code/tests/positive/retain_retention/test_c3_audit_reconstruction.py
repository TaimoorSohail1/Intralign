"""OBS-WA-002 C3/C4 — the full retention lifecycle is reconstructable (pure).

From the append-only ``history_record`` entries plus the collected A6 events
ALONE, the whole story of any canonical object is rebuilt: which attesting
source produced it, from what origin, through which integrity clearance,
through which versions, and whether/why it was archived — admission,
versioning, supersession, and archival each leave exactly their auditable
trace (C3: source, provenance, version chain, integrity-clearance reference).
"""

from __future__ import annotations

from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.archival import archive_assertion
from backend.responsibilities.retain.versioning import version_assertion, version_chain
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate


def _full_lifecycle(store, emitter):
    """admission -> version (v2) -> archival of v1; returns (candidate, v1, v2)."""
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(candidate, [draft()], store=store, emitter=emitter)
    v1_id = admitted.assertion_ids[0]
    versioned = version_assertion(
        v1_id, {"proposition": "revised."}, store=store, emitter=emitter
    )
    archive_assertion(
        v1_id, reason="superseded by v2", actor="user-42", store=store, emitter=emitter
    )
    return candidate, v1_id, versioned.assertion_id


def test_c3_lifecycle_reconstructable_from_history_alone() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate, v1_id, v2_id = _full_lifecycle(store, emitter)

    # --- v1's history tells its whole story, in order ----------------------
    v1_events = [h["event_type"] for h in store.history_for_assertion(v1_id)]
    assert v1_events == ["knowledge-versioned", "superseded", "archived"]
    v1_history = store.history_for_assertion(v1_id)
    # Admission trace: v1 creation names the candidate it came from.
    assert v1_history[0]["subject_ref"]["candidate_id"] == candidate["candidate_id"]
    # Supersession trace: prior names its successor (predecessor/successor C3).
    assert v1_history[1]["subject_ref"]["superseded_by"] == v2_id
    # Archival trace: reason + actor recorded; provenance still attached.
    assert v1_history[2]["subject_ref"]["reason"] == "superseded by v2"
    assert v1_history[2]["actor"] == "user-42"
    assert v1_history[2]["provenance_ref"]["integrity_clearance"]

    # --- v2's history names its predecessor --------------------------------
    v2_history = store.history_for_assertion(v2_id)
    assert [h["event_type"] for h in v2_history] == ["knowledge-versioned"]
    assert v2_history[0]["subject_ref"]["supersedes_id"] == v1_id

    # --- the integrity-clearance entry closes the admission trace (C5) -----
    clearance_entries = [
        h for h in store.history if h["event_type"] == "integrity-clearance"
    ]
    assert len(clearance_entries) == 1
    assert v1_id in clearance_entries[0]["subject_ref"]["assertion_ids"]
    assert (
        clearance_entries[0]["subject_ref"]["integrity_clearance"]
        == candidate["integrity_clearance"]
    )

    # --- version chain replays from the rows alone (C5) ---------------------
    assert [c["assertion_id"] for c in version_chain(v2_id, store=store)] == [
        v2_id,
        v1_id,
    ]


def test_c2_every_mutation_emitted_exactly_its_events_in_order() -> None:
    """C2 — emission stream mirrors the mutation story one-to-one, in order."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    _full_lifecycle(store, emitter)

    assert emitter.names == [
        # admission
        "knowledge_promoted",
        "knowledge_mutation_recorded",
        # versioning + explicit supersession
        "knowledge_versioned",
        "knowledge_superseded",
        "knowledge_mutation_recorded",
        # archival
        "knowledge_archived",
        "knowledge_mutation_recorded",
    ]
    # Every knowledge mutation also produced a history write: 3 mutations ->
    # integrity-clearance + v1-versioned + v2-versioned + superseded + archived.
    assert len(store.history) == 5


def test_c3_events_and_history_agree_on_identities() -> None:
    """Cross-check: the event stream and the history rows name the SAME objects."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    _, v1_id, v2_id = _full_lifecycle(store, emitter)

    by_name = {name: payload for name, payload in emitter.events}
    assert by_name["knowledge_promoted"]["assertion_ids"] == [v1_id]
    assert by_name["knowledge_versioned"]["assertion_id"] == v2_id
    assert by_name["knowledge_superseded"]["assertion_id"] == v1_id
    assert by_name["knowledge_superseded"]["superseded_by"] == v2_id
    assert by_name["knowledge_archived"]["assertion_id"] == v1_id

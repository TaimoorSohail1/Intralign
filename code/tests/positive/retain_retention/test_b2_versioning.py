"""QA-WA-002 B2.2/B2.5 — version-on-mutation + explicit supersession (pure).

A knowledge mutation produces a NEW version row (v2) with the prior (v1)
fully intact, marked superseded ONLY via explicit recorded events — both
history entries appended, all three A6 events emitted — and the version chain
is reconstructable from the rows alone.
"""

from __future__ import annotations

from backend.responsibilities.adapt.triggers import validate_trigger
from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.versioning import version_assertion, version_chain
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate


def _admitted_v1(store) -> dict:
    candidate = store.seed_candidate(ready_candidate())
    result = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    return store.get_assertion(result.assertion_ids[0])


def test_b2_2_mutation_creates_new_version_prior_intact() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    v1 = _admitted_v1(store)
    v1_snapshot = dict(v1)

    result = version_assertion(
        v1["assertion_id"],
        {"proposition": "The launch must hold — revised to Q1."},
        store=store,
        emitter=emitter,
    )

    # New row: version prior+1, explicit supersedes link (B2.2).
    v2 = store.get_assertion(result.assertion_id)
    assert v2["version"] == 2
    assert v2["supersedes_id"] == v1["assertion_id"]
    assert v2["proposition"] == "The launch must hold — revised to Q1."
    # BOTH rows present; the prior is byte-for-byte what it was (B3.1).
    assert len(store.assertions) == 2
    assert store.get_assertion(v1["assertion_id"]) == v1_snapshot
    # Unchanged fields carried from the prior (content continuity).
    assert v2["content_type"] == v1["content_type"]
    assert v2["attesting_source"] == v1["attesting_source"]


def test_b2_2_provenance_carried_forward_on_version() -> None:
    """B2.3/A4.10 — versioning never drops provenance; adds the version link."""
    store = InMemoryRetentionStore()
    v1 = _admitted_v1(store)
    result = version_assertion(
        v1["assertion_id"],
        {"proposition": "revised."},
        store=store,
        emitter=CollectingEventEmitter(),
    )
    v2 = store.get_assertion(result.assertion_id)
    for key in ("origin_artifact", "candidate_ref", "integrity_clearance"):
        assert v2["provenance_ref"][key] == v1["provenance_ref"][key]
    assert v2["provenance_ref"]["versioned_from"] == v1["assertion_id"]


def test_b2_5_supersession_is_explicit_marked_and_traceable() -> None:
    """B2.5 — explicit supersession: dual history entries + all three events."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    v1 = _admitted_v1(store)

    result = version_assertion(
        v1["assertion_id"], {"proposition": "revised."}, store=store, emitter=emitter
    )

    # History: knowledge-versioned (new) AND superseded (prior) — A4.9.
    new_history = store.history_for_assertion(result.assertion_id)
    assert [h["event_type"] for h in new_history] == ["knowledge-versioned"]
    assert new_history[0]["subject_ref"]["supersedes_id"] == v1["assertion_id"]
    prior_history = store.history_for_assertion(v1["assertion_id"])
    assert "superseded" in [h["event_type"] for h in prior_history]
    superseded_entry = next(
        h for h in prior_history if h["event_type"] == "superseded"
    )
    assert superseded_entry["subject_ref"]["superseded_by"] == result.assertion_id
    # Events: versioned + superseded + mutation recorded, in order (A6).
    assert emitter.names == [
        "knowledge_versioned",
        "knowledge_superseded",
        "knowledge_mutation_recorded",
    ]
    superseded_payload = emitter.events[1][1]
    assert superseded_payload["assertion_id"] == v1["assertion_id"]
    assert superseded_payload["superseded_by"] == result.assertion_id


def test_b2_6_versioning_constructs_a_valid_knowledge_change_trigger() -> None:
    store = InMemoryRetentionStore()
    v1 = _admitted_v1(store)
    result = version_assertion(
        v1["assertion_id"],
        {"proposition": "revised."},
        store=store,
        emitter=CollectingEventEmitter(),
    )
    claim = result.change_trigger
    assert claim.trigger_type.value == "knowledge-change"
    assert claim.information_changed is True
    assert validate_trigger(claim) is claim


def test_version_chain_reconstructs_v2_then_v1() -> None:
    """A3.7/C5 — the ordered version story is readable from the rows alone."""
    store = InMemoryRetentionStore()
    v1 = _admitted_v1(store)
    r2 = version_assertion(
        v1["assertion_id"], {"proposition": "v2."}, store=store,
        emitter=CollectingEventEmitter(),
    )
    r3 = version_assertion(
        r2.assertion_id, {"proposition": "v3."}, store=store,
        emitter=CollectingEventEmitter(),
    )

    chain = version_chain(r3.assertion_id, store=store)
    assert [c["assertion_id"] for c in chain] == [
        r3.assertion_id,
        r2.assertion_id,
        v1["assertion_id"],
    ]
    assert [c["version"] for c in chain] == [3, 2, 1]
    # A draft (not just a mapping) is accepted as the new content too.
    r4 = version_assertion(
        r3.assertion_id, draft(proposition="v4 from a draft."), store=store,
        emitter=CollectingEventEmitter(),
    )
    assert store.get_assertion(r4.assertion_id)["proposition"] == "v4 from a draft."

    # version_chain of a missing id is empty, never an error loop.
    assert version_chain("00000000-0000-0000-0000-000000000000", store=store) == []

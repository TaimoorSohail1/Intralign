"""QA-WA-002 B2.1/B2.3/B2.4 + §B+ 4/5 — integrity-gated admission (pure).

A ready, integrity-cleared Promotion Candidate is admitted as one
``attested_assertion`` row per draft (Knowledge Promoted, initial version),
every row carrying full provenance (origin artifact + candidate ref +
integrity-clearance ref), history appended (``integrity-clearance`` +
``knowledge-versioned``), both A6 events emitted, and a VALID 00R
``promotion`` TriggerClaim constructed (never submitted).
"""

from __future__ import annotations

from backend.responsibilities.adapt.triggers import validate_trigger
from backend.responsibilities.retain.admission import admit_candidate
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate


def _admit(store, emitter, drafts=None, **candidate_overrides):
    candidate = store.seed_candidate(ready_candidate(**candidate_overrides))
    drafts = drafts if drafts is not None else [draft()]
    return candidate, admit_candidate(
        candidate, drafts, store=store, emitter=emitter
    )


def test_b2_1_ready_cleared_candidate_is_admitted_as_initial_version() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate, result = _admit(
        store,
        emitter,
        drafts=[
            draft(content_type="constraint", proposition="The launch must hold."),
            draft(content_type="fact", proposition="The deadline is 2026-09-01."),
        ],
    )

    # One attested_assertion row per draft, each the INITIAL version (B2.1).
    assert len(result.assertion_ids) == 2
    assert len(store.assertions) == 2
    for row in store.assertions:
        assert row["version"] == 1
        assert row["supersedes_id"] is None
        assert row["epistemic_state"] == "attested-evidence"
        assert row["project_id"] == candidate["project_id"]
    assert {r["content_type"] for r in store.assertions} == {"constraint", "fact"}
    # Both A6 events, in order (knowledge promoted + mutation recorded).
    assert emitter.names == ["knowledge_promoted", "knowledge_mutation_recorded"]
    promoted = emitter.events[0][1]
    assert promoted["assertion_ids"] == result.assertion_ids
    assert promoted["candidate_id"] == candidate["candidate_id"]


def test_b2_3_provenance_carried_on_every_admitted_row() -> None:
    """B2.3 / §B+ 5 — origin, candidate ref, and clearance ref on every object."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    the_draft = draft()
    candidate, result = _admit(store, emitter, drafts=[the_draft])

    row = store.get_assertion(result.assertion_ids[0])
    # source attribution + evidence locus preserved verbatim (A3.3/A4.10).
    assert row["attesting_source"] == the_draft.attesting_source
    assert row["source_ref"] == the_draft.source_ref
    # provenance_ref: origin artifact + candidate ref + integrity-clearance ref.
    prov = row["provenance_ref"]
    assert prov["origin_artifact"] == candidate["artifact_ref"]
    assert prov["candidate_ref"] == candidate["candidate_id"]
    assert prov["integrity_clearance"] == candidate["integrity_clearance"]
    assert prov["integrity_clearance"]["attribution"]["present"] is True


def test_b2_4_history_appended_for_admission() -> None:
    """B2.4 — admission produces append-only history: clearance + v1 creation."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate, result = _admit(store, emitter)

    kinds = [h["event_type"] for h in store.history]
    assert kinds == ["integrity-clearance", "knowledge-versioned"]
    clearance_entry = store.history[0]
    assert clearance_entry["subject_ref"]["candidate_id"] == candidate["candidate_id"]
    assert clearance_entry["subject_ref"]["assertion_ids"] == result.assertion_ids
    assert (
        clearance_entry["subject_ref"]["integrity_clearance"]
        == candidate["integrity_clearance"]
    )
    versioned_entry = store.history[1]
    assert versioned_entry["subject_ref"]["assertion_id"] == result.assertion_ids[0]
    assert versioned_entry["subject_ref"]["version"] == 1


def test_b2_6_admission_constructs_a_valid_promotion_trigger() -> None:
    """B2.6 — the mutation event constructs valid 00R input; Retain never runs it."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate, result = _admit(store, emitter)

    claim = result.promotion_trigger
    assert claim.trigger_type.value == "promotion"
    assert claim.information_changed is True
    assert claim.project_id == candidate["project_id"]
    # The constructed claim passes the 00R gate verbatim (A3.10).
    assert validate_trigger(claim) is claim
    # Constructed only: no recompute event was emitted by admission.
    assert "recompute_started" not in emitter.names
    assert "reanalysis_triggered" not in emitter.names


def test_b_plus_4_attested_assumption_constraint_dependency_admit() -> None:
    """§B+ positive 4 — attested assumption/constraint/dependency admission."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    _, result = _admit(
        store,
        emitter,
        drafts=[
            draft(content_type="assumption", proposition="We assume EU launch."),
            draft(content_type="constraint", proposition="It must ship in Q4."),
            draft(content_type="dependency", proposition="It depends on auth."),
        ],
    )
    assert len(result.assertion_ids) == 3
    assert {r["content_type"] for r in store.assertions} == {
        "assumption",
        "constraint",
        "dependency",
    }
    # All admitted as evidence-attested — never Derived (one-way flow intact).
    assert {r["epistemic_state"] for r in store.assertions} == {"attested-evidence"}


def test_candidate_can_be_passed_by_id() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate())
    result = admit_candidate(
        candidate["candidate_id"], [draft()], store=store, emitter=emitter
    )
    assert result.candidate_id == candidate["candidate_id"]
    assert len(store.assertions) == 1

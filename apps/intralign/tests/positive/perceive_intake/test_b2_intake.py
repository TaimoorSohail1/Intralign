"""QA-WA-001 B2 positive suite (pure) — the intake pipeline over fakes.

B2.1 preserved with provenance, append-only · B2.2 normalization preserves
meaning · B2.3 integrity clearance -> attributed Promotion Candidate ·
B2.4 idempotent re-intake, time-attributed ordering · B2.6 change/stale signal
on edit. (B2.5 acceptance capture lives in test_b2_acceptance_capture.py;
the live end-to-end pass lives in test_intake_live.py.)
"""

from __future__ import annotations

from datetime import UTC, datetime

from backend.responsibilities.adapt.triggers import validate_trigger
from backend.responsibilities.perceive.intake import (
    NORMALIZATION_RULES,
    NORMALIZATION_VERSION,
    IntakeSubmission,
    compute_dedup_key,
    normalize_content,
    receive_context_signal,
    submit_artifact,
)
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.perceive_intake.fakes import InMemoryBodyStore, InMemoryIntakeStore

PROJECT = "11111111-1111-1111-1111-111111111111"


def _submission(**overrides) -> IntakeSubmission:
    fields = {
        "project_id": PROJECT,
        "source": "evidence-source-7",
        "submitted_by": "user-42",
        "content": "# Plan\n\n- The deadline is 2026-09-01.\n- We must ship v1.\n",
        "submitted_at": datetime(2026, 6, 12, 9, 0, tzinfo=UTC),
    }
    return IntakeSubmission(**{**fields, **overrides})


def test_b2_1_artifact_preserved_with_full_provenance_append_only() -> None:
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    result = submit_artifact(_submission(), store=store, bodies=bodies, emitter=emitter)

    assert result.created is True
    [artifact] = store.artifacts
    # who / when / from-where (A3.1) — preserved verbatim.
    assert artifact["provenance"]["who"] == "user-42"
    assert artifact["provenance"]["from_where"] == "evidence-source-7"
    assert artifact["provenance"]["when"] == "2026-06-12T09:00:00+00:00"
    assert artifact["submitted_by"] == "user-42"
    assert artifact["epistemic_state"] == "attested-evidence"
    assert artifact["provenance_ref"]["dedup_key"] == result.dedup_key
    # The raw body is preserved byte-exactly in the body store.
    assert bodies.download_body(result.body_ref).decode() == _submission().content
    # Append-only: the store exposes NO mutator surface at all.
    assert not [n for n in dir(store) if n.startswith(("set_", "update_", "delete_"))]
    # A6 event chain for a clean intake, in A7 state order.
    assert emitter.names == [
        "artifact_received",
        "artifact_normalizing",
        "artifact_normalized",
        "promotion_candidate_ready",
    ]
    # C3 audit fields ride on every event: who/when/source.
    for _, payload in emitter.events:
        assert payload["submitted_by"] == "user-42"
        assert payload["source"] == "evidence-source-7"
        assert payload["submitted_at"] == "2026-06-12T09:00:00+00:00"


def test_b2_2_normalization_preserves_meaning() -> None:
    raw = "# Title\r\nline one.  \r\n\r\n\r\n- bullet must hold.\t\n\n\n"
    form = normalize_content(raw)
    # Documented, versioned rules ride with the form.
    assert form["version"] == NORMALIZATION_VERSION
    assert form["rules"] == list(NORMALIZATION_RULES)
    # Meaning preserved: the non-whitespace character stream is UNTOUCHED.
    assert "".join(form["text"].split()) == "".join(raw.split())
    # The transforms themselves: LF only, no trailing blanks, runs collapsed.
    assert "\r" not in form["text"]
    assert form["text"] == "# Title\nline one.\n\n- bullet must hold."
    # Section split on the heading; the split adds no characters.
    assert [s["heading"] for s in form["sections"]] == ["# Title"]
    assert form["sections"][0]["lines"] == ["line one.", "", "- bullet must hold."]


def test_b2_3_integrity_clearance_produces_attributed_candidate() -> None:
    store, bodies = InMemoryIntakeStore(), InMemoryBodyStore()
    result = submit_artifact(_submission(), store=store, bodies=bodies)

    assert result.readiness_state == "ready"
    [candidate] = store.candidates
    assert candidate["artifact_ref"] == result.artifact["artifact_id"]
    assert candidate["project_id"] == PROJECT
    clearance = candidate["integrity_clearance"]
    # All three integrity results recorded (A3.3): attribution, idempotency,
    # evidence chain — the OBS C3 integrity-clearance reference.
    assert clearance["attribution"] == {
        "present": True,
        "submitted_by": "user-42",
        "source": "evidence-source-7",
    }
    assert clearance["idempotency"]["dedup_key"] == result.dedup_key
    assert clearance["evidence_chain"]["intact"] is True
    assert clearance["evidence_chain"]["re_derivable"] is True
    assert clearance["evidence_chain"]["body_ref"] == result.body_ref


def test_b2_3_evidence_chain_failure_yields_failed_candidate() -> None:
    """A whitespace-only body cannot anchor evidence -> readiness fails, evented."""
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    result = submit_artifact(
        _submission(content="   \n  \n"), store=store, bodies=bodies, emitter=emitter
    )
    assert result.readiness_state == "failed"
    assert store.candidates[0]["readiness_state"] == "failed"
    assert emitter.names[-1] == "promotion_readiness_failed"
    failed_payload = emitter.events[-1][1]
    assert failed_payload["reason"] == "evidence-chain-incomplete"


def test_b2_4_idempotent_reintake_same_artifact_no_new_objects() -> None:
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    first = submit_artifact(_submission(), store=store, bodies=bodies, emitter=emitter)
    again = submit_artifact(_submission(), store=store, bodies=bodies, emitter=emitter)

    # Same submission is never double-admitted (A3.3/A3.8).
    assert again.created is False
    assert again.artifact["artifact_id"] == first.artifact["artifact_id"]
    assert again.dedup_key == first.dedup_key
    assert len(store.artifacts) == 1          # no second artifact row
    assert len(store.candidates) == 1         # no second candidate
    assert bodies.upload_calls == 1           # no second Storage object
    assert again.candidate["candidate_id"] == first.candidate["candidate_id"]
    assert again.modified_trigger is None     # unchanged content = no signal
    # Ordering/time attribution preserved: the original receipt stands.
    assert store.artifacts[0]["provenance"]["when"] == "2026-06-12T09:00:00+00:00"


def test_b2_4_dedup_key_is_project_and_source_scoped() -> None:
    """The same content from another project/source is a DIFFERENT admission."""
    key = compute_dedup_key(PROJECT, "evidence-source-7", "same words")
    assert key != compute_dedup_key(PROJECT, "evidence-source-8", "same words")
    assert key != compute_dedup_key(
        "22222222-2222-2222-2222-222222222222", "evidence-source-7", "same words"
    )
    assert key == compute_dedup_key(PROJECT, "evidence-source-7", "same words")


def test_b2_6_change_signal_on_resubmission_with_changed_content() -> None:
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    first = submit_artifact(_submission(), store=store, bodies=bodies, emitter=emitter)
    changed = submit_artifact(
        _submission(content="# Plan\n\n- The deadline MOVED to 2026-10-01.\n"),
        store=store,
        bodies=bodies,
        emitter=emitter,
    )

    # A NEW artifact version supersedes the prior one (append, never overwrite).
    assert changed.created is True
    assert changed.artifact["artifact_id"] != first.artifact["artifact_id"]
    assert changed.artifact["version"] == 2
    assert changed.artifact["supersedes_id"] == first.artifact["artifact_id"]
    # The change signal was emitted...
    assert "artifact_modified" in emitter.names
    modified_payload = next(p for n, p in emitter.events if n == "artifact_modified")
    assert modified_payload["supersedes_artifact_id"] == first.artifact["artifact_id"]
    # ...and a VALID 00R knowledge-change TriggerClaim was constructed (A9):
    # constructed only — submitting it is the caller's (orchestration's) move.
    claim = changed.modified_trigger
    assert claim is not None
    assert validate_trigger(claim) is claim
    assert claim.trigger_type.value == "knowledge-change"
    assert claim.information_changed is True
    assert claim.project_id == PROJECT


def test_context_signal_captured_and_evented() -> None:
    emitter = CollectingEventEmitter()
    signal = receive_context_signal(
        {
            "project_id": PROJECT,
            "signal_type": "external-update",
            "source": "calendar-feed",
        },
        emitter=emitter,
    )
    assert signal.signal_type == "external-update"
    assert emitter.names == ["context_signal_received"]
    assert emitter.events[0][1]["source"] == "calendar-feed"

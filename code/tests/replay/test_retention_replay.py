"""OBS-WA-002 C5 — retention replay: record-exact + version-chain (DTM-0008).

Same harness pattern as the CHR record-exact axis (canonical JSON, sorted
keys, byte-compare, tolerance 0 — Attested rows are stored facts):

- **Record-exact** — an admitted ``attested_assertion`` row replays
  byte-exactly against its capture snapshot; a tampered snapshot is detected
  and the differing field named (pure negative, never skips).
- **Version-chain replay** — the full ordered v1 -> v2 sequence reconstructs
  from the rows alone, BOTH rows present, the prior byte-for-byte intact, and
  every admission/version traceable to its integrity clearance
  (integrity-clearance verification, C5).

Pure axes use the in-memory retention fake; live axes run the same story
against the local Supabase stack (skip contract unchanged).
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping
from typing import Any

import pytest

from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.versioning import version_assertion, version_chain
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate
from tests.replay.conftest import live


def canonical_row_bytes(row: Mapping[str, Any]) -> bytes:
    """Canonical JSON serialization of a stored row (sorted, compact, UTF-8)."""
    return json.dumps(
        dict(row), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _diff_fields(expected: bytes, actual: bytes) -> tuple[str, ...]:
    left, right = json.loads(expected), json.loads(actual)
    keys = sorted(set(left) | set(right))
    return tuple(k for k in keys if left.get(k, ...) != right.get(k, ...))


def replay_assertion_record(assertion_id: str, store, snapshot: bytes) -> None:
    """Record-exact replay: re-read the assertion; byte-compare to snapshot."""
    current = store.get_assertion(assertion_id)
    assert current is not None, f"assertion {assertion_id} does not exist"
    current_bytes = canonical_row_bytes(current)
    if current_bytes != snapshot:
        fields = _diff_fields(snapshot, current_bytes)
        raise AssertionError(
            f"Critical determinism failure: attested_assertion {assertion_id} "
            f"is not record-exact on replay — differing field(s): "
            f"{', '.join(fields)}"
        )


def _admit_v1_v2(store):
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    v1_id = admitted.assertion_ids[0]
    versioned = version_assertion(
        v1_id,
        {"proposition": "The launch must hold — revised."},
        store=store,
        emitter=CollectingEventEmitter(),
    )
    return candidate, v1_id, versioned.assertion_id


# --- record-exact axis (pure) -------------------------------------------------


def test_admitted_assertion_replays_record_exact_pure() -> None:
    store = InMemoryRetentionStore()
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    assertion_id = admitted.assertion_ids[0]
    snapshot = canonical_row_bytes(store.get_assertion(assertion_id))
    # Byte-exact replay: any diff would raise; None return == exact match.
    assert replay_assertion_record(assertion_id, store, snapshot) is None


def test_tampered_assertion_snapshot_detected_naming_the_field_pure() -> None:
    """Negative: mutate the SNAPSHOT (the store untouched) -> loud failure."""
    store = InMemoryRetentionStore()
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    assertion_id = admitted.assertion_ids[0]
    tampered = json.loads(canonical_row_bytes(store.get_assertion(assertion_id)))
    tampered["proposition"] = "forged-after-capture"
    tampered_bytes = json.dumps(
        tampered, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

    with pytest.raises(AssertionError, match="proposition"):
        replay_assertion_record(assertion_id, store, tampered_bytes)


# --- version-chain axis (pure) -------------------------------------------------


def test_version_chain_replay_reconstructs_v1_v2_prior_intact_pure() -> None:
    store = InMemoryRetentionStore()
    candidate, v1_id, v2_id = _admit_v1_v2(store)
    v1_snapshot = canonical_row_bytes(store.get_assertion(v1_id))

    chain = version_chain(v2_id, store=store)
    # The full ordered sequence reconstructs: v2 then v1, links resolving.
    assert [c["assertion_id"] for c in chain] == [v2_id, v1_id]
    assert chain[0]["supersedes_id"] == v1_id
    assert chain[1]["supersedes_id"] is None
    assert [c["version"] for c in chain] == [2, 1]
    # Prior state intact — byte-for-byte (no silent overwrite, B3.1).
    assert replay_assertion_record(v1_id, store, v1_snapshot) is None
    # Integrity-clearance verification (C5): every chain hop references the
    # clearance that admitted the knowledge (no clearance-less canonical row).
    for hop in chain:
        assert hop["provenance_ref"]["integrity_clearance"], (
            f"assertion {hop['assertion_id']} has no integrity-clearance "
            "reference — C6 trust failure"
        )
    assert (
        chain[1]["provenance_ref"]["integrity_clearance"]
        == candidate["integrity_clearance"]
    )


# --- live axes (local Supabase stack) ------------------------------------------


@pytest.fixture()
def retention_store(client):
    from backend.services.persistence.retention_store import SupabaseRetentionStore

    return SupabaseRetentionStore(client)


@pytest.fixture()
def live_candidate(client):
    """A REAL ready candidate persisted by the DTM-0007 intake path."""
    from backend.responsibilities.perceive.intake import (
        IntakeSubmission,
        submit_artifact,
    )
    from backend.services.persistence.intake_store import SupabaseIntakeStore
    from backend.services.persistence.storage import ArtifactBodyStore

    result = submit_artifact(
        IntakeSubmission(
            project_id=str(uuid.uuid4()),
            source="evidence-source-replay-0008",
            submitted_by="user-replay",
            content="- The retention replay must hold.\n",
        ),
        store=SupabaseIntakeStore(client),
        bodies=ArtifactBodyStore(client),
    )
    assert result.readiness_state == "ready"
    return result.candidate


@live
def test_admitted_assertion_replays_record_exact_live(
    retention_store, live_candidate
) -> None:
    admitted = admit_candidate(
        live_candidate,
        [draft(proposition="The retention replay must hold.")],
        store=retention_store,
        emitter=CollectingEventEmitter(),
    )
    assertion_id = admitted.assertion_ids[0]
    snapshot = canonical_row_bytes(retention_store.get_assertion(assertion_id))
    assert replay_assertion_record(assertion_id, retention_store, snapshot) is None


@live
def test_version_chain_replay_live_both_rows_present_prior_intact(
    retention_store, live_candidate
) -> None:
    admitted = admit_candidate(
        live_candidate,
        [draft(proposition="The retention replay must hold.")],
        store=retention_store,
        emitter=CollectingEventEmitter(),
    )
    v1_id = admitted.assertion_ids[0]
    v1_snapshot = canonical_row_bytes(retention_store.get_assertion(v1_id))
    versioned = version_assertion(
        v1_id,
        {"proposition": "The retention replay must hold — revised."},
        store=retention_store,
        emitter=CollectingEventEmitter(),
    )

    chain = version_chain(versioned.assertion_id, store=retention_store)
    assert [c["assertion_id"] for c in chain] == [versioned.assertion_id, v1_id]
    assert [c["version"] for c in chain] == [2, 1]
    # BOTH rows present in the real table; the prior is byte-for-byte intact.
    assert replay_assertion_record(v1_id, retention_store, v1_snapshot) is None
    # Integrity-clearance verification against the REAL intake clearance.
    assert (
        chain[1]["provenance_ref"]["integrity_clearance"]
        == live_candidate["integrity_clearance"]
    )

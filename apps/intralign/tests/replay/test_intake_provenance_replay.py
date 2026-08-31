"""OBS-WA-001 C5 — provenance replay: reconstruct an intake's origin/lineage.

From the artifact + promotion_candidate rows alone (plus the body store), the
full intake story is rebuilt: who submitted, when, from where; what integrity
clearance the candidate carries; and the supersession chain of re-submissions.
Re-derivability is verified by re-running normalization over the preserved raw
body and comparing it to the stored normalized_form (record-exact).

Pure axis (in-memory fakes) never skips; the live axis runs against the local
Supabase stack (same skip contract as the other replay tests).
"""

from __future__ import annotations

import uuid

from backend.responsibilities.perceive.intake import (
    IntakeSubmission,
    normalize_content,
    submit_artifact,
)
from tests.positive.perceive_intake.fakes import InMemoryBodyStore, InMemoryIntakeStore
from tests.replay.conftest import live


def reconstruct_intake_provenance(artifact_id: str, store, bodies) -> dict:
    """Rebuild origin/lineage of one intake from its persisted rows (C5).

    Walks ``supersedes_id`` to the root, re-derives the normalized form from
    the preserved body, and returns the audit story. Raises AssertionError on
    any break — a non-reconstructable intake is a trust failure (C6).
    """
    chain: list[dict] = []
    cursor = store.get_artifact(artifact_id)
    assert cursor is not None, f"artifact {artifact_id} does not exist"
    while cursor is not None:
        provenance = cursor["provenance"]
        # Provenance present at every hop: who / when / from-where (C3).
        assert provenance.get("who") and provenance.get("when") and provenance.get(
            "source"
        ), f"artifact {cursor['artifact_id']} dropped provenance"
        # Record-exact re-derivation: normalize(preserved body) == stored form.
        body = bodies.download_body(cursor["body_ref"]).decode("utf-8")
        assert normalize_content(body) == cursor["normalized_form"], (
            f"artifact {cursor['artifact_id']} normalized_form is not "
            "re-derivable from its preserved body"
        )
        chain.append(cursor)
        parent_id = cursor.get("supersedes_id")
        cursor = store.get_artifact(str(parent_id)) if parent_id else None
    candidate = store.candidate_for_artifact(artifact_id)
    return {
        "artifact_chain": [str(a["artifact_id"]) for a in chain],
        "origin": chain[-1]["provenance"],
        "integrity_clearance": (
            candidate["integrity_clearance"] if candidate is not None else None
        ),
    }


def _submission(project_id: str, content: str) -> IntakeSubmission:
    return IntakeSubmission(
        project_id=project_id,
        source="evidence-source-replay",
        submitted_by="user-replay",
        content=content,
    )


def test_provenance_replay_reconstructs_origin_and_lineage_pure() -> None:
    store, bodies = InMemoryIntakeStore(), InMemoryBodyStore()
    project_id = str(uuid.uuid4())
    first = submit_artifact(_submission(project_id, "v1."), store=store, bodies=bodies)
    changed = submit_artifact(
        _submission(project_id, "v2 — changed."), store=store, bodies=bodies
    )

    story = reconstruct_intake_provenance(
        changed.artifact["artifact_id"], store, bodies
    )
    # Lineage: the new artifact heads the chain; the origin closes it.
    assert story["artifact_chain"] == [
        changed.artifact["artifact_id"],
        first.artifact["artifact_id"],
    ]
    assert story["origin"]["who"] == "user-replay"
    assert story["origin"]["source"] == "evidence-source-replay"
    # Integrity-clearance verification (C5): the candidate's results replay.
    clearance = story["integrity_clearance"]
    assert clearance["attribution"]["present"] is True
    assert clearance["evidence_chain"]["intact"] is True
    assert clearance["idempotency"]["dedup_key"] == changed.dedup_key


def test_provenance_replay_detects_a_broken_evidence_chain_pure() -> None:
    """Negative: tampering the stored normalized_form makes replay fail loudly."""
    import pytest

    store, bodies = InMemoryIntakeStore(), InMemoryBodyStore()
    project_id = str(uuid.uuid4())
    result = submit_artifact(_submission(project_id, "v1."), store=store, bodies=bodies)
    # Tamper the in-memory row (the REAL table forbids this — DB append-only).
    store.artifacts[0]["normalized_form"] = {"version": "wa001-n1", "text": "FORGED"}
    with pytest.raises(AssertionError, match="not\\s+.*re-derivable|re-derivable"):
        reconstruct_intake_provenance(result.artifact["artifact_id"], store, bodies)


@live
def test_provenance_replay_reconstructs_a_live_intake(client) -> None:
    from backend.services.persistence.intake_store import SupabaseIntakeStore
    from backend.services.persistence.storage import ArtifactBodyStore

    store, bodies = SupabaseIntakeStore(client), ArtifactBodyStore(client)
    project_id = str(uuid.uuid4())
    first = submit_artifact(
        _submission(project_id, "live v1."), store=store, bodies=bodies
    )
    changed = submit_artifact(
        _submission(project_id, "live v2 — changed."), store=store, bodies=bodies
    )

    story = reconstruct_intake_provenance(
        changed.artifact["artifact_id"], store, bodies
    )
    assert story["artifact_chain"] == [
        changed.artifact["artifact_id"],
        first.artifact["artifact_id"],
    ]
    assert story["origin"]["who"] == "user-replay"
    assert story["integrity_clearance"]["evidence_chain"]["intact"] is True

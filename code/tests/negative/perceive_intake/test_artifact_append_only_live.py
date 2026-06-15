"""B3.1/B3.6 LIVE — the artifact anchor is append-only AT THE DATABASE.

Mirrors the DTM-0002 enforcement suite for the new ``artifact`` table
(migration 20260612100000): UPDATE/DELETE blow up (REVOKE + trigger,
belt-and-braces) and the dedup_key UNIQUE constraint refuses double admission.
Skips unless the local Supabase stack is configured (existing pattern).
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

pytestmark = pytest.mark.skipif(
    create_client is None or not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL and "
        "SUPABASE_SERVICE_ROLE_KEY from `supabase status` (this live suite "
        "runs locally only)"
    ),
)


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def _seed_artifact(client) -> dict:
    row = {
        "project_id": str(uuid.uuid4()),
        "body_ref": "artifacts/test/deadbeef.txt",
        "normalized_form": {"version": "wa001-n1", "text": "x.", "sections": []},
        "provenance": {"who": "user-test", "when": "now", "source": "src"},
        "dedup_key": uuid.uuid4().hex,
        "submitted_by": "user-test",
        "created_by": "user-test",
        "provenance_ref": {"submission": {}},
    }
    resp = client.table("artifact").insert(row).execute()
    return resp.data[0]


def test_update_on_artifact_is_rejected_by_the_database(client) -> None:
    seeded = _seed_artifact(client)
    with pytest.raises(Exception) as excinfo:
        (
            client.table("artifact")
            .update({"submitted_by": "tampered"})
            .eq("artifact_id", seeded["artifact_id"])
            .execute()
        )
    assert "append-only" in str(excinfo.value) or "permission" in str(excinfo.value)


def test_delete_on_artifact_is_rejected_by_the_database(client) -> None:
    seeded = _seed_artifact(client)
    with pytest.raises(Exception) as excinfo:
        (
            client.table("artifact")
            .delete()
            .eq("artifact_id", seeded["artifact_id"])
            .execute()
        )
    assert "append-only" in str(excinfo.value) or "permission" in str(excinfo.value)


def test_duplicate_dedup_key_is_rejected_by_the_database(client) -> None:
    """Non-idempotent admission impossible at the store: UNIQUE(dedup_key)."""
    seeded = _seed_artifact(client)
    duplicate = {
        "project_id": seeded["project_id"],
        "body_ref": seeded["body_ref"],
        "normalized_form": seeded["normalized_form"],
        "provenance": seeded["provenance"],
        "dedup_key": seeded["dedup_key"],  # same key — must refuse
        "submitted_by": "user-test",
        "created_by": "user-test",
        "provenance_ref": {"submission": {}},
    }
    with pytest.raises(Exception) as excinfo:
        client.table("artifact").insert(duplicate).execute()
    assert "duplicate" in str(excinfo.value).lower() or "unique" in str(excinfo.value).lower()


def test_promotion_candidate_remains_mutable(client) -> None:
    """Contrast: the candidate is transient-but-audited — readiness moves."""
    seeded = _seed_artifact(client)
    inserted = (
        client.table("promotion_candidate")
        .insert(
            {
                "artifact_ref": seeded["artifact_id"],
                "normalized_form": seeded["normalized_form"],
                "readiness_state": "pending",
                "project_id": seeded["project_id"],
            }
        )
        .execute()
    )
    candidate_id = inserted.data[0]["candidate_id"]
    updated = (
        client.table("promotion_candidate")
        .update({"readiness_state": "ready"})
        .eq("candidate_id", candidate_id)
        .execute()
    )
    assert updated.data[0]["readiness_state"] == "ready"

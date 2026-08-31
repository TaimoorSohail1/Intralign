"""QA-WA-001 B2 — LIVE end-to-end intake against the local Supabase stack.

Skips unless the environment is configured (existing pattern):

    cd code && supabase start          # then read values from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key>
    export SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54332/postgres

Proves the real bindings: body in the Storage bucket ``artifacts`` (DL-054),
artifact + candidate rows in Postgres, idempotent re-intake without a second
Storage object, the changed-re-submission chain, and (integration) that the
CONSTRUCTED TriggerClaim is accepted by ``runner.submit_trigger``.
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.responsibilities.perceive.intake import IntakeSubmission, submit_artifact
from backend.services.observability.events import CollectingEventEmitter

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

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


@pytest.fixture(scope="module")
def store(client):
    from backend.services.persistence.intake_store import SupabaseIntakeStore

    return SupabaseIntakeStore(client)


@pytest.fixture(scope="module")
def bodies(client):
    from backend.services.persistence.storage import ArtifactBodyStore

    return ArtifactBodyStore(client)


def _submission(project_id: str, content: str) -> IntakeSubmission:
    return IntakeSubmission(
        project_id=project_id,
        source="evidence-source-live",
        submitted_by="user-live",
        content=content,
    )


def test_live_intake_preserves_body_in_storage_and_rows_in_postgres(
    client, store, bodies
) -> None:
    project_id = str(uuid.uuid4())
    content = "# Live plan\n\n- The launch must happen in Q4.\n"
    emitter = CollectingEventEmitter()

    result = submit_artifact(
        _submission(project_id, content), store=store, bodies=bodies, emitter=emitter
    )

    # B2.1: artifact row really in Postgres, fully attributed.
    row = store.get_artifact(result.artifact["artifact_id"])
    assert row is not None
    assert row["provenance"]["who"] == "user-live"
    assert row["epistemic_state"] == "attested-evidence"
    # DL-054: the body object really exists in the Storage bucket.
    object_names = bodies.list_bodies(project_id)
    assert object_names, "no Storage object found under the project prefix"
    assert result.body_ref.split("/")[-1] in object_names
    assert bodies.download_body(result.body_ref).decode() == content
    # B2.3: candidate row present and ready, clearance recorded.
    candidate = store.candidate_for_artifact(result.artifact["artifact_id"])
    assert candidate is not None
    assert candidate["readiness_state"] == "ready"
    assert candidate["integrity_clearance"]["evidence_chain"]["intact"] is True
    assert emitter.names[-1] == "promotion_candidate_ready"


def test_live_idempotent_reintake_no_second_storage_object(store, bodies) -> None:
    project_id = str(uuid.uuid4())
    content = "Idempotency body. The check must hold.\n"

    first = submit_artifact(_submission(project_id, content), store=store, bodies=bodies)
    objects_after_first = bodies.list_bodies(project_id)
    again = submit_artifact(_submission(project_id, content), store=store, bodies=bodies)

    assert again.created is False
    assert again.artifact["artifact_id"] == first.artifact["artifact_id"]
    # No second Storage object appeared (B2.4).
    assert bodies.list_bodies(project_id) == objects_after_first
    assert len(objects_after_first) == 1


def test_live_changed_resubmission_chains_and_signals(store, bodies) -> None:
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    first = submit_artifact(
        _submission(project_id, "v1 content."), store=store, bodies=bodies
    )
    changed = submit_artifact(
        _submission(project_id, "v2 content — it moved."),
        store=store,
        bodies=bodies,
        emitter=emitter,
    )

    assert changed.artifact["version"] == 2
    assert changed.artifact["supersedes_id"] == first.artifact["artifact_id"]
    assert "artifact_modified" in emitter.names
    assert changed.modified_trigger is not None


@pytest.mark.skipif(
    not SUPABASE_DB_URL,
    reason="SUPABASE_DB_URL required for the durable-run integration leg",
)
def test_live_constructed_trigger_is_accepted_by_the_00r_backbone(
    store, bodies
) -> None:
    """Integration: the claim intake CONSTRUCTS is valid 00R input (decision #8)."""
    from backend.orchestration import runner

    runner.reset_coalescing_guard()
    project_id = str(uuid.uuid4())
    submit_artifact(_submission(project_id, "before."), store=store, bodies=bodies)
    changed = submit_artifact(
        _submission(project_id, "after — changed."), store=store, bodies=bodies
    )
    claim = changed.modified_trigger
    assert claim is not None

    outcome = runner.submit_trigger("deep_pass", claim)
    assert outcome.status == "completed"
    assert outcome.state is not None
    assert outcome.state.trigger["trigger_type"] == "knowledge-change"
    runner.reset_coalescing_guard()

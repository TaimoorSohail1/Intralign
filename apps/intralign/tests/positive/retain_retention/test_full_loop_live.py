"""The full Wave A loop, LIVE (DTM-0008 done-criterion; IC-WA-001 + IC-WA-002 + IC-WA-00R).

One test, one story, real backing services:

    perceive.submit_artifact            (IC-WA-001: preserved, normalized, cleared)
      -> Promotion Candidate ready
      -> extraction drafts              (DL-047 EI-02, deterministic)
      -> retain.admit_candidate         (IC-WA-002: integrity-gated admission)
      -> knowledge_promoted emitted
      -> the CONSTRUCTED promotion TriggerClaim submitted via
         runner.submit_trigger          (IC-WA-00R: ONLY orchestration runs it)
      -> durable Deep Pass completes
      -> CognitionHistoryRecord appended (recompute receipt in the live DB)

Skips unless the local Supabase stack is configured (existing pattern).

The emission spec on the submitted claim follows the locked Wave A pattern
(DTM-0005/0006 backbone suites): with Infer/Evaluate placeholders, the
recompute's emissions are declared on the trigger payload and appended by the
REAL retain stage; its upstream lineage references the freshly admitted
assertions, closing the loop intake -> admission -> recompute -> receipt.
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.responsibilities.perceive.extraction import RuleBasedExtractor
from backend.responsibilities.perceive.intake import IntakeSubmission, submit_artifact
from backend.responsibilities.retain.admission import admit_candidate
from backend.services.observability.events import CollectingEventEmitter

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

pytestmark = pytest.mark.skipif(
    create_client is None
    or not SUPABASE_URL
    or not SUPABASE_SERVICE_ROLE_KEY
    or not SUPABASE_DB_URL,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL, "
        "SUPABASE_SERVICE_ROLE_KEY and SUPABASE_DB_URL (from `supabase "
        "status`); the Wave A loop runs live only"
    ),
)


def test_wave_a_full_loop_intake_to_admission_to_recompute_receipt() -> None:
    from backend.orchestration import runner
    from backend.responsibilities.retain.repository import ChrRepository
    from backend.services.persistence.intake_store import SupabaseIntakeStore
    from backend.services.persistence.retention_store import SupabaseRetentionStore
    from backend.services.persistence.storage import ArtifactBodyStore

    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    runner.reset_coalescing_guard()
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    # 1. Intake (IC-WA-001): preserve, normalize, clear.
    intake_result = submit_artifact(
        IntakeSubmission(
            project_id=project_id,
            source="evidence-source-wave-a",
            submitted_by="user-wave-a",
            content=(
                "# Launch plan\n\n"
                "- The launch must happen in Q4.\n"
                "- The rollout depends on the auth service.\n"
            ),
        ),
        store=SupabaseIntakeStore(client),
        bodies=ArtifactBodyStore(client),
        emitter=emitter,
    )
    assert intake_result.readiness_state == "ready"
    assert "promotion_candidate_ready" in emitter.names
    candidate = intake_result.candidate

    # 2. Extraction (DL-047 EI-02): deterministic drafts from the candidate.
    drafts = RuleBasedExtractor().extract(
        artifact_id=str(intake_result.artifact["artifact_id"]),
        normalized_form=intake_result.normalized_form,
        attesting_source="evidence-source-wave-a",
    )
    assert {d.content_type for d in drafts} == {"constraint", "dependency"}

    # 3. Admission (IC-WA-002): integrity-gated; knowledge promoted.
    retention_store = SupabaseRetentionStore(client)
    admitted = admit_candidate(
        candidate, drafts, store=retention_store, emitter=emitter
    )
    assert len(admitted.assertion_ids) == 2
    assert "knowledge_promoted" in emitter.names
    assert "knowledge_mutation_recorded" in emitter.names
    # The admitted rows are really in the live canonical store, v1, cleared.
    for assertion_id in admitted.assertion_ids:
        row = retention_store.get_assertion(assertion_id)
        assert row is not None and row["version"] == 1
        assert row["provenance_ref"]["integrity_clearance"]

    # 4. The CONSTRUCTED promotion trigger is submitted by ORCHESTRATION
    #    (Retain handed it back; only this test submits it — A3.10).
    claim = admitted.promotion_trigger.model_copy(
        update={
            "emissions": [
                {
                    "output_kind": "finding",
                    "output_payload": {"summary": "wave-a loop recompute emission"},
                    "input_attestation_version": "v1",
                    "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
                    "upstream_lineage": {"assertion_ids": admitted.assertion_ids},
                    "provenance_ref": {"emitted_by": "dtm-0008-wave-a-loop"},
                }
            ]
        }
    )
    chr_repo = ChrRepository(client=client)
    outcome = runner.submit_trigger(
        "deep_pass", claim, emitter=emitter, chr_repo=chr_repo
    )

    # 5. Durable Deep Pass completed off the promotion trigger.
    assert outcome.status == "completed"
    assert outcome.state is not None
    assert outcome.state.trigger["trigger_type"] == "promotion"
    assert outcome.state.cognition_state == "current"
    assert "recompute_completed" in emitter.names

    # 6. The recompute receipt (CHR) was APPENDED to the live canonical store,
    #    its lineage pointing back at the admitted knowledge.
    assert len(outcome.state.appended_chr_ids) == 1
    chr_id = outcome.state.appended_chr_ids[0]
    assert "cognition_history_record_appended" in emitter.names
    receipt = chr_repo.get(uuid.UUID(chr_id))
    assert receipt is not None
    assert receipt.recompute_trigger == "promotion"
    assert receipt.upstream_lineage == {"assertion_ids": admitted.assertion_ids}
    runner.reset_coalescing_guard()

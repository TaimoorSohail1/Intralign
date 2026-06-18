"""QA-WU-ACCEPT U2 — the Acceptance-Impact reconcile, LIVE end-to-end (DTM-0017).

One live story over the real backing services:

    a user ACCEPTS an item (record_acceptance → UAR + user-attested plan fact,
    pinned to the accepted value's CHR)
      → the underlying knowledge MOVES (a recompute appends a newer value CHR for
        the same accepted item, ≥10 pts / band change)
      → reconcile_acceptance_impact scans the project's active UARs
      → an acceptance_impact CHR appears for the accepted item, referencing the
        pinned vs the latest CHR; the UAR + plan-fact rows are BYTE-INTACT.

Env-gated (Wave A/B/C pattern): skips OFFLINE unless the local Supabase stack is
configured. The reconcile is a RULE comparison (no LLM / no provider call,
ADR-0004), so it is deterministic even live.
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
        "SUPABASE_SERVICE_ROLE_KEY (from `supabase status`); this live suite "
        "runs locally only"
    ),
)


def _seed_value_chr(repo, *, project_id, index, band):
    """Append a real outcome_confidence value CHR (the accepted item's value)."""
    from backend.responsibilities.retain import CognitionHistoryRecord

    record = CognitionHistoryRecord(
        project_id=project_id,
        output_kind="outcome_confidence",
        output_payload={"index": index, "band": band},
        input_attestation_version="v1",
        model_or_rule_version={"provider": "rule", "model_version": "caf-v0"},
        upstream_lineage={},
        recompute_trigger="knowledge-change",
        provenance_ref={"emitted_by": "evaluate"},
    )
    return repo.append(record)


def test_accept_then_drift_then_reconcile_emits_impact_and_leaves_uar_intact() -> None:
    from backend.orchestration.wave_u import reconcile_acceptance_impact
    from backend.responsibilities.perceive.acceptance_capture import capture_acceptance
    from backend.responsibilities.retain.acceptance import record_acceptance
    from backend.responsibilities.retain.repository import ChrRepository
    from backend.services.observability.events import CollectingEventEmitter
    from backend.services.persistence.retention_store import SupabaseRetentionStore

    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    repo = ChrRepository(client=client)
    store = SupabaseRetentionStore(client)

    project_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # --- the accepted value lands as a real CHR; the user accepts it ---------
    pinned = _seed_value_chr(repo, project_id=project_id, index=82.0, band="high")
    capture = capture_acceptance(
        {
            "user_id": user_id,
            "target_kind": "outcome_confidence",
            "version_pin": str(pinned.chr_id),
            "action": "accept",
            "project_id": project_id,
        },
        emitter=CollectingEventEmitter(),
    )

    class _PinReader:
        def get(self, chr_id):
            row = repo.get(chr_id)
            return {"output_payload": {"summary": "Confirmed outcome value."}} if row else None

    accept = record_acceptance(
        capture,
        project_id=project_id,
        store=store,
        emitter=CollectingEventEmitter(),
        chr_reader=_PinReader(),
    )
    uar_before = store.get_acceptance(accept.uar_id)
    plan_fact_before = store.get_assertion(accept.plan_fact_id)
    assert uar_before is not None and plan_fact_before is not None

    # --- the understanding MOVES: a recompute appends a newer value CHR ------
    latest = _seed_value_chr(repo, project_id=project_id, index=60.0, band="medium")

    # --- the reconcile surfaces the Acceptance-Impact Assessment ------------
    emitter = CollectingEventEmitter()
    raised = reconcile_acceptance_impact(
        project_id=project_id,
        store=store,
        chr_repo=repo,
        emitter=emitter,
        recompute_trigger="reanalysis",
    )

    assert len(raised) == 1
    assessment = raised[0]
    assert assessment.uar_ref == accept.uar_id
    assert assessment.pinned_chr == str(pinned.chr_id)
    assert assessment.latest_chr == str(latest.chr_id)
    assert assessment.band_changed is True
    assert "acceptance_impact_assessed" in emitter.names

    # The acceptance_impact CHR really landed in the live DB.
    impact = (
        client.table("cognition_history_record")
        .select("*")
        .eq("project_id", project_id)
        .eq("output_kind", "acceptance_impact")
        .execute()
    )
    assert len(impact.data) == 1
    assert impact.data[0]["upstream_lineage"]["uar_id"] == accept.uar_id
    assert impact.data[0]["epistemic_state"] == "attested-oslo"  # the CHR receipt

    # The UAR + plan-fact rows are BYTE-INTACT (read-only over both).
    assert store.get_acceptance(accept.uar_id) == uar_before
    assert store.get_assertion(accept.plan_fact_id) == plan_fact_before

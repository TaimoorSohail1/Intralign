"""DTM-0002 positive persistence suite — canonical inserts + derived updates.

Runs LIVE against the local Supabase stack only (Phase I CI has no Supabase, so
these tests SKIP unless the environment is configured). To run locally:

    cd code && supabase start          # then read keys from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key from `supabase status`>

Covers (task DTM-0002 / LDM v1):
- INSERT succeeds into each canonical append-only table (LDM §2.1/2.2/2.4/2.5),
  including a Plan Fact (attested_assertion row with attesting_source = 'user',
  LDM §2.4).
- Supersession chain: CHR A, then CHR B with supersedes_chr_id = A (LDM §5.1:
  change = new appended row).
- Derived projection tables (schema `derived`, LDM §3.1) accept INSERT and
  UPDATE — they are non-canonical, recomputable current-views.

Uses supabase-py (already a project dependency; psycopg is NOT transitively
available, so PostgREST via supabase-py is the test transport).
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # Phase I CI venv has no supabase-py installed
    create_client = None  # type: ignore[assignment]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

pytestmark = pytest.mark.skipif(
    create_client is None or not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL and "
        "SUPABASE_SERVICE_ROLE_KEY from `supabase status` (Phase I CI has no "
        "Supabase; this suite runs locally only)"
    ),
)

# One synthetic project scope per test run (no projects table yet in Phase I).
PROJECT_ID = str(uuid.uuid4())


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def _insert_chr(client, **overrides) -> dict:
    """Append one cognition_history_record (LDM §2.2) and return the row."""
    row = {
        "output_kind": "finding",
        "output_payload": {"summary": "test finding"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": [],
        "recompute_trigger": "promotion",
        "project_id": PROJECT_ID,
        "provenance_ref": {"emitted_by": "test-suite"},
    }
    row.update(overrides)
    resp = client.table("cognition_history_record").insert(row).execute()
    assert len(resp.data) == 1
    return resp.data[0]


def test_insert_attested_assertion_evidence(client) -> None:
    """LDM §2.1 — evidence-attested assertion row appends."""
    resp = (
        client.table("attested_assertion")
        .insert(
            {
                "content_type": "fact",
                "proposition": "The project deadline is 2026-09-01.",
                "attesting_source": "evidence-source-test",
                "source_ref": {"artifact": "artifact-1", "locus": "p.3"},
                "project_id": PROJECT_ID,
                "created_by": "source-system",
                "epistemic_state": "attested-evidence",
                "provenance_ref": {"artifact": "artifact-1"},
            }
        )
        .execute()
    )
    assert len(resp.data) == 1
    row = resp.data[0]
    assert row["assertion_id"]
    assert row["re_derivable"] is True  # default
    assert row["version"] == 1  # default


def test_insert_plan_fact_user_attested(client) -> None:
    """LDM §2.4 — Plan Fact = attested_assertion with attesting_source = user."""
    resp = (
        client.table("attested_assertion")
        .insert(
            {
                "content_type": "goal",
                "proposition": "Adopt recommendation R-1 as confirmed plan content.",
                "attesting_source": "user",
                "source_ref": {"acceptance_ref": str(uuid.uuid4())},
                "project_id": PROJECT_ID,
                "created_by": "user",
                "epistemic_state": "attested-user",
                "provenance_ref": {"uar": "test"},
            }
        )
        .execute()
    )
    assert resp.data[0]["attesting_source"] == "user"
    assert resp.data[0]["epistemic_state"] == "attested-user"


def test_chr_supersedes_chain(client) -> None:
    """LDM §2.2/§5.1 — recompute appends CHR B with supersedes_chr_id = CHR A."""
    chr_a = _insert_chr(client)
    chr_b = _insert_chr(
        client,
        recompute_trigger="knowledge-change",
        supersedes_chr_id=chr_a["chr_id"],
        upstream_lineage=[chr_a["chr_id"]],
    )
    assert chr_b["supersedes_chr_id"] == chr_a["chr_id"]
    assert chr_b["chr_id"] != chr_a["chr_id"]  # appended, not overwritten
    assert chr_b["epistemic_state"] == "attested-oslo"  # §2.2 default


def test_insert_user_acceptance_record(client) -> None:
    """LDM §2.4 — UAR appends, version-pinned to the exact CHR confirmed."""
    pinned = _insert_chr(client, output_kind="recommendation")
    resp = (
        client.table("user_acceptance_record")
        .insert(
            {
                "user_id": str(uuid.uuid4()),
                "action": "accept",
                "target_kind": "recommendation",
                "version_pin": pinned["chr_id"],
                "rationale": "Looks right.",
                "project_id": PROJECT_ID,
                "created_by": "user",
                "provenance_ref": {"pinned_chr": pinned["chr_id"]},
            }
        )
        .execute()
    )
    row = resp.data[0]
    assert row["uar_id"]
    assert row["version_pin"] == pinned["chr_id"]
    assert row["epistemic_state"] == "attested-user"  # §2.4 default


def test_insert_history_record(client) -> None:
    """LDM §2.5 — generic append-only audit entry."""
    resp = (
        client.table("history_record")
        .insert(
            {
                "event_type": "emission-appended",
                "subject_ref": {"kind": "chr", "id": str(uuid.uuid4())},
                "actor": "OSLO",
                "project_id": PROJECT_ID,
                "created_by": "OSLO",
                "epistemic_state": "attested-oslo",
                "provenance_ref": {"event": "test"},
            }
        )
        .execute()
    )
    row = resp.data[0]
    assert row["history_id"]
    assert row["at"]  # LDM §2.5 `at` timestamp populated by default


def test_derived_projection_insert_and_update(client) -> None:
    """LDM §3.1 — derived current-view rows are non-canonical and UPDATABLE."""
    chr_row = _insert_chr(client)
    derived = client.schema("derived")

    inserted = (
        derived.table("finding_current")
        .insert(
            {
                "project_id": PROJECT_ID,
                "current_payload": {"summary": "v1"},
                "current_chr_ref": chr_row["chr_id"],
                "confidence_value": 80,
                "confidence_band": "high",
            }
        )
        .execute()
    )
    projection_id = inserted.data[0]["projection_id"]
    assert inserted.data[0]["epistemic_label"] == "derived"  # §3.1 fixed label
    assert inserted.data[0]["conflict_state"] == "none"

    # Recompute replaces the live projection in place (history grows in CHR).
    new_chr = _insert_chr(client, recompute_trigger="reanalysis")
    updated = (
        derived.table("finding_current")
        .update(
            {
                "current_payload": {"summary": "v2"},
                "current_chr_ref": new_chr["chr_id"],
                "confidence_value": 60,
                "confidence_band": "medium",
            }
        )
        .eq("projection_id", projection_id)
        .execute()
    )
    assert len(updated.data) == 1
    assert updated.data[0]["current_payload"] == {"summary": "v2"}
    assert updated.data[0]["current_chr_ref"] == new_chr["chr_id"]

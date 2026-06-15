"""DTM-0004 positive retain suite — append-only CHR repository (IC-WA-00R A3.5; QA-WA-00R B2.2).

Runs LIVE against the local Supabase stack only (Phase I CI has no Supabase, so
these tests SKIP unless the environment is configured). To run locally:

    cd code && supabase start          # then read keys from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key from `supabase status`>

Covers (task DTM-0004 / LDM §2.2 / IC-WA-00R A3.5, A4.2):
- ``append`` persists a new ``cognition_history_record`` row and returns the
  record with server-assigned fields populated; the row is really in the DB.
- ``get`` round-trips an appended record by ``chr_id``.
- ``latest_for_output`` returns the most recent (``emitted_at``) record for a
  (project, output_kind) pair.
- ``lineage_chain`` walks the ``supersedes_chr_id`` ancestry A <- B <- C.
- Supersession is a NEW appended row pinning ``supersedes_chr_id`` — the
  superseded record stays intact (B2.2: prior records intact).
"""

from __future__ import annotations

import os
import uuid
from datetime import UTC, datetime, timedelta

import pytest

try:
    from supabase import create_client
except ImportError:  # Phase I CI venv has no supabase-py installed
    create_client = None  # type: ignore[assignment]

from backend.responsibilities.retain import ChrRepository, CognitionHistoryRecord
from shared.epistemic import EpistemicState

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


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@pytest.fixture(scope="module")
def repo(client) -> ChrRepository:
    return ChrRepository(client=client)


def _make_record(**overrides) -> CognitionHistoryRecord:
    """Build a valid CHR (LDM §2.2 fields) scoped to a fresh project by default."""
    fields: dict = {
        "output_kind": "finding",
        "output_payload": {"summary": "test finding"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": [], "assertion_ids": []},
        "recompute_trigger": "promotion",
        "project_id": uuid.uuid4(),
        "provenance_ref": {"emitted_by": "test-suite"},
    }
    fields.update(overrides)
    return CognitionHistoryRecord(**fields)


def test_append_returns_persisted_chr(repo, client) -> None:
    """B2.2 — append persists the receipt; server-assigned fields are populated."""
    record = _make_record()
    persisted = repo.append(record)

    assert isinstance(persisted, CognitionHistoryRecord)
    assert persisted.chr_id == record.chr_id
    assert persisted.emitted_at is not None  # server default now()
    assert persisted.created_at is not None  # universal field, server default
    assert persisted.epistemic_state is EpistemicState.ATTESTED_OSLO
    assert persisted.created_by == "OSLO"
    assert persisted.version == 1

    # The row is really in the DB (independent read, not the repo's word for it).
    resp = (
        client.table("cognition_history_record")
        .select("*")
        .eq("chr_id", str(record.chr_id))
        .execute()
    )
    assert len(resp.data) == 1
    assert resp.data[0]["output_payload"] == {"summary": "test finding"}
    assert resp.data[0]["epistemic_state"] == "attested-oslo"


def test_get_round_trips_appended_record(repo) -> None:
    """get(chr_id) returns the appended record with identical content."""
    record = _make_record(
        output_kind="recommendation",
        output_payload={"text": "do the thing"},
        model_or_rule_version={
            "provider": "openai",
            "model": "gpt-test",
            "langsmith_run_id": str(uuid.uuid4()),
        },
    )
    repo.append(record)

    fetched = repo.get(record.chr_id)
    assert fetched is not None
    assert fetched.chr_id == record.chr_id
    assert fetched.output_kind == "recommendation"
    assert fetched.output_payload == {"text": "do the thing"}
    assert fetched.model_or_rule_version == record.model_or_rule_version
    assert fetched.project_id == record.project_id
    assert fetched.input_attestation_version == "v1"


def test_get_unknown_id_returns_none(repo) -> None:
    assert repo.get(uuid.uuid4()) is None


def test_latest_for_output_picks_most_recent(repo) -> None:
    """latest_for_output returns the newest emitted_at for (project, output_kind)."""
    project_id = uuid.uuid4()
    older = datetime(2026, 6, 12, 10, 0, 0, tzinfo=UTC)
    newer = older + timedelta(minutes=5)

    repo.append(_make_record(project_id=project_id, emitted_at=older))
    second = _make_record(
        project_id=project_id, emitted_at=newer, recompute_trigger="reanalysis"
    )
    repo.append(second)

    latest = repo.latest_for_output(project_id, "finding")
    assert latest is not None
    assert latest.chr_id == second.chr_id
    assert latest.emitted_at == newer

    # Different output_kind in the same project -> nothing yet.
    assert repo.latest_for_output(project_id, "risk") is None


def test_supersession_is_a_new_appended_row(repo) -> None:
    """A4.2 — supersession appends a NEW row; the superseded record stays intact."""
    project_id = uuid.uuid4()
    original = repo.append(_make_record(project_id=project_id))
    superseding = repo.append(
        _make_record(
            project_id=project_id,
            recompute_trigger="knowledge-change",
            supersedes_chr_id=original.chr_id,
            upstream_lineage={"chr_ids": [str(original.chr_id)]},
        )
    )

    assert superseding.chr_id != original.chr_id  # appended, not overwritten
    assert superseding.supersedes_chr_id == original.chr_id

    untouched = repo.get(original.chr_id)
    assert untouched is not None
    assert untouched.output_payload == original.output_payload
    assert untouched.supersedes_chr_id is None


def test_lineage_chain_walks_supersession_ancestry(repo) -> None:
    """lineage_chain(C) walks A <- B <- C, most recent first."""
    project_id = uuid.uuid4()
    chr_a = repo.append(_make_record(project_id=project_id))
    chr_b = repo.append(
        _make_record(
            project_id=project_id,
            recompute_trigger="clarification",
            supersedes_chr_id=chr_a.chr_id,
        )
    )
    chr_c = repo.append(
        _make_record(
            project_id=project_id,
            recompute_trigger="user-action",
            supersedes_chr_id=chr_b.chr_id,
        )
    )

    chain = repo.lineage_chain(chr_c.chr_id)
    assert [r.chr_id for r in chain] == [chr_c.chr_id, chr_b.chr_id, chr_a.chr_id]

    # A root record's chain is just itself.
    assert [r.chr_id for r in repo.lineage_chain(chr_a.chr_id)] == [chr_a.chr_id]

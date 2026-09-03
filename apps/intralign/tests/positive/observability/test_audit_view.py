"""DTM-0006 positive — C3 audit assembly for a REAL recompute run (live).

audit_view(events, repo) must assemble every C3 field: trigger source,
inputs/versions consumed (input_attestation_version + model_or_rule_version
incl. provider/model and the optional langsmith_run_id), emissions produced
(-> which CHRs appended), and outcome — plus the auditable append-not-overwrite
property (supersession priors intact).

Live: needs the local Supabase stack (skip contract identical to DTM-0005).
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.orchestration import runner
from backend.responsibilities.retain import ChrRepository
from backend.services.observability.audit import audit_view
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
        "SUPABASE_SERVICE_ROLE_KEY and SUPABASE_DB_URL (DB URL from "
        "`supabase status`); this live suite runs locally only"
    ),
)


@pytest.fixture(scope="module")
def repo() -> ChrRepository:
    return ChrRepository(client=create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY))


@pytest.fixture(scope="module")
def checkpointer():
    from backend.orchestration.checkpointer import build_checkpointer

    return build_checkpointer()


@pytest.fixture(autouse=True)
def _fresh_guard():
    runner.reset_coalescing_guard()
    yield
    runner.reset_coalescing_guard()


def _emission(**overrides) -> dict:
    fields: dict = {
        "output_kind": "finding",
        "output_payload": {"summary": "audit emission"},
        "input_attestation_version": "attested-v7",
        "model_or_rule_version": {"provider": "openai", "model": "gpt-x"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0006-tests"},
    }
    fields.update(overrides)
    return fields


def test_audit_record_contains_all_c3_fields_for_a_real_run(
    repo, checkpointer, monkeypatch
) -> None:
    monkeypatch.setenv("LANGSMITH_TRACING", "true")  # DL-054 cond.1 linkage on
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    outcome = runner.submit_trigger(
        "deep_pass",
        {
            "trigger_type": "knowledge-change",
            "project_id": project_id,
            "information_changed": True,
            "source": "dtm-0006-audit-test",
            "emissions": [
                _emission(),
                _emission(output_kind="risk", output_payload={"summary": "risk"}),
            ],
        },
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert outcome.status == "completed"
    run_id = outcome.state.run_id

    record = audit_view(emitter.events, repo)

    # C3: trigger source.
    assert record.trigger_type == "knowledge-change"
    assert record.trigger_source == "dtm-0006-audit-test"
    assert record.project_id == project_id
    assert record.run_id == run_id

    # C3: emissions produced -> which history records appended.
    assert record.appended_chr_ids == outcome.state.appended_chr_ids
    assert [e.output_kind for e in record.emissions] == ["finding", "risk"]
    assert [e.chr_id for e in record.emissions] == record.appended_chr_ids

    # C3: inputs/versions consumed — Attested set + full model/rule identity.
    for entry in record.emissions:
        assert entry.input_attestation_version == "attested-v7"
        assert entry.model_or_rule_version["provider"] == "openai"
        assert entry.model_or_rule_version["model"] == "gpt-x"
        assert entry.model_or_rule_version["langsmith_run_id"] == run_id

    # C3: outcome + the full state-transition trail of THIS run.
    assert record.outcome == "completed"
    assert record.failure is None
    assert record.state_transitions == [
        ("current", "stale"),
        ("stale", "reanalyzing"),
        ("reanalyzing", "current"),
    ]


def test_failed_run_audit_carries_failure_outcome(repo, checkpointer) -> None:
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()
    outcome = runner.submit_trigger(
        "deep_pass",
        {
            "trigger_type": "reanalysis",
            "project_id": project_id,
            "information_changed": True,
            "source": "dtm-0006-audit-test",
            "emissions": [_emission(output_kind="not-a-kind")],
        },
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert outcome.status == "failed"

    record = audit_view(emitter.events, repo)
    assert record.outcome == "failed"
    assert record.failure is not None and record.failure["stage"] == "retain"
    assert record.appended_chr_ids == []  # no emission claimed by a failed run
    assert record.state_transitions[-1] == ("reanalyzing", "failed")

"""DTM-0005 positive orchestration suite — deep_pass backbone end-to-end (QA-WA-00R B2).

LIVE tests: run against the local Supabase stack (CHR appends via DTM-0004 repo,
durable checkpoints via SUPABASE_DB_URL). Skips unless the environment is set:

    cd code && supabase start          # then read values from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key>
    export SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54332/postgres

Covers: B2.1 (each valid trigger -> full state cycle with A6 events in order),
B2.2 (one NEW CHR per emission, priors intact), B2.3 (all transitions emitted),
B2.4 (failure -> Failed, last-known-good retained, CHR count unchanged).
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
from backend.orchestration.checkpointer import build_checkpointer
from backend.orchestration.state import GraphState
from backend.responsibilities.retain import ChrRepository
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

_ALL_FIVE = ["promotion", "knowledge-change", "clarification", "user-action", "reanalysis"]


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@pytest.fixture(scope="module")
def repo(client) -> ChrRepository:
    return ChrRepository(client=client)


@pytest.fixture(scope="module")
def checkpointer():
    return build_checkpointer()


@pytest.fixture(autouse=True)
def _fresh_guard():
    runner.reset_coalescing_guard()
    yield
    runner.reset_coalescing_guard()


def _emission(**overrides) -> dict:
    fields: dict = {
        "output_kind": "finding",
        "output_payload": {"summary": "backbone test emission"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0005-tests"},
    }
    fields.update(overrides)
    return fields


def _trigger(project_id: str, trigger_type: str, emissions: list[dict]) -> dict:
    return {
        "trigger_type": trigger_type,
        "project_id": project_id,
        "information_changed": True,
        "source": "dtm-0005-tests",
        "emissions": emissions,
    }


def _chr_count(client, project_id: str) -> int:
    resp = (
        client.table("cognition_history_record")
        .select("chr_id")
        .eq("project_id", project_id)
        .execute()
    )
    return len(resp.data)


def _assert_in_order(names: list[str], expected: list[str]) -> None:
    """Assert ``expected`` appears as a subsequence of ``names``."""
    cursor = 0
    for want in expected:
        try:
            cursor = names.index(want, cursor) + 1
        except ValueError:  # pragma: no cover - assertion message path
            pytest.fail(f"event {want!r} missing/out of order in {names}")


@pytest.mark.parametrize("trigger_type", _ALL_FIVE)
def test_b2_1_valid_trigger_full_cycle(
    trigger_type: str, client, repo, checkpointer
) -> None:
    """B2.1 — each valid trigger runs the full stale->reanalyzing->current cycle."""
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, trigger_type, [_emission()]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )

    assert outcome.status == "completed"
    final = outcome.state
    assert final is not None
    assert final.cognition_state == "current"
    assert len(final.appended_chr_ids) == 1
    # Live projection replaced with the recompute result (A3.4).
    assert final.live_projection_ref is not None
    assert final.live_projection_ref["chr_ids"] == final.appended_chr_ids

    # A6 events, in contract order.
    _assert_in_order(
        emitter.names,
        [
            "stale_detected",
            "reanalysis_triggered",
            "recompute_started",
            "cognition_history_record_appended",
            "recompute_completed",
        ],
    )
    transitions = [
        (p["from_state"], p["to_state"])
        for n, p in emitter.events
        if n == "state_transition_occurred"
    ]
    assert transitions == [
        ("current", "stale"),
        ("stale", "reanalyzing"),
        ("reanalyzing", "current"),
    ]
    assert "recompute_failed" not in emitter.names
    # The CHR really landed, carrying this trigger.
    assert _chr_count(client, project_id) == 1
    persisted = repo.get(uuid.UUID(final.appended_chr_ids[0]))
    assert persisted is not None
    assert persisted.recompute_trigger == trigger_type


def test_b2_2_each_emission_appends_new_chr_priors_intact(
    client, repo, checkpointer
) -> None:
    """B2.2 — one NEW CHR per emission; prior records untouched (live DB)."""
    project_id = str(uuid.uuid4())
    # A prior receipt exists before the recompute.
    from backend.responsibilities.retain.models import CognitionHistoryRecord

    prior = repo.append(
        CognitionHistoryRecord(
            recompute_trigger="promotion",
            project_id=uuid.UUID(project_id),
            **_emission(output_payload={"summary": "prior"}),
        )
    )
    assert _chr_count(client, project_id) == 1

    emitter = CollectingEventEmitter()
    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(
            project_id,
            "knowledge-change",
            [
                _emission(supersedes_chr_id=str(prior.chr_id)),
                _emission(output_kind="risk", output_payload={"summary": "risk"}),
            ],
        ),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )

    assert outcome.status == "completed"
    assert len(outcome.state.appended_chr_ids) == 2
    assert _chr_count(client, project_id) == 3  # 1 prior + 2 appended, nothing replaced
    assert emitter.names.count("cognition_history_record_appended") == 2

    # Prior record intact — appended-not-overwritten (A3.5/A4.2).
    untouched = repo.get(prior.chr_id)
    assert untouched is not None
    assert untouched.output_payload == {"summary": "prior"}
    assert untouched.supersedes_chr_id is None


def test_b2_3_state_transitions_emitted_across_success_and_failure(
    client, repo, checkpointer
) -> None:
    """B2.3 — stale/reanalyzing/current/failed transitions all emitted as events."""
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    ok = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "promotion", [_emission()]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert ok.status == "completed"

    # Second run fails (invalid emission) starting from the now-current state.
    bad = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "reanalysis", [_emission(output_kind="not-a-kind")]),
        base_state=ok.state,
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert bad.status == "failed"

    transitions = {
        (p["from_state"], p["to_state"])
        for n, p in emitter.events
        if n == "state_transition_occurred"
    }
    assert {
        ("current", "stale"),
        ("stale", "reanalyzing"),
        ("reanalyzing", "current"),
        ("reanalyzing", "failed"),
    } <= transitions


def test_b2_4_failure_retains_last_known_good_history_uncorrupted(
    client, repo, checkpointer
) -> None:
    """B2.4 — failed run: Failed state, live ref unchanged, CHR count unchanged."""
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    # Establish a last-known-good live projection via a successful run.
    good = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "promotion", [_emission()]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert good.status == "completed"
    last_known_good = good.state.live_projection_ref
    count_before = _chr_count(client, project_id)

    failing_emitter = CollectingEventEmitter()
    bad = runner.submit_trigger(
        "deep_pass",
        _trigger(
            project_id, "knowledge-change", [_emission(output_kind="not-a-kind")]
        ),
        base_state=good.state,
        checkpointer=checkpointer,
        emitter=failing_emitter,
        chr_repo=repo,
    )

    assert bad.status == "failed"
    assert bad.state.cognition_state == "failed"
    assert bad.state.failure is not None
    # A3.7 — the live Derived projection reference is NOT replaced.
    assert bad.state.live_projection_ref == last_known_good
    # History uncorrupted: the failed run appended nothing (live DB count).
    assert _chr_count(client, project_id) == count_before
    # Failure evented; no completion claimed.
    assert "recompute_failed" in failing_emitter.names
    assert "recompute_completed" not in failing_emitter.names
    failed_payloads = [
        p for n, p in failing_emitter.events if n == "recompute_failed"
    ]
    assert failed_payloads[0]["last_known_good_retained"] is True


def test_b2_1_run_resumes_with_same_thread_id(client, repo, checkpointer) -> None:
    """Durable resume — interrupted run continues when re-invoked, same thread_id.

    Interrupt is simulated with a compile-time breakpoint before ``stage_infer``
    (partial execution checkpointed in Postgres); re-invoking the same thread_id
    resumes from the checkpoint and completes — no emission is appended twice.
    """
    project_id = str(uuid.uuid4())
    thread_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()

    state = GraphState(
        project_id=project_id,
        run_id=thread_id,
        trigger=_trigger(project_id, "reanalysis", []),
        emissions=[_emission()],
        cognition_state="stale",
    )

    partial = runner.run(
        "deep_pass",
        state,
        thread_id=thread_id,
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
        interrupt_before=["stage_infer"],
    )
    # Partial execution: reanalyzing reached, CHR appended, run NOT completed.
    assert partial.cognition_state == "reanalyzing"
    assert len(partial.appended_chr_ids) == 1
    assert "recompute_completed" not in emitter.names

    resumed = runner.run(
        "deep_pass",
        None,  # resume: continue from the durable checkpoint
        thread_id=thread_id,
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert resumed.cognition_state == "current"
    assert resumed.appended_chr_ids == partial.appended_chr_ids
    assert "recompute_completed" in emitter.names
    # Resume did not re-append: exactly one CHR for the project.
    assert _chr_count(client, project_id) == 1

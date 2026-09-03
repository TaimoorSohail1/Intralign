from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from oslo_api.analysis.models import (
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisRunStatus,
    EvidenceFragment,
    RunKind,
)
from oslo_api.analysis.reanalysis import (
    FirstRunState,
    PendingChange,
    ReadFreshness,
    ReanalysisBatch,
)
from oslo_api.analysis.store import InMemoryAnalysisStore

PROJECT_ID = UUID("20000000-0000-0000-0000-000000000001")


def test_grounding_changes_coalesce_by_project_into_one_scoped_fast_batch() -> None:
    started_at = datetime(2026, 8, 12, 9, 0, tzinfo=UTC)
    batch = ReanalysisBatch.start(
        PendingChange(
            event_id="act-1",
            project_id=PROJECT_ID,
            change_kind="confirm",
            scope="requirements",
            occurred_at=started_at,
        )
    )

    combined = batch.add(
        PendingChange(
            event_id="act-2",
            project_id=PROJECT_ID,
            change_kind="route",
            scope="schedule",
            occurred_at=started_at + timedelta(milliseconds=400),
        )
    )

    assert combined.project_id == PROJECT_ID
    assert combined.event_ids == ("act-1", "act-2")
    assert combined.scopes == ("requirements", "schedule")
    assert combined.pass_kind == "fast"
    assert combined.trigger == "batch"


def test_batch_rejects_a_change_from_another_project() -> None:
    occurred_at = datetime(2026, 8, 12, 9, 0, tzinfo=UTC)
    batch = ReanalysisBatch.start(
        PendingChange("act-1", PROJECT_ID, "confirm", "intent", occurred_at)
    )

    with pytest.raises(ValueError, match="cannot cross project boundaries"):
        batch.add(
            PendingChange(
                "act-2",
                UUID("20000000-0000-0000-0000-000000000002"),
                "route",
                "schedule",
                occurred_at,
            )
        )


def test_read_freshness_keeps_last_good_while_a_batch_is_pending_and_running() -> None:
    state = ReadFreshness.fresh(
        project_id=PROJECT_ID,
        based_on_run_id="run-1",
    )

    stale = state.enqueue("act-1")
    running = stale.start_reanalysis("run-2")

    assert stale.state == "stale"
    assert stale.pending_event_ids == ("act-1",)
    assert stale.based_on_run_id == "run-1"
    assert running.state == "reanalyzing"
    assert running.active_run_id == "run-2"
    assert running.based_on_run_id == "run-1"


def test_changes_arriving_mid_run_remain_as_one_follow_up_batch_after_land() -> None:
    running = (
        ReadFreshness.fresh(project_id=PROJECT_ID, based_on_run_id="run-1")
        .enqueue("act-1")
        .start_reanalysis("run-2")
    )

    landed = running.enqueue("act-2").land(
        run_id="run-2",
        consumed_event_ids=("act-1",),
    )

    assert landed.state == "stale"
    assert landed.based_on_run_id == "run-2"
    assert landed.pending_event_ids == ("act-2",)
    assert landed.active_run_id is None


def test_first_run_unlock_is_latched_after_two_grounding_acts() -> None:
    state = FirstRunState(first_run=True, grounding_act_count=0, ever_unlocked=False)

    unlocked = state.record_act("confirm").record_act("route")
    withdrawn = unlocked.withdraw_act("confirm")

    assert unlocked.ever_unlocked is True
    assert unlocked.freeze_on is False
    assert withdrawn.grounding_act_count == 1
    assert withdrawn.ever_unlocked is True
    assert withdrawn.freeze_on is False


def test_queued_run_merges_a_second_change_without_creating_another_run() -> None:
    store = InMemoryAnalysisStore()
    run = store.create_run(
        AnalysisRunRequest(
            workspace_id=UUID("20000000-0000-0000-0000-000000000010"),
            project_id=PROJECT_ID,
            requested_by=UUID("20000000-0000-0000-0000-000000000011"),
            kind=RunKind.EXTENDED,
            description="A governed plan.",
            source_names=(),
        )
    )

    merged = store.merge_queued_run(
        run.id,
        evidence=(EvidenceFragment(reference="act:2", content="Route to Priya"),),
        event_ids=(UUID("20000000-0000-0000-0000-000000000022"),),
    )

    assert merged.id == run.id
    assert [item.reference for item in merged.request.user_evidence] == ["act:2"]
    assert merged.request.consolidated_event_ids == (
        UUID("20000000-0000-0000-0000-000000000022"),
    )


def test_transient_auto_retry_is_available_exactly_once_on_the_same_run() -> None:
    store = InMemoryAnalysisStore()
    run = store.create_run(
        AnalysisRunRequest(
            workspace_id=UUID("20000000-0000-0000-0000-000000000010"),
            project_id=PROJECT_ID,
            requested_by=UUID("20000000-0000-0000-0000-000000000011"),
            kind=RunKind.EXTENDED,
            description="A governed plan.",
            source_names=(),
        )
    )
    store.fail(
        run.id,
        error_code="OPENAI_TIMEOUT",
        phase=AnalysisPhase.PERCEIVE,
        retryable=True,
    )

    retried = store.queue_auto_retry(run.id)

    assert retried.id == run.id
    assert retried.status is AnalysisRunStatus.QUEUED
    assert retried.request.auto_retry_count == 1
    with pytest.raises(ValueError, match="failed"):
        store.queue_auto_retry(run.id)

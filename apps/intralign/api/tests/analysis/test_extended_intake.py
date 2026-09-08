from types import SimpleNamespace
from uuid import uuid4

import pytest

from oslo_api.analysis import AnalysisRun, AnalysisRunRequest, AnalysisRunStatus, RunKind
from oslo_api.analysis.models import EvidenceFragment
from oslo_api.analysis.service import DatabaseSliceTwoApplication
from oslo_api.slice_two import SliceTwoNotFound


class RecordingStore:
    def __init__(self, parent: AnalysisRun | None = None) -> None:
        self.parent = parent
        self.created: list[AnalysisRunRequest] = []

    def current_snapshot(self, _project_id):
        if self.parent is None:
            return None
        return SimpleNamespace(analysis_run_id=self.parent.id)

    def get_run(self, _run_id):
        return self.parent

    def create_run(self, request: AnalysisRunRequest):
        self.created.append(request)
        return AnalysisRun.queued(request)


class RecordingExecutor:
    def __init__(self) -> None:
        self.run_ids = []

    def submit(self, _function, run_id):
        self.run_ids.append(run_id)


class RecordingDurableExecutor(RecordingExecutor):
    def __init__(self) -> None:
        super().__init__()
        self.claimed: list[tuple[object, str, int]] = []
        self.completed: list[object] = []
        self.released: list[tuple[object, str, int]] = []

    def claim_run(self, run_id, *, worker_id, lease_seconds):
        self.claimed.append((run_id, worker_id, lease_seconds))
        return run_id

    def complete(self, run_id):
        self.completed.append(run_id)

    def release(self, run_id, *, error_code, delay_seconds):
        self.released.append((run_id, error_code, delay_seconds))


def build_application(store: RecordingStore) -> DatabaseSliceTwoApplication:
    application = DatabaseSliceTwoApplication(
        engine=object(),  # type: ignore[arg-type]
        store=store,  # type: ignore[arg-type]
        workflow=object(),  # type: ignore[arg-type]
        executor=RecordingExecutor(),
        document_store=object(),  # type: ignore[arg-type]
    )
    workspace_id = uuid4()
    application._workspace_for_project = lambda *_args: workspace_id  # type: ignore[method-assign]
    application._validate_documents = lambda **_kwargs: None  # type: ignore[method-assign]
    return application


def test_extended_intake_keeps_the_current_read_and_adds_new_evidence() -> None:
    workspace_id = uuid4()
    project_id = uuid4()
    actor_id = uuid4()
    original_document_id = uuid4()
    new_document_id = uuid4()
    confirmed = EvidenceFragment(reference="intent:confirmed", content="Owned outcome")
    parent_request = AnalysisRunRequest(
        workspace_id=workspace_id,
        project_id=project_id,
        requested_by=actor_id,
        kind=RunKind.INITIAL,
        description="Original plan context",
        source_names=("original.pdf",),
        source_document_ids=(original_document_id,),
        user_evidence=(confirmed,),
    )
    parent = AnalysisRun(
        id=uuid4(),
        request=parent_request,
        status=AnalysisRunStatus.COMPLETED,
    )
    store = RecordingStore(parent)
    application = build_application(store)

    application.start_analysis(
        actor_user_id=actor_id,
        project_id=project_id,
        description="New delivery evidence",
        source_names=("update.pdf",),
        source_document_ids=(new_document_id,),
        kind=RunKind.EXTENDED,
        key="existing-project-update",
    )

    request = store.created[-1]
    assert request.kind is RunKind.EXTENDED
    assert request.parent_run_id == parent.id
    assert request.description == "Original plan context\n\nNew delivery evidence"
    assert request.source_names == ("original.pdf", "update.pdf")
    assert request.source_document_ids == (original_document_id, new_document_id)
    assert request.user_evidence == (confirmed,)


def test_extended_intake_without_a_current_read_is_rejected() -> None:
    application = build_application(RecordingStore())

    with pytest.raises(SliceTwoNotFound):
        application.start_analysis(
            actor_user_id=uuid4(),
            project_id=uuid4(),
            description="Update",
            source_names=(),
            source_document_ids=(),
            kind=RunKind.EXTENDED,
            key="missing-parent-run",
        )


def test_initial_intake_can_mark_the_fast_read_for_automatic_deepening() -> None:
    store = RecordingStore()
    application = build_application(store)

    application.start_analysis(
        actor_user_id=uuid4(),
        project_id=uuid4(),
        description="Initial project evidence",
        source_names=("brief.pdf",),
        source_document_ids=(uuid4(),),
        kind=RunKind.INITIAL,
        key="initial-provisional-run",
        provisional=True,
    )

    request = store.created[-1]
    assert request.kind is RunKind.INITIAL
    assert request.provisional is True


def test_deferred_intake_queues_work_without_blocking_the_request_executor() -> None:
    store = RecordingStore()
    request_executor = RecordingExecutor()
    deferred_executor = RecordingExecutor()
    application = DatabaseSliceTwoApplication(
        engine=object(),  # type: ignore[arg-type]
        store=store,  # type: ignore[arg-type]
        workflow=object(),  # type: ignore[arg-type]
        executor=request_executor,
        deferred_executor=deferred_executor,  # type: ignore[arg-type]
        document_store=object(),  # type: ignore[arg-type]
    )
    application._workspace_for_project = lambda *_args: uuid4()  # type: ignore[method-assign]
    application._validate_documents = lambda **_kwargs: None  # type: ignore[method-assign]

    run = application.start_analysis(
        actor_user_id=uuid4(),
        project_id=uuid4(),
        description="Initial project evidence",
        source_names=("brief.pdf",),
        source_document_ids=(uuid4(),),
        kind=RunKind.INITIAL,
        key="deferred-initial-run",
        defer_execution=True,
    )

    assert request_executor.run_ids == []
    assert deferred_executor.run_ids == [run.id]


def test_deferred_worker_leases_and_completes_the_queued_run() -> None:
    workspace_id = uuid4()
    project_id = uuid4()
    actor_id = uuid4()
    request = AnalysisRunRequest(
        workspace_id=workspace_id,
        project_id=project_id,
        requested_by=actor_id,
        kind=RunKind.INITIAL,
        description="Initial project evidence",
        source_names=("brief.pdf",),
        source_document_ids=(uuid4(),),
    )
    queued = AnalysisRun.queued(request)
    completed = AnalysisRun(
        id=queued.id,
        request=request,
        status=AnalysisRunStatus.COMPLETED,
    )
    deferred_executor = RecordingDurableExecutor()
    application = DatabaseSliceTwoApplication(
        engine=object(),  # type: ignore[arg-type]
        store=RecordingStore(queued),  # type: ignore[arg-type]
        workflow=object(),  # type: ignore[arg-type]
        executor=RecordingExecutor(),
        deferred_executor=deferred_executor,
        document_store=object(),  # type: ignore[arg-type]
    )
    application._workspace_for_project = lambda *_args: workspace_id  # type: ignore[method-assign]
    application.execute_queued_run = lambda _run_id: completed  # type: ignore[method-assign]

    result = application.execute_deferred_analysis(
        actor_user_id=actor_id,
        run_id=queued.id,
        worker_id="request-worker-1",
    )

    assert result.status is AnalysisRunStatus.COMPLETED
    assert deferred_executor.claimed == [(queued.id, "request-worker-1", 900)]
    assert deferred_executor.completed == [queued.id]
    assert deferred_executor.released == []

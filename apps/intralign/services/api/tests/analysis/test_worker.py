from types import SimpleNamespace
from uuid import UUID

from oslo_api.analysis.models import AnalysisRunStatus
from oslo_api.analysis.worker import _process_claimed_run

RUN_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")


class FakeApplication:
    def __init__(self, status: AnalysisRunStatus) -> None:
        self.status = status

    def execute_queued_run(self, run_id: UUID):
        assert run_id == RUN_ID
        return SimpleNamespace(status=self.status)


class FakeQueue:
    def __init__(self) -> None:
        self.completed: list[UUID] = []
        self.released: list[tuple[UUID, str, int]] = []

    def complete(self, run_id: UUID) -> None:
        self.completed.append(run_id)

    def release(self, run_id: UUID, *, error_code: str, delay_seconds: int) -> None:
        self.released.append((run_id, error_code, delay_seconds))


def test_worker_preserves_an_auto_retry_queued_by_the_application() -> None:
    queue = FakeQueue()

    _process_claimed_run(
        application=FakeApplication(AnalysisRunStatus.QUEUED),
        queue=queue,
        run_id=RUN_ID,
        retry_delay_seconds=5,
    )

    assert queue.completed == []
    assert queue.released == []


def test_worker_completes_a_terminal_job() -> None:
    queue = FakeQueue()

    _process_claimed_run(
        application=FakeApplication(AnalysisRunStatus.COMPLETED),
        queue=queue,
        run_id=RUN_ID,
        retry_delay_seconds=5,
    )

    assert queue.completed == [RUN_ID]
    assert queue.released == []


def test_worker_releases_a_crashed_job_for_retry() -> None:
    queue = FakeQueue()
    application = FakeApplication(AnalysisRunStatus.COMPLETED)

    def crash(_run_id: UUID):
        raise RuntimeError("boom")

    application.execute_queued_run = crash  # type: ignore[method-assign]

    _process_claimed_run(
        application=application,
        queue=queue,
        run_id=RUN_ID,
        retry_delay_seconds=5,
    )

    assert queue.completed == []
    assert queue.released == [(RUN_ID, "RuntimeError", 5)]

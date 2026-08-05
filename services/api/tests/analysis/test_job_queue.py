from contextlib import contextmanager
from uuid import UUID

from oslo_api.analysis.job_queue import DatabaseAnalysisJobQueue

RUN_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")


class FakeResult:
    def __init__(self, value=None) -> None:
        self._value = value

    def scalar_one_or_none(self):
        return self._value


class FakeConnection:
    def __init__(self, result=None) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.result = result

    def execute(self, statement, parameters):
        self.calls.append((str(statement), parameters))
        return FakeResult(self.result)


class FakeEngine:
    def __init__(self, result=None) -> None:
        self.connection = FakeConnection(result)

    @contextmanager
    def begin(self):
        yield self.connection


def test_submit_persists_a_replayable_job() -> None:
    engine = FakeEngine()
    queue = DatabaseAnalysisJobQueue(engine)  # type: ignore[arg-type]

    queue.submit(lambda _: None, RUN_ID)

    sql, parameters = engine.connection.calls[0]
    assert "insert into public.analysis_jobs" in sql
    assert "on conflict (analysis_run_id)" in sql
    assert parameters == {"run_id": RUN_ID}


def test_claim_uses_a_lease_and_skip_locked() -> None:
    engine = FakeEngine(RUN_ID)
    queue = DatabaseAnalysisJobQueue(engine)  # type: ignore[arg-type]

    claimed = queue.claim(worker_id="worker-1", lease_seconds=900)

    sql, parameters = engine.connection.calls[0]
    assert claimed == RUN_ID
    assert "for update skip locked" in sql
    assert parameters == {"worker_id": "worker-1", "lease_seconds": 900}


def test_release_requeues_without_persisting_unbounded_error_detail() -> None:
    engine = FakeEngine()
    queue = DatabaseAnalysisJobQueue(engine)  # type: ignore[arg-type]

    queue.release(RUN_ID, error_code="x" * 500, delay_seconds=5)

    _, parameters = engine.connection.calls[0]
    assert parameters["run_id"] == RUN_ID
    assert parameters["delay_seconds"] == 5
    assert len(parameters["error_code"]) == 120

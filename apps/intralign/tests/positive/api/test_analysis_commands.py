"""Analysis-command endpoints (DTM-0032) — :fast / :deep / :cancel.

The command router wires the EXISTING ``submit_trigger`` orchestration seam
(materializer injected, DTM-0030) and persists the affected ``AnalysisRun`` via
the DTM-0031 repo. Each command:

- creates + persists a ``queued`` (or ``cancelled``) run,
- calls ``submit_trigger`` with a valid ``TriggerClaim`` AND the materializer,
- returns the affected ``AnalysisRun`` DTO,
- emits the §8.8 event verbatim (``fast/deep_analysis_requested`` /
  ``analysis_cancelled``).

``Idempotency-Key`` returns the SAME run on retry (no second persist/trigger).
Workspace-scoped via the overridden ``current_principal``.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_analysis_run_repo,
    get_materializer,
    get_projection_reader,
    get_trigger_submitter,
    reset_idempotency_store,
)
from backend.responsibilities.adapt.triggers import TriggerClaim
from tests.positive.api.conftest import AUTH, PROJECT, FakeReader


class FakeRunRepo:
    """In-memory analysis_run repo (mirrors SupabaseAnalysisRunRepository write API)."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}

    def create(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        self.rows[str(stored["analysis_run_id"])] = stored
        return stored

    def update_status(
        self, analysis_run_id: str, run_status: str, **fields: Any
    ) -> dict[str, Any]:
        row = self.rows[str(analysis_run_id)]
        row["run_status"] = run_status
        row.update(fields)
        return row

    def get(self, analysis_run_id: str) -> dict[str, Any] | None:
        return self.rows.get(str(analysis_run_id))


class FakeSubmitter:
    """Captures every submit_trigger call (graph + claim + materializer)."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, graph_name: str, trigger: Any, **kwargs: Any) -> Any:
        self.calls.append(
            {"graph_name": graph_name, "trigger": trigger, "kwargs": kwargs}
        )
        return object()


SENTINEL_MATERIALIZER = object()


@pytest.fixture
def run_repo() -> FakeRunRepo:
    return FakeRunRepo()


@pytest.fixture
def submitter() -> FakeSubmitter:
    return FakeSubmitter()


@pytest.fixture
def cmd_client(
    reader: FakeReader,
    principal: Principal,
    run_repo: FakeRunRepo,
    submitter: FakeSubmitter,
) -> TestClient:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_analysis_run_repo] = lambda: run_repo
    app.dependency_overrides[get_trigger_submitter] = lambda: submitter
    app.dependency_overrides[get_materializer] = lambda: SENTINEL_MATERIALIZER
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    reset_idempotency_store()


# ---- :fast -------------------------------------------------------------------

def test_fast_creates_queued_run_and_returns_dto(
    cmd_client: TestClient, run_repo: FakeRunRepo
) -> None:
    resp = cmd_client.post(f"/v1/projects/{PROJECT}/analysis-runs:fast", headers=AUTH)
    assert resp.status_code == 201
    body = resp.json()
    assert body["project_id"] == PROJECT
    assert body["run_type"] == "fast_analysis_pass"
    assert body["run_status"] == "queued"
    # persisted via the repo
    assert run_repo.rows[body["analysis_run_id"]]["run_status"] == "queued"


def test_fast_calls_submit_trigger_with_claim_and_materializer(
    cmd_client: TestClient, submitter: FakeSubmitter
) -> None:
    cmd_client.post(f"/v1/projects/{PROJECT}/analysis-runs:fast", headers=AUTH)
    assert len(submitter.calls) == 1
    call = submitter.calls[0]
    claim = call["trigger"]
    assert isinstance(claim, TriggerClaim)
    assert claim.project_id == PROJECT
    assert claim.information_changed is True  # A4.6: a real info-change claim
    # the DTM-0030 materializer is injected so derived.*_current materializes
    assert call["kwargs"].get("materializer") is SENTINEL_MATERIALIZER


def test_fast_emits_fast_analysis_requested(cmd_client: TestClient) -> None:
    from backend.api.deps import get_event_emitter

    captured: list[tuple[str, dict]] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append((name, dict(payload)))

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        cmd_client.post(f"/v1/projects/{PROJECT}/analysis-runs:fast", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "fast_analysis_requested" in [name for name, _ in captured]


# ---- :deep -------------------------------------------------------------------

def test_deep_creates_queued_run_with_trigger_source(
    cmd_client: TestClient, submitter: FakeSubmitter
) -> None:
    resp = cmd_client.post(
        f"/v1/projects/{PROJECT}/analysis-runs:deep",
        headers=AUTH,
        json={"trigger_source": "manual"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["run_type"] == "deep_analysis_pass"
    assert body["run_status"] == "queued"
    # submit_trigger called on the deep_pass graph
    assert submitter.calls[0]["graph_name"] == "deep_pass"


def test_deep_emits_deep_analysis_requested(cmd_client: TestClient) -> None:
    from backend.api.deps import get_event_emitter

    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        cmd_client.post(
            f"/v1/projects/{PROJECT}/analysis-runs:deep",
            headers=AUTH,
            json={"trigger_source": "manual"},
        )
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "deep_analysis_requested" in captured


# ---- :cancel -----------------------------------------------------------------

def test_cancel_transitions_run_to_cancelled(
    cmd_client: TestClient, run_repo: FakeRunRepo
) -> None:
    run_repo.rows["run-q"] = {
        "analysis_run_id": "run-q", "project_id": PROJECT,
        "run_type": "deep_analysis_pass", "run_status": "queued",
    }
    resp = cmd_client.post("/v1/analysis-runs/run-q:cancel", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["run_status"] == "cancelled"
    assert run_repo.rows["run-q"]["run_status"] == "cancelled"


def test_cancel_emits_analysis_cancelled(
    cmd_client: TestClient, run_repo: FakeRunRepo
) -> None:
    from backend.api.deps import get_event_emitter

    run_repo.rows["run-r"] = {
        "analysis_run_id": "run-r", "project_id": PROJECT,
        "run_type": "deep_analysis_pass", "run_status": "running",
    }
    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        cmd_client.post("/v1/analysis-runs/run-r:cancel", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "analysis_cancelled" in captured


# ---- idempotency -------------------------------------------------------------

def test_idempotency_key_returns_same_run(
    cmd_client: TestClient, run_repo: FakeRunRepo, submitter: FakeSubmitter
) -> None:
    headers = {**AUTH, "Idempotency-Key": "k-1"}
    first = cmd_client.post(
        f"/v1/projects/{PROJECT}/analysis-runs:fast", headers=headers
    )
    second = cmd_client.post(
        f"/v1/projects/{PROJECT}/analysis-runs:fast", headers=headers
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["analysis_run_id"] == second.json()["analysis_run_id"]
    # the retry neither persisted a second run nor re-triggered
    assert len(run_repo.rows) == 1
    assert len(submitter.calls) == 1

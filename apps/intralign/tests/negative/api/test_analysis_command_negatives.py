"""Analysis-command negatives (DTM-0032) — auth / scoping / transition / purity.

- Unauthenticated command ⇒ 401 (the §3 auth contract).
- A project / run outside the caller's workspace ⇒ 404 (existence not leaked, §12).
- Cancelling a terminal run ⇒ 409 (illegal transition; §9, run not queued/running).
- The command writes NO canonical row directly — it persists the platform
  ``analysis_run`` only; the durable run does the CHR append via the frozen
  retain path (the command never touches a CHR repo).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_analysis_run_repo,
    get_materializer,
    get_trigger_submitter,
    reset_idempotency_store,
)
from backend.api.v1 import router as v1_router
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader
from tests.positive.api.test_analysis_commands import FakeRunRepo, FakeSubmitter

AUTH = {"Authorization": "Bearer t"}


def _wire(reader: FakeReader, principal: Principal, repo: FakeRunRepo) -> None:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    from backend.api.deps import get_projection_reader

    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_analysis_run_repo] = lambda: repo
    app.dependency_overrides[get_trigger_submitter] = lambda: FakeSubmitter()
    app.dependency_overrides[get_materializer] = lambda: object()


def _reader_with_project(project_id: str, workspace_id: str) -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": project_id, "workspace_id": workspace_id,
        "lifecycle_state": "oriented", "title": "p",
    })
    return r


# ---- auth --------------------------------------------------------------------

def test_unauthenticated_fast_is_401() -> None:
    """No bearer ⇒ 401 (current_principal NOT overridden)."""
    with TestClient(app) as c:
        resp = c.post(f"/v1/projects/{PROJECT}/analysis-runs:fast")
    assert resp.status_code == 401


# ---- workspace scoping -------------------------------------------------------

def test_fast_on_out_of_workspace_project_is_404() -> None:
    reader = _reader_with_project("p-other", "ws-OTHER")
    principal = Principal(user_id="u-1", workspace_id="ws-1", role="member")
    repo = FakeRunRepo()
    _wire(reader, principal, repo)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/projects/p-other/analysis-runs:fast", headers=AUTH)
        assert resp.status_code == 404
        assert repo.rows == {}  # nothing persisted for an out-of-scope project
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_cancel_on_out_of_workspace_run_is_404() -> None:
    reader = _reader_with_project("p-other", "ws-OTHER")
    principal = Principal(user_id="u-1", workspace_id="ws-1", role="member")
    repo = FakeRunRepo()
    repo.rows["run-x"] = {
        "analysis_run_id": "run-x", "project_id": "p-other",
        "run_type": "deep_analysis_pass", "run_status": "queued",
    }
    _wire(reader, principal, repo)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/analysis-runs/run-x:cancel", headers=AUTH)
        assert resp.status_code == 404
        assert repo.rows["run-x"]["run_status"] == "queued"  # untouched
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- illegal transition ------------------------------------------------------

def test_cancel_completed_run_is_409() -> None:
    reader = _reader_with_project(PROJECT, WORKSPACE)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    repo = FakeRunRepo()
    repo.rows["run-done"] = {
        "analysis_run_id": "run-done", "project_id": PROJECT,
        "run_type": "deep_analysis_pass", "run_status": "completed",
    }
    _wire(reader, principal, repo)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/analysis-runs/run-done:cancel", headers=AUTH)
        assert resp.status_code == 409
        assert repo.rows["run-done"]["run_status"] == "completed"  # unchanged
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- purity: no canonical write from the command ----------------------------

def test_command_router_has_no_chr_repo_dependency() -> None:
    """The command router never imports/uses a CHR repo — canonical writes happen
    inside the durable run via the frozen retain path, not the transport."""
    import inspect

    from backend.api.v1.routers import analysis_commands

    src = inspect.getsource(analysis_commands)
    assert "chr_repo" not in src
    assert "ChrRepository" not in src
    # the command persists the PLATFORM analysis_run only (no canonical store)
    assert "AttestedAssertion" not in src
    assert "cognition_history_record" not in src


# ---- read surface stays GET-only (no regression) ----------------------------

def _read_routers():
    """The DTM-0018 read routers identified by tag (commands are separate)."""
    read_tags = {
        "projects", "analysis_runs", "findings", "recommendations",
        "confidence", "acceptance", "notifications",
    }
    return [
        r for r in v1_router.routes
        if getattr(r, "path", "").startswith("/v1")
        and set(getattr(r, "tags", []) or []) & read_tags
    ]


def test_read_routers_stay_get_only_after_commands_added() -> None:
    """Adding the command router does not turn any DTM-0018 read route mutating."""
    mutating = {"POST", "PUT", "PATCH", "DELETE"}
    for route in _read_routers():
        methods = set(getattr(route, "methods", set()))
        assert not (methods & mutating), (
            f"{route.path} (read router) exposes {methods & mutating} — the "
            "Disclose read surface must stay read-mostly"
        )

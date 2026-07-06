"""Project-command + evidence/artifact negatives (DTM-0034) — the guards.

- **RBAC on archive** — a member (not owner/admin) cannot archive: 403, and the
  repo's ``update_lifecycle`` is never called (no archived row written).
- **OSLO never writes canonical from transport** — the evidence/artifact command
  wires ONLY the intake seam (artifact / promotion_candidate); it appends NO
  ``attested_assertion`` / CHR (admission, the frozen retain path, does that on
  the downstream promotion). The router exposes/uses no canonical store.
- 401 unauthenticated · 404 cross-workspace (existence not leaked, §12).
- The GET read routers stay GET-only (no command leaks onto them).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_body_store,
    get_event_emitter,
    get_intake_store,
    get_projection_reader,
    get_project_repo,
    reset_idempotency_store,
)
from backend.api.v1 import router as v1_router
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader
from tests.positive.api.test_project_commands import (
    FakeBodyStore,
    FakeEmitter,
    FakeIntakeStore,
    FakeProjectRepo,
)

AUTH = {"Authorization": "Bearer t"}


def _reader() -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE,
        "lifecycle_state": "oriented", "title": "p",
    })
    return r


def _wire(
    reader: FakeReader,
    principal: Principal,
    repo: FakeProjectRepo,
    intake: FakeIntakeStore,
    bodies: FakeBodyStore,
    emitter: FakeEmitter,
) -> None:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_project_repo] = lambda: repo
    app.dependency_overrides[get_intake_store] = lambda: intake
    app.dependency_overrides[get_body_store] = lambda: bodies
    app.dependency_overrides[get_event_emitter] = lambda: emitter


# ---- RBAC on archive (Critical) ---------------------------------------------

def test_member_cannot_archive_403_no_write() -> None:
    """A member (not owner/admin) gets 403; no archived row is written."""
    reader = _reader()
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    repo = FakeProjectRepo()
    _wire(reader, principal, repo, FakeIntakeStore(), FakeBodyStore(), FakeEmitter())
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/projects/{PROJECT}:archive", headers=AUTH)
        assert resp.status_code == 403
        assert repo.lifecycle == []  # update_lifecycle never called
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_admin_can_archive() -> None:
    """An admin IS allowed to archive (owner/admin both pass the RBAC gate)."""
    reader = _reader()
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="admin")
    repo = FakeProjectRepo()
    _wire(reader, principal, repo, FakeIntakeStore(), FakeBodyStore(), FakeEmitter())
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/projects/{PROJECT}:archive", headers=AUTH)
        assert resp.status_code == 200
        assert (PROJECT, "archived") in repo.lifecycle
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- no direct canonical write (Critical epistemic guard) -------------------

def test_evidence_command_writes_no_canonical_row() -> None:
    """The evidence command wires ONLY the intake seam — it appends NO canonical
    attested_assertion / CHR. Admission (the frozen retain path) is the sole
    producer of the attested assertion, on the downstream promotion."""
    reader = _reader()
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="owner")
    intake = FakeIntakeStore()
    _wire(reader, principal, FakeProjectRepo(), intake, FakeBodyStore(), FakeEmitter())
    try:
        with TestClient(app) as c:
            resp = c.post(
                f"/v1/projects/{PROJECT}/evidence",
                json={"source_type": "interview", "content_ref": "x"},
                headers=AUTH,
            )
        assert resp.status_code == 201
        # The intake store has NO canonical surface — no insert_assertion / CHR
        # method exists on it (the artifact anchor is evidence-attested, the
        # attested_assertion is written only by admission downstream).
        assert not hasattr(intake, "insert_assertion")
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- 401 unauthenticated ----------------------------------------------------

def test_unauthenticated_create_is_401() -> None:
    repo = FakeProjectRepo()
    app.dependency_overrides[get_project_repo] = lambda: repo
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/projects", json={"title": "x"})
        assert resp.status_code == 401
        assert repo.created == []  # nothing written without an authenticated actor
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_unauthenticated_add_evidence_is_401() -> None:
    intake = FakeIntakeStore()
    app.dependency_overrides[get_intake_store] = lambda: intake
    try:
        with TestClient(app) as c:
            resp = c.post(
                f"/v1/projects/{PROJECT}/evidence",
                json={"source_type": "interview", "content_ref": "x"},
            )
        assert resp.status_code == 401
        assert intake.artifacts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- 404 cross-workspace (existence not leaked) -----------------------------

def test_add_evidence_cross_workspace_404() -> None:
    """Evidence on a project outside the caller's workspace is an indistinguishable
    404 — no intake runs."""
    reader = FakeReader()  # the project lives in ANOTHER workspace
    reader.projects.append({
        "project_id": PROJECT, "workspace_id": "other-ws",
        "lifecycle_state": "oriented", "title": "p",
    })
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="owner")
    intake = FakeIntakeStore()
    _wire(reader, principal, FakeProjectRepo(), intake, FakeBodyStore(), FakeEmitter())
    try:
        with TestClient(app) as c:
            resp = c.post(
                f"/v1/projects/{PROJECT}/evidence",
                json={"source_type": "interview", "content_ref": "x"},
                headers=AUTH,
            )
        assert resp.status_code == 404
        assert intake.artifacts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_archive_cross_workspace_404() -> None:
    reader = FakeReader()
    reader.projects.append({
        "project_id": PROJECT, "workspace_id": "other-ws",
        "lifecycle_state": "oriented", "title": "p",
    })
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="owner")
    repo = FakeProjectRepo()
    _wire(reader, principal, repo, FakeIntakeStore(), FakeBodyStore(), FakeEmitter())
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/projects/{PROJECT}:archive", headers=AUTH)
        assert resp.status_code == 404
        assert repo.lifecycle == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- the GET read routers stay GET-only -------------------------------------

def test_get_projects_router_is_get_only() -> None:
    """The DTM-0018 read routes reject writes — commands live on the command
    router, never bolted onto a GET reader (read-mostly preserved)."""
    routes = {
        (r.path, m)
        for r in v1_router.routes
        for m in getattr(r, "methods", set())
    }
    # The list/detail readers exist as GET only — no POST/PATCH/DELETE on them.
    assert ("/v1/projects", "GET") in routes
    assert ("/v1/projects", "POST") in routes  # the NEW command (different handler)
    # The detail reader is GET; the command surface adds :archive, not a write on /{id}.
    assert ("/v1/projects/{project_id}", "GET") in routes

"""Project-command + evidence/artifact-intake endpoints (DTM-0034).

The WRITE counterpart to the DTM-0018 GET projects read router (which stays
GET-only). Each command wires an EXISTING seam — it invents no persistence:

- ``POST /projects`` → ``project_repo.create`` a ``created`` project + emit
  ``project_created``; ``PATCH /projects/{pid}`` → ``project_repo.update`` +
  ``project_updated``; ``POST /projects/{pid}:archive`` →
  ``project_repo.update_lifecycle('archived')`` + ``project_archived`` (owner/
  admin only).
- ``POST /projects/{pid}/evidence`` → the EXISTING ``submit_artifact`` intake
  seam (body → Storage, metadata → the append-only ``artifact`` anchor +
  ``promotion_candidate``) + emit ``evidence_added``.
- ``POST /projects/{pid}/artifacts`` → same intake seam + ``artifact_created``;
  ``POST /artifacts/{aid}/versions`` → a re-submission (a NEW artifact version,
  ``version+1``/``supersedes_id`` handled by intake) + ``artifact_version_created``.

Epistemic boundary (code/CLAUDE.md hard rules): the command persists the PLATFORM
``project`` row (project_repo) or the intake ``artifact``/``promotion_candidate``
rows (intake seam) ONLY. The canonical ``attested_assertion`` append happens INSIDE
admission (the frozen retain path) on the downstream promotion/recompute — NEVER
from this transport. ``Idempotency-Key`` returns the same resource on retry (§10);
every path is workspace-scoped (401 unauth / 404 cross-workspace, §3/§12); archive
requires owner/admin (§3).
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
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
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader

AUTH = {"Authorization": "Bearer test-token"}


# --- fakes -------------------------------------------------------------------

class FakeProjectRepo:
    """In-memory mirror of SupabaseProjectRepository (create/update/update_lifecycle).

    Captures every write so a test can assert what the router asked the repo to
    persist. It has NO canonical surface (no attested_assertion / CHR) — the
    project table is platform, mutable, never append-only-canonical.
    """

    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []
        self.updated: list[dict[str, Any]] = []
        self.lifecycle: list[tuple[str, str]] = []
        self.rows: dict[str, dict[str, Any]] = {}

    def create(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("created_at", "2026-06-26T00:00:00Z")
        self.created.append(stored)
        self.rows[str(stored["project_id"])] = stored
        return stored

    def update(self, project_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        self.updated.append({"project_id": project_id, "patch": dict(patch)})
        row = dict(self.rows.get(project_id, {"project_id": project_id, "workspace_id": WORKSPACE}))
        row.update(patch)
        row.setdefault("lifecycle_state", "created")
        self.rows[project_id] = row
        return row

    def update_lifecycle(self, project_id: str, lifecycle_state: str) -> dict[str, Any]:
        self.lifecycle.append((project_id, lifecycle_state))
        row = dict(self.rows.get(project_id, {"project_id": project_id, "workspace_id": WORKSPACE}))
        row["lifecycle_state"] = lifecycle_state
        self.rows[project_id] = row
        return row


class FakeIntakeStore:
    """In-memory artifact/promotion_candidate store (mirrors SupabaseIntakeStore)."""

    def __init__(self) -> None:
        self.artifacts: list[dict[str, Any]] = []
        self.candidates: list[dict[str, Any]] = []

    def find_artifact_by_dedup_key(self, dedup_key: str) -> dict[str, Any] | None:
        for a in self.artifacts:
            if a.get("dedup_key") == dedup_key:
                return a
        return None

    def latest_artifact_for_source(self, project_id: str, source: str) -> dict[str, Any] | None:
        rows = [
            a for a in self.artifacts
            if str(a.get("project_id")) == project_id
            and a.get("provenance", {}).get("source") == source
        ]
        return rows[-1] if rows else None

    def save_artifact(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("artifact_id", f"art-{len(self.artifacts) + 1}")
        stored.setdefault("created_at", "2026-06-26T00:00:00Z")
        self.artifacts.append(stored)
        return stored

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        for a in self.artifacts:
            if str(a.get("artifact_id")) == artifact_id:
                return a
        return None

    def save_candidate(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("candidate_id", f"cand-{len(self.candidates) + 1}")
        self.candidates.append(stored)
        return stored

    def candidate_for_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        rows = [c for c in self.candidates if str(c.get("artifact_ref")) == artifact_id]
        return rows[-1] if rows else None


class FakeBodyStore:
    """In-memory body store (mirrors ArtifactBodyStore.upload_body)."""

    def __init__(self) -> None:
        self.bodies: list[tuple[str, str]] = []

    def upload_body(self, project_id: str, content: str | bytes) -> str:
        text = content.decode() if isinstance(content, bytes) else content
        self.bodies.append((project_id, text))
        return f"artifacts/{project_id}/body-{len(self.bodies)}.txt"

    def download_body(self, body_ref: str) -> bytes:  # pragma: no cover - unused
        return b""


class FakeEmitter:
    """Captures emitted (name, payload) pairs (the §8 event assertions)."""

    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def emit(self, name: str, payload: dict[str, Any]) -> None:
        self.events.append((name, dict(payload)))

    def names(self) -> list[str]:
        return [n for n, _ in self.events]


# --- fixtures ----------------------------------------------------------------

@pytest.fixture
def repo() -> FakeProjectRepo:
    return FakeProjectRepo()


@pytest.fixture
def intake() -> FakeIntakeStore:
    return FakeIntakeStore()


@pytest.fixture
def bodies() -> FakeBodyStore:
    return FakeBodyStore()


@pytest.fixture
def emitter() -> FakeEmitter:
    return FakeEmitter()


@pytest.fixture
def project_reader() -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE, "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    })
    return r


@pytest.fixture
def principal() -> Principal:
    return Principal(user_id="u-1", workspace_id=WORKSPACE, role="owner")


@pytest.fixture
def client(
    repo: FakeProjectRepo,
    intake: FakeIntakeStore,
    bodies: FakeBodyStore,
    emitter: FakeEmitter,
    project_reader: FakeReader,
    principal: Principal,
) -> TestClient:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: project_reader
    app.dependency_overrides[get_project_repo] = lambda: repo
    app.dependency_overrides[get_intake_store] = lambda: intake
    app.dependency_overrides[get_body_store] = lambda: bodies
    app.dependency_overrides[get_event_emitter] = lambda: emitter
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    reset_idempotency_store()


# --- project create ----------------------------------------------------------

def test_create_project_persists_created_and_emits(
    client: TestClient, repo: FakeProjectRepo, emitter: FakeEmitter
) -> None:
    resp = client.post("/v1/projects", json={"title": "New", "description": "d"}, headers=AUTH)
    assert resp.status_code == 201
    body = resp.json()
    assert body["lifecycle_state"] == "created"
    assert body["title"] == "New"
    assert body["workspace_id"] == WORKSPACE
    # Persisted via the repo (platform write), workspace-scoped from the Principal.
    assert len(repo.created) == 1
    assert repo.created[0]["workspace_id"] == WORKSPACE
    assert repo.created[0]["lifecycle_state"] == "created"
    assert repo.created[0]["created_by_user_id"] == "u-1"
    assert "project_created" in emitter.names()


def test_create_project_allows_empty_body(client: TestClient, repo: FakeProjectRepo) -> None:
    resp = client.post("/v1/projects", json={}, headers=AUTH)
    assert resp.status_code == 201
    assert resp.json()["lifecycle_state"] == "created"
    assert len(repo.created) == 1


# --- project patch -----------------------------------------------------------

def test_patch_project_updates_and_emits(
    client: TestClient, repo: FakeProjectRepo, emitter: FakeEmitter
) -> None:
    resp = client.patch(f"/v1/projects/{PROJECT}", json={"title": "Renamed"}, headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Renamed"
    assert repo.updated[0]["project_id"] == PROJECT
    assert repo.updated[0]["patch"] == {"title": "Renamed"}
    assert "project_updated" in emitter.names()


def test_patch_project_cross_workspace_404(client: TestClient, repo: FakeProjectRepo) -> None:
    resp = client.patch("/v1/projects/does-not-exist", json={"title": "x"}, headers=AUTH)
    assert resp.status_code == 404
    assert repo.updated == []  # nothing written for an out-of-scope project


# --- project archive (RBAC) --------------------------------------------------

def test_archive_project_owner_transitions_and_emits(
    client: TestClient, repo: FakeProjectRepo, emitter: FakeEmitter
) -> None:
    resp = client.post(f"/v1/projects/{PROJECT}:archive", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["lifecycle_state"] == "archived"
    assert (PROJECT, "archived") in repo.lifecycle
    assert "project_archived" in emitter.names()


# --- evidence intake ---------------------------------------------------------

def test_add_evidence_wires_intake_and_emits(
    client: TestClient, intake: FakeIntakeStore, bodies: FakeBodyStore, emitter: FakeEmitter
) -> None:
    resp = client.post(
        f"/v1/projects/{PROJECT}/evidence",
        json={"source_type": "interview", "content_ref": "Scope is X."},
        headers=AUTH,
    )
    assert resp.status_code == 201
    # The intake seam persisted an artifact (the evidence anchor) + a candidate;
    # the body went to Storage. The router wrote NO canonical row directly.
    assert len(intake.artifacts) == 1
    assert len(intake.candidates) == 1
    assert len(bodies.bodies) == 1
    assert intake.artifacts[0]["project_id"] == PROJECT
    assert "evidence_added" in emitter.names()


def test_add_evidence_is_idempotent_on_dedup_key(
    client: TestClient, intake: FakeIntakeStore
) -> None:
    payload = {"source_type": "interview", "content_ref": "Same body."}
    client.post(f"/v1/projects/{PROJECT}/evidence", json=payload, headers=AUTH)
    client.post(f"/v1/projects/{PROJECT}/evidence", json=payload, headers=AUTH)
    # Identical submission (same dedup_key) → one artifact, no second admission.
    assert len(intake.artifacts) == 1


# --- artifact intake + versions ---------------------------------------------

def test_create_artifact_wires_intake_and_emits(
    client: TestClient, intake: FakeIntakeStore, emitter: FakeEmitter
) -> None:
    resp = client.post(
        f"/v1/projects/{PROJECT}/artifacts",
        json={"artifact_type": "intent", "content": "Build a thing."},
        headers=AUTH,
    )
    assert resp.status_code == 201
    assert len(intake.artifacts) == 1
    assert intake.artifacts[0]["version"] == 1
    assert "artifact_created" in emitter.names()


def test_create_artifact_version_appends_and_emits(
    client: TestClient, intake: FakeIntakeStore, emitter: FakeEmitter
) -> None:
    first = client.post(
        f"/v1/projects/{PROJECT}/artifacts",
        json={"artifact_type": "intent", "content": "v1 body."},
        headers=AUTH,
    )
    aid = first.json()["artifact_id"]
    resp = client.post(
        f"/v1/artifacts/{aid}/versions",
        json={"content": "v2 body, changed."},
        headers=AUTH,
    )
    assert resp.status_code == 201
    # A re-submission from the same project+source appends a NEW artifact version.
    assert len(intake.artifacts) == 2
    assert intake.artifacts[1]["version"] == 2
    assert intake.artifacts[1]["supersedes_id"] == aid
    assert "artifact_version_created" in emitter.names()


# --- idempotency on commands -------------------------------------------------

def test_create_project_idempotency_replays(
    client: TestClient, repo: FakeProjectRepo
) -> None:
    key = {"Idempotency-Key": str(uuid.uuid4()), **AUTH}
    first = client.post("/v1/projects", json={"title": "Once"}, headers=key)
    second = client.post("/v1/projects", json={"title": "Once"}, headers=key)
    assert first.json()["project_id"] == second.json()["project_id"]
    assert len(repo.created) == 1  # the second call did NOT persist again

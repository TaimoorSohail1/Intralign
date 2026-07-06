"""Finding-lifecycle + notification-state command endpoints (DTM-0035).

Two additive command routers, separate from the DTM-0018 GET read surface:

- ``POST /v1/findings/{fid}:acknowledge`` / ``:address`` / ``:reopen`` — the finding
  WORKFLOW STATUS transition. Per State Model §10 the finding status is an ATTRIBUTE
  on the Derived projection (``derived.finding_current`` ``current_payload.status``),
  NOT a user-attested record: the command reads the projection, advances its status
  per the §10 transition table, and UPSERTs it back through the DTM-0030 projection
  store. It appends NO CHR, writes NO canonical row, and creates NO UAR (it is not an
  acceptance). Per API Contract §5 + catalog: :acknowledge/:address emit
  ``finding_updated`` (resulting status in payload); :reopen emits ``finding_reopened``.
- ``POST /v1/notifications/{nid}:view`` / ``:dismiss`` — the PLATFORM awareness state
  transition via the DTM-0031 ``notification_repo`` (mark_viewed/mark_dismissed). It
  is non-canonical: it changes no assessment, drives no analysis, alters no Finding.
  Emits ``notification_viewed`` / ``notification_dismissed`` (EM §12).

``Idempotency-Key`` returns the same DTO on retry (no second write); every path is
workspace-scoped via ``current_principal`` (401 unauth / 404 cross-workspace, §9/§12).
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_event_emitter,
    get_notification_repo,
    get_projection_reader,
    get_projection_store,
    reset_idempotency_store,
)
from tests.positive.api.conftest import AUTH, PROJECT, WORKSPACE, FakeReader

FINDING_ID = "f-1"
NOTIF_ID = "n-1"


class FakeProjectionStore:
    """In-memory ``derived.*_current`` store (mirrors SupabaseProjectionStore.upsert).

    Captures every ``upsert_projection`` call so a test can assert the finding
    status was advanced on the DERIVED projection (and ONLY there — no canonical
    surface exists on this class, mirroring production).
    """

    def __init__(self) -> None:
        self.upserts: list[tuple[str, dict[str, Any]]] = []

    def upsert_projection(self, output_kind: str, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        self.upserts.append((output_kind, stored))
        return stored


class FakeNotificationRepo:
    """In-memory platform ``notification`` repo (mirrors mark_viewed/mark_dismissed).

    Holds rows keyed by id so the command can resolve + scope them, and records
    which mutation was applied (awareness state only — never canonical).
    """

    def __init__(self, rows: list[dict[str, Any]] | None = None) -> None:
        self.rows: dict[str, dict[str, Any]] = {
            str(r["notification_id"]): dict(r) for r in (rows or [])
        }
        self.viewed: list[str] = []
        self.dismissed: list[str] = []

    def get(self, notification_id: str) -> dict[str, Any] | None:
        return self.rows.get(notification_id)

    def mark_viewed(self, notification_id: str, viewed_at: str | None = None) -> dict[str, Any]:
        self.viewed.append(notification_id)
        row = self.rows.get(notification_id, {})
        row = {**row, "state": "viewed"}
        if viewed_at is not None:
            row["viewed_at"] = viewed_at
        self.rows[notification_id] = row
        return row

    def mark_dismissed(
        self, notification_id: str, dismissed_at: str | None = None
    ) -> dict[str, Any]:
        self.dismissed.append(notification_id)
        row = self.rows.get(notification_id, {})
        row = {**row, "state": "dismissed"}
        if dismissed_at is not None:
            row["dismissed_at"] = dismissed_at
        self.rows[notification_id] = row
        return row


class CapturingEmitter:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def emit(self, name: str, payload: dict[str, Any]) -> None:
        self.events.append((name, dict(payload)))

    @property
    def names(self) -> list[str]:
        return [n for n, _ in self.events]


def _reader_with_finding(status: str = "detected") -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE,
        "lifecycle_state": "oriented", "title": "Demo",
    })
    r.projections.setdefault("finding", []).append({
        "projection_id": FINDING_ID,
        "project_id": PROJECT,
        "output_kind": "finding",
        "current_payload": {
            "finding_id": FINDING_ID, "finding_type": "conflict", "summary": "x",
            "evidence_anchors": ["a-0"], "status": status,
        },
        "current_chr_ref": "chr-1",
        "epistemic_label": "derived",
        "confidence_value": 60.0, "confidence_band": "medium",
        "conflict_state": "contested", "recomputed_at": "2026-06-25T00:00:00Z",
    })
    return r


def _notif_row(state: str = "created") -> dict[str, Any]:
    return {
        "notification_id": NOTIF_ID, "workspace_id": WORKSPACE, "project_id": PROJECT,
        "source_object_type": "finding", "source_object_id": FINDING_ID,
        "event_type": "created", "state": state,
    }


@pytest.fixture
def store() -> FakeProjectionStore:
    return FakeProjectionStore()


@pytest.fixture
def notif_repo() -> FakeNotificationRepo:
    return FakeNotificationRepo([_notif_row()])


@pytest.fixture
def emitter() -> CapturingEmitter:
    return CapturingEmitter()


def _wire(
    reader: FakeReader,
    store: FakeProjectionStore,
    notif_repo: FakeNotificationRepo,
    emitter: CapturingEmitter,
    principal: Principal | None = None,
) -> None:
    reset_idempotency_store()
    p = principal or Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    app.dependency_overrides[current_principal] = lambda: p
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_projection_store] = lambda: store
    app.dependency_overrides[get_notification_repo] = lambda: notif_repo
    app.dependency_overrides[get_event_emitter] = lambda: emitter


# ---- finding :acknowledge (detected → acknowledged) --------------------------

def test_acknowledge_advances_projection_status_and_emits(
    store: FakeProjectionStore, notif_repo: FakeNotificationRepo, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("detected")
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["status"] == "acknowledged"
        assert resp.json()["finding_id"] == FINDING_ID
        # the DERIVED projection status was advanced (the ONLY write)
        assert len(store.upserts) == 1
        kind, row = store.upserts[0]
        assert kind == "finding"
        assert row["current_payload"]["status"] == "acknowledged"
        # API §5 / catalog: :acknowledge carries finding_updated (status in payload)
        assert "finding_updated" in emitter.names
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- finding :address (acknowledged → addressed) -----------------------------

def test_address_advances_projection_status_and_emits(
    store: FakeProjectionStore, notif_repo: FakeNotificationRepo, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("acknowledged")
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:address", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["status"] == "addressed"
        assert store.upserts[0][1]["current_payload"]["status"] == "addressed"
        assert "finding_updated" in emitter.names
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- finding :reopen (closed → reopened) -------------------------------------

def test_reopen_advances_projection_status_and_emits(
    store: FakeProjectionStore, notif_repo: FakeNotificationRepo, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("closed")
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:reopen", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["status"] == "reopened"
        assert store.upserts[0][1]["current_payload"]["status"] == "reopened"
        # API §5 / catalog: :reopen carries finding_reopened
        assert "finding_reopened" in emitter.names
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_finding_command_preserves_cognition_payload(
    store: FakeProjectionStore, notif_repo: FakeNotificationRepo, emitter: CapturingEmitter
) -> None:
    """Only ``status`` changes — the finding's content/confidence/CHR are untouched."""
    reader = _reader_with_finding("detected")
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=AUTH)
        _, row = store.upserts[0]
        # the cognition snapshot is preserved verbatim apart from status
        assert row["current_payload"]["summary"] == "x"
        assert row["current_payload"]["finding_type"] == "conflict"
        assert row["current_payload"]["evidence_anchors"] == ["a-0"]
        # the envelope (CHR lineage + confidence) is unchanged — no recompute
        assert row["current_chr_ref"] == "chr-1"
        assert row["confidence_value"] == 60.0
        assert row["confidence_band"] == "medium"
        assert row["epistemic_label"] == "derived"
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- notification :view (created → viewed) -----------------------------------

def test_view_marks_viewed_via_repo_and_emits(
    store: FakeProjectionStore, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("detected")
    notif_repo = FakeNotificationRepo([_notif_row("created")])
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/notifications/{NOTIF_ID}:view", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["state"] == "viewed"
        assert notif_repo.viewed == [NOTIF_ID]
        assert "notification_viewed" in emitter.names
        # the awareness command wrote NO derived projection (no cognition touched)
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- notification :dismiss (→ dismissed) -------------------------------------

def test_dismiss_marks_dismissed_via_repo_and_emits(
    store: FakeProjectionStore, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("detected")
    notif_repo = FakeNotificationRepo([_notif_row("viewed")])
    _wire(reader, store, notif_repo, emitter)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/notifications/{NOTIF_ID}:dismiss", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json()["state"] == "dismissed"
        assert notif_repo.dismissed == [NOTIF_ID]
        assert "notification_dismissed" in emitter.names
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- idempotency -------------------------------------------------------------

def test_acknowledge_idempotency_replays_no_double_upsert(
    store: FakeProjectionStore, notif_repo: FakeNotificationRepo, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("detected")
    _wire(reader, store, notif_repo, emitter)
    headers = {**AUTH, "Idempotency-Key": "ack-1"}
    try:
        with TestClient(app) as c:
            first = c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=headers)
            second = c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=headers)
        assert first.json()["finding_id"] == second.json()["finding_id"]
        assert len(store.upserts) == 1  # the retry wrote no second projection upsert
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_dismiss_idempotency_replays_no_double_mark(
    store: FakeProjectionStore, emitter: CapturingEmitter
) -> None:
    reader = _reader_with_finding("detected")
    notif_repo = FakeNotificationRepo([_notif_row("created")])
    _wire(reader, store, notif_repo, emitter)
    headers = {**AUTH, "Idempotency-Key": "dis-1"}
    try:
        with TestClient(app) as c:
            first = c.post(f"/v1/notifications/{NOTIF_ID}:dismiss", headers=headers)
            second = c.post(f"/v1/notifications/{NOTIF_ID}:dismiss", headers=headers)
        assert first.json()["notification_id"] == second.json()["notification_id"]
        assert notif_repo.dismissed == [NOTIF_ID]  # the retry did not mark twice
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()

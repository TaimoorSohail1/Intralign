"""Finding-lifecycle + notification-state command negatives (DTM-0035).

The Critical epistemic guards:

- **Notification state is PLATFORM / non-canonical** — :view/:dismiss change NO
  assessment, drive NO analysis, write NO derived projection, append NO CHR. A
  dismiss leaves the referenced Finding's confidence/content unchanged (§12
  clarification: notification state changes do not alter Findings).
- **Finding lifecycle is NOT an acceptance + NOT a cognition change** — :acknowledge/
  :address/:reopen update the DERIVED projection ``status`` ONLY (State Model §10:
  a status attribute, not a user-attested record). They write NO UAR, NO canonical
  row, and never recompute (confidence/content/CHR unchanged). The projection store
  has no canonical surface; the command never touches the retention store.
- **Invalid transitions are 409** (API §5 — e.g. acknowledge a non-``detected``
  finding) and never silently mutate.
- 401 unauthenticated · 404 cross-workspace / missing (existence not leaked, §12).
- The GET read routers stay GET-only after the command routers are added.
"""

from __future__ import annotations

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
from backend.api.v1 import router as v1_router
from tests.positive.api.conftest import WORKSPACE
from tests.positive.api.test_finding_notification_commands import (
    FINDING_ID,
    NOTIF_ID,
    CapturingEmitter,
    FakeNotificationRepo,
    FakeProjectionStore,
    _notif_row,
    _reader_with_finding,
)

AUTH = {"Authorization": "Bearer t"}


def _wire(reader, store, notif_repo, emitter, principal: Principal) -> None:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_projection_store] = lambda: store
    app.dependency_overrides[get_notification_repo] = lambda: notif_repo
    app.dependency_overrides[get_event_emitter] = lambda: emitter


# ---- notification state is non-canonical (Critical) --------------------------

def test_dismiss_does_not_change_the_referenced_finding() -> None:
    """A notification :dismiss alters NO Finding — no derived projection is written.

    §12 clarification: notification state changes do not alter Findings or
    Recommendations. The finding's confidence/content/status are untouched.
    """
    reader = _reader_with_finding("detected")
    finding_before = dict(reader.projections["finding"][0]["current_payload"])
    conf_before = reader.projections["finding"][0]["confidence_value"]
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row("created")])
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/notifications/{NOTIF_ID}:dismiss", headers=AUTH)
        assert resp.status_code == 200
        # NO derived projection write — the awareness command touches no cognition
        assert store.upserts == []
        # the referenced finding is byte-for-byte unchanged (confidence + content)
        assert reader.projections["finding"][0]["current_payload"] == finding_before
        assert reader.projections["finding"][0]["confidence_value"] == conf_before
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_notification_command_uses_repo_only_no_canonical_or_assessment_write() -> None:
    """The router wires notification_repo only — no projection/retention/CHR write."""
    import inspect

    from backend.api.v1.routers import notification_commands

    src = inspect.getsource(notification_commands)
    assert "mark_viewed" in src or "mark_dismissed" in src
    # it never reaches into a canonical / assessment write surface
    assert "upsert_projection" not in src
    assert "insert_acceptance" not in src
    assert "insert_assertion" not in src
    assert "chr_repo" not in src
    assert ".append(" not in src


# ---- finding lifecycle is no UAR + no cognition change (Critical) -------------

def test_finding_command_writes_no_uar_and_does_not_recompute() -> None:
    """:acknowledge advances the projection status ONLY — no UAR, no recompute.

    State Model §10: the finding status is a Derived-projection attribute, not a
    user-attested record. The command appends no CHR and changes neither the
    finding's confidence nor its content (it is not a cognition change).
    """
    reader = _reader_with_finding("detected")
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=AUTH)
        assert len(store.upserts) == 1
        _, row = store.upserts[0]
        # the ONLY field changed is status — confidence + content + CHR are intact
        assert row["confidence_value"] == 60.0
        assert row["current_payload"]["summary"] == "x"
        assert row["current_chr_ref"] == "chr-1"
        # the projection write stays in the DERIVED schema only (status attribute)
        assert row["epistemic_label"] == "derived"
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_finding_command_wires_projection_store_only_no_acceptance() -> None:
    """The finding router updates the projection — it reimplements no UAR/CHR write."""
    import inspect

    from backend.api.v1.routers import finding_commands

    src = inspect.getsource(finding_commands)
    assert "upsert_projection" in src
    # it never authors an acceptance record or appends a CHR (not an acceptance /
    # no cognition change) — no acceptance/retention/CHR WRITE call is wired.
    assert "record_acceptance(" not in src
    assert "insert_acceptance" not in src
    assert "insert_assertion" not in src
    assert "chr_repo.append" not in src
    assert "get_retention_store" not in src


# ---- invalid transition is 409 (no silent mutation) --------------------------

def test_acknowledge_non_detected_finding_is_409_no_write() -> None:
    """Acknowledging a finding that is not ``detected`` is a 409 conflict (API §5)."""
    reader = _reader_with_finding("addressed")  # not detected
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=AUTH)
        assert resp.status_code == 409
        assert resp.json()["detail"]["error"]["code"] == "conflict"
        assert store.upserts == []  # the invalid transition wrote nothing
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_reopen_non_closed_finding_is_409_no_write() -> None:
    reader = _reader_with_finding("detected")  # reopen requires closed
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:reopen", headers=AUTH)
        assert resp.status_code == 409
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- 401 unauthenticated -----------------------------------------------------

def test_unauthenticated_finding_command_is_401() -> None:
    store = FakeProjectionStore()
    app.dependency_overrides[get_projection_store] = lambda: store
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:acknowledge")
        assert resp.status_code == 401
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_unauthenticated_notification_command_is_401() -> None:
    notif_repo = FakeNotificationRepo([_notif_row()])
    app.dependency_overrides[get_notification_repo] = lambda: notif_repo
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/notifications/{NOTIF_ID}:dismiss")
        assert resp.status_code == 401
        assert notif_repo.dismissed == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- 404 cross-workspace / missing (existence not leaked) --------------------

def test_finding_command_out_of_workspace_is_404() -> None:
    reader = _reader_with_finding("detected")
    # the finding's project is in WORKSPACE; the caller is in another workspace
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])
    principal = Principal(user_id="u-1", workspace_id="ws-OTHER", role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/findings/{FINDING_ID}:acknowledge", headers=AUTH)
        assert resp.status_code == 404
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_finding_command_missing_is_404() -> None:
    reader = _reader_with_finding("detected")
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/findings/does-not-exist:acknowledge", headers=AUTH)
        assert resp.status_code == 404
        assert store.upserts == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_notification_command_out_of_workspace_is_404() -> None:
    reader = _reader_with_finding("detected")
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([_notif_row()])  # workspace = WORKSPACE
    principal = Principal(user_id="u-1", workspace_id="ws-OTHER", role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/notifications/{NOTIF_ID}:view", headers=AUTH)
        assert resp.status_code == 404
        assert notif_repo.viewed == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_notification_command_missing_is_404() -> None:
    reader = _reader_with_finding("detected")
    store = FakeProjectionStore()
    notif_repo = FakeNotificationRepo([])  # empty
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, store, notif_repo, CapturingEmitter(), principal)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/notifications/missing:view", headers=AUTH)
        assert resp.status_code == 404
        assert notif_repo.viewed == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- read routers stay GET-only (no regression) ------------------------------

def _read_routers():
    read_tags = {
        "projects", "analysis_runs", "findings", "recommendations",
        "confidence", "acceptance", "notifications",
    }
    return [
        r for r in v1_router.routes
        if getattr(r, "path", "").startswith("/v1")
        and set(getattr(r, "tags", []) or []) & read_tags
    ]


def test_read_routers_stay_get_only_after_finding_notification_commands_added() -> None:
    """Adding the command routers makes no GET read route mutating.

    The GET findings/notifications read routers (tags ``findings``/``notifications``)
    stay GET-only; the lifecycle/state commands live on the separate command routers.
    """
    mutating = {"PUT", "PATCH", "DELETE"}
    for route in _read_routers():
        methods = set(getattr(route, "methods", set()))
        tags = getattr(route, "tags", []) or []
        if "findings" in tags or "notifications" in tags:
            assert "POST" not in methods, (
                f"{route.path} (READ router) exposes POST — the command affordance "
                "must live on the separate command router"
            )
        assert not (methods & mutating)

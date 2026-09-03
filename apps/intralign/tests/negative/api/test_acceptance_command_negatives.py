"""Acceptance-command negatives (DTM-0033) — the Critical epistemic guards.

- **Mandatory version_pin** — a recommendation with NO current CHR cannot be
  accepted: the existing ``AcceptanceRecordingError`` path rejects it and NO
  UAR is written (no unpinned acceptance record ever exists).
- **OSLO never self-accepts** — the actor is ALWAYS ``Principal.user_id``; the
  command exposes no server-initiated / auto accept, and a missing bearer is 401
  (there is no path to an OSLO-authored acceptance).
- **reject / defer write NO plan fact** — only the UAR (the user's action) is
  recorded; nothing is confirmed as factual.
- 401 unauthenticated · 404 cross-workspace (existence not leaked, §12).
- The command never marks the recommendation "true" / world-truth and the read
  router stays GET-only.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_acceptance_chr_reader,
    get_materializer,
    get_projection_reader,
    get_retention_store,
    get_trigger_submitter,
    reset_idempotency_store,
)
from backend.api.v1 import router as v1_router
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader
from tests.positive.api.test_acceptance_commands import (
    REC_ID,
    FakeChrReader,
    FakeRetentionStore,
    FakeSubmitter,
)

AUTH = {"Authorization": "Bearer t"}


def _reader_with_rec(
    project_id: str, workspace_id: str, *, current_chr_ref: str | None = "chr-1"
) -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": project_id, "workspace_id": workspace_id,
        "lifecycle_state": "oriented", "title": "p",
    })
    row = {
        "projection_id": REC_ID,
        "project_id": project_id,
        "output_kind": "recommendation",
        "current_payload": {
            "recommendation_id": REC_ID, "anchor": "f-1",
            "recommendation_type": "candidate_improvement",
            "summary": "Clarify scope.", "state": "generated",
        },
        "current_chr_ref": current_chr_ref,
        "epistemic_label": "derived",
        "confidence_value": 60.0, "confidence_band": "medium",
        "conflict_state": "none", "recomputed_at": "2026-06-25T00:00:00Z",
    }
    r.projections.setdefault("recommendation", []).append(row)
    return r


def _wire(reader: FakeReader, principal: Principal, store: FakeRetentionStore) -> None:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_retention_store] = lambda: store
    app.dependency_overrides[get_acceptance_chr_reader] = lambda: FakeChrReader()
    app.dependency_overrides[get_trigger_submitter] = lambda: FakeSubmitter()
    app.dependency_overrides[get_materializer] = lambda: object()


# ---- mandatory version_pin (Critical) ---------------------------------------

def test_accept_without_current_chr_is_rejected_no_unpinned_uar() -> None:
    """A recommendation with NO current CHR has no version_pin → rejected; NO UAR.

    The mandatory-pin invariant: a User Acceptance Record must pin the exact
    emission accepted (the existing AcceptanceRecordingError path). No unpinned
    acceptance is ever written.
    """
    reader = _reader_with_rec(PROJECT, WORKSPACE, current_chr_ref=None)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
        assert resp.status_code == 422  # unprocessable — no version to pin
        assert store.acceptances == []  # NO unpinned UAR was written
        assert store.assertions == []  # and certainly no plan fact
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- OSLO never self-accepts (Critical) -------------------------------------

def test_unauthenticated_accept_is_401_no_self_accept() -> None:
    """No bearer ⇒ 401. There is no server-initiated/auto accept — acceptance
    REQUIRES an authenticated user actor (OSLO never self-accepts)."""
    store = FakeRetentionStore()
    app.dependency_overrides[get_retention_store] = lambda: store
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/recommendations/{REC_ID}:accept")
        assert resp.status_code == 401
        assert store.acceptances == []  # nothing recorded without a user actor
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_actor_is_always_the_principal_user() -> None:
    """The recorded actor is the authenticated Principal — never OSLO/the server."""
    reader = _reader_with_rec(PROJECT, WORKSPACE)
    principal = Principal(user_id="alice", workspace_id=WORKSPACE, role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
        assert resp.status_code == 200
        assert store.acceptances[0]["user_id"] == "alice"
        assert store.acceptances[0]["created_by"] == "alice"
        # the plan fact, too, is attributed to the user — never OSLO-authored
        assert store.assertions[0]["attesting_source"] == "alice"
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_command_never_marks_recommendation_world_true() -> None:
    """No UAR/plan-fact field marks the recommendation true/approved/world-truth.

    The recording is a HUMAN DECISION only (DL-043 amendment 4) — the only state
    is the user-action + version_pin; nothing flags the item canonical-as-truth.
    """
    reader = _reader_with_rec(PROJECT, WORKSPACE)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    try:
        with TestClient(app) as c:
            c.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
        uar = store.acceptances[0]
        banned = {"approved", "true", "is_true", "world_truth", "canonical", "governed"}
        assert not (banned & set(uar.keys()))
        # the plan fact records the user-attested content, not OSLO-promotion
        assert store.assertions[0]["epistemic_state"] == "attested-user"
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- workspace scoping (404) -------------------------------------------------

def test_accept_on_out_of_workspace_recommendation_is_404() -> None:
    reader = _reader_with_rec("p-other", "ws-OTHER")
    principal = Principal(user_id="u-1", workspace_id="ws-1", role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    try:
        with TestClient(app) as c:
            resp = c.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
        assert resp.status_code == 404
        assert store.acceptances == []  # nothing recorded for an out-of-scope rec
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_accept_on_missing_recommendation_is_404() -> None:
    reader = _reader_with_rec(PROJECT, WORKSPACE)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    try:
        with TestClient(app) as c:
            resp = c.post("/v1/recommendations/does-not-exist:accept", headers=AUTH)
        assert resp.status_code == 404
        assert store.acceptances == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- reject / defer write NO plan fact (Critical) ---------------------------

def test_reject_and_defer_write_no_plan_fact() -> None:
    for action in ("reject", "defer"):
        reader = _reader_with_rec(PROJECT, WORKSPACE)
        principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
        store = FakeRetentionStore()
        _wire(reader, principal, store)
        try:
            with TestClient(app) as c:
                resp = c.post(f"/v1/recommendations/{REC_ID}:{action}", headers=AUTH)
            assert resp.status_code == 200
            assert len(store.acceptances) == 1  # the UAR records the action
            assert store.assertions == []  # but NO plan fact is confirmed
        finally:
            app.dependency_overrides.clear()
            reset_idempotency_store()


# ---- purity: the command wires record_acceptance (no reimplemented logic) ----

def test_command_router_wires_record_acceptance_only() -> None:
    """The router calls record_acceptance; it reimplements no UAR/plan-fact write."""
    import inspect

    from backend.api.v1.routers import acceptance_commands

    src = inspect.getsource(acceptance_commands)
    assert "record_acceptance" in src
    # it does NOT reach into the canonical stores directly to author records
    assert "insert_assertion" not in src
    assert "insert_acceptance" not in src


# ---- read surface stays GET-only (no regression) ----------------------------

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


def test_read_routers_stay_get_only_after_acceptance_commands_added() -> None:
    """Adding the acceptance command router does not make any read route mutating.

    The GET recommendations read router (tag ``recommendations``) stays GET-only;
    the accept/reject/defer/implement commands live on their own command router.
    """
    mutating = {"PUT", "PATCH", "DELETE"}
    for route in _read_routers():
        methods = set(getattr(route, "methods", set()))
        # the GET recommendations read router exposes no POST/PUT/PATCH/DELETE
        if "recommendations" in (getattr(route, "tags", []) or []):
            assert "POST" not in methods, (
                f"{route.path} (recommendations READ router) exposes POST — the "
                "command affordance must live on the separate command router"
            )
        assert not (methods & mutating)


def test_idempotency_replays_same_uar_no_double_write() -> None:
    reader = _reader_with_rec(PROJECT, WORKSPACE)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    store = FakeRetentionStore()
    _wire(reader, principal, store)
    headers = {**AUTH, "Idempotency-Key": "neg-acc-1"}
    try:
        with TestClient(app) as c:
            first = c.post(f"/v1/recommendations/{REC_ID}:accept", headers=headers)
            second = c.post(f"/v1/recommendations/{REC_ID}:accept", headers=headers)
        assert first.json()["recommendation_id"] == second.json()["recommendation_id"]
        assert len(store.acceptances) == 1  # the retry wrote no second UAR
        assert len(store.assertions) == 1
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()

"""Acceptance-command endpoints (DTM-0033) — :accept / :reject / :defer / :implement.

The command router wires the EXISTING ``record_acceptance`` retain seam — it
invents no acceptance logic. Each command:

- resolves the recommendation's CURRENT CHR as the mandatory ``version_pin``,
- builds an ``AcceptanceCapture`` (action + target_kind=recommendation + the
  authenticated user as actor + version_pin),
- calls ``record_acceptance`` (the UAR always; the plan fact on ``accept`` ONLY),
- returns the affected ``Recommendation`` DTO (state per DL-055),
- emits the Event-Model §8 event verbatim
  (``recommendation_accepted/rejected/deferred/implemented``).

``:implement`` ALSO triggers a Deep recompute via ``submit_trigger`` (materializer
injected, DTM-0032) — implementation is new evidence. ``Idempotency-Key`` returns
the SAME UAR on retry; every path is workspace-scoped via ``current_principal``.

OSLO NEVER self-accepts: the actor is always ``Principal.user_id`` — there is no
server-initiated/auto accept, and the command never marks the rec "true".
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_acceptance_chr_reader,
    get_event_emitter,
    get_materializer,
    get_projection_reader,
    get_retention_store,
    get_trigger_submitter,
    reset_idempotency_store,
)
from backend.responsibilities.perceive.acceptance_capture import AcceptanceCapture
from tests.positive.api.conftest import AUTH, FakeReader

REC_ID = "r-1"
REC_CHR = "chr-1"  # the recommendation projection's current_chr_ref (the pin)


class FakeRetentionStore:
    """In-memory append-only retention store (mirrors the insert_* write API).

    Captures every UAR and plan-fact INSERT so the test can assert what
    ``record_acceptance`` wrote (and what it did NOT write on reject/defer).
    """

    def __init__(self) -> None:
        self.acceptances: list[dict[str, Any]] = []
        self.assertions: list[dict[str, Any]] = []
        self.history: list[dict[str, Any]] = []

    def insert_acceptance(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("uar_id", f"uar-{len(self.acceptances) + 1}")
        self.acceptances.append(stored)
        return stored

    def insert_assertion(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("assertion_id", f"pf-{len(self.assertions) + 1}")
        self.assertions.append(stored)
        return stored

    def insert_history(self, row: dict[str, Any]) -> dict[str, Any]:
        stored = dict(row)
        stored.setdefault("history_id", f"h-{len(self.history) + 1}")
        self.history.append(stored)
        return stored


class FakeChrReader:
    """Reads the pinned CHR's output_payload (the accept plan-fact source)."""

    def __init__(self, payload: dict[str, Any] | None = None) -> None:
        self.payload = payload if payload is not None else {"summary": "Clarify scope."}
        self.requested: list[Any] = []

    def get(self, chr_id: Any) -> dict[str, Any]:
        self.requested.append(chr_id)
        return {"output_payload": self.payload}


class FakeSubmitter:
    """Captures every submit_trigger call (graph + claim + materializer)."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, graph_name: str, trigger: Any, **kwargs: Any) -> Any:
        self.calls.append({"graph_name": graph_name, "trigger": trigger, "kwargs": kwargs})
        return object()


SENTINEL_MATERIALIZER = object()


@pytest.fixture
def store() -> FakeRetentionStore:
    return FakeRetentionStore()


@pytest.fixture
def chr_reader() -> FakeChrReader:
    return FakeChrReader()


@pytest.fixture
def submitter() -> FakeSubmitter:
    return FakeSubmitter()


@pytest.fixture
def acc_client(
    reader: FakeReader,
    principal: Principal,
    store: FakeRetentionStore,
    chr_reader: FakeChrReader,
    submitter: FakeSubmitter,
) -> TestClient:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_retention_store] = lambda: store
    app.dependency_overrides[get_acceptance_chr_reader] = lambda: chr_reader
    app.dependency_overrides[get_trigger_submitter] = lambda: submitter
    app.dependency_overrides[get_materializer] = lambda: SENTINEL_MATERIALIZER
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    reset_idempotency_store()


# ---- :accept -----------------------------------------------------------------

def test_accept_writes_uar_and_plan_fact_and_returns_dto(
    acc_client: TestClient, store: FakeRetentionStore
) -> None:
    resp = acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["recommendation_id"] == REC_ID
    assert body["status"] == "accepted"  # DL-055 state per the action just recorded
    # the UAR was written, version-pinned to the recommendation's current CHR
    assert len(store.acceptances) == 1
    uar = store.acceptances[0]
    assert uar["action"] == "accept"
    assert uar["target_kind"] == "recommendation"
    assert uar["version_pin"] == REC_CHR
    assert uar["user_id"] == "u-1"  # the actor is the authenticated user
    # the plan fact was ALSO written (accept only)
    assert len(store.assertions) == 1
    assert store.assertions[0]["attesting_source"] == "u-1"


def test_accept_capture_carries_user_actor_and_version_pin(
    acc_client: TestClient, store: FakeRetentionStore
) -> None:
    """The capture is built FROM the Principal — the actor is the user, never OSLO."""
    acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
    uar = store.acceptances[0]
    assert uar["created_by"] == "u-1"
    assert uar["epistemic_state"] == "attested-user"
    assert uar["version_pin"] == REC_CHR  # the recommendation's CURRENT CHR


def test_accept_emits_recommendation_accepted(acc_client: TestClient) -> None:
    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "recommendation_accepted" in captured


# ---- :reject / :defer (UAR only — NO plan fact) ------------------------------

def test_reject_writes_uar_only_no_plan_fact(
    acc_client: TestClient, store: FakeRetentionStore
) -> None:
    resp = acc_client.post(f"/v1/recommendations/{REC_ID}:reject", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"
    assert len(store.acceptances) == 1
    assert store.acceptances[0]["action"] == "reject"
    assert store.assertions == []  # NO plan fact on reject


def test_defer_writes_uar_only_no_plan_fact(
    acc_client: TestClient, store: FakeRetentionStore
) -> None:
    resp = acc_client.post(f"/v1/recommendations/{REC_ID}:defer", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["status"] == "deferred"
    assert len(store.acceptances) == 1
    assert store.acceptances[0]["action"] == "defer"
    assert store.assertions == []  # NO plan fact on defer


def test_reject_emits_recommendation_rejected(acc_client: TestClient) -> None:
    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        acc_client.post(f"/v1/recommendations/{REC_ID}:reject", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "recommendation_rejected" in captured


def test_defer_emits_recommendation_deferred(acc_client: TestClient) -> None:
    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        acc_client.post(f"/v1/recommendations/{REC_ID}:defer", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "recommendation_deferred" in captured


# ---- :implement (UAR + Deep recompute) ---------------------------------------

def test_implement_writes_uar_and_triggers_deep_recompute(
    acc_client: TestClient, store: FakeRetentionStore, submitter: FakeSubmitter
) -> None:
    resp = acc_client.post(f"/v1/recommendations/{REC_ID}:implement", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["status"] == "implemented"
    # a UAR was recorded (implement is a user action)
    assert len(store.acceptances) == 1
    assert store.acceptances[0]["action"] == "implement"
    # DL-055: implementation is new evidence → a Deep recompute is triggered
    assert len(submitter.calls) == 1
    call = submitter.calls[0]
    assert call["graph_name"] == "deep_pass"
    assert call["kwargs"].get("materializer") is SENTINEL_MATERIALIZER
    # implement records the UAR but writes NO plan fact (accept-only behavior)
    assert store.assertions == []


def test_implement_emits_recommendation_implemented(acc_client: TestClient) -> None:
    captured: list[str] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append(name)

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        acc_client.post(f"/v1/recommendations/{REC_ID}:implement", headers=AUTH)
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    assert "recommendation_implemented" in captured


# ---- version_pin resolution --------------------------------------------------

def test_version_pin_resolved_from_current_chr(
    acc_client: TestClient, store: FakeRetentionStore, chr_reader: FakeChrReader
) -> None:
    """The pin is the recommendation's CURRENT CHR (its projection current_chr_ref)."""
    acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
    assert store.acceptances[0]["version_pin"] == REC_CHR
    # the accept plan fact reads that pinned CHR's payload (a data read, no LLM)
    assert chr_reader.requested == [REC_CHR]


# ---- idempotency -------------------------------------------------------------

def test_idempotency_key_returns_same_uar(
    acc_client: TestClient, store: FakeRetentionStore
) -> None:
    headers = {**AUTH, "Idempotency-Key": "acc-1"}
    first = acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=headers)
    second = acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=headers)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["recommendation_id"] == second.json()["recommendation_id"]
    # the retry wrote NO second UAR / plan fact
    assert len(store.acceptances) == 1
    assert len(store.assertions) == 1


def test_capture_is_an_acceptance_capture_with_recommendation_target(
    acc_client: TestClient, store: FakeRetentionStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The router builds an AcceptanceCapture (target_kind=recommendation) and hands
    it to record_acceptance — it invents no acceptance logic."""
    seen: list[Any] = []
    import backend.api.v1.routers.acceptance_commands as mod

    real = mod.record_acceptance

    def spy(capture: Any, **kwargs: Any) -> Any:
        seen.append(capture)
        return real(capture, **kwargs)

    monkeypatch.setattr(mod, "record_acceptance", spy)
    acc_client.post(f"/v1/recommendations/{REC_ID}:accept", headers=AUTH)
    assert len(seen) == 1
    capture = seen[0]
    assert isinstance(capture, AcceptanceCapture)
    assert capture.action == "accept"
    assert capture.target_kind == "recommendation"
    assert capture.version_pin == REC_CHR
    assert capture.user_id == "u-1"

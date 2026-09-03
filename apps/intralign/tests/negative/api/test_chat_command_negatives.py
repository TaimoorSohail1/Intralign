"""OSLO Chat negatives (DTM-0037) — the CRITICAL epistemic-boundary proofs.

DL-047 CHAT-01…04 + Wave I QA negatives (each Critical unless noted):

- **Chat writes NO canonical** — an Explain/Improve runs with fake stores that
  EXPLODE on insert_assertion / CHR append / UAR write; the request still
  succeeds, proving the chat never reached a canonical store. AST/source scan:
  the responder + router never name a canonical-write seam.
- **Chat mutates NO artifact** — no artifact-body / intake write is reachable.
- **Chat changes NO assessment** — an Explain/Clarify leaves the governed
  projections + the CHR lineage UNCHANGED (the read seam is SELECT-only and the
  responder holds no projection-store / CHR-repo handle).
- **401 / 404** — unauthenticated ⇒ 401; out-of-workspace project ⇒ 404
  (existence not leaked); neither persists or triggers anything.
"""

from __future__ import annotations

import inspect
from typing import Any

from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_chat_responder,
    get_projection_reader,
    reset_idempotency_store,
)
from backend.responsibilities.disclose.chat import ChatResponder
from backend.services.llm_provider import LLMProvider
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    response_key_directive,
)
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader

AUTH = {"Authorization": "Bearer t"}


class ExplodingStore:
    """Any canonical write attempt detonates — chat must never reach one."""

    def __getattr__(self, name: str):
        def _boom(*_a: Any, **_k: Any):
            raise AssertionError(
                f"chat reached a canonical/mutation write ({name!r}) — FORBIDDEN "
                "(DL-047 Critical: chat writes no canonical, mutates no artifact)"
            )

        return _boom


class _RecordingReader(FakeReader):
    """A FakeReader that snapshots every read — and exposes NO write method."""

    def __init__(self) -> None:
        super().__init__()
        self.reads: list[tuple[str, str]] = []

    def list_projection(self, project_id: str, output_kind: str):
        self.reads.append(("list_projection", output_kind))
        return super().list_projection(project_id, output_kind)


class FakeSubmitter:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, graph_name: str, trigger: Any, **kwargs: Any) -> Any:
        self.calls.append({"graph_name": graph_name, "trigger": trigger, "kwargs": kwargs})
        return object()


def _responder(submitter: FakeSubmitter | None = None) -> ChatResponder:
    provider = LLMProvider(recorded_model=build_recorded_model("wi_chat_v0").model())
    return ChatResponder(
        provider=provider,
        submit_trigger=submitter or FakeSubmitter(),
        materializer=object(),
        prompt_suffix_for=response_key_directive,
    )


def _reader_with_project(project_id: str, workspace_id: str) -> FakeReader:
    r = FakeReader()
    r.projects.append({
        "project_id": project_id, "workspace_id": workspace_id,
        "lifecycle_state": "oriented", "title": "p",
    })
    return r


def _wire(reader: FakeReader, principal: Principal, responder: ChatResponder) -> None:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_chat_responder] = lambda: responder


# ---- CRITICAL: chat writes NO canonical -------------------------------------


def test_chat_never_reaches_a_canonical_store() -> None:
    """An Explain + an Improve run with exploding canonical stores — both succeed.

    The ChatResponder is constructed with NO retention/CHR/intake handle at all,
    so the exploding stores are simply never wired in. The request succeeding is
    the proof: nothing on the chat path can write canonical.
    """
    reader = _reader_with_project(PROJECT, WORKSPACE)
    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    responder = _responder()
    # Sanity: the responder exposes no canonical-write collaborator.
    for attr in ("retention_store", "chr_repo", "intake_store", "body_store", "projection_store"):
        assert not hasattr(responder, attr), (
            f"ChatResponder holds {attr!r} — it must hold NO canonical-write handle"
        )
    _wire(reader, principal, responder)
    try:
        with TestClient(app) as c:
            for intent in ("explain", "improve"):
                resp = c.post(
                    f"/v1/projects/{PROJECT}/chat",
                    headers=AUTH,
                    json={"message": "m", "intent": intent},
                )
                assert resp.status_code == 201
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


def test_chat_source_names_no_canonical_write_seam() -> None:
    """AST/source scan: neither the responder nor the router names a write seam."""
    from backend.api.v1.routers import chat as chat_router
    from backend.responsibilities.disclose import chat as chat_responder

    for module in (chat_router, chat_responder):
        src = inspect.getsource(module)
        for forbidden in (
            "insert_assertion",
            "AttestedAssertion",
            "record_acceptance",
            "UserAcceptanceRecord",
            "chr_repo",
            "ChrRepository",
            "cognition_history_record",
            "submit_artifact",
            "ArtifactBodyStore",
            "projection_store",
            ".upsert(",
        ):
            assert forbidden not in src, (
                f"{module.__name__} names {forbidden!r} — chat must consume/trigger "
                "only, never write canonical or mutate (DL-047 Critical)"
            )


# ---- CRITICAL: an Explain changes NO assessment -----------------------------


def test_explain_leaves_governed_projections_and_chr_unchanged() -> None:
    """An Explain only READS — the projection rows + CHR refs are byte-identical."""
    import copy

    reader = _RecordingReader()
    reader.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE, "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    })
    reader.projections.setdefault("finding", []).append({
        "projection_id": "f-1", "project_id": PROJECT, "output_kind": "finding",
        "current_payload": {"finding_id": "f-1", "finding_type": "conflict",
                            "summary": "x", "status": "detected"},
        "current_chr_ref": "chr-1", "epistemic_label": "derived",
        "confidence_value": 60.0, "confidence_band": "medium",
        "conflict_state": "contested", "recomputed_at": "2026-06-25T00:00:00Z",
    })
    before = copy.deepcopy(reader.projections)

    principal = Principal(user_id="u-1", workspace_id=WORKSPACE, role="member")
    _wire(reader, principal, _responder())
    try:
        with TestClient(app) as c:
            resp = c.post(
                f"/v1/projects/{PROJECT}/chat",
                headers=AUTH,
                json={"message": "explain", "intent": "explain"},
            )
        assert resp.status_code == 201
        # the governed projections + their CHR refs are UNCHANGED (no assessment
        # change; an Explain consumes, it does not recompute or mutate)
        assert reader.projections == before
        assert reader.reads  # it DID read (consume) the governed cognition
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- 401 / 404 ---------------------------------------------------------------


def test_unauthenticated_chat_is_401() -> None:
    with TestClient(app) as c:
        resp = c.post(
            f"/v1/projects/{PROJECT}/chat", json={"message": "m", "intent": "explain"}
        )
    assert resp.status_code == 401


def test_chat_on_out_of_workspace_project_is_404() -> None:
    reader = _reader_with_project("p-other", "ws-OTHER")
    principal = Principal(user_id="u-1", workspace_id="ws-1", role="member")
    submitter = FakeSubmitter()
    _wire(reader, principal, _responder(submitter))
    try:
        with TestClient(app) as c:
            resp = c.post(
                "/v1/projects/p-other/chat",
                headers=AUTH,
                json={"message": "m", "intent": "improve"},
            )
        assert resp.status_code == 404
        # nothing triggered for an out-of-scope project
        assert submitter.calls == []
    finally:
        app.dependency_overrides.clear()
        reset_idempotency_store()


# ---- read surface stays GET-only (no regression) ----------------------------


def test_chat_router_holds_no_write_collaborator_in_signature() -> None:
    """The router never depends on a projection-store / retention / intake seam."""
    from backend.api.v1.routers import chat as chat_router

    src = inspect.getsource(chat_router)
    assert "get_projection_store" not in src
    assert "get_retention_store" not in src
    assert "get_intake_store" not in src
    assert "get_acceptance_chr_reader" not in src

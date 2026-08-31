"""OSLO Chat endpoint (DTM-0037) — POST /v1/projects/{pid}/chat.

DL-047 CHAT-01…04 (Disclose-class interaction surface). Each request:

- Intent **Explain / Clarify / Resolve** = CONSUME existing cognition (read the
  governed projections via the read seam) + an LLM-PHRASED response (fixture in
  CI, ADR-0004 — zero provider calls), with the launching object's context
  INHERITED into the exchange.
- Intent **Improve** = TRIGGER cognition: build a ``TriggerClaim`` + call the
  EXISTING ``submit_trigger("deep_pass", …)`` seam with the DTM-0030 materializer
  injected (like DTM-0032), then phrase an acknowledgement.

The endpoint returns a NON-CANONICAL ``ChatExchange`` (the user message + OSLO's
response + inherited context) and emits the non-canonical ``chat_exchange``
event. CRITICAL: chat writes NO canonical (no AttestedAssertion / CHR / UAR),
mutates NO artifact, changes NO assessment (the negatives prove it).
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import (
    Principal,
    current_principal,
    get_chat_responder,
    get_event_emitter,
    get_projection_reader,
    reset_idempotency_store,
)
from backend.responsibilities.disclose.chat import ChatResponder
from backend.services.llm_provider import LLMProvider
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    response_key_directive,
)
from tests.positive.api.conftest import AUTH, PROJECT, FakeReader


@pytest.fixture
def chat_session():
    """A recorded-fixture session — proves zero live provider calls in CI."""
    return build_recorded_model("wi_chat_v0")


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
def submitter() -> FakeSubmitter:
    return FakeSubmitter()


@pytest.fixture
def responder(chat_session, submitter: FakeSubmitter) -> ChatResponder:
    """A ChatResponder wired to the recorded fixture + a fake trigger seam.

    The responder CONSUMES cognition through the read seam (injected per request)
    and, for Improve, TRIGGERS via the injected ``submit_trigger`` (materializer
    injected) — it never constructs a real provider or a real run.
    """
    provider = LLMProvider(recorded_model=chat_session.model())
    return ChatResponder(
        provider=provider,
        submit_trigger=submitter,
        materializer=SENTINEL_MATERIALIZER,
        prompt_suffix_for=response_key_directive,
    )


@pytest.fixture
def chat_client(
    reader: FakeReader, principal: Principal, responder: ChatResponder
) -> TestClient:
    reset_idempotency_store()
    app.dependency_overrides[current_principal] = lambda: principal
    app.dependency_overrides[get_projection_reader] = lambda: reader
    app.dependency_overrides[get_chat_responder] = lambda: responder
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    reset_idempotency_store()


# ---- Explain / Clarify / Resolve = consume + phrase --------------------------


def test_explain_returns_a_chat_exchange_with_a_phrased_response(
    chat_client: TestClient,
) -> None:
    resp = chat_client.post(
        f"/v1/projects/{PROJECT}/chat",
        headers=AUTH,
        json={"message": "What is going on with my schedule?", "intent": "explain"},
    )
    assert resp.status_code == 201
    body = resp.json()
    # A ChatExchange (non-canonical interaction record): the user message + OSLO's
    # phrased response, marked non-canonical (NOT attested, NOT derived cognition).
    assert body["project_id"] == PROJECT
    assert body["intent"] == "explain"
    assert body["user_message"] == "What is going on with my schedule?"
    assert body["response"]  # an LLM-phrased response (from the fixture)
    assert body["epistemic_state"] == "non-canonical"


def test_explain_consumes_governed_cognition(
    chat_client: TestClient, chat_session
) -> None:
    """Explain READS the governed projections (the fixture is served, zero live)."""
    resp = chat_client.post(
        f"/v1/projects/{PROJECT}/chat",
        headers=AUTH,
        json={"message": "explain", "intent": "explain"},
    )
    assert resp.status_code == 201
    # the phrasing pass ran entirely on the recorded fixture (no provider call)
    assert chat_session.call_count == 1
    assert chat_session.served_keys == ["explain"]


def test_context_is_inherited_into_the_exchange(chat_client: TestClient) -> None:
    """Launched from a finding/recommendation, the context inherits (CHAT-01)."""
    resp = chat_client.post(
        f"/v1/projects/{PROJECT}/chat",
        headers=AUTH,
        json={
            "message": "clarify this",
            "intent": "clarify",
            "context": {"object_type": "recommendation", "object_id": "r-1"},
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["context"] == {"object_type": "recommendation", "object_id": "r-1"}


def test_clarify_and_resolve_phrase_a_response(chat_client: TestClient) -> None:
    for intent in ("clarify", "resolve"):
        resp = chat_client.post(
            f"/v1/projects/{PROJECT}/chat",
            headers=AUTH,
            json={"message": "m", "intent": intent},
        )
        assert resp.status_code == 201
        assert resp.json()["response"]
        assert resp.json()["triggered_run"] is None  # consume-only, no trigger


# ---- Improve = trigger cognition (submit_trigger + materializer) -------------


def test_improve_calls_submit_trigger_with_claim_and_materializer(
    chat_client: TestClient, submitter: FakeSubmitter
) -> None:
    resp = chat_client.post(
        f"/v1/projects/{PROJECT}/chat",
        headers=AUTH,
        json={"message": "make this better", "intent": "improve"},
    )
    assert resp.status_code == 201
    # Improve triggers the FROZEN cognition path (DTM-0032 pattern) — never a
    # canonical write from chat; the recompute owns its CHR append.
    assert len(submitter.calls) == 1
    call = submitter.calls[0]
    assert call["graph_name"] == "deep_pass"
    from backend.responsibilities.adapt.triggers import TriggerClaim

    assert isinstance(call["trigger"], TriggerClaim)
    assert call["trigger"].project_id == PROJECT
    # the DTM-0030 materializer is injected so derived.*_current materializes
    assert call["kwargs"].get("materializer") is SENTINEL_MATERIALIZER
    # the exchange reports the triggered run id (non-canonical bookkeeping)
    assert resp.json()["triggered_run"] is not None


def test_consume_intents_do_not_trigger(
    chat_client: TestClient, submitter: FakeSubmitter
) -> None:
    for intent in ("explain", "clarify", "resolve"):
        chat_client.post(
            f"/v1/projects/{PROJECT}/chat",
            headers=AUTH,
            json={"message": "m", "intent": intent},
        )
    assert submitter.calls == []  # consume intents never trigger cognition


# ---- the ChatExchange event --------------------------------------------------


def test_chat_emits_the_chat_exchange_event(chat_client: TestClient) -> None:
    captured: list[tuple[str, dict]] = []

    class CapturingEmitter:
        def emit(self, name: str, payload: dict) -> None:
            captured.append((name, dict(payload)))

    app.dependency_overrides[get_event_emitter] = lambda: CapturingEmitter()
    try:
        chat_client.post(
            f"/v1/projects/{PROJECT}/chat",
            headers=AUTH,
            json={"message": "m", "intent": "explain"},
        )
    finally:
        app.dependency_overrides.pop(get_event_emitter, None)
    names = [name for name, _ in captured]
    assert "chat_exchange" in names
    # exactly ONE chat_exchange event, and NO canonical append event
    assert names.count("chat_exchange") == 1
    assert "cognition_history_record_appended" not in names


# ---- idempotency -------------------------------------------------------------


def test_idempotency_key_returns_the_same_exchange(
    chat_client: TestClient, submitter: FakeSubmitter
) -> None:
    headers = {**AUTH, "Idempotency-Key": "chat-k-1"}
    body = {"message": "make this better", "intent": "improve"}
    first = chat_client.post(f"/v1/projects/{PROJECT}/chat", headers=headers, json=body)
    second = chat_client.post(f"/v1/projects/{PROJECT}/chat", headers=headers, json=body)
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["exchange_id"] == second.json()["exchange_id"]
    # the retry did NOT re-trigger cognition
    assert len(submitter.calls) == 1

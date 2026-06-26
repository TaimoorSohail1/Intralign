"""Recorded-fixture harness self-test for the OSLO Chat fixture (DTM-0037; ADR-0004).

NOT a "replay" (reserved — event-log reconstruction that does not re-run the
LLM; CONTEXT.md Register). It lives under tests/replay/ only because that is the
determinism-harness home, and it proves the DTM-0037 Chat phrasing runs ENTIRELY
on recorded responses — PR CI makes ZERO provider calls. Chat answer TEXT is
SEMANTIC (many valid phrasings); the non-canonical exchange SURFACE (the intent,
the inherited context, the triggered-run bookkeeping) is record-exact.
"""

from __future__ import annotations

import sys

from backend.responsibilities.disclose.chat import ChatResponder
from backend.services.llm_provider import LLMProvider, live_calls_enabled
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    load_fixture,
    response_key_directive,
)

_PROJECT = "11111111-1111-1111-1111-111111111111"


class _CapturingSubmitter:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def __call__(self, graph_name, trigger, **kwargs):
        self.calls.append((graph_name, trigger, kwargs))
        return object()


def test_wi_chat_fixture_carries_a_baseline_stamp() -> None:
    fixture = load_fixture("wi_chat_v0")
    assert fixture.model_version
    assert fixture.config
    assert "explain" in fixture.responses
    assert "improve" in fixture.responses


def test_chat_phrasing_runs_entirely_on_recorded_responses() -> None:
    """The chat phrasing serves recorded output — zero live provider calls."""
    session = build_recorded_model("wi_chat_v0")
    provider = LLMProvider(recorded_model=session.model())
    responder = ChatResponder(
        provider=provider,
        submit_trigger=_CapturingSubmitter(),
        materializer=object(),
        prompt_suffix_for=response_key_directive,
    )
    before = set(sys.modules)
    governed = {"finding": [{"finding_id": "f-1", "summary": "conflict on Q3 date"}]}
    exchange = responder.respond(
        project_id=_PROJECT,
        message="explain my schedule",
        intent="explain",
        governed=governed,
        context=None,
    )
    assert session.call_count == 1
    assert session.served_keys == ["explain"]
    # Record-exact axis: the non-canonical exchange surface.
    assert exchange.intent == "explain"
    assert exchange.triggered_run is None
    assert exchange.response  # SEMANTIC text, never byte-pinned
    # No provider SDK imported by exercising the harness.
    newly = set(sys.modules) - before
    assert not any(
        m.startswith(("pydantic_ai.models.openai", "pydantic_ai.models.anthropic"))
        for m in newly
    )


def test_chat_improve_triggers_and_serves_the_improve_response() -> None:
    session = build_recorded_model("wi_chat_v0")
    provider = LLMProvider(recorded_model=session.model())
    submitter = _CapturingSubmitter()
    responder = ChatResponder(
        provider=provider,
        submit_trigger=submitter,
        materializer=object(),
        prompt_suffix_for=response_key_directive,
    )
    exchange = responder.respond(
        project_id=_PROJECT, message="improve", intent="improve", governed={}, context=None
    )
    assert len(submitter.calls) == 1
    assert submitter.calls[0][0] == "deep_pass"
    assert exchange.triggered_run is not None
    assert session.served_keys == ["improve"]


def test_pr_ci_never_enables_live_calls() -> None:
    assert not live_calls_enabled()

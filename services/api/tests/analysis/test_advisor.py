import json
from types import SimpleNamespace
from uuid import UUID

import pytest

from oslo_api.analysis import (
    AnalysisRunRequest,
    AnalysisWorkflow,
    DeterministicAgentHarness,
    InMemoryAnalysisStore,
    RunKind,
)
from oslo_api.analysis.advisor import OpenAIProjectAdvisor, ProjectAdvisorError

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")


class FakeResponses:
    def __init__(self) -> None:
        self.requests: list[dict] = []

    def parse(self, **kwargs):
        self.requests.append(kwargs)
        return SimpleNamespace(
            output_parsed=kwargs["text_format"].model_validate(
                {
                    "answer": "Confirm the accountable owner and contingency first.",
                    "follow_up_questions": ["Who owns the dependency?"],
                }
            )
        )


class FakeOpenAI:
    def __init__(self) -> None:
        self.responses = FakeResponses()


class FailingResponses:
    def parse(self, **kwargs):
        del kwargs
        raise RuntimeError("Sensitive provider detail")


class FailingOpenAI:
    def __init__(self) -> None:
        self.responses = FailingResponses()


def completed_snapshot():
    store = InMemoryAnalysisStore()
    result = AnalysisWorkflow(
        store=store,
        harness=DeterministicAgentHarness(),
    ).run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.INITIAL,
            description="The project has an unresolved critical dependency.",
            source_names=(),
            idempotency_key="advisor-snapshot-001",
        )
    )
    assert result.snapshot is not None
    return result.snapshot


def test_live_advisor_uses_a_bounded_structured_project_snapshot() -> None:
    client = FakeOpenAI()
    advisor = OpenAIProjectAdvisor(
        api_key="not-used-by-the-fake",
        model="gpt-test",
        client=client,
    )

    reply = advisor.answer(
        snapshot=completed_snapshot(),
        question="What should I address first?",
    )

    request = client.responses.requests[0]
    payload = json.loads(request["input"][1]["content"])
    assert request["model"] == "gpt-test"
    assert request["max_output_tokens"] == 1_200
    assert payload["question"] == "What should I address first?"
    assert payload["project_snapshot"]["assessment"]["issues"]
    assert "confidence_index" not in payload["project_snapshot"]["assessment"]
    assert "numeric confidence" in request["input"][0]["content"]
    assert payload["project_snapshot"]["artifacts"][0]["sections"]
    assert "body" in payload["project_snapshot"]["artifacts"][0]["sections"][0]
    assert "assumptions" in payload["project_snapshot"]["artifacts"][0]
    assert "evidence_citations" in payload["project_snapshot"]
    assert "API" not in request["input"][0]["content"]
    assert reply.answer == "Confirm the accountable owner and contingency first."
    assert reply.follow_up_questions == ("Who owns the dependency?",)


def test_provider_failure_returns_only_a_safe_advisor_error() -> None:
    advisor = OpenAIProjectAdvisor(
        api_key="not-used-by-the-fake",
        model="gpt-test",
        client=FailingOpenAI(),
    )

    with pytest.raises(ProjectAdvisorError) as raised:
        advisor.answer(
            snapshot=completed_snapshot(),
            question="What should I address first?",
        )

    assert str(raised.value) == "PROJECT_ADVISOR_UNAVAILABLE"
    assert "Sensitive" not in str(raised.value)

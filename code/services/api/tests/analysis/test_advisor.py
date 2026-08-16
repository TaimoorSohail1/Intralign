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
from oslo_api.analysis.advisor import (
    GroundedProjectAdvisor,
    OpenAIProjectAdvisor,
    ProjectAdvisorError,
    with_current_issue_lifecycle,
)
from oslo_api.analysis.models import EvidenceFragment

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


def atlas_budget_snapshot():
    evidence = (
        EvidenceFragment(
            reference="atlas:charter:page:1",
            source_name="01_executive_charter_and_benefits.pdf",
            location="Page 1",
            content=(
                "The approved funding ceiling is GBP 1,800,000, including GBP 120,000 "
                "management contingency."
            ),
        ),
        EvidenceFragment(
            reference="atlas:raid:page:1",
            source_name="05_raid_status_change_decisions.pdf",
            location="Page 1",
            content=(
                "Forecast at completion is GBP 1,845,000 against the approved GBP "
                "1,800,000 ceiling. The GBP 45,000 forecast variance is not approved. "
                "DEC-03 Approve GBP 45,000 funding action Steering Committee 03 Sep 2026 Pending."
            ),
        ),
    )
    result = AnalysisWorkflow(
        store=InMemoryAnalysisStore(),
        harness=DeterministicAgentHarness(),
    ).run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.EXTENDED,
            description="",
            source_names=tuple(item.source_name or "" for item in evidence),
            user_evidence=evidence,
            idempotency_key="advisor-atlas-budget-001",
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


def test_grounded_fallback_answers_from_the_current_snapshot() -> None:
    reply = GroundedProjectAdvisor().answer(
        snapshot=completed_snapshot(),
        question="What should I address first?",
    )

    assert reply.answer
    assert "current read" in reply.answer.lower()
    assert reply.follow_up_questions


def test_grounded_fallback_does_not_recommend_issues_resolved_after_the_snapshot() -> None:
    snapshot = completed_snapshot()
    projected = with_current_issue_lifecycle(
        snapshot,
        [
            {"issue_id": issue.id, "status": "resolved"}
            for issue in snapshot.assessment.issues
        ],
    )

    reply = GroundedProjectAdvisor().answer(
        snapshot=projected,
        question="Explain the Attention map and what I should address first.",
    )

    assert "no open issues" in reply.answer.lower()
    assert reply.follow_up_questions == ()


def test_grounded_fallback_explains_the_issue_named_by_the_workspace() -> None:
    snapshot = atlas_budget_snapshot()
    selected = next(
        issue
        for issue in snapshot.assessment.issues
        if issue.title == "GBP 45,000 forecast variance is not approved"
    )

    reply = GroundedProjectAdvisor().answer(
        snapshot=snapshot,
        question=f"Explain this issue: {selected.title}",
    )

    assert selected.title in reply.answer
    assert selected.recommendation in reply.answer
    assert reply.follow_up_questions == (selected.clarification,)


def test_grounded_fallback_cites_source_evidence_and_next_budget_verification() -> None:
    reply = GroundedProjectAdvisor().answer(
        snapshot=atlas_budget_snapshot(),
        question=(
            "Which source evidence supports the GBP 45,000 budget conflict, "
            "and what should I verify next?"
        ),
    )

    assert "GBP 45,000" in reply.answer
    assert "01_executive_charter_and_benefits.pdf" in reply.answer
    assert "05_raid_status_change_decisions.pdf" in reply.answer
    assert "Steering Committee" in reply.answer
    assert "not approved" in reply.answer

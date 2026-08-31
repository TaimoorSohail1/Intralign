from __future__ import annotations

from oslo_api.analysis.models import EvidenceFragment


def build_clarification_evidence(
    *,
    issue_id: str,
    issue_title: str,
    question: str,
    answer: str,
    answer_key: str,
) -> EvidenceFragment:
    return EvidenceFragment(
        reference=f"user:clarification:{issue_id}:answer:{answer_key}",
        content=(
            f"Issue: {issue_title}\n"
            f"Question: {question}\n"
            f"Answer: {answer.strip()}"
        ),
        source_name="User-confirmed clarification",
        location=f"Issue {issue_id}",
    )


def build_reviewer_evidence(
    *,
    response_key: str,
    reviewer_name: str,
    issue_id: str | None,
    issue_title: str,
    response_kind: str,
    body: str,
) -> EvidenceFragment:
    return EvidenceFragment(
        reference=f"user:review:{response_key}",
        content=(
            f"Reviewer: {reviewer_name}\n"
            f"Issue: {issue_title}\n"
            f"Response type: {response_kind.replace('_', ' ')}\n"
            f"Response: {body.strip()}\n"
            "Reviewer approval and rejection are opposing alignment evidence; "
            "comments and alternatives are reliability evidence."
        ),
        source_name=f"Reviewer response from {reviewer_name}",
        location=f"Issue {issue_id}" if issue_id else "Project-wide review",
    )

from oslo_api.analysis.models import ArtifactType, Issue
from oslo_api.analysis.persistence import _active_issue_keys


def _issue(issue_id: str, status: str) -> Issue:
    return Issue(
        id=issue_id,
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Clarity",
        severity="Moderate",
        title=f"Issue {issue_id}",
        why="The current read needs clarification.",
        recommendation="Confirm the missing evidence.",
        evidence_refs=("document:test:page:1:fragment:1",),
        status=status,
    )


def test_active_issue_keys_only_counts_the_published_open_read() -> None:
    issues = (
        _issue("ISS-OPEN", "open"),
        _issue("ISS-ADDRESSED", "addressed"),
        _issue("ISS-RESOLVED", "resolved"),
    )

    assert _active_issue_keys(issues) == {"ISS-OPEN", "ISS-ADDRESSED"}

from oslo_api.analysis.models import Artifact, ArtifactSection, ArtifactType, Issue
from oslo_api.analysis.persistence import _active_issue_keys, _primary_outcome_title


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


def test_primary_outcome_uses_the_grounded_intent_instead_of_extractor_status_copy() -> None:
    intent = Artifact(
        artifact_type=ArtifactType.INTENT,
        title="Intent",
        summary=(
            "Initial structured intent extracted from Executive summary, Objectives and "
            "success measures, Business case, Sponsorship and authority."
        ),
        reliability="High",
        evidence_refs=("document:charter:page:1:fragment:0",),
        sections=(
            ArtifactSection(
                heading="Executive summary",
                body=(
                    "Atlas Retail Group will launch a self-service B2B commerce portal for "
                    "420 wholesale customers in the United Kingdom and Ireland. The portal "
                    "will support ordering and returns."
                ),
                evidence_refs=("document:charter:page:1:fragment:0",),
            ),
        ),
    )

    assert _primary_outcome_title((intent,)) == (
        "Atlas Retail Group will launch a self-service B2B commerce portal for 420 wholesale "
        "customers in the United Kingdom and Ireland."
    )

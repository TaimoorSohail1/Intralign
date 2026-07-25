from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    Assessment,
    AssessmentSnapshot,
    Issue,
    RunKind,
)
from oslo_api.analysis.understanding import enrich_assessment


def _artifacts() -> tuple[Artifact, ...]:
    return tuple(
        Artifact(
            artifact_type=artifact_type,
            title=artifact_type.value,
            summary=f"Evidence-qualified {artifact_type.value}.",
            reliability="Moderate",
            evidence_refs=(f"document:plan:page:{index}:fragment:0",),
        )
        for index, artifact_type in enumerate(ARTIFACT_TYPES, start=1)
    )


def _assessment(
    *,
    score: int = 58,
    band: str = "Moderate",
    reliability: str = "Moderate",
) -> Assessment:
    return Assessment(
        confidence_index=score,
        confidence_band=band,
        reliability=reliability,
        clarity="High",
        alignment="Moderate",
        feasibility="Low",
        issues=(),
    )


def _snapshot(assessment: Assessment) -> AssessmentSnapshot:
    return AssessmentSnapshot(
        id=uuid4(),
        analysis_run_id=uuid4(),
        workspace_id=uuid4(),
        project_id=uuid4(),
        state="provisional",
        summary="Previous published read.",
        artifacts=_artifacts(),
        assessment=assessment,
        published_at=datetime.now(UTC),
    )


def test_extended_runs_expose_stage_and_evidence_based_direction() -> None:
    previous = _snapshot(_assessment(score=52))

    expanded = enrich_assessment(
        assessment=_assessment(score=58),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description="Run a deeper evidence pass.",
    )
    validated = enrich_assessment(
        assessment=_assessment(score=46),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description="USER_CLARIFICATION: the delivery owner is not appointed.",
    )

    assert expanded.understanding_stage == "expanded"
    assert expanded.confidence_direction == "strengthened"
    assert validated.understanding_stage == "validated"
    assert validated.confidence_direction == "weakened"


def test_high_confidence_with_low_reliability_is_flagged() -> None:
    assessment = enrich_assessment(
        assessment=_assessment(score=84, band="High", reliability="Low"),
        artifacts=_artifacts(),
        kind=RunKind.INITIAL,
        previous_snapshot=None,
        description="A confident claim with weak supporting evidence.",
    )

    assert assessment.false_confidence is True
    assert assessment.limiting_dimension == "feasibility"
    assert assessment.confidence_direction == "unchanged"


def test_open_findings_always_expose_a_clarification_request() -> None:
    issue = Issue(
        id="ISS-MIGRATION",
        artifact_type=ARTIFACT_TYPES[3],
        dimension="Feasibility",
        severity="Critical",
        title="Migration acceptance is unresolved",
        why="No reconciliation threshold is approved.",
        recommendation="Approve reconciliation and rollback criteria.",
        evidence_refs=("document:plan:page:4:fragment:0",),
        clarification=None,
    )

    result = enrich_assessment(
        assessment=replace(_assessment(), issues=(issue,)),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=None,
        description="Run a deeper evidence pass.",
    )

    assert result.issues[0].clarification
    assert "Migration acceptance is unresolved" in result.issues[0].clarification


def test_clarification_reanalysis_keeps_a_repeated_issue_addressed_until_validated() -> None:
    issue = Issue(
        id="ISS-OWNER",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Critical",
        title="Delivery owner is not confirmed",
        why="No accountable owner is named.",
        recommendation="Name the owner and fallback.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery?",
    )
    previous = _snapshot(replace(_assessment(), issues=(issue,)))
    repeated = replace(_assessment(score=60), issues=(issue,))

    result = enrich_assessment(
        assessment=repeated,
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-OWNER\n"
            "Answer: Priya is accountable, but no fallback has been approved."
        ),
    )

    assert result.understanding_stage == "validated"
    assert result.issues[0].status == "addressed"
    assert result.resolved_issue_count == 0


def test_clarification_reanalysis_preserves_resolved_issue_when_model_omits_it() -> None:
    issue = Issue(
        id="ISS-OWNER",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Critical",
        title="Delivery owner is not confirmed",
        why="No accountable owner is named.",
        recommendation="Name the owner and fallback.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery?",
    )
    previous = _snapshot(replace(_assessment(), issues=(issue,)))

    result = enrich_assessment(
        assessment=replace(_assessment(score=66), issues=()),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-OWNER\n"
            "Question: Who owns delivery?\n"
            "Answer: Priya is accountable and Liam is the approved fallback."
        ),
    )

    assert result.issues[0].id == "ISS-OWNER"
    assert result.issues[0].status == "resolved"
    assert result.resolved_issue_count == 1
    assert result.confirmed_dependency_count == 1


def test_complete_user_confirmation_resolves_repeated_issue() -> None:
    issue = Issue(
        id="ISS-OWNER",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Critical",
        title="Delivery owner is not confirmed",
        why="No accountable owner is named.",
        recommendation="Name the owner and fallback.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery and who is the fallback?",
    )
    previous = _snapshot(replace(_assessment(), issues=(issue,)))

    result = enrich_assessment(
        assessment=replace(_assessment(score=66), issues=(issue,)),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-OWNER\n"
            "Question: Who owns delivery and who is the fallback?\n"
            "Answer: Priya Shah is the approved accountable owner from 24 July "
            "2026, and Liam Chen is the approved fallback with delegated authority."
        ),
    )

    assert result.issues[0].status == "resolved"
    assert result.resolved_issue_count == 1


def test_latest_clarification_controls_issue_lifecycle() -> None:
    latest = Issue(
        id="ISS-LATEST",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Critical",
        title="Delivery owner is not confirmed",
        why="No accountable owner is named.",
        recommendation="Name the owner and fallback.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery?",
    )
    previous = _snapshot(replace(_assessment(), issues=(latest,)))

    result = enrich_assessment(
        assessment=replace(_assessment(score=66), issues=(latest,)),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-OLD\nQuestion: Old?\n"
            "Answer: Old answer.\nEND_USER_CLARIFICATION\n\n"
            "USER_CLARIFICATION\nIssue ID: ISS-LATEST\nQuestion: Who owns delivery?\n"
            "Answer: Priya Shah is the approved accountable owner and Liam Chen "
            "is the approved fallback with delegated authority from 24 July 2026.\n"
            "END_USER_CLARIFICATION"
        ),
    )

    assert result.issues[0].id == "ISS-LATEST"
    assert result.issues[0].status == "resolved"

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactSection,
    Assessment,
    AssessmentSnapshot,
    EvidenceFragment,
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


def test_high_coverage_high_reliability_artifacts_cannot_publish_low_reliability() -> None:
    artifacts = tuple(
        replace(artifact, reliability="High")
        for artifact in _artifacts()
    )

    assessment = enrich_assessment(
        assessment=_assessment(reliability="Low"),
        artifacts=artifacts,
        kind=RunKind.EXTENDED,
        previous_snapshot=None,
        description="Run a deeper evidence pass.",
    )

    assert assessment.reliability == "High"
    assert assessment.reliability_basis.coverage == "High"
    assert assessment.reliability_basis.evidence == "High"
    assert assessment.reliability_basis.assessability == "High"
    assert "Reliability is high" in assessment.confidence_explanation


def test_fully_cited_rows_establish_high_reliability_despite_plan_conflicts() -> None:
    artifacts = tuple(
        replace(
            artifact,
            reliability="Moderate",
            sections=(
                ArtifactSection(
                    heading="Evidence",
                    rows=(("Confirmed row",),),
                    row_evidence_refs=(artifact.evidence_refs,),
                ),
            ),
        )
        for artifact in _artifacts()
    )

    assessment = enrich_assessment(
        assessment=_assessment(reliability="Moderate"),
        artifacts=artifacts,
        kind=RunKind.EXTENDED,
        previous_snapshot=None,
        description="A complete but internally conflicting evidence pack.",
    )

    assert assessment.reliability == "High"
    assert assessment.reliability_basis.evidence == "High"
    assert assessment.reliability_basis.assessability == "High"


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


def test_missing_clarified_issue_is_not_resolved_when_reanalysis_splits_it() -> None:
    previous_issue = Issue(
        id="ISS-OWNER",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Critical",
        title="Delivery ownership and fallback are not confirmed",
        why="No accountable owner or fallback is named.",
        recommendation="Name the owner and approved fallback.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery and who is the approved fallback?",
    )
    owner_issue = replace(
        previous_issue,
        id="MODEL-OWNER",
        title="Delivery owner is only partly confirmed",
    )
    fallback_issue = replace(
        previous_issue,
        id="MODEL-FALLBACK",
        title="Delivery fallback is still missing",
    )
    previous = _snapshot(replace(_assessment(), issues=(previous_issue,)))

    result = enrich_assessment(
        assessment=replace(
            _assessment(score=60),
            issues=(owner_issue, fallback_issue),
        ),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-OWNER\n"
            "Answer: Priya owns delivery, but no fallback has been approved."
        ),
    )

    tied = next(issue for issue in result.issues if issue.id == "ISS-OWNER")
    assert tied.status == "addressed"
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


def test_disappeared_issue_remains_open_without_resolution_evidence() -> None:
    issue = Issue(
        id="ISS-OLD",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Feasibility",
        severity="Moderate",
        title="An earlier resource gap",
        why="The previous read could not find an owner.",
        recommendation="Name the owner.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery?",
    )
    previous = _snapshot(replace(_assessment(), issues=(issue,)))

    result = enrich_assessment(
        assessment=replace(_assessment(score=66), issues=()),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description="The new governed read includes an accountable owner.",
    )

    assert result.issues[0].id == "ISS-OLD"
    assert result.issues[0].status == "open"
    assert result.resolved_issue_count == 0


def test_fresh_initial_read_does_not_carry_a_stale_previous_issue() -> None:
    issue = Issue(
        id="ISS-STALE-EDIT",
        artifact_type=ARTIFACT_TYPES[0],
        dimension="Clarity",
        severity="Warning",
        title="A stale user edit is malformed",
        why="The previous draft contained malformed data.",
        recommendation="Correct the draft.",
        evidence_refs=("user:artifact:intent:version:3",),
        clarification="What value should replace the malformed edit?",
    )
    previous = _snapshot(replace(_assessment(), issues=(issue,)))

    result = enrich_assessment(
        assessment=replace(_assessment(), issues=()),
        artifacts=_artifacts(),
        kind=RunKind.INITIAL,
        previous_snapshot=previous,
        description="A fresh complete read of the source documents.",
    )

    assert result.issues == ()


def test_structured_clarification_evidence_updates_only_the_tied_issue() -> None:
    owner_issue = Issue(
        id="ISS-OWNER",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Clarity",
        severity="Critical",
        title="Accountable owner is missing",
        why="No accountable delivery owner is named.",
        recommendation="Name an owner.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns delivery?",
    )
    previous = _snapshot(replace(_assessment(), issues=(owner_issue,)))
    result = enrich_assessment(
        assessment=replace(_assessment(), issues=(owner_issue,)),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description="Project Nova delivery plan.",
        user_evidence=(
            EvidenceFragment(
                reference="user:clarification:ISS-OWNER:answer:answer-1",
                content=(
                    "Issue: Accountable owner is missing\n"
                    "Question: Who owns delivery?\n"
                    "Answer: Priya owns delivery, with Liam as fallback, effective "
                    "1 August 2026 and approved by the sponsor."
                ),
                source_name="User-confirmed clarification",
                location="Issue ISS-OWNER",
            ),
        ),
    )

    issue = next(item for item in result.issues if item.id == "ISS-OWNER")
    assert issue.status == "addressed"
    assert result.understanding_stage == "validated"


def test_clarification_reanalysis_preserves_unrelated_open_issues_when_model_omits_them() -> None:
    answered_issue = Issue(
        id="ISS-PAYMENT",
        artifact_type=ARTIFACT_TYPES[-1],
        dimension="Alignment",
        severity="Warning",
        title="Payment gateway conflicts with launch scope",
        why="The dependency is listed while billing is out of scope.",
        recommendation="Confirm whether payment processing is required.",
        evidence_refs=("document:plan:page:2:fragment:0",),
        clarification="Is payment processing required for launch?",
    )
    unrelated_issue = Issue(
        id="ISS-MILESTONE",
        artifact_type=ARTIFACT_TYPES[-2],
        dimension="Clarity",
        severity="Moderate",
        title="Milestones have no owners or dates",
        why="Named milestones are not tied to accountable owners or calendar dates.",
        recommendation="Assign owners and dated acceptance gates.",
        evidence_refs=("document:plan:page:1:fragment:0",),
        clarification="Who owns each milestone and when is it due?",
    )
    previous = _snapshot(
        replace(_assessment(), issues=(answered_issue, unrelated_issue))
    )

    result = enrich_assessment(
        assessment=replace(_assessment(score=66), issues=()),
        artifacts=_artifacts(),
        kind=RunKind.EXTENDED,
        previous_snapshot=previous,
        description=(
            "USER_CLARIFICATION\nIssue ID: ISS-PAYMENT\n"
            "Question: Is payment processing required for launch?\n"
            "Answer: Payment processing is not required for the initial launch. "
            "Remove the gateway dependency and keep billing out of scope."
        ),
    )

    issues_by_id = {issue.id: issue for issue in result.issues}
    assert issues_by_id["ISS-PAYMENT"].status == "resolved"
    assert issues_by_id["ISS-MILESTONE"].status == "open"


def test_complete_user_confirmation_addresses_a_weakness_still_found_by_analysis() -> None:
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

    assert result.issues[0].status == "addressed"
    assert result.resolved_issue_count == 0


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
    assert result.issues[0].status == "addressed"

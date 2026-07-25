import re
from dataclasses import replace

from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    Assessment,
    AssessmentSnapshot,
    ReliabilityBasis,
    RunKind,
)

_BAND_ORDER = {
    "Very Low": 0,
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Very High": 4,
}


def _latest_clarification(description: str) -> str | None:
    matches = list(
        re.finditer(
            r"^USER_CLARIFICATION[^\n]*\n(?P<body>.*?)"
            r"(?:^END_USER_CLARIFICATION\s*$|\Z)",
            description,
            re.MULTILINE | re.DOTALL,
        )
    )
    return matches[-1].group("body") if matches else None


def enrich_assessment(
    *,
    assessment: Assessment,
    artifacts: tuple[Artifact, ...],
    kind: RunKind,
    previous_snapshot: AssessmentSnapshot | None,
    description: str,
) -> Assessment:
    """Derive the Slice 3 console read from validated, persisted analysis output."""

    basis = _reliability_basis(artifacts)
    limiting_dimension = min(
        ("clarity", "alignment", "feasibility"),
        key=lambda name: _BAND_ORDER.get(getattr(assessment, name), -1),
    )
    stage = (
        "orientation"
        if kind is RunKind.INITIAL
        else "validated"
        if "USER_CLARIFICATION" in description
        else "expanded"
    )
    direction = _confidence_direction(assessment, previous_snapshot)
    false_confidence = (
        assessment.confidence_band in {"High", "Very High"}
        and assessment.reliability == "Low"
    )
    clarification_block = _latest_clarification(description)
    clarification_match = re.search(
        r"^Issue ID:\s*(\S+)\s*$",
        clarification_block or "",
        re.MULTILINE,
    )
    clarification_issue_id = (
        clarification_match.group(1) if clarification_match else None
    )
    complete_confirmation = _complete_user_confirmation(clarification_block)
    issues = [
        replace(
            issue,
            clarification=issue.clarification
            or (
                "What evidence or decision confirms that this issue is addressed: "
                f"{issue.title}?"
            ),
            status=(
                "resolved"
                if issue.id == clarification_issue_id
                and issue.status != "resolved"
                and complete_confirmation
                else "addressed"
                if issue.id == clarification_issue_id
                and issue.status != "resolved"
                else issue.status
            ),
        )
        for issue in assessment.issues
    ]
    if clarification_issue_id and previous_snapshot is not None:
        previous_issue = next(
            (
                issue
                for issue in previous_snapshot.assessment.issues
                if issue.id == clarification_issue_id
            ),
            None,
        )
        if previous_issue is not None:
            exact_index = next(
                (
                    index
                    for index, issue in enumerate(issues)
                    if issue.id == clarification_issue_id
                ),
                None,
            )
            if exact_index is None:
                related_indexes = [
                    index
                    for index, issue in enumerate(issues)
                    if issue.artifact_type == previous_issue.artifact_type
                    and issue.dimension == previous_issue.dimension
                ]
                if len(related_indexes) == 1:
                    related_index = related_indexes[0]
                    related_issue = issues[related_index]
                    issues[related_index] = replace(
                        related_issue,
                        id=previous_issue.id,
                        clarification=(
                            related_issue.clarification
                            or previous_issue.clarification
                        ),
                        status=(
                            "resolved"
                            if related_issue.status == "resolved"
                            or complete_confirmation
                            else "addressed"
                        ),
                    )
                else:
                    issues.append(replace(previous_issue, status="resolved"))
    existing_ids = {issue.id for issue in issues}
    if previous_snapshot is not None:
        issues.extend(
            issue
            for issue in previous_snapshot.assessment.issues
            if issue.status == "resolved" and issue.id not in existing_ids
        )
    issues_tuple = tuple(issues)
    resolved = sum(issue.status == "resolved" for issue in issues_tuple)
    confirmed = sum(
        issue.status == "resolved" and bool(issue.clarification)
        for issue in issues_tuple
    )
    explanation = (
        f"The {assessment.confidence_band.lower()} confidence read is limited by "
        f"{limiting_dimension}. Reliability is {assessment.reliability.lower()} "
        f"because coverage is {basis.coverage.lower()}, evidence is "
        f"{basis.evidence.lower()}, and assessability is "
        f"{basis.assessability.lower()}."
    )
    return replace(
        assessment,
        understanding_stage=stage,
        reliability_basis=basis,
        confidence_direction=direction,
        limiting_dimension=limiting_dimension,
        false_confidence=false_confidence,
        confidence_explanation=explanation,
        issues=issues_tuple,
        resolved_issue_count=resolved,
        confirmed_dependency_count=confirmed,
    )


def _complete_user_confirmation(clarification: str | None) -> bool:
    if not clarification:
        return False
    answer_match = re.search(
        r"^Answer:\s*(.+)\Z",
        clarification,
        re.MULTILINE | re.DOTALL,
    )
    if not answer_match:
        return False
    answer = " ".join(answer_match.group(1).split()).lower()
    if len(answer) < 60:
        return False
    incomplete = re.search(
        r"\b(unknown|unconfirmed|pending|tbd|not yet|cannot|unsure|"
        r"no fallback|but no|not approved|not confirmed)\b",
        answer,
    )
    return incomplete is None


def _reliability_basis(artifacts: tuple[Artifact, ...]) -> ReliabilityBasis:
    covered = sum(bool(artifact.evidence_refs) for artifact in artifacts)
    coverage = (
        "High"
        if covered == len(ARTIFACT_TYPES)
        else "Moderate"
        if covered >= 4
        else "Low"
    )
    distinct_refs = {
        evidence_ref
        for artifact in artifacts
        for evidence_ref in artifact.evidence_refs
    }
    evidence = "High" if len(distinct_refs) >= 7 else "Moderate" if distinct_refs else "Low"
    reliable = sum(
        artifact.reliability in {"Moderate", "High"}
        for artifact in artifacts
    )
    assessability = (
        "High"
        if reliable == len(ARTIFACT_TYPES)
        and all(artifact.reliability == "High" for artifact in artifacts)
        else "Moderate"
        if reliable >= 4
        else "Low"
    )
    return ReliabilityBasis(
        coverage=coverage,
        evidence=evidence,
        assessability=assessability,
    )


def _confidence_direction(
    assessment: Assessment,
    previous_snapshot: AssessmentSnapshot | None,
) -> str:
    if previous_snapshot is None:
        return "unchanged"
    delta = (
        assessment.confidence_index
        - previous_snapshot.assessment.confidence_index
    )
    if delta >= 3:
        return "strengthened"
    if delta <= -3:
        return "weakened"
    return "unchanged"

import re
from dataclasses import replace

from oslo_api.analysis.integrity import (
    IntegrityArtifact,
    IntegrityIssue,
    build_integrity_read,
)
from oslo_api.analysis.issue_identity import deduplicate_issues
from oslo_api.analysis.models import (
    ARTIFACT_TYPES,
    Artifact,
    ArtifactType,
    Assessment,
    AssessmentSnapshot,
    EvidenceFragment,
    Issue,
    ReliabilityBasis,
    RunKind,
)
from oslo_api.analysis.provenance import build_project_provenance

_BAND_ORDER = {
    "Very Low": 0,
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Very High": 4,
}

_OUTCOME_CHECKPOINT_PATTERN = re.compile(
    r"^(?:Outcome checkpoint\s*[—-]\s*|Add checkpoint:\s*)read\s+"
    r"(?P<indicator>[^;\n]+);\s*"
    r"(?P<timing>[^;\n]+);\s*"
    r"if it drifts,\s*(?P<lever>[^\n]+?)\.?$",
    re.IGNORECASE | re.MULTILINE,
)


def _register_confirmed_schedule_checkpoints(
    assessment: Assessment,
    user_evidence: tuple[EvidenceFragment, ...],
) -> Assessment:
    """Promote explicit user-authored schedule gates into the signed read.

    A saved checkpoint is only complete when the evidence states the signal,
    timing, and corrective lever.  This deterministic promotion closes the
    loop between the editable Schedule artifact and Adaptability without
    weakening the existing checkpoint formula or trusting placeholder rows.
    """

    schedule_evidence = tuple(
        evidence
        for evidence in user_evidence
        if evidence.reference.startswith("user:artifact:schedule:version:")
    )
    if not schedule_evidence or not assessment.outcome_checkpoints:
        return assessment
    latest = schedule_evidence[-1]
    confirmed = tuple(_OUTCOME_CHECKPOINT_PATTERN.finditer(latest.content))
    if not confirmed:
        return assessment

    checkpoints = list(assessment.outcome_checkpoints)
    open_indexes = [
        index for index, checkpoint in enumerate(checkpoints) if not checkpoint.registered
    ]
    for match, checkpoint_index in zip(confirmed, open_indexes, strict=False):
        checkpoint = checkpoints[checkpoint_index]
        checkpoints[checkpoint_index] = replace(
            checkpoint,
            leading_indicator=match.group("indicator").strip(),
            timing=match.group("timing").strip(),
            lever=match.group("lever").strip().rstrip("."),
            registered=True,
            evidence_refs=(latest.reference,),
        )
    return replace(assessment, outcome_checkpoints=tuple(checkpoints))


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
    user_evidence: tuple[EvidenceFragment, ...] = (),
) -> Assessment:
    """Derive the Slice 3 console read from validated, persisted analysis output."""

    assessment = _register_confirmed_schedule_checkpoints(assessment, user_evidence)
    basis = _reliability_basis(artifacts)
    reliability = (
        "High"
        if {
            basis.coverage,
            basis.evidence,
            basis.assessability,
        }
        == {"High"}
        else assessment.reliability
    )
    clarity_issues = tuple(
        issue
        for issue in assessment.issues
        if issue.status != "resolved" and issue.dimension == "Clarity"
    )
    clarity = (
        "High"
        if basis.assessability == "High"
        and not any(issue.severity == "Critical" for issue in clarity_issues)
        and len(clarity_issues) <= 2
        else assessment.clarity
    )
    assessment = replace(
        assessment,
        reliability=reliability,
        clarity=clarity,
    )
    limiting_dimension = min(
        ("clarity", "alignment", "feasibility"),
        key=lambda name: _BAND_ORDER.get(getattr(assessment, name), -1),
    )
    structured_clarification = _latest_structured_clarification(user_evidence)
    stage = (
        "orientation"
        if kind is RunKind.INITIAL
        else "validated"
        if "USER_CLARIFICATION" in description or structured_clarification is not None
        else "expanded"
    )
    direction = _confidence_direction(assessment, previous_snapshot)
    false_confidence = (
        assessment.confidence_band in {"High", "Very High"}
        and reliability == "Low"
    )
    clarification_block = (
        structured_clarification[1]
        if structured_clarification is not None
        else _latest_clarification(description)
    )
    clarification_match = re.search(
        r"^Issue ID:\s*(\S+)\s*$",
        clarification_block or "",
        re.MULTILINE,
    )
    clarification_issue_id = (
        structured_clarification[0]
        if structured_clarification is not None
        else clarification_match.group(1)
        if clarification_match
        else None
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
                "addressed"
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
                            else "addressed"
                        ),
                    )
                else:
                    issues.append(
                        replace(
                            previous_issue,
                            status=(
                                "resolved"
                                if complete_confirmation
                                else "addressed"
                            ),
                        )
                    )
    existing_ids = {issue.id for issue in issues}
    if previous_snapshot is not None and kind is RunKind.EXTENDED:
        issues.extend(
            issue
            for issue in previous_snapshot.assessment.issues
            if issue.id not in existing_ids
        )
    # Extended reads retain findings that the deeper pass omitted so issue
    # lifecycle remains stable.  Deduplicate after that merge as well: the
    # deeper pass may describe the same weakness under another artifact or a
    # newly stabilised identity.
    issues_tuple = (
        tuple(issues)
        if clarification_issue_id
        else deduplicate_issues(tuple(issues))
    )
    resolved = sum(issue.status == "resolved" for issue in issues_tuple)
    confirmed = sum(
        issue.status in {"addressed", "resolved"} and bool(issue.clarification)
        for issue in issues_tuple
    )
    explanation = (
        f"The {assessment.confidence_band.lower()} confidence read is limited by "
        f"{limiting_dimension}. Reliability is {reliability.lower()} "
        f"because coverage is {basis.coverage.lower()}, evidence is "
        f"{basis.evidence.lower()}, and assessability is "
        f"{basis.assessability.lower()}."
    )
    enriched = replace(
        assessment,
        reliability=reliability,
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
    return with_integrity(enriched, artifacts)


_INTEGRITY_ARTIFACT_TYPES = (
    "intent",
    "context",
    "scope",
    "requirements",
)


def with_integrity(
    assessment: Assessment,
    artifacts: tuple[Artifact, ...],
) -> Assessment:
    """Project the persisted analysis into the signed Slice 1 read contract."""

    base_issues = tuple(
        issue
        for issue in assessment.issues
        if not issue.id.startswith(("ISS-FC-", "ISS-CP-"))
    )
    provenance = build_project_provenance(artifacts=artifacts, issues=base_issues)
    artifact_provenance = {
        item["artifact_type"]: item for item in provenance["artifacts"]
    }
    by_type = {artifact.artifact_type.value: artifact for artifact in artifacts}
    integrity_artifacts: list[IntegrityArtifact] = []
    for artifact_type in _INTEGRITY_ARTIFACT_TYPES:
        artifact = by_type.get(artifact_type)
        if artifact is None:
            continue
        evidence = artifact_provenance[artifact_type]
        open_caf_issue = any(
            issue.status != "resolved"
            and issue.artifact_type.value == artifact_type
            and issue.dimension in {"Clarity", "Alignment", "Feasibility"}
            for issue in base_issues
        )
        integrity_artifacts.append(
            IntegrityArtifact(
                key=artifact_type,
                title=artifact.title,
                viable=not open_caf_issue,
                reads_strong=artifact.reliability == "High",
                grounded_items=evidence["grounded"],
                inferred_items=evidence["inferred"],
                primary_outcome=artifact_type == "intent",
                evidence_grounded_items=evidence["grounded"],
                evidence_inferred_items=evidence["inferred"],
            )
        )
    domain_issues = tuple(_domain_issue(issue) for issue in base_issues)
    read = build_integrity_read(
        artifacts=tuple(integrity_artifacts),
        checkpoints=assessment.outcome_checkpoints,
        issues=domain_issues,
    )
    by_id = {issue.id: issue for issue in base_issues}
    for issue in read.issues:
        if issue.id not in by_id:
            by_id[issue.id] = _derived_issue(issue, artifacts)
    ranked = tuple(
        replace(
            by_id[issue.id],
            exposure_rank=float(len(read.issues) - index),
        )
        for index, issue in enumerate(read.issues)
    )
    return replace(
        assessment,
        issues=ranked,
        integrity=read.integrity,
        resolved_issue_count=sum(issue.status == "resolved" for issue in ranked),
    )


def _domain_issue(issue: Issue) -> IntegrityIssue:
    pillar = (
        "Viability"
        if issue.dimension in {"Clarity", "Alignment", "Feasibility"}
        else issue.dimension
    )
    return IntegrityIssue(
        id=issue.id,
        dim=pillar,
        dims=(pillar,),
        finding_type=issue.finding_type or f"{issue.dimension} Gap",
        section=issue.section or issue.artifact_type.value,
        severity=issue.severity,
        status=issue.status,
        title=issue.title,
        why=issue.why,
        recommendation=issue.recommendation,
        recommendation_from_oslo=issue.recommendation_from_oslo,
    )


def _derived_issue(
    issue: IntegrityIssue,
    artifacts: tuple[Artifact, ...],
) -> Issue:
    artifact_type = next(
        (
            artifact.artifact_type
            for artifact in artifacts
            if artifact.title == issue.section
        ),
        ArtifactType.SCHEDULE,
    )
    return Issue(
        id=issue.id,
        artifact_type=artifact_type,
        dimension=issue.dim,
        severity=issue.severity,
        title=issue.title,
        why=issue.why,
        recommendation=issue.recommendation,
        evidence_refs=(),
        status=issue.status,
        dimensions=issue.dims,
        finding_type=issue.finding_type,
        section=issue.section,
        recommendation_from_oslo=issue.recommendation_from_oslo,
    )


def _latest_structured_clarification(
    evidence: tuple[EvidenceFragment, ...],
) -> tuple[str, str] | None:
    for item in reversed(evidence):
        match = re.fullmatch(
            r"user:clarification:(?P<issue>[^:]+):answer:[^:]+",
            item.reference,
        )
        if match is not None:
            return match.group("issue"), item.content
    return None


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
    incomplete = re.search(
        r"\b(unknown|unconfirmed|pending|tbd|not yet|cannot|unsure|"
        r"no fallback|but no|not approved|not confirmed)\b",
        answer,
    )
    if incomplete is not None:
        return False
    explicit_closure = re.search(
        r"\b(?:accountable|owns?|owner)\b.{0,100}"
        r"\b(?:approved\s+fallback|fallback\s+is|effective|approved\s+by)\b|"
        r"\bapproved\b.{0,100}\b(?:threshold|decision|date|owner|fallback)\b",
        answer,
    )
    return len(answer) >= 60 or explicit_closure is not None


def _reliability_basis(artifacts: tuple[Artifact, ...]) -> ReliabilityBasis:
    covered = sum(bool(artifact.evidence_refs) for artifact in artifacts)
    coverage = (
        "High"
        if covered == len(ARTIFACT_TYPES)
        else "Moderate"
        if covered >= 4
        else "Low"
    )
    distinct_refs = set()
    row_count = 0
    cited_row_count = 0
    for artifact in artifacts:
        distinct_refs.update(artifact.evidence_refs)
        for section in artifact.sections:
            distinct_refs.update(section.evidence_refs)
            row_count += len(section.rows)
            cited_row_count += sum(
                bool(references) for references in section.row_evidence_refs
            )
            for references in section.row_evidence_refs:
                distinct_refs.update(references)
        for assumption in artifact.assumptions:
            distinct_refs.update(assumption.evidence_refs)
        for conflict in artifact.conflicts:
            distinct_refs.update(conflict.evidence_refs)
    evidence = "High" if len(distinct_refs) >= 7 else "Moderate" if distinct_refs else "Low"
    row_coverage = cited_row_count / row_count if row_count else 1
    fully_reliable_artifacts = all(
        artifact.reliability == "High" for artifact in artifacts
    )
    assessability = (
        "High"
        if covered == len(ARTIFACT_TYPES)
        and evidence == "High"
        and (
            fully_reliable_artifacts
            or (row_count > 0 and row_coverage >= 0.9)
        )
        else "Moderate"
        if covered >= 4 and row_coverage >= 0.6
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

from dataclasses import replace

from oslo_api.analysis.issue_identity import deduplicate_issues, stabilize_issue_ids
from oslo_api.analysis.models import ArtifactType, Issue


def _issue(
    issue_id: str,
    *,
    title: str,
    why: str,
    dimension: str = "Clarity",
    artifact_type: ArtifactType = ArtifactType.REQUIREMENTS,
    severity: str = "Critical",
    evidence_refs: tuple[str, ...] = ("document:plan:page:2:fragment:4",),
) -> Issue:
    return Issue(
        id=issue_id,
        artifact_type=artifact_type,
        dimension=dimension,
        severity=severity,
        title=title,
        why=why,
        recommendation="Confirm the migration threshold.",
        evidence_refs=evidence_refs,
        clarification="What patient-match threshold is approved?",
    )


def test_semantically_equivalent_issue_keeps_previous_stable_id() -> None:
    previous = _issue(
        "ISS-MIGRATION",
        title="Production migration acceptance thresholds undefined",
        why="No approved patient-match threshold is documented.",
    )
    current = _issue(
        "MODEL-GENERATED-NEW-ID",
        title="Migration scope and patient-match threshold remain unconfirmed",
        why="The production migration has no confirmed patient-match threshold.",
        dimension="Feasibility",
    )

    stabilized = stabilize_issue_ids((current,), (previous,))

    assert stabilized[0].id == "ISS-MIGRATION"
    assert stabilized[0].dimension == "Feasibility"


def test_new_issue_receives_deterministic_id_independent_of_model_id() -> None:
    first = _issue(
        "MODEL-ONE",
        title="Acceptance criteria are insufficient for release",
        why="Release acceptance criteria are not measurable.",
    )
    second = _issue(
        "MODEL-TWO",
        title="Acceptance criteria are insufficient for release",
        why="Release acceptance criteria are not measurable.",
    )

    first_id = stabilize_issue_ids((first,), ())[0].id
    second_id = stabilize_issue_ids((second,), ())[0].id

    assert first_id == second_id
    assert first_id.startswith("ISS-REQUIREMENTS-")


def test_duplicate_root_cause_merges_and_keeps_stronger_finding() -> None:
    model = _issue(
        "MODEL-BUDGET",
        artifact_type=ArtifactType.RESOURCES,
        title="Investment total does not reconcile",
        why="The stated investment total conflicts with the itemised budget.",
        severity="Moderate",
        evidence_refs=("document:plan:page:8:fragment:2",),
    )
    deterministic = _issue(
        "DET-BUDGET",
        artifact_type=ArtifactType.RESOURCES,
        title="Investment budget total does not reconcile",
        why="The investment total conflicts with the itemised budget lines.",
        severity="Critical",
        evidence_refs=(
            "document:plan:page:8:fragment:2",
            "document:plan:page:9:fragment:1",
        ),
    )

    merged = deduplicate_issues((model, deterministic))

    assert len(merged) == 1
    assert merged[0].id == "DET-BUDGET"
    assert merged[0].severity == "Critical"
    assert merged[0].evidence_refs == (
        "document:plan:page:8:fragment:2",
        "document:plan:page:9:fragment:1",
    )


def test_distinct_findings_with_one_shared_page_are_not_merged() -> None:
    accessibility = _issue(
        "ACCESSIBILITY",
        title="Accessibility verification is absent",
        why="The plan has no accessibility verification activity.",
        evidence_refs=("document:plan:page:12:fragment:1",),
    )
    privacy = _issue(
        "PRIVACY",
        title="Privacy impact assessment is absent",
        why="The plan has no privacy impact assessment or owner.",
        evidence_refs=("document:plan:page:12:fragment:1",),
    )

    assert deduplicate_issues((accessibility, privacy)) == (
        accessibility,
        privacy,
    )


def test_distinct_cross_artifact_conflicts_on_one_fragment_are_not_merged() -> None:
    timeline = _issue(
        "TIMELINE",
        artifact_type=ArtifactType.SCHEDULE,
        title="Conflicting project timelines",
        why="The evidence states 6 months and 12 months.",
        evidence_refs=("document:plan:page:1:fragment:1",),
    )
    budget = _issue(
        "BUDGET",
        artifact_type=ArtifactType.RESOURCES,
        title="Conflicting project budgets",
        why="The evidence states £1.8M and £2.5M.",
        evidence_refs=("document:plan:page:1:fragment:1",),
    )

    assert deduplicate_issues((timeline, budget)) == (timeline, budget)


def test_paraphrased_duplicate_titles_merge_with_shared_evidence() -> None:
    scope = _issue(
        "SCOPE-CAUSES",
        artifact_type=ArtifactType.SCOPE,
        title="Principal withdrawal causes lack corresponding interventions",
        why="The evidenced causes do not trace to scope.",
        evidence_refs=(
            "document:plan:page:2:fragment:1",
            "document:plan:page:4:fragment:1",
        ),
    )
    intent = _issue(
        "INTENT-CAUSES",
        artifact_type=ArtifactType.INTENT,
        title="Key withdrawal causes are not matched to interventions",
        why="No intervention addresses the evidenced causes.",
        evidence_refs=(
            "document:plan:page:2:fragment:1",
            "document:plan:page:4:fragment:1",
        ),
    )

    assert len(deduplicate_issues((scope, intent))) == 1


def test_same_numeric_root_cause_merges_across_different_evidence_rows() -> None:
    intent = _issue(
        "INTENT-TRAINING",
        artifact_type=ArtifactType.INTENT,
        title="Operations workforce competency population is inconsistent",
        why="The acceptance criterion uses 48 staff while the success measure uses 62.",
        evidence_refs=("document:plan:page:4:fragment:1",),
    )
    requirements = _issue(
        "REQUIREMENTS-TRAINING",
        artifact_type=ArtifactType.REQUIREMENTS,
        title="Training acceptance and success metric use different populations",
        why="Training acceptance covers 48 people but the KPI covers 62 staff.",
        evidence_refs=("document:plan:page:10:fragment:1",),
    )

    merged = deduplicate_issues((intent, requirements))

    assert len(merged) == 1
    assert merged[0].evidence_refs == (
        "document:plan:page:4:fragment:1",
        "document:plan:page:10:fragment:1",
    )


def test_same_performance_root_cause_merges_across_artifact_impacts() -> None:
    intent = _issue(
        "INTENT-AVAILABILITY",
        artifact_type=ArtifactType.INTENT,
        dimension="Alignment",
        title=(
            "Availability-search response target versus partner response time "
            "is inconsistent"
        ),
        why=(
            "The objective requires 400ms while all 14 partners can take up to "
            "800ms and must be queried synchronously."
        ),
        evidence_refs=("document:plan:page:6:fragment:1",),
    )
    requirements = _issue(
        "REQUIREMENTS-AVAILABILITY",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Feasibility",
        title=(
            "Synchronous channel-search design is incompatible with the "
            "availability target"
        ),
        why=(
            "A 400ms response cannot wait synchronously for channel partners "
            "whose contracted response time is 800ms."
        ),
        evidence_refs=(
            "document:plan:page:6:fragment:1",
            "document:plan:page:8:fragment:1",
        ),
    )

    merged = deduplicate_issues((intent, requirements))

    assert len(merged) == 1
    assert merged[0].evidence_refs == (
        "document:plan:page:6:fragment:1",
        "document:plan:page:8:fragment:1",
    )


def test_active_status_wins_when_duplicate_issue_states_disagree() -> None:
    addressed = _issue(
        "ADDRESSED",
        artifact_type=ArtifactType.REQUIREMENTS,
        title="Availability target conflicts with partner response time",
        why="The response target is 400ms but partners can take 800ms.",
        evidence_refs=("document:plan:page:6:fragment:1",),
    )
    addressed = replace(addressed, status="addressed")
    resolved = replace(addressed, id="RESOLVED", status="resolved")

    merged = deduplicate_issues((resolved, addressed))

    assert len(merged) == 1
    assert merged[0].status == "addressed"


def test_aggregate_conflict_does_not_replace_distinct_numeric_conflicts() -> None:
    berth = _issue(
        "BERTH",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        title="Berth length is internally inconsistent",
        why="The approved berth is 210 m but the meeting agreed 185 m.",
    )
    vessel = _issue(
        "VESSEL",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        title="Design vessel is internally inconsistent",
        why="The approved vessel is 180 m but the meeting agreed 195 m.",
    )
    aggregate = _issue(
        "AGGREGATE",
        artifact_type=ArtifactType.RESOURCES,
        dimension="Feasibility",
        title="Forecast coverage is internally inconsistent",
        why=(
            "The forecast retains a 210 m berth and 180 m vessel while the "
            "meeting agreed a 185 m berth and 195 m vessel."
        ),
    )

    merged = deduplicate_issues((berth, vessel, aggregate))

    assert {issue.id for issue in merged} == {"BERTH", "VESSEL", "AGGREGATE"}


def test_numeric_formatting_does_not_create_duplicate_issue_identity() -> None:
    formatted = _issue(
        "FORMATTED",
        artifact_type=ArtifactType.SCOPE,
        dimension="Alignment",
        title="Capital dredge volume is inconsistent",
        why="The brief states 240,000 cubic metres and the report states 310,000.",
    )
    normalized = _issue(
        "NORMALIZED",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Alignment",
        title="Dredge volume has conflicting measured values",
        why="The evidence states 240000 cubic metres and 310000 cubic metres.",
    )

    merged = deduplicate_issues((formatted, normalized))

    assert len(merged) == 1

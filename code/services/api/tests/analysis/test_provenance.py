from oslo_api.analysis.models import (
    Artifact,
    ArtifactAssumption,
    ArtifactSection,
    ArtifactType,
    Issue,
)
from oslo_api.analysis.provenance import build_project_provenance


def test_provenance_counts_rows_from_evidence_contract_not_ui_text() -> None:
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.SCHEDULE,
            title="Schedule",
            summary="Delivery plan",
            reliability="High",
            evidence_refs=("document:plan:page:2:fragment:0",),
            sections=(
                ArtifactSection(
                    heading="Milestones",
                    columns=("Milestone", "Date"),
                    rows=(("Pilot", "10 Jan 2027"), ("Rollout", "TBD")),
                    row_evidence_refs=(
                        ("document:plan:page:2:fragment:0",),
                        (),
                    ),
                    row_states=("confirmed", "inferred"),
                ),
            ),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=())

    schedule = next(item for item in result["artifacts"] if item["artifact_type"] == "schedule")
    assert schedule == {
        "artifact_type": "schedule",
        "grounded": 1,
        "inferred": 1,
        "total": 2,
        "verify_first": False,
    }
    assert result["grounded_claims"] == 1
    assert result["inferred_claims"] == 1
    assert result["structure"]["untraceable_numbers"] == 0


def test_provenance_counts_legacy_source_grounded_rows_as_grounded() -> None:
    reference = "document:charter:page:1"
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.INTENT,
            title="Intent",
            summary="Launch the portal.",
            reliability="High",
            evidence_refs=(reference,),
            sections=(
                ArtifactSection(
                    heading="Objectives",
                    columns=("ID", "Objective"),
                    rows=(("OBJ-01", "Launch the portal"),),
                    row_evidence_refs=((reference,),),
                    row_states=("source_grounded",),
                ),
            ),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=())

    assert result["grounded_claims"] == 1
    assert result["inferred_claims"] == 0


def test_provenance_links_load_bearing_assumptions_to_governed_issues() -> None:
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.RESOURCES,
            title="Resources",
            summary="Ownership is incomplete",
            reliability="Moderate",
            evidence_refs=(),
            assumptions=(
                ArtifactAssumption(
                    id="ASM-OWNER",
                    statement="No accountable delivery owner is named.",
                    state="inferred",
                    load_bearing=True,
                ),
            ),
        ),
    )
    issues = (
        Issue(
            id="ISS-OWNER",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Clarity",
            severity="Critical",
            title="Accountable delivery owner is missing",
            why="No accountable delivery owner is named.",
            recommendation="Name an owner.",
            evidence_refs=(),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=issues)

    assert result["load_bearing_inferences"] == 1
    assert result["structure"]["unconfirmed_dependencies"] == 1
    assert result["structure"]["unowned_parties"] == 1
    assert result["assumptions"][0]["issue_id"] == "ISS-OWNER"


def test_provenance_links_paraphrased_assumptions_using_shared_evidence() -> None:
    reference = "document:kiln:page:12:fragment:3"
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.RESOURCES,
            title="Resources",
            summary="Supplier capacity depends on one vendor.",
            reliability="Moderate",
            evidence_refs=(reference,),
            assumptions=(
                ArtifactAssumption(
                    id="A-04",
                    statement="The nominated refractory supplier can meet the shutdown date.",
                    state="inferred",
                    load_bearing=True,
                    evidence_refs=(reference,),
                ),
            ),
        ),
    )
    issues = (
        Issue(
            id="ISS-SUPPLIER",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Feasibility",
            severity="Critical",
            title="Single-vendor delivery has no fallback",
            why="The refractory package relies on the nominated vendor meeting the shutdown date.",
            recommendation="Qualify an alternate supplier.",
            evidence_refs=(reference,),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=issues)

    assert result["assumptions"][0]["issue_id"] == "ISS-SUPPLIER"
    assert result["assumptions"][0]["issue_title"] == "Single-vendor delivery has no fallback"


def test_provenance_links_assumptions_to_cross_artifact_findings_using_evidence() -> None:
    reference = "document:kiln:page:9:fragment:2"
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.SCOPE,
            title="Scope",
            summary="Planning assumptions",
            reliability="Moderate",
            evidence_refs=(reference,),
            assumptions=(
                ArtifactAssumption(
                    id="A-02",
                    statement="Aseptic recruitment will achieve two hires per month.",
                    state="inferred",
                    load_bearing=False,
                    evidence_refs=(reference,),
                ),
            ),
        ),
    )
    issues = (
        Issue(
            id="ISS-OPERATORS",
            artifact_type=ArtifactType.RESOURCES,
            dimension="Feasibility",
            severity="Critical",
            title="Operator recruitment cannot meet the qualification date",
            why="Recruitment at two hires per month cannot supply enough aseptic operators.",
            recommendation="Add qualified capacity or move the date.",
            evidence_refs=(reference,),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=issues)

    assert result["assumptions"][0]["issue_id"] == "ISS-OPERATORS"
    assert result["assumptions"][0]["load_bearing"] is True
    assert result["structure"]["unconfirmed_dependencies"] == 1


def test_provenance_deduplicates_the_same_project_assumption_across_artifacts() -> None:
    reference = "document:plan:page:3:fragment:1"
    repeated = "The incumbent supplier will extend the support agreement."
    artifacts = (
        Artifact(
            artifact_type=ArtifactType.SCOPE,
            title="Scope",
            summary="Scope assumption",
            reliability="Moderate",
            evidence_refs=(reference,),
            assumptions=(
                ArtifactAssumption(
                    id="ASM-SCOPE-SUPPLIER",
                    statement=repeated,
                    state="inferred",
                    load_bearing=False,
                    evidence_refs=(reference,),
                ),
            ),
        ),
        Artifact(
            artifact_type=ArtifactType.RESOURCES,
            title="Resources",
            summary="Commercial assumption",
            reliability="Moderate",
            evidence_refs=(reference,),
            assumptions=(
                ArtifactAssumption(
                    id="ASM-RESOURCES-SUPPLIER",
                    statement=repeated,
                    state="inferred",
                    load_bearing=True,
                    evidence_refs=(reference,),
                ),
            ),
        ),
    )

    result = build_project_provenance(artifacts=artifacts, issues=())

    assert len(result["assumptions"]) == 1
    assert result["assumptions"][0]["load_bearing"] is True
    assert result["load_bearing_inferences"] == 1

from datetime import UTC, datetime
from uuid import UUID

from oslo_api.analysis.load_bearing import (
    PlanDependencyGraph,
    PlanEdge,
    PlanNode,
    SensitivityCandidate,
    StructuralTarget,
)
from oslo_api.analysis.models import (
    Artifact,
    ArtifactSection,
    ArtifactType,
    Assessment,
    AssessmentSnapshot,
    Issue,
)
from oslo_api.analysis.persistence import (
    _active_issue_keys,
    _issue_observation_dimension,
    _primary_outcome_title,
    _snapshot_dict,
    _snapshot_from_dict,
    _snapshot_with_persisted_issue_lifecycle,
)


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
        finding_type="dependency_may_fail",
        structural_target="edge",
        graph_node_id="dependency",
    )


def test_active_issue_keys_only_counts_the_published_open_read() -> None:
    issues = (
        _issue("ISS-OPEN", "open"),
        _issue("ISS-ADDRESSED", "addressed"),
        _issue("ISS-RESOLVED", "resolved"),
    )

    assert _active_issue_keys(issues) == {"ISS-OPEN", "ISS-ADDRESSED"}


def test_model_gap_observation_keeps_its_dimension_unclassified() -> None:
    model_gap = _issue("ISS-MODEL-GAP", "open")
    model_gap = Issue(
        id=model_gap.id,
        artifact_type=model_gap.artifact_type,
        dimension="",
        severity=model_gap.severity,
        title=model_gap.title,
        why=model_gap.why,
        recommendation=model_gap.recommendation,
        evidence_refs=model_gap.evidence_refs,
        finding_basis="model_gap",
        classification_state="escalated",
        unassessed=True,
    )

    assert _issue_observation_dimension(model_gap) is None
    assert _issue_observation_dimension(_issue("ISS-CLARITY", "open")) == "Clarity"


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


def test_primary_outcome_rejects_an_absence_statement() -> None:
    intent = Artifact(
        artifact_type=ArtifactType.INTENT,
        title="Intent",
        summary="The conference purpose is not defined.",
        reliability="High",
        evidence_refs=("document:brief:page:1:fragment:0",),
        sections=(
            ArtifactSection(
                heading="Purpose, objectives and outcomes",
                body="The conference purpose is not defined.",
                evidence_refs=("document:brief:page:1:fragment:0",),
            ),
        ),
    )

    assert _primary_outcome_title((intent,)) is None


def test_snapshot_round_trip_retains_slice_ten_graph_and_sensitivity_contract() -> None:
    graph = PlanDependencyGraph(
        nodes=(
            PlanNode("dependency", "inference", "Dependency", "inferred", 0.8),
            PlanNode("outcome", "outcome", "Outcome", "accepted", 1.0),
        ),
        edges=(PlanEdge("dependency", "outcome", "supports", 0.7, 0.9),),
    )
    candidate = SensitivityCandidate(
        id="ISS-DEPENDENCY",
        node_id="dependency",
        structural_target=StructuralTarget.EDGE,
        favorable_integrity=0.8,
        adverse_integrity=0.2,
        runway_factor=1.1,
        edge_key=("dependency", "outcome"),
        stakes=1.0,
    )
    assessment = Assessment(
        confidence_index=50,
        confidence_band="Moderate",
        reliability="Moderate",
        clarity="Moderate",
        alignment="Moderate",
        feasibility="Moderate",
        issues=(_issue("ISS-DEPENDENCY", "open"),),
        dependency_graph=graph,
        sensitivity_candidates=(candidate,),
    )
    snapshot = AssessmentSnapshot(
        id=UUID("018f9f7e-8de2-7000-8000-000000000001"),
        analysis_run_id=UUID("018f9f7e-8de2-7000-8000-000000000002"),
        workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000003"),
        project_id=UUID("018f9f7e-8de2-7000-8000-000000000004"),
        state="current",
        summary="Current governed read.",
        artifacts=(),
        assessment=assessment,
        published_at=datetime(2026, 8, 16, tzinfo=UTC),
    )

    restored = _snapshot_from_dict(_snapshot_dict(snapshot))

    assert restored.assessment.dependency_graph == graph
    assert restored.assessment.sensitivity_candidates == (candidate,)
    assert restored.assessment.issues[0].graph_node_id == "dependency"


def test_retained_snapshot_projects_durable_lifecycle_into_history_provenance() -> None:
    """A reanalysis must retain the evidence-backed lifecycle it follows."""
    issue = Issue(
        id="ISS-VERIFIED",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Grounding",
        severity="Moderate",
        title="Owner confirmation is required",
        why="The project owner is not yet evidenced.",
        recommendation="Confirm the owner.",
        evidence_refs=("document:test:page:1:fragment:1",),
        status="open",
        load_bearing=True,
        primary_act="verify",
    )
    snapshot = AssessmentSnapshot(
        id=UUID("018f9f7e-8de2-7000-8000-000000000011"),
        analysis_run_id=UUID("018f9f7e-8de2-7000-8000-000000000012"),
        workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000013"),
        project_id=UUID("018f9f7e-8de2-7000-8000-000000000014"),
        state="current",
        summary="Read after a governed confirmation.",
        artifacts=(),
        assessment=Assessment(0, "Low", "Low", "Low", "Low", "Low", (issue,)),
        published_at=datetime(2026, 9, 11, tzinfo=UTC),
    )
    lifecycle = (
        {
            "issue_id": issue.id,
            "action": "confirm",
            "status": "resolved",
            "basis": "documented",
        },
    )

    retained = _snapshot_with_persisted_issue_lifecycle(snapshot, lifecycle)
    payload = _snapshot_dict(retained, issue_actions=lifecycle)

    assert snapshot.assessment.issues[0].status == "open"
    assert retained.assessment.issues[0].status == "resolved"
    assert payload["provenance"]["grounding"] == {
        "grounded": 1,
        "addressed": 0,
        "routed": 0,
        "inferred": 0,
        "total": 1,
        "basis": 1.0,
        "band": "Sound",
    }


def test_retained_snapshot_does_not_credit_a_resolution_without_evidence() -> None:
    """A lifecycle status alone never manufactures Grounding evidence."""
    issue = Issue(
        id="ISS-UNSUPPORTED",
        artifact_type=ArtifactType.REQUIREMENTS,
        dimension="Grounding",
        severity="Moderate",
        title="Owner confirmation is required",
        why="The project owner is not yet evidenced.",
        recommendation="Confirm the owner.",
        evidence_refs=(),
        status="open",
        load_bearing=True,
        primary_act="verify",
    )
    snapshot = AssessmentSnapshot(
        id=UUID("018f9f7e-8de2-7000-8000-000000000021"),
        analysis_run_id=UUID("018f9f7e-8de2-7000-8000-000000000022"),
        workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000023"),
        project_id=UUID("018f9f7e-8de2-7000-8000-000000000024"),
        state="current",
        summary="Read with unsupported lifecycle status.",
        artifacts=(),
        assessment=Assessment(0, "Low", "Low", "Low", "Low", "Low", (issue,)),
        published_at=datetime(2026, 9, 11, tzinfo=UTC),
    )
    lifecycle = ({"issue_id": issue.id, "action": "confirm", "status": "resolved"},)

    payload = _snapshot_dict(
        _snapshot_with_persisted_issue_lifecycle(snapshot, lifecycle),
        issue_actions=lifecycle,
    )

    assert payload["provenance"]["grounding"]["grounded"] == 0
    assert payload["provenance"]["grounding"]["addressed"] == 1


def test_unobserved_issue_is_retained_in_a_new_snapshot() -> None:
    from oslo_api.analysis.persistence import _retain_unobserved_issues

    issue = Issue(
        id="ISS-V2-RETAINED", artifact_type=ArtifactType.INTENT, dimension="Grounding",
        severity="Critical", title="Retained issue", why="Still needs a transition.",
        recommendation="Resolve or withdraw it.", evidence_refs=(), load_bearing=True,
    )
    def snapshot_with(issues: tuple[Issue, ...], run_suffix: str) -> AssessmentSnapshot:
        return AssessmentSnapshot(
            id=UUID(f"018f9f7e-8de2-7000-8000-00000000000{run_suffix}"),
            analysis_run_id=UUID(f"018f9f7e-8de2-7000-8000-00000000001{run_suffix}"),
            workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000003"),
            project_id=UUID("018f9f7e-8de2-7000-8000-000000000004"),
            state="current", summary="read", artifacts=(),
            assessment=Assessment(0, "Low", "Low", "Low", "Low", "Low", issues),
            published_at=datetime(2026, 9, 11, tzinfo=UTC),
        )

    baseline = snapshot_with((issue,), "1")
    reanalysis = snapshot_with((), "2")

    retained = _retain_unobserved_issues(reanalysis, baseline)

    assert tuple(item.id for item in retained.assessment.issues) == ("ISS-V2-RETAINED",)

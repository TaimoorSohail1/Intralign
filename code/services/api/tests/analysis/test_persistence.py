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

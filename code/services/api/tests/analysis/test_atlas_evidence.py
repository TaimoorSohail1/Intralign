from pathlib import Path
from uuid import UUID

from oslo_api.analysis.advisor import GroundedProjectAdvisor
from oslo_api.analysis.documents import parse_document
from oslo_api.analysis.harness import DeterministicAgentHarness
from oslo_api.analysis.models import (
    AnalysisRunRequest,
    ArtifactType,
    EvidenceFragment,
    RunKind,
)
from oslo_api.analysis.store import InMemoryAnalysisStore
from oslo_api.analysis.workflow import AnalysisWorkflow

PACK_ROOT = Path(__file__).resolve().parents[4] / "output" / "pdf" / "atlas-five-document-pack"
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")


def atlas_evidence() -> tuple[EvidenceFragment, ...]:
    evidence: list[EvidenceFragment] = []
    for path in sorted(PACK_ROOT.glob("0*.pdf")):
        parsed = parse_document(
            file_name=path.name,
            declared_content_type="application/pdf",
            content=path.read_bytes(),
        )
        for fragment in parsed.fragments:
            page = fragment.locator.get("page", 1)
            evidence.append(
                EvidenceFragment(
                    reference=f"atlas:{path.name}:page:{page}:fragment:{fragment.ordinal}",
                    content=fragment.content,
                    source_name=path.name,
                    location=f"Page {page}",
                )
            )
    return tuple(evidence)


def test_atlas_documents_construct_distinct_structured_artifacts() -> None:
    harness = DeterministicAgentHarness()
    perception = harness.perceive(
        description="",
        source_names=tuple(path.name for path in sorted(PACK_ROOT.glob("0*.pdf"))),
        evidence=atlas_evidence(),
        kind=RunKind.EXTENDED,
    )

    artifacts = {
        artifact.artifact_type: artifact
        for artifact in harness.construct(perception=perception, kind=RunKind.EXTENDED)
    }

    expected_rows = {
        ArtifactType.INTENT: {"Objectives and success measures": 5},
        ArtifactType.CONTEXT: {"Stakeholder register": 7, "Governance forums": 4},
        ArtifactType.SCOPE: {"Included deliverables": 6, "Explicit exclusions": 5},
        ArtifactType.REQUIREMENTS: {
            "Functional requirements": 8,
            "Non-functional and acceptance gates": 6,
        },
        ArtifactType.WORK_BREAKDOWN: {"Work breakdown": 9},
        ArtifactType.SCHEDULE: {"Integrated milestones": 9, "Critical dependencies": 4},
        ArtifactType.RESOURCES: {"Resource plan": 8, "RACI": 7},
    }
    for artifact_type, sections in expected_rows.items():
        artifact = artifacts[artifact_type]
        indexed = {section.heading: section for section in artifact.sections}
        for heading, count in sections.items():
            assert heading in indexed
            assert len(indexed[heading].rows) == count
            assert all(indexed[heading].row_evidence_refs)

    assert len(artifacts[ArtifactType.CONTEXT].assumptions) == 4
    assert all(
        artifact.project_title == "Atlas B2B Commerce Launch" for artifact in artifacts.values()
    )
    assert len({artifact.summary for artifact in artifacts.values()}) == 7

    conflicts = {
        artifact_type: {conflict.field: conflict.values for conflict in artifact.conflicts}
        for artifact_type, artifact in artifacts.items()
    }
    assert conflicts[ArtifactType.SCHEDULE]["ERP pricing API date"] == (
        "08 Feb 2027 needed",
        "22 Feb 2027 supplier commitment",
    )
    assert conflicts[ArtifactType.RESOURCES]["Project cost"] == (
        "GBP 1,800,000 approved ceiling",
        "GBP 1,845,000 forecast",
    )
    assert conflicts[ArtifactType.SCOPE]["Native offline ordering"] == (
        "Explicitly excluded",
        "CR-002 rejected",
    )


def test_atlas_gaps_and_conflicts_become_traceable_issues() -> None:
    evidence = atlas_evidence()
    result = AnalysisWorkflow(
        store=InMemoryAnalysisStore(),
        harness=DeterministicAgentHarness(),
    ).run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.EXTENDED,
            description="",
            source_names=tuple(path.name for path in sorted(PACK_ROOT.glob("0*.pdf"))),
            user_evidence=evidence,
            idempotency_key="atlas-evidence-issues-v1",
        )
    )

    assert result.snapshot is not None
    issues = {issue.title: issue for issue in result.snapshot.assessment.issues}
    expected = {
        "OBJ-05 target is missing a unit",
        "REQ-007 has no accountable owner",
        "ParcelLink access is unconfirmed",
        "Solution Architect has no named backup",
        "Integration Lead has a 0.5 FTE shortfall",
        "Required data-steward capacity is missing",
        "Pen-test vendor is not contracted",
        "GBP 45,000 forecast variance is not approved",
        "ERP pricing API date is internally inconsistent",
        "Project cost is internally inconsistent",
        "Native offline ordering is internally inconsistent",
    }
    assert expected <= issues.keys()
    assert "Critical delivery capacity is not confirmed" not in issues
    assert all(issues[title].evidence_refs for title in expected)


def test_atlas_budget_question_names_the_variance_sources_and_decision_authority() -> None:
    evidence = (
        EvidenceFragment(
            reference="atlas:intake",
            source_name="Project description",
            location="Intake",
            content=(
                "QA rerun with Atlas B2B commerce launch governance, requirements, "
                "schedule, RACI and RAID evidence."
            ),
        ),
        *atlas_evidence(),
    )
    result = AnalysisWorkflow(
        store=InMemoryAnalysisStore(),
        harness=DeterministicAgentHarness(),
    ).run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.EXTENDED,
            description="",
            source_names=tuple(path.name for path in sorted(PACK_ROOT.glob("0*.pdf"))),
            user_evidence=evidence,
            idempotency_key="atlas-evidence-advisor-v1",
        )
    )
    assert result.snapshot is not None

    reply = GroundedProjectAdvisor().answer(
        snapshot=result.snapshot,
        question=(
            "Who must approve the GBP 45,000 forecast variance, and which documents prove it?"
        ),
    )

    assert "GBP 45,000" in reply.answer
    assert "01_executive_charter_and_benefits.pdf" in reply.answer
    assert "05_raid_status_change_decisions.pdf" in reply.answer
    assert "Steering Committee" in reply.answer
    assert "not approved" in reply.answer
    assert "Project description (Intake)" not in reply.answer

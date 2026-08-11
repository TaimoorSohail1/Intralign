from oslo_api.analysis.harness import DeterministicAgentHarness
from oslo_api.analysis.models import EvidenceFragment, RunKind


def test_stress_evidence_produces_evidence_linked_clarity_alignment_and_feasibility_issues():
    evidence = (
        EvidenceFragment(
            reference="document:stress:page:6:fragment:1",
            content=(
                "Initial duration is 9 months. Another section states 6 months. "
                "A later roadmap mentions 12 months. Budget approved as $2.5M. "
                "Finance references $2.1M. Steering committee mentions $1.8M."
            ),
        ),
        EvidenceFragment(
            reference="document:stress:page:11:fragment:2",
            content=(
                "The mobile app, HR module and inventory integration are inconsistently "
                "included. Success metrics are not defined. Production deployment requires "
                "regulatory approval not included in the timeline. Conflicting Resource Plan: "
                "one section assumes 4 backend developers while another assumes 8. "
                "Final vendor undecided. Migration volume unknown."
            ),
        ),
    )
    harness = DeterministicAgentHarness()

    perception = harness.perceive(
        description="",
        source_names=("stress.pdf",),
        evidence=evidence,
        kind=RunKind.EXTENDED,
    )
    artifacts = harness.construct(perception=perception, kind=RunKind.EXTENDED)
    assessment = harness.evaluate(
        artifacts=artifacts,
        perception=perception,
        kind=RunKind.EXTENDED,
    )

    titles = {issue.title for issue in assessment.issues}
    assert assessment.confidence_band == "Low"
    assert assessment.clarity == "Low"
    assert assessment.alignment == "Low"
    assert assessment.feasibility == "Low"
    assert "Conflicting project timelines" in titles
    assert "Conflicting project budgets" in titles
    assert "Project scope is ambiguous" in titles
    assert "Success metrics are missing" in titles
    assert "Deployment depends on unresolved regulatory approval" in titles
    assert "Resource allocations conflict" in titles
    assert "Vendor selection is unresolved" in titles
    assert "Migration volume is unknown" in titles
    assert all(issue.evidence_refs for issue in assessment.issues)

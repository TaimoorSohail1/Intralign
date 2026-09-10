"""IC-WU-ACCEPT / IC-WA-00R: reanalysis must retain the attested subject.

The synthetic workshop fixture captures the Production 45eb351 failure:
one and two confirmations were retained but the read became 0/9 and 0/10.
Public issue payloads omit graph IDs, so the replay also covers legacy keys.
"""

import json
from dataclasses import replace
from pathlib import Path
from uuid import uuid4

import pytest

from oslo_api.analysis import (
    AnalysisPassKind,
    AnalysisRunRequest,
    AnalysisRunStatus,
    AnalysisWorkflow,
    DeterministicAgentHarness,
    EvidenceFragment,
    InMemoryAnalysisStore,
    RunKind,
)
from oslo_api.analysis.models import ReanalysisTrigger
from oslo_api.analysis.persistence import _issue_from_dict
from oslo_api.analysis.provenance import build_project_provenance


def _captured_issues(phase):
    fixture = json.loads(
        (Path(__file__).parent / "fixtures/workshop_attestation_reanalysis.json").read_text()
    )
    return tuple(_issue_from_dict(issue) for issue in fixture[phase])


class RewordingHarness(DeterministicAgentHarness):
    def __init__(self):
        self.evaluations = 0

    def evaluate(self, **kwargs):
        phase = ("baseline", "after_one_settled", "after_two_settled")[min(self.evaluations, 2)]
        self.evaluations += 1
        return replace(
            super().evaluate(**kwargs),
            issues=_captured_issues(phase),
            outcome_checkpoints=(),
            dependency_graph=None,
            sensitivity_candidates=(),
        )


def _baseline():
    store = InMemoryAnalysisStore()
    harness = RewordingHarness()
    workflow = AnalysisWorkflow(store=store, harness=harness)
    request = AnalysisRunRequest(
        workspace_id=uuid4(),
        project_id=uuid4(),
        requested_by=uuid4(),
        kind=RunKind.EXTENDED,
        pass_kind=AnalysisPassKind.DEEP,
        description="Synthetic library workshop QA fixture.",
        source_names=(),
    )
    first = workflow.run(request)
    assert first.status is AnalysisRunStatus.COMPLETED
    return store, harness, workflow, first


def _confirmation(parent, issue):
    return replace(
        parent.request,
        parent_run_id=parent.id,
        idempotency_key=str(uuid4()),
        reanalysis_trigger=ReanalysisTrigger.BATCH,
        pass_kind=AnalysisPassKind.FAST,
        user_evidence=parent.request.user_evidence
        + (
            EvidenceFragment(
                reference=f"user:issue-act:confirm:{uuid4()}",
                content=f"The user recorded a governed confirm act for {issue.title}.",
                source_name="Issue attestation",
                location=issue.title,
            ),
        ),
    )


def test_two_confirmations_preserve_the_plan_and_ground_both_retained_subjects():
    store, _harness, workflow, first = _baseline()
    baseline = first.snapshot
    parent = store.get_run(first.run_id)
    issues = tuple(
        issue
        for issue in baseline.assessment.issues
        if "deadline" in issue.title or issue.title == "Postponement action is unowned"
    )
    assert len(issues) == 2
    original_ids = {issue.id for issue in baseline.assessment.issues}
    assert len(original_ids) == 6
    actions = []
    for count, issue in enumerate(issues, 1):
        result = workflow.run(_confirmation(parent, issue))
        assert result.status is AnalysisRunStatus.COMPLETED
        assert result.snapshot.id != parent.snapshot.id
        assert result.snapshot.artifacts == baseline.artifacts
        assert {item.id for item in result.snapshot.assessment.issues} == original_ids
        assert (
            build_project_provenance(
                artifacts=result.snapshot.artifacts,
                issues=result.snapshot.assessment.issues,
            )["grounding"]["grounded"]
            == 0
        )
        # The real overview supplies these persisted acts only after the run lands.
        actions.append(
            {"issue_id": issue.id, "action": "confirm", "basis": "documented", "status": "resolved"}
        )
        grounding = build_project_provenance(
            artifacts=result.snapshot.artifacts,
            issues=result.snapshot.assessment.issues,
            issue_actions=tuple(actions),
        )["grounding"]
        assert grounding["grounded"] == count
        assert grounding["band"] == ("Fragile" if count == 1 else "Weak")
        assert grounding["total"] == len(original_ids)
        parent = store.get_run(result.run_id)


@pytest.mark.parametrize(
    "change",
    ("description", "evidence", "sources", "explicit", "custom_content", "custom_reference"),
)
def test_attestation_does_not_hide_a_new_plan_input(change):
    store, harness, workflow, first = _baseline()
    parent = store.get_run(first.run_id)
    request = _confirmation(parent, parent.snapshot.assessment.issues[0])
    if change == "description":
        request = replace(request, description="Changed workshop scope.")
    elif change == "evidence":
        request = replace(
            request,
            user_evidence=request.user_evidence
            + (
                EvidenceFragment(
                    reference="user:artifact:scope:version:2",
                    content="Changed scope",
                    source_name="User-confirmed Scope edit",
                    location="Scope",
                ),
            ),
        )
    elif change == "sources":
        request = replace(request, source_names=("new-plan.txt",))
    elif change == "custom_content":
        request = replace(
            request,
            user_evidence=(replace(request.user_evidence[-1], content="Owner is now Priya."),),
        )
    elif change == "custom_reference":
        request = replace(
            request,
            user_evidence=(replace(request.user_evidence[-1], reference="document:new-evidence"),),
        )
    else:
        request = replace(request, reanalysis_trigger=ReanalysisTrigger.EXPLICIT)
    result = workflow.run(request)
    assert result.status is AnalysisRunStatus.COMPLETED
    assert harness.evaluations == 2


@pytest.mark.parametrize("act", ("confirm", "ground", "flag", "withdraw"))
def test_state_only_batches_retain_subjects_without_fabricating_grounding(act):
    store, harness, workflow, first = _baseline()
    parent = store.get_run(first.run_id)
    issues = parent.snapshot.assessment.issues[:2]
    request = _confirmation(parent, issues[0])
    request = replace(
        request,
        user_evidence=tuple(
            EvidenceFragment(
                reference=f"user:issue-act:{act}:test:batch:{index}",
                content=f"The user recorded a governed {act} act for {issue.title}.",
                source_name="Issue attestation",
                location=issue.title,
            )
            for index, issue in enumerate(issues)
        ),
    )
    result = workflow.run(request)
    assert result.status is AnalysisRunStatus.COMPLETED
    assert harness.evaluations == 1
    assert result.snapshot.artifacts == first.snapshot.artifacts
    assert result.snapshot.assessment.issues == first.snapshot.assessment.issues
    assert (
        build_project_provenance(
            artifacts=result.snapshot.artifacts,
            issues=result.snapshot.assessment.issues,
        )["grounding"]["grounded"]
        == 0
    )

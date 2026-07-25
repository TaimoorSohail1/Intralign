from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.analysis import (
    AnalysisPhase,
    AnalysisRunRequest,
    AnalysisWorkflow,
    DeterministicAgentHarness,
    EvidenceFragment,
    InMemoryAnalysisStore,
    RunKind,
)
from oslo_api.analysis.advisor import AdvisorReply
from oslo_api.main import create_app
from oslo_api.slice_two import SliceTwoIssueNotAnswerable

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")


class AuthenticatedSliceOne:
    def authenticate(self, access_token: str):
        assert access_token == "valid-access-token"
        return type("User", (), {"id": USER_ID, "email": "member@example.com"})()


class RecordingSliceTwo:
    def __init__(self, store=None) -> None:
        self.store = store or InMemoryAnalysisStore()
        self.started: list[AnalysisRunRequest] = []
        self.latest_extended = None
        self.orientation_seen = False

    def start_analysis(
        self,
        *,
        actor_user_id,
        project_id,
        description,
        source_names,
        source_document_ids,
        kind,
        key,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        request = AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=project_id,
            requested_by=actor_user_id,
            kind=kind,
            description=description,
            source_names=source_names,
            source_document_ids=source_document_ids,
            idempotency_key=key,
        )
        self.started.append(request)
        return self.store.create_run(request)

    def get_run(self, *, actor_user_id, run_id):
        assert actor_user_id == USER_ID
        run = self.store.get_run(run_id)
        if run is None:
            raise AssertionError("run missing")
        return run

    def events_after(self, *, actor_user_id, run_id, sequence):
        assert actor_user_id == USER_ID
        return self.store.events_after(run_id, sequence)

    def wait_for_events(self, *, actor_user_id, run_id, sequence, timeout):
        assert actor_user_id == USER_ID
        return self.store.wait_for_events(run_id, sequence, timeout)

    def complete_latest(self):
        return AnalysisWorkflow(
            store=self.store,
            harness=DeterministicAgentHarness(),
        ).run(self.started[-1])

    def current_overview(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        snapshot = self.store.current_snapshot(project_id)
        if snapshot is None:
            raise AssertionError("snapshot missing")
        return snapshot

    def latest_extended_run(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        return self.latest_extended

    def has_seen_orientation(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        return self.orientation_seen

    def upload_document(
        self,
        *,
        actor_user_id,
        project_id,
        file_name,
        content_type,
        content,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        assert file_name == "plan.txt"
        assert content_type == "text/plain"
        assert content == b"Timeline is 6 months."
        return type(
            "UploadedDocument",
            (),
            {
                "id": UUID("018f9f7e-8de2-7000-8000-000000000099"),
                "file_name": file_name,
                "status": "parsed",
                "fragment_count": 1,
            },
        )()

    def answer_issue(
        self,
        *,
        actor_user_id,
        project_id,
        issue_id,
        answer,
        key,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        assert issue_id == "ISS-001"
        assert answer == "Priya owns migration and the fallback is the legacy import."
        assert key == "answer-issue-001"
        return self.store.create_run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=answer,
                source_names=(),
                idempotency_key=f"clarification:{key}",
            )
        )


class RecordingAdvisor:
    def __init__(self) -> None:
        self.calls = []

    def answer(self, *, snapshot, question):
        self.calls.append((snapshot, question))
        return AdvisorReply(
            answer="Resolve the migration baseline first because it blocks credible delivery.",
            follow_up_questions=(
                "Which regions have not validated their source volumes?",
                "Who owns the migration baseline?",
            ),
        )


class EvidenceRecordingStore(InMemoryAnalysisStore):
    def evidence_for(self, request):
        return (
            EvidenceFragment(
                reference="document:plan:page:4:fragment:2",
                content="The approved Phase 1 budget and migration owner are unresolved.",
                source_name="Programme plan.pdf",
                location="Page 4",
            ),
        )


class NonAnswerableSliceTwo(RecordingSliceTwo):
    def answer_issue(self, **kwargs):
        raise SliceTwoIssueNotAnswerable


def test_authenticated_user_starts_analysis_idempotently() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))
    headers = {
        "Authorization": "Bearer valid-access-token",
        "Idempotency-Key": "intake-submit-001",
    }
    payload = {
        "kind": "initial",
        "description": "Launch the new customer portal.",
        "source_names": [],
    }

    first = client.post(
        f"/v1/projects/{PROJECT_ID}/analysis-runs",
        headers=headers,
        json=payload,
    )
    second = client.post(
        f"/v1/projects/{PROJECT_ID}/analysis-runs",
        headers=headers,
        json=payload,
    )

    assert first.status_code == 202
    assert second.status_code == 202
    assert first.json()["run_id"] == second.json()["run_id"]
    assert first.json()["status"] == "queued"
    assert slice_two.started[0].kind is RunKind.INITIAL


def test_analysis_run_keeps_uploaded_document_ids() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))
    document_id = "018f9f7e-8de2-7000-8000-000000000099"

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/analysis-runs",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "document-analysis-001",
        },
        json={
            "description": "",
            "source_names": ["plan.txt"],
            "source_document_ids": [document_id],
        },
    )

    assert response.status_code == 202
    assert slice_two.started[-1].source_document_ids == (UUID(document_id),)


def test_authenticated_user_uploads_a_document_for_analysis() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/documents",
        headers={"Authorization": "Bearer valid-access-token"},
        files={"file": ("plan.txt", b"Timeline is 6 months.", "text/plain")},
    )

    assert response.status_code == 201
    assert response.json() == {
        "document_id": "018f9f7e-8de2-7000-8000-000000000099",
        "file_name": "plan.txt",
        "status": "parsed",
        "fragment_count": 1,
    }


def test_authenticated_user_gets_a_project_grounded_advisor_answer() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="Migration volumes are not yet validated.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="advisor-overview-001",
    )
    slice_two.complete_latest()
    advisor = RecordingAdvisor()
    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            slice_two=slice_two,
            project_advisor=advisor,
        )
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/advisor/messages",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"question": "What should I address first?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Resolve the migration baseline first because it blocks credible delivery.",
        "follow_up_questions": [
            "Which regions have not validated their source volumes?",
            "Who owns the migration baseline?",
        ],
    }
    assert advisor.calls[0][1] == "What should I address first?"
    assert advisor.calls[0][0].project_id == PROJECT_ID


def test_authenticated_user_answers_an_issue_and_starts_reanalysis() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-001/answers",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "answer-issue-001",
        },
        json={"answer": "Priya owns migration and the fallback is the legacy import."},
    )

    assert response.status_code == 202
    assert response.json()["project_id"] == str(PROJECT_ID)
    assert response.json()["kind"] == "extended"
    assert response.json()["status"] == "queued"


def test_issue_without_an_open_clarification_cannot_start_reanalysis() -> None:
    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            slice_two=NonAnswerableSliceTwo(),
        )
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-002/answers",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "answer-issue-002",
        },
        json={"answer": "This issue has no clarification request."},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "ISSUE_NOT_ANSWERABLE"


def test_overview_reports_a_failed_extended_run_for_safe_retry() -> None:
    slice_two = RecordingSliceTwo()
    initial = slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="Migration volumes require validation.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="overview-extended-status-001",
    )
    slice_two.complete_latest()
    extended = slice_two.store.create_run(
        AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            requested_by=USER_ID,
            kind=RunKind.EXTENDED,
            description="Migration volumes require validation.",
            source_names=(),
            parent_run_id=initial.id,
        )
    )
    slice_two.store.start_run(extended.id)
    slice_two.store.start_phase(extended.id, AnalysisPhase.PERCEIVE)
    slice_two.store.fail(
        extended.id,
        error_code="EVIDENCE_REFERENCE_CONTRACT_FAILED",
        phase=AnalysisPhase.PERCEIVE,
        retryable=True,
    )
    slice_two.latest_extended = slice_two.store.get_run(extended.id)
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two)
    )

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/overview",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["extended_analysis"] == {
        "run_id": str(extended.id),
        "project_id": str(PROJECT_ID),
        "kind": "extended",
        "status": "failed",
        "phase": "perceive",
        "completed_phases": [],
        "error_code": "EVIDENCE_REFERENCE_CONTRACT_FAILED",
    }


def test_overview_exposes_the_evidence_qualified_understanding_console() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="Migration volumes and the accountable owner are not yet validated.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="slice-three-overview-001",
    )
    slice_two.complete_latest()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two)
    )

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/overview",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["orientation_seen"] is False
    assessment = response.json()["assessment"]
    assert assessment["understanding_stage"] == "orientation"
    assert assessment["reliability_basis"] == {
        "coverage": "High",
        "evidence": "Moderate",
        "assessability": "Moderate",
    }
    assert assessment["confidence_direction"] == "unchanged"
    assert assessment["limiting_dimension"] == "feasibility"
    assert assessment["false_confidence"] is False
    assert assessment["confidence_explanation"]
    assert assessment["resolved_issue_count"] == 0
    assert assessment["confirmed_dependency_count"] == 0


def test_overview_exposes_readable_issue_evidence_without_requiring_raw_ids() -> None:
    slice_two = RecordingSliceTwo(store=EvidenceRecordingStore())
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="",
        source_names=("Programme plan.pdf",),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="slice-three-citations-001",
    )
    slice_two.complete_latest()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two)
    )

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/overview",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    issue = response.json()["assessment"]["issues"][0]
    assert issue["evidence"][0] == {
        "source_name": "Programme plan.pdf",
        "location": "Page 4",
        "excerpt": "The approved Phase 1 budget and migration owner are unresolved.",
    }


def test_advisor_rejects_an_empty_question_before_calling_the_model() -> None:
    advisor = RecordingAdvisor()
    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            slice_two=RecordingSliceTwo(),
            project_advisor=advisor,
        )
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/advisor/messages",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"question": "   "},
    )

    assert response.status_code == 422
    assert advisor.calls == []


def test_refresh_reads_durable_state_and_sse_replays_only_missed_events() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))
    headers = {
        "Authorization": "Bearer valid-access-token",
        "Idempotency-Key": "refresh-replay-001",
    }
    started = client.post(
        f"/v1/projects/{PROJECT_ID}/analysis-runs",
        headers=headers,
        json={"description": "A project that survives browser refresh.", "source_names": []},
    ).json()
    completed = slice_two.complete_latest()

    state = client.get(
        f"/v1/analysis-runs/{completed.run_id}",
        headers={"Authorization": "Bearer valid-access-token"},
    )
    stream = client.get(
        f"/v1/analysis-runs/{completed.run_id}/events",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Last-Event-ID": "4",
        },
    )

    assert started["run_id"] == str(completed.run_id)
    assert state.status_code == 200
    assert state.json()["status"] == "completed"
    assert "id: 4\n" not in stream.text
    assert "event: assessment.published" in stream.text
    assert "event: analysis.completed" in stream.text

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
from oslo_api.slice_two import (
    SliceTwoAnalysisInProgress,
    SliceTwoArtifactConflict,
    SliceTwoIssueNotAnswerable,
)

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
        self.issue_actions: list[dict] = []
        self.history = {
            "project_id": str(PROJECT_ID),
            "groups": [],
            "trend": [],
            "next_cursor": None,
        }

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
        provisional=False,
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
            provisional=provisional,
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
    def runtime_state(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        snapshot = self.store.current_snapshot(project_id)
        return {
            "freshness": {
                "state": "fresh",
                "pending_count": 0,
                "based_on_run_id": snapshot.analysis_run_id if snapshot else None,
                "active_run_id": None,
                "last_act_at": None,
                "last_landed_at": snapshot.published_at if snapshot else None,
                "latest_pending_event_id": None,
            },
            "first_run": {
                "first_run": False,
                "onboarded": True,
                "grounding_act_count": 2,
                "ever_unlocked": True,
                "unlock_threshold": 2,
                "freeze_on": False,
            },
            "notifications": [],
        }

    def run_reanalysis_now(self, *, actor_user_id, project_id, deep, key):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        request = AnalysisRunRequest(
            workspace_id=WORKSPACE_ID,
            project_id=project_id,
            requested_by=actor_user_id,
            kind=RunKind.EXTENDED,
            description="Explicit governed reanalysis.",
            source_names=(),
            idempotency_key=key,
        )
        return self.store.create_run(request)

    def withdraw_pending_act(self, *, actor_user_id, project_id, event_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        return {
            "event_id": event_id,
            "state": "withdrawn",
            "pending_count": 0,
            "grounding_act_count": 1,
            "ever_unlocked": True,
            "freeze_on": False,
        }

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

    def act_on_issue(
        self,
        *,
        actor_user_id,
        project_id,
        issue_id,
        action,
        resolution,
        key,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        assert issue_id == "ISS-001"
        assert action in {"select", "apply", "custom"}
        assert resolution == "Assign Priya as the accountable migration owner."
        assert key in {"issue-resolution-001", "issue-resolution-apply-001"}
        run = None
        if action in {"apply", "custom"}:
            run = self.store.create_run(
                AnalysisRunRequest(
                    workspace_id=WORKSPACE_ID,
                    project_id=project_id,
                    requested_by=actor_user_id,
                    kind=RunKind.EXTENDED,
                    description=resolution,
                    source_names=(),
                    idempotency_key=f"issue-action:{key}",
                )
            )
        result = {
            "issue_id": issue_id,
            "action": action,
            "status": "addressed",
            "selected_resolution": resolution,
            "analysis_run": run,
        }
        self.issue_actions = [result]
        return result

    def list_issue_actions(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        return self.issue_actions

    def act_on_issue_lifecycle(
        self,
        *,
        actor_user_id,
        project_id,
        issue_id,
        act,
        basis,
        evidence_ref,
        resolution,
        reviewer,
        key,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        assert issue_id == "ISS-001"
        assert act == "flag"
        assert basis == "documented"
        assert evidence_ref == "evidence:registration-export"
        assert resolution is None
        assert reviewer is None
        assert key == "issue-lifecycle-flag-001"
        run = self.store.create_run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description="Flagged from documented evidence.",
                source_names=(),
                idempotency_key=f"issue-lifecycle:{key}",
            )
        )
        return {
            "issue_id": issue_id,
            "act": act,
            "status": "addressed",
            "attestation": {
                "id": "attestation-001",
                "act": act,
                "basis": basis,
                "evidence_ref": evidence_ref,
                "attributed_to": {
                    "id": str(actor_user_id),
                    "display_name": "Member",
                    "role": "owner",
                },
                "supersedes": None,
            },
            "analysis_run": run,
        }

    def list_issue_proposals(self, *, actor_user_id, project_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        return [
            {
                "id": "018f9f7e-8de2-7000-8000-000000000155",
                "issue_id": "ISS-001",
                "kind": "build",
                "resolver_key": "accountable-owner",
                "title": "Assign Priya as the accountable owner.",
                "rationale": "The delivery path needs one accountable owner.",
                "artifact_type": "requirements",
                "load_bearing": True,
                "accepted": False,
                "rejected": False,
                "surface": None,
            }
        ]

    def decide_issue_proposal(
        self,
        *,
        actor_user_id,
        project_id,
        proposal_id,
        accepted,
        surface,
        key,
    ):
        proposal = self.list_issue_proposals(
            actor_user_id=actor_user_id,
            project_id=project_id,
        )[0]
        assert str(proposal_id) == proposal["id"]
        assert accepted is True
        assert surface == "artifact"
        assert key == "proposal-decision-001"
        proposal = {**proposal, "accepted": True, "surface": surface}
        run = self.store.create_run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=proposal["title"],
                source_names=(),
                idempotency_key=f"proposal:{key}",
            )
        )
        return {"proposal": proposal, "analysis_run": run}

    def list_history(
        self,
        *,
        actor_user_id,
        project_id,
        category,
        cursor,
        limit,
    ):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        assert category == "analysis"
        assert cursor is None
        assert limit == 25
        return self.history

    def history_snapshot(self, *, actor_user_id, project_id, run_id):
        assert actor_user_id == USER_ID
        assert project_id == PROJECT_ID
        snapshot = self.store.current_snapshot(project_id)
        if snapshot is None or snapshot.analysis_run_id != run_id:
            raise AssertionError("snapshot missing")
        return snapshot

    def get_artifact(self, *, actor_user_id, project_id, artifact_type):
        snapshot = self.current_overview(
            actor_user_id=actor_user_id,
            project_id=project_id,
        )
        artifact = next(
            item for item in snapshot.artifacts if item.artifact_type.value == artifact_type
        )
        return {
            "artifact_type": artifact_type,
            "title": artifact.title,
            "content": {
                "sections": [
                    {
                        "heading": "",
                        "body": artifact.summary,
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    }
                ]
            },
            "version": 1,
            "provenance": "from_oslo",
            "reliability": artifact.reliability,
            "basis": artifact.basis,
            "evidence_refs": list(artifact.evidence_refs),
            "evidence_citations": list(snapshot.evidence_citations),
            "issues": [
                issue
                for issue in snapshot.assessment.issues
                if issue.artifact_type.value == artifact_type
            ],
            "updated_at": snapshot.published_at,
        }

    def update_artifact(
        self,
        *,
        actor_user_id,
        project_id,
        artifact_type,
        content,
        expected_version,
        key,
    ):
        artifact = self.get_artifact(
            actor_user_id=actor_user_id,
            project_id=project_id,
            artifact_type=artifact_type,
        )
        artifact.update(
            content=content,
            version=expected_version + 1,
            provenance="confirmed_by_user",
        )
        run = self.store.create_run(
            AnalysisRunRequest(
                workspace_id=WORKSPACE_ID,
                project_id=project_id,
                requested_by=actor_user_id,
                kind=RunKind.EXTENDED,
                description=str(content),
                source_names=(),
                idempotency_key=f"artifact-edit:{key}",
            )
        )
        return artifact, run


def test_orientation_state_is_available_before_the_overview_is_published() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.orientation_seen = True
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/orientation-seen",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json() == {"seen": True}


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


class ConflictingArtifactSliceTwo(RecordingSliceTwo):
    def update_artifact(self, **kwargs):
        raise SliceTwoArtifactConflict


class BusyArtifactSliceTwo(RecordingSliceTwo):
    def update_artifact(self, **kwargs):
        raise SliceTwoAnalysisInProgress


class ConflictingIssueActionSliceTwo(RecordingSliceTwo):
    def act_on_issue(self, **kwargs):
        raise SliceTwoArtifactConflict


def test_authenticated_user_starts_analysis_idempotently() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))
    headers = {
        "Authorization": "Bearer valid-access-token",
        "Idempotency-Key": "intake-submit-001",
    }
    payload = {
        "kind": "initial",
        "provisional": True,
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
    assert slice_two.started[0].provisional is True


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


def test_authenticated_user_lists_append_only_project_history() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.history = {
        "project_id": str(PROJECT_ID),
        "groups": [
            {
                "run_id": "018f9f7e-8de2-7000-8000-000000000040",
                "kind": "extended",
                "status": "completed",
                "current": True,
                "occurred_at": "2026-07-26T10:00:00Z",
                "confidence_index": 62,
                "confidence_band": "Moderate",
                "confidence_direction": "up",
                "understanding_stage": "expanded",
                "changes": [{"label": "Feasibility Very Low → Low", "tone": "positive"}],
                "events": [
                    {
                        "id": 9,
                        "category": "analysis",
                        "event_type": "analysis.extended_completed",
                        "summary": "Extended Analysis complete",
                        "detail": "The deeper evidence read is now current.",
                        "actor_type": "oslo",
                        "artifact_type": None,
                        "artifact_version": None,
                        "issue_id": None,
                        "occurred_at": "2026-07-26T10:00:00Z",
                    }
                ],
            }
        ],
        "trend": [
            {
                "run_id": "018f9f7e-8de2-7000-8000-000000000040",
                "confidence_index": 62,
                "confidence_band": "Moderate",
                "direction": "up",
                "cause": "Feasibility rose from Very Low to Low.",
                "occurred_at": "2026-07-26T10:00:00Z",
                "current": True,
            }
        ],
        "next_cursor": None,
    }
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/history?category=analysis",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json() == slice_two.history


def test_project_history_accepts_collaboration_events() -> None:
    class CollaborationHistorySliceTwo(RecordingSliceTwo):
        def list_history(
            self,
            *,
            actor_user_id,
            project_id,
            category,
            cursor,
            limit,
        ):
            assert actor_user_id == USER_ID
            assert project_id == PROJECT_ID
            assert category == "collaboration"
            assert cursor is None
            assert limit == 25
            return self.history

    slice_two = CollaborationHistorySliceTwo()
    slice_two.history = {
        "project_id": str(PROJECT_ID),
        "groups": [
            {
                "run_id": "018f9f7e-8de2-7000-8000-000000000040",
                "kind": "extended",
                "status": "completed",
                "current": True,
                "occurred_at": "2026-07-26T10:00:00Z",
                "confidence_index": 62,
                "confidence_band": "Moderate",
                "confidence_direction": "up",
                "understanding_stage": "expanded",
                "changes": [],
                "events": [
                    {
                        "id": 10,
                        "category": "collaboration",
                        "event_type": "reviewer.approved",
                        "summary": "Reviewer approved",
                        "detail": "The project review was approved.",
                        "actor_type": "user",
                        "artifact_type": None,
                        "artifact_version": None,
                        "issue_id": None,
                        "occurred_at": "2026-07-26T10:05:00Z",
                    }
                ],
            }
        ],
        "trend": [],
        "next_cursor": None,
    }
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/history?category=collaboration",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json() == slice_two.history


def test_project_history_rejects_a_malformed_cursor() -> None:
    class InvalidCursorSliceTwo(RecordingSliceTwo):
        def list_history(
            self,
            *,
            actor_user_id,
            project_id,
            category,
            cursor,
            limit,
        ):
            assert actor_user_id == USER_ID
            assert project_id == PROJECT_ID
            assert category == "all"
            assert cursor == "not-a-history-cursor"
            assert limit == 25
            raise ValueError("INVALID_HISTORY_CURSOR")

    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            slice_two=InvalidCursorSliceTwo(),
        )
    )

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/history?cursor=not-a-history-cursor",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "History cursor is invalid"}


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


def test_authenticated_user_can_withdraw_a_pending_act_without_relatching_freeze() -> None:
    event_id = UUID("018f9f7e-8de2-7000-8000-000000000077")
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    response = client.delete(
        f"/v1/projects/{PROJECT_ID}/acts/{event_id}",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "event_id": str(event_id),
        "state": "withdrawn",
        "pending_count": 0,
        "grounding_act_count": 1,
        "ever_unlocked": True,
        "freeze_on": False,
    }


def test_authenticated_user_selects_and_applies_an_issue_resolution() -> None:
    slice_two = RecordingSliceTwo()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    selected = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-001/actions",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "issue-resolution-001",
        },
        json={
            "action": "select",
            "resolution": "Assign Priya as the accountable migration owner.",
        },
    )
    applied = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-001/actions",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "issue-resolution-apply-001",
        },
        json={
            "action": "apply",
            "resolution": "Assign Priya as the accountable migration owner.",
        },
    )
    persisted = client.get(
        f"/v1/projects/{PROJECT_ID}/issue-actions",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert selected.status_code == 202
    assert selected.json() == {
        "issue_id": "ISS-001",
        "action": "select",
        "status": "addressed",
        "selected_resolution": "Assign Priya as the accountable migration owner.",
        "analysis_run": None,
    }
    assert applied.status_code == 202
    assert applied.json()["analysis_run"]["kind"] == "extended"
    assert persisted.status_code == 200
    assert persisted.json()[0]["issue_id"] == "ISS-001"
    assert persisted.json()[0]["selected_resolution"] == (
        "Assign Priya as the accountable migration owner."
    )


def test_authenticated_user_enqueues_a_typed_flag_attestation() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-001/acts",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "issue-lifecycle-flag-001",
        },
        json={
            "act": "flag",
            "basis": "documented",
            "evidence_ref": "evidence:registration-export",
        },
    )

    assert response.status_code == 202
    assert response.json()["status"] == "addressed"
    assert response.json()["attestation"] == {
        "id": "attestation-001",
        "act": "flag",
        "basis": "documented",
        "evidence_ref": "evidence:registration-export",
        "attributed_to": {
            "id": str(USER_ID),
            "display_name": "Member",
            "role": "owner",
        },
        "supersedes": None,
    }
    assert response.json()["analysis_run"]["kind"] == "extended"


def test_proposal_decision_is_shared_across_surfaces_and_reanalyzed() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    listed = client.get(
        f"/v1/projects/{PROJECT_ID}/proposals",
        headers={"Authorization": "Bearer valid-access-token"},
    )
    decided = client.post(
        f"/v1/projects/{PROJECT_ID}/proposals/"
        "018f9f7e-8de2-7000-8000-000000000155/decisions",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "proposal-decision-001",
        },
        json={"accepted": True, "surface": "artifact"},
    )

    assert listed.status_code == 200
    assert listed.json()[0]["accepted"] is False
    assert decided.status_code == 202
    assert decided.json()["proposal"]["accepted"] is True
    assert decided.json()["proposal"]["surface"] == "artifact"
    assert decided.json()["analysis_run"]["kind"] == "extended"


def test_issue_resolution_rejects_a_stale_artifact_version_safely() -> None:
    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            slice_two=ConflictingIssueActionSliceTwo(),
        )
    )

    response = client.post(
        f"/v1/projects/{PROJECT_ID}/issues/ISS-001/actions",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "issue-resolution-conflict-001",
        },
        json={
            "action": "apply",
            "resolution": "Assign Priya as the accountable migration owner.",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "ARTIFACT_VERSION_CONFLICT"


def test_overview_overlays_the_saved_resolution_and_addressed_status() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="Migration ownership is unresolved.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="issue-action-overview-001",
    )
    slice_two.complete_latest()
    snapshot = slice_two.store.current_snapshot(PROJECT_ID)
    assert snapshot is not None
    issue_id = snapshot.assessment.issues[0].id
    slice_two.issue_actions = [
        {
            "issue_id": issue_id,
            "action": "select",
            "status": "addressed",
            "selected_resolution": "Assign Priya as the accountable migration owner.",
            "analysis_run": None,
        }
    ]
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/overview",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    issue = response.json()["assessment"]["issues"][0]
    assert issue["status"] == "addressed"
    assert issue["selected_resolution"] == ("Assign Priya as the accountable migration owner.")


def test_history_snapshot_does_not_overlay_current_issue_actions() -> None:
    slice_two = RecordingSliceTwo()
    run = slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="Migration ownership is unresolved.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="historical-issue-state-001",
    )
    slice_two.complete_latest()
    snapshot = slice_two.store.current_snapshot(PROJECT_ID)
    assert snapshot is not None
    issue_id = snapshot.assessment.issues[0].id
    slice_two.issue_actions = [
        {
            "issue_id": issue_id,
            "action": "select",
            "status": "addressed",
            "selected_resolution": "Assign Priya as the migration owner.",
            "analysis_run": None,
        }
    ]
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/history/runs/{run.id}",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    issue = response.json()["assessment"]["issues"][0]
    assert issue["status"] == "open"
    assert issue["selected_resolution"] is None


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
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

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
        "pass_kind": "fast",
        "trigger": "intake",
        "consolidated_event_ids": [],
        "provisional": False,
        "auto_retry_count": 0,
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
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

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
    integrity = assessment["integrity"]
    assert integrity["level"] in {
        "Fragile",
        "Weak",
        "Developing",
        "Solid",
        "Sound",
    }
    assert integrity["limiting_pillar"] in {
        "Viability",
        "Grounding",
        "Adaptability",
    }
    assert [pillar["key"] for pillar in integrity["decomposition"]] == [
        "Viability",
        "Grounding",
        "Adaptability",
    ]
    assert integrity["posture"] == "moment-in-time"
    assert integrity["tracking"] == "pending-execution"
    checkpoint_issue = next(
        issue for issue in assessment["issues"] if issue["id"].startswith("ISS-CP-")
    )
    assert checkpoint_issue["pillar"] == "Adaptability"
    assert checkpoint_issue["finding_type"] == "Coverage Gap"
    assert checkpoint_issue["section"] == "Schedule"
    assert checkpoint_issue["recommendation_from_oslo"] is True
    assert checkpoint_issue["exposure_rank"] > 0
    provenance = response.json()["provenance"]
    assert provenance["schema_version"] == 1
    assert len(provenance["artifacts"]) == 7
    assert provenance["total_claims"] == (
        provenance["grounded_claims"] + provenance["inferred_claims"]
    )


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
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

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


def test_artifact_workspace_loads_and_autosave_starts_reanalysis() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="A launch plan with an unresolved owner.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="slice-five-artifact-seed",
    )
    slice_two.complete_latest()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    loaded = client.get(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={"Authorization": "Bearer valid-access-token"},
    )
    saved = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-001",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "",
                        "body": "Launch the service with a named owner.",
                        "bullets": ["Owner confirmed before launch."],
                        "columns": [],
                        "rows": [],
                        "provenance": "confirmed_by_user",
                        "row_provenance": [],
                    }
                ]
            },
        },
    )

    assert loaded.status_code == 200
    assert loaded.json()["artifact_type"] == "intent"
    assert loaded.json()["provenance"] == "from_oslo"
    assert loaded.json()["content"]["sections"][0]["provenance"] == "from_oslo"
    assert saved.status_code == 202
    assert saved.json()["version"] == 2
    assert saved.json()["provenance"] == "confirmed_by_user"
    assert saved.json()["content"]["sections"][0]["provenance"] == "confirmed_by_user"
    assert saved.json()["analysis_run"]["kind"] == "extended"


def test_artifact_workspace_reads_source_grounded_rows_from_structured_extraction() -> None:
    class SourceGroundedArtifactSliceTwo(RecordingSliceTwo):
        def get_artifact(self, **kwargs):
            artifact = super().get_artifact(**kwargs)
            artifact["content"] = {
                "sections": [
                    {
                        "heading": "Objectives",
                        "body": "",
                        "bullets": [],
                        "columns": ["ID", "Objective"],
                        "rows": [["OBJ-01", "Launch the portal"]],
                        "row_states": ["source_grounded"],
                        "row_evidence_refs": [["document:charter:page:1"]],
                    }
                ]
            }
            return artifact

    slice_two = SourceGroundedArtifactSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="A grounded launch objective.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="source-grounded-artifact-seed",
    )
    slice_two.complete_latest()
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["content"]["sections"][0]["row_states"] == ["confirmed"]


def test_artifact_workspace_returns_readable_issue_evidence() -> None:
    slice_two = RecordingSliceTwo()
    slice_two.start_analysis(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
        description="A launch plan has an unresolved owner and delivery dependency.",
        source_names=(),
        source_document_ids=(),
        kind=RunKind.INITIAL,
        key="slice-five-evidence-seed",
    )
    slice_two.complete_latest()
    snapshot = slice_two.current_overview(
        actor_user_id=USER_ID,
        project_id=PROJECT_ID,
    )
    issue = snapshot.assessment.issues[0]
    slice_two.issue_actions = [
        {
            "issue_id": issue.id,
            "action": "select",
            "status": "addressed",
            "selected_resolution": "Confirm the accountable delivery owner.",
            "analysis_run": None,
        }
    ]
    client = TestClient(create_app(slice_one=AuthenticatedSliceOne(), slice_two=slice_two))

    response = client.get(
        f"/v1/projects/{PROJECT_ID}/artifacts/{issue.artifact_type.value}",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    returned_issue = next(item for item in response.json()["issues"] if item["id"] == issue.id)
    assert returned_issue["evidence"]
    assert returned_issue["evidence"][0]["source_name"] == "Project description"
    assert returned_issue["status"] == "addressed"
    assert returned_issue["selected_resolution"] == "Confirm the accountable delivery owner."


def test_artifact_workspace_rejects_malformed_table_rows() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    response = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/schedule",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-invalid",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "Milestones",
                        "body": "",
                        "bullets": [],
                        "columns": ["Milestone", "Date", "Status"],
                        "rows": [["Launch", "1 July"]],
                    }
                ]
            },
        },
    )

    assert response.status_code == 422


def test_artifact_workspace_rejects_misaligned_row_provenance() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    invalid_response = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/schedule",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-misaligned-provenance",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "Milestones",
                        "body": "",
                        "bullets": [],
                        "columns": ["Milestone", "Date"],
                        "rows": [["Launch", "1 July"]],
                        "row_provenance": [
                            "from_oslo",
                            "confirmed_by_user",
                        ],
                    }
                ]
            },
        },
    )

    assert invalid_response.status_code == 422


def test_artifact_workspace_rejects_a_heading_only_section() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=RecordingSliceTwo())
    )

    response = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-empty-section",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "New section",
                        "body": "   ",
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    }
                ]
            },
        },
    )

    assert response.status_code == 422
    assert "needs body text" in response.text


def test_artifact_workspace_rejects_a_stale_version() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=ConflictingArtifactSliceTwo())
    )

    response = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-stale",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "",
                        "body": "A stale edit.",
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    }
                ]
            },
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "ARTIFACT_VERSION_CONFLICT"


def test_artifact_workspace_rejects_overlapping_reanalysis() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_two=BusyArtifactSliceTwo())
    )

    response = client.patch(
        f"/v1/projects/{PROJECT_ID}/artifacts/intent",
        headers={
            "Authorization": "Bearer valid-access-token",
            "Idempotency-Key": "artifact-save-busy",
        },
        json={
            "expected_version": 1,
            "content": {
                "sections": [
                    {
                        "heading": "",
                        "body": "A material edit while another analysis is active.",
                        "bullets": [],
                        "columns": [],
                        "rows": [],
                    }
                ]
            },
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "ARTIFACT_ANALYSIS_IN_PROGRESS"

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.collaboration.service import CollaborationError
from oslo_api.main import create_app

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000012")
RUN_ID = UUID("018f9f7e-8de2-7000-8000-000000000013")


class AuthenticatedApplication:
    def authenticate(self, access_token: str):
        assert access_token == "valid-access-token"
        return SimpleNamespace(id=USER_ID, email="owner@example.com")


class RecordingCollaboration:
    def __init__(self) -> None:
        self.comment = None
        self.response = None
        self.linked_run = None

    def state(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {
            "actor_role": "owner",
            "plan": {
                "name": "Free",
                "collaborator_seats": 3,
                "collaborator_seats_used": 1,
                "monthly_invites": 2,
                "viewers_unlimited": True,
                "reviewers_unmetered": True,
                "export_formats": ["pdf"],
            },
            "participants": [],
            "comments": [],
            "reviews": [],
            "share_links": [],
        }

    def add_comment(self, **payload):
        self.comment = payload
        return {
            "id": "comment-1",
            "issue_id": payload["issue_id"],
            "body": payload["body"],
            "mentions": payload["mentions"],
            "created_at": datetime(2026, 7, 27, tzinfo=UTC),
        }

    def respond_to_review(self, *, token, kind, body):
        self.response = (token, kind, body)
        return {
            "id": "018f9f7e-8de2-7000-8000-000000000014",
            "created_by": str(USER_ID),
            "project_id": str(PROJECT_ID),
            "issue_id": "issue-1",
            "reviewer_name": "Amina",
            "response_kind": kind,
            "body": body,
        }

    def link_review_run(self, *, response_id, run_id):
        self.linked_run = (response_id, run_id)


class RecordingAnalysis:
    def __init__(self) -> None:
        self.attestation = None

    def apply_reviewer_attestation(
        self,
        *,
        actor_user_id,
        project_id,
        issue_id,
        reviewer_name,
        response_kind,
        body,
        key,
    ):
        self.attestation = {
            "actor_user_id": actor_user_id,
            "project_id": project_id,
            "issue_id": issue_id,
            "reviewer_name": reviewer_name,
            "response_kind": response_kind,
            "body": body,
            "key": key,
        }
        return SimpleNamespace(id=RUN_ID, status="queued")


def client_for(
    collaboration: RecordingCollaboration,
    analysis: RecordingAnalysis | None = None,
) -> TestClient:
    return TestClient(
        create_app(
            slice_one=AuthenticatedApplication(),
            slice_two=analysis,
            collaboration=collaboration,
        )
    )


def test_collaboration_state_is_authenticated_and_exposes_plan_boundaries() -> None:
    response = client_for(RecordingCollaboration()).get(
        f"/v1/projects/{PROJECT_ID}/collaboration",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["plan"] == {
        "name": "Free",
        "collaborator_seats": 3,
        "collaborator_seats_used": 1,
        "monthly_invites": 2,
        "viewers_unlimited": True,
        "reviewers_unmetered": True,
        "export_formats": ["pdf"],
    }


def test_issue_comment_is_append_only_and_keeps_mentions() -> None:
    collaboration = RecordingCollaboration()
    response = client_for(collaboration).post(
        f"/v1/projects/{PROJECT_ID}/issues/issue-1/comments",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"body": "Please confirm this with @amina.", "mentions": ["amina"]},
    )

    assert response.status_code == 201
    assert collaboration.comment == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
        "issue_id": "issue-1",
        "body": "Please confirm this with @amina.",
        "mentions": ["amina"],
    }


def test_reviewer_response_becomes_attested_evidence_and_queues_analysis() -> None:
    collaboration = RecordingCollaboration()
    analysis = RecordingAnalysis()
    response = client_for(collaboration, analysis).post(
        "/v1/public/review/review-token/responses",
        json={
            "kind": "approve",
            "body": "The steering committee approved the pilot.",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "response_id": "018f9f7e-8de2-7000-8000-000000000014",
        "analysis_run_id": str(RUN_ID),
        "status": "queued",
    }
    assert analysis.attestation["response_kind"] == "approve"
    assert analysis.attestation["reviewer_name"] == "Amina"
    assert analysis.attestation["key"] == "018f9f7e-8de2-7000-8000-000000000014"
    assert collaboration.linked_run is not None


def test_expired_public_review_fails_closed() -> None:
    class ExpiredReview(RecordingCollaboration):
        def respond_to_review(self, **_payload):
            raise CollaborationError(
                "REVIEW_LINK_EXPIRED",
                "This review link has expired.",
                410,
            )

    response = client_for(ExpiredReview(), RecordingAnalysis()).post(
        "/v1/public/review/expired/responses",
        json={"kind": "comment", "body": "Late response"},
    )

    assert response.status_code == 410
    assert response.json()["detail"]["code"] == "REVIEW_LINK_EXPIRED"

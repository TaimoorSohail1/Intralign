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
        self.saved_report = None
        self.report_delivery = None
        self.review_delivery = None
        self.asana_import = None

    def state(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {
            "actor_role": "owner",
            "plan": {
                "name": "Free",
                "collaborators_unmetered": True,
                "invitations_unmetered": True,
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

    def roll_up(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {"integrity": {"limiting_pillar": "Grounding"}, "decision_queue": []}

    def grounding_map(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {"counts": {"inferred": 1}, "nodes": []}

    def resolve_review(self, token):
        assert token == "review-token"
        return {
            "id": "review-request-1",
            "reviewer_name": "Amina",
            "project_name": "Transformation",
            "expires_at": datetime(2026, 8, 21, tzinfo=UTC),
            "question": "Is the steering committee decision confirmed?",
            "source": {
                "reference": "brief.md#decision-log",
                "excerpt": "The steering committee decision is due on 20 August.",
            },
            "response_kind": None,
            "snapshot_json": {"summary": "This must never cross the scoped boundary."},
            "issue_id": "issue-1",
            "project_id": str(PROJECT_ID),
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

    def mark_review_delivered(self, **payload):
        self.review_delivery = payload
        return {
            "id": str(payload["grant_id"]),
            "delivery_state": "awaiting",
            "delivery_attempts": 0,
            "delivered_at": datetime(2026, 8, 14, tzinfo=UTC),
        }

    def review_response_for_evidence(self, *, actor_user_id, project_id, response_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        assert response_id == UUID("018f9f7e-8de2-7000-8000-000000000014")
        return {
            "id": str(response_id),
            "created_by": str(USER_ID),
            "project_id": str(PROJECT_ID),
            "issue_id": "issue-1",
            "reviewer_name": "Amina",
            "response_kind": "approve",
            "body": "The steering committee approved the pilot.",
            "analysis_run_id": None,
        }

    def report_state(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {
            "project_id": str(PROJECT_ID),
            "project_name": "Transformation",
            "snapshot_id": str(RUN_ID),
            "content": self.saved_report["content"] if self.saved_report else None,
            "updated_at": None,
            "analysis_completed_at": datetime(2026, 7, 27, tzinfo=UTC),
            "deliveries": [],
        }

    def save_report(self, **payload):
        self.saved_report = payload
        return {
            "project_id": str(PROJECT_ID),
            "snapshot_id": str(payload["snapshot_id"]),
            "content": payload["content"],
            "updated_at": datetime(2026, 7, 27, tzinfo=UTC),
        }

    def deliver_report(self, **payload):
        self.report_delivery = payload
        return {
            "id": "delivery-1",
            "recipient_email": payload["recipient_email"],
            "recipient_label": payload["recipient_label"],
            "status": "sent",
            "scheduled_for": datetime(2026, 7, 27, tzinfo=UTC),
            "sent_at": datetime(2026, 7, 27, tzinfo=UTC),
            "error_code": None,
            "created_at": datetime(2026, 7, 27, tzinfo=UTC),
        }

    def report_schedules(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return []

    def create_report_schedule(self, **payload):
        self.report_schedule = payload
        return {
            "id": "018f9f7e-8de2-7000-8000-000000000099",
            "recipient_email": payload["recipient_email"],
            "recipient_class": payload["recipient_class"],
            "weekday": payload["weekday"],
            "local_time": payload["local_time"].isoformat(),
            "timezone": payload["timezone"],
            "state": "enabled",
            "next_run_at": datetime(2026, 7, 28, 8, 0, tzinfo=UTC),
            "last_run_at": None,
            "last_delivery_id": None,
            "created_at": datetime(2026, 7, 27, tzinfo=UTC),
            "updated_at": datetime(2026, 7, 27, tzinfo=UTC),
        }

    def update_report_schedule(self, **payload):
        self.updated_report_schedule = payload
        return {"id": str(payload["schedule_id"]), "state": payload["state"]}

    def delete_report_schedule(self, **payload):
        self.deleted_report_schedule = payload

    def record_report_export(self, **payload):
        self.report_export = payload
        return {
            "id": "export-1",
            "format": payload["export_format"],
            "status": "completed",
        }

    def asana_handoff_state(self, *, actor_user_id, project_id):
        assert (actor_user_id, project_id) == (USER_ID, PROJECT_ID)
        return {
            "configured": True,
            "entitled": True,
            "destination_gid": "asana-project-1",
            "snapshot_id": str(RUN_ID),
            "preview": [{"task": "Confirm launch", "owner": "Maya"}],
            "latest": None,
        }

    def import_asana_handoff(self, **payload):
        self.asana_import = payload
        return {
            "id": "handoff-1",
            "state": "completed",
            "total_count": 1,
            "completed_count": 1,
            "safe_error_code": None,
            "destination_gid": "asana-project-1",
        }


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
        "collaborators_unmetered": True,
        "invitations_unmetered": True,
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


def test_report_draft_and_delivery_are_server_backed() -> None:
    collaboration = RecordingCollaboration()
    client = client_for(collaboration)
    content = {
        "sections": [
            {"id": f"section-{index}", "title": f"Section {index}", "body": ["Detail"]}
            for index in range(7)
        ]
    }

    saved = client.put(
        f"/v1/projects/{PROJECT_ID}/report",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"snapshot_id": str(RUN_ID), "content": content},
    )
    delivered = client.post(
        f"/v1/projects/{PROJECT_ID}/report/deliveries",
        headers={"Authorization": "Bearer valid-access-token"},
        json={
            "snapshot_id": str(RUN_ID),
            "recipient_email": "sponsor@example.com",
            "recipient_label": "Sponsor",
            "subject": "Transformation readout",
            "content": content,
            "confirm_previous_analysis": True,
        },
    )

    assert saved.status_code == 200
    assert saved.json()["content"] == content
    assert delivered.status_code == 201
    assert delivered.json()["status"] == "sent"
    assert collaboration.report_delivery["recipient_email"] == "sponsor@example.com"
    assert collaboration.report_delivery["confirm_previous_analysis"] is True


def test_weekly_report_schedule_has_a_typed_authenticated_contract() -> None:
    collaboration = RecordingCollaboration()
    client = client_for(collaboration)
    schedule_id = "018f9f7e-8de2-7000-8000-000000000099"

    created = client.post(
        f"/v1/projects/{PROJECT_ID}/report/schedules",
        headers={"Authorization": "Bearer valid-access-token"},
        json={
            "recipient_email": "sponsor@example.com",
            "recipient_class": "exec-sponsor",
            "weekday": 1,
            "local_time": "13:30:00",
            "timezone": "Asia/Karachi",
        },
    )
    paused = client.patch(
        f"/v1/projects/{PROJECT_ID}/report/schedules/{schedule_id}",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"state": "paused"},
    )
    removed = client.delete(
        f"/v1/projects/{PROJECT_ID}/report/schedules/{schedule_id}",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert created.status_code == 201
    assert created.json()["state"] == "enabled"
    assert collaboration.report_schedule["timezone"] == "Asia/Karachi"
    assert paused.status_code == 200
    assert paused.json()["state"] == "paused"
    assert removed.status_code == 204
    assert collaboration.deleted_report_schedule["schedule_id"] == UUID(schedule_id)


def test_weekly_report_schedule_rejects_invalid_day_and_timezone_shape() -> None:
    response = client_for(RecordingCollaboration()).post(
        f"/v1/projects/{PROJECT_ID}/report/schedules",
        headers={"Authorization": "Bearer valid-access-token"},
        json={
            "recipient_email": "sponsor@example.com",
            "recipient_class": "exec-sponsor",
            "weekday": 7,
            "local_time": "13:30:00",
            "timezone": "",
        },
    )

    assert response.status_code == 422


def test_report_export_is_recorded_without_storing_the_file() -> None:
    collaboration = RecordingCollaboration()
    response = client_for(collaboration).post(
        f"/v1/projects/{PROJECT_ID}/report/exports",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"format": "csv", "content_checksum": "abc123"},
    )

    assert response.status_code == 201
    assert response.json() == {"id": "export-1", "format": "csv", "status": "completed"}
    assert collaboration.report_export["content_checksum"] == "abc123"


def test_asana_handoff_has_preview_and_idempotent_import_contracts() -> None:
    collaboration = RecordingCollaboration()
    client = client_for(collaboration)
    headers = {"Authorization": "Bearer valid-access-token"}

    preview = client.get(f"/v1/projects/{PROJECT_ID}/report/asana", headers=headers)
    imported = client.post(f"/v1/projects/{PROJECT_ID}/report/asana", headers=headers)

    assert preview.status_code == 200
    assert preview.json()["preview"] == [{"task": "Confirm launch", "owner": "Maya"}]
    assert imported.status_code == 201
    assert imported.json()["state"] == "completed"
    assert collaboration.asana_import == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
    }


def test_report_export_uses_a_header_safe_unicode_filename() -> None:
    class UnicodeReport(RecordingCollaboration):
        def report_state(self, *, actor_user_id, project_id):
            state = super().report_state(
                actor_user_id=actor_user_id,
                project_id=project_id,
            )
            return {
                **state,
                "project_name": "Project Lumen — Student Experience",
                "content": {
                    "sections": [
                        {
                            "id": f"section-{index}",
                            "title": f"Section {index}",
                            "body": ["Detail"],
                        }
                        for index in range(7)
                    ]
                },
            }

    response = client_for(UnicodeReport()).get(
        f"/v1/projects/{PROJECT_ID}/reports/pdf",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    disposition = response.headers["content-disposition"]
    assert "—" not in disposition
    assert "filename*=UTF-8''Project%20Lumen%20%E2%80%94%20Student" in disposition


def test_reviewer_confirmation_is_attributed_and_queues_reanalysis() -> None:
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
    assert analysis.attestation == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
        "issue_id": "issue-1",
        "reviewer_name": "Amina",
        "response_kind": "approve",
        "body": "The steering committee approved the pilot.",
        "key": "review:018f9f7e-8de2-7000-8000-000000000014",
    }
    assert collaboration.linked_run == (
        UUID("018f9f7e-8de2-7000-8000-000000000014"),
        RUN_ID,
    )


def test_reviewer_rejection_is_attributed_and_queues_reanalysis() -> None:
    collaboration = RecordingCollaboration()
    analysis = RecordingAnalysis()
    response = client_for(collaboration, analysis).post(
        "/v1/public/review/review-token/responses",
        json={"kind": "reject", "body": "The cited decision was not approved."},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "queued"
    assert analysis.attestation == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
        "issue_id": "issue-1",
        "reviewer_name": "Amina",
        "response_kind": "reject",
        "body": "The cited decision was not approved.",
        "key": "review:018f9f7e-8de2-7000-8000-000000000014",
    }


def test_manual_review_delivery_is_server_confirmed_before_awaiting() -> None:
    collaboration = RecordingCollaboration()
    grant_id = UUID("018f9f7e-8de2-7000-8000-000000000015")

    response = client_for(collaboration).post(
        f"/v1/projects/{PROJECT_ID}/review-grants/{grant_id}/deliveries/manual",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["delivery_state"] == "awaiting"
    assert collaboration.review_delivery == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
        "grant_id": grant_id,
    }


def test_collaboration_projections_are_authenticated_read_models() -> None:
    client = client_for(RecordingCollaboration())
    headers = {"Authorization": "Bearer valid-access-token"}

    roll_up = client.get(
        f"/v1/projects/{PROJECT_ID}/collaboration/roll-up",
        headers=headers,
    )
    grounding_map = client.get(
        f"/v1/projects/{PROJECT_ID}/collaboration/grounding-map",
        headers=headers,
    )

    assert roll_up.status_code == 200
    assert roll_up.json()["integrity"]["limiting_pillar"] == "Grounding"
    assert grounding_map.status_code == 200
    assert grounding_map.json()["counts"]["inferred"] == 1
def test_scoped_public_review_exposes_only_question_and_source() -> None:
    response = client_for(RecordingCollaboration()).get(
        "/v1/public/review/review-token"
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "review-request-1",
        "reviewer_name": "Amina",
        "project_name": "Transformation",
        "expires_at": "2026-08-21T00:00:00Z",
        "question": "Is the steering committee decision confirmed?",
        "source": {
            "reference": "brief.md#decision-log",
            "excerpt": "The steering committee decision is due on 20 August.",
        },
        "response_kind": None,
    }


def test_reviewer_comment_stays_discussion_only() -> None:
    collaboration = RecordingCollaboration()
    analysis = RecordingAnalysis()

    response = client_for(collaboration, analysis).post(
        "/v1/public/review/review-token/responses",
        json={"kind": "comment", "body": "Could you clarify the cited date?"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "recorded"
    assert response.json()["analysis_run_id"] is None
    assert analysis.attestation is None
    assert collaboration.linked_run == (
        UUID("018f9f7e-8de2-7000-8000-000000000014"),
        None,
    )


def test_project_team_explicitly_promotes_review_response_to_project_evidence() -> None:
    collaboration = RecordingCollaboration()
    analysis = RecordingAnalysis()
    response = client_for(collaboration, analysis).post(
        (
            f"/v1/projects/{PROJECT_ID}/review-responses/"
            "018f9f7e-8de2-7000-8000-000000000014/evidence"
        ),
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 202
    assert response.json() == {
        "response_id": "018f9f7e-8de2-7000-8000-000000000014",
        "analysis_run_id": str(RUN_ID),
        "status": "queued",
    }
    assert analysis.attestation == {
        "actor_user_id": USER_ID,
        "project_id": PROJECT_ID,
        "issue_id": "issue-1",
        "reviewer_name": "Amina",
        "response_kind": "approve",
        "body": "The steering committee approved the pilot.",
        "key": "review:018f9f7e-8de2-7000-8000-000000000014",
    }
    assert collaboration.linked_run == (
        UUID("018f9f7e-8de2-7000-8000-000000000014"),
        RUN_ID,
    )


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

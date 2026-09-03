from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.feedback import FeedbackCategory, FeedbackContext, FeedbackTicket
from oslo_api.main import create_app
from oslo_api.slice_one import AuthenticatedUser, SessionContext

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
HEADERS = {"Authorization": "Bearer valid-access-token"}


class AuthenticatedSliceOne:
    def authenticate(self, access_token: str) -> AuthenticatedUser:
        assert access_token == "valid-access-token"
        return AuthenticatedUser(id=USER_ID, email="owner@example.com")

    def get_session_context(self, *, actor_user_id: UUID) -> SessionContext:
        assert actor_user_id == USER_ID
        return SessionContext(
            user_id=USER_ID,
            email="owner@example.com",
            workspace_id=WORKSPACE_ID,
            display_name="Owner",
            account_role="owner",
            welcome_required=False,
        )


class RecordingFeedbackApplication:
    def __init__(self) -> None:
        self.requests = []
        self.tickets = []

    def file_ticket(self, **kwargs) -> FeedbackTicket:
        self.requests.append(kwargs)
        ticket = FeedbackTicket(
            id=UUID("018f9f7e-8de2-7000-8000-000000000012"),
            ticket_id="ENH-0001",
            actor_user_id=kwargs["actor_user_id"],
            workspace_id=kwargs["workspace_id"],
            session_id=kwargs["session_id"],
            category=kwargs["category"],
            title="The audience control should stay selected.",
            body="The audience control should stay selected.",
            expected=kwargs["expected"],
            impact=kwargs["impact"],
            context=kwargs["context"],
            status="Filed",
            created_at=datetime(2026, 8, 16, 9, 30, tzinfo=UTC),
        )
        self.tickets.append(ticket)
        return ticket

    def list_session_tickets(self, **_kwargs) -> list[FeedbackTicket]:
        return list(self.tickets)


def test_authenticated_feedback_round_trip_returns_server_ticket_and_session_list() -> None:
    feedback = RecordingFeedbackApplication()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), feedback=feedback)
    )
    payload = {
        "session_id": "browser-session-001",
        "category": "enhancement",
        "body": "The audience control should stay selected.",
        "expected": "Keep the selected audience visible.",
        "impact": "slowing",
        "context": {
            "where": "Reports",
            "view": "reports",
            "role": "owner",
            "grounded_x": 4,
            "total_y": 13,
            "first_run_flag": False,
            "ts": "2026-08-16T09:29:00Z",
        },
    }

    response = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/feedback/tickets",
        headers=HEADERS,
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["ticket_id"] == "ENH-0001"
    assert response.json()["status"] == "Filed"
    assert feedback.requests[0]["category"] is FeedbackCategory.ENHANCEMENT
    assert feedback.requests[0]["expected"] is None
    assert feedback.requests[0]["impact"] is None
    assert feedback.requests[0]["context"] == FeedbackContext(**payload["context"])

    listed = client.get(
        f"/v1/workspaces/{WORKSPACE_ID}/feedback/tickets",
        headers=HEADERS,
        params={"session_id": "browser-session-001"},
    )
    assert listed.status_code == 200
    assert [item["ticket_id"] for item in listed.json()] == ["ENH-0001"]


def test_feedback_rejects_a_workspace_outside_the_authenticated_session() -> None:
    client = TestClient(
        create_app(
            slice_one=AuthenticatedSliceOne(),
            feedback=RecordingFeedbackApplication(),
        )
    )

    response = client.post(
        "/v1/workspaces/018f9f7e-8de2-7000-8000-000000000099/feedback/tickets",
        headers=HEADERS,
        json={
            "session_id": "browser-session-001",
            "category": "other",
            "body": "A note",
            "expected": None,
            "impact": None,
            "context": {
                "where": "History",
                "view": "history",
                "role": "owner",
                "grounded_x": 4,
                "total_y": 13,
                "first_run_flag": False,
                "ts": "2026-08-16T09:29:00Z",
            },
        },
    )

    assert response.status_code == 403

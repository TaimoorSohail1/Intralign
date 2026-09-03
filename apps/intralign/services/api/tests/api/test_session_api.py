from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.main import create_app
from oslo_api.slice_one import AuthenticatedUser, SessionContext

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")


class SessionApplication:
    def __init__(self, role: str) -> None:
        self.role = role

    def authenticate(self, access_token: str) -> AuthenticatedUser:
        assert access_token == "valid-access-token"
        return AuthenticatedUser(id=USER_ID, email=f"{self.role}@example.com")

    def get_session_context(self, *, actor_user_id: UUID) -> SessionContext:
        assert actor_user_id == USER_ID
        return SessionContext(
            user_id=USER_ID,
            email=f"{self.role}@example.com",
            workspace_id=WORKSPACE_ID,
            display_name=f"OSLO {self.role.title()}",
            account_role=self.role,
            welcome_required=False,
        )

    def complete_welcome(self, *, actor_user_id: UUID, workspace_id: UUID) -> None:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID


def test_owner_session_resolves_its_real_workspace() -> None:
    response = TestClient(create_app(slice_one=SessionApplication("owner"))).get(
        "/v1/session",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(USER_ID),
        "email": "owner@example.com",
        "workspace_id": str(WORKSPACE_ID),
        "display_name": "OSLO Owner",
        "account_role": "owner",
        "welcome_required": False,
    }


def test_platform_admin_is_distinct_from_workspace_owner() -> None:
    response = TestClient(create_app(slice_one=SessionApplication("admin"))).get(
        "/v1/session",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()["account_role"] == "admin"


def test_owner_can_complete_welcome_without_creating_another_project() -> None:
    response = TestClient(create_app(slice_one=SessionApplication("owner"))).post(
        f"/v1/workspaces/{WORKSPACE_ID}/welcome",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 204

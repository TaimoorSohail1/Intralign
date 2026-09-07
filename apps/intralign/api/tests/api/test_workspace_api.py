from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.application import ActiveProjectLimitReached
from oslo_api.main import create_app
from oslo_api.slice_one import (
    AuthenticatedUser,
    WorkspaceNotification,
    WorkspacePreferences,
    WorkspaceProject,
    WorkspaceSummary,
)
from oslo_api.tiering.policy import get_plan_policy

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
HEADERS = {"Authorization": "Bearer valid-access-token"}


class RecordingWorkspaceApplication:
    def __init__(self) -> None:
        self.archived: list[tuple[UUID, UUID, UUID]] = []
        self.restored: list[tuple[UUID, UUID, UUID]] = []
        self.read_keys: list[str] = []
        self.plan_changes: list[str] = []
        self.preferences = WorkspacePreferences(
            theme="dark",
            analysis_notifications=True,
            failure_notifications=True,
            stale_notifications=True,
            display_name="Workspace member",
            role_title="",
            workspace_name="OSLO Alpha",
            actor_role="owner",
        )

    def authenticate(self, access_token: str) -> AuthenticatedUser:
        assert access_token == "valid-access-token"
        return AuthenticatedUser(id=USER_ID, email="member@example.com")

    def get_workspace_summary(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspaceSummary:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID
        now = datetime(2026, 7, 26, 10, 0, tzinfo=UTC)
        return WorkspaceSummary(
            id=workspace_id,
            name="OSLO Alpha",
            role="owner",
            plan="free",
            projects=[
                WorkspaceProject(
                    id=PROJECT_ID,
                    name="Transformation",
                    status="active",
                    archived=False,
                    updated_at=now,
                    analysis_status="current",
                    confidence_index=62,
                    confidence_band="Moderate",
                    reliability="Moderate",
                    open_issues=4,
                    artifact_count=7,
                    weakest_pillar="Grounding",
                )
            ],
            notifications=[
                WorkspaceNotification(
                    key="analysis:run-1",
                    project_id=PROJECT_ID,
                    project_name="Transformation",
                    kind="extended",
                    status="completed",
                    title="Extended Analysis complete",
                    created_at=now,
                    read=False,
                )
            ],
        )

    def start_first_project(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> None:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID
        raise ActiveProjectLimitReached(get_plan_policy("free"))

    def set_workspace_plan(
        self, *, actor_user_id: UUID, workspace_id: UUID, plan: str
    ) -> WorkspaceSummary:
        self.plan_changes.append(plan)
        return self.get_workspace_summary(
            actor_user_id=actor_user_id, workspace_id=workspace_id
        )

    def archive_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None:
        self.archived.append((actor_user_id, workspace_id, project_id))

    def restore_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None:
        self.restored.append((actor_user_id, workspace_id, project_id))

    def mark_workspace_notifications_read(
        self, *, actor_user_id: UUID, workspace_id: UUID, keys: list[str]
    ) -> None:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID
        self.read_keys.extend(keys)

    def get_workspace_preferences(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspacePreferences:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID
        return self.preferences

    def update_workspace_preferences(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        theme: str,
        analysis_notifications: bool,
        failure_notifications: bool,
        stale_notifications: bool,
        display_name: str,
        role_title: str,
        workspace_name: str,
        mentions_notifications: bool,
        reply_notifications: bool,
        shared_notifications: bool,
    ) -> WorkspacePreferences:
        assert actor_user_id == USER_ID
        assert workspace_id == WORKSPACE_ID
        self.preferences = WorkspacePreferences(
            theme=theme,
            analysis_notifications=analysis_notifications,
            failure_notifications=failure_notifications,
            stale_notifications=stale_notifications,
            display_name=display_name,
            role_title=role_title,
            workspace_name=workspace_name,
            actor_role=self.preferences.actor_role,
            mentions_notifications=mentions_notifications,
            reply_notifications=reply_notifications,
            shared_notifications=shared_notifications,
        )
        return self.preferences


def test_workspace_summary_serializes_projects_and_activity() -> None:
    application = RecordingWorkspaceApplication()
    response = TestClient(create_app(slice_one=application)).get(
        f"/v1/workspaces/{WORKSPACE_ID}", headers=HEADERS
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "OSLO Alpha"
    assert payload["active_project_limit"] == 1
    assert payload["member_count"] == 1
    assert payload["collaborator_seats_used"] == 1
    assert "confidence_index" not in payload["projects"][0]
    assert payload["projects"][0]["weakest_pillar"] == "Grounding"
    assert payload["notifications"][0]["key"] == "analysis:run-1"


def test_second_plan_returns_a_named_commitment_gate() -> None:
    application = RecordingWorkspaceApplication()

    response = TestClient(create_app(slice_one=application)).post(
        f"/v1/workspaces/{WORKSPACE_ID}/projects", headers=HEADERS
    )

    assert response.status_code == 422
    assert response.json()["detail"] == {
        "code": "CAPACITY_COMMITMENT_REQUIRED",
        "wall_key": "multiPlan",
        "capability": "Create and optimize multiple plans",
        "tier": "basic",
        "tier_label": "Basic",
        "price_usd_monthly": 29,
        "price_usd_annual": 290,
        "limit": 1,
        "free_path": "archive_plan",
        "checkout_path": f"/v1/workspaces/{WORKSPACE_ID}/billing/checkout-sessions",
    }


def test_browser_cannot_grant_basic_by_updating_the_plan_directly() -> None:
    application = RecordingWorkspaceApplication()

    response = TestClient(create_app(slice_one=application)).put(
        f"/v1/workspaces/{WORKSPACE_ID}/plan",
        headers=HEADERS,
        json={"plan": "basic"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == {
        "code": "CHECKOUT_REQUIRED",
        "checkout_path": f"/v1/workspaces/{WORKSPACE_ID}/billing/checkout-sessions",
    }
    assert application.plan_changes == []


def test_archive_and_notification_reads_are_scoped_to_actor_and_workspace() -> None:
    application = RecordingWorkspaceApplication()
    client = TestClient(create_app(slice_one=application))

    archived = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/archive",
        headers=HEADERS,
    )
    marked = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/notifications/read",
        headers=HEADERS,
        json={"keys": ["analysis:run-1"]},
    )

    assert archived.status_code == 204
    assert marked.status_code == 204
    assert application.archived == [(USER_ID, WORKSPACE_ID, PROJECT_ID)]
    assert application.read_keys == ["analysis:run-1"]


def test_restore_is_not_limited_by_the_workspace_plan() -> None:
    application = RecordingWorkspaceApplication()

    response = TestClient(create_app(slice_one=application)).post(
        f"/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/restore",
        headers=HEADERS,
    )

    assert response.status_code == 204
    assert application.restored == [(USER_ID, WORKSPACE_ID, PROJECT_ID)]


def test_preferences_round_trip_without_starting_analysis() -> None:
    application = RecordingWorkspaceApplication()
    client = TestClient(create_app(slice_one=application))

    initial = client.get(
        f"/v1/workspaces/{WORKSPACE_ID}/preferences", headers=HEADERS
    )
    updated = client.put(
        f"/v1/workspaces/{WORKSPACE_ID}/preferences",
        headers=HEADERS,
        json={
            "theme": "light",
            "analysis_notifications": False,
            "failure_notifications": True,
            "stale_notifications": False,
            "display_name": "Workspace member",
            "role_title": "Programme lead",
            "workspace_name": "OSLO Alpha",
            "mentions_notifications": False,
            "reply_notifications": True,
            "shared_notifications": True,
        },
    )

    assert initial.status_code == 200
    assert initial.json()["theme"] == "dark"
    assert updated.status_code == 200
    assert updated.json() == {
        "theme": "light",
        "analysis_notifications": False,
        "failure_notifications": True,
        "stale_notifications": False,
        "display_name": "Workspace member",
        "role_title": "Programme lead",
        "workspace_name": "OSLO Alpha",
        "actor_role": "owner",
        "mentions_notifications": False,
        "reply_notifications": True,
        "shared_notifications": True,
    }

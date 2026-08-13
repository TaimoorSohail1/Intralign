from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.entitlements.service import OutcomeCapacityReached
from oslo_api.main import create_app
from oslo_api.slice_four import OutcomeProvenance, OutcomeStatus, ProjectOutcome
from oslo_api.slice_one import AuthenticatedUser

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
OUTCOME_ID = UUID("018f9f7e-8de2-7000-8000-000000000030")
HEADERS = {"Authorization": "Bearer valid-access-token"}


class AuthenticatedSliceOne:
    def authenticate(self, access_token: str) -> AuthenticatedUser:
        assert access_token == "valid-access-token"
        return AuthenticatedUser(id=USER_ID, email="member@example.com")


class AtCapacitySliceFour:
    def create_outcome(self, **_kwargs):
        raise OutcomeCapacityReached(active_outcome_limit=1)


class RecordingOutcomesSliceFour:
    def __init__(self) -> None:
        self.status = OutcomeStatus.ACTIVE

    def _outcome(self) -> ProjectOutcome:
        return ProjectOutcome(
            id=OUTCOME_ID,
            workspace_id=WORKSPACE_ID,
            project_id=PROJECT_ID,
            title="Improve successful delivery",
            status=self.status,
            is_primary=True,
            provenance=OutcomeProvenance.DECLARED,
            created_at=datetime(2026, 8, 13, tzinfo=UTC),
            archived_at=(
                datetime(2026, 8, 13, 1, tzinfo=UTC)
                if self.status is OutcomeStatus.ARCHIVED
                else None
            ),
        )

    def list_outcomes(self, **_kwargs) -> list[ProjectOutcome]:
        return [self._outcome()]

    def archive_outcome(self, **_kwargs) -> ProjectOutcome:
        self.status = OutcomeStatus.ARCHIVED
        return self._outcome()

    def reactivate_outcome(self, **_kwargs) -> ProjectOutcome:
        self.status = OutcomeStatus.ACTIVE
        return self._outcome()


def test_second_active_outcome_returns_named_basic_gate_with_free_path() -> None:
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=AtCapacitySliceFour())
    )

    response = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/outcomes",
        headers=HEADERS,
        json={"title": "Reduce avoidable rework", "provenance": "declared"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == {
        "code": "CAPACITY_COMMITMENT_REQUIRED",
        "wall_key": "multiOutcome",
        "capability": "Optimize all your outcomes",
        "tier": "basic",
        "tier_label": "Basic",
        "price_usd_monthly": 29,
        "price_usd_annual": 290,
        "limit": 1,
        "free_path": "archive_outcome",
        "checkout_path": f"/v1/workspaces/{WORKSPACE_ID}/billing/checkout-sessions",
    }


def test_archive_keeps_the_outcome_visible_and_reactivation_restores_it() -> None:
    slice_four = RecordingOutcomesSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    archived = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/outcomes/{OUTCOME_ID}:archive",
        headers=HEADERS,
    )
    visible = client.get(
        f"/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/outcomes",
        headers=HEADERS,
    )
    restored = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/outcomes/{OUTCOME_ID}:reactivate",
        headers=HEADERS,
    )

    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"
    assert visible.json()[0]["status"] == "archived"
    assert restored.status_code == 200
    assert restored.json()["status"] == "active"

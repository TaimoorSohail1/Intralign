from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from oslo_api.application import (
    CollaboratorSeatLimitReached,
    InvalidInvitation,
    InvitationDeliveryFailed,
    InvitationEmailMismatch,
    InvitationLimitReached,
)
from oslo_api.identity import InvalidSession
from oslo_api.invitations import (
    Invitation,
    InvitationStatus,
    InvitePermissionDenied,
    MembershipRole,
)
from oslo_api.main import create_app
from oslo_api.slice_one import ActivationResult, InvitationDetails

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
INVITATION_ID = UUID("018f9f7e-8de2-7000-8000-000000000001")


class RecordingSliceOneApplication:
    def __init__(self) -> None:
        self.invite_request = None

    def authenticate(self, access_token: str):
        assert access_token == "valid-access-token"
        return type("User", (), {"id": USER_ID, "email": "owner@example.com"})()

    def invite_member(self, *, actor_user_id, workspace_id, email, role):
        self.invite_request = (actor_user_id, workspace_id, email, role)
        now = datetime(2026, 7, 20, 9, 0, tzinfo=UTC)
        return Invitation(
            id=INVITATION_ID,
            workspace_id=workspace_id,
            invited_by_user_id=actor_user_id,
            email=email,
            role=role,
            token_hash=b"private",
            status=InvitationStatus.PENDING,
            created_at=now,
            expires_at=now + timedelta(days=7),
        )

    def activate_invitation(self, *, token, display_name, password):
        assert (token, display_name, password) == (
            "activation-token",
            "New Member",
            "ActivationTest123!",
        )
        return ActivationResult(
            user_id=USER_ID,
            email="new.member@example.com",
            workspace_id=WORKSPACE_ID,
            access_token="new-access-token",
            refresh_token="new-refresh-token",
            expires_in=3600,
            welcome_required=True,
        )

    def resolve_invitation(self, token):
        assert token == "activation-token"
        return InvitationDetails(
            email="new.member@example.com",
            workspace_name="OSLO Product Grill",
            role=MembershipRole.COLLABORATOR,
            expires_at=datetime(2026, 7, 27, 9, 0, tzinfo=UTC),
            account_exists=False,
        )

    def accept_invitation_for_existing_user(self, *, token, email, password):
        assert (token, email, password) == (
            "activation-token",
            "existing.member@example.com",
            "ExistingMember123!",
        )
        return ActivationResult(
            user_id=USER_ID,
            email=email,
            workspace_id=WORKSPACE_ID,
            access_token="existing-access-token",
            refresh_token="existing-refresh-token",
            expires_in=3600,
            welcome_required=True,
        )

    def list_invitations(self, *, actor_user_id, workspace_id):
        assert (actor_user_id, workspace_id) == (USER_ID, WORKSPACE_ID)
        now = datetime(2026, 7, 20, 9, 0, tzinfo=UTC)
        return [
            Invitation(
                id=INVITATION_ID,
                workspace_id=workspace_id,
                invited_by_user_id=actor_user_id,
                email="pending.member@example.com",
                role=MembershipRole.COLLABORATOR,
                token_hash=b"private",
                status=InvitationStatus.PENDING,
                created_at=now,
                expires_at=now + timedelta(days=7),
            )
        ]


class NonOwnerSliceOneApplication(RecordingSliceOneApplication):
    def invite_member(self, **_kwargs):
        raise InvitePermissionDenied

    def resend_invitation(self, **_kwargs):
        raise InvitePermissionDenied

    def revoke_invitation(self, **_kwargs):
        raise InvitePermissionDenied


class UnavailableInvitationApplication(RecordingSliceOneApplication):
    def resolve_invitation(self, _token):
        raise InvalidInvitation

    def activate_invitation(self, **_kwargs):
        raise InvalidInvitation

    def accept_invitation_for_existing_user(self, **_kwargs):
        raise InvalidInvitation


class MismatchedInvitationApplication(RecordingSliceOneApplication):
    def accept_invitation_for_existing_user(self, **_kwargs):
        raise InvitationEmailMismatch


class ExpiredSessionApplication(RecordingSliceOneApplication):
    def authenticate(self, _access_token):
        raise InvalidSession


class DeliveryFailureApplication(RecordingSliceOneApplication):
    def invite_member(self, **_kwargs):
        raise InvitationDeliveryFailed(INVITATION_ID)


class MonthlyLimitApplication(RecordingSliceOneApplication):
    def invite_member(self, **_kwargs):
        raise InvitationLimitReached


class SeatLimitApplication(RecordingSliceOneApplication):
    def invite_member(self, **_kwargs):
        raise CollaboratorSeatLimitReached


def test_inviting_requires_an_authenticated_session() -> None:
    response = TestClient(create_app()).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_expired_session_cannot_manage_invitations() -> None:
    response = TestClient(create_app(slice_one=ExpiredSessionApplication())).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer expired-access-token"},
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 401


def test_owner_can_create_an_invitation_through_the_api() -> None:
    application = RecordingSliceOneApplication()
    response = TestClient(create_app(slice_one=application)).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": str(INVITATION_ID),
        "email": "new.member@example.com",
        "role": "collaborator",
        "status": "pending",
        "expires_at": "2026-07-27T09:00:00Z",
    }
    assert application.invite_request == (
        USER_ID,
        WORKSPACE_ID,
        "new.member@example.com",
        MembershipRole.COLLABORATOR,
    )


def test_non_owner_cannot_create_an_invitation_through_the_api() -> None:
    response = TestClient(create_app(slice_one=NonOwnerSliceOneApplication())).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Only workspace Owners can manage invitations"}


@pytest.mark.parametrize("operation", ["resend", "revoke"])
def test_non_owner_cannot_resend_or_revoke_an_invitation(operation: str) -> None:
    client = TestClient(create_app(slice_one=NonOwnerSliceOneApplication()))
    invitation_url = f"/v1/workspaces/{WORKSPACE_ID}/invitations/{INVITATION_ID}"

    response = (
        client.post(
            f"{invitation_url}/resend", headers={"Authorization": "Bearer valid-access-token"}
        )
        if operation == "resend"
        else client.delete(invitation_url, headers={"Authorization": "Bearer valid-access-token"})
    )

    assert response.status_code == 403


def test_email_delivery_failure_is_reported_as_retryable() -> None:
    response = TestClient(create_app(slice_one=DeliveryFailureApplication())).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == {
        "code": "INVITATION_DELIVERY_FAILED",
        "message": "Invitation was saved but email delivery failed. Retry from Invitations.",
        "invitation_id": str(INVITATION_ID),
    }


@pytest.mark.parametrize(
    ("application", "code"),
    [
        (MonthlyLimitApplication(), "INVITATION_LIMIT_REACHED"),
        (SeatLimitApplication(), "COLLABORATOR_SEAT_LIMIT_REACHED"),
    ],
)
def test_free_plan_invitation_limits_are_reported_as_conflicts(
    application: RecordingSliceOneApplication,
    code: str,
) -> None:
    response = TestClient(create_app(slice_one=application)).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": "new.member@example.com", "role": "collaborator"},
    )

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == code


@pytest.mark.parametrize("email", ["not-an-email", "missing-at.example.com", "@example.com"])
def test_invalid_email_is_rejected(email: str) -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": email, "role": "collaborator"},
    )

    assert response.status_code == 422


def test_unknown_role_cannot_be_injected_through_the_api() -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).post(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
        json={"email": "new.member@example.com", "role": "super-admin"},
    )

    assert response.status_code == 422


def test_new_user_can_activate_an_invitation() -> None:
    application = RecordingSliceOneApplication()
    response = TestClient(create_app(slice_one=application)).post(
        "/v1/invitations/activate",
        json={
            "token": "activation-token",
            "display_name": "New Member",
            "password": "ActivationTest123!",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(USER_ID),
        "email": "new.member@example.com",
        "workspace_id": str(WORKSPACE_ID),
        "access_token": "new-access-token",
        "refresh_token": "new-refresh-token",
        "expires_in": 3600,
        "welcome_required": True,
    }


def test_activation_rejects_a_weak_password_before_identity_changes() -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).post(
        "/v1/invitations/activate",
        json={
            "token": "activation-token",
            "display_name": "New Member",
            "password": "too-short",
        },
    )

    assert response.status_code == 422


def test_activation_link_resolves_invitation_context() -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).post(
        "/v1/invitations/resolve",
        json={"token": "activation-token"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "email": "new.member@example.com",
        "workspace_name": "OSLO Product Grill",
        "role": "collaborator",
        "expires_at": "2026-07-27T09:00:00Z",
        "account_exists": False,
    }


@pytest.mark.parametrize(
    "token",
    ["modified-token", "expired-token", "revoked-token", "accepted-token", "old-resend-token"],
)
def test_unavailable_invitation_links_fail_closed(token: str) -> None:
    response = TestClient(create_app(slice_one=UnavailableInvitationApplication())).post(
        "/v1/invitations/resolve",
        json={"token": token},
    )

    assert response.status_code == 410
    assert response.json()["detail"]["code"] == "INVITATION_UNAVAILABLE"


def test_existing_user_signs_in_and_accepts_the_invitation() -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).post(
        "/v1/invitations/accept-existing",
        json={
            "token": "activation-token",
            "email": "existing.member@example.com",
            "password": "ExistingMember123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["workspace_id"] == str(WORKSPACE_ID)
    assert response.json()["welcome_required"] is True


def test_existing_user_must_use_the_invited_email() -> None:
    response = TestClient(create_app(slice_one=MismatchedInvitationApplication())).post(
        "/v1/invitations/accept-existing",
        json={
            "token": "activation-token",
            "email": "different.member@example.com",
            "password": "ExistingMember123!",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "EMAIL_MISMATCH"


def test_owner_can_list_workspace_invitations() -> None:
    response = TestClient(create_app(slice_one=RecordingSliceOneApplication())).get(
        f"/v1/workspaces/{WORKSPACE_ID}/invitations",
        headers={"Authorization": "Bearer valid-access-token"},
    )

    assert response.status_code == 200
    assert response.json()[0]["email"] == "pending.member@example.com"
    assert "token_hash" not in response.json()[0]

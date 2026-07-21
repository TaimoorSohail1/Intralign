from datetime import UTC, datetime, timedelta
from hashlib import sha256
from uuid import UUID

import pytest

from oslo_api.invitations import (
    InvitationStatus,
    InviteMember,
    InviteMemberCommand,
    InvitePermissionDenied,
    MembershipRole,
)


class RecordingInvitationStore:
    def __init__(self) -> None:
        self.saved = []

    def save(self, invitation) -> None:
        self.saved.append(invitation)


class FixedMemberships:
    def __init__(self, role: MembershipRole | None) -> None:
        self.role = role

    def role_for(self, workspace_id: UUID, user_id: UUID) -> MembershipRole | None:
        return self.role


def test_owner_can_invite_a_collaborator_for_seven_days() -> None:
    now = datetime(2026, 7, 20, 9, 0, tzinfo=UTC)
    store = RecordingInvitationStore()
    invite_member = InviteMember(
        invitations=store,
        memberships=FixedMemberships(MembershipRole.OWNER),
        clock=lambda: now,
        new_id=lambda: UUID("018f9f7e-8de2-7000-8000-000000000001"),
        new_token=lambda: "raw-activation-token",
    )

    issued = invite_member(
        InviteMemberCommand(
            workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000010"),
            invited_by_user_id=UUID("018f9f7e-8de2-7000-8000-000000000011"),
            email="new.member@example.com",
            role=MembershipRole.COLLABORATOR,
        )
    )
    invitation = issued.invitation

    assert invitation.status is InvitationStatus.PENDING
    assert invitation.expires_at == now + timedelta(days=7)
    assert store.saved == [invitation]
    assert issued.token == "raw-activation-token"
    assert invitation.token_hash == sha256(b"raw-activation-token").digest()
    assert "raw-activation-token" not in repr(invitation)


@pytest.mark.parametrize(
    "actor_role",
    [MembershipRole.COLLABORATOR, MembershipRole.VIEWER],
)
def test_non_owners_cannot_invite_members(actor_role: MembershipRole) -> None:
    store = RecordingInvitationStore()
    invite_member = InviteMember(
        invitations=store,
        memberships=FixedMemberships(actor_role),
        clock=lambda: datetime(2026, 7, 20, 9, 0, tzinfo=UTC),
        new_id=lambda: UUID("018f9f7e-8de2-7000-8000-000000000001"),
        new_token=lambda: "raw-activation-token",
    )

    with pytest.raises(InvitePermissionDenied):
        invite_member(
            InviteMemberCommand(
                workspace_id=UUID("018f9f7e-8de2-7000-8000-000000000010"),
                invited_by_user_id=UUID("018f9f7e-8de2-7000-8000-000000000011"),
                email="new.member@example.com",
            )
        )

    assert store.saved == []

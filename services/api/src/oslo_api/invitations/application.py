from collections.abc import Callable
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Protocol
from uuid import UUID

from oslo_api.invitations.models import (
    Invitation,
    InvitationStatus,
    InviteMemberCommand,
    IssuedInvitation,
    MembershipRole,
)


class InvitePermissionDenied(Exception):
    """Raised when a non-owner attempts to manage invitations."""


class InvitationStore(Protocol):
    def save(self, invitation: Invitation) -> None: ...


class MembershipReader(Protocol):
    def role_for(self, workspace_id: UUID, user_id: UUID) -> MembershipRole | None: ...


class InviteMember:
    def __init__(
        self,
        *,
        invitations: InvitationStore,
        memberships: MembershipReader,
        clock: Callable[[], datetime],
        new_id: Callable[[], UUID],
        new_token: Callable[[], str],
        validity: timedelta = timedelta(days=14),
    ) -> None:
        self._invitations = invitations
        self._memberships = memberships
        self._clock = clock
        self._new_id = new_id
        self._new_token = new_token
        self._validity = validity

    def __call__(self, command: InviteMemberCommand) -> IssuedInvitation:
        actor_role = self._memberships.role_for(
            command.workspace_id,
            command.invited_by_user_id,
        )
        if actor_role is not MembershipRole.OWNER:
            raise InvitePermissionDenied

        now = self._clock()
        token = self._new_token()
        invitation = Invitation(
            id=self._new_id(),
            workspace_id=command.workspace_id,
            invited_by_user_id=command.invited_by_user_id,
            email=command.email.strip().lower(),
            role=MembershipRole.OWNER,
            token_hash=sha256(token.encode("utf-8")).digest(),
            status=InvitationStatus.PENDING,
            created_at=now,
            expires_at=now + self._validity,
        )
        self._invitations.save(invitation)
        return IssuedInvitation(invitation=invitation, token=token)

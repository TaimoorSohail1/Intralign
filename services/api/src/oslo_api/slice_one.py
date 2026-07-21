from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from oslo_api.invitations import Invitation, MembershipRole


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    id: UUID
    email: str


@dataclass(frozen=True, slots=True)
class AuthSession:
    user_id: UUID
    email: str
    access_token: str
    refresh_token: str
    expires_in: int


@dataclass(frozen=True, slots=True)
class ActivationResult:
    user_id: UUID
    email: str
    workspace_id: UUID
    access_token: str
    refresh_token: str
    expires_in: int
    welcome_required: bool


@dataclass(frozen=True, slots=True)
class InvitationDetails:
    email: str
    workspace_name: str
    role: MembershipRole
    expires_at: datetime
    account_exists: bool


@dataclass(frozen=True, slots=True)
class Project:
    id: UUID
    workspace_id: UUID
    name: str
    status: str


class SliceOneApplication(Protocol):
    def authenticate(self, access_token: str) -> AuthenticatedUser: ...

    def invite_member(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        email: str,
        role: MembershipRole,
    ) -> Invitation: ...

    def activate_invitation(
        self,
        *,
        token: str,
        display_name: str,
        password: str,
    ) -> ActivationResult: ...

    def resolve_invitation(self, token: str) -> InvitationDetails: ...

    def accept_invitation_for_existing_user(
        self,
        *,
        token: str,
        email: str,
        password: str,
    ) -> ActivationResult: ...

    def list_invitations(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
    ) -> list[Invitation]: ...

    def resend_invitation(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        invitation_id: UUID,
    ) -> Invitation: ...

    def revoke_invitation(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        invitation_id: UUID,
    ) -> None: ...

    def start_first_project(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
    ) -> Project: ...

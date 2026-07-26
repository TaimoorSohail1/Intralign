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


@dataclass(frozen=True, slots=True)
class WorkspaceProject:
    id: UUID
    name: str
    status: str
    archived: bool
    updated_at: datetime
    analysis_status: str
    confidence_index: int | None
    confidence_band: str | None
    reliability: str | None
    open_issues: int
    artifact_count: int


@dataclass(frozen=True, slots=True)
class WorkspaceNotification:
    key: str
    project_id: UUID
    project_name: str
    kind: str
    status: str
    title: str
    created_at: datetime
    read: bool


@dataclass(frozen=True, slots=True)
class WorkspaceSummary:
    id: UUID
    name: str
    role: str
    plan: str
    active_project_limit: int
    projects: list[WorkspaceProject]
    notifications: list[WorkspaceNotification]


@dataclass(frozen=True, slots=True)
class WorkspacePreferences:
    theme: str
    analysis_notifications: bool
    failure_notifications: bool
    stale_notifications: bool


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

    def get_workspace_summary(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspaceSummary: ...

    def archive_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None: ...

    def restore_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None: ...

    def mark_workspace_notifications_read(
        self, *, actor_user_id: UUID, workspace_id: UUID, keys: list[str]
    ) -> None: ...

    def get_workspace_preferences(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspacePreferences: ...

    def update_workspace_preferences(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        theme: str,
        analysis_notifications: bool,
        failure_notifications: bool,
        stale_notifications: bool,
    ) -> WorkspacePreferences: ...

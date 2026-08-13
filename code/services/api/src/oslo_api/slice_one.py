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
class SessionContext:
    user_id: UUID
    email: str
    workspace_id: UUID
    display_name: str
    account_role: str
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
    weakest_pillar: str | None = None


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
    projects: list[WorkspaceProject]
    notifications: list[WorkspaceNotification]
    plan_label: str = "Free"
    price_usd_monthly: int = 0
    document_limit: int = 20
    word_limit: int = 50_000
    collaborator_seat_limit: int | None = None
    monthly_analysis_limit: int | None = None
    monthly_analyses_used: int = 0
    can_manage_plan: bool = False
    member_count: int = 1
    collaborator_seats_used: int = 1
    active_project_limit: int = 1
    can_create_project: bool = True


@dataclass(frozen=True, slots=True)
class WorkspacePreferences:
    theme: str
    analysis_notifications: bool
    failure_notifications: bool
    stale_notifications: bool
    display_name: str = ""
    role_title: str = ""
    workspace_name: str = ""
    actor_role: str = "owner"
    mentions_notifications: bool = True
    reply_notifications: bool = True
    shared_notifications: bool = True


class SliceOneApplication(Protocol):
    def authenticate(self, access_token: str) -> AuthenticatedUser: ...

    def get_session_context(self, *, actor_user_id: UUID) -> SessionContext: ...

    def complete_welcome(self, *, actor_user_id: UUID, workspace_id: UUID) -> None: ...

    def invite_member(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        email: str,
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
        display_name: str,
        role_title: str,
        workspace_name: str,
        mentions_notifications: bool,
        reply_notifications: bool,
        shared_notifications: bool,
    ) -> WorkspacePreferences: ...

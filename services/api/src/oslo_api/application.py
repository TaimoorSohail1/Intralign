import json
from datetime import UTC, datetime
from hashlib import sha256
from secrets import token_urlsafe
from typing import Protocol
from urllib.parse import urlencode
from uuid import UUID, uuid4

from sqlalchemy import Connection, Engine, RowMapping, text

from oslo_api.invitations import (
    Invitation,
    InvitationStatus,
    InviteMember,
    InviteMemberCommand,
    InvitePermissionDenied,
    MembershipRole,
)
from oslo_api.slice_one import (
    ActivationResult,
    AuthenticatedUser,
    AuthSession,
    InvitationDetails,
    Project,
    WorkspaceNotification,
    WorkspacePreferences,
    WorkspaceProject,
    WorkspaceSummary,
)


class InvitationMailer(Protocol):
    def send_invitation(
        self,
        *,
        email: str,
        workspace_name: str,
        role: str,
        activation_url: str,
        expires_at: datetime,
    ) -> None: ...


class IdentityProvider(Protocol):
    def authenticate(self, access_token: str) -> AuthenticatedUser: ...

    def find_user_by_email(self, email: str) -> AuthenticatedUser | None: ...

    def create_user(self, *, email: str, password: str, display_name: str) -> AuthenticatedUser: ...

    def delete_user(self, user_id: UUID) -> None: ...

    def sign_in_with_password(self, *, email: str, password: str) -> AuthSession: ...


class InvalidInvitation(Exception):
    """Raised when an invitation token cannot be used."""


class AccountAlreadyExists(Exception):
    """Raised when activation must continue through existing-user login."""


class InvitationEmailMismatch(Exception):
    """Raised when the authenticated account differs from the invited email."""


class InvitationDeliveryFailed(Exception):
    """Raised when a persisted invitation could not be delivered."""

    def __init__(self, invitation_id: UUID) -> None:
        self.invitation_id = invitation_id
        super().__init__("Invitation delivery failed")


class ProjectLimitReached(Exception):
    """Raised when the workspace plan cannot create another active project."""


class ProjectArchiveDenied(Exception):
    """Raised when a member cannot archive or restore the requested project."""


class SqlMembershipReader:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def role_for(self, workspace_id: UUID, user_id: UUID) -> MembershipRole | None:
        role = self._connection.execute(
            text(
                "select role from public.memberships "
                "where workspace_id = :workspace_id and user_id = :user_id"
            ),
            {"workspace_id": workspace_id, "user_id": user_id},
        ).scalar_one_or_none()
        return MembershipRole(role) if role else None


class SqlInvitationStore:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def save(self, invitation: Invitation) -> None:
        self._connection.execute(
            text(
                """
                insert into public.invitations (
                  id, workspace_id, email, role, token_hash, status,
                  invited_by, created_at, expires_at
                ) values (
                  :id, :workspace_id, :email, :role, :token_hash, :status,
                  :invited_by, :created_at, :expires_at
                )
                """
            ),
            {
                "id": invitation.id,
                "workspace_id": invitation.workspace_id,
                "email": invitation.email,
                "role": invitation.role.value,
                "token_hash": invitation.token_hash,
                "status": invitation.status.value,
                "invited_by": invitation.invited_by_user_id,
                "created_at": invitation.created_at,
                "expires_at": invitation.expires_at,
            },
        )


class DatabaseSliceOneApplication:
    def __init__(
        self,
        *,
        engine: Engine,
        mailer: InvitationMailer,
        web_url: str,
        identity: IdentityProvider | None = None,
    ) -> None:
        self._engine = engine
        self._mailer = mailer
        self._web_url = web_url.rstrip("/")
        self._identity = identity

    def authenticate(self, access_token: str) -> AuthenticatedUser:
        if self._identity is None:
            raise RuntimeError("Identity provider is not configured")
        return self._identity.authenticate(access_token)

    def invite_member(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        email: str,
        role: MembershipRole,
    ) -> Invitation:
        normalised_email = email.strip().lower()
        with self._engine.begin() as connection:
            memberships = SqlMembershipReader(connection)
            if memberships.role_for(workspace_id, actor_user_id) is not MembershipRole.OWNER:
                raise InvitePermissionDenied
            connection.execute(
                text("select pg_advisory_xact_lock(hashtextextended(:scope, 0))"),
                {"scope": f"{workspace_id}:{normalised_email}"},
            )
            existing = (
                connection.execute(
                    text(
                        """
                    select id, workspace_id, invited_by, email::text, role,
                           status, created_at, expires_at
                    from public.invitations
                    where workspace_id = :workspace_id and email = :email
                      and status = 'pending'
                    """
                    ),
                    {"workspace_id": workspace_id, "email": normalised_email},
                )
                .mappings()
                .one_or_none()
            )
            if existing is not None:
                return Invitation(
                    id=existing["id"],
                    workspace_id=existing["workspace_id"],
                    invited_by_user_id=existing["invited_by"],
                    email=existing["email"],
                    role=MembershipRole(existing["role"]),
                    token_hash=b"",
                    status=InvitationStatus(existing["status"]),
                    created_at=existing["created_at"],
                    expires_at=existing["expires_at"],
                )
            issued = InviteMember(
                invitations=SqlInvitationStore(connection),
                memberships=memberships,
                clock=lambda: datetime.now(UTC),
                new_id=uuid4,
                new_token=lambda: token_urlsafe(32),
            )(
                InviteMemberCommand(
                    workspace_id=workspace_id,
                    invited_by_user_id=actor_user_id,
                    email=normalised_email,
                    role=role,
                )
            )
            workspace_name = connection.execute(
                text("select name from public.workspaces where id = :workspace_id"),
                {"workspace_id": workspace_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id, metadata
                    ) values (
                      :workspace_id, :actor_user_id, 'invitation.created',
                      'invitation', :subject_id, cast(:metadata as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "subject_id": str(issued.invitation.id),
                    "metadata": json.dumps({"email": issued.invitation.email, "role": role.value}),
                },
            )

        query = urlencode({"token": issued.token})
        try:
            self._mailer.send_invitation(
                email=issued.invitation.email,
                workspace_name=workspace_name,
                role=issued.invitation.role.value.title(),
                activation_url=f"{self._web_url}/activate?{query}",
                expires_at=issued.invitation.expires_at,
            )
        except Exception as error:
            raise InvitationDeliveryFailed(issued.invitation.id) from error
        return issued.invitation

    def list_invitations(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
    ) -> list[Invitation]:
        with self._engine.connect() as connection:
            if (
                SqlMembershipReader(connection).role_for(workspace_id, actor_user_id)
                is not MembershipRole.OWNER
            ):
                raise InvitePermissionDenied
            rows = (
                connection.execute(
                    text(
                        """
                    select id, workspace_id, invited_by, email::text, role,
                           status, created_at, expires_at
                    from public.invitations
                    where workspace_id = :workspace_id
                    order by created_at desc
                    """
                    ),
                    {"workspace_id": workspace_id},
                )
                .mappings()
                .all()
            )
        now = datetime.now(UTC)
        return [
            Invitation(
                id=row["id"],
                workspace_id=row["workspace_id"],
                invited_by_user_id=row["invited_by"],
                email=row["email"],
                role=MembershipRole(row["role"]),
                token_hash=b"",
                status=(
                    InvitationStatus.EXPIRED
                    if row["status"] == "pending" and row["expires_at"] <= now
                    else InvitationStatus(row["status"])
                ),
                created_at=row["created_at"],
                expires_at=row["expires_at"],
            )
            for row in rows
        ]

    def resend_invitation(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        invitation_id: UUID,
    ) -> Invitation:
        with self._engine.begin() as connection:
            memberships = SqlMembershipReader(connection)
            if memberships.role_for(workspace_id, actor_user_id) is not MembershipRole.OWNER:
                raise InvitePermissionDenied
            previous = (
                connection.execute(
                    text(
                        """
                    select email::text, role from public.invitations
                    where id = :invitation_id and workspace_id = :workspace_id
                      and status = 'pending'
                    for update
                    """
                    ),
                    {"invitation_id": invitation_id, "workspace_id": workspace_id},
                )
                .mappings()
                .one_or_none()
            )
            if previous is None:
                raise InvalidInvitation
            connection.execute(
                text(
                    """
                    update public.invitations set status = 'revoked', revoked_at = now()
                    where id = :invitation_id
                    """
                ),
                {"invitation_id": invitation_id},
            )
            issued = InviteMember(
                invitations=SqlInvitationStore(connection),
                memberships=memberships,
                clock=lambda: datetime.now(UTC),
                new_id=uuid4,
                new_token=lambda: token_urlsafe(32),
            )(
                InviteMemberCommand(
                    workspace_id=workspace_id,
                    invited_by_user_id=actor_user_id,
                    email=previous["email"],
                    role=MembershipRole(previous["role"]),
                )
            )
            workspace_name = connection.execute(
                text("select name from public.workspaces where id = :workspace_id"),
                {"workspace_id": workspace_id},
            ).scalar_one()
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id, metadata
                    ) values (
                      :workspace_id, :actor_user_id, 'invitation.resent',
                      'invitation', :subject_id, cast(:metadata as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "subject_id": str(issued.invitation.id),
                    "metadata": json.dumps({"replaced_invitation_id": str(invitation_id)}),
                },
            )
        try:
            self._mailer.send_invitation(
                email=issued.invitation.email,
                workspace_name=workspace_name,
                role=issued.invitation.role.value.title(),
                activation_url=f"{self._web_url}/activate?{urlencode({'token': issued.token})}",
                expires_at=issued.invitation.expires_at,
            )
        except Exception as error:
            raise InvitationDeliveryFailed(issued.invitation.id) from error
        return issued.invitation

    def revoke_invitation(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        invitation_id: UUID,
    ) -> None:
        with self._engine.begin() as connection:
            if (
                SqlMembershipReader(connection).role_for(workspace_id, actor_user_id)
                is not MembershipRole.OWNER
            ):
                raise InvitePermissionDenied
            revoked = connection.execute(
                text(
                    """
                    update public.invitations set status = 'revoked', revoked_at = now()
                    where id = :invitation_id and workspace_id = :workspace_id
                      and status = 'pending'
                    """
                ),
                {"invitation_id": invitation_id, "workspace_id": workspace_id},
            )
            if revoked.rowcount != 1:
                raise InvalidInvitation
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id
                    ) values (
                      :workspace_id, :actor_user_id, 'invitation.revoked',
                      'invitation', :subject_id
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "subject_id": str(invitation_id),
                },
            )

    def start_first_project(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
    ) -> Project:
        project_id = uuid4()
        with self._engine.begin() as connection:
            if SqlMembershipReader(connection).role_for(workspace_id, actor_user_id) is None:
                raise InvitePermissionDenied
            connection.execute(
                text("select pg_advisory_xact_lock(hashtextextended(:scope, 0))"),
                {"scope": f"project-limit:{workspace_id}"},
            )
            active_count = connection.execute(
                text(
                    "select count(*) from public.projects "
                    "where workspace_id = :workspace_id and archived_at is null"
                ),
                {"workspace_id": workspace_id},
            ).scalar_one()
            if active_count >= 1:
                raise ProjectLimitReached
            connection.execute(
                text(
                    """
                    insert into public.projects (id, workspace_id, name, status, created_by)
                    values (:id, :workspace_id, 'Untitled project', 'draft', :created_by)
                    """
                ),
                {"id": project_id, "workspace_id": workspace_id, "created_by": actor_user_id},
            )
            connection.execute(
                text(
                    """
                    update public.memberships
                    set welcome_seen_at = coalesce(welcome_seen_at, now())
                    where workspace_id = :workspace_id and user_id = :user_id
                    """
                ),
                {"workspace_id": workspace_id, "user_id": actor_user_id},
            )
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id
                    ) values (
                      :workspace_id, :actor_user_id, 'project.created', 'project', :subject_id
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "subject_id": str(project_id),
                },
            )
        return Project(
            id=project_id,
            workspace_id=workspace_id,
            name="Untitled project",
            status="draft",
        )

    def get_workspace_summary(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspaceSummary:
        with self._engine.connect() as connection:
            role = SqlMembershipReader(connection).role_for(workspace_id, actor_user_id)
            if role is None:
                raise InvitePermissionDenied
            workspace_name = connection.execute(
                text("select name from public.workspaces where id = :workspace_id"),
                {"workspace_id": workspace_id},
            ).scalar_one()
            rows = (
                connection.execute(
                    text(
                        """
                        select p.id, p.name, p.status, p.archived_at, p.updated_at,
                               latest.snapshot_state,
                               (latest.snapshot_json -> 'assessment' ->> 'confidence_index')::int
                                 as confidence_index,
                               latest.snapshot_json -> 'assessment' ->> 'confidence_band'
                                 as confidence_band,
                               latest.snapshot_json -> 'assessment' ->> 'reliability'
                                 as reliability,
                               coalesce(issue_counts.open_issues, 0) as open_issues,
                               coalesce(jsonb_array_length(latest.snapshot_json -> 'artifacts'), 0)
                                 as artifact_count
                        from public.projects p
                        left join lateral (
                          select s.snapshot_state, s.snapshot_json
                          from public.assessment_snapshots s
                          where s.project_id = p.id
                          order by s.published_at desc
                          limit 1
                        ) latest on true
                        left join lateral (
                          select count(*)::int as open_issues
                          from public.issues i
                          where i.project_id = p.id and i.current_status <> 'resolved'
                        ) issue_counts on true
                        where p.workspace_id = :workspace_id
                        order by p.archived_at nulls first, p.updated_at desc
                        """
                    ),
                    {"workspace_id": workspace_id},
                )
                .mappings()
                .all()
            )
            notification_rows = (
                connection.execute(
                    text(
                        """
                        select
                          'analysis:' || run.id::text || ':' || run.status::text as key,
                          run.project_id,
                          project.name as project_name,
                          run.kind::text as kind,
                          run.status::text as status,
                          case
                            when run.status = 'failed' then
                              case when run.kind = 'extended'
                                then 'Extended Analysis needs attention'
                                else 'Initial Analysis needs attention'
                              end
                            when run.kind = 'extended' then 'Extended Analysis completed'
                            else 'Initial Analysis completed'
                          end as title,
                          coalesce(run.completed_at, run.updated_at) as created_at,
                          reads.notification_key is not null as read
                        from public.analysis_runs run
                        join public.projects project on project.id = run.project_id
                        left join public.workspace_notification_reads reads
                          on reads.workspace_id = run.workspace_id
                         and reads.user_id = :actor_user_id
                         and reads.notification_key =
                           'analysis:' || run.id::text || ':' || run.status::text
                        where run.workspace_id = :workspace_id
                          and run.status in ('completed', 'failed')
                        order by coalesce(run.completed_at, run.updated_at) desc
                        limit 12
                        """
                    ),
                    {"workspace_id": workspace_id, "actor_user_id": actor_user_id},
                )
                .mappings()
                .all()
            )
        return WorkspaceSummary(
            id=workspace_id,
            name=workspace_name,
            role=role.value,
            plan="free",
            active_project_limit=1,
            projects=[
                WorkspaceProject(
                    id=row["id"],
                    name=row["name"],
                    status=row["status"],
                    archived=row["archived_at"] is not None,
                    updated_at=row["updated_at"],
                    analysis_status=row["snapshot_state"] or "not_analyzed",
                    confidence_index=row["confidence_index"],
                    confidence_band=row["confidence_band"],
                    reliability=row["reliability"],
                    open_issues=row["open_issues"],
                    artifact_count=row["artifact_count"],
                )
                for row in rows
            ],
            notifications=[
                WorkspaceNotification(
                    key=row["key"],
                    project_id=row["project_id"],
                    project_name=row["project_name"],
                    kind=row["kind"],
                    status=row["status"],
                    title=row["title"],
                    created_at=row["created_at"],
                    read=row["read"],
                )
                for row in notification_rows
            ],
        )

    def _set_project_archived(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
        archived: bool,
    ) -> None:
        with self._engine.begin() as connection:
            if (
                SqlMembershipReader(connection).role_for(workspace_id, actor_user_id)
                is not MembershipRole.OWNER
            ):
                raise ProjectArchiveDenied
            connection.execute(
                text("select pg_advisory_xact_lock(hashtextextended(:scope, 0))"),
                {"scope": f"project-limit:{workspace_id}"},
            )
            if not archived:
                active_count = connection.execute(
                    text(
                        "select count(*) from public.projects "
                        "where workspace_id = :workspace_id and archived_at is null"
                    ),
                    {"workspace_id": workspace_id},
                ).scalar_one()
                if active_count >= 1:
                    raise ProjectLimitReached
            updated = connection.execute(
                text(
                    """
                    update public.projects
                    set archived_at = case when :archived then now() else null end,
                        archived_by = case when :archived then :actor_user_id else null end,
                        updated_at = now()
                    where id = :project_id and workspace_id = :workspace_id
                      and ((:archived and archived_at is null)
                           or (not :archived and archived_at is not null))
                    """
                ),
                {
                    "archived": archived,
                    "actor_user_id": actor_user_id,
                    "project_id": project_id,
                    "workspace_id": workspace_id,
                },
            )
            if updated.rowcount != 1:
                raise ProjectArchiveDenied
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id
                    ) values (
                      :workspace_id, :actor_user_id, :action, 'project', :subject_id
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "action": "project.archived" if archived else "project.restored",
                    "subject_id": str(project_id),
                },
            )

    def archive_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None:
        self._set_project_archived(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            project_id=project_id,
            archived=True,
        )

    def restore_project(
        self, *, actor_user_id: UUID, workspace_id: UUID, project_id: UUID
    ) -> None:
        self._set_project_archived(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            project_id=project_id,
            archived=False,
        )

    def mark_workspace_notifications_read(
        self, *, actor_user_id: UUID, workspace_id: UUID, keys: list[str]
    ) -> None:
        if not keys:
            return
        with self._engine.begin() as connection:
            if SqlMembershipReader(connection).role_for(workspace_id, actor_user_id) is None:
                raise InvitePermissionDenied
            for notification_key in set(keys):
                if not notification_key.startswith("analysis:"):
                    continue
                connection.execute(
                    text(
                        """
                        insert into public.workspace_notification_reads (
                          workspace_id, user_id, notification_key
                        ) values (:workspace_id, :user_id, :notification_key)
                        on conflict (workspace_id, user_id, notification_key)
                          do update set read_at = now()
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "user_id": actor_user_id,
                        "notification_key": notification_key,
                    },
                )

    def get_workspace_preferences(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> WorkspacePreferences:
        with self._engine.begin() as connection:
            if SqlMembershipReader(connection).role_for(workspace_id, actor_user_id) is None:
                raise InvitePermissionDenied
            row = (
                connection.execute(
                    text(
                        """
                        insert into public.workspace_member_preferences (workspace_id, user_id)
                        values (:workspace_id, :user_id)
                        on conflict (workspace_id, user_id) do update
                          set updated_at = public.workspace_member_preferences.updated_at
                        returning theme, analysis_notifications, failure_notifications,
                                  stale_notifications
                        """
                    ),
                    {"workspace_id": workspace_id, "user_id": actor_user_id},
                )
                .mappings()
                .one()
            )
        return WorkspacePreferences(**row)

    def update_workspace_preferences(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        theme: str,
        analysis_notifications: bool,
        failure_notifications: bool,
        stale_notifications: bool,
    ) -> WorkspacePreferences:
        if theme not in {"dark", "light", "system"}:
            raise ValueError("Unsupported theme")
        with self._engine.begin() as connection:
            if SqlMembershipReader(connection).role_for(workspace_id, actor_user_id) is None:
                raise InvitePermissionDenied
            row = (
                connection.execute(
                    text(
                        """
                        insert into public.workspace_member_preferences (
                          workspace_id, user_id, theme, analysis_notifications,
                          failure_notifications, stale_notifications
                        ) values (
                          :workspace_id, :user_id, :theme, :analysis_notifications,
                          :failure_notifications, :stale_notifications
                        )
                        on conflict (workspace_id, user_id) do update set
                          theme = excluded.theme,
                          analysis_notifications = excluded.analysis_notifications,
                          failure_notifications = excluded.failure_notifications,
                          stale_notifications = excluded.stale_notifications,
                          updated_at = now()
                        returning theme, analysis_notifications, failure_notifications,
                                  stale_notifications
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "user_id": actor_user_id,
                        "theme": theme,
                        "analysis_notifications": analysis_notifications,
                        "failure_notifications": failure_notifications,
                        "stale_notifications": stale_notifications,
                    },
                )
                .mappings()
                .one()
            )
        return WorkspacePreferences(**row)

    def activate_invitation(
        self,
        *,
        token: str,
        display_name: str,
        password: str,
    ) -> ActivationResult:
        with self._engine.connect() as lock_connection:
            lock_connection.execute(
                text("select pg_advisory_lock(hashtextextended(:scope, 0))"),
                {"scope": f"invitation-activation:{sha256(token.encode()).hexdigest()}"},
            )
            try:
                return self._activate_invitation_once(
                    token=token,
                    display_name=display_name,
                    password=password,
                )
            finally:
                lock_connection.execute(
                    text("select pg_advisory_unlock(hashtextextended(:scope, 0))"),
                    {"scope": f"invitation-activation:{sha256(token.encode()).hexdigest()}"},
                )

    def _activate_invitation_once(
        self,
        *,
        token: str,
        display_name: str,
        password: str,
    ) -> ActivationResult:
        if self._identity is None:
            raise RuntimeError("Identity provider is not configured")
        invitation = self._resolve_pending_invitation(token, allow_accepted=True)
        if invitation["status"] == "accepted":
            return self._resume_accepted_invitation(
                invitation=invitation,
                email=invitation["email"],
                password=password,
            )
        now = datetime.now(UTC)
        email = invitation["email"]
        if self._identity.find_user_by_email(email) is not None:
            raise AccountAlreadyExists

        user = self._identity.create_user(
            email=email,
            password=password,
            display_name=display_name.strip(),
        )
        try:
            with self._engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        insert into public.profiles (id, display_name)
                        values (:user_id, :display_name)
                        """
                    ),
                    {"user_id": user.id, "display_name": display_name.strip()},
                )
                connection.execute(
                    text(
                        """
                        insert into public.memberships (workspace_id, user_id, role)
                        values (:workspace_id, :user_id, :role)
                        """
                    ),
                    {
                        "workspace_id": invitation["workspace_id"],
                        "user_id": user.id,
                        "role": invitation["role"],
                    },
                )
                accepted = connection.execute(
                    text(
                        """
                        update public.invitations
                        set status = 'accepted', accepted_by = :user_id, accepted_at = :accepted_at
                        where id = :invitation_id
                          and status = 'pending'
                          and expires_at > :accepted_at
                        """
                    ),
                    {
                        "user_id": user.id,
                        "accepted_at": now,
                        "invitation_id": invitation["id"],
                    },
                )
                if accepted.rowcount != 1:
                    raise InvalidInvitation
                connection.execute(
                    text(
                        """
                        insert into public.audit_events (
                          workspace_id, actor_user_id, action, subject_type, subject_id, metadata
                        ) values (
                          :workspace_id, :user_id, 'invitation.accepted',
                          'invitation', :subject_id, '{}'::jsonb
                        )
                        """
                    ),
                    {
                        "workspace_id": invitation["workspace_id"],
                        "user_id": user.id,
                        "subject_id": str(invitation["id"]),
                    },
                )
        except Exception:
            self._identity.delete_user(user.id)
            raise

        session = self._identity.sign_in_with_password(email=email, password=password)
        return ActivationResult(
            user_id=session.user_id,
            email=session.email,
            workspace_id=invitation["workspace_id"],
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
            welcome_required=True,
        )

    def resolve_invitation(self, token: str) -> InvitationDetails:
        if self._identity is None:
            raise RuntimeError("Identity provider is not configured")
        invitation = self._resolve_pending_invitation(token)
        return InvitationDetails(
            email=invitation["email"],
            workspace_name=invitation["workspace_name"],
            role=MembershipRole(invitation["role"]),
            expires_at=invitation["expires_at"],
            account_exists=self._identity.find_user_by_email(invitation["email"]) is not None,
        )

    def accept_invitation_for_existing_user(
        self,
        *,
        token: str,
        email: str,
        password: str,
    ) -> ActivationResult:
        with self._engine.connect() as lock_connection:
            lock_connection.execute(
                text("select pg_advisory_lock(hashtextextended(:scope, 0))"),
                {"scope": f"invitation-activation:{sha256(token.encode()).hexdigest()}"},
            )
            try:
                return self._accept_invitation_for_existing_user_once(
                    token=token,
                    email=email,
                    password=password,
                )
            finally:
                lock_connection.execute(
                    text("select pg_advisory_unlock(hashtextextended(:scope, 0))"),
                    {"scope": f"invitation-activation:{sha256(token.encode()).hexdigest()}"},
                )

    def _accept_invitation_for_existing_user_once(
        self,
        *,
        token: str,
        email: str,
        password: str,
    ) -> ActivationResult:
        if self._identity is None:
            raise RuntimeError("Identity provider is not configured")
        invitation = self._resolve_pending_invitation(token, allow_accepted=True)
        if invitation["status"] == "accepted":
            return self._resume_accepted_invitation(
                invitation=invitation,
                email=email,
                password=password,
            )
        session = self._identity.sign_in_with_password(email=email, password=password)
        if session.email.casefold() != invitation["email"].casefold():
            raise InvitationEmailMismatch
        with self._engine.begin() as connection:
            membership_exists = connection.execute(
                text(
                    "select 1 from public.memberships "
                    "where workspace_id = :workspace_id and user_id = :user_id"
                ),
                {"workspace_id": invitation["workspace_id"], "user_id": session.user_id},
            ).scalar_one_or_none()
            connection.execute(
                text(
                    """
                    insert into public.profiles (id, display_name)
                    values (:user_id, :display_name)
                    on conflict (id) do nothing
                    """
                ),
                {"user_id": session.user_id, "display_name": session.email.split("@")[0]},
            )
            connection.execute(
                text(
                    """
                    insert into public.memberships (workspace_id, user_id, role)
                    values (:workspace_id, :user_id, :role)
                    on conflict (workspace_id, user_id) do nothing
                    """
                ),
                {
                    "workspace_id": invitation["workspace_id"],
                    "user_id": session.user_id,
                    "role": invitation["role"],
                },
            )
            accepted_at = datetime.now(UTC)
            accepted = connection.execute(
                text(
                    """
                    update public.invitations
                    set status = 'accepted', accepted_by = :user_id, accepted_at = :accepted_at
                    where id = :invitation_id
                      and status = 'pending'
                      and expires_at > :accepted_at
                    """
                ),
                {
                    "user_id": session.user_id,
                    "accepted_at": accepted_at,
                    "invitation_id": invitation["id"],
                },
            )
            if accepted.rowcount != 1:
                raise InvalidInvitation
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id
                    ) values (
                      :workspace_id, :user_id, 'invitation.accepted',
                      'invitation', :subject_id
                    )
                    """
                ),
                {
                    "workspace_id": invitation["workspace_id"],
                    "user_id": session.user_id,
                    "subject_id": str(invitation["id"]),
                },
            )
        return ActivationResult(
            user_id=session.user_id,
            email=session.email,
            workspace_id=invitation["workspace_id"],
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
            welcome_required=membership_exists is None,
        )

    def _resume_accepted_invitation(
        self,
        *,
        invitation: RowMapping,
        email: str,
        password: str,
    ) -> ActivationResult:
        if self._identity is None:
            raise RuntimeError("Identity provider is not configured")
        session = self._identity.sign_in_with_password(email=email, password=password)
        if session.email.casefold() != invitation["email"].casefold():
            raise InvitationEmailMismatch
        if session.user_id != invitation["accepted_by"]:
            raise InvalidInvitation
        with self._engine.connect() as connection:
            membership = (
                connection.execute(
                    text(
                        "select created_at, welcome_seen_at from public.memberships "
                        "where workspace_id = :workspace_id and user_id = :user_id"
                    ),
                    {"workspace_id": invitation["workspace_id"], "user_id": session.user_id},
                )
                .mappings()
                .one_or_none()
            )
        if membership is None:
            raise InvalidInvitation
        joined_from_this_invitation = membership["created_at"] >= invitation["created_at"]
        return ActivationResult(
            user_id=session.user_id,
            email=session.email,
            workspace_id=invitation["workspace_id"],
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=session.expires_in,
            welcome_required=(
                membership["welcome_seen_at"] is None and joined_from_this_invitation
            ),
        )

    def _resolve_pending_invitation(
        self,
        token: str,
        *,
        allow_accepted: bool = False,
    ) -> RowMapping:
        token_hash = sha256(token.encode("utf-8")).digest()
        with self._engine.connect() as connection:
            invitation = (
                connection.execute(
                    text(
                        """
                    select i.id, i.workspace_id, i.email::text, i.role,
                           i.status, i.created_at, i.expires_at, i.accepted_by,
                           w.name as workspace_name
                    from public.invitations i
                    join public.workspaces w on w.id = i.workspace_id
                    where i.token_hash = :token_hash
                    """
                    ),
                    {"token_hash": token_hash},
                )
                .mappings()
                .one_or_none()
            )
        if (
            invitation is None
            or (
                invitation["status"] != "pending"
                and not (allow_accepted and invitation["status"] == "accepted")
            )
            or invitation["expires_at"] <= datetime.now(UTC)
        ):
            raise InvalidInvitation
        return invitation

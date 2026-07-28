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
from oslo_api.tiering.policy import PlanPolicy, get_plan_policy
from oslo_api.tiering.repository import (
    count_monthly_analysis_usage,
    get_workspace_plan,
    record_limit_event,
)
from oslo_api.tiering.repository import (
    set_workspace_plan as persist_workspace_plan,
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


class InvitationLimitReached(Exception):
    """Raised when the workspace has used its monthly invitation allocation."""

    def __init__(self, policy: PlanPolicy | None = None) -> None:
        policy = policy or get_plan_policy("free")
        self.plan = policy.code.value
        self.plan_label = policy.label
        self.monthly_invitation_limit = policy.monthly_invitation_limit
        self.remedies = ("wait_for_next_month", "compare_plans")
        super().__init__("Workspace monthly invitation allocation reached")


class CollaboratorSeatLimitReached(Exception):
    """Raised when another collaborator would exceed the workspace seat cap."""

    def __init__(self, policy: PlanPolicy | None = None) -> None:
        policy = policy or get_plan_policy("free")
        self.plan = policy.code.value
        self.collaborator_seat_limit = policy.collaborator_seat_limit
        self.remedies = ("invite_as_viewer", "compare_plans")
        super().__init__("Workspace collaborator seat limit reached")


class ProjectLimitReached(Exception):
    """Raised when the workspace plan cannot create another active project."""

    def __init__(self, policy: PlanPolicy | None = None) -> None:
        policy = policy or get_plan_policy("free")
        self.plan = policy.code.value
        self.active_project_limit = policy.active_project_limit
        self.remedies = ("archive_project", "compare_plans")
        super().__init__("Workspace active project limit reached")


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

    def _record_blocked_limit_event(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        project_id: UUID | None,
        limit_kind: str,
        details: dict[str, object],
        idempotency_key: str,
    ) -> None:
        # A blocked allocation raises from the caller's transaction. Persist its
        # audit evidence independently so that rollback does not erase it.
        with self._engine.begin() as audit_connection:
            record_limit_event(
                audit_connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                project_id=project_id,
                limit_kind=limit_kind,
                outcome="blocked",
                details=details,
                idempotency_key=idempotency_key,
            )

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
            policy = get_workspace_plan(connection, workspace_id)
            monthly_invites_used = connection.execute(
                text(
                    """
                    select count(*)
                    from public.invitations
                    where workspace_id = :workspace_id
                      and created_at >= date_trunc('month', now())
                      and (
                        status = 'accepted'
                        or (status = 'pending' and expires_at > now())
                      )
                    """
                ),
                {"workspace_id": workspace_id},
            ).scalar_one()
            if monthly_invites_used >= policy.monthly_invitation_limit:
                self._record_blocked_limit_event(
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=None,
                    limit_kind="monthly_invitations",
                    details={
                        "plan": policy.code.value,
                        "limit": policy.monthly_invitation_limit,
                        "used": int(monthly_invites_used),
                        "remedies": ["wait_for_next_month", "compare_plans"],
                    },
                    idempotency_key=f"invite-allocation:{normalised_email}:blocked",
                )
                raise InvitationLimitReached(policy)
            if role is MembershipRole.COLLABORATOR:
                reserved_collaborator_seats = connection.execute(
                    text(
                        """
                        select
                          (
                            select count(*)
                            from public.memberships
                            where workspace_id = :workspace_id
                              and role in ('owner', 'collaborator')
                          )
                          +
                          (
                            select count(*)
                            from public.invitations
                            where workspace_id = :workspace_id
                              and role = 'collaborator'
                              and status = 'pending'
                              and expires_at > now()
                          )
                        """
                    ),
                    {"workspace_id": workspace_id},
                ).scalar_one()
                decision = policy.decide_collaborator_capacity(
                    occupied_seats=int(reserved_collaborator_seats)
                )
                if not decision.allowed:
                    self._record_blocked_limit_event(
                        workspace_id=workspace_id,
                        actor_user_id=actor_user_id,
                        project_id=None,
                        limit_kind="collaborator_seats",
                        details={
                            "plan": policy.code.value,
                            "limit": policy.collaborator_seat_limit,
                            "occupied": int(reserved_collaborator_seats),
                            "remedies": list(decision.remedies),
                        },
                        idempotency_key=f"invite-seat:{normalised_email}:blocked",
                    )
                    raise CollaboratorSeatLimitReached(policy)
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
            if role is MembershipRole.COLLABORATOR:
                record_limit_event(
                    connection,
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=None,
                    limit_kind="collaborator_seats",
                    outcome="allowed",
                    details={
                        "plan": policy.code.value,
                        "limit": policy.collaborator_seat_limit,
                        "occupied_before": int(reserved_collaborator_seats),
                    },
                    idempotency_key=f"invite-seat:{issued.invitation.id}:allowed",
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
            policy = get_workspace_plan(connection, workspace_id)
            decision = policy.decide_project_capacity(active_projects=int(active_count))
            if not decision.allowed:
                self._record_blocked_limit_event(
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=None,
                    limit_kind="active_projects",
                    details={
                        "plan": policy.code.value,
                        "limit": policy.active_project_limit,
                        "active": int(active_count),
                        "remedies": list(decision.remedies),
                    },
                    idempotency_key=f"project-create:{project_id}:blocked",
                )
                raise ProjectLimitReached(policy)
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
            record_limit_event(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                project_id=project_id,
                limit_kind="active_projects",
                outcome="allowed",
                details={
                    "plan": policy.code.value,
                    "limit": policy.active_project_limit,
                    "active_before": int(active_count),
                },
                idempotency_key=f"project-create:{project_id}:allowed",
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
            member_count = int(
                connection.execute(
                    text(
                        """
                        select count(*)
                        from public.memberships
                        where workspace_id = :workspace_id
                        """
                    ),
                    {"workspace_id": workspace_id},
                ).scalar_one()
            )
            policy = get_workspace_plan(connection, workspace_id)
            monthly_analyses_used = count_monthly_analysis_usage(
                connection, workspace_id=workspace_id
            )
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
                        with activity as (
                          select
                            'analysis:' || run.id::text || ':' || run.status::text as key,
                            run.project_id,
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
                            coalesce(run.completed_at, run.updated_at) as created_at
                          from public.analysis_runs run
                          where run.workspace_id = :workspace_id
                            and run.status in ('completed', 'failed')

                          union all

                          select
                            'review:' || event.aggregate_id::text as key,
                            (event.payload ->> 'project_id')::uuid as project_id,
                            'review' as kind,
                            'completed' as status,
                            coalesce(event.payload ->> 'reviewer_name', 'A reviewer')
                              || ' submitted '
                              || replace(
                                coalesce(event.payload ->> 'response_kind', 'feedback'),
                                '_',
                                ' '
                              ) as title,
                            event.occurred_at as created_at
                          from public.outbox_events event
                          where event.workspace_id = :workspace_id
                            and event.event_type = 'review.responded'
                        )
                        select
                          activity.key,
                          activity.project_id,
                          project.name as project_name,
                          activity.kind,
                          activity.status,
                          activity.title,
                          activity.created_at,
                          reads.notification_key is not null as read
                        from activity
                        join public.projects project on project.id = activity.project_id
                        left join public.workspace_notification_reads reads
                          on reads.workspace_id = :workspace_id
                         and reads.user_id = :actor_user_id
                         and reads.notification_key = activity.key
                        order by activity.created_at desc
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
            plan=policy.code.value,
            active_project_limit=policy.active_project_limit,
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
            plan_label=policy.label,
            price_usd_monthly=policy.price_usd_monthly,
            document_limit=policy.document_limit,
            word_limit=policy.word_limit,
            collaborator_seat_limit=policy.collaborator_seat_limit,
            monthly_analysis_limit=policy.monthly_analysis_limit,
            monthly_analyses_used=monthly_analyses_used,
            can_manage_plan=role is MembershipRole.OWNER,
            member_count=member_count,
        )

    def set_workspace_plan(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        plan: str,
    ) -> WorkspaceSummary:
        with self._engine.begin() as connection:
            if (
                SqlMembershipReader(connection).role_for(workspace_id, actor_user_id)
                is not MembershipRole.OWNER
            ):
                raise InvitePermissionDenied
            connection.execute(
                text("select pg_advisory_xact_lock(hashtextextended(:scope, 0))"),
                {"scope": f"workspace-plan:{workspace_id}"},
            )
            previous = get_workspace_plan(connection, workspace_id)
            selected = persist_workspace_plan(
                connection,
                workspace_id=workspace_id,
                actor_user_id=actor_user_id,
                plan_code=plan,
            )
            connection.execute(
                text(
                    """
                    insert into public.audit_events (
                      workspace_id, actor_user_id, action, subject_type, subject_id, metadata
                    ) values (
                      :workspace_id, :actor_user_id, 'workspace.plan_changed',
                      'workspace', :subject_id, cast(:metadata as jsonb)
                    )
                    """
                ),
                {
                    "workspace_id": workspace_id,
                    "actor_user_id": actor_user_id,
                    "subject_id": str(workspace_id),
                    "metadata": json.dumps(
                        {
                            "from": previous.code.value,
                            "to": selected.code.value,
                            "simulated": True,
                        }
                    ),
                },
            )
        return self.get_workspace_summary(
            actor_user_id=actor_user_id, workspace_id=workspace_id
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
                policy = get_workspace_plan(connection, workspace_id)
                decision = policy.decide_project_capacity(
                    active_projects=int(active_count)
                )
                if not decision.allowed:
                    self._record_blocked_limit_event(
                        workspace_id=workspace_id,
                        actor_user_id=actor_user_id,
                        project_id=project_id,
                        limit_kind="active_projects",
                        details={
                            "plan": policy.code.value,
                            "limit": policy.active_project_limit,
                            "active": int(active_count),
                            "remedies": list(decision.remedies),
                        },
                        idempotency_key=f"project-restore:{project_id}:blocked",
                    )
                    raise ProjectLimitReached(policy)
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
            if not archived:
                record_limit_event(
                    connection,
                    workspace_id=workspace_id,
                    actor_user_id=actor_user_id,
                    project_id=project_id,
                    limit_kind="active_projects",
                    outcome="allowed",
                    details={
                        "plan": policy.code.value,
                        "limit": policy.active_project_limit,
                        "active_before": int(active_count),
                    },
                    idempotency_key=f"project-restore:{project_id}:allowed",
                )
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
                if not notification_key.startswith(("analysis:", "review:")):
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
            actor_role = SqlMembershipReader(connection).role_for(
                workspace_id, actor_user_id
            )
            if actor_role is None:
                raise InvitePermissionDenied
            connection.execute(
                text(
                    """
                    insert into public.workspace_member_preferences (workspace_id, user_id)
                    values (:workspace_id, :user_id)
                    on conflict (workspace_id, user_id) do nothing
                    """
                ),
                {"workspace_id": workspace_id, "user_id": actor_user_id},
            )
            row = (
                connection.execute(
                    text(
                        """
                        select preference.theme, preference.analysis_notifications,
                               preference.failure_notifications,
                               preference.stale_notifications,
                               coalesce(
                                 nullif(preference.display_name, ''),
                                 profile.display_name
                               ) as display_name,
                               preference.role_title,
                               workspace.name as workspace_name,
                               preference.mentions_notifications,
                               preference.reply_notifications,
                               preference.shared_notifications
                        from public.workspace_member_preferences preference
                        join public.profiles profile on profile.id = preference.user_id
                        join public.workspaces workspace
                          on workspace.id = preference.workspace_id
                        where preference.workspace_id = :workspace_id
                          and preference.user_id = :user_id
                        """
                    ),
                    {"workspace_id": workspace_id, "user_id": actor_user_id},
                )
                .mappings()
                .one()
            )
        return WorkspacePreferences(**row, actor_role=actor_role.value)

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
        if theme not in {"dark", "light", "system"}:
            raise ValueError("Unsupported theme")
        display_name = " ".join(display_name.split())
        role_title = " ".join(role_title.split())
        workspace_name = " ".join(workspace_name.split())
        if not 1 <= len(display_name) <= 120:
            raise ValueError("Display name must be between 1 and 120 characters")
        if len(role_title) > 120:
            raise ValueError("Role title must be 120 characters or fewer")
        if not 1 <= len(workspace_name) <= 120:
            raise ValueError("Workspace name must be between 1 and 120 characters")
        with self._engine.begin() as connection:
            actor_role = SqlMembershipReader(connection).role_for(
                workspace_id, actor_user_id
            )
            if actor_role is None:
                raise InvitePermissionDenied
            current_workspace_name = connection.execute(
                text("select name from public.workspaces where id = :workspace_id"),
                {"workspace_id": workspace_id},
            ).scalar_one()
            if workspace_name != current_workspace_name:
                if actor_role is not MembershipRole.OWNER:
                    raise InvitePermissionDenied
                connection.execute(
                    text(
                        """
                        update public.workspaces
                        set name = :workspace_name, updated_at = now()
                        where id = :workspace_id
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "workspace_name": workspace_name,
                    },
                )
            row = (
                connection.execute(
                    text(
                        """
                        insert into public.workspace_member_preferences (
                          workspace_id, user_id, theme, analysis_notifications,
                          failure_notifications, stale_notifications, display_name,
                          role_title, mentions_notifications, reply_notifications,
                          shared_notifications
                        ) values (
                          :workspace_id, :user_id, :theme, :analysis_notifications,
                          :failure_notifications, :stale_notifications, :display_name,
                          :role_title, :mentions_notifications, :reply_notifications,
                          :shared_notifications
                        )
                        on conflict (workspace_id, user_id) do update set
                          theme = excluded.theme,
                          analysis_notifications = excluded.analysis_notifications,
                          failure_notifications = excluded.failure_notifications,
                          stale_notifications = excluded.stale_notifications,
                          display_name = excluded.display_name,
                          role_title = excluded.role_title,
                          mentions_notifications = excluded.mentions_notifications,
                          reply_notifications = excluded.reply_notifications,
                          shared_notifications = excluded.shared_notifications,
                          updated_at = now()
                        returning theme, analysis_notifications, failure_notifications,
                                  stale_notifications, display_name, role_title,
                                  mentions_notifications, reply_notifications,
                                  shared_notifications
                        """
                    ),
                    {
                        "workspace_id": workspace_id,
                        "user_id": actor_user_id,
                        "theme": theme,
                        "analysis_notifications": analysis_notifications,
                        "failure_notifications": failure_notifications,
                        "stale_notifications": stale_notifications,
                        "display_name": display_name,
                        "role_title": role_title,
                        "mentions_notifications": mentions_notifications,
                        "reply_notifications": reply_notifications,
                        "shared_notifications": shared_notifications,
                    },
                )
                .mappings()
                .one()
            )
        return WorkspacePreferences(
            **row,
            workspace_name=workspace_name,
            actor_role=actor_role.value,
        )

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

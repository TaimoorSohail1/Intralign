from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import httpx
import pytest
from sqlalchemy import create_engine, text

from oslo_api.application import (
    DatabaseSliceOneApplication,
    InvalidInvitation,
    InvitationDeliveryFailed,
    ProjectArchiveDenied,
)
from oslo_api.identity import SupabaseIdentityProvider
from oslo_api.invitations import InvitationStatus, InvitePermissionDenied, MembershipRole
from oslo_api.project_access import find_project_access
from oslo_api.settings import Settings

SETTINGS = Settings()  # type: ignore[call-arg]
DATABASE_URL = SETTINGS.database_url
SUPABASE_URL = SETTINGS.supabase_url
SUPABASE_SECRET_KEY = SETTINGS.supabase_secret_key
# Keep invitation integration fixtures separate from the local platform-admin
# workspace (…0099). Reusing that workspace changes its security semantics and
# can make later browser tests treat the administrator as a tenant Owner.
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000098")


@pytest.fixture(autouse=True)
def isolated_invitation_workspace():
    """Keep invitation integration tests independent from local demo data and each other."""
    engine = create_engine(DATABASE_URL)

    def reset_workspace() -> None:
        with engine.begin() as connection:
            owner_id = connection.execute(
                text("select id from auth.users where email = 'admin@oslo.local'")
            ).scalar_one()
            connection.execute(
                text(
                    "insert into public.workspaces (id, name, created_by) "
                    "values (:workspace_id, :name, :owner_id) "
                    "on conflict (id) do update set name = excluded.name, "
                    "created_by = excluded.created_by"
                ),
                {
                    "workspace_id": WORKSPACE_ID,
                    "name": "Invitation Integration Tests",
                    "owner_id": owner_id,
                },
            )
            connection.execute(
                text("delete from public.invitations where workspace_id = :workspace_id"),
                {"workspace_id": WORKSPACE_ID},
            )
            connection.execute(
                text("delete from public.project_memberships where workspace_id = :workspace_id"),
                {"workspace_id": WORKSPACE_ID},
            )
            connection.execute(
                text("delete from public.projects where workspace_id = :workspace_id"),
                {"workspace_id": WORKSPACE_ID},
            )
            connection.execute(
                text("delete from public.memberships where workspace_id = :workspace_id"),
                {"workspace_id": WORKSPACE_ID},
            )
            connection.execute(
                text(
                    "insert into public.memberships (workspace_id, user_id, role) "
                    "values (:workspace_id, :owner_id, 'owner')"
                ),
                {"workspace_id": WORKSPACE_ID, "owner_id": owner_id},
            )
            connection.execute(
                text(
                    "delete from public.workspace_subscriptions "
                    "where workspace_id = :workspace_id"
                ),
                {"workspace_id": WORKSPACE_ID},
            )
            connection.execute(
                text(
                    "delete from public.workspace_limit_events "
                    "where workspace_id = :workspace_id"
                ),
                {"workspace_id": WORKSPACE_ID},
            )

    reset_workspace()
    yield
    reset_workspace()


class RecordingInvitationMailer:
    def __init__(self) -> None:
        self.messages = []

    def send_invitation(self, *, email, workspace_name, role, activation_url, expires_at) -> None:
        self.messages.append((email, workspace_name, activation_url, expires_at, role))


class FailingInvitationMailer:
    def send_invitation(self, **_kwargs) -> None:
        raise OSError("SMTP unavailable")


def test_owner_invitation_is_persisted_and_delivered_without_storing_raw_token() -> None:
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"),
            {"email": "integration.member@example.com"},
        )
    application = DatabaseSliceOneApplication(
        engine=engine,
        mailer=mailer,
        web_url="http://localhost:3000",
    )

    invitation = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email="integration.member@example.com",
    )

    assert invitation.status is InvitationStatus.PENDING
    assert len(mailer.messages) == 1
    activation_url = mailer.messages[0][2]
    raw_token = activation_url.rsplit("=", maxsplit=1)[1]
    with engine.connect() as connection:
        stored_hash = connection.execute(
            text("select token_hash from public.invitations where id = :id"),
            {"id": invitation.id},
        ).scalar_one()
        audit_action = connection.execute(
            text(
                "select action from public.audit_events "
                "where subject_id = :id order by id desc limit 1"
            ),
            {"id": str(invitation.id)},
        ).scalar_one()

    assert raw_token.encode() not in stored_hash
    assert audit_action == "invitation.created"


def test_invitations_are_not_plan_metered_or_written_as_limit_events() -> None:
    engine = create_engine(DATABASE_URL)
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
    application = DatabaseSliceOneApplication(
        engine=engine,
        mailer=RecordingInvitationMailer(),
        web_url="http://localhost:3000",
    )

    for index in range(3):
        application.invite_member(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            email=f"monthly-limit-{index}@example.com",
        )

    with engine.connect() as connection:
        invitation_count = connection.execute(
            text(
                """
                select count(*) from public.invitations
                where workspace_id = :workspace_id and status = 'pending'
                """
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
        event_count = connection.execute(
            text(
                "select count(*) from public.workspace_limit_events "
                "where workspace_id = :workspace_id "
                "and limit_kind in ('monthly_invitations', 'collaborator_seats')"
            ),
            {"workspace_id": WORKSPACE_ID},
        ).scalar_one()
    assert invitation_count == 3
    assert event_count == 0


def test_duplicate_pending_invitation_is_idempotent_after_email_normalisation() -> None:
    email = "duplicate.integration@example.com"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"), {"email": email}
        )
    application = DatabaseSliceOneApplication(
        engine=engine, mailer=mailer, web_url="http://localhost:3000"
    )

    first = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email="  Duplicate.Integration@Example.com ",
    )
    second = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email=email,
    )

    assert second.id == first.id
    assert second.role.value == "owner"
    assert len(mailer.messages) == 1
    with engine.connect() as connection:
        count = connection.execute(
            text(
                "select count(*) from public.invitations "
                "where workspace_id = :workspace_id and email = :email "
                "and status = 'pending'"
            ),
            {"workspace_id": WORKSPACE_ID, "email": email},
        ).scalar_one()
    assert count == 1


def test_concurrent_double_send_creates_one_pending_invitation() -> None:
    email = "concurrent.invite.integration@example.com"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"), {"email": email}
        )
    application = DatabaseSliceOneApplication(
        engine=engine, mailer=mailer, web_url="http://localhost:3000"
    )

    def invite_once():
        return application.invite_member(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            email=email,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        invitations = list(executor.map(lambda _index: invite_once(), range(2)))

    assert len({invitation.id for invitation in invitations}) == 1
    assert len(mailer.messages) == 1


def test_accept_and_revoke_race_has_one_terminal_winner() -> None:
    email = "admin@oslo.local"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"), {"email": email}
        )
    invitation = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email=email,
    )
    raw_token = mailer.messages[0][2].rsplit("=", maxsplit=1)[1]

    def accept():
        try:
            application.accept_invitation_for_existing_user(
                token=raw_token,
                email=email,
                password="OsloLocalAdmin123!",
            )
            return "accepted"
        except InvalidInvitation:
            return "unavailable"

    def revoke():
        try:
            application.revoke_invitation(
                actor_user_id=owner_id,
                workspace_id=WORKSPACE_ID,
                invitation_id=invitation.id,
            )
            return "revoked"
        except InvalidInvitation:
            return "unavailable"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = [executor.submit(accept), executor.submit(revoke)]
        outcomes = [future.result() for future in results]

    assert outcomes.count("unavailable") == 1
    assert ("accepted" in outcomes) ^ ("revoked" in outcomes)


def test_existing_member_acceptance_is_idempotent_and_does_not_downgrade_role() -> None:
    email = "admin@oslo.local"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        previous_membership = connection.execute(
            text(
                "select welcome_seen_at, created_at from public.memberships "
                "where workspace_id = :workspace_id and user_id = :user_id"
            ),
            {"workspace_id": WORKSPACE_ID, "user_id": owner_id},
        ).mappings().one()
        connection.execute(
            text(
                "update public.memberships set welcome_seen_at = null "
                "where workspace_id = :workspace_id and user_id = :user_id"
            ),
            {"workspace_id": WORKSPACE_ID, "user_id": owner_id},
        )
        connection.execute(
            text("delete from public.invitations where email = :email"), {"email": email}
        )
    try:
        application.invite_member(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            email=email,
        )
        raw_token = mailer.messages[0][2].rsplit("=", maxsplit=1)[1]

        activation = application.accept_invitation_for_existing_user(
            token=raw_token,
            email=email,
            password="OsloLocalAdmin123!",
        )
        with engine.begin() as connection:
            connection.execute(
                text(
                    "update public.memberships set created_at = ("
                    "select created_at from public.invitations "
                    "where email = :email and status = 'accepted'"
                    ") where workspace_id = :workspace_id and user_id = :user_id"
                ),
                {
                    "email": email,
                    "workspace_id": WORKSPACE_ID,
                    "user_id": owner_id,
                },
            )
        repeated_activation = application.accept_invitation_for_existing_user(
            token=raw_token,
            email=email,
            password="OsloLocalAdmin123!",
        )

        assert activation.welcome_required is False
        assert repeated_activation.welcome_required is False
        with engine.connect() as connection:
            memberships = (
                connection.execute(
                    text(
                        "select role from public.memberships "
                        "where workspace_id = :workspace_id and user_id = :user_id"
                    ),
                    {"workspace_id": WORKSPACE_ID, "user_id": owner_id},
                )
                .scalars()
                .all()
            )
        assert memberships == ["owner"]
    finally:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "update public.memberships "
                    "set welcome_seen_at = :welcome_seen_at, created_at = :created_at "
                    "where workspace_id = :workspace_id and user_id = :user_id"
                ),
                {
                    "welcome_seen_at": previous_membership["welcome_seen_at"],
                    "created_at": previous_membership["created_at"],
                    "workspace_id": WORKSPACE_ID,
                    "user_id": owner_id,
                },
            )


def test_existing_user_can_join_a_different_workspace() -> None:
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    workspace_id = uuid4()
    owner_email = f"workspace-owner-{workspace_id}@example.com"
    owner = identity.create_user(
        email=owner_email,
        password="WorkspaceOwner123!",
        display_name="Workspace Owner",
    )
    try:
        with engine.begin() as connection:
            admin_id = connection.execute(
                text("select id from auth.users where email = 'admin@oslo.local'")
            ).scalar_one()
            connection.execute(
                text("insert into public.profiles (id, display_name) values (:id, :name)"),
                {"id": owner.id, "name": "Workspace Owner"},
            )
            connection.execute(
                text(
                    "insert into public.workspaces (id, name, created_by) "
                    "values (:id, :name, :owner_id)"
                ),
                {"id": workspace_id, "name": "Second Workspace", "owner_id": owner.id},
            )
            connection.execute(
                text(
                    "insert into public.memberships (workspace_id, user_id, role) "
                    "values (:workspace_id, :owner_id, 'owner')"
                ),
                {"workspace_id": workspace_id, "owner_id": owner.id},
            )

        application.invite_member(
            actor_user_id=owner.id,
            workspace_id=workspace_id,
            email="admin@oslo.local",
        )
        raw_token = mailer.messages[0][2].rsplit("=", maxsplit=1)[1]
        activation = application.accept_invitation_for_existing_user(
            token=raw_token,
            email="admin@oslo.local",
            password="OsloLocalAdmin123!",
        )

        assert activation.workspace_id == workspace_id
        assert activation.welcome_required is True
        with engine.connect() as connection:
            role = connection.execute(
                text(
                    "select role from public.memberships "
                    "where workspace_id = :workspace_id and user_id = :user_id"
                ),
                {"workspace_id": workspace_id, "user_id": admin_id},
            ).scalar_one()
        assert role == "owner"
    finally:
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.workspaces where id = :workspace_id"),
                {"workspace_id": workspace_id},
            )
        identity.delete_user(owner.id)


def test_resend_invalidates_the_old_link_and_only_the_new_link_resolves() -> None:
    email = "resend.old-link.integration@example.com"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"),
            {"email": email},
        )
    original = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email=email,
    )
    old_token = mailer.messages[-1][2].rsplit("=", maxsplit=1)[1]
    replacement = application.resend_invitation(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        invitation_id=original.id,
    )
    new_token = mailer.messages[-1][2].rsplit("=", maxsplit=1)[1]

    with pytest.raises(InvalidInvitation):
        application.resolve_invitation(old_token)
    resolved = application.resolve_invitation(new_token)

    assert replacement.id != original.id
    assert resolved.email == email


@pytest.mark.parametrize("state", ["expired", "revoked", "accepted"])
def test_resolve_rejects_terminal_or_expired_invitations(state: str) -> None:
    email = f"{state}.link.integration@example.com"
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"),
            {"email": email},
        )
    invitation = application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email=email,
    )
    raw_token = mailer.messages[-1][2].rsplit("=", maxsplit=1)[1]
    now = datetime.now(UTC)
    with engine.begin() as connection:
        if state == "expired":
            connection.execute(
                text(
                    "update public.invitations "
                    "set created_at = :created_at, expires_at = :expires_at "
                    "where id = :invitation_id"
                ),
                {
                    "created_at": now - timedelta(days=8),
                    "expires_at": now - timedelta(days=1),
                    "invitation_id": invitation.id,
                },
            )
        elif state == "revoked":
            connection.execute(
                text(
                    "update public.invitations set status = 'revoked', revoked_at = :now "
                    "where id = :invitation_id"
                ),
                {"now": now, "invitation_id": invitation.id},
            )
        else:
            connection.execute(
                text(
                    "update public.invitations "
                    "set status = 'accepted', accepted_by = :user_id, accepted_at = :now "
                    "where id = :invitation_id"
                ),
                {"user_id": owner_id, "now": now, "invitation_id": invitation.id},
            )

    with pytest.raises(InvalidInvitation):
        application.resolve_invitation(raw_token)


def test_failed_email_delivery_does_not_leave_a_pending_invitation() -> None:
    email = "delivery.failure.integration@example.com"
    engine = create_engine(DATABASE_URL)
    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text("delete from public.invitations where email = :email"), {"email": email}
        )
    failing = DatabaseSliceOneApplication(
        engine=engine, mailer=FailingInvitationMailer(), web_url="http://localhost:3000"
    )

    with pytest.raises(InvitationDeliveryFailed):
        failing.invite_member(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            email=email,
        )

    with engine.connect() as connection:
        pending = connection.execute(
            text(
                "select count(*) from public.invitations "
                "where email = :email and status = 'pending'"
            ),
            {"email": email},
        ).scalar_one()

    assert pending == 0


def test_concurrent_activation_submissions_are_idempotent() -> None:
    email = "activation.integration@example.com"
    engine = create_engine(DATABASE_URL)
    headers = {
        "apikey": SUPABASE_SECRET_KEY,
        "authorization": f"Bearer {SUPABASE_SECRET_KEY}",
    }
    with httpx.Client(base_url=SUPABASE_URL, headers=headers) as admin:
        users = admin.get("/auth/v1/admin/users", params={"page": 1, "per_page": 1000}).json()[
            "users"
        ]
        existing_user = next((user for user in users if user["email"] == email), None)
        with engine.begin() as connection:
            connection.execute(
                text("delete from public.invitations where email = :email"),
                {"email": email},
            )
            if existing_user:
                connection.execute(
                    text("delete from public.audit_events where actor_user_id = :user_id"),
                    {"user_id": existing_user["id"]},
                )
        if existing_user:
            admin.delete(f"/auth/v1/admin/users/{existing_user['id']}").raise_for_status()

    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    with engine.connect() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
    application.invite_member(
        actor_user_id=owner_id,
        workspace_id=WORKSPACE_ID,
        email=email,
    )
    raw_token = mailer.messages[0][2].rsplit("=", maxsplit=1)[1]

    def activate_once():
        return application.activate_invitation(
            token=raw_token,
            display_name="Activation Tester",
            password="ActivationTest123!",
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        activation, repeated_activation = [
            future.result()
            for future in [executor.submit(activate_once), executor.submit(activate_once)]
        ]

    assert activation.email == email
    assert repeated_activation.user_id == activation.user_id
    assert repeated_activation.workspace_id == activation.workspace_id
    assert activation.workspace_id == WORKSPACE_ID
    assert activation.welcome_required is True
    assert activation.access_token
    assert activation.refresh_token
    with engine.connect() as connection:
        membership = connection.execute(
            text(
                "select role, welcome_seen_at from public.memberships "
                "where workspace_id = :workspace_id and user_id = :user_id"
            ),
            {"workspace_id": WORKSPACE_ID, "user_id": activation.user_id},
        ).one()
        invitation_status = connection.execute(
            text("select status from public.invitations where email = :email"),
            {"email": email},
        ).scalar_one()
        membership_count = connection.execute(
            text(
                "select count(*) from public.memberships "
                "where workspace_id = :workspace_id and user_id = :user_id"
            ),
            {"workspace_id": WORKSPACE_ID, "user_id": activation.user_id},
        ).scalar_one()

    assert membership.role == "owner"
    assert membership.welcome_seen_at is None
    assert invitation_status == "accepted"
    assert membership_count == 1


def test_delegate_pm_invitation_grants_only_the_assigned_project() -> None:
    engine = create_engine(DATABASE_URL)
    mailer = RecordingInvitationMailer()
    identity = SupabaseIdentityProvider(
        client=httpx.Client(timeout=20),
        supabase_url=SUPABASE_URL,
        api_key=SUPABASE_SECRET_KEY,
    )
    application = DatabaseSliceOneApplication(
        engine=engine,
        identity=identity,
        mailer=mailer,
        web_url="http://localhost:3000",
    )
    assigned_project_id = uuid4()
    unassigned_project_id = uuid4()
    delegate_email = f"delegate-pm-{uuid4()}@example.com"
    delegate_user_id = None

    with engine.begin() as connection:
        owner_id = connection.execute(
            text("select id from auth.users where email = 'admin@oslo.local'")
        ).scalar_one()
        connection.execute(
            text(
                """
                insert into public.projects (id, workspace_id, name, status, created_by)
                values
                  (:assigned_id, :workspace_id, 'Assigned project', 'draft', :owner_id),
                  (:unassigned_id, :workspace_id, 'Unassigned project', 'draft', :owner_id)
                """
            ),
            {
                "assigned_id": assigned_project_id,
                "unassigned_id": unassigned_project_id,
                "workspace_id": WORKSPACE_ID,
                "owner_id": owner_id,
            },
        )

    try:
        invitation = application.invite_member(
            actor_user_id=owner_id,
            workspace_id=WORKSPACE_ID,
            project_id=assigned_project_id,
            email=delegate_email,
            role=MembershipRole.DELEGATE_PM,
        )
        raw_token = mailer.messages[0][2].rsplit("=", maxsplit=1)[1]
        activation = application.activate_invitation(
            token=raw_token,
            display_name="Delegate PM",
            password="DelegateProject123!",
        )
        delegate_user_id = activation.user_id

        assert invitation.role is MembershipRole.DELEGATE_PM
        assert invitation.project_id == assigned_project_id
        assert activation.workspace_id == WORKSPACE_ID
        assert activation.welcome_required is False

        session = application.get_session_context(actor_user_id=delegate_user_id)
        summary = application.get_workspace_summary(
            actor_user_id=delegate_user_id,
            workspace_id=WORKSPACE_ID,
        )
        assert session.account_role == MembershipRole.DELEGATE_PM.value
        assert summary.role == MembershipRole.DELEGATE_PM.value
        assert summary.can_create_project is False
        assert summary.can_manage_plan is False
        assert [project.id for project in summary.projects] == [assigned_project_id]

        with engine.connect() as connection:
            assigned_access = find_project_access(
                connection,
                actor_user_id=delegate_user_id,
                project_id=assigned_project_id,
            )
            unassigned_access = find_project_access(
                connection,
                actor_user_id=delegate_user_id,
                project_id=unassigned_project_id,
            )
            workspace_owner_membership = connection.execute(
                text(
                    "select 1 from public.memberships "
                    "where workspace_id = :workspace_id and user_id = :user_id"
                ),
                {"workspace_id": WORKSPACE_ID, "user_id": delegate_user_id},
            ).scalar_one_or_none()

        assert assigned_access is not None
        assert assigned_access.role == MembershipRole.DELEGATE_PM.value
        assert unassigned_access is None
        assert workspace_owner_membership is None

        with pytest.raises(InvitePermissionDenied):
            application.start_first_project(
                actor_user_id=delegate_user_id,
                workspace_id=WORKSPACE_ID,
            )
        with pytest.raises(ProjectArchiveDenied):
            application.archive_project(
                actor_user_id=delegate_user_id,
                workspace_id=WORKSPACE_ID,
                project_id=assigned_project_id,
            )
    finally:
        if delegate_user_id is not None:
            with engine.begin() as connection:
                connection.execute(
                    text("delete from public.audit_events where actor_user_id = :user_id"),
                    {"user_id": delegate_user_id},
                )
                connection.execute(
                    text(
                        "delete from public.workspace_notification_reads "
                        "where user_id = :user_id"
                    ),
                    {"user_id": delegate_user_id},
                )
                connection.execute(
                    text(
                        "delete from public.workspace_member_preferences "
                        "where user_id = :user_id"
                    ),
                    {"user_id": delegate_user_id},
                )
                connection.execute(
                    text("delete from public.project_memberships where user_id = :user_id"),
                    {"user_id": delegate_user_id},
                )
                connection.execute(
                    text("delete from public.invitations where accepted_by = :user_id"),
                    {"user_id": delegate_user_id},
                )
                connection.execute(
                    text("delete from public.profiles where id = :user_id"),
                    {"user_id": delegate_user_id},
                )
            identity.delete_user(delegate_user_id)

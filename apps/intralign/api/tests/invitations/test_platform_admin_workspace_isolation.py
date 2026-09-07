from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from uuid import UUID

from oslo_api.application import DatabaseSliceOneApplication
from oslo_api.slice_one import AuthenticatedUser, AuthSession

ADMIN_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
ADMIN_WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000099")
CLIENT_ID = UUID("018f9f7e-8de2-7000-8000-000000000022")
INVITATION_ID = UUID("018f9f7e-8de2-7000-8000-000000000033")


class FakeResult:
    def __init__(self, value=None, *, rowcount: int = 0) -> None:
        self.value = value
        self.rowcount = rowcount

    def mappings(self):
        return self

    def one_or_none(self):
        return self.value

    def scalar_one(self):
        return self.value

    def scalar_one_or_none(self):
        return self.value


class ActivationConnection:
    def __init__(self, *, platform_admin_invitation: bool) -> None:
        self.platform_admin_invitation = platform_admin_invitation
        self.workspace_insert: dict | None = None
        self.membership_insert: dict | None = None
        self.invitation_update: dict | None = None

    def execute(self, statement, parameters=None):
        sql = " ".join(str(statement).split()).lower()
        parameters = parameters or {}
        if "from public.invitations i" in sql:
            return FakeResult(
                {
                    "id": INVITATION_ID,
                    "workspace_id": ADMIN_WORKSPACE_ID,
                    "email": "client@example.com",
                    "role": "owner",
                    "status": "pending",
                    "created_at": datetime.now(UTC),
                    "expires_at": datetime.now(UTC) + timedelta(days=7),
                    "accepted_by": None,
                    "accepted_workspace_id": None,
                    "invited_by": ADMIN_ID,
                    "workspace_name": "OSLO Staging",
                }
            )
        if "from private.platform_admins" in sql:
            return FakeResult(self.platform_admin_invitation)
        if "insert into public.workspaces" in sql:
            self.workspace_insert = dict(parameters)
        elif "insert into public.memberships" in sql:
            self.membership_insert = dict(parameters)
        elif "update public.invitations" in sql:
            self.invitation_update = dict(parameters)
            return FakeResult(rowcount=1)
        return FakeResult()


class FakeEngine:
    def __init__(self, *, platform_admin_invitation: bool) -> None:
        self.connection = ActivationConnection(
            platform_admin_invitation=platform_admin_invitation
        )

    @contextmanager
    def connect(self):
        yield self.connection

    @contextmanager
    def begin(self):
        yield self.connection


class FakeIdentity:
    def find_user_by_email(self, _email: str):
        return None

    def create_user(self, *, email: str, password: str, display_name: str):
        assert password == "ClientPassword123!"
        assert display_name == "New Client"
        return AuthenticatedUser(id=CLIENT_ID, email=email)

    def delete_user(self, _user_id: UUID) -> None:
        raise AssertionError("Activation should not roll back")

    def sign_in_with_password(self, *, email: str, password: str):
        assert password == "ClientPassword123!"
        return AuthSession(
            user_id=CLIENT_ID,
            email=email,
            access_token="access-token",
            refresh_token="refresh-token",
            expires_in=3600,
        )


class NoopMailer:
    def send_invitation(self, **_kwargs) -> None:
        return None


def activate(*, platform_admin_invitation: bool):
    engine = FakeEngine(platform_admin_invitation=platform_admin_invitation)
    application = DatabaseSliceOneApplication(
        engine=engine,  # type: ignore[arg-type]
        identity=FakeIdentity(),  # type: ignore[arg-type]
        mailer=NoopMailer(),
        web_url="https://oslo.example",
    )
    result = application.activate_invitation(
        token="invitation-token",
        display_name="New Client",
        password="ClientPassword123!",
    )
    return engine.connection, result


def test_platform_admin_invitation_provisions_an_isolated_client_workspace() -> None:
    connection, result = activate(platform_admin_invitation=True)

    assert connection.workspace_insert is not None
    assert result.workspace_id != ADMIN_WORKSPACE_ID
    assert connection.workspace_insert["workspace_id"] == result.workspace_id
    assert connection.membership_insert == {
        "workspace_id": result.workspace_id,
        "user_id": CLIENT_ID,
        "role": "owner",
    }
    assert connection.invitation_update["accepted_workspace_id"] == result.workspace_id


def test_regular_owner_invitation_still_joins_the_existing_workspace() -> None:
    connection, result = activate(platform_admin_invitation=False)

    assert connection.workspace_insert is None
    assert result.workspace_id == ADMIN_WORKSPACE_ID
    assert connection.membership_insert == {
        "workspace_id": ADMIN_WORKSPACE_ID,
        "user_id": CLIENT_ID,
        "role": "owner",
    }
    assert connection.invitation_update["accepted_workspace_id"] == ADMIN_WORKSPACE_ID

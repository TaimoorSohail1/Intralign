from contextlib import contextmanager
from uuid import UUID

import pytest

from oslo_api.application import DatabaseSliceOneApplication, InvitationLimitReached
from oslo_api.invitations import InvitationStatus

ADMIN_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000099")


class FakeResult:
    def __init__(self, value=None) -> None:
        self.value = value

    def mappings(self):
        return self

    def one_or_none(self):
        return self.value

    def scalar_one(self):
        return self.value

    def scalar_one_or_none(self):
        return self.value


class PlatformAdminConnection:
    def __init__(self, *, is_platform_admin: bool) -> None:
        self.is_platform_admin = is_platform_admin
        self.statements: list[str] = []

    def execute(self, statement, _parameters=None):
        sql = " ".join(str(statement).split()).lower()
        self.statements.append(sql)
        if "select exists (select 1 from private.platform_admins" in sql:
            return FakeResult(self.is_platform_admin)
        if "select exists" in sql:
            return FakeResult(True)
        if "from public.invitations" in sql and "status = 'pending'" in sql:
            if "select id," in sql:
                return FakeResult(None)
            return FakeResult(2)
        if "from public.workspace_subscriptions" in sql:
            return FakeResult("free")
        if "select name from public.workspaces" in sql:
            return FakeResult("Admin Workspace")
        return FakeResult()


class FakeEngine:
    def __init__(self, *, is_platform_admin: bool) -> None:
        self.connection = PlatformAdminConnection(is_platform_admin=is_platform_admin)

    @contextmanager
    def begin(self):
        yield self.connection


class RecordingMailer:
    def __init__(self) -> None:
        self.recipients: list[str] = []

    def send_invitation(self, *, email, **_kwargs) -> None:
        self.recipients.append(email)


def test_platform_admin_bypasses_workspace_invitation_and_seat_limits() -> None:
    engine = FakeEngine(is_platform_admin=True)
    mailer = RecordingMailer()
    application = DatabaseSliceOneApplication(
        engine=engine,  # type: ignore[arg-type]
        mailer=mailer,
        web_url="https://oslo.example",
    )

    invitation = application.invite_member(
        actor_user_id=ADMIN_ID,
        workspace_id=WORKSPACE_ID,
        email="another.owner@example.com",
    )

    assert invitation.status is InvitationStatus.PENDING
    assert mailer.recipients == ["another.owner@example.com"]
    assert not any(
        "from public.workspace_subscriptions" in statement
        for statement in engine.connection.statements
    )


def test_workspace_owner_remains_subject_to_plan_invitation_limits() -> None:
    engine = FakeEngine(is_platform_admin=False)
    application = DatabaseSliceOneApplication(
        engine=engine,  # type: ignore[arg-type]
        mailer=RecordingMailer(),
        web_url="https://oslo.example",
    )

    with pytest.raises(InvitationLimitReached):
        application.invite_member(
            actor_user_id=ADMIN_ID,
            workspace_id=WORKSPACE_ID,
            email="limited.owner@example.com",
        )

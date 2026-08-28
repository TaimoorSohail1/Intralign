"""Reset OSLO's local Playwright identities and workspace fixtures.

The guardrails deliberately refuse non-local Supabase instances. Product data,
non-E2E projects, analyses, and non-E2E identities are never removed.
"""

from __future__ import annotations

from pathlib import Path
from time import sleep
from urllib.parse import urlparse
from uuid import UUID

import psycopg
from seed_local import (
    WORKSPACE_ID,
    ensure_application_records,
    ensure_auth_user,
    local_status,
)

E2E_MEMBER_EMAIL = "e2e-existing@example.com"
E2E_MEMBER_PASSWORD = "ExistingMember123!"
E2E_OWNER_EMAIL = "e2e-owner@example.com"
E2E_OWNER_PASSWORD = "E2EOwner123!"
E2E_WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000020")
E2E_EMAIL_PATTERNS = (
    "slice-one-%@example.com",
    "existing-%@example.com",
    "invitation-actions-%@example.com",
)


def _require_local_status(status: dict[str, str]) -> None:
    for key in ("API_URL", "DB_URL"):
        host = (urlparse(status[key]).hostname or "").lower()
        if host not in {"127.0.0.1", "localhost"}:
            raise RuntimeError(f"Refusing to reset E2E fixtures on non-local {key}: {host}")


def _reset_invitation_fixtures_once(
    *,
    database_url: str,
    existing_user_id: UUID,
    owner_user_id: UUID,
) -> None:
    patterns = list(E2E_EMAIL_PATTERNS) + [E2E_MEMBER_EMAIL]
    with psycopg.connect(database_url) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            delete from public.memberships membership
            using public.invitations invitation
            where invitation.workspace_id = %s
              and membership.workspace_id = invitation.workspace_id
              and membership.user_id = invitation.accepted_by
              and invitation.email::text like any(%s)
            """,
            (WORKSPACE_ID, patterns),
        )
        cursor.execute(
            """
            delete from public.invitations
            where workspace_id = %s
              and email::text like any(%s)
            """,
            (WORKSPACE_ID, patterns),
        )
        cursor.execute(
            """
            delete from public.memberships
            where workspace_id = %s and user_id = %s
            """,
            (WORKSPACE_ID, existing_user_id),
        )
        cursor.execute(
            """
            insert into public.profiles (id, display_name)
            values (%s, 'E2E Workspace Owner')
            on conflict (id) do update set
              display_name = excluded.display_name,
              updated_at = now()
            """,
            (owner_user_id,),
        )
        cursor.execute(
            """
            insert into public.workspaces (id, name, created_by)
            values (%s, 'Intralign E2E', %s)
            on conflict (id) do update set
              name = excluded.name,
              updated_at = now()
            """,
            (E2E_WORKSPACE_ID, owner_user_id),
        )
        cursor.execute(
            """
            delete from public.projects
            where workspace_id = %s
            """,
            (E2E_WORKSPACE_ID,),
        )
        cursor.execute(
            """
            delete from public.memberships
            where user_id = %s
            """,
            (owner_user_id,),
        )
        cursor.execute(
            """
            insert into public.memberships (
              workspace_id, user_id, role, welcome_seen_at
            )
            values (%s, %s, 'owner', now())
            on conflict (workspace_id, user_id) do update set
              role = excluded.role,
              welcome_seen_at = excluded.welcome_seen_at
            """,
            (E2E_WORKSPACE_ID, owner_user_id),
        )
        cursor.execute(
            """
            insert into public.profiles (id, display_name)
            values (%s, 'Existing Member')
            on conflict (id) do update set
              display_name = excluded.display_name,
              updated_at = now()
            """,
            (existing_user_id,),
        )
        cursor.execute(
            """
            insert into public.workspace_subscriptions (
              workspace_id, plan_code, status, changed_by
            )
            select %s, 'basic', 'active', created_by
            from public.workspaces
            where id = %s
            on conflict (workspace_id) do update set
              plan_code = excluded.plan_code,
              status = excluded.status,
              changed_by = excluded.changed_by,
              updated_at = now()
            """,
            (E2E_WORKSPACE_ID, E2E_WORKSPACE_ID),
        )


def _reset_invitation_fixtures(
    *,
    database_url: str,
    existing_user_id: UUID,
    owner_user_id: UUID,
) -> None:
    """Reset E2E data after any in-flight worker transaction releases its locks.

    Playwright deliberately resets the same isolated workspace before every
    journey. A worker from the preceding journey can finish its final database
    write at the same instant as the cascading project delete. PostgreSQL
    resolves that race by aborting one complete transaction, so retrying the
    whole reset on a fresh connection is safe and keeps fixture setup atomic.
    """

    max_attempts = 4
    for attempt in range(max_attempts):
        try:
            _reset_invitation_fixtures_once(
                database_url=database_url,
                existing_user_id=existing_user_id,
                owner_user_id=owner_user_id,
            )
            return
        except psycopg.errors.DeadlockDetected:
            if attempt == max_attempts - 1:
                raise
            sleep(0.25 * (2**attempt))


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    status = local_status(repository_root)
    _require_local_status(status)
    admin_user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email="admin@oslo.local",
        password="OsloLocalAdmin123!",
    )
    # E2E runs can follow integration tests that temporarily make the platform
    # administrator a workspace Owner. Restore the production-shaped admin
    # boundary before every browser journey so invitations provision an
    # isolated client workspace instead of exposing the admin workspace.
    ensure_application_records(
        database_url=status["DB_URL"],
        user_id=admin_user_id,
    )
    existing_user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email=E2E_MEMBER_EMAIL,
        password=E2E_MEMBER_PASSWORD,
    )
    owner_user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email=E2E_OWNER_EMAIL,
        password=E2E_OWNER_PASSWORD,
    )
    _reset_invitation_fixtures(
        database_url=status["DB_URL"],
        existing_user_id=existing_user_id,
        owner_user_id=owner_user_id,
    )
    print("Reset local Playwright identities and workspace fixtures.")


if __name__ == "__main__":
    main()

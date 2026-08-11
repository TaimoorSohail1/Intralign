"""Reset OSLO's local Playwright identities and workspace fixtures.

The guardrails deliberately refuse non-local Supabase instances. Product data,
non-E2E projects, analyses, and non-E2E identities are never removed.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
from uuid import UUID

import psycopg
from seed_local import (
    WORKSPACE_ID,
    ensure_auth_user,
    local_status,
)

E2E_MEMBER_EMAIL = "e2e-existing@example.com"
E2E_MEMBER_PASSWORD = "ExistingMember123!"
E2E_OWNER_EMAIL = "e2e-owner@example.com"
E2E_OWNER_PASSWORD = "E2EOwner123!"
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


def _reset_invitation_fixtures(
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
            delete from public.projects
            where workspace_id = %s and created_by = %s
            """,
            (WORKSPACE_ID, owner_user_id),
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
            insert into public.memberships (
              workspace_id, user_id, role, welcome_seen_at
            )
            values (%s, %s, 'owner', now())
            on conflict (workspace_id, user_id) do update set
              role = excluded.role,
              welcome_seen_at = excluded.welcome_seen_at
            """,
            (WORKSPACE_ID, owner_user_id),
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
            (WORKSPACE_ID, WORKSPACE_ID),
        )


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    status = local_status(repository_root)
    _require_local_status(status)
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

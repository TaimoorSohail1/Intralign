"""Idempotently seed the local OSLO owner through Supabase Auth."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from uuid import UUID

import httpx
import psycopg

WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
WORKSPACE_NAME = "OSLO Product Grill"


def supabase_executable(repository_root: Path, *, platform_name: str | None = None) -> Path:
    """Return the platform-specific Supabase CLI shim installed by pnpm."""
    platform_name = platform_name or os.name
    executable_name = "supabase.cmd" if platform_name == "nt" else "supabase"
    return repository_root / "node_modules" / ".bin" / executable_name


def local_status(repository_root: Path) -> dict[str, str]:
    executable = supabase_executable(repository_root)
    result = subprocess.run(  # noqa: S603
        [str(executable), "status", "-o", "json"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def ensure_auth_user(
    *,
    api_url: str,
    secret_key: str,
    email: str,
    password: str,
) -> UUID:
    headers = {"apikey": secret_key, "Authorization": f"Bearer {secret_key}"}
    with httpx.Client(base_url=api_url, headers=headers, timeout=20) as client:
        users_response = client.get("/auth/v1/admin/users", params={"page": 1, "per_page": 1000})
        users_response.raise_for_status()
        existing = next(
            (user for user in users_response.json()["users"] if user["email"] == email),
            None,
        )
        if existing:
            return UUID(existing["id"])

        create_response = client.post(
            "/auth/v1/admin/users",
            json={
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {"display_name": "OSLO Admin"},
            },
        )
        create_response.raise_for_status()
        return UUID(create_response.json()["id"])


def ensure_application_records(*, database_url: str, user_id: UUID) -> None:
    with psycopg.connect(database_url) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            insert into public.profiles (id, display_name)
            values (%s, 'OSLO Admin')
            on conflict (id) do update set
              display_name = excluded.display_name,
              updated_at = now()
            """,
            (user_id,),
        )
        cursor.execute(
            """
            insert into public.workspaces (id, name, created_by)
            values (%s, %s, %s)
            on conflict (id) do update set
              name = excluded.name,
              updated_at = now()
            """,
            (WORKSPACE_ID, WORKSPACE_NAME, user_id),
        )
        cursor.execute(
            """
            insert into public.memberships (workspace_id, user_id, role, welcome_seen_at)
            values (%s, %s, 'owner', now())
            on conflict (workspace_id, user_id) do update set role = 'owner'
            """,
            (WORKSPACE_ID, user_id),
        )
        cursor.execute(
            """
            insert into public.workspace_subscriptions (
              workspace_id, plan_code, status, changed_by
            )
            values (%s, 'basic', 'active', %s)
            on conflict (workspace_id) do update set
              plan_code = excluded.plan_code,
              status = excluded.status,
              changed_by = excluded.changed_by,
              updated_at = now()
            """,
            (WORKSPACE_ID, user_id),
        )


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    status = local_status(repository_root)
    email = os.getenv("OSLO_LOCAL_ADMIN_EMAIL", "admin@oslo.local").strip().lower()
    password = os.getenv("OSLO_LOCAL_ADMIN_PASSWORD", "OsloLocalAdmin123!")
    user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email=email,
        password=password,
    )
    ensure_application_records(database_url=status["DB_URL"], user_id=user_id)
    print(f"Seeded local owner {email} in workspace {WORKSPACE_ID}.")


if __name__ == "__main__":
    main()

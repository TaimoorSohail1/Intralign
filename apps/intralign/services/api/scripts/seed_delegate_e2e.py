"""Create an isolated local Delegate-PM browser fixture."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import psycopg
from seed_e2e import E2E_OWNER_EMAIL, E2E_OWNER_PASSWORD, E2E_WORKSPACE_ID
from seed_local import ensure_auth_user, local_status

DELEGATE_EMAIL = "e2e-delegate@example.com"
DELEGATE_PASSWORD = "E2EDelegate123!"
ASSIGNED_PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000021")
UNASSIGNED_PROJECT_ID = UUID("018f9f7e-8de2-7000-8000-000000000022")


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    status = local_status(repository_root)
    owner_user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email=E2E_OWNER_EMAIL,
        password=E2E_OWNER_PASSWORD,
    )
    delegate_user_id = ensure_auth_user(
        api_url=status["API_URL"],
        secret_key=status["SECRET_KEY"],
        email=DELEGATE_EMAIL,
        password=DELEGATE_PASSWORD,
    )

    with psycopg.connect(status["DB_URL"]) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            insert into public.profiles (id, display_name)
            values (%s, 'E2E Delegate PM')
            on conflict (id) do update set
              display_name = excluded.display_name,
              updated_at = now()
            """,
            (delegate_user_id,),
        )
        cursor.execute(
            "delete from public.projects where workspace_id = %s",
            (E2E_WORKSPACE_ID,),
        )
        cursor.executemany(
            """
            insert into public.projects (id, workspace_id, name, created_by)
            values (%s, %s, %s, %s)
            """,
            [
                (
                    ASSIGNED_PROJECT_ID,
                    E2E_WORKSPACE_ID,
                    "Delegate assignment",
                    owner_user_id,
                ),
                (
                    UNASSIGNED_PROJECT_ID,
                    E2E_WORKSPACE_ID,
                    "Owner-only project",
                    owner_user_id,
                ),
            ],
        )
        cursor.execute(
            """
            insert into public.project_memberships (
              workspace_id, project_id, user_id, role, assigned_by,
              orientation_seen_at
            )
            values (%s, %s, %s, 'delegate_pm', %s, now())
            """,
            (
                E2E_WORKSPACE_ID,
                ASSIGNED_PROJECT_ID,
                delegate_user_id,
                owner_user_id,
            ),
        )
    print("Seeded isolated Delegate-PM browser fixture.")


if __name__ == "__main__":
    main()

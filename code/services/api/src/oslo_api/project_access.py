"""Project-scoped authorization shared by the R2 application services."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection


@dataclass(frozen=True)
class ProjectAccess:
    workspace_id: UUID
    role: str

    @property
    def can_edit(self) -> bool:
        return self.role in {"owner", "delegate_pm"}

    @property
    def is_owner(self) -> bool:
        return self.role == "owner"


def find_project_access(
    connection: Connection,
    *,
    actor_user_id: UUID,
    project_id: UUID,
) -> ProjectAccess | None:
    """Resolve owner or assigned Delegate-PM access for exactly one project."""

    row = (
        connection.execute(
            text(
                """
                select project.workspace_id,
                       case
                         when owner.user_id is not null then 'owner'
                         when delegate.user_id is not null then 'delegate_pm'
                       end as role
                from public.projects project
                left join public.memberships owner
                  on owner.workspace_id = project.workspace_id
                 and owner.user_id = :user_id
                 and owner.role = 'owner'
                left join public.project_memberships delegate
                  on delegate.project_id = project.id
                 and delegate.user_id = :user_id
                 and delegate.role = 'delegate_pm'
                where project.id = :project_id
                  and (owner.user_id is not null or delegate.user_id is not null)
                """
            ),
            {"project_id": project_id, "user_id": actor_user_id},
        )
        .mappings()
        .one_or_none()
    )
    if row is None:
        return None
    return ProjectAccess(workspace_id=row["workspace_id"], role=row["role"])

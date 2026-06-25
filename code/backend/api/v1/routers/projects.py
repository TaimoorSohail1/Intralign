"""Projects read router (DTM-0018) — GET list/detail (read-mostly; ADR-0003).

Presents Project rows as Data Model v1.2 ``Project`` DTOs, workspace-scoped to
the caller (§12). Consumed by the Dashboard + Project Workspace
(UI_SCREEN_INVENTORY). GET ONLY — create/update/archive stay on the existing
command seam.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, project_to_dto
from shared.entities import Project

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=list[Project])
def list_projects(
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Project]:
    """List the caller's workspace projects (workspace-scoped from the Principal)."""
    return [project_to_dto(row) for row in reader.list_projects(principal.workspace_id)]


@router.get("/projects/{project_id}", response_model=Project)
def get_project(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> Project:
    """Get one project (404 if absent or outside the caller's workspace, §12)."""
    row = reader.get_project(project_id)
    if row is None or str(row.get("workspace_id")) != principal.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "project not found"}},
        )
    return project_to_dto(row)

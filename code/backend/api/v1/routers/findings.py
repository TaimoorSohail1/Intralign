"""Findings read router (DTM-0018) — GET list/detail (read-mostly; ADR-0003).

Presents the Derived Finding projections (``derived.finding_current``) as Data
Model v1.2 ``Finding`` DTOs, each carrying its epistemic label (Derived + band +
conflict). Consumed by the Findings Workspace / 60-Second Orientation surfaces
(UI_SCREEN_INVENTORY). GET ONLY — the finding lifecycle commands
(:acknowledge/:address/:close/:reopen) stay on the existing Wave seams; the read
surface mutates nothing.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, finding_to_dto
from shared.entities import Finding

router = APIRouter(tags=["findings"])


@router.get("/projects/{project_id}/findings", response_model=list[Finding])
def list_findings(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Finding]:
    """List the project's current Findings (Derived projections) with labels."""
    rows = reader.list_projection(project_id, "finding")
    return [finding_to_dto(row) for row in rows]


@router.get("/findings/{finding_id}", response_model=Finding)
def get_finding(
    finding_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> Finding:
    """Get one Finding by its projection id (404 if outside the caller's scope)."""
    row = reader.get_projection("finding", finding_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "finding not found"}},
        )
    return finding_to_dto(row)

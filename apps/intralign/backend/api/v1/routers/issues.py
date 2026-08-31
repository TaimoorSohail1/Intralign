"""Issues read router (DTM-0038) — GET list/detail (read-mostly; ADR-0003).

Presents the Derived Issue projections (``derived.issue_current``, populated by
the DTM-0030 materializer from the ``issue`` CHRs) as Data Model ``Issue`` DTOs —
the first-class, prioritized Finding (``Issue ──from──> Finding``, severity an
attribute; Object Model §8). Each carries its epistemic label (Derived + band +
conflict) and the source-Finding lineage (``finding_id``). Mirrors the Findings
read router. GET ONLY — Issue formation stays on the Evaluate seam; the read
surface mutates nothing.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, issue_to_dto
from shared.entities import Issue

router = APIRouter(tags=["issues"])


@router.get("/projects/{project_id}/issues", response_model=list[Issue])
def list_issues(
    project_id: str,
    finding_id: str | None = None,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Issue]:
    """List the project's current Issues (Derived projections), with labels + lineage.

    Optionally filtered to the Issues formed from one source Finding (``finding_id``).
    """
    rows = reader.list_projection(project_id, "issue")
    dtos = [issue_to_dto(row) for row in rows]
    if finding_id is not None:
        dtos = [d for d in dtos if d.finding_id == finding_id]
    return dtos


@router.get("/issues/{issue_id}", response_model=Issue)
def get_issue(
    issue_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> Issue:
    """Get one Issue by its projection id (404 if outside the caller's scope)."""
    row = reader.get_projection("issue", issue_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "issue not found"}},
        )
    return issue_to_dto(row)

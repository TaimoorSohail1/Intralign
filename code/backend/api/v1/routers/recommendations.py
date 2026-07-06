"""Recommendations read router (DTM-0018) — GET list/detail (read-mostly; ADR-0003).

Presents the Derived Recommendation projections (``derived.recommendation_current``)
as Data Model v1.2 ``Recommendation`` DTOs (RS-R3 + RS-R7 card fields), each
carrying its epistemic label. Consumed by the Recommendation Workspace
(UI_SCREEN_INVENTORY). Both the project-scoped list and the per-Finding list (the
RP-C1 Finding-context list) are exposed. GET ONLY — accept/reject/defer/implement
stay on the existing Wave U capture seam (decision #3/#4); the read surface never
mutates a recommendation.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, recommendation_to_dto
from shared.entities import Recommendation

router = APIRouter(tags=["recommendations"])


@router.get("/projects/{project_id}/recommendations", response_model=list[Recommendation])
def list_recommendations(
    project_id: str,
    finding_id: str | None = None,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Recommendation]:
    """List the project's current Recommendations (optionally filtered by finding_id)."""
    rows = reader.list_projection(project_id, "recommendation")
    dtos = [recommendation_to_dto(row) for row in rows]
    if finding_id is not None:
        dtos = [d for d in dtos if d.finding_id == finding_id]
    return dtos


@router.get("/findings/{finding_id}/recommendations", response_model=list[Recommendation])
def list_recommendations_for_finding(
    finding_id: str,
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Recommendation]:
    """List the Recommendations anchored to a Finding (RP-C1 Finding-context list).

    ``project_id`` scopes the read; the result is filtered to those anchored to
    the given Finding (one Recommendation → one Finding; a Finding → many).
    """
    rows = reader.list_projection(project_id, "recommendation")
    return [
        d for d in (recommendation_to_dto(row) for row in rows) if d.finding_id == finding_id
    ]


@router.get("/recommendations/{recommendation_id}", response_model=Recommendation)
def get_recommendation(
    recommendation_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> Recommendation:
    """Get one Recommendation by its projection id (404 if outside scope)."""
    row = reader.get_projection("recommendation", recommendation_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "recommendation not found"}},
        )
    return recommendation_to_dto(row)

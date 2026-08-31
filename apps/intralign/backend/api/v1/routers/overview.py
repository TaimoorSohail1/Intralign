"""Overview read router (DTM-0038) — GET counts + aggregates (read-mostly; ADR-0003).

Presents, for one project, a PRESENTATION of the governed objects: the counts of
the governed lists (Findings / Issues / Recommendations) plus the aggregate
Outcome-Confidence band + CAF (each Derived-labelled). Consumed by the Overview
View (UI_SCREEN_INVENTORY).

CRITICAL (Wave E not-project-health rule): the Overview is COUNTS + labelled
aggregates — never a health / readiness / probability / score. It computes
nothing new: every number is a count of, or a pass-through band from, an already
-governed object. GET ONLY — the read surface mutates nothing.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, overview_to_dto
from shared.entities import Overview

router = APIRouter(tags=["overview"])


@router.get("/projects/{project_id}/overview", response_model=Overview)
def get_overview(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> Overview:
    """Project Overview: counts of the governed lists + the Derived aggregates.

    Aggregates the existing governed projections (no new compute): the counts come
    from the governed lists; the Outcome-Confidence + CAF are mapped through their
    existing Derived mappers (the band travels). NOT a project-health number.
    """
    return overview_to_dto(
        project_id,
        finding_rows=reader.list_projection(project_id, "finding"),
        issue_rows=reader.list_projection(project_id, "issue"),
        recommendation_rows=reader.list_projection(project_id, "recommendation"),
        outcome_confidence_rows=reader.list_projection(project_id, "outcome_confidence"),
        caf_rows=reader.list_projection(project_id, "caf"),
    )

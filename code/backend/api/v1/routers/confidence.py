"""Confidence read router (DTM-0018) — GET current confidence + CAF (read-mostly).

Presents the Derived OutcomeConfidence + CAF projections (``derived.
outcome_confidence_current`` / ``derived.caf_current``) as Data Model v1.2
``ConfidenceState`` / ``CAFState`` DTOs, each carrying its epistemic label. The
band is the user-facing value (never a bare number / project health). Consumed by
the Dashboard + Confidence Experience + 60-Second Orientation (UI_SCREEN_INVENTORY).
GET ONLY — Disclose never recomputes confidence.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, caf_to_dto, confidence_to_dto
from shared.entities import CAFState, ConfidenceState

router = APIRouter(tags=["confidence"])


@router.get("/projects/{project_id}/confidence", response_model=ConfidenceState | None)
def get_confidence(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> ConfidenceState | None:
    """Current Outcome Confidence for the project (Derived; band + reliability)."""
    rows = reader.list_projection(project_id, "outcome_confidence")
    if not rows:
        return None
    return confidence_to_dto(rows[0])


@router.get("/projects/{project_id}/caf", response_model=CAFState | None)
def get_caf(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> CAFState | None:
    """Current CAF assessment for the project (three co-equal dimensions)."""
    rows = reader.list_projection(project_id, "caf")
    if not rows:
        return None
    return caf_to_dto(rows[0])

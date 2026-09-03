"""Acceptance read router (DTM-0018) — GET UARs + plan facts + acceptance-impact.

Presents the Wave U canonical receipts and the Derived acceptance-impact:
- ``UserAcceptanceRecord`` + ``PlanFact`` — user-attested (attested-user); the
  read surface presents them, it NEVER records an acceptance (acceptance stays on
  the existing Wave U capture seam — decision #3).
- ``AcceptanceImpactAssessment`` — Derived ("a decision you confirmed is
  affected"), carrying its epistemic label.
Consumed by the History/Timeline + Notification/Awareness surfaces. GET ONLY.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import (
    ProjectionReader,
    acceptance_impact_to_dto,
    plan_fact_to_dto,
    uar_to_dto,
)
from shared.entities import (
    AcceptanceImpactAssessment,
    PlanFact,
    UserAcceptanceRecord,
)

router = APIRouter(tags=["acceptance"])


@router.get("/projects/{project_id}/acceptance", response_model=list[UserAcceptanceRecord])
def list_acceptances(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[UserAcceptanceRecord]:
    """List the project's User Acceptance Records (user-attested; newest first)."""
    return [uar_to_dto(row) for row in reader.list_acceptances(project_id)]


@router.get("/projects/{project_id}/plan-facts", response_model=list[PlanFact])
def list_plan_facts(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[PlanFact]:
    """List the project's user-attested Plan Facts (confirmed-content; not truth)."""
    return [plan_fact_to_dto(row) for row in reader.list_plan_facts(project_id)]


@router.get(
    "/projects/{project_id}/acceptance-impact",
    response_model=list[AcceptanceImpactAssessment],
)
def list_acceptance_impact(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[AcceptanceImpactAssessment]:
    """List the project's Acceptance-Impact assessments (Derived drift; labeled)."""
    rows = reader.list_projection(project_id, "acceptance_impact")
    return [acceptance_impact_to_dto(row) for row in rows]

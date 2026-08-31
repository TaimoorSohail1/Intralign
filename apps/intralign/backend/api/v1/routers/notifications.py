"""Notifications read router (DTM-0018) — GET list (read-mostly; ADR-0003).

Presents Notification rows as Data Model v1.2 ``Notification`` DTOs,
workspace-scoped to the caller. Awareness only — a notification never drives
analysis (§13). Consumed by the Dashboard + Notification Center
(UI_SCREEN_INVENTORY). GET ONLY — :view/:dismiss are awareness state commands on
the existing platform seam, NOT part of this read surface.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, notification_to_dto
from shared.entities import Notification

router = APIRouter(tags=["notifications"])


@router.get("/notifications", response_model=list[Notification])
def list_notifications(
    project_id: str | None = None,
    state: str | None = None,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[Notification]:
    """List the caller's workspace notifications (filter by project_id / state)."""
    dtos = [notification_to_dto(row) for row in reader.list_notifications(principal.workspace_id)]
    if project_id is not None:
        dtos = [n for n in dtos if n.project_id == project_id]
    if state is not None:
        dtos = [n for n in dtos if n.state.value == state]
    return dtos

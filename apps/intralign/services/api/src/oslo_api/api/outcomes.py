from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from oslo_api.api.billing import slice_four_application
from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.entitlements.service import (
    OutcomeCapacityReached,
    OutcomeNotFound,
    OutcomePermissionDenied,
)
from oslo_api.slice_four import (
    OutcomeProvenance,
    OutcomeStatus,
    ProjectOutcome,
    SliceFourApplication,
)
from oslo_api.tiering.policy import get_plan_policy

router = APIRouter(prefix="/v1", tags=["outcomes"])


class CreateOutcomeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=240)
    provenance: OutcomeProvenance


class OutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    project_id: UUID
    title: str
    status: OutcomeStatus
    is_primary: bool
    provenance: OutcomeProvenance
    created_at: datetime
    archived_at: datetime | None


def _capacity_gate_detail(workspace_id: UUID, limit: int) -> dict[str, object]:
    basic = get_plan_policy("basic")
    return {
        "code": "CAPACITY_COMMITMENT_REQUIRED",
        "wall_key": "multiOutcome",
        "capability": "Optimize all your outcomes",
        "tier": "basic",
        "tier_label": "Basic",
        "price_usd_monthly": basic.price_usd_monthly,
        "price_usd_annual": basic.price_usd_annual,
        "limit": limit,
        "free_path": "archive_outcome",
        "checkout_path": f"/v1/workspaces/{workspace_id}/billing/checkout-sessions",
    }


@router.post(
    "/workspaces/{workspace_id}/projects/{project_id}/outcomes",
    response_model=OutcomeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_outcome(
    workspace_id: UUID,
    project_id: UUID,
    payload: CreateOutcomeRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> ProjectOutcome:
    try:
        return application.create_outcome(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            project_id=project_id,
            title=payload.title.strip(),
            provenance=payload.provenance,
        )
    except OutcomePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except OutcomeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except OutcomeCapacityReached as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=_capacity_gate_detail(workspace_id, error.active_outcome_limit),
        ) from error


@router.get(
    "/workspaces/{workspace_id}/projects/{project_id}/outcomes",
    response_model=list[OutcomeResponse],
)
def list_outcomes(
    workspace_id: UUID,
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> list[ProjectOutcome]:
    try:
        return application.list_outcomes(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            project_id=project_id,
        )
    except OutcomePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error


def _change_outcome_status(
    *,
    action: str,
    workspace_id: UUID,
    outcome_id: UUID,
    context: InvitationRequestContext,
    application: SliceFourApplication,
) -> ProjectOutcome:
    try:
        operation = (
            application.archive_outcome
            if action == "archive"
            else application.reactivate_outcome
        )
        return operation(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            outcome_id=outcome_id,
        )
    except OutcomePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except OutcomeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except OutcomeCapacityReached as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=_capacity_gate_detail(workspace_id, error.active_outcome_limit),
        ) from error


@router.post(
    "/workspaces/{workspace_id}/outcomes/{outcome_id}:archive",
    response_model=OutcomeResponse,
)
def archive_outcome(
    workspace_id: UUID,
    outcome_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> ProjectOutcome:
    return _change_outcome_status(
        action="archive",
        workspace_id=workspace_id,
        outcome_id=outcome_id,
        context=context,
        application=application,
    )


@router.post(
    "/workspaces/{workspace_id}/outcomes/{outcome_id}:reactivate",
    response_model=OutcomeResponse,
)
def reactivate_outcome(
    workspace_id: UUID,
    outcome_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> ProjectOutcome:
    return _change_outcome_status(
        action="reactivate",
        workspace_id=workspace_id,
        outcome_id=outcome_id,
        context=context,
        application=application,
    )

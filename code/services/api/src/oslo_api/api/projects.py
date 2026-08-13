from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.application import ActiveProjectLimitReached, ProjectArchiveDenied
from oslo_api.invitations import InvitePermissionDenied
from oslo_api.tiering.policy import get_plan_policy

router = APIRouter(prefix="/v1", tags=["projects"])


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    name: str
    status: str


class WorkspaceProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    status: str
    archived: bool
    updated_at: datetime
    analysis_status: str
    confidence_index: int | None
    confidence_band: str | None
    reliability: str | None
    open_issues: int
    artifact_count: int
    weakest_pillar: str | None = None


class WorkspaceNotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    key: str
    project_id: UUID
    project_name: str
    kind: str
    status: str
    title: str
    created_at: datetime
    read: bool


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    role: str
    plan: str
    plan_label: str
    price_usd_monthly: int
    document_limit: int
    word_limit: int
    collaborator_seat_limit: int | None
    monthly_analysis_limit: int | None
    monthly_analyses_used: int
    can_manage_plan: bool
    member_count: int
    collaborator_seats_used: int
    active_project_limit: int
    can_create_project: bool
    projects: list[WorkspaceProjectResponse]
    notifications: list[WorkspaceNotificationResponse]


class WorkspacePreferencesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    theme: str
    analysis_notifications: bool
    failure_notifications: bool
    stale_notifications: bool
    display_name: str = ""
    role_title: str = ""
    workspace_name: str = ""
    actor_role: str = "owner"
    mentions_notifications: bool = True
    reply_notifications: bool = True
    shared_notifications: bool = True


class WorkspacePreferencesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theme: str
    analysis_notifications: bool
    failure_notifications: bool
    stale_notifications: bool
    display_name: str = ""
    role_title: str = ""
    workspace_name: str = ""
    mentions_notifications: bool = True
    reply_notifications: bool = True
    shared_notifications: bool = True


class WorkspacePlanRequest(BaseModel):
    plan: str


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_first_project(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> ProjectResponse:
    try:
        project = context.application.start_first_project(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except ActiveProjectLimitReached as error:
        basic = get_plan_policy("basic")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "code": "CAPACITY_COMMITMENT_REQUIRED",
                "wall_key": "multiPlan",
                "capability": "Create and optimize multiple plans",
                "tier": "basic",
                "tier_label": "Basic",
                "price_usd_monthly": basic.price_usd_monthly,
                "price_usd_annual": basic.price_usd_annual,
                "limit": error.active_project_limit,
                "free_path": "archive_plan",
                "checkout_path": (
                    f"/v1/workspaces/{workspace_id}/billing/checkout-sessions"
                ),
            },
        ) from error
    return ProjectResponse.model_validate(project)


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> WorkspaceResponse:
    try:
        summary = context.application.get_workspace_summary(
            actor_user_id=context.user.id, workspace_id=workspace_id
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    return WorkspaceResponse.model_validate(summary)


@router.put("/workspaces/{workspace_id}/plan", response_model=WorkspaceResponse)
def update_workspace_plan(
    workspace_id: UUID,
    payload: WorkspacePlanRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> WorkspaceResponse:
    if payload.plan not in {"free", "basic"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_PLAN", "supported": ["free", "basic"]},
        )
    if payload.plan == "basic":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "CHECKOUT_REQUIRED",
                "checkout_path": (
                    f"/v1/workspaces/{workspace_id}/billing/checkout-sessions"
                ),
            },
        )
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "code": "BILLING_PORTAL_REQUIRED",
            "portal_path": f"/v1/workspaces/{workspace_id}/billing/portal-sessions",
        },
    )


@router.post(
    "/workspaces/{workspace_id}/projects/{project_id}/archive",
    status_code=status.HTTP_204_NO_CONTENT,
)
def archive_project(
    workspace_id: UUID,
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> None:
    try:
        context.application.archive_project(
            actor_user_id=context.user.id, workspace_id=workspace_id, project_id=project_id
        )
    except ProjectArchiveDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error


@router.post(
    "/workspaces/{workspace_id}/projects/{project_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
)
def restore_project(
    workspace_id: UUID,
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> None:
    try:
        context.application.restore_project(
            actor_user_id=context.user.id, workspace_id=workspace_id, project_id=project_id
        )
    except ProjectArchiveDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error


class NotificationReadRequest(BaseModel):
    keys: list[str]


@router.post(
    "/workspaces/{workspace_id}/notifications/read",
    status_code=status.HTTP_204_NO_CONTENT,
)
def mark_notifications_read(
    workspace_id: UUID,
    payload: NotificationReadRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> None:
    try:
        context.application.mark_workspace_notifications_read(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            keys=payload.keys,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error


@router.get(
    "/workspaces/{workspace_id}/preferences",
    response_model=WorkspacePreferencesResponse,
)
def get_preferences(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> WorkspacePreferencesResponse:
    try:
        result = context.application.get_workspace_preferences(
            actor_user_id=context.user.id, workspace_id=workspace_id
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    return WorkspacePreferencesResponse.model_validate(result)


@router.put(
    "/workspaces/{workspace_id}/preferences",
    response_model=WorkspacePreferencesResponse,
)
def update_preferences(
    workspace_id: UUID,
    payload: WorkspacePreferencesRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> WorkspacePreferencesResponse:
    try:
        result = context.application.update_workspace_preferences(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            **payload.model_dump(),
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_SETTINGS", "message": str(error)},
        ) from error
    return WorkspacePreferencesResponse.model_validate(result)

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.invitations import InvitePermissionDenied

router = APIRouter(prefix="/v1", tags=["projects"])


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    name: str
    status: str


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
    return ProjectResponse.model_validate(project)

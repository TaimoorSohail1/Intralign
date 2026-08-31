from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.feedback import (
    FeedbackApplication,
    FeedbackCategory,
    FeedbackContext,
    FeedbackImpact,
    FeedbackTicket,
)
from oslo_api.invitations import InvitePermissionDenied

router = APIRouter(prefix="/v1", tags=["feedback"])


class FeedbackContextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    where: str = Field(min_length=1, max_length=80)
    view: str = Field(min_length=1, max_length=40)
    role: str = Field(min_length=1, max_length=40)
    grounded_x: int = Field(ge=0)
    total_y: int = Field(ge=0)
    first_run_flag: bool
    ts: str = Field(min_length=1, max_length=64)


class FeedbackTicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(pattern=r"^[A-Za-z0-9_-]{8,128}$")
    category: FeedbackCategory
    body: str = Field(min_length=1, max_length=4000)
    expected: str | None = Field(default=None, max_length=4000)
    impact: FeedbackImpact | None = None
    context: FeedbackContextRequest


class FeedbackTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    title: str
    status: str
    created_at: datetime


def feedback_application(request: Request) -> FeedbackApplication:
    application: FeedbackApplication | None = request.app.state.feedback
    if application is None:
        from oslo_api.bootstrap import build_feedback_application

        application = build_feedback_application()
        request.app.state.feedback = application
    return application


def _authorize_workspace(
    context: InvitationRequestContext,
    workspace_id: UUID,
) -> None:
    try:
        session = context.application.get_session_context(actor_user_id=context.user.id)
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    if session.workspace_id != workspace_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    "/workspaces/{workspace_id}/feedback/tickets",
    response_model=FeedbackTicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def file_feedback_ticket(
    workspace_id: UUID,
    payload: FeedbackTicketRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[FeedbackApplication, Depends(feedback_application)],
) -> FeedbackTicket:
    _authorize_workspace(context, workspace_id)
    return application.file_ticket(
        actor_user_id=context.user.id,
        workspace_id=workspace_id,
        session_id=payload.session_id,
        category=payload.category,
        body=payload.body,
        expected=(payload.expected if payload.category is FeedbackCategory.DEFECT else None),
        impact=(payload.impact if payload.category is FeedbackCategory.DEFECT else None),
        context=FeedbackContext(**payload.context.model_dump()),
    )


@router.get(
    "/workspaces/{workspace_id}/feedback/tickets",
    response_model=list[FeedbackTicketResponse],
)
def list_feedback_tickets(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[FeedbackApplication, Depends(feedback_application)],
    session_id: Annotated[str, Query(pattern=r"^[A-Za-z0-9_-]{8,128}$")],
) -> list[FeedbackTicket]:
    _authorize_workspace(context, workspace_id)
    return application.list_session_tickets(
        actor_user_id=context.user.id,
        workspace_id=workspace_id,
        session_id=session_id,
    )

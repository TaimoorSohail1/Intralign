from dataclasses import dataclass
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from oslo_api.api.authentication import require_access_token
from oslo_api.application import (
    AccountAlreadyExists,
    CollaboratorSeatLimitReached,
    InvalidInvitation,
    InvitationDeliveryFailed,
    InvitationEmailMismatch,
    InvitationLimitReached,
)
from oslo_api.identity import InvalidCredentials, InvalidSession
from oslo_api.invitations import InvitationStatus, InvitePermissionDenied, MembershipRole
from oslo_api.slice_one import (
    ActivationResult,
    AuthenticatedUser,
    InvitationDetails,
    SliceOneApplication,
)

router = APIRouter(prefix="/v1", tags=["invitations"])


class InviteMemberRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr


class InvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    role: MembershipRole
    status: InvitationStatus
    expires_at: datetime


class ActivateInvitationRequest(BaseModel):
    token: str = Field(min_length=1, max_length=256)
    display_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=12, max_length=128)


class ActivationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    email: EmailStr
    workspace_id: UUID
    access_token: str
    refresh_token: str
    expires_in: int
    welcome_required: bool


class ResolveInvitationRequest(BaseModel):
    token: str = Field(min_length=1, max_length=256)


class InvitationDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    workspace_name: str
    role: MembershipRole
    expires_at: datetime
    account_exists: bool


class AcceptExistingInvitationRequest(BaseModel):
    token: str = Field(min_length=1, max_length=256)
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


@dataclass(frozen=True, slots=True)
class InvitationRequestContext:
    application: SliceOneApplication
    user: AuthenticatedUser


def slice_one_application(request: Request) -> SliceOneApplication:
    application: SliceOneApplication | None = request.app.state.slice_one
    if application is None:
        from oslo_api.bootstrap import build_slice_one_application

        application = build_slice_one_application()
        request.app.state.slice_one = application
    return application


def invitation_request_context(
    request: Request,
    access_token: Annotated[str, Depends(require_access_token)],
) -> InvitationRequestContext:
    application = slice_one_application(request)
    try:
        user = application.authenticate(access_token)
    except InvalidSession as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        ) from error
    return InvitationRequestContext(application=application, user=user)


@router.post(
    "/workspaces/{workspace_id}/invitations",
    status_code=status.HTTP_201_CREATED,
    response_model=InvitationResponse,
)
def invite_member(
    workspace_id: UUID,
    payload: InviteMemberRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> InvitationResponse:
    try:
        invitation = context.application.invite_member(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            email=payload.email,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace Owners can manage invitations",
        ) from error
    except InvitationLimitReached as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "INVITATION_LIMIT_REACHED",
                "message": (
                    f"The {error.plan_label} plan includes "
                    f"{error.monthly_invitation_limit} invitations per calendar month. "
                    "Wait for the next allocation or compare plans."
                ),
                "plan": error.plan,
                "monthly_invitation_limit": error.monthly_invitation_limit,
                "remedies": list(error.remedies),
            },
        ) from error
    except CollaboratorSeatLimitReached as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "COLLABORATOR_SEAT_LIMIT_REACHED",
                "message": (
                    f"The {error.plan.title()} plan includes "
                    f"{error.collaborator_seat_limit} workspace owner seats. "
                    "Upgrade the workspace before inviting another owner."
                ),
                "plan": error.plan,
                "collaborator_seat_limit": error.collaborator_seat_limit,
                "remedies": list(error.remedies),
            },
        ) from error
    except InvitationDeliveryFailed as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "INVITATION_DELIVERY_FAILED",
                "message": (
                    "Invitation was saved but email delivery failed. "
                    "Retry from Invitations."
                ),
                "invitation_id": str(error.invitation_id),
            },
        ) from error
    return InvitationResponse.model_validate(invitation)


@router.get(
    "/workspaces/{workspace_id}/invitations",
    response_model=list[InvitationResponse],
)
def list_invitations(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> list[InvitationResponse]:
    try:
        invitations = context.application.list_invitations(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace Owners can manage invitations",
        ) from error
    return [InvitationResponse.model_validate(invitation) for invitation in invitations]


@router.post(
    "/workspaces/{workspace_id}/invitations/{invitation_id}/resend",
    response_model=InvitationResponse,
)
def resend_invitation(
    workspace_id: UUID,
    invitation_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> InvitationResponse:
    try:
        invitation = context.application.resend_invitation(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            invitation_id=invitation_id,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except InvalidInvitation as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from error
    except InvitationDeliveryFailed as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "INVITATION_DELIVERY_FAILED",
                "message": (
                    "Invitation was saved but email delivery failed. "
                    "Retry from Invitations."
                ),
                "invitation_id": str(error.invitation_id),
            },
        ) from error
    return InvitationResponse.model_validate(invitation)


@router.delete(
    "/workspaces/{workspace_id}/invitations/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def revoke_invitation(
    workspace_id: UUID,
    invitation_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
) -> None:
    try:
        context.application.revoke_invitation(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            invitation_id=invitation_id,
        )
    except InvitePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except InvalidInvitation as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from error


@router.post("/invitations/activate", response_model=ActivationResponse)
def activate_invitation(
    payload: ActivateInvitationRequest,
    request: Request,
) -> ActivationResponse:
    application = slice_one_application(request)
    try:
        activation: ActivationResult = application.activate_invitation(
            token=payload.token,
            display_name=payload.display_name,
            password=payload.password,
        )
    except AccountAlreadyExists as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "ACCOUNT_EXISTS", "message": "Sign in to accept this invitation"},
        ) from error
    except InvalidCredentials as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect"},
        ) from error
    except InvalidInvitation as error:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "code": "INVITATION_UNAVAILABLE",
                "message": "Invitation is invalid or expired",
            },
        ) from error
    return ActivationResponse.model_validate(activation)


@router.post("/invitations/resolve", response_model=InvitationDetailsResponse)
def resolve_invitation(
    payload: ResolveInvitationRequest,
    request: Request,
) -> InvitationDetailsResponse:
    application = slice_one_application(request)
    try:
        details: InvitationDetails = application.resolve_invitation(payload.token)
    except InvalidInvitation as error:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "code": "INVITATION_UNAVAILABLE",
                "message": "Invitation is invalid or expired",
            },
        ) from error
    return InvitationDetailsResponse.model_validate(details)


@router.post("/invitations/accept-existing", response_model=ActivationResponse)
def accept_existing_invitation(
    payload: AcceptExistingInvitationRequest,
    request: Request,
) -> ActivationResponse:
    application = slice_one_application(request)
    try:
        activation = application.accept_invitation_for_existing_user(
            token=payload.token,
            email=str(payload.email),
            password=payload.password,
        )
    except InvalidCredentials as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect"},
        ) from error
    except InvitationEmailMismatch as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "EMAIL_MISMATCH", "message": "Sign in with the invited email"},
        ) from error
    except InvalidInvitation as error:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={"code": "INVITATION_UNAVAILABLE", "message": "Invitation is unavailable"},
        ) from error
    return ActivationResponse.model_validate(activation)

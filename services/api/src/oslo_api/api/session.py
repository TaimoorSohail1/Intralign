from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict

from oslo_api.api.authentication import require_access_token
from oslo_api.identity import InvalidSession
from oslo_api.invitations import InvitePermissionDenied
from oslo_api.slice_one import SessionContext, SliceOneApplication

router = APIRouter(prefix="/v1", tags=["session"])


class SessionContextResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    email: str
    workspace_id: UUID
    display_name: str
    account_role: str
    welcome_required: bool


def slice_one_application(request: Request) -> SliceOneApplication:
    application: SliceOneApplication | None = request.app.state.slice_one
    if application is None:
        from oslo_api.bootstrap import build_slice_one_application

        application = build_slice_one_application()
        request.app.state.slice_one = application
    return application


@router.get("/session", response_model=SessionContextResponse)
def get_session_context(
    request: Request,
    access_token: Annotated[str, Depends(require_access_token)],
) -> SessionContextResponse:
    application = slice_one_application(request)
    try:
        user = application.authenticate(access_token)
        context: SessionContext = application.get_session_context(actor_user_id=user.id)
    except InvalidSession as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        ) from error
    except InvitePermissionDenied as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has no OSLO access",
        ) from error
    return SessionContextResponse.model_validate(context)


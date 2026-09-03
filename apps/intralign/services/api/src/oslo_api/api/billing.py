from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.entitlements.service import (
    BillingConfigurationMissing,
    BillingCustomerMissing,
    BillingPermissionDenied,
    InvalidWebhookSignature,
    OutcomePermissionDenied,
)
from oslo_api.slice_four import (
    BillingInterval,
    EntitlementView,
    HostedCheckoutSession,
    IntentChoice,
    SliceFourApplication,
    WallKey,
)

router = APIRouter(prefix="/v1", tags=["billing"])


class CheckoutSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    interval: BillingInterval
    wall_key: WallKey


class CheckoutSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    url: str


class IntentSignalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wall_key: WallKey
    chosen_path: IntentChoice
    full_option_set: list[str]
    context: dict[str, object]


class EntitlementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workspace_id: UUID
    tier: str
    enforcement_mode: str
    max_active_outcomes: int | None
    max_active_plans: int
    intake_word_envelope: int
    never_metered_exemptions: list[str]
    subscription_status: str
    cancel_at_period_end: bool
    current_period_end: datetime | None
    grace_ends_at: datetime | None
    can_manage_billing: bool


def slice_four_application(request: Request) -> SliceFourApplication:
    application: SliceFourApplication | None = request.app.state.slice_four
    if application is None:
        from oslo_api.bootstrap import build_slice_four_application

        try:
            application = build_slice_four_application()
        except BillingConfigurationMissing as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"code": "BILLING_NOT_CONFIGURED"},
            ) from error
        request.app.state.slice_four = application
    return application


@router.get(
    "/workspaces/{workspace_id}/entitlement",
    response_model=EntitlementResponse,
)
def get_entitlement(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> EntitlementView:
    try:
        return application.get_entitlement(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
        )
    except OutcomePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error


@router.post(
    "/workspaces/{workspace_id}/billing/checkout-sessions",
    response_model=CheckoutSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_checkout_session(
    workspace_id: UUID,
    payload: CheckoutSessionRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> HostedCheckoutSession:
    try:
        return application.create_checkout_session(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            interval=payload.interval,
            wall_key=payload.wall_key,
        )
    except BillingPermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except BillingConfigurationMissing as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "BILLING_NOT_CONFIGURED"},
        ) from error


@router.post(
    "/workspaces/{workspace_id}/billing/portal-sessions",
    response_model=CheckoutSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portal_session(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
):
    try:
        return application.create_portal_session(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
        )
    except BillingPermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    except BillingCustomerMissing as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "BILLING_CUSTOMER_MISSING"},
        ) from error
    except BillingConfigurationMissing as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "BILLING_NOT_CONFIGURED"},
        ) from error


@router.post(
    "/billing/webhooks/stripe",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str, Header(alias="Stripe-Signature")],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> Response:
    payload = await request.body()
    try:
        application.handle_webhook(payload=payload, signature=stripe_signature)
    except InvalidWebhookSignature as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_WEBHOOK_SIGNATURE"},
        ) from error
    except BillingConfigurationMissing as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "BILLING_NOT_CONFIGURED"},
        ) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/workspaces/{workspace_id}/intent-signals",
    status_code=status.HTTP_204_NO_CONTENT,
)
def record_intent_signal(
    workspace_id: UUID,
    payload: IntentSignalRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    application: Annotated[SliceFourApplication, Depends(slice_four_application)],
) -> Response:
    try:
        application.record_intent(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
            wall_key=payload.wall_key,
            chosen_path=payload.chosen_path,
            full_option_set=tuple(payload.full_option_set),
            context=payload.context,
        )
    except OutcomePermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)

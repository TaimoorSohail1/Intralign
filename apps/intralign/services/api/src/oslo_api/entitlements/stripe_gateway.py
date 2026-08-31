from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import stripe

from oslo_api.entitlements.service import InvalidWebhookSignature
from oslo_api.slice_four import (
    BillingInterval,
    HostedCheckoutSession,
    HostedPortalSession,
    SubscriptionState,
    VerifiedCheckoutCompletion,
    VerifiedSubscriptionState,
    WallKey,
)


class StripeBillingGateway:
    def __init__(
        self,
        *,
        secret_key: str,
        webhook_secret: str,
        monthly_price_id: str,
        annual_price_id: str,
        success_url: str,
        cancel_url: str,
        create_session: Callable[..., Any] = stripe.checkout.Session.create,
        create_portal_session: Callable[..., Any] = stripe.billing_portal.Session.create,
        construct_event: Callable[..., Any] = stripe.Webhook.construct_event,
    ) -> None:
        self._secret_key = secret_key
        self._webhook_secret = webhook_secret
        self._monthly_price_id = monthly_price_id
        self._annual_price_id = annual_price_id
        self._success_url = success_url
        self._cancel_url = cancel_url
        self._create_session = create_session
        self._create_portal_session = create_portal_session
        self._construct_event = construct_event

    def create_basic_checkout(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession:
        price_id = (
            self._monthly_price_id
            if interval is BillingInterval.MONTHLY
            else self._annual_price_id
        )
        metadata = {
            "workspace_id": str(workspace_id),
            "actor_user_id": str(actor_user_id),
            "plan_code": "basic",
            "billing_interval": interval.value,
            "wall_key": wall_key.value,
        }
        session = self._create_session(
            api_key=self._secret_key,
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=self._success_url,
            cancel_url=self._cancel_url,
            client_reference_id=str(workspace_id),
            metadata=metadata,
            subscription_data={
                "metadata": {
                    "workspace_id": str(workspace_id),
                    "plan_code": "basic",
                }
            },
        )
        if not session.url:
            raise RuntimeError("Stripe did not return a hosted Checkout URL")
        return HostedCheckoutSession(id=session.id, url=session.url)

    def create_billing_portal(self, *, customer_id: str) -> HostedPortalSession:
        session = self._create_portal_session(
            api_key=self._secret_key,
            customer=customer_id,
            return_url=self._success_url.split("?", maxsplit=1)[0],
        )
        return HostedPortalSession(id=session.id, url=session.url)

    def verify_billing_event(
        self, *, payload: bytes, signature: str
    ) -> VerifiedCheckoutCompletion | VerifiedSubscriptionState | None:
        try:
            event = self._construct_event(
                payload,
                signature,
                self._webhook_secret,
                api_key=self._secret_key,
            )
        except (ValueError, stripe.error.SignatureVerificationError) as error:
            raise InvalidWebhookSignature from error

        event_type = event["type"]
        provider_object: Mapping[str, Any] = event["data"]["object"]
        if event_type == "checkout.session.completed":
            return self._checkout_completion(event_id=str(event["id"]), checkout=provider_object)
        if event_type in {"customer.subscription.updated", "customer.subscription.deleted"}:
            return self._subscription_state(
                event_id=str(event["id"]),
                event_type=event_type,
                subscription=provider_object,
            )
        return None

    @staticmethod
    def _checkout_completion(
        *, event_id: str, checkout: Mapping[str, Any]
    ) -> VerifiedCheckoutCompletion | None:
        if checkout.get("mode") != "subscription" or checkout.get("payment_status") != "paid":
            return None
        metadata = checkout.get("metadata") or {}
        if metadata.get("plan_code") != "basic":
            return None
        try:
            workspace_id = UUID(str(metadata["workspace_id"]))
        except (KeyError, ValueError) as error:
            raise InvalidWebhookSignature from error
        customer_id = checkout.get("customer")
        subscription_id = checkout.get("subscription")
        if not isinstance(customer_id, str) or not isinstance(subscription_id, str):
            return None
        return VerifiedCheckoutCompletion(
            event_id=event_id,
            checkout_session_id=str(checkout["id"]),
            workspace_id=workspace_id,
            customer_id=customer_id,
            subscription_id=subscription_id,
        )

    @staticmethod
    def _subscription_state(
        *, event_id: str, event_type: str, subscription: Mapping[str, Any]
    ) -> VerifiedSubscriptionState | None:
        subscription_id = subscription.get("id")
        if not isinstance(subscription_id, str):
            return None
        provider_status = str(subscription.get("status", ""))
        if event_type == "customer.subscription.deleted" or provider_status == "canceled":
            state = SubscriptionState.CANCELLED
        elif provider_status in {"active", "trialing"}:
            state = SubscriptionState.ACTIVE
        else:
            state = SubscriptionState.PAST_DUE
        period_end = subscription.get("current_period_end")
        return VerifiedSubscriptionState(
            event_id=event_id,
            subscription_id=subscription_id,
            state=state,
            cancel_at_period_end=bool(subscription.get("cancel_at_period_end", False)),
            current_period_end=(
                datetime.fromtimestamp(period_end, tz=UTC)
                if isinstance(period_end, int | float)
                else None
            ),
        )

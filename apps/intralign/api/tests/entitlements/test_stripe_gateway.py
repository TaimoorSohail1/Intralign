from types import SimpleNamespace
from uuid import UUID

import pytest

from oslo_api.entitlements.service import InvalidWebhookSignature
from oslo_api.entitlements.stripe_gateway import StripeBillingGateway
from oslo_api.slice_four import BillingInterval, VerifiedCheckoutCompletion, WallKey

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")


def test_checkout_is_hosted_subscription_checkout_with_server_owned_metadata() -> None:
    requests: list[dict[str, object]] = []

    def create_session(**params: object) -> SimpleNamespace:
        requests.append(params)
        return SimpleNamespace(
            id="cs_test_123",
            url="https://checkout.stripe.com/c/pay/cs_test_123",
        )

    gateway = StripeBillingGateway(
        secret_key="sk_test_example",
        webhook_secret="whsec_example",
        monthly_price_id="price_basic_monthly",
        annual_price_id="price_basic_annual",
        success_url="https://app.example.com/settings?checkout=success",
        cancel_url="https://app.example.com/settings?checkout=cancelled",
        create_session=create_session,
    )

    session = gateway.create_basic_checkout(
        workspace_id=WORKSPACE_ID,
        actor_user_id=USER_ID,
        interval=BillingInterval.ANNUAL,
        wall_key=WallKey.MULTI_OUTCOME,
    )

    assert session.id == "cs_test_123"
    assert requests == [
        {
            "api_key": "sk_test_example",
            "mode": "subscription",
            "line_items": [{"price": "price_basic_annual", "quantity": 1}],
            "success_url": "https://app.example.com/settings?checkout=success",
            "cancel_url": "https://app.example.com/settings?checkout=cancelled",
            "client_reference_id": str(WORKSPACE_ID),
            "metadata": {
                "workspace_id": str(WORKSPACE_ID),
                "actor_user_id": str(USER_ID),
                "plan_code": "basic",
                "billing_interval": "annual",
                "wall_key": "multiOutcome",
            },
            "subscription_data": {
                "metadata": {
                    "workspace_id": str(WORKSPACE_ID),
                    "plan_code": "basic",
                }
            },
        }
    ]


def test_only_stripe_verified_paid_basic_checkout_is_converted_to_a_grant() -> None:
    observed: list[tuple[bytes, str, str, str]] = []

    def construct_event(
        payload: bytes, signature: str, secret: str, *, api_key: str
    ) -> dict[str, object]:
        observed.append((payload, signature, secret, api_key))
        return {
            "id": "evt_paid",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_paid",
                    "mode": "subscription",
                    "payment_status": "paid",
                    "customer": "cus_paid",
                    "subscription": "sub_paid",
                    "metadata": {
                        "workspace_id": str(WORKSPACE_ID),
                        "plan_code": "basic",
                    },
                }
            },
        }

    gateway = StripeBillingGateway(
        secret_key="sk_test_example",
        webhook_secret="whsec_example",
        monthly_price_id="price_basic_monthly",
        annual_price_id="price_basic_annual",
        success_url="https://app.example.com/settings?checkout=success",
        cancel_url="https://app.example.com/settings?checkout=cancelled",
        construct_event=construct_event,
    )

    completion = gateway.verify_billing_event(
        payload=b'{"id":"evt_paid"}',
        signature="signed-header",
    )

    assert completion == VerifiedCheckoutCompletion(
        event_id="evt_paid",
        checkout_session_id="cs_paid",
        workspace_id=WORKSPACE_ID,
        customer_id="cus_paid",
        subscription_id="sub_paid",
    )
    assert observed == [
        (
            b'{"id":"evt_paid"}',
            "signed-header",
            "whsec_example",
            "sk_test_example",
        )
    ]


def test_invalid_stripe_signature_never_becomes_a_billing_event() -> None:
    def reject_event(*_args: object, **_kwargs: object) -> None:
        raise ValueError("invalid signature")

    gateway = StripeBillingGateway(
        secret_key="sk_test_example",
        webhook_secret="whsec_example",
        monthly_price_id="price_basic_monthly",
        annual_price_id="price_basic_annual",
        success_url="https://app.example.com/settings?checkout=success",
        cancel_url="https://app.example.com/settings?checkout=cancelled",
        construct_event=reject_event,
    )

    with pytest.raises(InvalidWebhookSignature):
        gateway.verify_billing_event(payload=b"{}", signature="forged")

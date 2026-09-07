from datetime import UTC, datetime
from uuid import UUID

from fastapi.testclient import TestClient

from oslo_api.main import create_app
from oslo_api.slice_four import (
    BillingInterval,
    EntitlementView,
    HostedCheckoutSession,
    HostedPortalSession,
    IntentChoice,
    WallKey,
)
from oslo_api.slice_one import AuthenticatedUser

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")
HEADERS = {"Authorization": "Bearer valid-access-token"}


class AuthenticatedSliceOne:
    def authenticate(self, access_token: str) -> AuthenticatedUser:
        assert access_token == "valid-access-token"
        return AuthenticatedUser(id=USER_ID, email="owner@example.com")


class RecordingSliceFour:
    def __init__(self) -> None:
        self.checkout_requests: list[tuple[UUID, UUID, BillingInterval, WallKey]] = []
        self.webhooks: list[tuple[bytes, str]] = []
        self.intents: list[tuple[UUID, UUID, WallKey, IntentChoice]] = []
        self.portal_requests: list[tuple[UUID, UUID]] = []

    def create_checkout_session(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession:
        self.checkout_requests.append((actor_user_id, workspace_id, interval, wall_key))
        return HostedCheckoutSession(
            id="cs_test_123",
            url="https://checkout.stripe.com/c/pay/cs_test_123",
        )

    def handle_webhook(self, *, payload: bytes, signature: str) -> None:
        self.webhooks.append((payload, signature))

    def record_intent(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        wall_key: WallKey,
        chosen_path: IntentChoice,
        **_kwargs,
    ) -> None:
        self.intents.append((actor_user_id, workspace_id, wall_key, chosen_path))

    def create_portal_session(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> HostedPortalSession:
        self.portal_requests.append((actor_user_id, workspace_id))
        return HostedPortalSession(
            id="bps_test_123",
            url="https://billing.stripe.com/p/session/bps_test_123",
        )

    def get_entitlement(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> EntitlementView:
        return EntitlementView(
            workspace_id=workspace_id,
            tier="free",
            enforcement_mode="enforce",
            max_active_outcomes=1,
            max_active_plans=1,
            intake_word_envelope=50_000,
            never_metered_exemptions=(
                "record",
                "reviewer_loop",
                "crr",
                "viewers",
                "judgment_quality",
            ),
            subscription_status="active",
            cancel_at_period_end=False,
            current_period_end=datetime(2026, 9, 13, tzinfo=UTC),
            grace_ends_at=datetime(2026, 9, 20, tzinfo=UTC),
            can_manage_billing=True,
        )


def test_owner_can_start_real_hosted_basic_checkout() -> None:
    slice_four = RecordingSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    response = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/billing/checkout-sessions",
        headers=HEADERS,
        json={"interval": "monthly", "wall_key": "multiPlan"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": "cs_test_123",
        "url": "https://checkout.stripe.com/c/pay/cs_test_123",
    }
    assert slice_four.checkout_requests == [
        (USER_ID, WORKSPACE_ID, BillingInterval.MONTHLY, WallKey.MULTI_PLAN)
    ]


def test_stripe_webhook_uses_the_raw_signed_payload_without_user_auth() -> None:
    slice_four = RecordingSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    response = client.post(
        "/v1/billing/webhooks/stripe",
        content=b'{"id":"evt_123"}',
        headers={"Stripe-Signature": "t=123,v1=signature"},
    )

    assert response.status_code == 204
    assert slice_four.webhooks == [
        (b'{"id":"evt_123"}', "t=123,v1=signature")
    ]


def test_capacity_gate_choice_is_recorded_for_the_authenticated_member() -> None:
    slice_four = RecordingSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    response = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/intent-signals",
        headers=HEADERS,
        json={
            "wall_key": "multiOutcome",
            "chosen_path": "declined",
            "full_option_set": ["archive_to_switch", "upgrade_basic", "not_now"],
            "context": {"surface": "outcome_gate"},
        },
    )

    assert response.status_code == 204
    assert slice_four.intents == [
        (USER_ID, WORKSPACE_ID, WallKey.MULTI_OUTCOME, IntentChoice.DECLINED)
    ]


def test_owner_can_open_hosted_billing_portal_for_cancellation() -> None:
    slice_four = RecordingSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    response = client.post(
        f"/v1/workspaces/{WORKSPACE_ID}/billing/portal-sessions",
        headers=HEADERS,
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": "bps_test_123",
        "url": "https://billing.stripe.com/p/session/bps_test_123",
    }
    assert slice_four.portal_requests == [(USER_ID, WORKSPACE_ID)]


def test_entitlement_exposes_capacity_and_never_metered_contract() -> None:
    slice_four = RecordingSliceFour()
    client = TestClient(
        create_app(slice_one=AuthenticatedSliceOne(), slice_four=slice_four)
    )

    response = client.get(
        f"/v1/workspaces/{WORKSPACE_ID}/entitlement",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "workspace_id": str(WORKSPACE_ID),
        "tier": "free",
        "enforcement_mode": "enforce",
        "max_active_outcomes": 1,
        "max_active_plans": 1,
        "intake_word_envelope": 50_000,
        "never_metered_exemptions": [
            "record",
            "reviewer_loop",
            "crr",
            "viewers",
            "judgment_quality",
        ],
        "subscription_status": "active",
        "cancel_at_period_end": False,
        "current_period_end": "2026-09-13T00:00:00Z",
        "grace_ends_at": "2026-09-20T00:00:00Z",
        "can_manage_billing": True,
    }

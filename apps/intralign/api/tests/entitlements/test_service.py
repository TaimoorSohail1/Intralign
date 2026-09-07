from dataclasses import dataclass
from uuid import UUID

import pytest

from oslo_api.entitlements.service import (
    BillingConfigurationMissing,
    EntitlementService,
    InvalidWebhookSignature,
)
from oslo_api.slice_four import (
    BillingInterval,
    HostedCheckoutSession,
    IntentChoice,
    SubscriptionState,
    VerifiedCheckoutCompletion,
    VerifiedSubscriptionState,
    WallKey,
)

USER_ID = UUID("018f9f7e-8de2-7000-8000-000000000011")
WORKSPACE_ID = UUID("018f9f7e-8de2-7000-8000-000000000010")


@dataclass
class RecordingRepository:
    owner_checks: list[tuple[UUID, UUID]]
    checkout_starts: list[tuple[UUID, UUID, str, BillingInterval, WallKey]]
    grants: list[str]
    intents: list[tuple[UUID, UUID, WallKey, IntentChoice]]
    subscription_changes: list[VerifiedSubscriptionState]

    def require_owner(self, *, workspace_id: UUID, actor_user_id: UUID) -> None:
        self.owner_checks.append((workspace_id, actor_user_id))

    def record_checkout_started(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        checkout_session_id: str,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> None:
        self.checkout_starts.append(
            (workspace_id, actor_user_id, checkout_session_id, interval, wall_key)
        )

    def commit_checkout_and_grant_basic(
        self, *, completion: VerifiedCheckoutCompletion
    ) -> None:
        self.grants.append(completion.checkout_session_id)

    def record_intent(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        wall_key: WallKey,
        chosen_path: IntentChoice,
        full_option_set: tuple[str, ...],
        context: dict[str, object],
    ) -> None:
        self.intents.append((actor_user_id, workspace_id, wall_key, chosen_path))

    def apply_subscription_state(
        self, *, change: VerifiedSubscriptionState
    ) -> None:
        self.subscription_changes.append(change)


class RecordingGateway:
    def __init__(self) -> None:
        self.requests: list[tuple[UUID, UUID, BillingInterval]] = []

    def create_basic_checkout(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession:
        self.requests.append((workspace_id, actor_user_id, interval))
        return HostedCheckoutSession(
            id="cs_test_123",
            url="https://checkout.stripe.com/c/pay/cs_test_123",
        )

    def verify_billing_event(
        self, *, payload: bytes, signature: str
    ) -> VerifiedCheckoutCompletion | VerifiedSubscriptionState | None:
        if signature != "verified-signature":
            if signature == "verified-cancellation":
                return VerifiedSubscriptionState(
                    event_id="evt_cancelled",
                    subscription_id="sub_123",
                    state=SubscriptionState.CANCELLED,
                    cancel_at_period_end=False,
                    current_period_end=None,
                )
            raise InvalidWebhookSignature
        return VerifiedCheckoutCompletion(
            event_id="evt_123",
            checkout_session_id="cs_test_123",
            workspace_id=WORKSPACE_ID,
            customer_id="cus_123",
            subscription_id="sub_123",
        )


def test_checkout_records_pending_state_but_does_not_grant_basic() -> None:
    repository = RecordingRepository([], [], [], [], [])
    gateway = RecordingGateway()
    service = EntitlementService(repository=repository, billing_gateway=gateway)

    session = service.create_checkout_session(
        actor_user_id=USER_ID,
        workspace_id=WORKSPACE_ID,
        interval=BillingInterval.MONTHLY,
        wall_key=WallKey.MULTI_PLAN,
    )

    assert session.id == "cs_test_123"
    assert repository.owner_checks == [(WORKSPACE_ID, USER_ID)]
    assert repository.checkout_starts == [
        (
            WORKSPACE_ID,
            USER_ID,
            "cs_test_123",
            BillingInterval.MONTHLY,
            WallKey.MULTI_PLAN,
        )
    ]
    assert repository.grants == []


def test_non_billing_entitlement_work_remains_available_without_stripe() -> None:
    repository = RecordingRepository([], [], [], [], [])
    service = EntitlementService(repository=repository, billing_gateway=None)

    service.record_intent(
        actor_user_id=USER_ID,
        workspace_id=WORKSPACE_ID,
        wall_key=WallKey.MULTI_OUTCOME,
        chosen_path=IntentChoice.FREE_PATH,
        full_option_set=("archive_to_switch", "upgrade_basic", "not_now"),
        context={"surface": "outcome_gate"},
    )

    assert repository.intents == [
        (USER_ID, WORKSPACE_ID, WallKey.MULTI_OUTCOME, IntentChoice.FREE_PATH)
    ]
    with pytest.raises(BillingConfigurationMissing):
        service.create_checkout_session(
            actor_user_id=USER_ID,
            workspace_id=WORKSPACE_ID,
            interval=BillingInterval.MONTHLY,
            wall_key=WallKey.MULTI_OUTCOME,
        )


def test_only_a_signature_verified_checkout_completion_grants_basic() -> None:
    repository = RecordingRepository([], [], [], [], [])
    gateway = RecordingGateway()
    service = EntitlementService(repository=repository, billing_gateway=gateway)

    with pytest.raises(InvalidWebhookSignature):
        service.handle_webhook(payload=b"{}", signature="forged-signature")

    assert repository.grants == []

    service.handle_webhook(payload=b"{}", signature="verified-signature")

    assert repository.grants == ["cs_test_123"]


def test_verified_subscription_cancellation_updates_entitlement_state() -> None:
    repository = RecordingRepository([], [], [], [], [])
    service = EntitlementService(
        repository=repository,
        billing_gateway=RecordingGateway(),
    )

    service.handle_webhook(payload=b"{}", signature="verified-cancellation")

    assert repository.subscription_changes == [
        VerifiedSubscriptionState(
            event_id="evt_cancelled",
            subscription_id="sub_123",
            state=SubscriptionState.CANCELLED,
            cancel_at_period_end=False,
            current_period_end=None,
        )
    ]


@pytest.mark.parametrize("chosen_path", list(IntentChoice))
def test_every_capacity_wall_branch_is_recorded(chosen_path: IntentChoice) -> None:
    repository = RecordingRepository([], [], [], [], [])
    service = EntitlementService(
        repository=repository,
        billing_gateway=RecordingGateway(),
    )

    service.record_intent(
        actor_user_id=USER_ID,
        workspace_id=WORKSPACE_ID,
        wall_key=WallKey.MULTI_OUTCOME,
        chosen_path=chosen_path,
        full_option_set=("archive_to_switch", "upgrade_basic", "not_now"),
        context={"surface": "outcome_gate"},
    )

    assert repository.intents == [
        (USER_ID, WORKSPACE_ID, WallKey.MULTI_OUTCOME, chosen_path)
    ]

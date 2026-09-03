from typing import Protocol
from uuid import UUID

from oslo_api.slice_four import (
    BillingInterval,
    EntitlementView,
    HostedCheckoutSession,
    HostedPortalSession,
    IntentChoice,
    OutcomeProvenance,
    ProjectOutcome,
    VerifiedCheckoutCompletion,
    VerifiedSubscriptionState,
    WallKey,
)


class InvalidWebhookSignature(Exception):
    """Raised when the billing provider cannot authenticate a webhook payload."""


class BillingPermissionDenied(Exception):
    """Raised when a non-Owner attempts a workspace billing operation."""


class UnknownCheckoutSession(Exception):
    """Raised when a verified event does not match a server-created checkout."""


class UnknownSubscription(Exception):
    """Raised so an out-of-order subscription event remains retryable."""


class BillingConfigurationMissing(Exception):
    """Raised when hosted billing is not configured for this environment."""


class BillingCustomerMissing(Exception):
    """Raised when a workspace has no provider customer for portal access."""


class OutcomePermissionDenied(Exception):
    """Raised when a workspace member cannot manage the requested Outcome."""


class OutcomeCapacityReached(Exception):
    """Raised when activating another Outcome requires a Basic commitment."""

    def __init__(self, *, active_outcome_limit: int) -> None:
        self.active_outcome_limit = active_outcome_limit
        super().__init__("Workspace active Outcome limit reached")


class OutcomeNotFound(Exception):
    """Raised when the requested Outcome is outside the actor's workspace scope."""


class EntitlementRepository(Protocol):
    def get_entitlement(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> EntitlementView: ...

    def require_owner(self, *, workspace_id: UUID, actor_user_id: UUID) -> None: ...

    def customer_id_for_owner(
        self, *, workspace_id: UUID, actor_user_id: UUID
    ) -> str: ...

    def record_checkout_started(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        checkout_session_id: str,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> None: ...

    def commit_checkout_and_grant_basic(
        self, *, completion: VerifiedCheckoutCompletion
    ) -> None: ...

    def apply_subscription_state(
        self, *, change: VerifiedSubscriptionState
    ) -> None: ...

    def create_outcome(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
        title: str,
        provenance: OutcomeProvenance,
    ) -> ProjectOutcome: ...

    def list_outcomes(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
    ) -> list[ProjectOutcome]: ...

    def archive_outcome(
        self, *, actor_user_id: UUID, workspace_id: UUID, outcome_id: UUID
    ) -> ProjectOutcome: ...

    def reactivate_outcome(
        self, *, actor_user_id: UUID, workspace_id: UUID, outcome_id: UUID
    ) -> ProjectOutcome: ...

    def record_intent(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        wall_key: WallKey,
        chosen_path: IntentChoice,
        full_option_set: tuple[str, ...],
        context: dict[str, object],
    ) -> None: ...


class BillingGateway(Protocol):
    def create_basic_checkout(
        self,
        *,
        workspace_id: UUID,
        actor_user_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession: ...

    def create_billing_portal(self, *, customer_id: str) -> HostedPortalSession: ...

    def verify_billing_event(
        self, *, payload: bytes, signature: str
    ) -> VerifiedCheckoutCompletion | VerifiedSubscriptionState | None: ...


class EntitlementService:
    def __init__(
        self,
        *,
        repository: EntitlementRepository,
        billing_gateway: BillingGateway | None,
    ) -> None:
        self._repository = repository
        self._billing_gateway = billing_gateway

    def get_entitlement(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> EntitlementView:
        return self._repository.get_entitlement(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
        )

    def create_checkout_session(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession:
        self._repository.require_owner(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
        )
        if self._billing_gateway is None:
            raise BillingConfigurationMissing
        session = self._billing_gateway.create_basic_checkout(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            interval=interval,
            wall_key=wall_key,
        )
        self._repository.record_checkout_started(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            checkout_session_id=session.id,
            interval=interval,
            wall_key=wall_key,
        )
        return session

    def handle_webhook(self, *, payload: bytes, signature: str) -> None:
        if self._billing_gateway is None:
            raise BillingConfigurationMissing
        event = self._billing_gateway.verify_billing_event(
            payload=payload,
            signature=signature,
        )
        if event is None:
            return
        if isinstance(event, VerifiedCheckoutCompletion):
            self._repository.commit_checkout_and_grant_basic(completion=event)
            return
        self._repository.apply_subscription_state(change=event)

    def create_portal_session(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> HostedPortalSession:
        customer_id = self._repository.customer_id_for_owner(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
        )
        if self._billing_gateway is None:
            raise BillingConfigurationMissing
        return self._billing_gateway.create_billing_portal(customer_id=customer_id)

    def create_outcome(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
        title: str,
        provenance: OutcomeProvenance,
    ) -> ProjectOutcome:
        return self._repository.create_outcome(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            project_id=project_id,
            title=title,
            provenance=provenance,
        )

    def list_outcomes(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        project_id: UUID,
    ) -> list[ProjectOutcome]:
        return self._repository.list_outcomes(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            project_id=project_id,
        )

    def archive_outcome(
        self, *, actor_user_id: UUID, workspace_id: UUID, outcome_id: UUID
    ) -> ProjectOutcome:
        return self._repository.archive_outcome(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            outcome_id=outcome_id,
        )

    def reactivate_outcome(
        self, *, actor_user_id: UUID, workspace_id: UUID, outcome_id: UUID
    ) -> ProjectOutcome:
        return self._repository.reactivate_outcome(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            outcome_id=outcome_id,
        )

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
        self._repository.record_intent(
            actor_user_id=actor_user_id,
            workspace_id=workspace_id,
            wall_key=wall_key,
            chosen_path=chosen_path,
            full_option_set=full_option_set,
            context=context,
        )

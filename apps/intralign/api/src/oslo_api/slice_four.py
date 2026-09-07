from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID


class BillingInterval(StrEnum):
    MONTHLY = "monthly"
    ANNUAL = "annual"


class WallKey(StrEnum):
    MULTI_OUTCOME = "multiOutcome"
    MULTI_PLAN = "multiPlan"
    ENVELOPE = "envelope"
    SCHEDULE = "schedule"


class IntentChoice(StrEnum):
    COMMITTED = "committed"
    FREE_PATH = "free_path"
    DECLINED = "declined"
    KEEP_BOTH = "keep_both"


class SubscriptionState(StrEnum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"


class OutcomeStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class OutcomeProvenance(StrEnum):
    DECLARED = "declared"
    INFERRED = "inferred"


@dataclass(frozen=True, slots=True)
class HostedCheckoutSession:
    id: str
    url: str


@dataclass(frozen=True, slots=True)
class HostedPortalSession:
    id: str
    url: str


@dataclass(frozen=True, slots=True)
class EntitlementView:
    workspace_id: UUID
    tier: str
    enforcement_mode: str
    max_active_outcomes: int | None
    max_active_plans: int
    intake_word_envelope: int
    never_metered_exemptions: tuple[str, ...]
    subscription_status: str
    cancel_at_period_end: bool
    current_period_end: datetime | None
    grace_ends_at: datetime | None
    can_manage_billing: bool


@dataclass(frozen=True, slots=True)
class VerifiedCheckoutCompletion:
    event_id: str
    checkout_session_id: str
    workspace_id: UUID
    customer_id: str
    subscription_id: str


@dataclass(frozen=True, slots=True)
class VerifiedSubscriptionState:
    event_id: str
    subscription_id: str
    state: SubscriptionState
    cancel_at_period_end: bool
    current_period_end: datetime | None


@dataclass(frozen=True, slots=True)
class ProjectOutcome:
    id: UUID
    workspace_id: UUID
    project_id: UUID
    title: str
    status: OutcomeStatus
    is_primary: bool
    provenance: OutcomeProvenance
    created_at: datetime
    archived_at: datetime | None


class SliceFourApplication(Protocol):
    def get_entitlement(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> EntitlementView: ...

    def create_checkout_session(
        self,
        *,
        actor_user_id: UUID,
        workspace_id: UUID,
        interval: BillingInterval,
        wall_key: WallKey,
    ) -> HostedCheckoutSession: ...

    def handle_webhook(self, *, payload: bytes, signature: str) -> None: ...

    def create_portal_session(
        self, *, actor_user_id: UUID, workspace_id: UUID
    ) -> HostedPortalSession: ...

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

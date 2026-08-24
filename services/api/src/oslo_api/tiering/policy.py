from dataclasses import dataclass
from enum import StrEnum


class PlanCode(StrEnum):
    FREE = "free"
    BASIC = "basic"


@dataclass(frozen=True, slots=True)
class CapacityDecision:
    allowed: bool
    partial: bool = False
    remedies: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PlanPolicy:
    code: PlanCode
    label: str
    price_usd_monthly: int
    judgment_profile: str
    document_limit: int
    word_limit: int
    collaborator_seat_limit: int
    monthly_invitation_limit: int
    monthly_analysis_limit: int | None
    chat_is_metered: bool = False

    def decide_document_capacity(
        self, *, document_count: int, word_count: int
    ) -> CapacityDecision:
        if document_count <= self.document_limit and word_count <= self.word_limit:
            return CapacityDecision(allowed=True)
        return CapacityDecision(
            allowed=False,
            remedies=("remove_documents", "compare_plans"),
        )

    def decide_collaborator_capacity(self, *, occupied_seats: int) -> CapacityDecision:
        if occupied_seats < self.collaborator_seat_limit:
            return CapacityDecision(allowed=True)
        return CapacityDecision(
            allowed=False,
            remedies=("invite_as_viewer", "compare_plans"),
        )


_POLICIES = {
    PlanCode.FREE: PlanPolicy(
        code=PlanCode.FREE,
        label="Free",
        price_usd_monthly=0,
        judgment_profile="oslo-governed-v1",
        document_limit=20,
        word_limit=50_000,
        collaborator_seat_limit=3,
        monthly_invitation_limit=2,
        monthly_analysis_limit=None,
    ),
    PlanCode.BASIC: PlanPolicy(
        code=PlanCode.BASIC,
        label="Basic",
        price_usd_monthly=12,
        judgment_profile="oslo-governed-v1",
        document_limit=40,
        word_limit=100_000,
        collaborator_seat_limit=10,
        monthly_invitation_limit=5,
        monthly_analysis_limit=None,
    ),
}


def get_plan_policy(code: PlanCode | str) -> PlanPolicy:
    try:
        normalized = PlanCode(str(code).lower())
    except ValueError:
        normalized = PlanCode.FREE
    return _POLICIES[normalized]

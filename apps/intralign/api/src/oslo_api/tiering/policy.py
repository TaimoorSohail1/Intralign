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
    price_usd_annual: int
    judgment_profile: str
    document_limit: int
    word_limit: int
    collaborator_seat_limit: int | None
    monthly_invitation_limit: int | None
    monthly_analysis_limit: int | None
    active_project_limit: int
    active_outcome_limit: int | None
    never_metered_exemptions: tuple[str, ...]
    chat_is_metered: bool = False

    def decide_document_capacity(
        self, *, document_count: int, word_count: int
    ) -> CapacityDecision:
        if word_count <= self.word_limit:
            return CapacityDecision(allowed=True)
        return CapacityDecision(
            allowed=False,
            remedies=("remove_documents", "compare_plans"),
        )

    def decide_collaborator_capacity(self, *, occupied_seats: int) -> CapacityDecision:
        return CapacityDecision(allowed=True)


_POLICIES = {
    PlanCode.FREE: PlanPolicy(
        code=PlanCode.FREE,
        label="Free",
        price_usd_monthly=0,
        price_usd_annual=0,
        judgment_profile="oslo-governed-v1",
        document_limit=100,
        word_limit=50_000,
        collaborator_seat_limit=None,
        monthly_invitation_limit=None,
        monthly_analysis_limit=None,
        active_project_limit=1,
        active_outcome_limit=1,
        never_metered_exemptions=(
            "record",
            "reviewer_loop",
            "crr",
            "viewers",
            "judgment_quality",
        ),
    ),
    PlanCode.BASIC: PlanPolicy(
        code=PlanCode.BASIC,
        label="Basic",
        price_usd_monthly=29,
        price_usd_annual=290,
        judgment_profile="oslo-governed-v1",
        document_limit=100,
        word_limit=100_000,
        collaborator_seat_limit=None,
        monthly_invitation_limit=None,
        monthly_analysis_limit=None,
        active_project_limit=3,
        active_outcome_limit=None,
        never_metered_exemptions=(
            "record",
            "reviewer_loop",
            "crr",
            "viewers",
            "judgment_quality",
        ),
    ),
}


def get_plan_policy(code: PlanCode | str) -> PlanPolicy:
    try:
        normalized = PlanCode(str(code).lower())
    except ValueError:
        normalized = PlanCode.FREE
    return _POLICIES[normalized]

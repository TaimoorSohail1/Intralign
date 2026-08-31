from oslo_api.tiering.policy import PlanCode, get_plan_policy


def test_free_and_basic_define_capacity_without_metering_people_or_quality() -> None:
    free = get_plan_policy(PlanCode.FREE)
    basic = get_plan_policy(PlanCode.BASIC)

    assert free.judgment_profile == basic.judgment_profile == "oslo-governed-v1"
    assert free.active_project_limit == 1
    assert basic.active_project_limit == 3
    assert free.active_outcome_limit == 1
    assert basic.active_outcome_limit is None
    assert free.price_usd_monthly == 0
    assert basic.price_usd_monthly == 29
    assert basic.price_usd_annual == 290
    assert free.document_limit == basic.document_limit
    assert free.word_limit == 50_000
    assert basic.word_limit == 100_000
    assert free.collaborator_seat_limit is None
    assert basic.collaborator_seat_limit is None
    assert free.monthly_invitation_limit is None
    assert basic.monthly_invitation_limit is None
    assert free.monthly_analysis_limit is None
    assert basic.monthly_analysis_limit is None
    assert free.chat_is_metered is False
    assert basic.chat_is_metered is False
    assert free.never_metered_exemptions == (
        "record",
        "reviewer_loop",
        "crr",
        "viewers",
        "judgment_quality",
    )


def test_plan_policy_exposes_contextual_remedies_without_destructive_actions() -> None:
    free = get_plan_policy(PlanCode.FREE)

    document_decision = free.decide_document_capacity(
        document_count=21,
        word_count=52_000,
    )
    file_count_decision = free.decide_document_capacity(
        document_count=21,
        word_count=49_000,
    )
    seat_decision = free.decide_collaborator_capacity(occupied_seats=10_000)

    assert document_decision.allowed is False
    assert document_decision.partial is False
    assert document_decision.remedies == ("remove_documents", "compare_plans")
    assert file_count_decision.allowed is True
    assert seat_decision.allowed is True
    assert seat_decision.remedies == ()

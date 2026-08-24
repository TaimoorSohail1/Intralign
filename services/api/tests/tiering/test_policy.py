from oslo_api.tiering.policy import PlanCode, get_plan_policy


def test_free_and_basic_share_the_same_judgment_and_unlimited_projects() -> None:
    free = get_plan_policy(PlanCode.FREE)
    basic = get_plan_policy(PlanCode.BASIC)

    assert free.judgment_profile == basic.judgment_profile == "oslo-governed-v1"
    assert not hasattr(free, "active_project_limit")
    assert not hasattr(basic, "active_project_limit")
    assert free.document_limit == 20
    assert basic.document_limit == 40
    assert free.word_limit == 50_000
    assert basic.word_limit == 100_000
    assert free.collaborator_seat_limit == 3
    assert basic.collaborator_seat_limit == 10
    assert free.monthly_invitation_limit == 2
    assert basic.monthly_invitation_limit == 5
    assert free.monthly_analysis_limit is None
    assert basic.monthly_analysis_limit is None
    assert free.chat_is_metered is False
    assert basic.chat_is_metered is False


def test_plan_policy_exposes_contextual_remedies_without_destructive_actions() -> None:
    free = get_plan_policy(PlanCode.FREE)

    document_decision = free.decide_document_capacity(
        document_count=21,
        word_count=52_000,
    )
    seat_decision = free.decide_collaborator_capacity(occupied_seats=3)

    assert document_decision.allowed is False
    assert document_decision.partial is False
    assert document_decision.remedies == ("remove_documents", "compare_plans")
    assert seat_decision.allowed is False
    assert seat_decision.remedies == ("invite_as_viewer", "compare_plans")

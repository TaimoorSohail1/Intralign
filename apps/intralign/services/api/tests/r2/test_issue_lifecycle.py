from oslo_api.analysis.issue_lifecycle import (
    Actor,
    Basis,
    IssueLifecycle,
    LifecycleAct,
    LifecycleState,
    basis_strength,
)


def test_confirm_is_typed_and_only_reanalysis_resolves() -> None:
    issue = IssueLifecycle.open("ISS-VENUE-WIFI")

    addressed = issue.enqueue(
        act=LifecycleAct.CONFIRM,
        actor=Actor(id="user-1", display_name="Idris", role="owner"),
        basis=Basis.VERIFIED_DIRECTLY,
        evidence_ref="evidence:venue-contract",
    )

    assert addressed.state is LifecycleState.ADDRESSED
    assert addressed.attestations[-1].basis is Basis.VERIFIED_DIRECTLY
    assert addressed.attestations[-1].evidence_ref == "evidence:venue-contract"
    assert addressed.history[-1].event_type == "grounding_act.confirmed"

    resolved = addressed.land_reanalysis()

    assert resolved.state is LifecycleState.RESOLVED
    assert resolved.history[-1].event_type == "issue.resolved"


def test_flag_grounds_the_item_but_never_firms_viability_or_closes_it() -> None:
    issue = IssueLifecycle.open("ISS-REGISTRATION-SHOW-RATE")

    addressed = issue.enqueue(
        act=LifecycleAct.FLAG,
        actor=Actor(id="user-1", display_name="Idris", role="owner"),
        basis=Basis.DOCUMENTED,
        evidence_ref="evidence:registration-export",
    )

    assert addressed.state is LifecycleState.ADDRESSED
    assert addressed.grounding_credited is False
    assert addressed.viability_firm is False

    needs_fix = addressed.land_reanalysis()

    assert needs_fix.state is LifecycleState.NEEDS_FIX
    assert needs_fix.grounding_credited is True
    assert needs_fix.statement_grounded is False
    assert needs_fix.viability_firm is False
    assert needs_fix.history[-1].event_type == "issue.needs_fix"


def test_fix_then_grounding_are_separate_acts_and_only_the_second_closes() -> None:
    actor = Actor(id="user-1", display_name="Idris", role="owner")
    needs_fix = IssueLifecycle.open("ISS-KEYNOTE-BACKUP").enqueue(
        act=LifecycleAct.FLAG,
        actor=actor,
        basis=Basis.DOCUMENTED,
        evidence_ref="evidence:speaker-plan",
    ).land_reanalysis()

    mitigated = needs_fix.enqueue(
        act=LifecycleAct.FIX,
        actor=actor,
        evidence_ref="artifact:requirements:v4",
    ).land_reanalysis()

    assert mitigated.state is LifecycleState.NEEDS_GROUNDING
    assert mitigated.viability_firm is True
    assert mitigated.statement_grounded is False
    assert [item.act for item in mitigated.attestations] == [
        LifecycleAct.FLAG,
        LifecycleAct.FIX,
    ]

    resolved = mitigated.enqueue(
        act=LifecycleAct.GROUND,
        actor=actor,
        basis=Basis.VENDOR_OR_OWNER_VERIFIED,
        evidence_ref="evidence:speaker-confirmation",
    ).land_reanalysis()

    assert resolved.state is LifecycleState.RESOLVED
    assert resolved.viability_firm is True
    assert resolved.statement_grounded is True
    assert [item.act for item in resolved.attestations] == [
        LifecycleAct.FLAG,
        LifecycleAct.FIX,
        LifecycleAct.GROUND,
    ]


def test_reviewer_reject_is_an_attributed_answered_flag() -> None:
    owner = Actor(id="user-1", display_name="Idris", role="owner")
    reviewer = Actor(id="reviewer-1", display_name="Priya", role="reviewer")
    routed = IssueLifecycle.open("ISS-CATERING-OWNER").route(
        actor=owner,
        reviewer=reviewer,
    )

    assert routed.state is LifecycleState.ROUTED
    assert routed.routed_to == reviewer
    assert routed.attestations[-1].act is LifecycleAct.ROUTE

    addressed = routed.respond_route(
        accepted=False,
        reviewer=reviewer,
        evidence_ref="review-response:reviewer-1",
    )

    assert addressed.state is LifecycleState.ADDRESSED
    assert addressed.attestations[-1].act is LifecycleAct.FLAG
    assert addressed.attestations[-1].actor == reviewer
    assert addressed.attestations[-1].basis is Basis.ANSWERED
    assert basis_strength(Basis.ANSWERED) < basis_strength(Basis.VERIFIED_DIRECTLY)
    assert addressed.land_reanalysis().state is LifecycleState.NEEDS_FIX


def test_withdraw_appends_a_reversal_reopens_and_preserves_activation() -> None:
    actor = Actor(id="user-1", display_name="Idris", role="owner")
    resolved = IssueLifecycle.open(
        "ISS-BUDGET-BUFFER",
        ever_unlocked=True,
    ).enqueue(
        act=LifecycleAct.CONFIRM,
        actor=actor,
        basis=Basis.VERIFIED_DIRECTLY,
        evidence_ref="evidence:finance-ledger",
    ).land_reanalysis()
    original = resolved.attestations[-1]

    withdrawn = resolved.withdraw(actor=actor)

    assert withdrawn.state is LifecycleState.OPEN
    assert withdrawn.needs_reanalysis is True
    assert withdrawn.ever_unlocked is True
    assert withdrawn.attestations[:-1] == resolved.attestations
    assert withdrawn.attestations[-1].act is LifecycleAct.WITHDRAW
    assert withdrawn.attestations[-1].supersedes == original.id
    assert withdrawn.history[-1].event_type == "grounding_act.withdrawn"

    reopened = withdrawn.land_reanalysis()

    assert reopened.state is LifecycleState.OPEN
    assert reopened.needs_reanalysis is False
    assert reopened.pending_act is None
    assert reopened.history[-1].event_type == "issue.reopened"


def test_comment_never_grounds_or_changes_any_lifecycle_band() -> None:
    actor = Actor(id="user-2", display_name="Taimoor", role="member")
    issue = IssueLifecycle.open("ISS-OUTCOME-CHECKPOINT")

    discussed = issue.add_comment(
        actor=actor,
        body="@Idris can you confirm the checkpoint owner?",
    )

    assert discussed.state is LifecycleState.OPEN
    assert discussed.attestations == ()
    assert discussed.grounding_credited is False
    assert discussed.statement_grounded is False
    assert discussed.viability_firm is False
    assert discussed.needs_reanalysis is False
    assert discussed.comments[-1].body.startswith("@Idris")
    assert discussed.history[-1].event_type == "issue.comment_added"

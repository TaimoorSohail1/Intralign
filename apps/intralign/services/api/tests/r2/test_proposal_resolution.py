from oslo_api.analysis.issue_lifecycle import Actor
from oslo_api.analysis.proposals import (
    Proposal,
    ProposalKind,
    ProposalResolution,
    ProposalSurface,
)


def test_build_finding_stays_open_until_every_resolver_lands_via_reanalysis() -> None:
    actor = Actor(id="user-1", display_name="Idris", role="owner")
    resolution = ProposalResolution.start(
        finding_id="ISS-KEYNOTE-BACKUP",
        proposals=(
            Proposal(
                id="proposal-requirement",
                kind=ProposalKind.BUILD,
                resolver_key="requirement",
                title="Add a backup-speaker requirement.",
                rationale="The headline program needs a committed fallback.",
            ),
            Proposal(
                id="proposal-task",
                kind=ProposalKind.BUILD,
                resolver_key="task",
                title="Add a task to confirm the backup speaker.",
                rationale="A requirement without execution ownership is incomplete.",
            ),
        ),
    )

    partial = resolution.accept(
        proposal_id="proposal-requirement",
        actor=actor,
        surface=ProposalSurface.ISSUE_CARD,
    )

    assert partial.finding_resolved is False
    assert partial.land_reanalysis().finding_resolved is False

    complete = partial.accept(
        proposal_id="proposal-task",
        actor=actor,
        surface=ProposalSurface.ARTIFACT,
    )

    assert complete.finding_resolved is False
    assert complete.ready_to_resolve is True
    assert complete.land_reanalysis().finding_resolved is True


def test_inference_and_optional_proposals_are_additive_and_ground_nothing() -> None:
    actor = Actor(id="user-1", display_name="Idris", role="owner")
    resolution = ProposalResolution.start(
        finding_id="ISS-SPONSOR-ASSUMPTION",
        proposals=(
            Proposal(
                id="proposal-inference",
                kind=ProposalKind.INFERENCE,
                resolver_key="sponsor-target-guess",
                title="Use OSLO's inferred sponsor target.",
                rationale="This remains a guess until verified.",
            ),
            Proposal(
                id="proposal-optional",
                kind=ProposalKind.OPTIONAL,
                resolver_key="networking-event",
                title="Add an evening networking event.",
                rationale="This rounds out the plan but is not load-bearing.",
            ),
        ),
    )

    accepted = resolution.accept(
        proposal_id="proposal-inference",
        actor=actor,
        surface=ProposalSurface.FOLDED_READ,
    ).accept(
        proposal_id="proposal-optional",
        actor=actor,
        surface=ProposalSurface.ISSUE_CARD,
    )

    assert accepted.accepted_resolvers == frozenset()
    assert accepted.ready_to_resolve is False
    assert accepted.land_reanalysis().finding_resolved is False


def test_reject_is_an_append_only_decision_and_never_accepts_a_resolver() -> None:
    actor = Actor(id="user-1", display_name="Idris", role="owner")
    resolution = ProposalResolution.start(
        finding_id="ISS-SPONSOR-TARGET",
        proposals=(
            Proposal(
                id="proposal-sponsor-kpi",
                kind=ProposalKind.BUILD,
                resolver_key="sponsor-kpi",
                title="Add a sponsor revenue KPI.",
                rationale="The intent names sponsor funding without a measurable target.",
            ),
        ),
    )

    rejected = resolution.reject(
        proposal_id="proposal-sponsor-kpi",
        actor=actor,
        surface=ProposalSurface.ISSUE_CARD,
    )

    assert rejected.decisions[-1].accepted is False
    assert rejected.accepted_resolvers == frozenset()
    assert rejected.ready_to_resolve is False

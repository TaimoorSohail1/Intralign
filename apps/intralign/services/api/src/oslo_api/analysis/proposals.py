from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from oslo_api.analysis.issue_lifecycle import Actor


class ProposalKind(StrEnum):
    BUILD = "build"
    INFERENCE = "inference"
    OPTIONAL = "optional"


class ProposalSurface(StrEnum):
    ISSUE_CARD = "issue_card"
    ARTIFACT = "artifact"
    FOLDED_READ = "folded_read"


@dataclass(frozen=True, slots=True)
class Proposal:
    id: str
    kind: ProposalKind
    resolver_key: str
    title: str
    rationale: str


@dataclass(frozen=True, slots=True)
class ProposalDecision:
    id: str
    proposal_id: str
    accepted: bool
    actor: Actor
    surface: ProposalSurface
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class ProposalResolution:
    finding_id: str
    proposals: tuple[Proposal, ...]
    decisions: tuple[ProposalDecision, ...] = ()
    accepted_resolvers: frozenset[str] = frozenset()
    finding_resolved: bool = False

    @classmethod
    def start(
        cls,
        *,
        finding_id: str,
        proposals: tuple[Proposal, ...],
    ) -> ProposalResolution:
        if not proposals:
            raise ValueError("FINDING_REQUIRES_ITEMIZED_PROPOSALS")
        if len({proposal.id for proposal in proposals}) != len(proposals):
            raise ValueError("PROPOSAL_IDS_MUST_BE_UNIQUE")
        return cls(finding_id=finding_id, proposals=proposals)

    @property
    def ready_to_resolve(self) -> bool:
        required = {
            proposal.resolver_key
            for proposal in self.proposals
            if proposal.kind is ProposalKind.BUILD
        }
        return bool(required) and required.issubset(self.accepted_resolvers)

    def accept(
        self,
        *,
        proposal_id: str,
        actor: Actor,
        surface: ProposalSurface,
    ) -> ProposalResolution:
        proposal = next(
            (candidate for candidate in self.proposals if candidate.id == proposal_id),
            None,
        )
        if proposal is None:
            raise ValueError("PROPOSAL_NOT_FOUND")
        if self.finding_resolved:
            raise ValueError("FINDING_ALREADY_RESOLVED")
        decision = ProposalDecision(
            id=str(uuid4()),
            proposal_id=proposal.id,
            accepted=True,
            actor=actor,
            surface=surface,
            occurred_at=datetime.now(UTC),
        )
        accepted_resolvers = self.accepted_resolvers
        if proposal.kind is ProposalKind.BUILD:
            accepted_resolvers = accepted_resolvers | {proposal.resolver_key}
        return replace(
            self,
            decisions=(*self.decisions, decision),
            accepted_resolvers=frozenset(accepted_resolvers),
        )

    def reject(
        self,
        *,
        proposal_id: str,
        actor: Actor,
        surface: ProposalSurface,
    ) -> ProposalResolution:
        proposal = next(
            (candidate for candidate in self.proposals if candidate.id == proposal_id),
            None,
        )
        if proposal is None:
            raise ValueError("PROPOSAL_NOT_FOUND")
        if self.finding_resolved:
            raise ValueError("FINDING_ALREADY_RESOLVED")
        decision = ProposalDecision(
            id=str(uuid4()),
            proposal_id=proposal.id,
            accepted=False,
            actor=actor,
            surface=surface,
            occurred_at=datetime.now(UTC),
        )
        return replace(self, decisions=(*self.decisions, decision))

    def land_reanalysis(self) -> ProposalResolution:
        if self.finding_resolved or not self.ready_to_resolve:
            return self
        return replace(self, finding_resolved=True)

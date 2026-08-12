from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class Basis(StrEnum):
    DOCUMENTED = "documented"
    VENDOR_OR_OWNER_VERIFIED = "vendor-or-owner-verified"
    VERIFIED_DIRECTLY = "verified-directly"
    ANSWERED = "answered"


def basis_strength(basis: Basis) -> int:
    return {
        Basis.DOCUMENTED: 1,
        Basis.ANSWERED: 2,
        Basis.VENDOR_OR_OWNER_VERIFIED: 3,
        Basis.VERIFIED_DIRECTLY: 4,
    }[basis]


class LifecycleAct(StrEnum):
    CONFIRM = "confirm"
    ANSWER = "answer"
    FLAG = "flag"
    FIX = "fix"
    GROUND = "ground"
    ROUTE = "route"
    WITHDRAW = "withdraw"


class LifecycleState(StrEnum):
    OPEN = "open"
    ADDRESSED = "addressed"
    ROUTED = "routed"
    NEEDS_FIX = "needs_fix"
    NEEDS_GROUNDING = "needs_grounding"
    RESOLVED = "resolved"


@dataclass(frozen=True, slots=True)
class Actor:
    id: str
    display_name: str
    role: str


@dataclass(frozen=True, slots=True)
class Attestation:
    id: str
    issue_id: str
    act: LifecycleAct
    actor: Actor
    basis: Basis | None
    evidence_ref: str | None
    created_at: datetime
    supersedes: str | None = None


@dataclass(frozen=True, slots=True)
class LifecycleEvent:
    event_type: str
    occurred_at: datetime
    attestation_id: str | None = None


@dataclass(frozen=True, slots=True)
class Comment:
    id: str
    issue_id: str
    actor: Actor
    body: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class IssueLifecycle:
    issue_id: str
    state: LifecycleState
    attestations: tuple[Attestation, ...] = ()
    history: tuple[LifecycleEvent, ...] = ()
    pending_act: LifecycleAct | None = None
    grounding_credited: bool = False
    statement_grounded: bool = False
    viability_firm: bool = False
    routed_to: Actor | None = None
    needs_reanalysis: bool = False
    ever_unlocked: bool = False
    comments: tuple[Comment, ...] = ()

    @classmethod
    def open(cls, issue_id: str, *, ever_unlocked: bool = False) -> IssueLifecycle:
        return cls(
            issue_id=issue_id,
            state=LifecycleState.OPEN,
            ever_unlocked=ever_unlocked,
        )

    def enqueue(
        self,
        *,
        act: LifecycleAct,
        actor: Actor,
        basis: Basis | None = None,
        evidence_ref: str | None = None,
    ) -> IssueLifecycle:
        basis_required = {
            LifecycleAct.ANSWER,
            LifecycleAct.CONFIRM,
            LifecycleAct.GROUND,
        }
        if act in basis_required and basis is None:
            raise ValueError(f"{act.value.upper()}_REQUIRES_BASIS")
        if self.state is LifecycleState.RESOLVED:
            raise ValueError("RESOLVED_ISSUE_IS_NOT_ACTIONABLE")
        if act is LifecycleAct.GROUND and self.state is not LifecycleState.NEEDS_GROUNDING:
            raise ValueError("GROUND_REQUIRES_MITIGATED_ISSUE")
        if act is LifecycleAct.FIX and self.state not in {
            LifecycleState.OPEN,
            LifecycleState.NEEDS_FIX,
        }:
            raise ValueError("FIX_REQUIRES_OPEN_OR_NEEDS_FIX_ISSUE")
        attestation = Attestation(
            id=str(uuid4()),
            issue_id=self.issue_id,
            act=act,
            actor=actor,
            basis=basis,
            evidence_ref=evidence_ref,
            created_at=datetime.now(UTC),
        )
        return replace(
            self,
            state=LifecycleState.ADDRESSED,
            attestations=(*self.attestations, attestation),
            history=(
                *self.history,
                LifecycleEvent(
                    event_type={
                        LifecycleAct.CONFIRM: "grounding_act.confirmed",
                        LifecycleAct.ANSWER: "grounding_act.answered",
                        LifecycleAct.FLAG: "grounding_act.flagged",
                        LifecycleAct.FIX: "grounding_act.fix_applied",
                        LifecycleAct.GROUND: "grounding_act.grounded",
                        LifecycleAct.ROUTE: "grounding_act.routed",
                        LifecycleAct.WITHDRAW: "grounding_act.withdrawn",
                    }[act],
                    occurred_at=attestation.created_at,
                    attestation_id=attestation.id,
                ),
            ),
            pending_act=act,
            needs_reanalysis=True,
        )

    def route(self, *, actor: Actor, reviewer: Actor) -> IssueLifecycle:
        if self.state is not LifecycleState.OPEN:
            raise ValueError("ONLY_OPEN_ISSUES_CAN_BE_ROUTED")
        attestation = Attestation(
            id=str(uuid4()),
            issue_id=self.issue_id,
            act=LifecycleAct.ROUTE,
            actor=actor,
            basis=None,
            evidence_ref=None,
            created_at=datetime.now(UTC),
        )
        return replace(
            self,
            state=LifecycleState.ROUTED,
            routed_to=reviewer,
            attestations=(*self.attestations, attestation),
            history=(
                *self.history,
                LifecycleEvent(
                    event_type="grounding_act.routed",
                    occurred_at=attestation.created_at,
                    attestation_id=attestation.id,
                ),
            ),
            needs_reanalysis=False,
        )

    def respond_route(
        self,
        *,
        accepted: bool,
        reviewer: Actor,
        evidence_ref: str,
    ) -> IssueLifecycle:
        if self.state is not LifecycleState.ROUTED or self.routed_to is None:
            raise ValueError("ISSUE_IS_NOT_AWAITING_REVIEW")
        if reviewer.id != self.routed_to.id:
            raise ValueError("REVIEWER_DOES_NOT_MATCH_ROUTE")
        return replace(self, state=LifecycleState.OPEN, routed_to=None).enqueue(
            act=LifecycleAct.ANSWER if accepted else LifecycleAct.FLAG,
            actor=reviewer,
            basis=Basis.ANSWERED,
            evidence_ref=evidence_ref,
        )

    def withdraw(self, *, actor: Actor) -> IssueLifecycle:
        if self.state is LifecycleState.OPEN or not self.attestations:
            raise ValueError("ISSUE_HAS_NO_LIVE_ACT_TO_WITHDRAW")
        prior = self.attestations[-1]
        reversal = Attestation(
            id=str(uuid4()),
            issue_id=self.issue_id,
            act=LifecycleAct.WITHDRAW,
            actor=actor,
            basis=None,
            evidence_ref=None,
            created_at=datetime.now(UTC),
            supersedes=prior.id,
        )
        return replace(
            self,
            state=LifecycleState.OPEN,
            attestations=(*self.attestations, reversal),
            history=(
                *self.history,
                LifecycleEvent(
                    event_type="grounding_act.withdrawn",
                    occurred_at=reversal.created_at,
                    attestation_id=reversal.id,
                ),
            ),
            pending_act=LifecycleAct.WITHDRAW,
            grounding_credited=False,
            statement_grounded=False,
            viability_firm=(
                False if self.state is LifecycleState.NEEDS_GROUNDING else self.viability_firm
            ),
            routed_to=None,
            needs_reanalysis=True,
        )

    def add_comment(self, *, actor: Actor, body: str) -> IssueLifecycle:
        normalized = body.strip()
        if not normalized:
            raise ValueError("COMMENT_BODY_REQUIRED")
        comment = Comment(
            id=str(uuid4()),
            issue_id=self.issue_id,
            actor=actor,
            body=normalized,
            created_at=datetime.now(UTC),
        )
        return replace(
            self,
            comments=(*self.comments, comment),
            history=(
                *self.history,
                LifecycleEvent(
                    event_type="issue.comment_added",
                    occurred_at=comment.created_at,
                ),
            ),
        )

    def land_reanalysis(self) -> IssueLifecycle:
        if self.state is LifecycleState.OPEN and self.pending_act is LifecycleAct.WITHDRAW:
            return replace(
                self,
                history=(
                    *self.history,
                    LifecycleEvent(event_type="issue.reopened", occurred_at=datetime.now(UTC)),
                ),
                pending_act=None,
                needs_reanalysis=False,
            )
        if self.state is not LifecycleState.ADDRESSED or self.pending_act is None:
            return self
        if self.pending_act is LifecycleAct.FLAG:
            return replace(
                self,
                state=LifecycleState.NEEDS_FIX,
                grounding_credited=True,
                history=(
                    *self.history,
                    LifecycleEvent(event_type="issue.needs_fix", occurred_at=datetime.now(UTC)),
                ),
                pending_act=None,
                needs_reanalysis=False,
            )
        if self.pending_act is LifecycleAct.FIX:
            return replace(
                self,
                state=LifecycleState.NEEDS_GROUNDING,
                statement_grounded=False,
                viability_firm=True,
                history=(
                    *self.history,
                    LifecycleEvent(
                        event_type="issue.needs_grounding",
                        occurred_at=datetime.now(UTC),
                    ),
                ),
                pending_act=None,
                needs_reanalysis=False,
            )
        return replace(
            self,
            state=LifecycleState.RESOLVED,
            grounding_credited=True,
            statement_grounded=True,
            history=(
                *self.history,
                LifecycleEvent(event_type="issue.resolved", occurred_at=datetime.now(UTC)),
            ),
            pending_act=None,
            needs_reanalysis=False,
        )

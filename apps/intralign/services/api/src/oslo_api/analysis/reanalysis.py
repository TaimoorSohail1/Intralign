from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

ReanalysisPassKind = Literal["fast", "deep"]
ReanalysisTrigger = Literal["batch", "explicit", "deep_supersede"]
ReadFreshnessState = Literal["fresh", "stale", "reanalyzing"]
GROUNDING_ACT_KINDS = frozenset({"confirm", "flag", "route"})


@dataclass(frozen=True, slots=True)
class PendingChange:
    event_id: str
    project_id: UUID
    change_kind: str
    scope: str
    occurred_at: datetime
    requires_deep_pass: bool = False


@dataclass(frozen=True, slots=True)
class ReanalysisBatch:
    project_id: UUID
    changes: tuple[PendingChange, ...]
    pass_kind: ReanalysisPassKind
    trigger: ReanalysisTrigger

    @classmethod
    def start(cls, change: PendingChange) -> ReanalysisBatch:
        return cls(
            project_id=change.project_id,
            changes=(change,),
            pass_kind="deep" if change.requires_deep_pass else "fast",
            trigger="batch",
        )

    @property
    def event_ids(self) -> tuple[str, ...]:
        return tuple(change.event_id for change in self.changes)

    @property
    def scopes(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(change.scope for change in self.changes))

    def add(self, change: PendingChange) -> ReanalysisBatch:
        if change.project_id != self.project_id:
            raise ValueError("A reanalysis batch cannot cross project boundaries")
        changes = self.changes + (change,)
        return ReanalysisBatch(
            project_id=self.project_id,
            changes=changes,
            pass_kind=(
                "deep"
                if self.pass_kind == "deep" or change.requires_deep_pass
                else "fast"
            ),
            trigger=self.trigger,
        )


@dataclass(frozen=True, slots=True)
class ReadFreshness:
    project_id: UUID
    state: ReadFreshnessState
    based_on_run_id: str
    pending_event_ids: tuple[str, ...] = ()
    active_run_id: str | None = None

    @classmethod
    def fresh(cls, *, project_id: UUID, based_on_run_id: str) -> ReadFreshness:
        return cls(
            project_id=project_id,
            state="fresh",
            based_on_run_id=based_on_run_id,
        )

    def enqueue(self, event_id: str) -> ReadFreshness:
        pending = tuple(dict.fromkeys((*self.pending_event_ids, event_id)))
        return ReadFreshness(
            project_id=self.project_id,
            state="stale",
            based_on_run_id=self.based_on_run_id,
            pending_event_ids=pending,
            active_run_id=self.active_run_id,
        )

    def start_reanalysis(self, run_id: str) -> ReadFreshness:
        if not self.pending_event_ids:
            raise ValueError("Reanalysis cannot start without a pending change")
        return ReadFreshness(
            project_id=self.project_id,
            state="reanalyzing",
            based_on_run_id=self.based_on_run_id,
            pending_event_ids=self.pending_event_ids,
            active_run_id=run_id,
        )

    def land(
        self,
        *,
        run_id: str,
        consumed_event_ids: tuple[str, ...],
    ) -> ReadFreshness:
        if self.active_run_id != run_id:
            raise ValueError("Only the active reanalysis run can land the read")
        consumed = set(consumed_event_ids)
        remaining = tuple(
            event_id for event_id in self.pending_event_ids if event_id not in consumed
        )
        return ReadFreshness(
            project_id=self.project_id,
            state="stale" if remaining else "fresh",
            based_on_run_id=run_id,
            pending_event_ids=remaining,
            active_run_id=None,
        )


@dataclass(frozen=True, slots=True)
class FirstRunState:
    first_run: bool
    grounding_act_count: int
    ever_unlocked: bool
    unlock_threshold: int = 2

    @property
    def freeze_on(self) -> bool:
        return (
            self.first_run
            and self.grounding_act_count < self.unlock_threshold
            and not self.ever_unlocked
        )

    def record_act(self, act_kind: str) -> FirstRunState:
        if act_kind not in GROUNDING_ACT_KINDS:
            return self
        next_count = self.grounding_act_count + 1
        return FirstRunState(
            first_run=self.first_run,
            grounding_act_count=next_count,
            ever_unlocked=self.ever_unlocked or next_count >= self.unlock_threshold,
            unlock_threshold=self.unlock_threshold,
        )

    def withdraw_act(self, act_kind: str) -> FirstRunState:
        if act_kind not in GROUNDING_ACT_KINDS:
            return self
        return FirstRunState(
            first_run=self.first_run,
            grounding_act_count=max(0, self.grounding_act_count - 1),
            ever_unlocked=self.ever_unlocked,
            unlock_threshold=self.unlock_threshold,
        )

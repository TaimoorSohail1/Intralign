"""Run / resume entrypoint for orchestration graphs — durable, coalesced (IC-WA-00R).

The single seam transport calls into. ``submit_trigger`` is the backbone entry:
it validates the trigger (A3.2/A4.6 — rejection happens BEFORE anything moves),
marks the project stale (Current/Failed -> Stale, evented), then executes the
named graph durably (thread_id = run id; Supabase-Postgres checkpointer by
default). ``run`` is the lower-level durable execute/resume seam — invoking it
again with the same ``thread_id`` resumes from the checkpoint.

Coalescing (locked decision; DL-046 Deep Pass is coalesced): a trigger arriving
while a project is Reanalyzing marks it stale-again and queues AT MOST ONE
follow-up — a later arrival REPLACES the queued one (no unbounded queue). The
guard is an in-memory per-process dict keyed by project_id for this increment;
the multi-dyno guard (Redis) is the flagged Phase-II-A follow-up.

OSLO never self-accepts and never autonomously applies a SuggestedFix — the
runner produces Derived output only; canonical writes happen inside the retain
responsibility (append-only CognitionHistoryRecord).
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass

from backend.orchestration import registry
from backend.orchestration.checkpointer import build_checkpointer
from backend.orchestration.stages import StageFn
from backend.orchestration.state import GraphState
from backend.responsibilities.adapt.states import CognitionState, CognitionStateMachine
from backend.responsibilities.adapt.triggers import TriggerClaim, validate_trigger
from backend.services.observability.emitters import ObservedEventEmitter
from backend.services.observability.events import CollectingEventEmitter, EventEmitter


class CoalescingGuard:
    """At-most-one queued follow-up per project (in-memory; Redis is Phase II-A)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._active: set[str] = set()
        self._queued: dict[str, TriggerClaim] = {}

    def try_acquire(self, project_id: str) -> bool:
        """Claim the project for a run; False when it is already Reanalyzing."""
        with self._lock:
            if project_id in self._active:
                return False
            self._active.add(project_id)
            return True

    def queue_followup(self, project_id: str, claim: TriggerClaim) -> None:
        """Mark stale-again: keep ONE pending follow-up (newest replaces)."""
        with self._lock:
            self._queued[project_id] = claim

    def release(self, project_id: str) -> TriggerClaim | None:
        """Free the project and hand back the single queued follow-up, if any."""
        with self._lock:
            self._active.discard(project_id)
            return self._queued.pop(project_id, None)


_GUARD = CoalescingGuard()


def reset_coalescing_guard() -> None:
    """Replace the process-wide guard (test isolation seam)."""
    global _GUARD
    _GUARD = CoalescingGuard()


@dataclass
class RunOutcome:
    """What a submitted trigger produced: a run, a failure, or a queued mark."""

    status: str  # "completed" | "failed" | "queued"
    state: GraphState | None = None
    followup: RunOutcome | None = None


def run(
    graph_name: str,
    state: GraphState | None,
    *,
    thread_id: str | None = None,
    checkpointer: object | None = None,
    emitter: EventEmitter | None = None,
    chr_repo: object | None = None,
    stages: dict[str, StageFn] | None = None,
    interrupt_before: list[str] | None = None,
) -> GraphState:
    """Execute a registered graph durably; same ``thread_id`` again = resume.

    ``state=None`` resumes the checkpointed run identified by ``thread_id``.
    The checkpointer defaults to the durable Supabase-Postgres saver
    (durable-by-default); run lifecycle events go through the same A6 seam.
    """
    # DTM-0006 (C2): observe the seam — structured log + OTel span events.
    # ObservedEventEmitter.wrap is idempotent and DELEGATES to the given
    # emitter, so a caller's CollectingEventEmitter still collects.
    seam = ObservedEventEmitter.wrap(
        emitter if emitter is not None else CollectingEventEmitter()
    )
    saver = checkpointer if checkpointer is not None else build_checkpointer()
    factory = registry.get(graph_name)
    graph = factory(
        checkpointer=saver,
        emitter=seam,
        chr_repo=chr_repo,
        stages=stages,
        interrupt_before=interrupt_before,
    )

    tid = thread_id or (state.run_id if state is not None else None)
    if tid is None:
        tid = str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}

    seam.emit(
        "recompute_started",
        {
            "project_id": state.project_id if state is not None else None,
            "run_id": tid,
            "graph": graph_name,
            "resumed": state is None,
        },
    )
    result = graph.invoke(state, config)
    final = GraphState.model_validate(result)

    if final.failure is None and final.cognition_state == CognitionState.CURRENT.value:
        seam.emit(
            "recompute_completed",
            {
                "project_id": final.project_id,
                "run_id": tid,
                "appended_chr_ids": list(final.appended_chr_ids),
                "live_projection_ref": final.live_projection_ref,
            },
        )
    # A failed run already emitted recompute_failed from the mark_failed node;
    # an interrupted run emits nothing further until resumed.
    return final


def submit_trigger(
    graph_name: str,
    trigger: TriggerClaim | dict,
    *,
    base_state: GraphState | None = None,
    checkpointer: object | None = None,
    emitter: EventEmitter | None = None,
    chr_repo: object | None = None,
    stages: dict[str, StageFn] | None = None,
) -> RunOutcome:
    """Backbone entry: validate -> mark stale -> durable Deep Pass run (coalesced).

    Raises a TriggerValidationError BEFORE any event or state move when the
    trigger is invalid (A3.2) or carries no information-change claim (A4.6).
    Returns ``status="queued"`` when the project is already Reanalyzing —
    stale-again is marked and AT MOST ONE follow-up stays queued; the follow-up
    runs (and is reported on the outcome) after the active run finishes.
    """
    # DTM-0006 (C2): same observed seam as run() — wrap is idempotent, so the
    # seam handed down to run() is not double-observed.
    seam = ObservedEventEmitter.wrap(
        emitter if emitter is not None else CollectingEventEmitter()
    )
    claim = validate_trigger(trigger)  # rejection path: nothing emitted, nothing runs
    project_id = claim.project_id

    if not _GUARD.try_acquire(project_id):
        _GUARD.queue_followup(project_id, claim)
        seam.emit(
            "stale_detected",
            {
                "project_id": project_id,
                "trigger": claim.trigger_type.value,
                "coalesced": True,  # arrived while Reanalyzing: stale-again mark
            },
        )
        return RunOutcome(status="queued")

    queued: TriggerClaim | None = None
    try:
        run_id = str(uuid.uuid4())
        initial = (
            CognitionState(base_state.cognition_state)
            if base_state is not None and base_state.cognition_state is not None
            else CognitionState.CURRENT
        )
        seam.emit(
            "stale_detected",
            {
                "project_id": project_id,
                "trigger": claim.trigger_type.value,
                "coalesced": False,
            },
        )
        machine = CognitionStateMachine(project_id, initial, seam)
        machine.transition(
            CognitionState.STALE, run_id=run_id, reason=claim.trigger_type.value
        )
        seam.emit(
            "reanalysis_triggered",
            {
                "project_id": project_id,
                "run_id": run_id,
                "trigger": claim.trigger_type.value,
                "source": claim.source,
            },
        )
        state = GraphState(
            project_id=project_id,
            run_id=run_id,
            trigger=claim.model_dump(mode="json"),
            emissions=list(claim.emissions),
            cognition_state=machine.state.value,
            live_projection_ref=(
                base_state.live_projection_ref if base_state is not None else None
            ),
        )
        final = run(
            graph_name,
            state,
            thread_id=run_id,
            checkpointer=checkpointer,
            emitter=seam,
            chr_repo=chr_repo,
            stages=stages,
        )
    finally:
        queued = _GUARD.release(project_id)

    followup: RunOutcome | None = None
    if queued is not None:
        followup = submit_trigger(
            graph_name,
            queued,
            base_state=final,
            checkpointer=checkpointer,
            emitter=seam,
            chr_repo=chr_repo,
            stages=stages,
        )

    status = "failed" if final.failure is not None else "completed"
    return RunOutcome(status=status, state=final, followup=followup)

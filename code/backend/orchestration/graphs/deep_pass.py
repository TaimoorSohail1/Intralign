"""Deep Pass — the IC-WA-00R recompute backbone as a durable LangGraph StateGraph.

Topology (wiring only — every node is THIN and delegates to adapt/perceive/
retain functions or an injected chain stage):

    START -> validate_trigger -> mark_reanalyzing
          -> append_chrs (the REAL injected ``retain`` stage: one CHR per
             emission via retain.ChrRepository — chain head per A3.3
             Retain -> Infer -> Evaluate -> Advise)
          -> stage_infer -> stage_evaluate -> stage_advise   (injected; Wave B/C
             placeholders in Phase II-A — no cognition, A4.3)
          -> mark_current  (live projection replaced, A3.4)        on success
          -> mark_failed   (last-known-good RETAINED, A3.7;        on failure
                            recompute_failed emitted)
          -> END

A stage failure is captured into ``state.failure`` (never swallowed) so the
failure edge routes to ``mark_failed``; downstream stages skip themselves. The
state machine moves live in the ``mark_*`` nodes (adapt.CognitionStateMachine —
every transition evented through the seam, A6/A7).
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from backend.orchestration import registry
from backend.orchestration.stages import (
    CHAIN_STAGE_ORDER,
    StageContext,
    StageFn,
    default_stages,
)
from backend.orchestration.state import GraphState
from backend.responsibilities.adapt.states import CognitionState, CognitionStateMachine
from backend.responsibilities.adapt.triggers import validate_trigger
from backend.responsibilities.retain import ChrRepository
from backend.services.observability.events import CollectingEventEmitter, EventEmitter

GRAPH_NAME = "deep_pass"


def build_deep_pass_graph(
    *,
    checkpointer: object | None = None,
    emitter: EventEmitter | None = None,
    chr_repo: ChrRepository | None = None,
    stages: dict[str, StageFn] | None = None,
    interrupt_before: list[str] | None = None,
):
    """Compile the Deep Pass graph with its wiring injected.

    Args:
        checkpointer: LangGraph saver (durable Postgres by default — runner).
        emitter: the A6 event seam; defaults to a collecting emitter.
        chr_repo: DTM-0004 append-only repository the retain stage writes through.
        stages: chain-stage overrides merged over the registered defaults
            (locked decision #6 — stages are injected, never implemented here).
        interrupt_before: compile-time breakpoint(s) — test-only knob used to
            simulate interruption for durable-resume proof.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    chain: dict[str, StageFn] = {**default_stages(), **(stages or {})}
    missing = [name for name in CHAIN_STAGE_ORDER if name not in chain]
    if missing:
        raise ValueError(f"chain stages missing from registry: {missing}")
    ctx = StageContext(emitter=seam, chr_repo=chr_repo)

    def _machine(state: GraphState) -> CognitionStateMachine:
        if state.cognition_state is None:
            raise ValueError(
                "deep_pass requires state marked 'stale' before the run "
                "(runner.submit_trigger does this) — cognition_state is None"
            )
        return CognitionStateMachine(
            project_id=state.project_id,
            state=CognitionState(state.cognition_state),
            emitter=seam,
        )

    def validate_trigger_node(state: GraphState) -> dict[str, Any]:
        """Re-validate the trigger claim (A3.2/A4.6) — defense inside the run."""
        if state.trigger is None:
            raise ValueError("deep_pass started without a trigger claim (A3.2)")
        validate_trigger(state.trigger)
        return {}

    def mark_reanalyzing(state: GraphState) -> dict[str, Any]:
        machine = _machine(state)
        machine.transition(
            CognitionState.REANALYZING,
            run_id=state.run_id,
            reason=(state.trigger or {}).get("trigger_type"),
        )
        return {"cognition_state": machine.state.value}

    def _run_stage(name: str, state: GraphState) -> dict[str, Any]:
        """Execute one injected chain stage; capture failure for the A7 edge."""
        if state.failure is not None:
            return {}  # short-circuit to the failure edge
        try:
            return chain[name](state, ctx) or {}
        except Exception as exc:  # noqa: BLE001 — failure edge, never swallowed
            return {
                "failure": {
                    "stage": name,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            }

    def append_chrs(state: GraphState) -> dict[str, Any]:
        """Chain head: the REAL retain stage (one CHR per emission, A3.5)."""
        return _run_stage("retain", state)

    def stage_infer(state: GraphState) -> dict[str, Any]:
        return _run_stage("infer", state)

    def stage_evaluate(state: GraphState) -> dict[str, Any]:
        return _run_stage("evaluate", state)

    def stage_advise(state: GraphState) -> dict[str, Any]:
        return _run_stage("advise", state)

    def mark_current(state: GraphState) -> dict[str, Any]:
        """Success: Reanalyzing -> Current'; live Derived projection replaced (A3.4)."""
        machine = _machine(state)
        machine.transition(CognitionState.CURRENT, run_id=state.run_id)
        return {
            "cognition_state": machine.state.value,
            "live_projection_ref": {
                "chr_ids": list(state.appended_chr_ids),
                "run_id": state.run_id,
            },
        }

    def mark_failed(state: GraphState) -> dict[str, Any]:
        """Failure: Reanalyzing -> Failed; last-known-good RETAINED (A3.7).

        ``live_projection_ref`` is deliberately NOT touched — the previous live
        projection reference survives the failed run. History stays uncorrupted
        (nothing appended here, nothing ever overwritten).
        """
        machine = _machine(state)
        machine.transition(
            CognitionState.FAILED,
            run_id=state.run_id,
            reason=(state.failure or {}).get("error_type"),
        )
        seam.emit(
            "recompute_failed",
            {
                "project_id": state.project_id,
                "run_id": state.run_id,
                "failure": state.failure,
                "last_known_good_retained": True,
            },
        )
        return {"cognition_state": machine.state.value}

    def route_outcome(state: GraphState) -> str:
        return "mark_failed" if state.failure is not None else "mark_current"

    graph = StateGraph(GraphState)
    graph.add_node("validate_trigger", validate_trigger_node)
    graph.add_node("mark_reanalyzing", mark_reanalyzing)
    graph.add_node("append_chrs", append_chrs)
    graph.add_node("stage_infer", stage_infer)
    graph.add_node("stage_evaluate", stage_evaluate)
    graph.add_node("stage_advise", stage_advise)
    graph.add_node("mark_current", mark_current)
    graph.add_node("mark_failed", mark_failed)

    graph.add_edge(START, "validate_trigger")
    graph.add_edge("validate_trigger", "mark_reanalyzing")
    graph.add_edge("mark_reanalyzing", "append_chrs")
    graph.add_edge("append_chrs", "stage_infer")
    graph.add_edge("stage_infer", "stage_evaluate")
    graph.add_edge("stage_evaluate", "stage_advise")
    graph.add_conditional_edges(
        "stage_advise", route_outcome, ["mark_current", "mark_failed"]
    )
    graph.add_edge("mark_current", END)
    graph.add_edge("mark_failed", END)

    return graph.compile(
        checkpointer=checkpointer, interrupt_before=interrupt_before or None
    )


# Register in the named-graph index (looked up lazily by registry.get).
if GRAPH_NAME not in registry.GRAPHS:
    registry.register(GRAPH_NAME, build_deep_pass_graph)

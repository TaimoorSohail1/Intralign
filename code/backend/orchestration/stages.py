"""Chain-stage registry — Retain -> Infer -> Evaluate -> Advise stages are INJECTED.

Locked decision #6 (deep-task-decisions): the backbone re-runs a REGISTERED
chain; it never implements cognition. Phase II-A registers:

- ``retain`` — REAL: appends one CognitionHistoryRecord per emission handed to
  it via DTM-0004's append-only ``ChrRepository`` (A3.5). Thin wiring — the
  canonical write lives in the retain responsibility.
- ``infer`` / ``evaluate`` — WAVE_B_PLACEHOLDER no-op pass-throughs.
- ``advise`` — WAVE_C_PLACEHOLDER no-op pass-through.

Placeholders return their input unchanged and PRODUCE NO COGNITION (A4.3): no
findings, no scores, no emissions, no events. Waves B/C replace them through
this same registry without touching the graph topology.

A stage is ``Callable[[GraphState, StageContext], dict]`` returning the state
UPDATES it produces (``{}`` = pass-through).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from backend.orchestration.state import GraphState
from backend.responsibilities.retain import ChrRepository, CognitionHistoryRecord
from backend.services.observability.events import EventEmitter
from backend.services.observability.langsmith_linkage import langsmith_run_linkage

# Contract chain order (IC-WA-00R A3.3).
CHAIN_STAGE_ORDER: tuple[str, ...] = ("retain", "infer", "evaluate", "advise")


@dataclass(frozen=True)
class StageContext:
    """Wiring handed to a stage: the event seam and the retain repository."""

    emitter: EventEmitter
    chr_repo: ChrRepository | None = None


StageFn = Callable[[GraphState, StageContext], dict[str, Any]]


def retain_stage(state: GraphState, ctx: StageContext) -> dict[str, Any]:
    """REAL retain stage — append one CHR per emission handed to it (A3.5).

    Canonical writes go ONLY through ``ChrRepository.append`` (append-only;
    one-way flow, A4.4/A4.5). Emits ``cognition_history_record_appended`` per
    receipt (A6). With placeholder stages downstream, a recompute run appends
    exactly one CHR per emission declared in the trigger payload (zero if none).
    """
    if not state.emissions:
        return {"appended_chr_ids": []}
    if ctx.chr_repo is None:
        raise RuntimeError(
            "retain stage needs a ChrRepository — emissions were declared but "
            "no repository was wired (orchestration builds the graph with one)"
        )
    trigger = state.trigger or {}
    # DTM-0006 / DL-054 cond.1: when LANGSMITH_TRACING=true and a run id
    # exists, the appended CHR carries langsmith_run_id inside
    # model_or_rule_version (additive merge; provider/model identity wins on
    # collision). {} when tracing is off / no run id — dev-allowed (A3).
    linkage = langsmith_run_linkage(state.run_id)
    appended: list[str] = []
    for spec in state.emissions:
        if linkage:
            spec = {
                **spec,
                "model_or_rule_version": {
                    **linkage,
                    **spec.get("model_or_rule_version", {}),
                },
            }
        record = CognitionHistoryRecord(
            project_id=state.project_id,
            recompute_trigger=trigger.get("trigger_type"),
            **spec,
        )
        persisted = ctx.chr_repo.append(record)
        appended.append(str(persisted.chr_id))
        ctx.emitter.emit(
            "cognition_history_record_appended",
            {
                "project_id": state.project_id,
                "run_id": state.run_id,
                "chr_id": str(persisted.chr_id),
                "output_kind": persisted.output_kind,
                "supersedes_chr_id": (
                    str(persisted.supersedes_chr_id)
                    if persisted.supersedes_chr_id
                    else None
                ),
            },
        )
    return {"appended_chr_ids": appended}


def wave_b_placeholder_infer(state: GraphState, ctx: StageContext) -> dict[str, Any]:
    """WAVE_B_PLACEHOLDER — Infer does not exist until Wave B.

    No-op pass-through: returns the input unchanged and produces NO cognition
    (A4.3) — no findings, no emissions, no events. Replaced via the stage
    registry by the Wave B Infer responsibility.
    """
    return {}


def wave_b_placeholder_evaluate(state: GraphState, ctx: StageContext) -> dict[str, Any]:
    """WAVE_B_PLACEHOLDER — Evaluate does not exist until Wave B.

    No-op pass-through: returns the input unchanged and produces NO cognition
    (A4.3) — no scores, no confidence, no events. Replaced via the stage
    registry by the Wave B Evaluate responsibility.
    """
    return {}


def wave_c_placeholder_advise(state: GraphState, ctx: StageContext) -> dict[str, Any]:
    """WAVE_C_PLACEHOLDER — Advise does not exist until Wave C.

    No-op pass-through: returns the input unchanged and produces NO cognition
    (A4.3) — no recommendations, no events. Replaced via the stage registry by
    the Wave C Advise responsibility.
    """
    return {}


# The Phase II-A registry content (locked decision #6).
_DEFAULT_STAGES: dict[str, StageFn] = {
    "retain": retain_stage,
    "infer": wave_b_placeholder_infer,
    "evaluate": wave_b_placeholder_evaluate,
    "advise": wave_c_placeholder_advise,
}


def default_stages() -> dict[str, StageFn]:
    """A fresh copy of the registered chain stages (safe to override per run)."""
    return dict(_DEFAULT_STAGES)


def register_stage(name: str, stage: StageFn) -> None:
    """Register/replace a chain stage (how Waves B/C inject the real owners)."""
    if name not in CHAIN_STAGE_ORDER:
        raise ValueError(
            f"unknown chain stage {name!r} — the chain is exactly "
            f"{' -> '.join(CHAIN_STAGE_ORDER)} (A3.3)"
        )
    _DEFAULT_STAGES[name] = stage

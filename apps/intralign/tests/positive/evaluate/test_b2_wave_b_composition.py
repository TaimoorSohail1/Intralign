"""QA-WB-EVAL B2 — the Wave-B composition (Part B) exercised OFFLINE.

Proves the composed `infer` stage (synthesis → finding, by CALLING the frozen
stage fns) hands its findings + model to the `evaluate` stage over the same run
— WITHOUT a Supabase stack and WITHOUT editing any frozen file. The live durable
end-to-end (with the real graph + Supabase CHR repo) is the env-gated
``test_b2_live_chain_e2e``; this asserts the composition wiring itself.
"""

from __future__ import annotations

from collections import Counter

from backend.orchestration.wave_b import WaveBChain
from backend.responsibilities.evaluate.stage import (
    OUTPUT_KIND_CAF,
    OUTPUT_KIND_OUTCOME_CONFIDENCE,
)
from backend.responsibilities.infer.finding_stage import OUTPUT_KIND_FINDING
from backend.responsibilities.infer.stage import OUTPUT_KIND_SYNTHESIZED_MODEL
from backend.services.llm_provider import LLMProvider
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    response_key_directive,
)
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    PROJECT,
    sample_drafts,
)
from tests.positive.synthesis.fakes import FakeStageContext


class _State:
    """A tiny GraphState stand-in (run_id + project_id + inputs) for the closures."""

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.project_id = PROJECT
        self.inputs = {
            "project_id": PROJECT,
            "assertions": sample_drafts(),
            "assertion_ids": ASSERTION_IDS,
            "declared_outcome": DECLARED_OUTCOME,
            "outcome_anchor": OUTCOME_ANCHOR,
            "input_attestation_version": "v1",
            # The CHR recompute_trigger (LDM §2.2) — the trigger that fired this
            # run; never null (the live wiring carries it from the trigger).
            "recompute_trigger": "knowledge-change",
        }


def _provider() -> LLMProvider:
    syn = build_recorded_model("ws_synthesis_v0")
    fnd = build_recorded_model("wb_infer_v0")

    from pydantic_ai.models.function import FunctionModel

    def fn(messages, info):
        for s in (syn, fnd):
            try:
                return s._function(messages, info)
            except KeyError:
                continue
        return syn._function(messages, info)

    return LLMProvider(recorded_model=FunctionModel(fn, model_name="recorded:wave-b"))


def _chain() -> WaveBChain:
    return WaveBChain(
        provider=_provider(),
        extract_infer_inputs=lambda state: dict(state.inputs),
        tier="free",
        mode="fast",
        confidence_stage="orientation",
        prompt_suffix_for=response_key_directive,
    )


def test_b2_composed_infer_runs_synthesis_then_finding_over_one_run() -> None:
    ctx = FakeStageContext()
    chain = _chain()
    state = _State(run_id="run-1")
    out = chain._infer_stage(state, ctx)
    # Synthesis produced the model AND finding analyzed it — both CHR kinds present.
    assert ctx.chr_repo.rows_for_kind(OUTPUT_KIND_SYNTHESIZED_MODEL)
    assert ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    assert out["outputs"]["finding_ids"]
    assert out["outputs"]["synthesized_planning_model_version"]
    # Both stage fns' events fired (the frozen fns were CALLED, not edited).
    names = Counter(ctx.emitter.names)
    assert names["synthesized_model_updated"] == 1
    assert names["finding_detected"] >= 1


def test_b2_evaluate_stage_reads_the_findings_the_infer_node_produced() -> None:
    ctx = FakeStageContext()
    chain = _chain()
    state = _State(run_id="run-2")
    # infer node first (stashes findings + model for the same run)...
    chain._infer_stage(state, ctx)
    # ...then evaluate node pops them and scores.
    out = chain._evaluate_stage(state, ctx)
    assert ctx.chr_repo.rows_for_kind(OUTPUT_KIND_CAF)
    assert ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)
    assert out["outputs"]["issue_ids"]          # Issues formed from the findings
    assert out["outputs"]["outcome_confidence_band"] in ("low", "medium", "high")
    names = Counter(ctx.emitter.names)
    assert names["issue_generated"] >= 1
    assert names["caf_assessed"] == 1
    assert names["outcome_confidence_computed"] == 1


def test_b2_handoff_is_per_run_and_consumed_once() -> None:
    """The infer→evaluate handoff is keyed by run_id and popped by the evaluate node."""
    ctx = FakeStageContext()
    chain = _chain()
    state = _State(run_id="run-3")
    chain._infer_stage(state, ctx)
    assert "run-3" in chain._handoff           # stashed by infer
    chain._evaluate_stage(state, ctx)
    assert "run-3" not in chain._handoff       # popped by evaluate (no leak)


def test_b2_register_replaces_placeholders_without_topology_change() -> None:
    """register() swaps the placeholders via the registry — no graph edit."""
    from backend.orchestration import stages as stages_mod

    saved = stages_mod.default_stages()
    try:
        chain = _chain()
        chain.register()
        live = stages_mod.default_stages()
        # Bound methods compare by (__func__, __self__) — same underlying chain.
        assert live["infer"].__self__ is chain
        assert live["infer"].__func__ is WaveBChain._infer_stage
        assert live["evaluate"].__self__ is chain
        assert live["evaluate"].__func__ is WaveBChain._evaluate_stage
        # The chain order is untouched (topology unchanged).
        assert stages_mod.CHAIN_STAGE_ORDER == ("retain", "infer", "evaluate", "advise")
    finally:
        for name, fn in saved.items():
            stages_mod.register_stage(name, fn)

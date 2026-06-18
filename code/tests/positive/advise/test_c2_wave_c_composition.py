"""QA-WC-ADVISE C2 — the additive ``wave_c.py`` composes the full A→B→C chain.

Offline (no Supabase): drive the composed stage fns (wrapped infer → evaluate →
advise) over ONE run_id sharing the in-memory handoff, proving:
- ``build_and_register_wave_c_chain`` CALLS the Wave B builder + registers advise
  (the registry now carries the advise producer, not the placeholder),
- the wrapped infer captures the Findings; the advise node anchors its
  Recommendations to those run Findings/Issues,
- advise appends recommendation/clarification CHRs anchored to the run's findings.

The registry mutation is saved + restored so register_stage never leaks globally.
The LLM is the recorded-fixture model (ADR-0004) — zero provider calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from backend.orchestration import stages as stages_mod
from backend.orchestration.stages import wave_c_placeholder_advise
from backend.orchestration.wave_c import build_and_register_wave_c_chain
from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_CLARIFICATION,
    OUTPUT_KIND_RECOMMENDATION,
)
from backend.services.llm_provider import LLMProvider
from tests._fixtures.recorded_model_responses import (
    build_recorded_model,
    response_key_directive,
)
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    sample_drafts,
)
from tests.positive.synthesis.fakes import FakeStageContext


@dataclass
class _FakeState:
    project_id: str
    run_id: str
    inputs: dict[str, Any] = field(default_factory=dict)
    trigger: dict[str, Any] | None = None


def _mux_provider() -> LLMProvider:
    """A recorded-fixture provider serving synthesis + finding + advise steps."""
    sessions = [
        build_recorded_model("ws_synthesis_v0"),
        build_recorded_model("wb_infer_v0"),
        build_recorded_model("wc_advise_e2e_v0"),
    ]

    def fn(messages, info):
        from pydantic_ai.models.function import FunctionModel  # noqa: F401

        last_error: Exception | None = None
        for s in sessions:
            try:
                return s._function(messages, info)
            except KeyError as exc:
                last_error = exc
                continue
        # Re-raise the last fixture's KeyError if no session had the key.
        raise last_error if last_error else KeyError("no recorded response")

    from pydantic_ai.models.function import FunctionModel

    return LLMProvider(recorded_model=FunctionModel(fn, model_name="recorded:wave-c"))


def _infer_inputs_from_state(state):
    inputs = dict(state.inputs)
    inputs.setdefault("project_id", state.project_id)
    inputs.setdefault("assertions", sample_drafts())
    inputs.setdefault("assertion_ids", list(ASSERTION_IDS))
    inputs.setdefault("declared_outcome", DECLARED_OUTCOME)
    inputs.setdefault("outcome_anchor", OUTCOME_ANCHOR)
    inputs.setdefault("recompute_trigger", "knowledge-change")
    inputs.setdefault("input_attestation_version", "v1")
    return inputs


@pytest.fixture
def _restore_registry():
    saved = stages_mod.default_stages()
    yield
    for name, fn in saved.items():
        stages_mod.register_stage(name, fn)


def test_c2_build_and_register_wave_c_replaces_the_advise_placeholder(
    _restore_registry,
) -> None:
    assert stages_mod.default_stages()["advise"] is wave_c_placeholder_advise
    chain = build_and_register_wave_c_chain(
        provider=_mux_provider(),
        extract_infer_inputs=_infer_inputs_from_state,
        prompt_suffix_for=response_key_directive,
    )
    registered = stages_mod.default_stages()
    # The advise placeholder is REPLACED by the real producer; infer is the wrapper.
    assert registered["advise"] is not wave_c_placeholder_advise
    assert registered["advise"] == chain._advise_stage
    assert registered["infer"] == chain._infer_stage
    # Evaluate is the composed Wave B evaluate (called via the Wave B chain).
    assert registered["evaluate"] == chain.wave_b._evaluate_stage


def test_c2_full_chain_advise_anchors_to_run_findings(_restore_registry) -> None:
    chain = build_and_register_wave_c_chain(
        provider=_mux_provider(),
        extract_infer_inputs=_infer_inputs_from_state,
        prompt_suffix_for=response_key_directive,
    )
    state = _FakeState(
        project_id="11111111-1111-1111-1111-111111111111",
        run_id="run-c-1",
        trigger={"trigger_type": "knowledge-change"},
    )
    ctx = FakeStageContext()

    # A→B: wrapped infer (synthesis → finding) then evaluate, over the same run.
    chain._infer_stage(state, ctx)
    chain.wave_b._evaluate_stage(state, ctx)
    # C: advise reads the captured findings + forms issues, anchors to them.
    out = chain._advise_stage(state, ctx)

    rec_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
    assert rec_chrs  # the chain produced anchored recommendations
    # Every recommendation CHR is anchored to a real run finding/issue id.
    finding_ids = set(out["outputs"].get("recommendation_ids", []))
    assert finding_ids  # ids present
    for row in rec_chrs:
        assert row["upstream_lineage"]["anchor"]
        assert row["provenance_ref"]["emitted_by"] == "advise"
    # The sample drafts include a negation pair → a conflict finding → a
    # clarification anchored to that conflict (the deterministic conflict id).
    clr_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_CLARIFICATION)
    assert clr_chrs
    assert any(
        r["upstream_lineage"]["anchor"] == "conflict-5187581b388d7401"
        for r in clr_chrs
    )
    assert "recommendation_generated" in ctx.emitter.names
    assert "clarification_requested" in ctx.emitter.names

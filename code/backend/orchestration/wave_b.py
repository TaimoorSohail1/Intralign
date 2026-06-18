"""Wave B live-chain wiring (DTM-0011 carried integration; ADDITIVE ONLY).

The single `infer` chain node holds ONE stage fn, but Infer now spans synthesis
(DTM-0009) + finding (DTM-0010). This module — the ONLY orchestration write Wave
B authorizes (decisions "Infer-node fusion") — composes a single `infer` stage
that runs synthesis FIRST (producing the `SynthesizedPlanningModel`) THEN finding
(which analyzes that model), by CALLING the frozen stage fns; and builds the
`evaluate` stage (this slice). Both are registered via ``register_stage(...)``.

It does **NOT** edit any frozen file: not `infer/stage.py` (synthesis), not
`infer/finding_stage.py` (finding), not `evaluate/stage.py` (it calls
``run_evaluate_stage``), not `deep_pass.py` / `state.py` / `runner.py` /
`registry.py`. Composition is by *calling* the existing stage fns over the same
run; the graph topology (``append_chrs → stage_infer → stage_evaluate →
stage_advise``) is untouched.

Cross-node handoff (additive, no GraphState change): the graph runs `stage_infer`
and `stage_evaluate` as SEPARATE nodes that each read `state`. The rich Finding /
model objects the infer node produces do not fit the serialized GraphState
cleanly, and `state.py` is READ-ONLY. So the composed infer stage and the
evaluate stage are built as a **closure pair sharing an in-memory, per-run
handoff** keyed by ``run_id`` (``WaveBChain.build``): the infer node stashes the
findings + model it just derived; the evaluate node pops them for the same run.
This is wiring state private to the chain — it changes NO graph topology, NO
GraphState field, and NO frozen module. If a future need required a topology or
GraphState change, that would be a STOP/escalate (it is not needed here).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from backend.orchestration.stages import register_stage
from backend.responsibilities.evaluate.stage import run_evaluate_stage
from backend.responsibilities.evaluate.engine import EvaluateEngine
from backend.responsibilities.infer.finding import FindingEngine
from backend.responsibilities.infer.finding_stage import run_finding_stage
from backend.responsibilities.infer.stage import run_synthesis_stage
from backend.responsibilities.infer.synthesis import SynthesisEngine
from backend.services.llm_provider import LLMProvider
from shared.epistemic import Finding, SynthesizedPlanningModel


@dataclass
class _RunHandoff:
    """The in-memory handoff from the composed infer node to the evaluate node."""

    findings: tuple[Finding, ...]
    model: SynthesizedPlanningModel | None


@dataclass
class WaveBChain:
    """Builds + registers the composed `infer` stage and the `evaluate` stage.

    ``provider`` is the shared LLM seam (a recorded-fixture model offline). The
    two stage fns share ``_handoff`` so the evaluate node reads exactly the
    findings + model the infer node produced for the same ``run_id``.
    """

    provider: LLMProvider
    extract_infer_inputs: Callable[[Any], dict[str, Any]]
    tier: str = "free"
    mode: str = "fast"
    user: str = "anonymous"
    confidence_stage: str = "orientation"
    understanding_state: str = "initial"
    prompt_suffix_for: Any = field(default=None)
    _handoff: dict[str, _RunHandoff] = field(default_factory=dict)

    # -- the composed `infer` stage (synthesis → finding) --------------------

    def _infer_stage(self, state: Any, ctx: Any) -> dict[str, Any]:
        """Run DTM-0009 synthesis THEN DTM-0010 finding over the same run.

        Synthesis produces the model; finding analyzes it. Both append their own
        CHRs through ``ctx.chr_repo`` and emit their own events (the frozen stage
        fns are CALLED, never edited). The findings + model are stashed for the
        evaluate node.
        """
        inputs = self.extract_infer_inputs(state)
        run_key = self._run_key(state)

        synthesis_engine = SynthesisEngine(
            provider=self.provider,
            tier=self.tier,
            mode=self.mode,  # type: ignore[arg-type]
            user=self.user,
            confidence_stage=self.confidence_stage,  # type: ignore[arg-type]
            understanding_state=self.understanding_state,  # type: ignore[arg-type]
            prompt_suffix_for=self.prompt_suffix_for,
        )
        synthesis_result = run_synthesis_stage(
            engine=synthesis_engine,
            project_id=inputs["project_id"],
            assertions=inputs["assertions"],
            assertion_ids=inputs["assertion_ids"],
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            budget=inputs.get("synthesis_budget"),
        )

        finding_engine = FindingEngine(
            provider=self.provider,
            tier=self.tier,
            mode=self.mode,  # type: ignore[arg-type]
            user=self.user,
            confidence_stage=self.confidence_stage,  # type: ignore[arg-type]
            understanding_state=self.understanding_state,  # type: ignore[arg-type]
            prompt_suffix_for=self.prompt_suffix_for,
        )
        finding_result = run_finding_stage(
            engine=finding_engine,
            project_id=inputs["project_id"],
            assertions=inputs["assertions"],
            assertion_ids=inputs["assertion_ids"],
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            model=synthesis_result.model,
            declared_outcome=inputs.get("declared_outcome"),
            outcome_anchor=inputs.get("outcome_anchor"),
            prior_chr_id_for=inputs.get("finding_prior_chr_id_for"),
            budget=inputs.get("finding_budget"),
        )

        # Stash for the evaluate node (same run).
        self._handoff[run_key] = _RunHandoff(
            findings=finding_result.findings, model=synthesis_result.model
        )
        return {
            "outputs": {
                "synthesized_planning_model_version": synthesis_result.model.model_version,
                "generated_artifact_types": [
                    a.artifact_type for a in synthesis_result.artifacts
                ],
                "finding_ids": [f.finding_id for f in finding_result.findings],
                "finding_types": [f.finding_type for f in finding_result.findings],
            }
        }

    # -- the `evaluate` stage (this slice) -----------------------------------

    def _evaluate_stage(self, state: Any, ctx: Any) -> dict[str, Any]:
        """Score the findings the composed infer node just produced (same run)."""
        run_key = self._run_key(state)
        handoff = self._handoff.pop(run_key, _RunHandoff(findings=(), model=None))
        inputs = self.extract_infer_inputs(state)

        engine = EvaluateEngine(
            tier=self.tier,
            mode=self.mode,  # type: ignore[arg-type]
            user=self.user,
            confidence_stage=self.confidence_stage,  # type: ignore[arg-type]
        )
        result = run_evaluate_stage(
            engine=engine,
            project_id=inputs["project_id"],
            findings=handoff.findings,
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            model=handoff.model,
            prior_understanding_state=inputs.get("prior_understanding_state"),
            prior_chr_id_for=inputs.get("evaluate_prior_chr_id_for"),
            tier=self.tier,
            user=self.user,
            mode=self.mode,
        )
        return {
            "outputs": {
                "issue_ids": [i.issue_id for i in result.issues],
                "confidence_band": result.confidence.band,
                "outcome_confidence_band": result.outcome_confidence.band,
                "false_confidence_flagged": result.outcome_confidence.false_confidence_flagged,
                "understanding_state": result.understanding_state,
            }
        }

    @staticmethod
    def _run_key(state: Any) -> str:
        """A stable per-run key for the infer→evaluate handoff (run_id, then project)."""
        run_id = getattr(state, "run_id", None)
        if run_id:
            return str(run_id)
        return str(getattr(state, "project_id", "default"))

    # -- registration --------------------------------------------------------

    def register(self) -> None:
        """Register the composed `infer` + the `evaluate` stage (decision #4).

        Replaces the Wave-B placeholders through the registry — NO graph
        topology change (``register_stage`` only; deep_pass.py untouched).
        """
        register_stage("infer", self._infer_stage)
        register_stage("evaluate", self._evaluate_stage)


def build_and_register_wave_b_chain(
    *,
    provider: LLMProvider,
    extract_infer_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
    prompt_suffix_for: Any = None,
) -> WaveBChain:
    """Build the Wave-B chain and register both stages; return it (test handle).

    Returning the chain lets a caller (or a live e2e test) pass it as a stage
    override too: ``{"infer": chain._infer_stage, "evaluate": chain._evaluate_stage}``.
    """
    chain = WaveBChain(
        provider=provider,
        extract_infer_inputs=extract_infer_inputs,
        tier=tier,
        mode=mode,
        user=user,
        confidence_stage=confidence_stage,
        understanding_state=understanding_state,
        prompt_suffix_for=prompt_suffix_for,
    )
    chain.register()
    return chain

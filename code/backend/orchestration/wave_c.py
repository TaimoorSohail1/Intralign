"""Wave C live-chain wiring (DTM-0014; ADDITIVE ONLY — the full A→B→C chain).

This module composes the full **A→B→C** chain by *calling* the frozen Wave B
chain builder (``build_and_register_wave_b_chain`` — synthesis → finding →
evaluate) and ADDING the ``advise`` stage. Both are registered via
``register_stage(...)`` (decision #2). It does **NOT** edit any frozen file: not
``wave_b.py`` (it CALLS its builder + reuses the composed infer/evaluate stage
fns), not ``deep_pass.py`` topology (which already has a ``stage_advise`` node),
not ``state.py`` / ``runner.py`` / ``registry.py`` / ``stages.py`` (only
``register_stage`` is used).

Cross-node handoff (additive, no GraphState change — mirroring the Wave B
``_RunHandoff`` pattern): the graph runs ``stage_infer``, ``stage_evaluate`` and
``stage_advise`` as SEPARATE nodes that each read ``state``. The rich Finding /
Issue objects the upstream nodes produce do not fit the serialized GraphState
cleanly, and ``state.py`` is READ-ONLY. So Wave C keeps its OWN in-memory,
per-run handoff keyed by ``run_id``: a thin WRAPPER around the Wave B chain's
``_infer_stage`` runs the frozen infer stage unchanged, then captures the
Findings it just derived (read from the Wave B chain's per-run handoff, before
the evaluate node pops it) into the Wave C handoff; the ``advise`` node pops them
for the same run, forms the Issues (reusing ``EvaluateEngine.form_issue`` — a
pure, rule-based read; no provider call), and anchors its Recommendations /
Clarifications to those Finding/Issue ids.

This is wiring state private to the chain — it changes NO graph topology, NO
GraphState field, and NO frozen module. If a future need required a topology or
GraphState change, that would be a STOP/escalate (it is not needed here).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from backend.orchestration.stages import register_stage
from backend.orchestration.wave_b import WaveBChain, build_and_register_wave_b_chain
from backend.responsibilities.advise.engine import AdviseEngine
from backend.responsibilities.advise.stage import run_advise_stage
from backend.responsibilities.evaluate.engine import EvaluateEngine
from backend.services.llm_provider import LLMProvider
from shared.epistemic import Finding, Issue


@dataclass
class _AdviseHandoff:
    """The in-memory handoff from the (wrapped) infer node to the advise node."""

    findings: tuple[Finding, ...]


@dataclass
class WaveCChain:
    """Builds + registers the full A→B→C chain: Wave B + the ``advise`` stage.

    ``provider`` is the shared LLM seam (a recorded-fixture model offline). The
    Wave B chain is built by CALLING its frozen builder; the advise stage reads
    the Findings the infer node produced for the same ``run_id`` (its own
    handoff, mirroring the Wave B ``_RunHandoff`` pattern) and forms the Issues
    to anchor to.
    """

    provider: LLMProvider
    extract_infer_inputs: Callable[[Any], dict[str, Any]]
    tier: str = "free"
    mode: str = "fast"
    user: str = "anonymous"
    confidence_stage: str = "orientation"
    understanding_state: str = "initial"
    prompt_suffix_for: Any = field(default=None)
    _wave_b: WaveBChain | None = field(default=None)
    _advise_handoff: dict[str, _AdviseHandoff] = field(default_factory=dict)

    # -- the wrapped `infer` stage (Wave B infer + capture for advise) --------

    def _infer_stage(self, state: Any, ctx: Any) -> dict[str, Any]:
        """Run the frozen Wave B composed infer stage, then capture its Findings.

        The Wave B chain's ``_infer_stage`` is CALLED unchanged (synthesis →
        finding); it stashes ``findings + model`` in the Wave B chain's own
        per-run handoff. We read those Findings straight after (before the
        evaluate node pops them) and stash them in the Wave C advise handoff for
        the same run.
        """
        assert self._wave_b is not None
        result = self._wave_b._infer_stage(state, ctx)
        run_key = WaveBChain._run_key(state)
        wave_b_handoff = self._wave_b._handoff.get(run_key)
        findings = wave_b_handoff.findings if wave_b_handoff is not None else ()
        self._advise_handoff[run_key] = _AdviseHandoff(findings=findings)
        return result

    # -- the `advise` stage (this slice) -------------------------------------

    def _advise_stage(self, state: Any, ctx: Any) -> dict[str, Any]:
        """Generate Recommendations/Clarifications anchored to the run's Findings/Issues."""
        run_key = WaveBChain._run_key(state)
        handoff = self._advise_handoff.pop(run_key, _AdviseHandoff(findings=()))
        inputs = self.extract_infer_inputs(state)

        findings = handoff.findings
        issues = self._form_issues(findings)

        engine = AdviseEngine(
            provider=self.provider,
            tier=self.tier,
            mode=self.mode,  # type: ignore[arg-type]
            user=self.user,
            confidence_stage=self.confidence_stage,  # type: ignore[arg-type]
            understanding_state=self.understanding_state,  # type: ignore[arg-type]
            prompt_suffix_for=self.prompt_suffix_for,
        )
        model_identity = self.provider.resolve(
            tier=self.tier, stage="advise"  # type: ignore[arg-type]
        ).model_ref.as_dict()
        result = run_advise_stage(
            engine=engine,
            project_id=inputs["project_id"],
            findings=findings,
            issues=issues,
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            prior_chr_id_for=inputs.get("advise_prior_chr_id_for"),
            model_identity=model_identity,
            tier=self.tier,
            user=self.user,
            mode=self.mode,
        )
        return {
            "outputs": {
                "recommendation_ids": [r.recommendation_id for r in result.recommendations],
                "recommendation_types": [
                    r.recommendation_type for r in result.recommendations
                ],
                "clarification_ids": [c.clarification_id for c in result.clarifications],
                "advise_degraded": result.degraded,
            }
        }

    def _form_issues(self, findings: tuple[Finding, ...]) -> tuple[Issue, ...]:
        """Form the Issues the advise stage anchors to (reusing Evaluate, read-only).

        ``EvaluateEngine.form_issue`` is a pure, rule-based mapping (severity →
        Issue) with NO provider call and NO emission — reused here ONLY to
        reconstruct the anchorable Issue ids for the same Findings (Evaluate
        remains the sole producer of the Issues persisted in its own stage; this
        is a read for anchoring, never a second canonical write).
        """
        eval_engine = EvaluateEngine(
            tier=self.tier,
            mode=self.mode,  # type: ignore[arg-type]
            user=self.user,
            confidence_stage=self.confidence_stage,  # type: ignore[arg-type]
        )
        return tuple(eval_engine.form_issue(f) for f in findings)

    @property
    def wave_b(self) -> WaveBChain:
        """The composed Wave B chain (test handle)."""
        assert self._wave_b is not None
        return self._wave_b

    # -- registration --------------------------------------------------------

    def register(self) -> None:
        """Register the (wrapped) ``infer`` + ``evaluate`` + the ``advise`` stage.

        The Wave B builder registers the composed ``infer`` + ``evaluate``; we
        then REPLACE the ``infer`` registration with the thin Wave C wrapper (so
        advise captures the Findings) and register ``advise``. NO graph topology
        change (``register_stage`` only; deep_pass.py untouched).
        """
        register_stage("infer", self._infer_stage)
        register_stage("advise", self._advise_stage)


def build_and_register_wave_c_chain(
    *,
    provider: LLMProvider,
    extract_infer_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
    prompt_suffix_for: Any = None,
) -> WaveCChain:
    """Build the full A→B→C chain and register all stages; return it (test handle).

    Composes by CALLING the frozen Wave B builder (which registers the composed
    ``infer`` + ``evaluate``), then wraps ``infer`` for the advise handoff and
    registers ``advise``. Returning the chain lets a caller (or a live e2e test)
    pass the stages as overrides too:
    ``{"infer": chain._infer_stage, "evaluate": chain.wave_b._evaluate_stage,
       "advise": chain._advise_stage}``.
    """
    wave_b = build_and_register_wave_b_chain(
        provider=provider,
        extract_infer_inputs=extract_infer_inputs,
        tier=tier,
        mode=mode,
        user=user,
        confidence_stage=confidence_stage,
        understanding_state=understanding_state,
        prompt_suffix_for=prompt_suffix_for,
    )
    chain = WaveCChain(
        provider=provider,
        extract_infer_inputs=extract_infer_inputs,
        tier=tier,
        mode=mode,
        user=user,
        confidence_stage=confidence_stage,
        understanding_state=understanding_state,
        prompt_suffix_for=prompt_suffix_for,
        _wave_b=wave_b,
    )
    chain.register()
    return chain

"""The injected ``infer`` stage for Wave S synthesis (decision #4; A3.4/A6).

This wires the synthesis engine into the recompute backbone WITHOUT touching
graph topology (decision #4): orchestration injects it via
``register_stage("infer", build_infer_stage(...))``. The stage:

- runs synthesis + generation (the engine) over the run's Attested assertions,
- emits ``synthesized_model_updated`` and one ``planning_artifact_generated``
  (or ``planning_artifact_regenerated`` on recompute) per artifact, plus the
  shared ``ai_spend_recorded`` cost event — each carrying ``mode`` +
  ``confidence_stage``/``understanding_state`` (decision #6), and
- APPENDS one Cognition History Record per generation through ``ctx.chr_repo``
  (CHR-is-Retain-owned; A3.5) — and emits ``cognition_history_record_appended``
  for each (gate-5 append↔event pairing).

Derived, never Attested (hard rule #2): the model + artifacts carry
``epistemic_state=derived``. The stage NEVER writes a generated artifact to a
canonical table as Attested and NEVER autonomously edits a user artifact — a
user edit is a separate new Attested input via Retain (DTM-0008).

-----------------------------------------------------------------------------
PERSISTENCE (RESOLVED — owner-approved 2026-06-17, DTM-0009): the Wave-S Derived
outputs persist via the GENERIC CHR ``output_kind`` /``output_payload`` with
``output_kind ∈ {synthesized_planning_model, planning_artifact}``. The owner
approved widening the canonical CHR ``output_kind`` CHECK and the
``retain/models.py`` ``OutputKind`` Literal by EXACTLY these two values
(migration ``20260617120000_chr_output_kind_wave_s.sql`` + the 2 Literal values;
append-only PRESERVED — only the CHECK value list grows). This stage builds each
CHR *spec* via ``planning_chr_spec`` and appends it through ``ctx.chr_repo``
(Retain-owned, A3.5). NOTE: gate-4 (``ci/gate_invariants.py``) currently flags
that owner-approved ALTER as a canonical-table mutation — see the DTM-0009 worker
report; the gate's migration linter needs an owner-ratified allowlist for this
append-only-preserving CHECK widening (a build-governance change beyond this
worker's authorized scope).
-----------------------------------------------------------------------------
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from backend.responsibilities.infer.synthesis import (
    SYNTHESIS_VERSION,
    SynthesisEngine,
    SynthesisResult,
)
from backend.responsibilities.retain import CognitionHistoryRecord
from backend.services.llm_provider import LLMProvider, RunBudget
from shared.epistemic import PlanningArtifact, SynthesizedPlanningModel

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.orchestration.stages import StageContext
    from backend.responsibilities.perceive.extraction import AssertionDraft

# The Wave-S CHR output kinds (contract persistence default — task + decisions).
# NOTE: not yet in the canonical CHR Literal/CHECK — see the ESCALATION above.
OUTPUT_KIND_SYNTHESIZED_MODEL = "synthesized_planning_model"
OUTPUT_KIND_PLANNING_ARTIFACT = "planning_artifact"


def planning_chr_spec(
    *,
    output_kind: str,
    output_payload: dict[str, Any],
    input_attestation_version: str,
    upstream_lineage: dict[str, Any],
    recompute_trigger: str | None,
    model_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build the CHR spec for a Wave-S generation (the contracted CHR shape).

    Mirrors the LDM §2.2 CHR field set the retain stage uses, with the Wave-S
    ``output_kind`` and the model/prompt/rule version stamp. Kept as a plain
    dict so the append target (a repo) validates it — the canonical model
    currently rejects the Wave-S output_kind (ESCALATION).

    ``model_or_rule_version`` records the RESOLVED provider/model actually used
    (``model_identity`` = ``provider.resolve(...).model_ref.as_dict()``) merged
    with the synthesis prompt version, so the CHR audits the real model consumed
    (DL-054 cond. 3 / DL-069 cond. 2 model-consumption auditability) — not a
    hardcoded provider.
    """
    return {
        "output_kind": output_kind,
        "output_payload": output_payload,
        "input_attestation_version": input_attestation_version,
        "model_or_rule_version": {**(model_identity or {}), "model_version": SYNTHESIS_VERSION},
        "upstream_lineage": upstream_lineage,
        "recompute_trigger": recompute_trigger,
    }


def _model_payload(model: SynthesizedPlanningModel) -> dict[str, Any]:
    return {
        "intent_summary": model.intent_summary,
        "scope_summary": model.scope_summary,
        "epistemic_state": model.epistemic_state.value,
        "mode": model.mode,
        "confidence_stage": model.confidence_stage,
        "understanding_state": model.understanding_state,
        "flagged_assumptions": [
            {"statement": a.statement, "covers_gap": a.covers_gap}
            for a in model.flagged_assumptions
        ],
    }


def _artifact_payload(artifact: PlanningArtifact) -> dict[str, Any]:
    return {
        "artifact_type": artifact.artifact_type,
        "title": artifact.title,
        "body": artifact.body,
        "epistemic_state": artifact.epistemic_state.value,
        "mode": artifact.mode,
        "confidence_stage": artifact.confidence_stage,
        "understanding_state": artifact.understanding_state,
        "flagged_assumptions": [
            {"statement": a.statement, "covers_gap": a.covers_gap}
            for a in artifact.flagged_assumptions
        ],
    }


def run_synthesis_stage(
    *,
    engine: SynthesisEngine,
    project_id: str,
    assertions: Sequence[AssertionDraft],
    assertion_ids: Sequence[str],
    ctx: StageContext,
    input_attestation_version: str,
    recompute_trigger: str | None,
    is_recompute: bool,
    budget: RunBudget | None = None,
) -> SynthesisResult:
    """Run synthesis+generation, emit events, and append one CHR per generation.

    Each CHR append goes through ``ctx.chr_repo`` (Retain-owned, A3.5) and is
    paired with a ``cognition_history_record_appended`` emit (gate-5). The
    synthesis + per-artifact events carry the mode/stage attributes (decision
    #6). On recompute, artifacts emit ``planning_artifact_regenerated`` (the
    prior is superseded; history appended, never overwritten — A5/A4.3).
    """
    result = engine.synthesize_and_generate(
        project_id=project_id,
        assertions=assertions,
        assertion_ids=assertion_ids,
        budget=budget,
    )
    emitter = ctx.emitter
    # Resolved model identity for CHR provenance (the ACTUAL provider/model the
    # engine routes — DL-069 cond. 2 auditability). Synthesis + generation share
    # one routed model in the internal-primary routing; resolve the synthesis
    # stage as the representative routed identity.
    synthesis_identity = engine.provider.resolve(
        tier=engine.tier,  # type: ignore[arg-type]
        stage="synthesis",
    ).model_ref.as_dict()
    generation_identity = engine.provider.resolve(
        tier=engine.tier,  # type: ignore[arg-type]
        stage="generation",
    ).model_ref.as_dict()
    base_attrs = {
        "project_id": project_id,
        "mode": result.model.mode,
        "confidence_stage": result.model.confidence_stage,
        "understanding_state": result.model.understanding_state,
    }

    # --- synthesized model: CHR + event -------------------------------------
    _append_chr(
        ctx,
        planning_chr_spec(
            output_kind=OUTPUT_KIND_SYNTHESIZED_MODEL,
            output_payload=_model_payload(result.model),
            input_attestation_version=input_attestation_version,
            upstream_lineage={"assertion_ids": list(result.model.derived_from_assertions)},
            recompute_trigger=recompute_trigger,
            model_identity=synthesis_identity,
        ),
        project_id=project_id,
        emitter=emitter,
    )
    emitter.emit(
        "synthesized_model_updated",
        {**base_attrs, "model_version": result.model.model_version},
    )

    # --- each generated artifact: CHR + event -------------------------------
    artifact_event = (
        "planning_artifact_regenerated" if is_recompute else "planning_artifact_generated"
    )
    for artifact in result.artifacts:
        _append_chr(
            ctx,
            planning_chr_spec(
                output_kind=OUTPUT_KIND_PLANNING_ARTIFACT,
                output_payload=_artifact_payload(artifact),
                input_attestation_version=input_attestation_version,
                upstream_lineage={
                    "assertion_ids": list(artifact.derived_from_assertions),
                    "synthesized_model_version": artifact.synthesized_model_version,
                },
                recompute_trigger=recompute_trigger,
                model_identity=generation_identity,
            ),
            project_id=project_id,
            emitter=emitter,
        )
        emitter.emit(
            artifact_event,
            {**base_attrs, "artifact_type": artifact.artifact_type},
        )

    # --- cost governance: one ai_spend_recorded per run ---------------------
    emitter.emit("ai_spend_recorded", result.spend_payload)
    return result


def _append_chr(
    ctx: StageContext,
    spec: dict[str, Any],
    *,
    project_id: str,
    emitter: Any,
) -> None:
    """Append one CHR via the Retain-owned repo + emit the append event (gate-5).

    The append goes through ``ctx.chr_repo`` (A3.5 — CHR-is-Retain-owned). The
    repo returns a persisted record carrying a chr_id; we emit
    ``cognition_history_record_appended`` for it (append↔event pairing).
    """
    if ctx.chr_repo is None:
        raise RuntimeError(
            "infer stage needs a ChrRepository to append synthesis CHRs (A3.5) "
            "— orchestration builds the graph with one"
        )
    # The Retain-owned repo persists a CognitionHistoryRecord MODEL (it calls
    # ``record.model_dump(...)``); construct it here, mirroring retain_stage —
    # the spec already carries the LDM §2.2 CHR fields incl. recompute_trigger.
    record = CognitionHistoryRecord(
        project_id=project_id,
        provenance_ref={"emitted_by": "infer.synthesis"},
        **spec,
    )
    persisted = ctx.chr_repo.append(record)
    chr_id = _persisted_chr_id(persisted)
    emitter.emit(
        "cognition_history_record_appended",
        {
            "project_id": project_id,
            "chr_id": chr_id,
            "output_kind": spec["output_kind"],
            "supersedes_chr_id": None,
        },
    )


def _persisted_chr_id(persisted: Any) -> str | None:
    """Pull a chr_id from the persisted record (dict or model), tolerant of shape."""
    if isinstance(persisted, dict):
        value = persisted.get("chr_id")
    else:
        value = getattr(persisted, "chr_id", None)
    return str(value) if value is not None else None


def build_infer_stage(
    *,
    provider: LLMProvider,
    extract_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    prompt_suffix_for: Callable[[str], str] | None = None,
) -> Callable[[Any, Any], dict[str, Any]]:
    """Build a stage fn for ``register_stage("infer", ...)`` (decision #4).

    ``extract_inputs(state)`` maps the GraphState into the synthesis inputs
    (project_id, assertions, assertion_ids, attestation version, recompute
    flag) — kept injectable so this module does not bind to a GraphState shape
    it does not own (orchestration is READ-ONLY). Returns the state updates the
    node produces (the live Derived projection refs); topology is untouched.
    """

    def infer_stage(state: Any, ctx: Any) -> dict[str, Any]:
        inputs = extract_inputs(state)
        engine = SynthesisEngine(
            provider=provider,
            tier=tier,
            mode=mode,  # type: ignore[arg-type]
            user=user,
            confidence_stage=inputs.get("confidence_stage", "orientation"),
            understanding_state=inputs.get("understanding_state", "initial"),
            prompt_suffix_for=prompt_suffix_for,
        )
        result = run_synthesis_stage(
            engine=engine,
            project_id=inputs["project_id"],
            assertions=inputs["assertions"],
            assertion_ids=inputs["assertion_ids"],
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            budget=inputs.get("budget"),
        )
        return {
            "outputs": {
                "synthesized_planning_model_version": result.model.model_version,
                "generated_artifact_types": [a.artifact_type for a in result.artifacts],
                "deferred_artifact_types": list(result.deferred_artifact_types),
                "synthesis_degraded": result.degraded,
            }
        }

    return infer_stage

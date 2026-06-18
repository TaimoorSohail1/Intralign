"""The injected ``advise`` stage (DTM-0014; IC-WC-ADVISE 1.1; decision #2).

Wires the Advise engine into the recompute backbone WITHOUT touching graph
topology: orchestration injects it via ``register_stage("advise", ...)`` (the
Wave-C placeholder ``wave_c_placeholder_advise`` is replaced, never the graph
re-wired). The stage:

- generates **Recommendations** (anchored to a Finding/Issue) + **Clarification
  Requests** (on blocking ambiguity) from the upstream Findings/Issues,
- APPENDS one Cognition History Record per emission through ``ctx.chr_repo``
  (CHR-is-Retain-owned, A3.5) — ``output_kind ∈ {recommendation, clarification}``,
  BOTH already in the canonical CHECK + ``OutputKind`` Literal, so NO migration —
  pairing each append with a ``cognition_history_record_appended`` emit (gate-5),
- carries the input-attestation version + the model/rule version + the upstream
  Finding/Issue ANCHOR lineage on every CHR (the "which finding motivated this"
  audit backbone),
- on a recompute RE-DERIVES and SUPERSEDES the prior emission (live replaced;
  history APPENDED — the prior CHR stays byte-intact; supersession keyed by the
  stable recommendation/clarification id),
- emits ``recommendation_generated`` / ``clarification_requested`` per emission,
  each carrying ``mode`` + ``confidence_stage`` (DL-046), and
- emits one ``ai_spend_recorded`` (DL-048) carrying the advise spend.

Advise PROPOSES, never DISPOSES (IC-WC-ADVISE forbidden): every output carries
``epistemic_state=derived``; the stage NEVER writes to a canonical table as
Attested, NEVER evaluates/scores (Evaluate's), NEVER generates Findings
(Infer's), NEVER governs/authorizes/executes, NEVER ACCEPTS its own output
(acceptance is the user's — DL-055; Wave U; the Recommendation ``state`` is
pinned ``generated``), and NEVER changes an assessment outside recompute.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from backend.responsibilities.advise.engine import (
    ADVISE_VERSION,
    AdviseEngine,
    AdviseResult,
)
from backend.responsibilities.retain import CognitionHistoryRecord
from shared.epistemic import ClarificationRequest, Recommendation

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.orchestration.stages import StageContext
    from shared.epistemic import Finding, Issue

# The Wave C Advise CHR output kinds (BOTH already in the canonical CHECK +
# ``OutputKind`` Literal — NO migration; decisions: "recommendation/clarification
# already exist").
OUTPUT_KIND_RECOMMENDATION = "recommendation"
OUTPUT_KIND_CLARIFICATION = "clarification"


# -- CHR payload shapes (the emitted value snapshots, LDM §2.2) ---------------


def _recommendation_payload(rec: Recommendation) -> dict[str, Any]:
    return {
        "recommendation_id": rec.recommendation_id,
        "recommendation_type": rec.recommendation_type,
        "anchor": rec.anchor,
        "summary": rec.summary,
        "state": rec.state,
        "epistemic_state": rec.epistemic_state.value,
        "mode": rec.mode,
        "confidence_stage": rec.confidence_stage,
        "understanding_state": rec.understanding_state,
    }


def _clarification_payload(clr: ClarificationRequest) -> dict[str, Any]:
    return {
        "clarification_id": clr.clarification_id,
        "anchor": clr.anchor,
        "question": clr.question,
        "epistemic_state": clr.epistemic_state.value,
        "mode": clr.mode,
        "confidence_stage": clr.confidence_stage,
        "understanding_state": clr.understanding_state,
    }


def run_advise_stage(
    *,
    engine: AdviseEngine,
    project_id: str,
    findings: Sequence[Finding] = (),
    issues: Sequence[Issue] = (),
    ctx: StageContext,
    input_attestation_version: str,
    recompute_trigger: str | None,
    is_recompute: bool,
    prior_chr_id_for: Callable[[str], str | None] | None = None,
    model_identity: dict[str, str] | None = None,
    tier: str = "free",
    user: str = "anonymous",
    mode: str = "fast",
) -> AdviseResult:
    """Derive Recommendations + Clarifications, emit events, append one CHR each.

    On a recompute, ``prior_chr_id_for(recommendation_id | clarification_id)``
    resolves the prior emission's CHR id so the new CHR carries
    ``supersedes_chr_id`` (lineage) — the prior CHR is never overwritten
    (append-only; A4.3). ``model_identity`` is the resolved provider/model the
    advise engine routed (DL-069 cond. 2 auditability), stamped on each CHR.
    """
    started = time.perf_counter()
    result = engine.derive(
        project_id=project_id, findings=findings, issues=issues
    )
    latency_ms = (time.perf_counter() - started) * 1000.0
    emitter = ctx.emitter

    # --- Recommendations: one CHR + recommendation_generated per Recommendation
    for rec in result.recommendations:
        prior = (
            prior_chr_id_for(rec.recommendation_id)
            if (is_recompute and prior_chr_id_for) else None
        )
        _append_chr(
            ctx,
            output_kind=OUTPUT_KIND_RECOMMENDATION,
            output_payload=_recommendation_payload(rec),
            input_attestation_version=input_attestation_version,
            upstream_lineage={
                "recommendation_id": rec.recommendation_id,
                "anchor": rec.anchor,
                "recommendation_type": rec.recommendation_type,
            },
            recompute_trigger=recompute_trigger,
            supersedes_chr_id=prior,
            project_id=project_id,
            model_identity=model_identity,
        )
        emitter.emit(
            "recommendation_generated",
            {
                "project_id": project_id,
                "recommendation_id": rec.recommendation_id,
                "recommendation_type": rec.recommendation_type,
                "anchor": rec.anchor,
                "state": rec.state,
                "mode": rec.mode,
                "confidence_stage": rec.confidence_stage,
                "supersedes_chr_id": prior,
            },
        )

    # --- Clarifications: one CHR + clarification_requested per request --------
    for clr in result.clarifications:
        prior = (
            prior_chr_id_for(clr.clarification_id)
            if (is_recompute and prior_chr_id_for) else None
        )
        _append_chr(
            ctx,
            output_kind=OUTPUT_KIND_CLARIFICATION,
            output_payload=_clarification_payload(clr),
            input_attestation_version=input_attestation_version,
            upstream_lineage={
                "clarification_id": clr.clarification_id,
                "anchor": clr.anchor,
            },
            recompute_trigger=recompute_trigger,
            supersedes_chr_id=prior,
            project_id=project_id,
            model_identity=model_identity,
        )
        emitter.emit(
            "clarification_requested",
            {
                "project_id": project_id,
                "clarification_id": clr.clarification_id,
                "anchor": clr.anchor,
                "mode": clr.mode,
                "confidence_stage": clr.confidence_stage,
                "supersedes_chr_id": prior,
            },
        )

    # --- cost governance + advise latency (DL-048 OBS) ----------------------
    emitter.emit(
        "ai_spend_recorded",
        {**result.spend_payload, "time_to_first_mri_ms": round(latency_ms, 3)},
    )
    return result


def _append_chr(
    ctx: StageContext,
    *,
    output_kind: str,
    output_payload: dict[str, Any],
    input_attestation_version: str,
    upstream_lineage: dict[str, Any],
    recompute_trigger: str | None,
    supersedes_chr_id: str | None,
    project_id: str,
    model_identity: dict[str, str] | None = None,
) -> None:
    """Append one Advise CHR via the Retain-owned repo + emit the append event.

    The append goes through ``ctx.chr_repo`` (A3.5 — CHR-is-Retain-owned). The
    repo returns a persisted record carrying a chr_id; we emit
    ``cognition_history_record_appended`` for it (append↔event pairing, gate-5).
    The CHR records the RESOLVED provider/model identity (DL-069 cond. 2) merged
    with the advise rule version.
    """
    if ctx.chr_repo is None:
        raise RuntimeError(
            "advise stage needs a ChrRepository to append advise CHRs "
            "(A3.5) — orchestration builds the graph with one"
        )
    spec = {
        "output_kind": output_kind,
        "output_payload": output_payload,
        "input_attestation_version": input_attestation_version,
        "model_or_rule_version": {**(model_identity or {}), "model_version": ADVISE_VERSION},
        "upstream_lineage": upstream_lineage,
        "recompute_trigger": recompute_trigger,
        "supersedes_chr_id": supersedes_chr_id,
    }
    # The Retain-owned repo persists a CognitionHistoryRecord MODEL (it calls
    # ``record.model_dump(...)``); construct it here, mirroring evaluate/stage.py
    # (the DTM-0013 model pattern — never a bare dict).
    record = CognitionHistoryRecord(
        project_id=project_id,
        provenance_ref={"emitted_by": "advise"},
        **spec,
    )
    persisted = ctx.chr_repo.append(record)
    chr_id = _persisted_chr_id(persisted)
    ctx.emitter.emit(
        "cognition_history_record_appended",
        {
            "project_id": project_id,
            "chr_id": chr_id,
            "output_kind": output_kind,
            "supersedes_chr_id": supersedes_chr_id,
        },
    )


def _persisted_chr_id(persisted: Any) -> str | None:
    """Pull a chr_id from the persisted record (dict or model), tolerant of shape."""
    if isinstance(persisted, dict):
        value = persisted.get("chr_id")
    else:
        value = getattr(persisted, "chr_id", None)
    return str(value) if value is not None else None


def build_advise_stage(
    *,
    provider: Any,
    extract_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    prompt_suffix_for: Callable[[str], str] | None = None,
) -> Callable[[Any, Any], dict[str, Any]]:
    """Build a stage fn for ``register_stage("advise", ...)`` (decision #2).

    ``extract_inputs(state)`` maps the GraphState into the Advise inputs
    (project_id, findings, issues, attestation version, recompute flag,
    prior-CHR resolver) — injectable so this module never binds to a GraphState
    shape it does not own (orchestration is READ-ONLY). Returns the state updates
    the node produces (the live Derived projection refs); topology is untouched.
    """

    def advise_stage(state: Any, ctx: Any) -> dict[str, Any]:
        inputs = extract_inputs(state)
        engine = AdviseEngine(
            provider=provider,
            tier=inputs.get("tier", tier),
            mode=inputs.get("mode", mode),  # type: ignore[arg-type]
            user=inputs.get("user", user),
            confidence_stage=inputs.get("confidence_stage", "orientation"),
            understanding_state=inputs.get("understanding_state", "initial"),
            prompt_suffix_for=prompt_suffix_for,
        )
        model_identity = provider.resolve(
            tier=inputs.get("tier", tier), stage="advise"
        ).model_ref.as_dict()
        result = run_advise_stage(
            engine=engine,
            project_id=inputs["project_id"],
            findings=inputs.get("findings", ()),
            issues=inputs.get("issues", ()),
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            prior_chr_id_for=inputs.get("prior_chr_id_for"),
            model_identity=model_identity,
            tier=inputs.get("tier", tier),
            user=inputs.get("user", user),
            mode=inputs.get("mode", mode),
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

    return advise_stage

"""The injected ``evaluate`` stage (DTM-0011; IC-WB-EVAL 2.1; decision #4).

Wires the Evaluate engine into the recompute backbone WITHOUT touching graph
topology: orchestration injects it via ``register_stage("evaluate", ...)`` (the
Wave-B placeholder is replaced, never the graph re-wired). The stage:

- forms Issues from Findings (severity → Issue) and computes the v0
  CAF / Confidence / Reliability / OutcomeConfidence assessment,
- APPENDS one Cognition History Record per value through ``ctx.chr_repo``
  (CHR-is-Retain-owned, A3.5) — ``output_kind ∈ {issue, confidence, reliability,
  caf, outcome_confidence}``, ALL already in the canonical CHECK + ``OutputKind``
  Literal, so NO migration — pairing each append with a
  ``cognition_history_record_appended`` emit (gate-5),
- carries the input-attestation version + the pinned rule version + the upstream
  Finding/Issue LINEAGE on every CHR (the "why did confidence change" backbone),
- on a recompute RE-COMPUTES and SUPERSEDES the prior values (live replaced;
  history APPENDED — the prior CHR stays byte-intact; a confidence delta is
  reconstructable from the CHR lineage),
- emits ``issue_generated`` / ``caf_assessed`` / ``outcome_confidence_computed``,
  plus ``understanding_state_changed`` (AE-04) and ``false_confidence_flagged``
  (CONF-06) when they apply, each carrying ``mode`` + ``confidence_stage``, and
- emits one ``ai_spend_recorded`` (DL-048) carrying the Fast-Pass
  Time-to-First-MRI latency (over-budget latency = trust signal).

Derived, never Attested (hard rule #2): every value carries
``epistemic_state=derived``; the stage NEVER writes to a canonical table as
Attested, NEVER generates Findings (Infer) or recommendations (Advise), NEVER
accepts an interpretation, and NEVER changes a value outside recompute (a stage/
state change happens ONLY on a re-run).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from backend.responsibilities.evaluate.engine import (
    EvaluateEngine,
    EvaluationResult,
)
from backend.responsibilities.evaluate.scoring import CAF_RULE_VERSION
from backend.responsibilities.retain import CognitionHistoryRecord
from backend.services.llm_provider import estimate_cost_usd, routing_for_tier
from shared.epistemic import (
    CAFAssessment,
    Confidence,
    Finding,
    Issue,
    OutcomeConfidence,
    Reliability,
)

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.orchestration.stages import StageContext
    from shared.epistemic import SynthesizedPlanningModel

# The Wave B Evaluate CHR output kinds (ALL already in the canonical CHECK +
# ``OutputKind`` Literal — NO migration; decisions: "Wave B kinds already exist").
OUTPUT_KIND_ISSUE = "issue"
OUTPUT_KIND_CONFIDENCE = "confidence"
OUTPUT_KIND_RELIABILITY = "reliability"
OUTPUT_KIND_CAF = "caf"
OUTPUT_KIND_OUTCOME_CONFIDENCE = "outcome_confidence"


def _model_or_rule_version() -> dict[str, Any]:
    """The pinned rule-version stamp — rule arithmetic replays EXACT (ADR-0006)."""
    return {"provider": "rule", "model_version": CAF_RULE_VERSION}


# -- CHR payload shapes (the emitted value snapshots, LDM §2.2) ---------------


def _issue_payload(issue: Issue) -> dict[str, Any]:
    return {
        "issue_id": issue.issue_id,
        "finding_id": issue.finding_id,
        "finding_type": issue.finding_type,
        "severity": issue.severity,
        "summary": issue.summary,
        "evidence_anchors": list(issue.evidence_anchors),
        "epistemic_state": issue.epistemic_state.value,
        "mode": issue.mode,
        "confidence_stage": issue.confidence_stage,
        "understanding_state": issue.understanding_state,
    }


def _confidence_payload(confidence: Confidence) -> dict[str, Any]:
    return {
        "index": confidence.index,
        "band": confidence.band,
        "reliability_qualifier": confidence.reliability_qualifier,
        "basis": list(confidence.basis),
        "epistemic_state": confidence.epistemic_state.value,
        "mode": confidence.mode,
        "confidence_stage": confidence.confidence_stage,
        "understanding_state": confidence.understanding_state,
    }


def _reliability_payload(reliability: Reliability) -> dict[str, Any]:
    return {
        "level": reliability.level,
        "basis": reliability.basis,
        "epistemic_state": reliability.epistemic_state.value,
        "mode": reliability.mode,
        "confidence_stage": reliability.confidence_stage,
        "understanding_state": reliability.understanding_state,
    }


def _caf_payload(caf: CAFAssessment) -> dict[str, Any]:
    return {
        "dimensions": {
            d.dimension: {"index": d.index, "band": d.band, "reliability": d.reliability}
            for d in caf.dimensions()
        },
        "derived_from_findings": list(caf.derived_from_findings),
        "epistemic_state": caf.epistemic_state.value,
        "mode": caf.mode,
        "confidence_stage": caf.confidence_stage,
        "understanding_state": caf.understanding_state,
    }


def _outcome_confidence_payload(oc: OutcomeConfidence) -> dict[str, Any]:
    return {
        "index": oc.index,
        "band": oc.band,
        "reliability_qualifier": oc.reliability_qualifier,
        "false_confidence_flagged": oc.false_confidence_flagged,
        "basis": list(oc.basis),
        "derived_from_findings": list(oc.derived_from_findings),
        "epistemic_state": oc.epistemic_state.value,
        "mode": oc.mode,
        "confidence_stage": oc.confidence_stage,
        "understanding_state": oc.understanding_state,
    }


def run_evaluate_stage(
    *,
    engine: EvaluateEngine,
    project_id: str,
    findings: Sequence[Finding],
    ctx: StageContext,
    input_attestation_version: str,
    recompute_trigger: str | None,
    is_recompute: bool,
    model: SynthesizedPlanningModel | None = None,
    prior_understanding_state: str | None = None,
    prior_chr_id_for: Callable[[str], str | None] | None = None,
    tier: str = "free",
    user: str = "anonymous",
    mode: str = "fast",
) -> EvaluationResult:
    """Compute the assessment, emit events, and append one CHR per value.

    On a recompute, ``prior_chr_id_for(output_kind_or_key)`` resolves the prior
    value's CHR id so the new CHR carries ``supersedes_chr_id`` (lineage) — the
    prior CHR is never overwritten (append-only; A4.3). The
    ``prior_understanding_state`` lets the stage emit
    ``understanding_state_changed`` only when the state actually advanced (AE-04;
    a state change happens ONLY here, via recompute).
    """
    started = time.perf_counter()
    result = engine.assess(project_id=project_id, findings=findings, model=model)
    latency_ms = (time.perf_counter() - started) * 1000.0
    emitter = ctx.emitter

    finding_lineage = [f.finding_id for f in findings]

    # --- Issues: one CHR + issue_generated per Issue ------------------------
    for issue in result.issues:
        prior = prior_chr_id_for(issue.issue_id) if (is_recompute and prior_chr_id_for) else None
        _append_chr(
            ctx,
            output_kind=OUTPUT_KIND_ISSUE,
            output_payload=_issue_payload(issue),
            input_attestation_version=input_attestation_version,
            upstream_lineage={
                "issue_id": issue.issue_id,
                "finding_id": issue.finding_id,
                "evidence_anchors": list(issue.evidence_anchors),
            },
            recompute_trigger=recompute_trigger,
            supersedes_chr_id=prior,
            project_id=project_id,
        )
        emitter.emit(
            "issue_generated",
            {
                "project_id": project_id,
                "issue_id": issue.issue_id,
                "finding_id": issue.finding_id,
                "severity": issue.severity,
                "mode": issue.mode,
                "confidence_stage": issue.confidence_stage,
                "supersedes_chr_id": prior,
            },
        )

    # --- Reliability (separate qualifier): CHR only (no dedicated event) ----
    _append_chr(
        ctx,
        output_kind=OUTPUT_KIND_RELIABILITY,
        output_payload=_reliability_payload(result.reliability),
        input_attestation_version=input_attestation_version,
        upstream_lineage={"finding_ids": finding_lineage},
        recompute_trigger=recompute_trigger,
        supersedes_chr_id=(
            prior_chr_id_for(OUTPUT_KIND_RELIABILITY)
            if (is_recompute and prior_chr_id_for) else None
        ),
        project_id=project_id,
    )

    # --- CAF assessment: CHR + caf_assessed ---------------------------------
    _append_chr(
        ctx,
        output_kind=OUTPUT_KIND_CAF,
        output_payload=_caf_payload(result.caf),
        input_attestation_version=input_attestation_version,
        upstream_lineage={"finding_ids": finding_lineage},
        recompute_trigger=recompute_trigger,
        supersedes_chr_id=(
            prior_chr_id_for(OUTPUT_KIND_CAF) if (is_recompute and prior_chr_id_for) else None
        ),
        project_id=project_id,
    )
    emitter.emit(
        "caf_assessed",
        {
            "project_id": project_id,
            "dimensions": {
                d.dimension: {"band": d.band} for d in result.caf.dimensions()
            },
            "mode": result.caf.mode,
            "confidence_stage": result.caf.confidence_stage,
        },
    )

    # --- headline Confidence: CHR only (the band the MRI reads) -------------
    _append_chr(
        ctx,
        output_kind=OUTPUT_KIND_CONFIDENCE,
        output_payload=_confidence_payload(result.confidence),
        input_attestation_version=input_attestation_version,
        upstream_lineage={"finding_ids": finding_lineage},
        recompute_trigger=recompute_trigger,
        supersedes_chr_id=(
            prior_chr_id_for(OUTPUT_KIND_CONFIDENCE)
            if (is_recompute and prior_chr_id_for) else None
        ),
        project_id=project_id,
    )

    # --- Outcome Confidence: CHR + outcome_confidence_computed --------------
    _append_chr(
        ctx,
        output_kind=OUTPUT_KIND_OUTCOME_CONFIDENCE,
        output_payload=_outcome_confidence_payload(result.outcome_confidence),
        input_attestation_version=input_attestation_version,
        upstream_lineage={"finding_ids": finding_lineage},
        recompute_trigger=recompute_trigger,
        supersedes_chr_id=(
            prior_chr_id_for(OUTPUT_KIND_OUTCOME_CONFIDENCE)
            if (is_recompute and prior_chr_id_for) else None
        ),
        project_id=project_id,
    )
    emitter.emit(
        "outcome_confidence_computed",
        {
            "project_id": project_id,
            "band": result.outcome_confidence.band,
            "reliability_qualifier": result.outcome_confidence.reliability_qualifier,
            "mode": result.outcome_confidence.mode,
            "confidence_stage": result.outcome_confidence.confidence_stage,
        },
    )

    # --- CONF-06 false confidence: a trust signal, never silently dropped ---
    if result.outcome_confidence.false_confidence_flagged:
        emitter.emit(
            "false_confidence_flagged",
            {
                "project_id": project_id,
                "band": result.outcome_confidence.band,
                "reliability_qualifier": result.outcome_confidence.reliability_qualifier,
                "mode": result.outcome_confidence.mode,
                "confidence_stage": result.outcome_confidence.confidence_stage,
            },
        )

    # --- AE-04 understanding-state change: ONLY when it actually advanced ---
    if (
        prior_understanding_state is not None
        and prior_understanding_state != result.understanding_state
    ):
        emitter.emit(
            "understanding_state_changed",
            {
                "project_id": project_id,
                "from_state": prior_understanding_state,
                "to_state": result.understanding_state,
                "mode": mode,
                "confidence_stage": engine.confidence_stage,
            },
        )

    # --- cost governance + Fast-Pass Time-to-First-MRI latency (DL-048 OBS) --
    emitter.emit(
        "ai_spend_recorded",
        _spend_payload(
            tier=tier, user=user, mode=mode,
            confidence_stage=engine.confidence_stage,
            understanding_state=result.understanding_state,
            time_to_first_mri_ms=round(latency_ms, 3),
        ),
    )
    return result


def _spend_payload(
    *,
    tier: str,
    user: str,
    mode: str,
    confidence_stage: str,
    understanding_state: str,
    time_to_first_mri_ms: float,
) -> dict[str, Any]:
    """The shared ``ai_spend_recorded`` shape (DL-048). Evaluate is rule-arithmetic:
    it makes NO provider call (zero tokens) — the event still records the routed
    model + the Fast-Pass latency so cost/latency stay observable across the chain.
    """
    model_name = routing_for_tier(tier).model_for("synthesis").model  # type: ignore[arg-type]
    return {
        "tokens_in": 0,
        "tokens_out": 0,
        "est_cost": estimate_cost_usd(model_name, 0, 0),
        "tier": tier,
        "user": user,
        "mode": mode,
        "model": model_name,
        "confidence_stage": confidence_stage,
        "understanding_state": understanding_state,
        "over_budget": False,
        "degraded": False,
        "time_to_first_mri_ms": time_to_first_mri_ms,
    }


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
) -> None:
    """Append one Evaluate CHR via the Retain-owned repo + emit the append event.

    The append goes through ``ctx.chr_repo`` (A3.5 — CHR-is-Retain-owned). The
    repo returns a persisted record carrying a chr_id; we emit
    ``cognition_history_record_appended`` for it (append↔event pairing, gate-5).
    """
    if ctx.chr_repo is None:
        raise RuntimeError(
            "evaluate stage needs a ChrRepository to append assessment CHRs "
            "(A3.5) — orchestration builds the graph with one"
        )
    spec = {
        "output_kind": output_kind,
        "output_payload": output_payload,
        "input_attestation_version": input_attestation_version,
        "model_or_rule_version": _model_or_rule_version(),
        "upstream_lineage": upstream_lineage,
        "recompute_trigger": recompute_trigger,
        "supersedes_chr_id": supersedes_chr_id,
    }
    # The Retain-owned repo persists a CognitionHistoryRecord MODEL (it calls
    # ``record.model_dump(...)``); construct it here, mirroring retain_stage.
    record = CognitionHistoryRecord(
        project_id=project_id,
        provenance_ref={"emitted_by": "evaluate"},
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


def build_evaluate_stage(
    *,
    extract_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
) -> Callable[[Any, Any], dict[str, Any]]:
    """Build a stage fn for ``register_stage("evaluate", ...)`` (decision #4).

    ``extract_inputs(state)`` maps the GraphState into the Evaluate inputs
    (project_id, findings, synthesized model, attestation version, recompute
    flag, prior-state/CHR resolvers) — injectable so this module never binds to a
    GraphState shape it does not own (orchestration is READ-ONLY). Returns the
    state updates the node produces (the live Derived projection refs); topology
    is untouched.
    """

    def evaluate_stage(state: Any, ctx: Any) -> dict[str, Any]:
        inputs = extract_inputs(state)
        engine = EvaluateEngine(
            tier=inputs.get("tier", tier),
            mode=inputs.get("mode", mode),  # type: ignore[arg-type]
            user=inputs.get("user", user),
            confidence_stage=inputs.get("confidence_stage", "orientation"),
        )
        result = run_evaluate_stage(
            engine=engine,
            project_id=inputs["project_id"],
            findings=inputs.get("findings", []),
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            model=inputs.get("synthesized_model"),
            prior_understanding_state=inputs.get("prior_understanding_state"),
            prior_chr_id_for=inputs.get("prior_chr_id_for"),
            tier=inputs.get("tier", tier),
            user=inputs.get("user", user),
            mode=inputs.get("mode", mode),
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

    return evaluate_stage

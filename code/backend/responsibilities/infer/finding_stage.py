"""The injected ``infer`` Finding stage (DTM-0010; IC-WB-INFER 1.1; decision #4).

Wires the Finding engine into the recompute backbone WITHOUT touching graph
topology: orchestration injects it via ``register_stage("infer", ...)``. It is
ADDITIVE to the DTM-0009 synthesis stage (``stage.py``) — a separate stage fn so
the synthesis wiring is untouched. The stage:

- derives Gap / Conflict / Risk Findings over the run's Attested assertions +
  the DTM-0009 ``SynthesizedPlanningModel`` + the declared-outcome reference,
- APPENDS one Cognition History Record per Finding through ``ctx.chr_repo``
  (CHR-is-Retain-owned, A3.5; ``output_kind="finding"`` — already in the
  canonical CHECK + ``OutputKind`` Literal, so NO migration is needed), pairing
  each append with a ``cognition_history_record_appended`` emit (gate-5),
- emits ``finding_detected`` per Finding (or ``finding_superseded`` when a
  recompute re-derives a Finding that supersedes a prior one), each carrying
  ``mode`` + ``confidence_stage`` (DL-046), and
- on the Fast Pass emits the **Time-to-First-MRI latency** via the shared
  ``ai_spend_recorded`` cost event payload (over-budget latency = trust signal).

Derived, never Attested (hard rule #2): every Finding carries
``epistemic_state=derived`` and the stage NEVER writes a Finding to a canonical
table as Attested, NEVER computes severity/confidence (Evaluate / DTM-0011),
and NEVER resolves a conflict into canonical truth.

Recompute (IC-WB-INFER #4): a recompute RE-DERIVES Findings and SUPERSEDES the
prior ones (live replaced; history APPENDED — the prior CHR stays byte-intact,
A5/A4.3). Supersession is keyed by the stable ``finding_id``; ``mode`` /
``confidence_stage`` change ONLY on a recompute (never in place).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from backend.responsibilities.infer.finding import (
    FINDING_VERSION,
    FindingEngine,
    FindingResult,
)
from backend.responsibilities.retain import CognitionHistoryRecord
from backend.services.llm_provider import LLMProvider, RunBudget
from shared.epistemic import Finding

if TYPE_CHECKING:  # pragma: no cover - typing only
    from backend.orchestration.stages import StageContext
    from backend.responsibilities.perceive.extraction import AssertionDraft
    from shared.epistemic import SynthesizedPlanningModel

# The Wave B Finding CHR output kind (already in the canonical CHECK + Literal —
# NO migration; decisions: "Wave B kinds already exist").
OUTPUT_KIND_FINDING = "finding"


def finding_chr_spec(
    *,
    finding: Finding,
    input_attestation_version: str,
    recompute_trigger: str | None,
    supersedes_chr_id: str | None,
    model_identity: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build the CHR spec for one Finding emission (the contracted CHR shape).

    Carries the Finding payload, the input-attestation version, the model/rule
    version stamp, the upstream lineage (the Attested assertion ids the Finding
    derived from — the audit answer to "which assertions"), and, on a recompute,
    the ``supersedes_chr_id`` of the prior Finding CHR (lineage; never a mutation).

    ``model_or_rule_version`` records the RESOLVED provider/model actually used
    (``model_identity`` = ``provider.resolve(...).model_ref.as_dict()``) merged
    with the Finding rule version, so the CHR audits the real model consumed
    (DL-054 cond. 3 / DL-069 cond. 2) — not a hardcoded provider.
    """
    return {
        "output_kind": OUTPUT_KIND_FINDING,
        "output_payload": _finding_payload(finding),
        "input_attestation_version": input_attestation_version,
        "model_or_rule_version": {**(model_identity or {}), "model_version": FINDING_VERSION},
        "upstream_lineage": {
            "finding_id": finding.finding_id,
            "finding_type": finding.finding_type,
            "evidence_anchors": list(finding.evidence_anchors),
        },
        "recompute_trigger": recompute_trigger,
        "supersedes_chr_id": supersedes_chr_id,
    }


def _finding_payload(finding: Finding) -> dict[str, Any]:
    return {
        "finding_id": finding.finding_id,
        "finding_type": finding.finding_type,
        "summary": finding.summary,
        "evidence_anchors": list(finding.evidence_anchors),
        "gap_kind": finding.gap_kind,
        "epistemic_state": finding.epistemic_state.value,
        "mode": finding.mode,
        "confidence_stage": finding.confidence_stage,
        "understanding_state": finding.understanding_state,
    }


def run_finding_stage(
    *,
    engine: FindingEngine,
    project_id: str,
    assertions: Sequence[AssertionDraft],
    assertion_ids: Sequence[str],
    ctx: StageContext,
    input_attestation_version: str,
    recompute_trigger: str | None,
    is_recompute: bool,
    model: SynthesizedPlanningModel | None = None,
    declared_outcome: str | None = None,
    outcome_anchor: str | None = None,
    prior_chr_id_for: Callable[[str], str | None] | None = None,
    budget: RunBudget | None = None,
) -> FindingResult:
    """Derive Findings, emit events, and append one CHR per Finding.

    On a recompute, ``prior_chr_id_for(finding_id)`` resolves the prior
    Finding's CHR id so the new CHR carries ``supersedes_chr_id`` (lineage) and
    the emission is ``finding_superseded`` instead of ``finding_detected``. The
    prior CHR is never overwritten (append-only; A4.3). The Fast-Pass
    Time-to-First-MRI latency is emitted on the ``ai_spend_recorded`` payload.
    """
    started = time.perf_counter()
    result = engine.derive(
        project_id=project_id,
        assertions=assertions,
        assertion_ids=assertion_ids,
        model=model,
        declared_outcome=declared_outcome,
        outcome_anchor=outcome_anchor,
        budget=budget,
    )
    latency_ms = (time.perf_counter() - started) * 1000.0
    emitter = ctx.emitter
    # Resolved model identity for CHR provenance (the ACTUAL provider/model the
    # Finding engine routes — DL-069 cond. 2 auditability). Findings route via
    # the synthesis stage (finding.py uses stage="synthesis").
    finding_identity = engine.provider.resolve(
        tier=engine.tier,  # type: ignore[arg-type]
        stage="synthesis",
    ).model_ref.as_dict()

    for finding in result.findings:
        prior_chr_id = (
            prior_chr_id_for(finding.finding_id)
            if (is_recompute and prior_chr_id_for is not None)
            else None
        )
        superseding = prior_chr_id is not None
        _append_chr(
            ctx,
            finding_chr_spec(
                finding=finding,
                input_attestation_version=input_attestation_version,
                recompute_trigger=recompute_trigger,
                supersedes_chr_id=prior_chr_id,
                model_identity=finding_identity,
            ),
            project_id=project_id,
            supersedes_chr_id=prior_chr_id,
            emitter=emitter,
        )
        emitter.emit(
            "finding_superseded" if superseding else "finding_detected",
            {
                "project_id": project_id,
                "finding_id": finding.finding_id,
                "finding_type": finding.finding_type,
                "evidence_anchors": list(finding.evidence_anchors),
                "mode": finding.mode,
                "confidence_stage": finding.confidence_stage,
                "supersedes_chr_id": prior_chr_id,
            },
        )

    # Cost governance + Fast-Pass Time-to-First-MRI latency (DL-046/DL-048 OBS).
    emitter.emit(
        "ai_spend_recorded",
        {**result.spend_payload, "time_to_first_mri_ms": round(latency_ms, 3)},
    )
    return result


def _append_chr(
    ctx: StageContext,
    spec: dict[str, Any],
    *,
    project_id: str,
    supersedes_chr_id: str | None,
    emitter: Any,
) -> None:
    """Append one Finding CHR via the Retain-owned repo + emit the append event.

    The append goes through ``ctx.chr_repo`` (A3.5 — CHR-is-Retain-owned). The
    repo returns a persisted record carrying a chr_id; we emit
    ``cognition_history_record_appended`` for it (append<->event pairing, gate-5).
    """
    if ctx.chr_repo is None:
        raise RuntimeError(
            "infer Finding stage needs a ChrRepository to append Finding CHRs "
            "(A3.5) — orchestration builds the graph with one"
        )
    # The Retain-owned repo persists a CognitionHistoryRecord MODEL (it calls
    # ``record.model_dump(...)``); construct it here, mirroring retain_stage —
    # the spec already carries the LDM §2.2 CHR fields incl. recompute_trigger.
    record = CognitionHistoryRecord(
        project_id=project_id,
        provenance_ref={"emitted_by": "infer.finding"},
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


def build_finding_stage(
    *,
    provider: LLMProvider,
    extract_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    prompt_suffix_for: Callable[[str], str] | None = None,
) -> Callable[[Any, Any], dict[str, Any]]:
    """Build a stage fn for ``register_stage("infer", ...)`` (decision #4).

    ``extract_inputs(state)`` maps the GraphState into the Finding inputs
    (project_id, assertions, assertion_ids, synthesized model, declared outcome,
    attestation version, recompute flag, prior-CHR resolver) — injectable so
    this module never binds to a GraphState shape it does not own (orchestration
    is READ-ONLY). Returns the state updates the node produces (the live Derived
    Finding projection refs); topology is untouched.
    """

    def finding_stage(state: Any, ctx: Any) -> dict[str, Any]:
        inputs = extract_inputs(state)
        engine = FindingEngine(
            provider=provider,
            tier=tier,
            mode=mode,  # type: ignore[arg-type]
            user=user,
            confidence_stage=inputs.get("confidence_stage", "orientation"),
            understanding_state=inputs.get("understanding_state", "initial"),
            prompt_suffix_for=prompt_suffix_for,
        )
        result = run_finding_stage(
            engine=engine,
            project_id=inputs["project_id"],
            assertions=inputs["assertions"],
            assertion_ids=inputs["assertion_ids"],
            ctx=ctx,
            input_attestation_version=inputs.get("input_attestation_version", "v1"),
            recompute_trigger=inputs.get("recompute_trigger"),
            is_recompute=inputs.get("is_recompute", False),
            model=inputs.get("synthesized_model"),
            declared_outcome=inputs.get("declared_outcome"),
            outcome_anchor=inputs.get("outcome_anchor"),
            prior_chr_id_for=inputs.get("prior_chr_id_for"),
            budget=inputs.get("budget"),
        )
        return {
            "outputs": {
                "finding_ids": [f.finding_id for f in result.findings],
                "finding_types": [f.finding_type for f in result.findings],
                "findings_degraded": result.degraded,
            }
        }

    return finding_stage

"""Wave U reconcile wiring (DTM-0017; ADDITIVE ONLY — A→B→C + Acceptance-Impact).

This module composes the full **A→B→C** chain by *calling* the frozen Wave C
chain builder (``build_and_register_wave_c_chain`` — synthesis → finding →
evaluate → advise) and ADDS the Evaluate-owned **Acceptance-Impact reconcile**
that runs AFTER a recompute produces new values (IC-WU-ACCEPT U1.3; ADR-0009 —
reconcile owned by Evaluate, runs post-Evaluate in the recompute). It does **NOT**
edit any frozen file: not ``wave_c.py`` / ``wave_b.py`` (it CALLS the C builder),
not ``deep_pass.py`` topology, not ``state.py`` / ``runner.py`` / ``stages.py``,
and not the frozen ``evaluate/stage.py`` core (the reconcile is an ADDITIVE
call-out, not a change to the stage).

The reconcile (``reconcile_acceptance_impact``) is the smallest additive step:
after the chain has emitted the new values, it scans the project's **active
version-pinned UARs** (``store.acceptances_for_project`` — a SELECT, append-only
preserved); for each accepting UAR it reads the value at the **version-pinned**
CHR and the **latest** value for the same accepted item, runs the PURE compare
(``evaluate/acceptance_impact.py`` — ≥10 pts or band change, Calibration §3; no
LLM), and on drift appends ONE Derived ``AcceptanceImpactAssessment`` CHR (the
DTM-0013 model pattern: ``output_kind="acceptance_impact"``,
``provenance_ref={"emitted_by":"evaluate"}``, ``upstream_lineage={uar_id,
pinned_chr, latest_chr}``, ``supersedes_chr_id`` = the prior assessment for THIS
UAR), emitting ``cognition_history_record_appended`` + ``acceptance_impact_assessed``.

It is read-only over the UAR and the plan fact (it reads them; it mutates
neither). Below threshold it raises nothing. The assessment is **Derived**, never
canonical / world-truth (hard rule #2; the seven (G) forbidden).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from backend.responsibilities.evaluate.acceptance_impact import (
    AcceptedValue,
    compare_acceptance_impact,
)
from backend.responsibilities.evaluate.scoring import CAF_RULE_VERSION
from backend.responsibilities.retain import CognitionHistoryRecord
from backend.responsibilities.retain.repository import ChrRepository
from backend.services.observability.events import (
    CollectingEventEmitter,
    EventEmitter,
)
from shared.epistemic import AcceptanceImpactAssessment

# The user-confirm actions whose accepted item the reconcile watches for drift.
# An Acceptance-Impact alert is "a decision you confirmed is affected" — only
# accept / direct_edit confirm something (reject/defer write no plan fact, U1.2),
# so only those UARs are active for reconciliation.
_RECONCILED_ACTIONS: frozenset[str] = frozenset({"accept", "direct_edit"})

OUTPUT_KIND_ACCEPTANCE_IMPACT = "acceptance_impact"


def _accepted_value(payload: Any) -> AcceptedValue | None:
    """Read the (index, band) value behind an accepted item from a CHR payload.

    The value that drifts is the Evaluate value the CHR carries (``index`` +
    ``band``). A payload with no numeric value (e.g. a recommendation/finding
    snapshot) has no Acceptance-Impact value to compare — returns None (the
    reconcile skips it; nothing is invented). A pure data read; no LLM.
    """
    if not isinstance(payload, dict):
        return None
    index = payload.get("index")
    band = payload.get("band")
    if index is None or band is None:
        return None
    try:
        return AcceptedValue(index=float(index), band=str(band))
    except (TypeError, ValueError):
        return None


def reconcile_acceptance_impact(
    *,
    project_id: str,
    store: Any,
    chr_repo: ChrRepository,
    emitter: EventEmitter | None = None,
    recompute_trigger: str | None = "reanalysis",
    mode: str = "fast",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
) -> list[AcceptanceImpactAssessment]:
    """Scan the project's active UARs and raise an Acceptance-Impact Assessment per drift.

    For each accepting (version-pinned) UAR: read the value at the pinned CHR and
    the latest value for the same accepted item; if the drift crosses Calibration
    §3 (≥10 pts or band change), append ONE Derived ``AcceptanceImpactAssessment``
    CHR (DTM-0013 model pattern), superseding a prior assessment for the SAME UAR,
    and emit ``cognition_history_record_appended`` + ``acceptance_impact_assessed``.

    Read-only over the UAR + plan fact (mutates neither). Below threshold: nothing.
    Returns the assessments raised (test/handle convenience).
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    raised: list[AcceptanceImpactAssessment] = []

    for uar in store.acceptances_for_project(project_id):
        if str(uar.get("action")) not in _RECONCILED_ACTIONS:
            continue
        pin = uar.get("version_pin")
        if pin is None or not str(pin).strip():
            continue  # an unpinned UAR cannot be reconciled (pin is mandatory; U1.2)

        pinned_chr = chr_repo.get(pin)
        if pinned_chr is None:
            continue  # the pinned emission no longer resolvable — nothing to compare
        latest_chr = chr_repo.latest_for_output(
            pinned_chr.project_id, pinned_chr.output_kind
        )
        if latest_chr is None or str(latest_chr.chr_id) == str(pinned_chr.chr_id):
            continue  # no newer value for the accepted item — no drift to assess

        pinned_value = _accepted_value(pinned_chr.output_payload)
        latest_value = _accepted_value(latest_chr.output_payload)
        if pinned_value is None or latest_value is None:
            continue  # the accepted item carries no numeric value to drift on

        drift = compare_acceptance_impact(pinned=pinned_value, latest=latest_value)
        if not drift.is_drift:
            continue  # below the ≥10/band threshold — raise nothing (Calibration §3)

        uar_id = str(uar.get("uar_id"))
        prior = chr_repo.latest_acceptance_impact_for_uar(project_id, uar_id)
        supersedes = str(prior.chr_id) if prior is not None else None

        assessment = AcceptanceImpactAssessment(
            project_id=project_id,
            uar_ref=uar_id,
            pinned_chr=str(pinned_chr.chr_id),
            latest_chr=str(latest_chr.chr_id),
            delta=drift.delta,
            band_changed=drift.band_changed,
            pinned_band=drift.pinned_band,  # type: ignore[arg-type]
            latest_band=drift.latest_band,  # type: ignore[arg-type]
            model_or_rule_version=CAF_RULE_VERSION,
            mode=mode,  # type: ignore[arg-type]
            confidence_stage=confidence_stage,  # type: ignore[arg-type]
            understanding_state=understanding_state,  # type: ignore[arg-type]
        )
        raised.append(assessment)

        # DTM-0013 model pattern — append the Derived assessment as a CHR. The
        # UAR + plan fact are untouched (read-only); this is a NEW append-only
        # acceptance_impact receipt, superseding the prior assessment for THIS UAR.
        record = CognitionHistoryRecord(
            project_id=project_id,
            output_kind=OUTPUT_KIND_ACCEPTANCE_IMPACT,
            output_payload={
                "uar_ref": assessment.uar_ref,
                "pinned_chr": assessment.pinned_chr,
                "latest_chr": assessment.latest_chr,
                "delta": assessment.delta,
                "band_changed": assessment.band_changed,
                "pinned_band": assessment.pinned_band,
                "latest_band": assessment.latest_band,
                "epistemic_state": assessment.epistemic_state.value,
                "mode": assessment.mode,
                "confidence_stage": assessment.confidence_stage,
                "understanding_state": assessment.understanding_state,
            },
            input_attestation_version=str(latest_chr.input_attestation_version),
            model_or_rule_version={"provider": "rule", "model_version": CAF_RULE_VERSION},
            upstream_lineage={
                "uar_id": assessment.uar_ref,
                "pinned_chr": assessment.pinned_chr,
                "latest_chr": assessment.latest_chr,
            },
            recompute_trigger=recompute_trigger,
            supersedes_chr_id=supersedes,
            provenance_ref={"emitted_by": "evaluate"},
        )
        persisted = chr_repo.append(record)
        chr_id = str(persisted.chr_id)
        seam.emit(
            "cognition_history_record_appended",
            {
                "project_id": project_id,
                "chr_id": chr_id,
                "output_kind": OUTPUT_KIND_ACCEPTANCE_IMPACT,
                "supersedes_chr_id": supersedes,
            },
        )
        # OBS-WU-ACCEPT C3 — "Acceptance-Impact Assessment emitted": the audit of
        # which confirmed decision drifted (uar + pinned vs latest CHR lineage).
        seam.emit(
            "acceptance_impact_assessed",
            {
                "project_id": project_id,
                "chr_id": chr_id,
                "uar_id": assessment.uar_ref,
                "pinned_chr": assessment.pinned_chr,
                "latest_chr": assessment.latest_chr,
                "delta": assessment.delta,
                "band_changed": assessment.band_changed,
                "supersedes_chr_id": supersedes,
            },
        )

    return raised


def build_and_register_wave_u_chain(
    *,
    provider: Any,
    extract_infer_inputs: Callable[[Any], dict[str, Any]],
    tier: str = "free",
    mode: str = "fast",
    user: str = "anonymous",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
    prompt_suffix_for: Any = None,
) -> Any:
    """Build + register the full A→B→C chain (Wave C builder); return the chain.

    Wave U adds NO new graph stage — the Acceptance-Impact reconcile runs AFTER
    the recompute via ``reconcile_acceptance_impact`` (called by the recompute
    wiring / the live e2e once the chain's new values have landed). Composing here
    keeps the A→B→C + reconcile composition in one additive module mirroring
    ``wave_c.py``; it edits NO frozen file (only the Wave C builder is CALLED).
    """
    from backend.orchestration.wave_c import build_and_register_wave_c_chain

    return build_and_register_wave_c_chain(
        provider=provider,
        extract_infer_inputs=extract_infer_inputs,
        tier=tier,
        mode=mode,
        user=user,
        confidence_stage=confidence_stage,
        understanding_state=understanding_state,
        prompt_suffix_for=prompt_suffix_for,
    )

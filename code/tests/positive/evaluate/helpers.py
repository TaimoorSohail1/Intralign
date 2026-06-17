"""Shared builders for the Wave B Evaluate suites (DTM-0011; offline, rule-only).

Evaluate is rule-arithmetic — it makes NO provider call — so these helpers build
``Finding`` objects + a ``SynthesizedPlanningModel`` directly (the upstream Infer
outputs) and run the engine/stage over them. No recorded fixture is needed for
Evaluate itself; the live e2e (Part B) drives the whole chain through the
recorded-fixture harness.
"""

from __future__ import annotations

from backend.responsibilities.evaluate.engine import EvaluateEngine
from shared.epistemic import (
    Finding,
    FlaggedAssumption,
    SynthesizedPlanningModel,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
OUTCOME_ANCHOR = "outcome-ref"
ASSERTION_IDS = ["assertion-0", "assertion-1", "assertion-2", "assertion-3"]


def finding(
    *,
    finding_type: str = "gap",
    gap_kind: str | None = "coverage",
    summary: str = "A structural implication.",
    anchors: tuple[str, ...] = ("assertion-0",),
    fid: str | None = None,
    mode: str = "fast",
    confidence_stage: str = "orientation",
) -> Finding:
    """A Derived Finding (the upstream Infer output Evaluate consumes)."""
    return Finding(
        project_id=PROJECT,
        finding_type=finding_type,  # type: ignore[arg-type]
        finding_id=fid or f"{finding_type}-{gap_kind or 'x'}-{abs(hash(summary)) % 10**8}",
        summary=summary,
        evidence_anchors=anchors,
        gap_kind=gap_kind,  # type: ignore[arg-type]
        model_or_rule_version="wb-infer-finding-v0",
        mode=mode,  # type: ignore[arg-type]
        confidence_stage=confidence_stage,  # type: ignore[arg-type]
    )


def coverage_gap() -> Finding:
    return finding(finding_type="gap", gap_kind="coverage",
                   summary="No constraint evidence is attested.", anchors=("assertion-0",),
                   fid="gap-coverage-1")


def alignment_gap() -> Finding:
    return finding(finding_type="gap", gap_kind="alignment",
                   summary="Scope omits the payments integration.", anchors=("assertion-2",),
                   fid="gap-alignment-1")


def conflict() -> Finding:
    return finding(finding_type="conflict", gap_kind=None,
                   summary="Attested assertions contradict (surfaced, not resolved).",
                   anchors=("assertion-0", "assertion-1"), fid="conflict-1")


def risk() -> Finding:
    return finding(finding_type="risk", gap_kind=None,
                   summary="Feasibility risk: rollout depends on an unstable service.",
                   anchors=("assertion-2", "assertion-3"), fid="risk-1")


def synthesized_model(
    *, mode: str = "fast", confidence_stage: str = "orientation",
    n_assumptions: int = 1,
) -> SynthesizedPlanningModel:
    """A minimal DTM-0009 synthesized model the Evaluate engine seeds from (PS-03)."""
    assumptions = tuple(
        FlaggedAssumption(
            statement=f"assumption {i}", covers_gap=f"gap {i}"
        )
        for i in range(n_assumptions)
    )
    return SynthesizedPlanningModel(
        project_id=PROJECT,
        model_version="ws-synth-llm-v0",
        intent_summary="Ship the billing rollout.",
        scope_summary="Deliver billing.",
        derived_from_assertions=tuple(ASSERTION_IDS),
        flagged_assumptions=assumptions,
        mode=mode,  # type: ignore[arg-type]
        confidence_stage=confidence_stage,  # type: ignore[arg-type]
    )


def engine(*, mode: str = "fast", confidence_stage: str = "orientation",
           tier: str = "free", user: str = "user-1") -> EvaluateEngine:
    return EvaluateEngine(
        tier=tier, mode=mode, user=user, confidence_stage=confidence_stage,  # type: ignore[arg-type]
    )

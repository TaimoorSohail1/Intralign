"""Shared builders for the Wave C Advise suites (DTM-0014; offline, recorded fixtures).

Advise text is AI-text -> driven by the recorded-fixture harness in CI (zero
provider calls). These helpers build the upstream Finding/Issue objects (the
Infer/Evaluate outputs Advise consumes) with STABLE ids so the recorded fixture
can anchor its recommendations/clarifications to them, and wire an
``AdviseEngine`` over the ``wc_advise_v0`` fixture.
"""

from __future__ import annotations

from backend.responsibilities.advise.engine import AdviseEngine
from backend.responsibilities.evaluate.engine import EvaluateEngine
from backend.services.llm_provider import LLMProvider
from shared.epistemic import Finding, Issue
from tests._fixtures.recorded_model_responses import (
    RecordedModelSession,
    build_recorded_model,
    response_key_directive,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
ASSERTION_IDS = ("assertion-0", "assertion-1", "assertion-2", "assertion-3")

# Stable Finding ids the fixture anchors to (must match wc_advise_v0.json).
COVERAGE_GAP_ID = "gap-coverage-1"
CONFLICT_ID = "conflict-1"
RISK_ID = "risk-1"


def finding(
    *,
    finding_type: str = "gap",
    gap_kind: str | None = "coverage",
    summary: str = "A structural implication.",
    anchors: tuple[str, ...] = ("assertion-0",),
    fid: str = "gap-coverage-1",
    mode: str = "fast",
    confidence_stage: str = "orientation",
) -> Finding:
    """A Derived Finding (the upstream Infer output Advise consumes)."""
    return Finding(
        project_id=PROJECT,
        finding_type=finding_type,  # type: ignore[arg-type]
        finding_id=fid,
        summary=summary,
        evidence_anchors=anchors,
        gap_kind=gap_kind,  # type: ignore[arg-type]
        model_or_rule_version="wb-infer-finding-v0",
        mode=mode,  # type: ignore[arg-type]
        confidence_stage=confidence_stage,  # type: ignore[arg-type]
    )


def coverage_gap() -> Finding:
    return finding(
        finding_type="gap", gap_kind="coverage",
        summary="No constraint evidence is attested.", anchors=("assertion-0",),
        fid=COVERAGE_GAP_ID,
    )


def conflict() -> Finding:
    return finding(
        finding_type="conflict", gap_kind=None,
        summary="Attested assertions contradict (surfaced, not resolved).",
        anchors=("assertion-0", "assertion-1"), fid=CONFLICT_ID,
    )


def risk() -> Finding:
    return finding(
        finding_type="risk", gap_kind=None,
        summary="Feasibility risk: rollout depends on an unstable service.",
        anchors=("assertion-2", "assertion-3"), fid=RISK_ID,
    )


def issue_from(f: Finding, *, mode: str = "fast",
               confidence_stage: str = "orientation") -> Issue:
    """Form the Issue Evaluate would produce from a Finding (rule-based, no provider)."""
    return EvaluateEngine(
        tier="free", mode=mode, confidence_stage=confidence_stage,  # type: ignore[arg-type]
    ).form_issue(f)


def key_directive(step_to_key: dict[str, str] | None = None):
    """A ``prompt_suffix_for`` that maps each step key to a fixture response key.

    The default maps each step to its same-named fixture key (the engine's
    ``step_key`` IS the fixture key). A mapping override lets a NEGATIVE test
    select a deliberately-bad recorded response (e.g. an unanchored recommendation
    or an empty array) without touching the engine.
    """
    mapping = step_to_key or {}

    def directive(step: str) -> str:
        return response_key_directive(mapping.get(step, step))

    return directive


def advise_engine(
    *,
    fixture: str = "wc_advise_v0",
    tier: str = "free",
    mode: str = "fast",
    user: str = "user-1",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
    step_to_key: dict[str, str] | None = None,
) -> tuple[AdviseEngine, RecordedModelSession]:
    session = build_recorded_model(fixture)
    provider = LLMProvider(recorded_model=session.model())
    engine = AdviseEngine(
        provider=provider,
        tier=tier,
        mode=mode,  # type: ignore[arg-type]
        user=user,
        confidence_stage=confidence_stage,  # type: ignore[arg-type]
        understanding_state=understanding_state,  # type: ignore[arg-type]
        prompt_suffix_for=key_directive(step_to_key),
    )
    return engine, session

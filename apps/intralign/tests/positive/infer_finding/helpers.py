"""Shared builders for the Wave B Finding suites (offline; recorded fixtures)."""

from __future__ import annotations

from backend.responsibilities.infer.finding import FindingEngine
from backend.responsibilities.perceive.extraction import AssertionDraft
from backend.services.llm_provider import LLMProvider
from shared.epistemic import SynthesizedPlanningModel
from tests._fixtures.recorded_model_responses import (
    RecordedModelSession,
    build_recorded_model,
    response_key_directive,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
ARTIFACT = "44444444-4444-4444-4444-444444444444"
SOURCE = "evidence-source-7"
OUTCOME_ANCHOR = "outcome-ref"
DECLARED_OUTCOME = "Deliver the billing rollout."  # NOT SMART (no measure / date)
SMART_OUTCOME = "Deliver the billing rollout by Q3 with 99% uptime."  # SMART

# Assertion ids the engine anchors Findings to (the AttestedAssertion ids).
ASSERTION_IDS = ["assertion-0", "assertion-1", "assertion-2", "assertion-3"]


def draft(content_type: str, proposition: str) -> AssertionDraft:
    """A typed, source-attributed evidence draft (no cognition)."""
    return AssertionDraft(
        content_type=content_type,
        proposition=proposition,
        attesting_source=SOURCE,
        source_ref={"artifact_id": ARTIFACT, "locus": {"section": 0, "line": 0}},
    )


def sample_drafts() -> list[AssertionDraft]:
    """Attested assertions WITHOUT a constraint -> a rule-structural coverage gap.

    Includes a negation pair (assertion-0 vs assertion-1) sharing content so the
    rule-structural conflict detector surfaces a contradiction (EXACT tier).
    A dependency (assertion-2) and an assumption (assertion-3) are present, but
    NO constraint -> a coverage gap is derived deterministically.
    """
    return [
        draft("fact", "The rollout will finish by Q3."),
        draft("fact", "The rollout will not finish by Q3."),
        draft("dependency", "Billing depends on the payments service."),
        draft("assumption", "We assume headcount stays flat."),
    ]


def synthesized_model(*, mode: str = "fast") -> SynthesizedPlanningModel:
    """A minimal DTM-0009 synthesized model the Finding engine reads from."""
    from shared.epistemic import FlaggedAssumption

    return SynthesizedPlanningModel(
        project_id=PROJECT,
        model_version="ws-synth-llm-v0",
        intent_summary="Ship the billing rollout.",
        scope_summary="Deliver billing.",
        derived_from_assertions=tuple(ASSERTION_IDS),
        flagged_assumptions=(
            FlaggedAssumption(
                statement="The payments service API is stable.",
                covers_gap="No dependency-stability evidence was attested.",
            ),
        ),
        mode=mode,  # type: ignore[arg-type]
    )


def finding_engine(
    *,
    fixture: str = "wb_infer_v0",
    tier: str = "free",
    mode: str = "fast",
    user: str = "user-1",
    confidence_stage: str = "orientation",
    understanding_state: str = "initial",
) -> tuple[FindingEngine, RecordedModelSession]:
    session = build_recorded_model(fixture)
    provider = LLMProvider(recorded_model=session.model())
    engine = FindingEngine(
        provider=provider,
        tier=tier,
        mode=mode,  # type: ignore[arg-type]
        user=user,
        confidence_stage=confidence_stage,  # type: ignore[arg-type]
        understanding_state=understanding_state,  # type: ignore[arg-type]
        prompt_suffix_for=response_key_directive,
    )
    return engine, session

"""Shared builders for the Wave S synthesis suites (offline; recorded fixtures)."""

from __future__ import annotations

from backend.responsibilities.infer.synthesis import SynthesisEngine
from backend.responsibilities.perceive.extraction import AssertionDraft, LLMClaimExtractor
from backend.services.llm_provider import LLMProvider
from tests._fixtures.recorded_model_responses import (
    RecordedModelSession,
    build_recorded_model,
    response_key_directive,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
ARTIFACT = "44444444-4444-4444-4444-444444444444"
SOURCE = "evidence-source-7"

SAMPLE = (
    "# Delivery plan\n"
    "The team ships monthly.\n"
    "- The rollout must finish by Q3.\n"
    "- Billing depends on the payments service.\n"
    "- We assume headcount stays flat.\n"
)


def draft(content_type: str, proposition: str) -> AssertionDraft:
    """A typed, source-attributed evidence draft (no cognition)."""
    return AssertionDraft(
        content_type=content_type,
        proposition=proposition,
        attesting_source=SOURCE,
        source_ref={"artifact_id": ARTIFACT, "locus": {"section": 0, "line": 0}},
    )


def sample_drafts() -> list[AssertionDraft]:
    return [
        draft("fact", "The team ships monthly."),
        draft("constraint", "The rollout must finish by Q3."),
        draft("dependency", "Billing depends on the payments service."),
        draft("assumption", "We assume headcount stays flat."),
    ]


def extractor_session() -> tuple[LLMClaimExtractor, RecordedModelSession]:
    session = build_recorded_model("ws_extraction_v0")
    extractor = LLMClaimExtractor(
        session.model(), prompt_suffix=response_key_directive("delivery_plan")
    )
    return extractor, session


def synthesis_engine(
    *,
    fixture: str = "ws_synthesis_v0",
    tier: str = "free",
    mode: str = "fast",
    user: str = "user-1",
) -> tuple[SynthesisEngine, RecordedModelSession]:
    session = build_recorded_model(fixture)
    provider = LLMProvider(recorded_model=session.model())
    engine = SynthesisEngine(
        provider=provider,
        tier=tier,
        mode=mode,
        user=user,
        prompt_suffix_for=response_key_directive,
    )
    return engine, session

"""QA-WS-SYNTH B2 (Perceive extraction) — source-attributed, correctly-typed,
re-derivable claims, with NO Derived cognition (A3.1/A3.2).

The LLM-backed ``ClaimExtractor`` (behind the same Protocol as the rule-based
one) turns admitted evidence into evidence-attested ``AssertionDraft``s: each
typed (fact/assumption/constraint/dependency), attributed to its artifact +
evidence source, and re-derivable to a locus in the normalized form. It is
driven OFFLINE by a recorded model-response fixture — zero provider calls.
"""

from __future__ import annotations

from backend.responsibilities.perceive.extraction import (
    LLM_EXTRACTION_VERSION,
    AssertionDraft,
    ClaimExtractor,
    LLMClaimExtractor,
)
from shared.epistemic import PlanningArtifact, SynthesizedPlanningModel
from tests.positive.synthesis.helpers import (
    ARTIFACT,
    SAMPLE,
    SOURCE,
    extractor_session,
)


def _normalized_form() -> dict:
    return {"text": SAMPLE, "sections": [{"index": 0, "lines": SAMPLE.splitlines()}]}


def _extract() -> tuple[list[AssertionDraft], object]:
    extractor, session = extractor_session()
    drafts = extractor.extract(
        artifact_id=ARTIFACT,
        normalized_form=_normalized_form(),
        attesting_source=SOURCE,
    )
    return drafts, session


def test_b2_extraction_is_source_attributed_and_correctly_typed() -> None:
    drafts, _ = _extract()
    by_type = {(d.content_type, d.proposition) for d in drafts}
    assert ("fact", "The team ships monthly.") in by_type
    assert ("constraint", "The rollout must finish by Q3.") in by_type
    assert ("dependency", "Billing depends on the payments service.") in by_type
    assert ("assumption", "We assume headcount stays flat.") in by_type
    for d in drafts:
        # Attributed to the artifact + the evidence source (never 'oslo').
        assert d.attesting_source == SOURCE
        assert d.source_ref["artifact_id"] == ARTIFACT
        assert d.source_ref["extractor"] == LLM_EXTRACTION_VERSION


def test_b2_extraction_claims_are_re_derivable_to_their_source_locus() -> None:
    drafts, _ = _extract()
    for d in drafts:
        assert d.re_derivable is True
        locus = d.source_ref["locus"]
        # The recorded claims match a normalized line -> a concrete {section,line}.
        assert locus["section"] == 0
        assert isinstance(locus["line"], int)


def test_b2_extraction_performs_no_derived_cognition() -> None:
    """Perceive emits Attested-evidence only — no severity/score/Derived (A3.2)."""
    drafts, _ = _extract()
    for d in drafts:
        assert d.epistemic_state == "attested-evidence"
        dumped = d.model_dump()
        for forbidden in ("severity", "score", "confidence", "finding"):
            assert forbidden not in dumped
        # The draft is NOT a synthesis/generation object — it is pre-cognition.
        assert not isinstance(d, (SynthesizedPlanningModel, PlanningArtifact))


def test_b2_extraction_runs_entirely_offline_on_a_recorded_fixture() -> None:
    """Zero provider calls: the fixture served the one extraction response."""
    _, session = _extract()
    assert session.call_count == 1
    assert session.served_keys == ["delivery_plan"]


def test_b2_llm_extractor_satisfies_the_claimextractor_protocol() -> None:
    extractor, _ = extractor_session()
    assert isinstance(extractor, ClaimExtractor)
    assert isinstance(extractor, LLMClaimExtractor)

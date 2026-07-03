"""DL-047 EI-02 positive — extraction yields typed, source-attributed drafts.

Determinism tier: EXACT (rule-based; same normalized_form -> identical drafts).
"""

from __future__ import annotations

from backend.responsibilities.perceive.extraction import (
    EXTRACTION_VERSION,
    AssertionDraft,
    ClaimExtractor,
    RuleBasedExtractor,
)
from backend.responsibilities.perceive.intake import normalize_content

ARTIFACT_ID = "44444444-4444-4444-4444-444444444444"
SOURCE = "evidence-source-7"

SAMPLE = (
    "# Delivery plan\n"
    "The team ships monthly.\n"
    "- The rollout must finish by Q3.\n"
    "- Billing depends on the payments service.\n"
    "- We assume headcount stays flat.\n"
    "- The API uses REST.\n"
)


def _extract() -> list[AssertionDraft]:
    return RuleBasedExtractor().extract(
        artifact_id=ARTIFACT_ID,
        normalized_form=normalize_content(SAMPLE),
        attesting_source=SOURCE,
    )


def test_extraction_produces_correctly_typed_drafts() -> None:
    drafts = _extract()
    by_type = {d.content_type: d.proposition for d in drafts}
    assert by_type["constraint"] == "The rollout must finish by Q3."      # E1 must/shall
    assert by_type["dependency"] == "Billing depends on the payments service."  # E2
    assert by_type["assumption"] == "We assume headcount stays flat."     # E3
    assert "fact" in by_type                                              # E4 fallback
    assert {d.proposition for d in drafts if d.content_type == "fact"} == {
        "The team ships monthly.",
        "The API uses REST.",
    }


def test_every_draft_is_source_attributed_and_re_derivable() -> None:
    """DL-047 required: source attribution + re-derivability on EVERY draft."""
    drafts = _extract()
    assert drafts  # extraction is not vacuous
    for draft in drafts:
        assert draft.attesting_source == SOURCE          # the evidence-source id
        assert draft.source_ref["artifact_id"] == ARTIFACT_ID
        locus = draft.source_ref["locus"]
        assert set(locus) == {"section", "line"}          # artifact + locus
        assert draft.re_derivable is True
        assert draft.epistemic_state == "attested-evidence"


def test_locus_points_back_into_the_normalized_form() -> None:
    form = normalize_content(SAMPLE)
    for draft in _extract():
        locus = draft.source_ref["locus"]
        line = form["sections"][locus["section"]]["lines"][locus["line"]]
        # The proposition is exactly that line, minus any bullet marker.
        assert draft.proposition in line


def test_extraction_is_deterministic_exact_tier() -> None:
    """Record/rule determinism tier: byte-identical drafts, in order."""
    first, second = _extract(), _extract()
    assert first == second
    assert [d.model_dump() for d in first] == [d.model_dump() for d in second]


def test_extractor_satisfies_the_seam_protocol() -> None:
    """Decision #5: the LLM extractor later registers behind the SAME seam."""
    assert isinstance(RuleBasedExtractor(), ClaimExtractor)
    assert RuleBasedExtractor.version == EXTRACTION_VERSION


def test_headings_and_blank_lines_yield_no_drafts() -> None:
    drafts = RuleBasedExtractor().extract(
        artifact_id=ARTIFACT_ID,
        normalized_form=normalize_content("# Only a heading\n\n## Another\n"),
        attesting_source=SOURCE,
    )
    assert drafts == []

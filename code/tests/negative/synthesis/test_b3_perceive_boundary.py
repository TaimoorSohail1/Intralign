"""QA-WS-SYNTH B3 (Perceive boundary) — extraction can emit NO Derived cognition,
and NO unattributed assertion.

A4.1 forbids Perceive emitting a Finding/severity/confidence (Critical: it would
be Derived-as-Attested), and forbids admitting an UNATTRIBUTED "fact" (Major:
missing source attribution). The ``AssertionDraft`` shape makes the first
structurally impossible (``extra='forbid'`` + pinned ``attested-evidence``), and
the second is rejected by required attribution fields. Each impossibility is a
test (a contract negative is a real test, not a comment).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.responsibilities.perceive.extraction import AssertionDraft
from tests.positive.synthesis.helpers import ARTIFACT, SOURCE


def _ref() -> dict:
    return {"artifact_id": ARTIFACT, "locus": {"section": 0, "line": 0}}


def test_b3_draft_cannot_carry_a_severity_or_confidence_field() -> None:
    """CRITICAL — a Derived-cognition field on an extraction draft is rejected."""
    for forbidden in ("severity", "confidence", "score", "finding"):
        with pytest.raises(ValidationError):
            AssertionDraft(
                content_type="fact",
                proposition="x",
                attesting_source=SOURCE,
                source_ref=_ref(),
                **{forbidden: 1},
            )


def test_b3_draft_cannot_claim_a_derived_epistemic_state() -> None:
    """CRITICAL — extraction is Attested-evidence; it can never be Derived-as-Attested."""
    with pytest.raises(ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="x",
            attesting_source=SOURCE,
            source_ref=_ref(),
            epistemic_state="derived",
        )


def test_b3_draft_cannot_be_marked_non_re_derivable() -> None:
    with pytest.raises(ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="x",
            attesting_source=SOURCE,
            source_ref=_ref(),
            re_derivable=False,
        )


def test_b3_unattributed_assertion_is_rejected_major() -> None:
    """MAJOR — a draft with no attesting source cannot be constructed."""
    with pytest.raises(ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="An unattributed fact.",
            source_ref=_ref(),
        )  # type: ignore[call-arg]  -- attesting_source omitted
    with pytest.raises(ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="An unattributed fact.",
            attesting_source=SOURCE,
        )  # type: ignore[call-arg]  -- source_ref omitted


def test_b3_perceive_extraction_module_exports_no_assessment_producer() -> None:
    """A4.1 introspection — Perceive's extractor surface has no Finding/Confidence."""
    import backend.responsibilities.perceive.extraction as extraction

    public = {name for name in dir(extraction) if not name.startswith("_")}
    for assessment in ("Finding", "Confidence", "CAFAssessment", "Issue"):
        assert assessment not in public

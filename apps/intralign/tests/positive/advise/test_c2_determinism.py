"""QA-WC-ADVISE C2 — determinism tiers (decision #8).

AI-text (recommendation/clarification SUMMARY/QUESTION) is SEMANTIC — never
exact-replay-asserted. The record-exact surface is the EMISSION: the anchor, the
type, the stable id, the output_kind. Set-level >=90% stable identities across
recompute (a re-derivation over the same structural input re-derives the same
ids — supersession targets them).
"""

from __future__ import annotations

from tests.positive.advise.helpers import (
    COVERAGE_GAP_ID,
    PROJECT,
    advise_engine,
    coverage_gap,
    risk,
)


def test_c2_anchor_and_type_are_record_exact() -> None:
    """The emission surface (anchor, type, id) is EXACT across two runs."""
    e1, _ = advise_engine()
    e2, _ = advise_engine()
    r1 = e1.derive(project_id=PROJECT, findings=[coverage_gap(), risk()])
    r2 = e2.derive(project_id=PROJECT, findings=[coverage_gap(), risk()])
    sig1 = sorted((r.anchor, r.recommendation_type, r.recommendation_id)
                  for r in r1.recommendations)
    sig2 = sorted((r.anchor, r.recommendation_type, r.recommendation_id)
                  for r in r2.recommendations)
    assert sig1 == sig2  # record-exact emission surface


def test_c2_recommendation_id_is_stable_for_same_structural_input() -> None:
    """The id is a stable structural hash — the SAME input re-derives the SAME id."""
    e1, _ = advise_engine()
    e2, _ = advise_engine()
    ids1 = {r.recommendation_id for r in
            e1.derive(project_id=PROJECT, findings=[coverage_gap()]).recommendations}
    ids2 = {r.recommendation_id for r in
            e2.derive(project_id=PROJECT, findings=[coverage_gap()]).recommendations}
    assert ids1 == ids2


def test_c2_text_is_semantic_not_asserted_byte_for_byte() -> None:
    """AI-text is semantic: the summary is non-empty + on-topic, never byte-pinned.

    (We assert the CONTRACT — a recommendation carries advisory text anchored to
    its finding — not an exact phrasing; a model-version change is a NEW baseline,
    not a regression, DT-6.)
    """
    engine, _ = advise_engine()
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap()])
    for_gap = [r for r in result.recommendations if r.anchor == COVERAGE_GAP_ID]
    assert for_gap
    for rec in for_gap:
        assert isinstance(rec.summary, str)
        assert rec.summary.strip()  # advisory text present (semantic tier)

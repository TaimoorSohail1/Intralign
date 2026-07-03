"""QA-WB-INFER B2 (determinism tiers; decision #10) — rule-structural Findings
EXACT, AI-derived Findings SEMANTIC, set-level >=90% stable identities across
recompute.

Rule-structural gaps/conflicts replay byte-identical (same input -> same
finding_id + summary). AI alignment/risk Findings are stable in identity (same
finding_id set) because they run off the recorded fixture (the model-version x
fixture baseline component). The stable ``finding_id`` is what supersession
targets, so a recompute over the same Attested set re-derives the SAME ids.
"""

from __future__ import annotations

from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    PROJECT,
    finding_engine,
    sample_drafts,
    synthesized_model,
)


def _derive_once():
    engine, session = finding_engine()
    result = engine.derive(
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS,
        model=synthesized_model(),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
    )
    return result, session


def test_rule_structural_findings_are_byte_identical_across_runs() -> None:
    """EXACT tier — coverage/SMART gaps + conflicts reproduce byte-for-byte."""
    a, _ = _derive_once()
    b, _ = _derive_once()
    rule_a = sorted(
        (f.finding_type, f.gap_kind, f.summary, f.evidence_anchors)
        for f in a.findings if f.gap_kind in (None, "coverage", "smart")
        and f.finding_type in ("gap", "conflict")
    )
    rule_b = sorted(
        (f.finding_type, f.gap_kind, f.summary, f.evidence_anchors)
        for f in b.findings if f.gap_kind in (None, "coverage", "smart")
        and f.finding_type in ("gap", "conflict")
    )
    assert rule_a == rule_b


def test_finding_id_set_is_at_least_90_percent_stable_across_recompute() -> None:
    """Set-level >=90% stable-identity overlap across a recompute (decision #10)."""
    a, _ = _derive_once()
    b, _ = _derive_once()  # a recompute over the SAME Attested set
    ids_a = {f.finding_id for f in a.findings}
    ids_b = {f.finding_id for f in b.findings}
    overlap = len(ids_a & ids_b) / max(len(ids_a | ids_b), 1)
    assert overlap >= 0.90
    assert ids_a == ids_b  # the recorded baseline is fully stable here


def test_same_finding_id_is_a_stable_supersession_target() -> None:
    """The same structural input re-derives the same id (supersession key)."""
    a, _ = _derive_once()
    b, _ = _derive_once()
    by_summary_a = {f.summary: f.finding_id for f in a.findings}
    by_summary_b = {f.summary: f.finding_id for f in b.findings}
    for summary, fid in by_summary_a.items():
        assert by_summary_b[summary] == fid


def test_determinism_baseline_is_stamped_on_the_fixture() -> None:
    _, session = _derive_once()
    assert session.fixture.model_version
    assert session.fixture.config

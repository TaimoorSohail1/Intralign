"""QA-WB-INFER B2 — Findings derived, TYPED (gap/conflict/risk), and ANCHORED.

The Finding engine derives the three Finding types from Attested knowledge + the
synthesized model + the declared-outcome reference, each anchored to the
AttestedAssertion id(s) it derives from (IC-WB-INFER 1.1 required-behavior #1/2).
Rule-structural gaps/conflicts are EXACT; AI alignment/risk Findings come from
the recorded fixture (SEMANTIC tier). Every Finding is Derived and carries a
non-empty evidence anchor (a missing anchor is impossible by construction).
"""

from __future__ import annotations

from shared.epistemic import EpistemicState
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    finding_engine,
    sample_drafts,
    synthesized_model,
)


def _derive(**overrides):
    engine, session = finding_engine(**overrides.pop("engine_kwargs", {}))
    kwargs = dict(
        project_id="11111111-1111-1111-1111-111111111111",
        assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS,
        model=synthesized_model(),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
    )
    kwargs.update(overrides)
    result = engine.derive(**kwargs)
    return result, session


def test_b2_findings_are_derived_and_each_anchored() -> None:
    result, _ = _derive()
    assert result.findings, "at least one Finding must be derived"
    for finding in result.findings:
        assert finding.epistemic_state is EpistemicState.DERIVED
        assert finding.evidence_anchors  # non-empty anchor — IC-WB-INFER invariant


def test_b2_all_three_finding_types_are_produced_and_typed() -> None:
    """Gap (coverage/SMART + AI alignment), Conflict, Risk — typed correctly."""
    result, _ = _derive()
    types = {f.finding_type for f in result.findings}
    assert types == {"gap", "conflict", "risk"}
    for finding in result.findings:
        assert finding.finding_type in {"gap", "conflict", "risk"}


def test_b2_rule_structural_coverage_gap_is_derived_exact() -> None:
    """EXACT tier — the missing-constraint coverage gap is derived without a model."""
    result, _ = _derive()
    coverage = [f for f in result.of_type("gap") if f.gap_kind == "coverage"]
    assert any("constraint" in f.summary for f in coverage)
    # Anchored to the Attested set it was evaluated over.
    assert all(set(f.evidence_anchors) <= set(ASSERTION_IDS) for f in coverage)


def test_b2_rule_structural_smart_gap_for_non_measurable_outcome() -> None:
    """EXACT tier — a declared outcome with no measurable terms -> a SMART gap."""
    result, _ = _derive()
    smart = [f for f in result.of_type("gap") if f.gap_kind == "smart"]
    assert smart, "a non-SMART declared outcome must surface a SMART gap"
    assert all(f.evidence_anchors == (OUTCOME_ANCHOR,) for f in smart)


def test_b2_smart_outcome_produces_no_smart_gap() -> None:
    """A SMART declared outcome (date + metric) yields no SMART gap (EXACT)."""
    from tests.positive.infer_finding.helpers import SMART_OUTCOME

    result, _ = _derive(declared_outcome=SMART_OUTCOME)
    assert not [f for f in result.of_type("gap") if f.gap_kind == "smart"]


def test_b2_conflict_is_surfaced_anchored_to_both_assertions() -> None:
    """A negation pair surfaces ONE conflict Finding anchored to BOTH assertions."""
    result, _ = _derive()
    conflicts = result.of_type("conflict")
    assert len(conflicts) == 1
    anchors = set(conflicts[0].evidence_anchors)
    assert anchors == {"assertion-0", "assertion-1"}
    # Surfaced, NOT resolved — the summary names both, picks no winner.
    assert "surfaced, not resolved" in conflicts[0].summary


def test_b2_risk_signals_come_from_the_model_anchored() -> None:
    """SEMANTIC tier — risk Findings from the recorded fixture, each anchored."""
    result, session = _derive()
    risks = result.of_type("risk")
    assert risks
    valid = set(ASSERTION_IDS) | {OUTCOME_ANCHOR}
    for r in risks:
        assert set(r.evidence_anchors) <= valid
    assert "risk" in session.served_keys  # the model pass actually ran


def test_b2_ai_findings_with_no_resolvable_anchor_are_dropped() -> None:
    """A model Finding whose anchors don't resolve to a real assertion is dropped."""
    from tests.positive.infer_finding.helpers import finding_engine

    engine, _ = finding_engine()
    # Point the alignment pass at the unanchored recorded response.
    engine.prompt_suffix_for = lambda step: (
        "[[response_key:alignment_unanchored]]" if step == "alignment"
        else f"[[response_key:{step}]]"
    )
    result = engine.derive(
        project_id="11111111-1111-1111-1111-111111111111",
        assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS,
        model=synthesized_model(),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
    )
    # The alignment Finding (nonexistent-id anchor) is NOT admitted.
    assert all(
        "no resolvable anchor" not in f.summary for f in result.findings
    )


def test_b2_finding_version_is_stamped_for_determinism() -> None:
    from backend.responsibilities.infer.finding import FINDING_VERSION

    result, _ = _derive()
    assert all(f.model_or_rule_version == FINDING_VERSION for f in result.findings)

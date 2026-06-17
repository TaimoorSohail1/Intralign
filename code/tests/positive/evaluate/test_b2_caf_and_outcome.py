"""QA-WB-EVAL B2 — CAF aggregation, Outcome Confidence, reliability qualifier,
Non-Collapse invariant, and CONF-06 false confidence.

The three co-equal CAF dimensions consolidate through the v0 power mean (between
an average and a minimum); reliability is a SEPARATE qualifier (never multiplied
in); the band derives from the index ALONE (Non-Collapse).
"""

from __future__ import annotations

from backend.responsibilities.evaluate.scoring import band_for, power_mean
from shared.epistemic import CAFAssessment, OutcomeConfidence
from tests.positive.evaluate.helpers import (
    PROJECT,
    conflict,
    coverage_gap,
    engine,
    risk,
    synthesized_model,
)


def test_b2_caf_has_three_co_equal_dimensions_each_a_triple() -> None:
    eng = engine()
    result = eng.assess(
        project_id=PROJECT,
        findings=[coverage_gap(), conflict(), risk()],
        model=synthesized_model(),
    )
    caf = result.caf
    assert isinstance(caf, CAFAssessment)
    dims = {d.dimension for d in caf.dimensions()}
    assert dims == {"clarity", "alignment", "feasibility"}
    # Each dimension is a (index · band · per-dim reliability) triple.
    for d in caf.dimensions():
        assert 0.0 <= d.index <= 100.0
        assert d.band in ("low", "medium", "high")
        assert d.reliability in ("low", "moderate", "high")


def test_b2_findings_reduce_their_located_dimension_only() -> None:
    # A risk reduces FEASIBILITY (not clarity/alignment); structure, not coefficient.
    eng = engine()
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    assert result.caf.feasibility.index < 100.0
    assert result.caf.clarity.index == 100.0
    assert result.caf.alignment.index == 100.0


def test_b2_outcome_confidence_is_power_mean_of_the_three_dims() -> None:
    eng = engine()
    result = eng.assess(
        project_id=PROJECT, findings=[coverage_gap(), risk()], model=synthesized_model()
    )
    oc = result.outcome_confidence
    assert isinstance(oc, OutcomeConfidence)
    expected = power_mean(
        [result.caf.clarity.index, result.caf.alignment.index, result.caf.feasibility.index]
    )
    assert round(oc.index, 6) == round(expected, 6)
    assert oc.band == band_for(oc.index)


def test_b2_outcome_confidence_is_between_average_and_minimum() -> None:
    eng = engine()
    result = eng.assess(
        project_id=PROJECT, findings=[risk(), risk()], model=synthesized_model()
    )
    dims = [result.caf.clarity.index, result.caf.alignment.index, result.caf.feasibility.index]
    arithmetic = sum(dims) / 3
    minimum = min(dims)
    # Power mean (p<1) sits between the arithmetic mean and the minimum.
    assert minimum - 1e-6 <= result.outcome_confidence.index <= arithmetic + 1e-6


def test_b2_reliability_is_a_separate_qualifier_never_multiplied_in() -> None:
    """Two runs with identical CAF inputs but different reliability → SAME index."""
    eng = engine()
    # High reliability: no coverage gaps, no assumptions.
    strong = eng.assess(
        project_id=PROJECT, findings=[risk()],
        model=synthesized_model(n_assumptions=0),
    )
    # Low reliability: same risk finding, but many assumptions (weak supportability).
    weak = eng.assess(
        project_id=PROJECT, findings=[risk()],
        model=synthesized_model(n_assumptions=5),
    )
    # The CAF/Outcome INDEX is identical — reliability did NOT enter the number.
    assert strong.outcome_confidence.index == weak.outcome_confidence.index
    # Only the qualifier LABEL differs.
    assert strong.reliability.level == "high"
    assert weak.reliability.level == "low"


def test_b2_non_collapse_low_reliability_alone_does_not_drive_very_low_band() -> None:
    """Strong CAF + low reliability → band stays from the index (NOT collapsed)."""
    eng = engine()
    # No findings → all dims 100 → strong CAF; but force low reliability (many
    # assumptions). The band must reflect the STRONG index, not the reliability.
    result = eng.assess(
        project_id=PROJECT, findings=[], model=synthesized_model(n_assumptions=5)
    )
    assert result.reliability.level == "low"
    assert result.outcome_confidence.band == "high"  # NOT collapsed to low
    assert result.outcome_confidence.index >= 75.0


def test_b2_conf06_false_confidence_high_band_on_low_reliability_is_flagged() -> None:
    """CONF-06 — high confidence built on low reliability is the dangerous 4th state."""
    eng = engine()
    result = eng.assess(
        project_id=PROJECT, findings=[], model=synthesized_model(n_assumptions=5)
    )
    assert result.outcome_confidence.band == "high"
    assert result.reliability.level == "low"
    assert result.outcome_confidence.false_confidence_flagged is True


def test_b2_no_false_confidence_when_reliability_is_adequate() -> None:
    eng = engine()
    result = eng.assess(
        project_id=PROJECT, findings=[], model=synthesized_model(n_assumptions=0)
    )
    assert result.outcome_confidence.band == "high"
    assert result.reliability.level == "high"
    assert result.outcome_confidence.false_confidence_flagged is False


def test_b2_confidence_reduces_to_its_basis_never_a_bare_number() -> None:
    eng = engine()
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    # The headline Confidence reduces to its basis (a non-empty, explainable list).
    assert result.confidence.basis
    assert any("rule_version=wb-eval-caf-v0" in b for b in result.confidence.basis)
    assert any("reliability=" in b for b in result.confidence.basis)

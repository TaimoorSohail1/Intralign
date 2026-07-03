"""QA-WB-EVAL B3 — CAF decomposability *(negative — DL-072 C2 / RB-026)*.

DL-062 Condition 1 (Doctrine 06 prevails): the confidence drivers folded into the
CAF dimensions — and the per-dimension reliability sub-axes — MUST remain
**individually inspectable** in the confidence basis/explanation; **an opaque
Clarity rollup is non-conformant**. DL-062 makes a QA negative test mandatory;
the existing B3 evaluate negatives cover Confidence-isn't-health, Reliability
non-collapse, CONF-06 and non-empty basis, but none asserted driver-level
decomposability. This file closes that gap.

"Decomposable" here means, structurally:
  1. a CAFAssessment exposes clarity / alignment / feasibility as three
     individually-addressable CAFDimensionScore triples (index · band · per-dim
     reliability) — not one consolidated scalar; and
  2. no opaque rollup field can shadow or replace that decomposition
     (``extra='forbid'`` makes a hidden composite structurally impossible); and
  3. the three drivers cannot collapse to fewer (every dimension is required).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from shared.epistemic import CAFAssessment, CAFDimensionScore
from tests.positive.evaluate.helpers import PROJECT, engine, risk, synthesized_model


def _dim(name: str) -> CAFDimensionScore:
    return CAFDimensionScore(dimension=name, index=80.0, band="high", reliability="high")


def test_b3_caf_exposes_three_individually_inspectable_dimensions() -> None:
    """Decomposability preserved: each CAF driver is addressable on its own."""
    caf = engine().assess(project_id=PROJECT, findings=[risk()], model=synthesized_model()).caf

    dims = caf.dimensions()
    assert len(dims) == 3
    assert {d.dimension for d in dims} == {"clarity", "alignment", "feasibility"}
    # Each dimension reduces to its OWN inspectable triple — not a shared rollup.
    for d in dims:
        assert 0.0 <= d.index <= 100.0
        assert d.band in ("low", "medium", "high")
        assert d.reliability in ("low", "moderate", "high")  # per-dimension sub-axis
    # The three are independently addressable (no opaque consolidated scalar leaks).
    dumped = caf.model_dump()
    for opaque in ("score", "rollup", "composite", "caf_score", "clarity_rollup", "overall"):
        assert opaque not in dumped
    assert {"clarity", "alignment", "feasibility"} <= set(dumped)


def test_b3_caf_assessment_forbids_an_opaque_rollup_field() -> None:
    """An opaque consolidated field cannot be smuggled onto a CAFAssessment."""
    for opaque in ("clarity_rollup", "caf_score", "composite", "score", "overall"):
        with pytest.raises(ValidationError):
            CAFAssessment(
                project_id=PROJECT,
                clarity=_dim("clarity"),
                alignment=_dim("alignment"),
                feasibility=_dim("feasibility"),
                model_or_rule_version="wb-eval-caf-v0",
                mode="fast",
                **{opaque: 87.0},  # extra='forbid' rejects an opaque rollup
            )


def test_b3_caf_dimension_score_forbids_a_hidden_opaque_field() -> None:
    """A single dimension cannot hide a non-inspectable scalar either."""
    for opaque in ("rollup", "score", "composite", "weight"):
        with pytest.raises(ValidationError):
            CAFDimensionScore(
                dimension="clarity", index=80.0, band="high", reliability="high",
                **{opaque: 0.9},
            )


def test_b3_caf_cannot_collapse_the_three_drivers() -> None:
    """The drivers cannot be reduced below three — no collapse into a rollup."""
    for missing in ("clarity", "alignment", "feasibility"):
        kwargs = {
            "project_id": PROJECT,
            "clarity": _dim("clarity"),
            "alignment": _dim("alignment"),
            "feasibility": _dim("feasibility"),
            "model_or_rule_version": "wb-eval-caf-v0",
            "mode": "fast",
        }
        del kwargs[missing]
        with pytest.raises(ValidationError):
            CAFAssessment(**kwargs)

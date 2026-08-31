"""QA-WB-EVAL B2 — severity → Issue + v0 per-dimension scoring & bands.

Evaluate assigns a severity ATTRIBUTE to a Finding (→ Issue) and computes the v0
per-dimension index (``100·Π(1−impactᵢ)``) with the ±3 edge-guarded band. The
finding TYPE is a label; the MAGNITUDE (impactᵢ) does the reducing.
"""

from __future__ import annotations

from backend.responsibilities.evaluate.config import IMPACT_MAGNITUDE_TABLE
from backend.responsibilities.evaluate.scoring import band_for, per_dimension_index
from shared.epistemic import Issue
from tests.positive.evaluate.helpers import (
    PROJECT,
    alignment_gap,
    conflict,
    coverage_gap,
    engine,
    risk,
)


def test_b2_severity_assigned_forms_issue_from_finding() -> None:
    eng = engine()
    issue = eng.form_issue(coverage_gap())
    assert isinstance(issue, Issue)
    assert issue.finding_id == "gap-coverage-1"
    assert issue.finding_type == "gap"
    # Severity is a LABEL (not a number); a coverage gap is moderate.
    assert issue.severity == "moderate"
    # Lineage carried from the source Finding (audit: which Finding became this).
    assert issue.evidence_anchors == ("assertion-0",)
    assert issue.project_id == PROJECT


def test_b2_severity_is_a_label_not_a_score_and_scales_with_magnitude() -> None:
    eng = engine()
    # A conflict / risk reads more severe than a coverage gap (urgent to surface).
    assert eng.form_issue(conflict()).severity == "high"
    assert eng.form_issue(risk()).severity == "high"
    assert eng.form_issue(alignment_gap()).severity == "high"
    assert eng.form_issue(coverage_gap()).severity == "moderate"
    # Severity is one of the LABELS — never a bare number leaking out.
    for issue in (eng.form_issue(conflict()), eng.form_issue(coverage_gap())):
        assert issue.severity in ("info", "low", "moderate", "high", "critical")


def test_b2_no_findings_dimension_is_full_confidence() -> None:
    # No findings → empty product → 100 (no detected weakness).
    assert per_dimension_index([]) == 100.0
    assert band_for(100.0) == "high"


def test_b2_single_material_weakness_caps_dimension_at_low_band() -> None:
    # v0 §1: a single material (0.55) weakness caps the dim at 45 → low band.
    material = IMPACT_MAGNITUDE_TABLE["material"]
    index = per_dimension_index([material])
    assert round(index, 2) == 45.0
    assert band_for(index) == "low"


def test_b2_band_edge_guard_pulls_to_lower_band() -> None:
    # Calibration §2 ±3 edge guard: within 3 of a boundary reads the LOWER band.
    assert band_for(74.0) == "medium"
    assert band_for(76.0) == "medium"   # within +3 of the 75 high boundary → medium
    assert band_for(78.0) == "high"
    assert band_for(49.0) == "low"
    assert band_for(52.0) == "low"      # within +3 of the 50 medium boundary → low
    assert band_for(53.0) == "medium"


def test_b2_findings_accumulate_multiplicatively_saturating() -> None:
    # Many small findings accumulate (damped union), never below 0.
    minor = IMPACT_MAGNITUDE_TABLE["minor"]
    index = per_dimension_index([minor] * 10)
    assert 0.0 <= index <= 100.0
    assert index < per_dimension_index([minor])  # more findings → lower (felt)

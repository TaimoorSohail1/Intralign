"""QA-WU-ACCEPT U2 (positive) — the PURE Acceptance-Impact compare (DTM-0017).

The drift compare is rule-derived (Calibration §3: ≥10 pts OR a band change vs
the version-pinned acceptance) — EXACT, band-stable, no LLM. These pin the rule
itself: ≥10 fires, a band change fires, below-threshold raises nothing.
"""

from __future__ import annotations

from backend.responsibilities.evaluate.acceptance_impact import (
    AcceptedValue,
    compare_acceptance_impact,
)
from backend.responsibilities.evaluate.config import ACCEPTANCE_IMPACT_DRIFT_POINTS


def test_threshold_is_the_calibration_constant_ten_points() -> None:
    """Calibration §3 — the drift trigger is the config constant, never hardcoded."""
    assert ACCEPTANCE_IMPACT_DRIFT_POINTS == 10.0


def test_ten_point_drop_is_drift() -> None:
    drift = compare_acceptance_impact(
        pinned=AcceptedValue(index=80.0, band="high"),
        latest=AcceptedValue(index=70.0, band="medium"),
    )
    assert drift.is_drift is True
    assert drift.delta == -10.0
    assert drift.band_changed is True


def test_exactly_ten_point_move_same_band_is_drift() -> None:
    """≥10 is inclusive — a 10-pt move within a band still fires."""
    drift = compare_acceptance_impact(
        pinned=AcceptedValue(index=60.0, band="medium"),
        latest=AcceptedValue(index=70.0, band="medium"),
    )
    assert drift.is_drift is True
    assert drift.delta == 10.0
    assert drift.band_changed is False


def test_band_change_under_ten_points_is_drift() -> None:
    """A band change alone fires even when the points move < 10 (Calibration §3)."""
    drift = compare_acceptance_impact(
        pinned=AcceptedValue(index=51.0, band="medium"),
        latest=AcceptedValue(index=48.0, band="low"),
    )
    assert drift.is_drift is True
    assert abs(drift.delta) < ACCEPTANCE_IMPACT_DRIFT_POINTS
    assert drift.band_changed is True


def test_below_threshold_same_band_is_not_drift() -> None:
    """< 10 pts AND same band → NOTHING (below-threshold raises no assessment)."""
    drift = compare_acceptance_impact(
        pinned=AcceptedValue(index=80.0, band="high"),
        latest=AcceptedValue(index=75.0, band="high"),
    )
    assert drift.is_drift is False
    assert drift.delta == -5.0
    assert drift.band_changed is False


def test_compare_is_deterministic_exact() -> None:
    """Rule-derived: same inputs → identical result every call (exact tier)."""
    pinned = AcceptedValue(index=82.4, band="high")
    latest = AcceptedValue(index=64.1, band="medium")
    a = compare_acceptance_impact(pinned=pinned, latest=latest)
    b = compare_acceptance_impact(pinned=pinned, latest=latest)
    assert a == b

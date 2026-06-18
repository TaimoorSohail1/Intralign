"""v0 CAF / Confidence scoring parameters (Calibration Defaults §4h; ADR-0006).

These are *dials, not architecture* (ANTI_ASSUMPTION_BUILD_PROTOCOL; v0 spec §6):
the owner may retune any value without a new Decision once telemetry exists.
They are transcribed VERBATIM from ``RELEASE_1_CALIBRATION_DEFAULTS_V1.md`` §4h
(and the §2 bands) — the binding source. The STRUCTURE (baseline-minus-impact
dimensions, power-mean aggregation, reliability-as-qualifier, band mapping) is
doctrine-fixed; only these MAGNITUDES are calibration.

NO hard pass/fail numeric threshold lives here or is asserted anywhere — the
canonical formula remains an owner-calibration decision (Open-TBD F1). The
calibration harness records the inputs needed to fit ``p``/``ε``/the impact
table from real cohorts later; it asserts only the doctrinal band/±7 tolerance,
never a numeric gate (Anti-Assumption).
"""

from __future__ import annotations

from typing import Literal

# §4h — the Finding impact-magnitude table (impactᵢ ∈ [0, 1]); sized from a
# Finding's Impact Assessment (significance × support × pervasiveness), NOT its
# type. Owner-tunable; calibrate against real finding-count distributions.
AssessedMagnitude = Literal["trivial", "minor", "moderate", "significant", "material"]

IMPACT_MAGNITUDE_TABLE: dict[str, float] = {
    "trivial": 0.03,
    "minor": 0.08,
    "moderate": 0.18,
    "significant": 0.35,
    "material": 0.55,
}

# §4h — the aggregation power-mean exponent (revised 0 → −0.5 after the v0
# pressure-test; sweet spot p ∈ [−1, 0]; p = 1 arithmetic forbidden as default).
POWER_MEAN_EXPONENT: float = -0.5

# §4h — the dimension floor ε (prevents hard weakest-link domination when a
# dimension ≈ 0; a true-zero dim → ~37 Low, not 0).
DIMENSION_FLOOR_EPSILON: float = 5.0

# Calibration §2 — band boundaries (0–49 Low / 50–74 Medium / 75–100 High) and
# the ±3-point band-edge guard (a value within guard of a boundary reads as the
# LOWER band — conservative; never overstate confidence).
MEDIUM_BAND_FLOOR: float = 50.0
HIGH_BAND_FLOOR: float = 75.0
BAND_EDGE_GUARD: float = 3.0

# A conservative default impact for a Finding whose Impact Assessment has not
# sized a magnitude yet (v0: treat an un-sized Finding as MODERATE so it is felt
# but does not dominate — the magnitude is refined by Deep Pass / calibration).
DEFAULT_MAGNITUDE: AssessedMagnitude = "moderate"


def impact_for_magnitude(magnitude: str) -> float:
    """Map an assessed-magnitude label to its v0 ``impactᵢ`` (§4h table).

    An unknown label falls back to the default magnitude's impact rather than
    guessing a number (ANTI_ASSUMPTION) — the magnitude is a calibration dial,
    never invented per-call.
    """
    return IMPACT_MAGNITUDE_TABLE.get(
        magnitude, IMPACT_MAGNITUDE_TABLE[DEFAULT_MAGNITUDE]
    )

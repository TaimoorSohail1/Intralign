"""Acceptance-Impact reconcile — the PURE drift compare (DTM-0017; IC-WU-ACCEPT U1.3).

When the understanding behind a user-ACCEPTED item later moves, OSLO surfaces it.
This module is the EVALUATE-owned (it owns value/band semantics; ADR-0009) PURE
COMPARE at the heart of the reconcile: given the value at the version-pinned
Cognition History Record and the LATEST value for the SAME accepted item, decide
whether the drift crosses the Acceptance-Impact threshold.

Drift = (|delta| ≥ 10 points) OR (the band changed) vs the version-pinned
acceptance (Calibration §3 — ``ACCEPTANCE_IMPACT_DRIFT_POINTS`` /
``band_changed``, read from config, never hardcoded here). Below the threshold
this raises NOTHING.

This is a RULE comparison — NO LLM, NO provider call (ADR-0004): it reads two
already-emitted values and applies the calibration rule. It is read-only over
the UAR and the plan fact (it neither holds nor mutates them). The drift it
returns (signed ``delta`` + ``band_changed``) is EXACT given the same two values
+ the pinned rule version — band-stable on replay.

The Acceptance-Impact Assessment it backs is DERIVED, never canonical / world-
truth (hard rule #2; the seven (G) forbidden) — this module only DECIDES drift;
the wiring (``orchestration/wave_u.py``) builds the Derived
``AcceptanceImpactAssessment`` + appends its CHR.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.responsibilities.evaluate.config import ACCEPTANCE_IMPACT_DRIFT_POINTS
from backend.responsibilities.evaluate.scoring import CAF_RULE_VERSION


@dataclass(frozen=True)
class AcceptedValue:
    """One value behind an accepted item: its 0–100 index + its band.

    The PINNED value is read from the CHR the acceptance version-pinned; the
    LATEST value is read from the latest CHR for the same accepted item (same
    project + output_kind). Both are data reads of an already-emitted payload —
    no interpretation, no LLM.
    """

    index: float
    band: str


@dataclass(frozen=True)
class DriftResult:
    """The rule-derived drift between the pinned and the latest value.

    ``is_drift`` is true iff the move crosses Calibration §3 (≥10 pts OR a band
    change). ``delta`` is the signed move (latest − pinned); ``band_changed``
    records the band transition. Both are carried onto the Derived
    ``AcceptanceImpactAssessment`` regardless of ``is_drift`` so the audit answers
    "how far did it move" even when nothing is raised.
    """

    is_drift: bool
    delta: float
    band_changed: bool
    pinned_band: str
    latest_band: str
    rule_version: str = CAF_RULE_VERSION


def compare_acceptance_impact(
    *,
    pinned: AcceptedValue,
    latest: AcceptedValue,
    drift_points: float = ACCEPTANCE_IMPACT_DRIFT_POINTS,
) -> DriftResult:
    """Decide Acceptance-Impact drift for one accepted item (PURE; no LLM).

    Drift fires when the value behind the accepted item moved ``≥ drift_points``
    OR changed band vs the version-pinned acceptance (Calibration §3). The
    threshold defaults to the calibration constant — a caller never invents a
    different number. Returns the full :class:`DriftResult` (the signed delta +
    band transition) so the assessment can record the move even below threshold.
    """
    delta = float(latest.index) - float(pinned.index)
    band_changed = pinned.band != latest.band
    crosses_points = abs(delta) >= float(drift_points)
    return DriftResult(
        is_drift=crosses_points or band_changed,
        delta=delta,
        band_changed=band_changed,
        pinned_band=pinned.band,
        latest_band=latest.band,
    )

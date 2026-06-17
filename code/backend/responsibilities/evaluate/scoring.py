"""v0 CAF / Confidence scoring arithmetic (ADR-0006; CAF_CONFIDENCE_V0_SCORING_FORMULA_V1).

This module implements the v0 formula EXACTLY — the arithmetic the ratified v2
models deliberately deferred to "future calibration" (Open-TBD F1). It is the
EXACT-replay tier of the determinism baseline: given the same inputs and the
same pinned ``rule_version``, the output is byte-identical (no AI, no clock, no
randomness). The AI-derived INPUTS (finding detection, impact sizing) replay
band-semantic (±7 / same band); the arithmetic here replays exact.

The formula (v0 spec §1–§3; Calibration §4h):

1. **Per-dimension** (§1): each dimension starts at 100 and is reduced
   multiplicatively by each Finding whose Impact Assessment locates it on that
   dimension — ``Dim = 100 · Π(1 − impactᵢ)``, clamped [0, 100]. ``impactᵢ`` is
   the finding's reducing magnitude (significance × support × pervasiveness),
   sized from its Impact Assessment, NOT its type. No findings → empty product
   → 100. A single *material* (0.55) weakness caps the dim at 45 (low band).
2. **Aggregation** (§2): consolidate the three FLOORED dims with a symmetric
   power mean ``( (c^p + a^p + f^p)/3 )^(1/p)`` (p ≠ 0; geometric for p = 0) —
   provably "between an average and a minimum". v0 ``p = −0.5``, floor ``ε = 5``.
   Symmetric in (C, A, F): co-equal, no static weight.
3. **Bands** (§3 / Calibration §2): 0–49 Low / 50–74 Medium / 75–100 High, with
   the ±3 edge guard (a value within 3 pts of a boundary is the LOWER band —
   never overstate).

Reliability is NOT computed here — it is a SEPARATE qualifier (Reliability Model
v2), produced alongside and NEVER multiplied into these numbers.

ANTI-ASSUMPTION: every numeric parameter (the impact table, ``p``, ``ε``, the
band edges) lives in :mod:`config` (Calibration §4h) — owner-tunable dials, NOT
hard-coded thresholds. The STRUCTURE is doctrine-fixed; the MAGNITUDES are
calibration. No pass/fail numeric threshold is asserted anywhere (that is F1,
owner-deferred); the calibration harness records inputs to fit them later.
"""

from __future__ import annotations

from collections.abc import Sequence

from backend.responsibilities.evaluate.config import (
    BAND_EDGE_GUARD,
    DIMENSION_FLOOR_EPSILON,
    HIGH_BAND_FLOOR,
    MEDIUM_BAND_FLOOR,
    POWER_MEAN_EXPONENT,
    impact_for_magnitude,
)

# The pinned rule version — the determinism baseline component for the v0
# arithmetic (ADR-0006: pin so rule-arithmetic replays EXACT). A change here is
# a NEW baseline, never a regression (DT-6).
CAF_RULE_VERSION = "wb-eval-caf-v0"


def per_dimension_index(impacts: Sequence[float]) -> float:
    """v0 §1 — ``Dim = 100 · Π(1 − impactᵢ)``, clamped [0, 100].

    Multiplicative (damped-union) accumulation: many findings saturate toward a
    floor and never drive a dimension below 0 (or sum past 100). No impacts →
    empty product → 100.0 (no detected weakness).
    """
    product = 1.0
    for impact in impacts:
        # Each impact is a reducing magnitude in [0, 1]; clamp defensively so a
        # malformed input can never push a dimension below 0 or above 100.
        clamped = min(max(float(impact), 0.0), 1.0)
        product *= 1.0 - clamped
    return _clamp_0_100(100.0 * product)


def per_dimension_index_from_magnitudes(magnitudes: Sequence[str]) -> float:
    """Per-dimension index from assessed-magnitude LABELS (§1 + §4h table).

    The magnitude label (trivial/minor/moderate/significant/material) maps to
    ``impactᵢ`` via the owner-tunable §4h table — the finding TYPE never enters.
    """
    return per_dimension_index([impact_for_magnitude(m) for m in magnitudes])


def power_mean(values: Sequence[float], *, p: float = POWER_MEAN_EXPONENT,
               epsilon: float = DIMENSION_FLOOR_EPSILON) -> float:
    """v0 §2 — power mean of the FLOORED dims (between an average and a minimum).

    Each value is floored at ``ε`` (prevents hard weakest-link domination when a
    dimension ≈ 0). ``p ≠ 0``: ``( (Σ vᵢ^p)/n )^(1/p)``; ``p = 0``: geometric
    mean. Symmetric in the inputs — the dimensions stay co-equal (no weights).
    """
    if not values:
        return 100.0
    floored = [max(float(v), float(epsilon)) for v in values]
    n = len(floored)
    if p == 0:
        # Geometric mean (the p→0 limit).
        product = 1.0
        for v in floored:
            product *= v
        return _clamp_0_100(product ** (1.0 / n))
    summed = sum(v ** p for v in floored)
    return _clamp_0_100((summed / n) ** (1.0 / p))


def band_for(index: float) -> str:
    """v0 §3 / Calibration §2 — map an index to a band with the ±3 edge guard.

    0–49 low / 50–74 medium / 75–100 high. The ±3 edge guard pulls a value
    within ``BAND_EDGE_GUARD`` points of a boundary DOWN to the lower band
    (conservative — never overstate confidence). Boundaries are config dials.
    """
    # High boundary: only "well above" the boundary counts as high.
    if index >= HIGH_BAND_FLOOR + BAND_EDGE_GUARD:
        return "high"
    # Medium boundary: within +guard of the medium floor still reads low.
    if index >= MEDIUM_BAND_FLOOR + BAND_EDGE_GUARD:
        return "medium"
    return "low"


def _clamp_0_100(value: float) -> float:
    return min(max(value, 0.0), 100.0)

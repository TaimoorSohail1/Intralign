"""Calibration harness SCAFFOLD for the v0 CAF/Confidence formula (ADR-0006; F1).

The v0 parameters (the ``impactᵢ`` table, the power-mean ``p``, the floor ``ε``,
the band edges) are owner-tunable dials to be CALIBRATED FROM REAL DATA once
telemetry exists (Open-TBD F1) — the v0 is what calibration *refines*, not a
blank. This harness RECORDS the inputs a future fit needs (the per-dimension
impacts, the consolidated index, the band, the reliability) so the owner can
fit ``p``/``ε``/the impact table against real cohorts.

ANTI_ASSUMPTION_BUILD_PROTOCOL: this scaffold asserts NO numeric pass/fail
threshold. There is no "score must be ≥ X" gate anywhere — the canonical
formula is an owner decision (F1), and inventing a threshold would be assuming a
spec gap. The ONLY tolerances asserted in tests are the DOCTRINAL ones already
ratified (Calibration §1: exact for rule arithmetic; ±7 / same band for AI).

The harness is a recorder + a serializer; it does not judge. A test exercises it
to prove it records the right shape — never to assert a magnitude is "good".
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field

from backend.responsibilities.evaluate.scoring import CAF_RULE_VERSION


@dataclass(frozen=True)
class CalibrationSample:
    """One recorded scoring observation (the raw material a future fit needs).

    Records the INPUTS and the v0 OUTPUTS — never a pass/fail verdict. ``label``
    is an optional human/cohort tag (e.g. a project size) the owner correlates
    against; it carries no scoring meaning.
    """

    project_id: str
    dimension_indices: dict[str, float]
    dimension_impacts: dict[str, list[float]]
    outcome_index: float
    outcome_band: str
    reliability: str
    rule_version: str = CAF_RULE_VERSION
    label: str | None = None


@dataclass
class CalibrationRecorder:
    """Append-only recorder of calibration samples (no thresholds, no verdicts).

    The owner exports ``samples`` (or :meth:`to_jsonl`) to fit ``p``/``ε``/the
    impact table later. This recorder NEVER asserts a sample is acceptable — it
    has no notion of pass/fail (Anti-Assumption: the threshold is the owner's).
    """

    samples: list[CalibrationSample] = field(default_factory=list)

    def record(
        self,
        *,
        project_id: str,
        dimension_indices: dict[str, float],
        dimension_impacts: dict[str, Sequence[float]],
        outcome_index: float,
        outcome_band: str,
        reliability: str,
        label: str | None = None,
    ) -> CalibrationSample:
        """Record one observation; return it (the recorder makes no judgement)."""
        sample = CalibrationSample(
            project_id=project_id,
            dimension_indices=dict(dimension_indices),
            dimension_impacts={k: list(v) for k, v in dimension_impacts.items()},
            outcome_index=outcome_index,
            outcome_band=outcome_band,
            reliability=reliability,
            label=label,
        )
        self.samples.append(sample)
        return sample

    def to_jsonl(self) -> str:
        """Serialize the recorded samples as JSONL (the owner's fitting input)."""
        return "\n".join(json.dumps(asdict(s), sort_keys=True) for s in self.samples)

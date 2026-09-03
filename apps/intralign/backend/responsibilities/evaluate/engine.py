"""Wave B Evaluate engine (DTM-0011; IC-WB-EVAL 2.1) — Issue / Confidence /
Reliability / CAF / Outcome Confidence.

Evaluate is the SINGLE producer (one-producer rule #1) of the Understanding
layer's assessment values. It READS Findings (Infer) + the synthesized model
(PS-03 seed) and PRODUCES, all Derived:

- **Issue** — a Finding prioritized by an assigned **severity** attribute
  (severity → Issue; Severity is an attribute, Object Model §8). The severity
  LABEL comes from the Finding's type + its assessed magnitude — NEVER a leaked
  numeric score.
- **CAFAssessment** — Clarity / Alignment / Feasibility, three co-equal
  dimensions, each a (v0 index · band · per-dim reliability) triple. Each
  Finding reduces the dimension its Impact Assessment locates it on
  (``100·Π(1−impactᵢ)``); the finding TYPE is a label, the MAGNITUDE comes from
  the Impact Assessment (v0 spec §1; Calibration §4h).
- **OutcomeConfidence** — the three dims consolidated through the v0 power mean
  (between an average and a minimum), banded + reliability-qualified. Trust in
  UNDERSTANDING, never project health.
- **Confidence** — the headline trust-in-understanding band (the orientation /
  expanded / validated value), reliability-qualified, reducing to its basis.
- **Reliability** — a SEPARATE qualifier label (never multiplied into the
  numbers; Reliability Model v2), judged from coverage / evidence support.

FORBIDDEN here (IC-WB-EVAL 2.1; guardrails): NO Findings (Infer's), NO
recommendations/clarifications (Advise's), NO canonical write / promotion to
Attested, NO conflict resolution, NO interpretation acceptance, NO value change
outside recompute. Confidence is NEVER project health (the shapes forbid a
``score``/``health``/``probability`` field structurally).

CONF-06 false-confidence: a HIGH band built on LOW reliability/coverage is the
dangerous 4th state — flagged on the OutcomeConfidence and evented
(``false_confidence_flagged``), never silently dropped.

NON-COLLAPSE invariant (v0 doctrine): low reliability ALONE must not drive a
Very-Low band when the CAF arithmetic is strong — reliability QUALIFIES, it does
not enter the number. The band is computed from the index only; reliability is
attached alongside.

Determinism: the v0 arithmetic is EXACT under the pinned ``CAF_RULE_VERSION``
(scoring.py); the AI-derived inputs (impact sizing) are band-semantic (±7 / same
band). No provider is called here — Evaluate scores Findings, it does not
generate text.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass

from backend.responsibilities.evaluate.config import (
    DEFAULT_MAGNITUDE,
    impact_for_magnitude,
)
from backend.responsibilities.evaluate.scoring import (
    CAF_RULE_VERSION,
    band_for,
    per_dimension_index,
    power_mean,
)
from shared.epistemic import (
    CAFAssessment,
    CAFDimensionScore,
    Confidence,
    ConfidenceStage,
    Finding,
    Issue,
    Mode,
    OutcomeConfidence,
    Reliability,
    ReliabilityLevel,
    Severity,
    SynthesizedPlanningModel,
    UnderstandingState,
)

# Which CAF dimension a Finding reduces — by structure, NOT by a coefficient.
# Gaps reduce Clarity (or Alignment for an alignment gap); conflicts reduce
# Alignment (contradictions among Attested assertions); risks reduce
# Feasibility. The finding TYPE selects the dimension; the MAGNITUDE (impactᵢ)
# does the reducing (v0 §1 — type is never a coefficient).
_GAP_KIND_DIMENSION: dict[str, str] = {
    "coverage": "clarity",
    "quality": "clarity",
    "smart": "clarity",
    "alignment": "alignment",
}

# Severity LABEL by (finding_type, assessed magnitude). A LABEL, never a number:
# the magnitude sizes the reduction arithmetically (impactᵢ); the severity is a
# parallel descriptive attribute on the Issue. Conflicts and risks read one step
# more severe at the same magnitude (a contradiction / feasibility risk is more
# urgent to surface than a coverage gap of the same size).
_SEVERITY_BY_MAGNITUDE: dict[str, Severity] = {
    "trivial": "info",
    "minor": "low",
    "moderate": "moderate",
    "significant": "high",
    "material": "critical",
}


@dataclass(frozen=True)
class EvaluationResult:
    """The Derived outputs of one Evaluate run (IC-WB-EVAL) — all recomputable."""

    issues: tuple[Issue, ...]
    caf: CAFAssessment
    confidence: Confidence
    reliability: Reliability
    outcome_confidence: OutcomeConfidence
    understanding_state: UnderstandingState


@dataclass
class EvaluateEngine:
    """Assigns severity → Issues and computes the v0 CAF/Confidence assessment.

    ``reliability_basis`` / coverage are judged from the inputs (the synthesized
    model's flagged assumptions = uncertainty; the share of Findings that are
    coverage gaps = low coverage). No provider is called — Evaluate scores
    Findings; it never generates text (that is Infer / Advise).
    """

    tier: str = "free"
    mode: Mode = "fast"
    user: str = "anonymous"
    confidence_stage: ConfidenceStage = "orientation"

    # -- severity → Issue -----------------------------------------------------

    def form_issue(self, finding: Finding) -> Issue:
        """Form an Issue from a Finding by assigning a severity attribute.

        Severity is a LABEL derived from the Finding's assessed magnitude (and
        nudged up one step for conflicts/risks — more urgent to surface). It is
        NEVER a numeric score; the magnitude sizes the CAF reduction separately.
        """
        magnitude = self._magnitude_for(finding)
        severity = self._severity_for(finding.finding_type, magnitude)
        return Issue(
            project_id=finding.project_id,
            issue_id=self._issue_id(finding),
            finding_id=finding.finding_id,
            finding_type=finding.finding_type,
            severity=severity,
            summary=finding.summary,
            evidence_anchors=finding.evidence_anchors,
            model_or_rule_version=CAF_RULE_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state="initial",
        )

    # -- CAF / Confidence / Reliability / Outcome Confidence ------------------

    def assess(
        self,
        *,
        project_id: str,
        findings: Sequence[Finding],
        model: SynthesizedPlanningModel | None = None,
    ) -> EvaluationResult:
        """Compute the full Derived assessment from Findings (+ the PS-03 seed).

        PS-03: when a ``SynthesizedPlanningModel`` is supplied its flagged
        assumptions seed the reliability/coverage judgement (Evaluate's input is
        the model — DL-047). The CAF arithmetic is EXACT (v0); reliability is a
        SEPARATE qualifier (never multiplied in); the band derives from the
        index ALONE (Non-Collapse).
        """
        issues = tuple(self.form_issue(f) for f in findings)
        understanding_state = self._classify_understanding(findings=findings, model=model)
        reliability_level = self._reliability_level(findings=findings, model=model)

        # --- per-dimension v0 indices (100·Π(1−impactᵢ), clamped) -----------
        impacts_by_dim = self._impacts_by_dimension(findings)
        dim_scores = {
            dim: per_dimension_index(impacts_by_dim.get(dim, []))
            for dim in ("clarity", "alignment", "feasibility")
        }

        caf = CAFAssessment(
            project_id=project_id,
            clarity=self._dim_score("clarity", dim_scores["clarity"], reliability_level),
            alignment=self._dim_score("alignment", dim_scores["alignment"], reliability_level),
            feasibility=self._dim_score(
                "feasibility", dim_scores["feasibility"], reliability_level
            ),
            model_or_rule_version=CAF_RULE_VERSION,
            derived_from_findings=tuple(f.finding_id for f in findings),
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=understanding_state,
        )

        # --- aggregate: v0 power mean of the three FLOORED dims -------------
        outcome_index = power_mean(
            [dim_scores["clarity"], dim_scores["alignment"], dim_scores["feasibility"]]
        )
        outcome_band = band_for(outcome_index)  # band from the INDEX only (Non-Collapse)
        false_confidence = self._is_false_confidence(outcome_band, reliability_level)

        basis = self._basis(findings=findings, model=model, reliability=reliability_level)

        outcome_confidence = OutcomeConfidence(
            project_id=project_id,
            index=outcome_index,
            band=outcome_band,
            reliability_qualifier=reliability_level,
            false_confidence_flagged=false_confidence,
            basis=basis,
            model_or_rule_version=CAF_RULE_VERSION,
            derived_from_findings=tuple(f.finding_id for f in findings),
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=understanding_state,
        )

        # --- headline Confidence (trust in understanding) ------------------
        confidence = Confidence(
            project_id=project_id,
            index=outcome_index,
            band=outcome_band,
            reliability_qualifier=reliability_level,
            basis=basis,
            model_or_rule_version=CAF_RULE_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=understanding_state,
        )

        reliability = Reliability(
            project_id=project_id,
            level=reliability_level,
            basis=self._reliability_basis(findings=findings, model=model),
            model_or_rule_version=CAF_RULE_VERSION,
            mode=self.mode,
            confidence_stage=self.confidence_stage,
            understanding_state=understanding_state,
        )

        return EvaluationResult(
            issues=issues,
            caf=caf,
            confidence=confidence,
            reliability=reliability,
            outcome_confidence=outcome_confidence,
            understanding_state=understanding_state,
        )

    # -- internal: magnitude / severity / dimensions -------------------------

    def _magnitude_for(self, finding: Finding) -> str:
        """The assessed magnitude for a Finding (v0: from its sub-kind, defaulting).

        A real Impact Assessment will size this; the v0 maps the structural
        signal we have (a SMART/coverage gap is moderate; an alignment gap or a
        conflict/risk is significant) to a magnitude label — never a number, and
        never the finding TYPE used as a coefficient.
        """
        if finding.finding_type == "conflict":
            return "significant"
        if finding.finding_type == "risk":
            return "significant"
        # gap
        if finding.gap_kind == "alignment":
            return "significant"
        if finding.gap_kind in ("coverage", "smart", "quality"):
            return "moderate"
        return DEFAULT_MAGNITUDE

    def _severity_for(self, finding_type: str, magnitude: str) -> Severity:
        return _SEVERITY_BY_MAGNITUDE.get(magnitude, "moderate")

    def _dimension_for(self, finding: Finding) -> str:
        """Which CAF dimension a Finding reduces (by structure, not coefficient)."""
        if finding.finding_type == "risk":
            return "feasibility"
        if finding.finding_type == "conflict":
            return "alignment"
        # gap → clarity unless it is an alignment gap
        return _GAP_KIND_DIMENSION.get(finding.gap_kind or "", "clarity")

    def _impacts_by_dimension(
        self, findings: Sequence[Finding]
    ) -> dict[str, list[float]]:
        """Group each Finding's ``impactᵢ`` under the dimension it reduces."""
        impacts: dict[str, list[float]] = {}
        for finding in findings:
            dim = self._dimension_for(finding)
            impacts.setdefault(dim, []).append(
                impact_for_magnitude(self._magnitude_for(finding))
            )
        return impacts

    def _dim_score(
        self, dimension: str, index: float, reliability: ReliabilityLevel
    ) -> CAFDimensionScore:
        return CAFDimensionScore(
            dimension=dimension,  # type: ignore[arg-type]
            index=index,
            band=band_for(index),  # type: ignore[arg-type]
            reliability=reliability,
        )

    # -- internal: reliability (SEPARATE qualifier; never multiplied in) -----

    def _reliability_level(
        self,
        *,
        findings: Sequence[Finding],
        model: SynthesizedPlanningModel | None,
    ) -> ReliabilityLevel:
        """Judge source-trust from coverage + the model's flagged assumptions.

        High coverage-gap share OR many flagged assumptions (uncertainty) ⇒ Low;
        a moderate amount ⇒ Moderate; otherwise High. This is a LABEL — it is
        NEVER multiplied into the CAF/Confidence arithmetic (Reliability v2).
        """
        coverage_gaps = sum(
            1 for f in findings if f.finding_type == "gap" and f.gap_kind == "coverage"
        )
        assumptions = len(model.flagged_assumptions) if model is not None else 0
        weakness = coverage_gaps + assumptions
        if weakness >= 3:
            return "low"
        if weakness >= 1:
            return "moderate"
        return "high"

    def _reliability_basis(
        self,
        *,
        findings: Sequence[Finding],
        model: SynthesizedPlanningModel | None,
    ) -> str:
        coverage_gaps = sum(
            1 for f in findings if f.finding_type == "gap" and f.gap_kind == "coverage"
        )
        assumptions = len(model.flagged_assumptions) if model is not None else 0
        return (
            f"coverage_gaps={coverage_gaps}; flagged_assumptions={assumptions} "
            "(source-trust qualifier — not multiplied into the score)"
        )

    # -- internal: false confidence (CONF-06) + Non-Collapse -----------------

    def _is_false_confidence(
        self, band: str, reliability: ReliabilityLevel
    ) -> bool:
        """CONF-06 — a HIGH band built on LOW reliability is the dangerous 4th state."""
        return band == "high" and reliability == "low"

    # -- internal: understanding state (AE-04) -------------------------------

    def _classify_understanding(
        self,
        *,
        findings: Sequence[Finding],
        model: SynthesizedPlanningModel | None,
    ) -> UnderstandingState:
        """Classify Initial → Partial → Refined → Validated → Mature (AE-04).

        Never Unknown → Final-Truth (the jump is impossible by construction): the
        state advances by stage maturity, capped by the evidence available. With
        NO synthesized model we cannot be past Initial. The state changes ONLY
        via recompute (the stage carries it; a re-run with a matured stage
        advances it). This is an ATTRIBUTE, not a new object.
        """
        if model is None:
            return "initial"
        stage = self.confidence_stage
        if stage == "validated":
            # Validated stage with low residual weakness → Mature; else Validated.
            unresolved = sum(1 for f in findings if f.finding_type == "conflict")
            return "mature" if unresolved == 0 else "validated"
        if stage == "expanded":
            return "refined"
        # orientation
        return "partial" if findings else "initial"

    # -- internal: basis (the thing a Confidence reduces to) -----------------

    def _basis(
        self,
        *,
        findings: Sequence[Finding],
        model: SynthesizedPlanningModel | None,
        reliability: ReliabilityLevel,
    ) -> tuple[str, ...]:
        """The explainable basis (never a bare number) a Confidence reduces to."""
        return (
            f"finding_count={len(findings)}",
            f"finding_types={sorted({f.finding_type for f in findings})}",
            f"reliability={reliability}",
            f"rule_version={CAF_RULE_VERSION}",
            *( (f"seeded_from_model={model.model_version}",) if model else () ),
        )

    # -- internal: stable Issue identity (recompute supersedes the SAME id) --

    def _issue_id(self, finding: Finding) -> str:
        """A stable identity for the Issue formed from a Finding (supersession key)."""
        basis = json.dumps(
            [finding.project_id, "issue", finding.finding_id], sort_keys=True
        )
        return "issue-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]

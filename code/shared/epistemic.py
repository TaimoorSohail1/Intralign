"""Epistemic types shared across the cognition core (root-level per ratified tree).

Hard rule #6: every cognition entity carries an explicit `epistemic_state`.
There is NO bare "knowledge" type that hides it.

Hard rule #2: the canonical (Attested) layer and the derived projection are
separate. Nothing derived is ever written to the canonical store as Attested.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EpistemicState(str, Enum):
    """Whether an entity is an attested receipt or a recomputable derivation."""

    # LDM §1 universal-field vocabulary (the DB CHECK constraints use these three).
    ATTESTED_EVIDENCE = "attested-evidence"      # evidence-attested (from an artifact)
    ATTESTED_OSLO = "attested-oslo"              # OSLO-self-attested (CognitionHistoryRecord)
    ATTESTED_USER = "attested-user"              # user-attested (UserAcceptanceRecord / Plan Fact)
    DERIVED = "derived"                          # recomputable cognition (Finding/Issue/Recommendation)


class CognitionEntity(BaseModel):
    """Base for every governed cognition entity. Carries explicit epistemic state."""

    epistemic_state: EpistemicState = Field(
        ..., description="attested-* (canonical receipt) | derived (recomputable projection)"
    )

    @property
    def is_canonical(self) -> bool:
        return self.epistemic_state != EpistemicState.DERIVED


# Canonical vocabulary. Forbidden in new code: GovernanceDecision, Authority*,
# "Grounded/Candidate", and plane/layer names as primary identifiers.
CANONICAL_OUTPUTS = (
    "AttestedAssertion",
    "CognitionHistoryRecord",
    "UserAcceptanceRecord",
    "PlanFact",
    "Finding",
    "Issue",
    "Recommendation",
    "ClarificationRequest",
    "Confidence",
    "CAFAssessment",
    "OutcomeConfidence",
    "AcceptanceImpactAssessment",
    # DL-047 additions
    "SynthesizedPlanningModel",
    "PlanningArtifact",
    "ChatSession",
    "ChatExchange",
    "ReviewRequest",
    "StakeholderResponse",
    "SuggestedFix",
)


# =============================================================================
# Wave S (DL-047) — synthesis cognition types: SynthesizedPlanningModel and the
# seven PlanningArtifact types. Both are DERIVED Cognition (Infer-produced;
# recomputable; never written to the canonical store as Attested-truth, hard
# rule #2). The ONLY Attested write Wave S causes is the user's EDIT of a
# generated artifact, admitted through the existing Retain admission path
# (DTM-0008) as a new Attested input — not these objects.
#
# mode / confidence_stage / understanding_state are ATTRIBUTES, not objects
# (DL-046; DL-047 AE-04): carried on each emission and (downstream) its CHR.
# =============================================================================

# DL-046 — the two analysis modes (attribute on every emission).
Mode = Literal["fast", "deep"]

# DL-046 — confidence stage progression (attribute, not a new entity).
ConfidenceStage = Literal["orientation", "expanded", "validated"]

# DL-047 AE-04 — understanding-state progression (attribute, not a new entity).
UnderstandingState = Literal["initial", "partial", "refined", "validated", "mature"]

# DL-047 — the seven generated planning-artifact types.
PlanningArtifactType = Literal[
    "intent",
    "context",
    "scope",
    "requirements",
    "wbs",
    "resources",
    "schedule",
]

PLANNING_ARTIFACT_TYPES: tuple[PlanningArtifactType, ...] = (
    "intent",
    "context",
    "scope",
    "requirements",
    "wbs",
    "resources",
    "schedule",
)


class FlaggedAssumption(BaseModel):
    """An inferred assumption/constraint/dependency the model filled a gap with.

    Wave S A4 forbids SILENT gap-filling: every gap OSLO fills is surfaced HERE
    as an explicit, Derived assumption — never presented as an evidence-attested
    fact. The shape carries no severity/score (``extra='forbid'``); it records
    WHAT was assumed and WHY (the gap it covers), so the audit answers
    "why this Scope says X".
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    statement: str = Field(..., description="The inferred assumption, stated plainly.")
    covers_gap: str = Field(
        ..., description="The evidence gap this assumption fills (audit lineage)."
    )
    # Pinned: an assumption is Derived — NEVER an evidence-attested fact (A4.4).
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a flagged assumption is never Attested.",
    )


class SynthesizedPlanningModel(CognitionEntity):
    """OSLO's recomputable, Derived interpretation of the project (DL-047, Wave S A3.3).

    Built by Infer from Attested assertions (Evidence Extraction -> Context
    Expansion -> Planning Construction). Derived, recomputable, history-tracked;
    it backs the seven generated ``PlanningArtifact``s. Never Attested-as-truth
    (hard rule #2 / A4.2); a user edit is a new Attested input to Retain that
    triggers recompute (it does not mutate this record in place).
    """

    model_config = ConfigDict(frozen=True)

    project_id: str
    model_version: str = Field(
        ..., description="model/prompt/rule version stamp (audit + determinism)."
    )
    # Synthesis content (semantic-equivalence determinism tier; QA §2).
    intent_summary: str = Field(..., description="The synthesized project intent.")
    scope_summary: str = Field(..., description="The synthesized project scope.")
    derived_from_assertions: tuple[str, ...] = Field(
        ..., description="Lineage: the AttestedAssertion ids this model derived from."
    )
    flagged_assumptions: tuple[FlaggedAssumption, ...] = Field(
        default=(), description="Every gap-filling assumption, explicitly surfaced."
    )
    # DL-046 / DL-047 attributes (not objects).
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    # Pinned: a synthesized model is DERIVED cognition (A6 / hard rule #2).
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a synthesized model is never Attested-as-truth.",
    )


class PlanningArtifact(CognitionEntity):
    """A generated planning artifact (DL-047, Wave S A3.4) — Derived Cognition.

    One of the seven types (Intent / Context / Scope / Requirements / WBS /
    Resources / Schedule), generated from a ``SynthesizedPlanningModel``.
    Derived, recomputable, a CHR appended per generation, user-editable (an edit
    is a new Attested input -> recompute, NOT an in-place mutation). Carries its
    lineage to the source assertions and the flagged assumptions it relied on
    (audit: "why this Scope says X").
    """

    model_config = ConfigDict(frozen=True)

    project_id: str
    artifact_type: PlanningArtifactType
    title: str
    body: str = Field(..., description="The generated artifact content (semantic tier).")
    model_version: str = Field(..., description="model/prompt/rule version stamp.")
    derived_from_assertions: tuple[str, ...] = Field(
        ..., description="Lineage: the AttestedAssertion ids backing this artifact."
    )
    flagged_assumptions: tuple[FlaggedAssumption, ...] = Field(
        default=(), description="The gap-filling assumptions this artifact relied on."
    )
    synthesized_model_version: str = Field(
        ..., description="The SynthesizedPlanningModel version this was generated from."
    )
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    # Pinned: a generated artifact is DERIVED (A4.2 — never Attested-as-truth).
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a generated artifact is never Attested-as-truth.",
    )


# =============================================================================
# Wave B (DTM-0010, IC-WB-INFER) — the Finding cognition type. Infer is the
# SINGLE producer of Findings (one-producer rule #1). A Finding is DERIVED
# Cognition (recomputable; never written to the canonical store as Attested,
# hard rule #2) of one of three types — Gap, Conflict, Risk Signal — and is
# ANCHORED to the AttestedAssertion(s) it derives from (evidence_anchors;
# missing anchor = Major contract failure, IC-WB-INFER 1.1). Infer does NOT
# compute severity/confidence (Evaluate's, DTM-0011), generate recommendations/
# clarifications (Advise's), or resolve a conflict into canonical truth — a
# conflict is SURFACED as a Finding, never collapsed.
#
# mode / confidence_stage are ATTRIBUTES, not objects (DL-046): carried on each
# emission and (downstream) its CHR. confidence_stage matures ONLY via recompute.
# =============================================================================

# IC-WB-INFER — the three Finding types (Object Model §8: Gap/Conflict/Risk are
# Finding TYPES, not standalone objects).
FindingType = Literal["gap", "conflict", "risk"]

# The structural sub-kinds a Gap can take (IC-WB-INFER 1.1 required-behavior #1:
# gaps of alignment/coverage/quality/SMART). Recorded for audit only — it is a
# descriptive attribute of a gap Finding, NOT a severity/score (which is
# Evaluate's). ``None`` for conflict/risk Findings.
GapKind = Literal["alignment", "coverage", "quality", "smart"]


class Finding(CognitionEntity):
    """A Derived structural implication of the Attested knowledge (IC-WB-INFER).

    One of three types — Gap (alignment/coverage/quality/SMART), Conflict
    (contradiction among Attested assertions), or Risk Signal (feasibility) —
    derived by Infer from Attested knowledge + the synthesized model + the
    declared-outcome reference. ALWAYS anchored to the AttestedAssertion id(s)
    it derives from (``evidence_anchors`` — non-empty; a missing anchor is a
    Major failure, IC-WB-INFER). Derived/recomputable; never Attested-as-truth
    (hard rule #2). A conflict Finding SURFACES the contradiction; it never
    resolves it into canonical truth.

    Forbidden surface (``extra='forbid'``): a Finding carries NO severity /
    confidence / score / recommendation field — those belong to Evaluate
    (DTM-0011) and Advise. Infer owns ONLY the typed, anchored Finding.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    finding_type: FindingType
    finding_id: str = Field(
        ..., description="Stable identity (recompute supersedes the SAME id)."
    )
    summary: str = Field(..., description="The structural implication, stated plainly.")
    # MANDATORY lineage: the AttestedAssertion ids this Finding derived from.
    # A Finding with no anchor is rejected at construction (Major failure made
    # structurally impossible — IC-WB-INFER invariant "anchored to Attested").
    evidence_anchors: tuple[str, ...] = Field(
        ..., min_length=1,
        description="Lineage: the AttestedAssertion id(s) this Finding derives from.",
    )
    # Descriptive sub-kind for gap Findings (audit only; never a score). None
    # for conflict/risk.
    gap_kind: GapKind | None = Field(
        default=None, description="For gap Findings: the structural sub-kind (audit only)."
    )
    model_or_rule_version: str = Field(
        ..., description="model/prompt/rule version stamp (audit + determinism)."
    )
    # DL-046 attributes (not objects). confidence_stage matures ONLY via recompute.
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    # Pinned: a Finding is DERIVED cognition — never Attested-as-truth (rule #2).
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a Finding is never Attested-as-truth.",
    )


# =============================================================================
# Wave B (DTM-0011, IC-WB-EVAL) — the Evaluate cognition types. Evaluate is the
# SINGLE producer (one-producer rule #1) of: Issue (Core), the Severity/
# Confidence/Reliability attributes, the CAFAssessment (Core, derived), and the
# OutcomeConfidence (Core, derived aggregate). ALL are DERIVED Cognition
# (recomputable; never written to the canonical store as Attested — hard rule
# #2). Evaluate reads Findings (Infer) + Attested knowledge; it does NOT
# generate Findings (Infer's), recommendations/clarifications (Advise's),
# resolve a conflict, accept an interpretation, govern exposure, or change any
# value outside recompute.
#
# Scoring is the v0 CAF/Confidence formula (ADR-0006; CAF_CONFIDENCE_V0):
# per-dimension index = 100·Π(1−impactᵢ); the three co-equal dims consolidate
# via a power-mean (p≤1) with a floor ε; bands 0–49 / 50–74 / 75–100 with a ±3
# edge guard. RELIABILITY is a SEPARATE qualifier label, NEVER multiplied into
# the number (Reliability Model v2). Confidence = trust in UNDERSTANDING, NEVER
# project health / readiness / probability / a bare score — it reduces to its
# basis (band + reliability qualifier + the basis it was computed over).
#
# mode / confidence_stage / understanding_state are ATTRIBUTES, not objects
# (DL-046 / DL-047 AE-04); carried on each emission and (downstream) its CHR.
# They change ONLY via recompute.
# =============================================================================

# IC-WB-EVAL — Severity is an ATTRIBUTE of an Issue (Object Model §8), not a
# standalone object. The label set is the analysis-state severity, NOT a numeric
# score (no number leaks out as "the score" — that would be project health).
Severity = Literal["info", "low", "moderate", "high", "critical"]

# Reliability is a SEPARATE qualifier label (Reliability Model v2) — a source-
# trust attribute, NEVER arithmetically combined into Confidence. Three levels.
ReliabilityLevel = Literal["low", "moderate", "high"]

# Confidence band (Calibration §2): 0–49 Low / 50–74 Medium / 75–100 High, with
# the ±3 edge guard applied at computation (a value within 3 pts of a boundary
# is the LOWER band — never overstate). A BAND, never a bare number to the user.
ConfidenceBand = Literal["low", "medium", "high"]

# The CAF dimensions (Calibration Decision 001 D5 — co-equal, no hierarchy).
CAFDimension = Literal["clarity", "alignment", "feasibility"]


class Reliability(CognitionEntity):
    """A source-trust qualifier (Reliability Model v2) — a label, never a number.

    Reliability QUALIFIES Confidence; it is NEVER multiplied into the confidence
    arithmetic (Doctrine; v0 §3). It carries the basis it was judged on (e.g.
    coverage / evidence support) for explainability, but exposes no score.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    level: ReliabilityLevel = Field(..., description="low | moderate | high (a label).")
    basis: str = Field(
        ..., description="Why this reliability level (coverage / evidence support)."
    )
    model_or_rule_version: str = Field(..., description="rule/model version stamp.")
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — Reliability is never Attested-as-truth.",
    )


class Confidence(CognitionEntity):
    """Trust in OSLO's UNDERSTANDING — banded, reliability-qualified (IC-WB-EVAL).

    Confidence is NEVER project health / readiness / probability / a score
    (negative tests enforce). It reduces to its BASIS: a band, the reliability
    qualifier, and the inputs it was computed over. The raw 0–100 ``index`` is
    retained for explainability + determinism (exact rule replay) but the
    USER-FACING value is the ``band`` (a value within ±3 of a boundary is the
    lower band — never overstate). The shape carries NO ``score`` / ``health`` /
    ``probability`` field (``extra='forbid'`` makes that structurally impossible).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    # The computed 0–100 understanding-maturity index (explainability + exact
    # replay). NOT rendered to the user as a probability/health number.
    index: float = Field(..., ge=0.0, le=100.0, description="0–100 maturity index.")
    band: ConfidenceBand = Field(..., description="low | medium | high (±3 edge guard).")
    reliability_qualifier: ReliabilityLevel = Field(
        ..., description="The separate reliability label (never multiplied in)."
    )
    basis: tuple[str, ...] = Field(
        ..., min_length=1,
        description="The basis this confidence reduces to (never a bare number).",
    )
    model_or_rule_version: str = Field(..., description="rule/model version stamp.")
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — Confidence is never Attested-as-truth.",
    )


class CAFDimensionScore(BaseModel):
    """One CAF dimension: integrity index · band · per-dimension reliability.

    Each dimension is co-equal (no static weight, no hierarchy). The ``index``
    is the v0 per-dimension score (100·Π(1−impactᵢ), clamped [0,100]); the
    ``band`` applies the same ±3 edge guard; ``reliability`` is the per-dimension
    qualifier label (separate, never multiplied in).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    dimension: CAFDimension
    index: float = Field(..., ge=0.0, le=100.0)
    band: ConfidenceBand
    reliability: ReliabilityLevel


class CAFAssessment(CognitionEntity):
    """Clarity / Alignment / Feasibility — three co-equal dimensions (IC-WB-EVAL).

    A Derived aggregate: each dimension a (index · band · per-dimension
    reliability) triple. No dimension dominates by default; weakness is felt
    (power-mean aggregation lives in the OutcomeConfidence, not here). Carries no
    standalone severity/score field beyond the per-dimension indices.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    clarity: CAFDimensionScore
    alignment: CAFDimensionScore
    feasibility: CAFDimensionScore
    model_or_rule_version: str = Field(..., description="rule/model version stamp.")
    derived_from_findings: tuple[str, ...] = Field(
        default=(), description="Lineage: the Finding ids this assessment reduced."
    )
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a CAFAssessment is never Attested-as-truth.",
    )

    def dimensions(self) -> tuple[CAFDimensionScore, ...]:
        return (self.clarity, self.alignment, self.feasibility)


class OutcomeConfidence(CognitionEntity):
    """Aggregate alignment between current state and the declared outcome (IC-WB-EVAL).

    The Derived aggregate the MRI shows: the three CAF dimensions consolidated
    through the v0 power-mean (between an average and a minimum), banded and
    reliability-qualified. Like ``Confidence`` it is trust in UNDERSTANDING, NEVER
    project health / probability. ``false_confidence_flagged`` is the CONF-06
    trust signal (high band on low reliability). Reduces to its basis (never a
    bare number; the ``index`` is for explainability + exact replay only).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    index: float = Field(..., ge=0.0, le=100.0, description="0–100 aggregate index.")
    band: ConfidenceBand
    reliability_qualifier: ReliabilityLevel = Field(
        ..., description="The separate reliability label (never multiplied in)."
    )
    # CONF-06: high band built on low reliability/coverage — the dangerous 4th
    # state. A trust signal surfaced HERE (and evented), never silently dropped.
    false_confidence_flagged: bool = Field(
        default=False,
        description="CONF-06 — high confidence on low-reliability understanding.",
    )
    basis: tuple[str, ...] = Field(
        ..., min_length=1, description="The basis it reduces to (never a bare number)."
    )
    model_or_rule_version: str = Field(..., description="rule/model version stamp.")
    derived_from_findings: tuple[str, ...] = Field(
        default=(), description="Lineage: the Finding ids this aggregate reduced."
    )
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — OutcomeConfidence is never Attested-as-truth.",
    )


class Issue(CognitionEntity):
    """A prioritized Finding (IC-WB-EVAL) — Severity assigned by Evaluate; Derived.

    Evaluate forms an Issue FROM a Finding by assigning a ``severity`` attribute
    (Object Model §8 — Severity is an attribute, not a standalone object). The
    Issue carries the source Finding lineage (the audit answer to "which Finding
    became this Issue"). Derived/recomputable; never Attested-as-truth (rule #2).

    Forbidden surface (``extra='forbid'``): an Issue carries NO recommendation /
    clarification / resolution / confidence-as-health field — those belong to
    Advise (recommendations) and Evaluate's separate Confidence (trust, not
    health). Severity is a LABEL, never a leaked probability/score.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    issue_id: str = Field(..., description="Stable identity (recompute supersedes same id).")
    finding_id: str = Field(..., description="Lineage: the source Finding this prioritizes.")
    finding_type: FindingType = Field(..., description="The source Finding's type (label).")
    severity: Severity = Field(..., description="The assigned severity attribute (a label).")
    summary: str = Field(..., description="The prioritized issue, stated plainly.")
    evidence_anchors: tuple[str, ...] = Field(
        ..., min_length=1, description="Lineage carried from the source Finding."
    )
    model_or_rule_version: str = Field(..., description="rule/model version stamp.")
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — an Issue is never Attested-as-truth.",
    )


# =============================================================================
# Wave C (DTM-0014, IC-WC-ADVISE) — the Advise cognition types. Advise is the
# SINGLE producer (one-producer rule #1) of Recommendation + ClarificationRequest.
# Both are DERIVED Cognition (recomputable; never written to the canonical store
# as Attested — hard rule #2). Advise READS Findings (Infer) + Issues/assessment
# (Evaluate) + Attested knowledge and PROPOSES candidate responses; it does NOT
# evaluate/score (Evaluate's), generate Findings (Infer's), write canonical /
# promote to Attested, govern/authorize/execute, ACCEPT its own output
# (acceptance is the user's — DL-055; Wave U), or change an assessment outside
# recompute.
#
# Recommendation is ALWAYS anchored to a Finding/Issue (``anchor`` — never
# standalone; a missing anchor is a Major contract failure, IC-WC-ADVISE 1.1,
# made structurally impossible by the non-empty ``anchor`` field). Multiple
# alternatives persist as MULTIPLE Recommendations — there is NO standalone
# Resolution-Path object (Resolution Paths are presentation-only, AMB-1/Wave E;
# emitting one is a rejected negative). Advise emits Recommendations in the
# ``Generated`` state ONLY (DL-055): Accept/Defer/Reject/Apply are user actions
# recorded by Wave U, never produced here.
#
# mode / confidence_stage are ATTRIBUTES, not objects (DL-046); carried on each
# emission and (downstream) its CHR. They change ONLY via recompute.
# =============================================================================

# IC-WC-ADVISE — the two Recommendation types (C1: Suggested Action, Candidate
# Improvement). A LABEL describing the KIND of candidate response — never a
# severity/score (that is Evaluate's) and never an executed action (Advise
# proposes, never disposes).
RecommendationType = Literal["suggested_action", "candidate_improvement"]

# DL-055 — the Recommendation lifecycle state. Advise produces the ``generated``
# state ONLY; {accepted, rejected, deferred, implemented, superseded} are
# user-owned transitions recorded by Wave U (NOT produced here). Pinned on the
# Recommendation so a non-``generated`` state out of Advise is structurally
# impossible (self-accept made impossible — IC-WC-ADVISE forbidden, Critical).
RecommendationState = Literal["generated"]


class Recommendation(CognitionEntity):
    """A Derived, governable candidate response (IC-WC-ADVISE) — anchored, advisory.

    Produced by Advise from the Findings/Issues that motivate it; ALWAYS anchored
    to a Finding/Issue (``anchor`` — non-empty; a standalone/unanchored
    Recommendation is a Major failure made structurally impossible). One of two
    types — Suggested Action or Candidate Improvement. Derived/recomputable;
    never Attested-as-truth (hard rule #2). Advise PROPOSES; it never evaluates,
    scores, governs, accepts, authorizes, or executes — the ``state`` is pinned to
    ``generated`` (DL-055: acceptance is the user's, recorded by Wave U).

    Multiple alternatives are MULTIPLE Recommendations (no Resolution-Path
    object). Forbidden surface (``extra='forbid'``): a Recommendation carries NO
    severity / confidence / score field (Evaluate's), NO accept/approve/execute
    field, and NO resolution-path-object field — those are not Advise's to hold.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    recommendation_id: str = Field(
        ..., description="Stable identity (recompute supersedes the SAME id)."
    )
    recommendation_type: RecommendationType = Field(
        ..., description="suggested_action | candidate_improvement (a kind label)."
    )
    # MANDATORY anchor: the Finding/Issue id this Recommendation responds to. A
    # Recommendation with no anchor is rejected at construction (the
    # "Recommendation-only-in-Finding-context" invariant made structurally
    # impossible — IC-WC-ADVISE 1.1; standalone = Major failure).
    anchor: str = Field(
        ..., min_length=1,
        description="Lineage: the Finding/Issue id this Recommendation is anchored to.",
    )
    summary: str = Field(
        ..., description="The candidate response, stated plainly (AI-text; semantic tier)."
    )
    model_or_rule_version: str = Field(..., description="model/rule version stamp.")
    # DL-055: Advise emits the Generated state ONLY (never accepts its own output).
    state: RecommendationState = Field(
        default="generated",
        description="Pinned generated — acceptance is the user's (DL-055; Wave U).",
    )
    # DL-046 attributes (not objects). confidence_stage matures ONLY via recompute.
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    # Pinned: a Recommendation is DERIVED cognition — never Attested-as-truth.
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a Recommendation is never Attested-as-truth.",
    )


class ClarificationRequest(CognitionEntity):
    """A Derived request for user input on blocking ambiguity (IC-WC-ADVISE).

    Produced by Advise when ambiguity blocks understanding — an INFORMATION
    request (a question), NOT an action and NOT a Recommendation. Anchored to the
    Finding/Issue whose ambiguity it surfaces (``anchor`` — non-empty).
    Derived/recomputable; never Attested-as-truth. Advise never resolves the
    ambiguity itself or accepts an answer — it asks; the user answers (the answer
    re-enters through Retain admission and triggers recompute, never an in-place
    mutation here).

    Forbidden surface (``extra='forbid'``): a Clarification carries NO severity /
    score / answer / acceptance field — it is purely the question + its anchor.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    clarification_id: str = Field(
        ..., description="Stable identity (recompute supersedes the SAME id)."
    )
    anchor: str = Field(
        ..., min_length=1,
        description="Lineage: the Finding/Issue id whose ambiguity this surfaces.",
    )
    question: str = Field(
        ..., description="The information request (AI-text; semantic tier)."
    )
    model_or_rule_version: str = Field(..., description="model/rule version stamp.")
    mode: Mode
    confidence_stage: ConfidenceStage = "orientation"
    understanding_state: UnderstandingState = "initial"
    epistemic_state: Literal[EpistemicState.DERIVED] = Field(
        default=EpistemicState.DERIVED,
        description="Pinned derived — a ClarificationRequest is never Attested-as-truth.",
    )

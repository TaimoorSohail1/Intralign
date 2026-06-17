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

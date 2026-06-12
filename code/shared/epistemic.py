"""Epistemic types shared across the cognition core (root-level per ratified tree).

Hard rule #6: every cognition entity carries an explicit `epistemic_state`.
There is NO bare "knowledge" type that hides it.

Hard rule #2: the canonical (Attested) layer and the derived projection are
separate. Nothing derived is ever written to the canonical store as Attested.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


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

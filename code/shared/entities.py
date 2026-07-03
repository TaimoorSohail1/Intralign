"""Data Model v1.2 entity schemas — the canonical API resources (DTOs).

These are the request/response shapes the API exposes verbatim (API Contract
Spec §1: "request/response schemas use Data Model fields and enums verbatim").
They live in shared/ so both services.render (which produces them from internal
cognition) and the api/ transport (which exposes them as response_model) import
from one place — without the transport layer being imported by a service.

DISTINCT from shared.epistemic: those are the INTERNAL cognition types
(attested receipts / derived projections + CognitionHistoryRecord). The entities
here are the EXTERNAL Data Model resources. services.render maps internal
cognition → these entities.

Enums below are transcribed from the Endpoint Catalog + DL-055. EXACT entity
FIELD sets must be bound to RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2 under the
relevant Wave contract — do not invent fields (ANTI_ASSUMPTION protocol).
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ProjectLifecycle(str, Enum):
    CREATED = "created"
    ARCHIVED = "archived"   # terminal


class AnalysisRunStatus(str, Enum):
    QUEUED = "queued"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    # + intermediate states per the State Model — bind exactly under contract.


class FindingStatus(str, Enum):
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    ADDRESSED = "addressed"
    CLOSED = "closed"
    REOPENED = "reopened"


class RecommendationStatus(str, Enum):
    # State Model §11 (canonical; DL-055). "Modify" is NOT a state — an edit supersedes.
    GENERATED = "generated"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"   # the "Apply" action
    SUPERSEDED = "superseded"


# --- Entity skeletons (fields bound to Data Model v1.2 under contract) ---

class Project(BaseModel):
    id: str
    workspace_id: str
    lifecycle_state: ProjectLifecycle
    # title, description, timestamps, ... -> bind from Data Model v1.2.


class AnalysisRun(BaseModel):
    id: str
    project_id: str
    status: AnalysisRunStatus
    # mode (fast|deep), timestamps, ... -> bind from Data Model v1.2.


# --- DL-047 Wave S entities (Derived; exposed read-only over REST) ---
# The EXTERNAL Data Model resources for the synthesized planning model and the
# seven generated planning artifacts. The INTERNAL cognition that backs them
# lives in shared.epistemic (SynthesizedPlanningModel / PlanningArtifact
# CognitionEntity); services.render maps cognition -> these entities. Field
# sets are bound to Data Model v1.2 under IC-WS-SYNTH — skeletons here, not
# invented (ANTI_ASSUMPTION protocol).

class PlanningArtifactType(str, Enum):
    """The seven generated planning-artifact types (DL-047)."""

    INTENT = "intent"
    CONTEXT = "context"
    SCOPE = "scope"
    REQUIREMENTS = "requirements"
    WBS = "wbs"
    RESOURCES = "resources"
    SCHEDULE = "schedule"


class SynthesizedPlanningModel(BaseModel):
    """External DTO for OSLO's Derived planning model (DL-047)."""

    id: str
    project_id: str
    epistemic_label: str = "derived"  # always Derived (never Attested-as-truth).
    # intent/scope summaries, lineage, assumptions, version -> bind v1.2.


class PlanningArtifact(BaseModel):
    """External DTO for a generated planning artifact (DL-047; user-editable)."""

    id: str
    project_id: str
    artifact_type: PlanningArtifactType
    epistemic_label: str = "derived"  # generated artifacts are Derived.
    # title/body, lineage, assumptions, model version -> bind v1.2.

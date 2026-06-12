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

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

from pydantic import BaseModel, Field


class ProjectLifecycle(str, Enum):
    # Data Model v1.2 §7 (inherited v1.1) — the Project lifecycle_state enum, verbatim.
    CREATED = "created"
    ORIENTING = "orienting"
    ORIENTED = "oriented"
    DEEP_ANALYZING = "deep_analyzing"
    ANALYZED = "analyzed"
    ARCHIVED = "archived"   # terminal


class AnalysisRunType(str, Enum):
    # Data Model v1.2 §10 (inherited v1.1) — AnalysisRun.run_type, verbatim.
    FAST_ANALYSIS_PASS = "fast_analysis_pass"
    DEEP_ANALYSIS_PASS = "deep_analysis_pass"


class AnalysisRunStatus(str, Enum):
    # Data Model v1.2 §10 (inherited v1.1, Patch-001) — AnalysisRun.run_status, verbatim.
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SUPERSEDED = "superseded"


class FindingStatus(str, Enum):
    # Data Model v1.2 §11 (Finding unchanged) — Finding.status, verbatim.
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    ADDRESSED = "addressed"
    CLOSED = "closed"
    REOPENED = "reopened"
    SUPERSEDED = "superseded"


class FindingType(str, Enum):
    # Data Model v1.2 §11 (inherited v1.1) — Finding.finding_type flat taxonomy, verbatim.
    MISSING_INFORMATION = "missing_information"
    AMBIGUITY = "ambiguity"
    ASSUMPTION = "assumption"
    INFERENCE = "inference"
    CONFLICT = "conflict"
    CONSTRAINT = "constraint"
    COVERAGE_GAP = "coverage_gap"


class Dimension(str, Enum):
    # Data Model v1.2 — CAF dimension enum (clarity/alignment/feasibility), verbatim.
    CLARITY = "clarity"
    ALIGNMENT = "alignment"
    FEASIBILITY = "feasibility"


class Severity(str, Enum):
    # Data Model v1.2 §11 (inherited v1.1) — Finding.severity enum, verbatim.
    CRITICAL = "critical"
    MODERATE = "moderate"
    WARNING = "warning"


class RecommendationStatus(str, Enum):
    # Data Model v1.2 §12 (RS-R3) — Recommendation.status, verbatim.
    GENERATED = "generated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    IMPLEMENTED = "implemented"
    SUPERSEDED = "superseded"


class RecommendationType(str, Enum):
    # Data Model v1.2 §12 (RS-R1; 3 values) — Recommendation.recommendation_type, verbatim.
    IMPROVEMENT = "improvement"
    VALIDATION = "validation"
    SUGGESTED_FIX = "suggested_fix"


class EffortLevel(str, Enum):
    # Data Model v1.2 §12 (RS-R7) — Recommendation.effort, verbatim.
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConfidenceBand(str, Enum):
    # LDM §3.1 / Calibration Defaults §2 — the user-facing band on a Derived projection.
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ConflictState(str, Enum):
    # LDM §3.1 — the Live Cognition Projection conflict marker (travels with the object).
    NONE = "none"
    CONTESTED = "contested"


class NotificationState(str, Enum):
    # Data Model v1.2 §13 (R-4) — Notification.state, verbatim.
    CREATED = "created"
    VIEWED = "viewed"
    DISMISSED = "dismissed"
    EXPIRED = "expired"


class NotificationSourceType(str, Enum):
    # Data Model v1.2 §13 — Notification.source_object_type, verbatim.
    FINDING = "finding"
    RECOMMENDATION = "recommendation"
    ANALYSIS_RUN = "analysis_run"
    COMMENT = "comment"
    SHARED_ARTIFACT = "shared_artifact"


# =============================================================================
# Epistemic-safety envelope (IC-WE-DISCLOSE E0/E1; ADR-0003).
#
# Every Derived object the Disclose surface presents carries its epistemic label
# so the UI renders WITHOUT re-deriving (decision #5): Attested/Derived +
# confidence band + conflict. These are the LDM §3.1 Live Cognition Projection
# universal fields (``epistemic_label`` / ``confidence_value`` / ``confidence_band``
# / ``conflict_state`` / ``current_chr_ref``), surfaced verbatim on every Derived
# DTO. The internal ``shared.epistemic`` cognition types are NEVER serialized
# verbatim — ``services.render`` maps them into these DTOs (negative-proven).
# =============================================================================


class DerivedEnvelope(BaseModel):
    """The epistemic label that travels with every Derived object (LDM §3.1).

    A Derived DTO is presentation-ready: it already carries its epistemic label
    (always ``derived``), the confidence band (low/medium/high — never a bare
    number to the user), the optional 0–100 value for explainability, the
    conflict marker, and the ``current_chr_ref`` lineage to the Cognition History
    version presented (so what-was-shown is reconstructable, OBS-WE-DISCLOSE).
    """

    epistemic_label: str = Field(
        default="derived",
        description="Always 'derived' for a recomputable projection (LDM §5.6).",
    )
    confidence_value: float | None = Field(
        default=None, ge=0.0, le=100.0,
        description="0–100 explainability value (NOT a user-facing health number).",
    )
    confidence_band: ConfidenceBand | None = Field(
        default=None, description="low | medium | high (the user-facing band)."
    )
    conflict_state: ConflictState = Field(
        default=ConflictState.NONE,
        description="'contested' when the object surfaces an unresolved conflict.",
    )
    current_chr_ref: str | None = Field(
        default=None,
        description="Lineage: the Cognition History Record id this view reflects.",
    )


# --- Project / AnalysisRun (Data Model v1.2 §7 / §10 — verbatim field sets) ---

class Project(BaseModel):
    """Project DTO — Data Model v1.2 §7 (inherited v1.1), fields verbatim."""

    project_id: str
    workspace_id: str
    created_by_user_id: str | None = None
    title: str | None = None
    description: str | None = None
    lifecycle_state: ProjectLifecycle
    current_confidence_state_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AnalysisRun(BaseModel):
    """AnalysisRun DTO — Data Model v1.2 §10 (inherited v1.1), fields verbatim."""

    analysis_run_id: str
    project_id: str
    run_type: AnalysisRunType
    run_status: AnalysisRunStatus
    previous_run_id: str | None = None
    started_at: str | None = None
    completed_at: str | None = None


# --- Finding / Issue / Recommendation / Confidence DTOs (Derived projections) ---
# Each is a LDM §3.1 Live Cognition Projection: the Data-Model field set + the
# DerivedEnvelope label. ``render`` builds these from the derived.*_current rows
# (or the CHR payload) — never from the internal cognition type verbatim.

class Finding(BaseModel):
    """Finding DTO — Data Model v1.2 §11 (unchanged), verbatim + epistemic label."""

    finding_id: str
    project_id: str
    first_seen_run_id: str | None = None
    last_updated_run_id: str | None = None
    finding_type: FindingType
    affected_dimensions: list[Dimension] = Field(default_factory=list)
    severity: Severity | None = None
    status: FindingStatus = FindingStatus.DETECTED
    summary: str | None = None
    evidence_links: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
    closed_at: str | None = None
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


class Issue(BaseModel):
    """Issue DTO — the Derived, first-class prioritized Finding (LDM §2.2/§3.1).

    Object Model §8: an Issue is a Core Derived Runtime Object formed *from* a
    Finding (``Issue ──from──> Finding``) with ``severity`` as an attribute — it
    is NOT a separate canonical row. The persistence representation is the
    ``derived.issue_current`` live projection (the DTM-0030 materializer populates
    it from the ``issue`` CHRs). It carries the Finding's Data-Model field set
    (``finding_type`` / ``severity`` / ``summary`` / ``evidence_links``) PLUS its
    own first-class identity (``issue_id``) and the source-Finding lineage
    (``finding_id``). The epistemic ``label`` travels (always Derived + band +
    conflict, decision #5). No field is invented beyond the Finding field set +
    the Issue's identity/lineage (Data Model v1.2 introduces no new entity; Issue
    is the Object-Model Derived projection of a prioritized Finding).
    """

    issue_id: str
    project_id: str
    finding_id: str
    first_seen_run_id: str | None = None
    last_updated_run_id: str | None = None
    finding_type: FindingType
    affected_dimensions: list[Dimension] = Field(default_factory=list)
    severity: Severity | None = None
    status: FindingStatus = FindingStatus.DETECTED
    summary: str | None = None
    evidence_links: list[str] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None
    closed_at: str | None = None
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


class CAFDimensionView(BaseModel):
    """One CAF dimension snapshot — Data Model v1.2 §10 CAFState per-dimension fields."""

    dimension: Dimension
    index: float = Field(..., ge=0.0, le=100.0)
    band: ConfidenceBand
    reliability: str


class CAFState(BaseModel):
    """CAFState DTO — Data Model v1.2 §10 (inherited v1.1), three co-equal dimensions."""

    project_id: str
    clarity: CAFDimensionView
    alignment: CAFDimensionView
    feasibility: CAFDimensionView
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


class ConfidenceState(BaseModel):
    """ConfidenceState DTO — Data Model v1.2 §10 (inherited v1.1) + epistemic label.

    The aggregate alignment the MRI shows (OutcomeConfidence). ``confidence_band``
    is the user-facing value; ``outcome_confidence_value`` is the 0–100 index kept
    for explainability only (never rendered as project health / probability).
    """

    project_id: str
    confidence_state_id: str | None = None
    analysis_run_id: str | None = None
    outcome_confidence_value: float | None = Field(default=None, ge=0.0, le=100.0)
    confidence_band: ConfidenceBand | None = None
    reliability_qualifier: str | None = None
    false_confidence_flagged: bool = False
    basis: list[str] = Field(default_factory=list)
    supersedes_confidence_state_id: str | None = None
    created_at: str | None = None
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


class Recommendation(BaseModel):
    """Recommendation DTO — Data Model v1.2 §12 (RS-R3 + RS-R7), fields verbatim.

    Always anchored to ONE Finding (``finding_id``). The ``status`` is read from
    the governed source as-is; Disclose presents the accept/reject/defer/implement
    AFFORDANCE but the read surface itself NEVER mutates it (decision #3/#4 —
    acceptance routes to the existing Wave U capture seam).
    """

    recommendation_id: str
    project_id: str
    finding_id: str
    first_seen_run_id: str | None = None
    recommendation_type: RecommendationType | None = None
    status: RecommendationStatus = RecommendationStatus.GENERATED
    title: str | None = None
    description: str | None = None
    rationale: str | None = None
    expected_dimension: Dimension | None = None
    effort: EffortLevel | None = None
    artifact_reference: str | None = None
    artifact_element_reference: str | None = None
    supersedes_recommendation_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


# --- Overview / counts DTO (DTM-0038 — presentation of governed objects) -------
# CRITICAL (Wave E not-project-health rule): the Overview is a PRESENTATION of the
# governed objects — counts of Findings/Issues/Recommendations + the aggregate
# Outcome-Confidence band + CAF, each EPISTEMICALLY LABELLED. It is NEVER a
# health/readiness/probability score and computes nothing new: every number is a
# count of, or a pass-through band from, an already-governed object. There is no
# ``health`` / ``readiness`` / ``score`` / ``probability`` field on this DTO by
# construction (negative-proven).


class GovernedCount(BaseModel):
    """A labelled count of one governed-object kind (presentation, not a metric).

    ``label`` is the human-facing kind name (e.g. ``"findings"``); ``count`` is the
    number of governed objects of that kind currently presented. It is a COUNT of
    governed objects — never a health figure, never a percentage.
    """

    label: str = Field(description="The governed-object kind this counts (e.g. 'findings').")
    kind: str = Field(description="The governed-object kind key (finding|issue|recommendation).")
    count: int = Field(ge=0, description="How many governed objects of this kind are present.")


class Overview(BaseModel):
    """Overview DTO — counts of governed objects + labelled aggregates (DTM-0038).

    Presents, for one project: the counts of the governed lists (Findings,
    Issues, Recommendations) AND the aggregate epistemic signals OSLO already
    governs — the Outcome-Confidence band + the CAF snapshot — each carrying its
    Derived epistemic label so the UI renders without re-deriving (decision #5).

    NOT a health metric (Wave E): the counts are presentation of governed objects
    and the confidence/CAF are pass-throughs of their own governed bands. The DTO
    deliberately carries NO ``health`` / ``readiness`` / ``score`` / ``probability``
    field — Overview never reads as a single project-health number.
    """

    project_id: str
    counts: list[GovernedCount] = Field(default_factory=list)
    outcome_confidence: ConfidenceState | None = Field(
        default=None,
        description="The aggregate Outcome Confidence (Derived; band is user-facing).",
    )
    caf: CAFState | None = Field(
        default=None, description="The CAF snapshot (three co-equal Derived dimensions)."
    )


# --- History feed DTO (DTM-0038 — the Cognition-History trail, append-order) ----
# The "what OSLO said when" trail: each entry is read EXACT from a Cognition
# History Record (LDM §2.2; the append-only emission receipt) — Derived-labelled
# (a CHR is OSLO-self-attested, ``attested-oslo``). The feed is CHR-only (the
# existing UAR/plan-fact reads cover user-attested receipts; see the worker
# report). Append-order is preserved by ``emitted_at``. Read-exact: the entry
# surfaces the receipt's identity + lineage, never re-derives.


class HistoryEntry(BaseModel):
    """One Cognition-History trail entry — read exact from a CHR (LDM §2.2).

    Surfaces the emission receipt's identity (``chr_id``), the governed-output
    kind it emitted (``output_kind``), when it was emitted (``emitted_at``), what
    drove the (re)compute (``recompute_trigger``), and the supersession link
    (``supersedes_chr_id``) that makes the trail a drift backbone. ``epistemic_label``
    is ``attested-oslo`` — a CHR is OSLO-self-attested by definition; the entry is
    a Derived-trail receipt, never a canonical fact about the world.
    """

    chr_id: str
    project_id: str
    output_kind: str
    recompute_trigger: str | None = None
    supersedes_chr_id: str | None = None
    emitted_at: str | None = None
    epistemic_label: str = "attested-oslo"


# --- Notification DTO (Data Model v1.2 §13 — awareness only, never canonical) ---

class Notification(BaseModel):
    """Notification DTO — Data Model v1.2 §13 (R-4), fields verbatim.

    Platform awareness state (non-canonical): never drives analysis, carries no
    epistemic cognition label (it is not a Derived projection — it references a
    source object).
    """

    notification_id: str
    workspace_id: str
    project_id: str | None = None
    source_object_type: NotificationSourceType
    source_object_id: str
    event_type: str
    target_user_id: str | None = None
    state: NotificationState = NotificationState.CREATED
    created_at: str | None = None
    viewed_at: str | None = None
    dismissed_at: str | None = None
    expired_at: str | None = None


# --- Acceptance DTOs (Wave U canonical receipts — user-attested, never truth) ---

class UserAcceptanceRecord(BaseModel):
    """UserAcceptanceRecord DTO — the canonical, user-attested confirm receipt.

    "User U, at time T, took action A on item I at version_pin V" (DTM-0008). It
    records a HUMAN DECISION — it marks nothing world-true/approved/canonical. The
    ``epistemic_label`` is ``attested-user`` (the user authored it; OSLO never
    self-accepts, hard rule #5).
    """

    uar_id: str
    project_id: str
    user_id: str | None = None
    action: str
    target_kind: str | None = None
    version_pin: str
    epistemic_label: str = "attested-user"
    confirmed_at: str | None = None
    created_at: str | None = None


class PlanFact(BaseModel):
    """PlanFact DTO — the user-attested confirmed planning item (DTM-0016).

    The confirmed content recorded as "factual in the plan, attributed to the
    user" — NOT world-truth, NOT OSLO-approved. ``epistemic_label`` is
    ``attested-user``.
    """

    plan_fact_id: str
    project_id: str
    proposition: str
    content_type: str = "fact"
    attested_by_user: str | None = None
    version_pin: str | None = None
    epistemic_label: str = "attested-user"
    created_at: str | None = None


class AcceptanceImpactAssessment(BaseModel):
    """AcceptanceImpactAssessment DTO — a Derived drift assessment (DTM-0017).

    "A decision you confirmed is affected." Derived, never canonical: the
    ``label`` carries ``epistemic_label='derived'``. It holds REFERENCES to the
    UAR + the pinned/latest CHR — never the rows themselves.
    """

    uar_ref: str
    project_id: str
    pinned_chr: str
    latest_chr: str
    delta: float
    band_changed: bool
    pinned_band: ConfidenceBand | None = None
    latest_band: ConfidenceBand | None = None
    label: DerivedEnvelope = Field(default_factory=DerivedEnvelope)


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

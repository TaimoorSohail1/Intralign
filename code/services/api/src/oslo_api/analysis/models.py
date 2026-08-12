from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from oslo_api.analysis.integrity import Integrity, OutcomeCheckpoint


class RunKind(StrEnum):
    INITIAL = "initial"
    EXTENDED = "extended"


class AnalysisPassKind(StrEnum):
    FAST = "fast"
    DEEP = "deep"


class ReanalysisTrigger(StrEnum):
    INTAKE = "intake"
    BATCH = "batch"
    EXPLICIT = "explicit"
    DEEP_SUPERSEDE = "deep_supersede"


class AnalysisRunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AnalysisPhase(StrEnum):
    SUBMIT_INTAKE = "submit_intake"
    VALIDATE_SCOPE = "validate_scope"
    INGEST_PARSE = "ingest_parse"
    PERCEIVE = "perceive"
    RETRIEVE_EVIDENCE = "retrieve_evidence"
    CONSTRUCT_ARTIFACTS = "construct_artifacts"
    CHECKPOINT = "checkpoint"
    EVALUATE_ADVISE = "evaluate_advise"
    VALIDATE_RESULT = "validate_result"
    PUBLISH = "publish"
    PROJECT_BROWSER = "project_browser"
    EXTENDED_TRANSITION = "extended_transition"


class ArtifactType(StrEnum):
    INTENT = "intent"
    CONTEXT = "context"
    SCOPE = "scope"
    REQUIREMENTS = "requirements"
    WORK_BREAKDOWN = "work_breakdown"
    SCHEDULE = "schedule"
    RESOURCES = "resources"


ARTIFACT_TYPES = tuple(ArtifactType)


class ClaimKind(StrEnum):
    DATE = "date"
    DATE_RANGE = "date_range"
    MONEY = "money"
    PERCENTAGE = "percentage"
    QUANTITY = "quantity"
    REQUIREMENT = "requirement"
    CONSTRAINT = "constraint"
    DEPENDENCY = "dependency"
    OWNER = "owner"
    ASSUMPTION = "assumption"
    DECISION = "decision"
    RISK = "risk"
    TEXT = "text"


class ClaimProvenance(StrEnum):
    SOURCE_GROUNDED = "source_grounded"
    OSLO_INFERRED = "oslo_inferred"
    CONFIRMED_BY_USER = "confirmed_by_user"


@dataclass(frozen=True, slots=True)
class AnalysisRunRequest:
    workspace_id: UUID
    project_id: UUID
    requested_by: UUID
    kind: RunKind
    description: str
    source_names: tuple[str, ...]
    source_document_ids: tuple[UUID, ...] = ()
    user_evidence: tuple[EvidenceFragment, ...] = ()
    idempotency_key: str | None = None
    parent_run_id: UUID | None = None
    fail_at: AnalysisPhase | None = None
    consumes_analysis_allowance: bool = False
    pass_kind: AnalysisPassKind = AnalysisPassKind.FAST
    reanalysis_trigger: ReanalysisTrigger = ReanalysisTrigger.INTAKE
    consolidated_event_ids: tuple[UUID, ...] = ()
    provisional: bool = False
    auto_retry_count: int = 0


@dataclass(frozen=True, slots=True)
class EvidenceFragment:
    reference: str
    content: str
    source_name: str | None = None
    location: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceCitation:
    reference: str
    source_name: str
    location: str
    excerpt: str


@dataclass(frozen=True, slots=True)
class HarnessCallMetadata:
    provider: str
    model: str
    prompt_version: str
    response_id: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: int = 0
    attempts: int = 1
    mode: str = "primary"
    fallback_reason: str | None = None


@dataclass(slots=True)
class HarnessInvocation:
    run_id: UUID
    phase: AnalysisPhase
    metadata: HarnessCallMetadata | None = None


@dataclass(frozen=True, slots=True)
class EvidenceClaim:
    id: str
    kind: ClaimKind
    subject: str
    predicate: str
    value: str
    raw_text: str
    evidence_ref: str
    source_name: str | None = None
    location: str | None = None
    unit: str | None = None
    numeric_value: float | None = None
    provenance: ClaimProvenance = ClaimProvenance.SOURCE_GROUNDED


@dataclass(frozen=True, slots=True)
class ClaimRelation:
    source_claim_id: str
    target_claim_id: str
    relation_type: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvidenceGraph:
    claims: tuple[EvidenceClaim, ...]
    relations: tuple[ClaimRelation, ...]


@dataclass(frozen=True, slots=True)
class Perception:
    facts: tuple[str, ...]
    claims: tuple[str, ...]
    gaps: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    evidence: tuple[EvidenceFragment, ...] = ()
    structured_claims: tuple[EvidenceClaim, ...] = ()
    claim_relations: tuple[ClaimRelation, ...] = ()


@dataclass(frozen=True, slots=True)
class ArtifactSection:
    heading: str
    body: str = ""
    bullets: tuple[str, ...] = ()
    columns: tuple[str, ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()
    evidence_refs: tuple[str, ...] = ()
    row_evidence_refs: tuple[tuple[str, ...], ...] = ()
    row_states: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ArtifactAssumption:
    id: str
    statement: str
    state: str
    load_bearing: bool
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ArtifactConflict:
    id: str
    field: str
    values: tuple[str, ...]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Artifact:
    artifact_type: ArtifactType
    title: str
    summary: str
    reliability: str
    evidence_refs: tuple[str, ...]
    basis: str = "derived"
    sections: tuple[ArtifactSection, ...] = ()
    assumptions: tuple[ArtifactAssumption, ...] = ()
    conflicts: tuple[ArtifactConflict, ...] = ()
    project_title: str | None = None


@dataclass(frozen=True, slots=True)
class Issue:
    id: str
    artifact_type: ArtifactType
    dimension: str
    severity: str
    title: str
    why: str
    recommendation: str
    evidence_refs: tuple[str, ...]
    clarification: str | None = None
    status: str = "open"
    dimensions: tuple[str, ...] = ()
    finding_type: str = ""
    section: str = ""
    recommendation_from_oslo: bool = True
    load_bearing: bool = True
    exposure_rank: float = 0


@dataclass(frozen=True, slots=True)
class ReliabilityBasis:
    coverage: str
    evidence: str
    assessability: str


@dataclass(frozen=True, slots=True)
class Assessment:
    confidence_index: int
    confidence_band: str
    reliability: str
    clarity: str
    alignment: str
    feasibility: str
    issues: tuple[Issue, ...]
    understanding_stage: str = "orientation"
    reliability_basis: ReliabilityBasis = field(
        default_factory=lambda: ReliabilityBasis(
            coverage="Low",
            evidence="Low",
            assessability="Low",
        )
    )
    confidence_direction: str = "unchanged"
    limiting_dimension: str = "feasibility"
    false_confidence: bool = False
    confidence_explanation: str = ""
    resolved_issue_count: int = 0
    confirmed_dependency_count: int = 0
    outcome_checkpoints: tuple[OutcomeCheckpoint, ...] = ()
    integrity: Integrity | None = None


@dataclass(frozen=True, slots=True)
class AssessmentSnapshot:
    id: UUID
    analysis_run_id: UUID
    workspace_id: UUID
    project_id: UUID
    state: str
    summary: str
    artifacts: tuple[Artifact, ...]
    assessment: Assessment
    published_at: datetime
    evidence_citations: tuple[EvidenceCitation, ...] = ()
    project_title: str | None = None
    source_document_count: int = 0


@dataclass(frozen=True, slots=True)
class AnalysisEvent:
    run_id: UUID
    sequence: int
    event_type: str
    status: str
    phase: AnalysisPhase | None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    error_code: str | None = None
    retryable: bool | None = None
    artifact_type: ArtifactType | None = None


@dataclass(slots=True)
class AnalysisRun:
    id: UUID
    request: AnalysisRunRequest
    status: AnalysisRunStatus
    current_phase: AnalysisPhase | None = None
    completed_phases: list[AnalysisPhase] = field(default_factory=list)
    checkpoint_state: dict[str, object] = field(default_factory=dict)
    error_code: str | None = None
    snapshot: AssessmentSnapshot | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def queued(cls, request: AnalysisRunRequest) -> AnalysisRun:
        return cls(id=uuid4(), request=request, status=AnalysisRunStatus.QUEUED)


@dataclass(frozen=True, slots=True)
class AnalysisRunResult:
    run_id: UUID
    status: AnalysisRunStatus
    snapshot: AssessmentSnapshot | None
    error_code: str | None = None

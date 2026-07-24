from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


class RunKind(StrEnum):
    INITIAL = "initial"
    EXTENDED = "extended"


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


@dataclass(frozen=True, slots=True)
class AnalysisRunRequest:
    workspace_id: UUID
    project_id: UUID
    requested_by: UUID
    kind: RunKind
    description: str
    source_names: tuple[str, ...]
    source_document_ids: tuple[UUID, ...] = ()
    idempotency_key: str | None = None
    parent_run_id: UUID | None = None
    fail_at: AnalysisPhase | None = None


@dataclass(frozen=True, slots=True)
class EvidenceFragment:
    reference: str
    content: str


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
    fallback_active: bool = False
    metadata: HarnessCallMetadata | None = None


@dataclass(frozen=True, slots=True)
class Perception:
    facts: tuple[str, ...]
    claims: tuple[str, ...]
    gaps: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    evidence: tuple[EvidenceFragment, ...] = ()


@dataclass(frozen=True, slots=True)
class Artifact:
    artifact_type: ArtifactType
    title: str
    summary: str
    reliability: str
    evidence_refs: tuple[str, ...]
    basis: str = "derived"


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


@dataclass(frozen=True, slots=True)
class Assessment:
    confidence_index: int
    confidence_band: str
    reliability: str
    clarity: str
    alignment: str
    feasibility: str
    issues: tuple[Issue, ...]


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
    def queued(cls, request: AnalysisRunRequest) -> "AnalysisRun":
        return cls(id=uuid4(), request=request, status=AnalysisRunStatus.QUEUED)


@dataclass(frozen=True, slots=True)
class AnalysisRunResult:
    run_id: UUID
    status: AnalysisRunStatus
    snapshot: AssessmentSnapshot | None
    error_code: str | None = None

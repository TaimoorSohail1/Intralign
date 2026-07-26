import json
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator, model_validator

from oslo_api.analysis import AnalysisEvent, AnalysisRun, AssessmentSnapshot, RunKind
from oslo_api.analysis.advisor import (
    ProjectAdvisor,
    ProjectAdvisorError,
    build_project_advisor,
)
from oslo_api.analysis.documents import MAX_DOCUMENT_BYTES, DocumentRejected
from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.slice_two import (
    SliceTwoApplication,
    SliceTwoArtifactConflict,
    SliceTwoIssueNotAnswerable,
    SliceTwoNotFound,
    SliceTwoPermissionDenied,
)

router = APIRouter(prefix="/v1", tags=["analysis"])


class StartAnalysisRequest(BaseModel):
    kind: RunKind = RunKind.INITIAL
    description: str = Field(default="", max_length=100_000)
    source_names: list[str] = Field(default_factory=list, max_length=10)
    source_document_ids: list[UUID] = Field(default_factory=list, max_length=10)

    @model_validator(mode="after")
    def meaningful_input(self) -> "StartAnalysisRequest":
        if (
            not self.description.strip()
            and not self.source_names
            and not self.source_document_ids
        ):
            raise ValueError("A description or document is required")
        return self


class StartAnalysisResponse(BaseModel):
    run_id: UUID
    project_id: UUID
    kind: RunKind
    status: str


class UploadedDocumentResponse(BaseModel):
    document_id: UUID
    file_name: str
    status: str
    fragment_count: int


class AnalysisRunResponse(BaseModel):
    run_id: UUID
    project_id: UUID
    kind: RunKind
    status: str
    phase: str | None
    completed_phases: list[str]
    error_code: str | None


class ArtifactResponse(BaseModel):
    artifact_type: str
    title: str
    summary: str
    reliability: str
    evidence_refs: list[str]
    basis: str


class EvidenceResponse(BaseModel):
    source_name: str
    location: str
    excerpt: str


class IssueResponse(BaseModel):
    id: str
    artifact_type: str
    dimension: str
    severity: str
    title: str
    why: str
    recommendation: str
    evidence_refs: list[str]
    evidence: list[EvidenceResponse]
    clarification: str | None
    status: str


class ReliabilityBasisResponse(BaseModel):
    coverage: str
    evidence: str
    assessability: str


class AssessmentResponse(BaseModel):
    confidence_index: int
    confidence_band: str
    reliability: str
    clarity: str
    alignment: str
    feasibility: str
    issues: list[IssueResponse]
    understanding_stage: str
    reliability_basis: ReliabilityBasisResponse
    confidence_direction: str
    limiting_dimension: str
    false_confidence: bool
    confidence_explanation: str
    resolved_issue_count: int
    confirmed_dependency_count: int


class OverviewResponse(BaseModel):
    snapshot_id: UUID
    analysis_run_id: UUID
    project_id: UUID
    orientation_seen: bool
    state: Literal["provisional", "current", "last_good"]
    summary: str
    artifacts: list[ArtifactResponse]
    assessment: AssessmentResponse
    published_at: datetime
    extended_analysis: AnalysisRunResponse | None = None


class AdvisorMessageRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1_000)

    @field_validator("question")
    @classmethod
    def meaningful_question(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("A question is required")
        return normalized


class AdvisorMessageResponse(BaseModel):
    answer: str
    follow_up_questions: list[str]


class IssueAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=5_000)

    @field_validator("answer")
    @classmethod
    def meaningful_answer(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("An answer is required")
        return normalized


class ArtifactSectionPayload(BaseModel):
    heading: str = Field(default="", max_length=200)
    body: str = Field(default="", max_length=100_000)
    bullets: list[str] = Field(default_factory=list, max_length=100)
    columns: list[str] = Field(default_factory=list, max_length=20)
    rows: list[list[str]] = Field(default_factory=list, max_length=500)

    @field_validator("bullets")
    @classmethod
    def validate_bullets(cls, value: list[str]) -> list[str]:
        if any(len(item) > 10_000 for item in value):
            raise ValueError("Artifact bullet is too long")
        return value

    @model_validator(mode="after")
    def validate_table_shape(self) -> "ArtifactSectionPayload":
        if self.rows and not self.columns:
            raise ValueError("Artifact rows require columns")
        if any(len(row) != len(self.columns) for row in self.rows):
            raise ValueError("Artifact rows must match the column count")
        if any(len(cell) > 10_000 for row in self.rows for cell in row):
            raise ValueError("Artifact cell is too long")
        return self


class ArtifactContentPayload(BaseModel):
    sections: list[ArtifactSectionPayload] = Field(min_length=1, max_length=20)


class ArtifactUpdateRequest(BaseModel):
    content: ArtifactContentPayload
    expected_version: int = Field(ge=1)


class ArtifactWorkspaceResponse(BaseModel):
    artifact_type: str
    title: str
    content: ArtifactContentPayload
    version: int
    provenance: Literal["from_oslo", "confirmed_by_user"]
    reliability: str
    basis: str
    evidence_refs: list[str]
    issues: list[IssueResponse]
    updated_at: datetime
    analysis_run: AnalysisRunResponse | None = None


def slice_two_application(request: Request) -> SliceTwoApplication:
    application: SliceTwoApplication | None = request.app.state.slice_two
    if application is None:
        from oslo_api.analysis.service import build_slice_two_application

        application = build_slice_two_application()
        request.app.state.slice_two = application
    return application


def project_advisor(request: Request) -> ProjectAdvisor:
    advisor: ProjectAdvisor | None = request.app.state.project_advisor
    if advisor is None:
        from oslo_api.settings import Settings

        advisor = build_project_advisor(Settings())
        request.app.state.project_advisor = advisor
    return advisor


def _start_response(run: AnalysisRun) -> StartAnalysisResponse:
    return StartAnalysisResponse(
        run_id=run.id,
        project_id=run.request.project_id,
        kind=run.request.kind,
        status=run.status.value,
    )


def _run_response(run: AnalysisRun) -> AnalysisRunResponse:
    return AnalysisRunResponse(
        run_id=run.id,
        project_id=run.request.project_id,
        kind=run.request.kind,
        status=run.status.value,
        phase=run.current_phase.value if run.current_phase else None,
        completed_phases=[phase.value for phase in run.completed_phases],
        error_code=run.error_code,
    )


def _overview_response(
    snapshot: AssessmentSnapshot,
    extended_analysis: AnalysisRun | None = None,
    *,
    orientation_seen: bool = False,
) -> OverviewResponse:
    citations = {
        citation.reference: EvidenceResponse(
            source_name=citation.source_name,
            location=citation.location,
            excerpt=citation.excerpt,
        )
        for citation in snapshot.evidence_citations
    }
    return OverviewResponse(
        snapshot_id=snapshot.id,
        analysis_run_id=snapshot.analysis_run_id,
        project_id=snapshot.project_id,
        orientation_seen=orientation_seen,
        state=snapshot.state,  # type: ignore[arg-type]
        summary=snapshot.summary,
        artifacts=[
            ArtifactResponse(
                artifact_type=artifact.artifact_type.value,
                title=artifact.title,
                summary=artifact.summary,
                reliability=artifact.reliability,
                evidence_refs=list(artifact.evidence_refs),
                basis=artifact.basis,
            )
            for artifact in snapshot.artifacts
        ],
        assessment=AssessmentResponse(
            confidence_index=snapshot.assessment.confidence_index,
            confidence_band=snapshot.assessment.confidence_band,
            reliability=snapshot.assessment.reliability,
            clarity=snapshot.assessment.clarity,
            alignment=snapshot.assessment.alignment,
            feasibility=snapshot.assessment.feasibility,
            understanding_stage=snapshot.assessment.understanding_stage,
            reliability_basis=ReliabilityBasisResponse(
                coverage=snapshot.assessment.reliability_basis.coverage,
                evidence=snapshot.assessment.reliability_basis.evidence,
                assessability=snapshot.assessment.reliability_basis.assessability,
            ),
            confidence_direction=snapshot.assessment.confidence_direction,
            limiting_dimension=snapshot.assessment.limiting_dimension,
            false_confidence=snapshot.assessment.false_confidence,
            confidence_explanation=snapshot.assessment.confidence_explanation,
            resolved_issue_count=snapshot.assessment.resolved_issue_count,
            confirmed_dependency_count=snapshot.assessment.confirmed_dependency_count,
            issues=[
                IssueResponse(
                    id=issue.id,
                    artifact_type=issue.artifact_type.value,
                    dimension=issue.dimension,
                    severity=issue.severity,
                    title=issue.title,
                    why=issue.why,
                    recommendation=issue.recommendation,
                    evidence_refs=list(issue.evidence_refs),
                    evidence=[
                        citations[reference]
                        for reference in issue.evidence_refs
                        if reference in citations
                    ],
                    clarification=issue.clarification,
                    status=issue.status,
                )
                for issue in snapshot.assessment.issues
            ],
        ),
        published_at=snapshot.published_at,
        extended_analysis=(
            _run_response(extended_analysis) if extended_analysis is not None else None
        ),
    )


def _artifact_workspace_response(
    artifact: dict,
    run: AnalysisRun | None = None,
) -> ArtifactWorkspaceResponse:
    citations = {
        citation.reference: EvidenceResponse(
            source_name=citation.source_name,
            location=citation.location,
            excerpt=citation.excerpt,
        )
        for citation in artifact.get("evidence_citations", [])
    }
    return ArtifactWorkspaceResponse(
        artifact_type=artifact["artifact_type"],
        title=artifact["title"],
        content=ArtifactContentPayload.model_validate(artifact["content"]),
        version=artifact["version"],
        provenance=artifact["provenance"],
        reliability=artifact["reliability"],
        basis=artifact["basis"],
        evidence_refs=artifact["evidence_refs"],
        issues=[
            IssueResponse(
                id=issue.id,
                artifact_type=issue.artifact_type.value,
                dimension=issue.dimension,
                severity=issue.severity,
                title=issue.title,
                why=issue.why,
                recommendation=issue.recommendation,
                evidence_refs=list(issue.evidence_refs),
                evidence=[
                    citations[reference]
                    for reference in issue.evidence_refs
                    if reference in citations
                ],
                clarification=issue.clarification,
                status=issue.status,
            )
            for issue in artifact["issues"]
        ],
        updated_at=artifact["updated_at"],
        analysis_run=_run_response(run) if run is not None else None,
    )


@router.post(
    "/projects/{project_id}/documents",
    response_model=UploadedDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
    file: Annotated[UploadFile, File()],
) -> UploadedDocumentResponse:
    content = await file.read(MAX_DOCUMENT_BYTES + 1)
    try:
        document = slice_two_application(request).upload_document(
            actor_user_id=context.user.id,
            project_id=project_id,
            file_name=file.filename or "document",
            content_type=file.content_type,
            content=content,
        )
    except SliceTwoPermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except DocumentRejected as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    return UploadedDocumentResponse(
        document_id=document.id,
        file_name=document.file_name,
        status=document.status,
        fragment_count=document.fragment_count,
    )


@router.post(
    "/projects/{project_id}/analysis-runs",
    response_model=StartAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_analysis(
    project_id: UUID,
    payload: StartAnalysisRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=200)],
) -> StartAnalysisResponse:
    try:
        run = slice_two_application(request).start_analysis(
            actor_user_id=context.user.id,
            project_id=project_id,
            description=payload.description.strip(),
            source_names=tuple(payload.source_names),
            source_document_ids=tuple(payload.source_document_ids),
            kind=payload.kind,
            key=idempotency_key,
        )
    except SliceTwoPermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    return _start_response(run)


@router.get("/analysis-runs/{run_id}", response_model=AnalysisRunResponse)
def get_analysis_run(
    run_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> AnalysisRunResponse:
    try:
        run = slice_two_application(request).get_run(
            actor_user_id=context.user.id,
            run_id=run_id,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    return _run_response(run)


@router.post(
    "/analysis-runs/{run_id}/retry",
    response_model=StartAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def retry_analysis(
    run_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> StartAnalysisResponse:
    try:
        run = slice_two_application(request).retry(
            actor_user_id=context.user.id,
            run_id=run_id,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    return _start_response(run)


@router.get("/projects/{project_id}/overview", response_model=OverviewResponse)
def current_overview(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> OverviewResponse:
    try:
        application = slice_two_application(request)
        snapshot = application.current_overview(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
        extended_analysis = application.latest_extended_run(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
        orientation_seen = application.has_seen_orientation(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    return _overview_response(
        snapshot,
        extended_analysis,
        orientation_seen=orientation_seen,
    )


@router.post(
    "/projects/{project_id}/advisor/messages",
    response_model=AdvisorMessageResponse,
)
def ask_project_advisor(
    project_id: UUID,
    payload: AdvisorMessageRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> AdvisorMessageResponse:
    try:
        snapshot = slice_two_application(request).current_overview(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
        reply = project_advisor(request).answer(
            snapshot=snapshot,
            question=payload.question,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except ProjectAdvisorError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Project Advisor is temporarily unavailable",
        ) from error
    return AdvisorMessageResponse(
        answer=reply.answer,
        follow_up_questions=list(reply.follow_up_questions),
    )


@router.get(
    "/projects/{project_id}/artifacts/{artifact_type}",
    response_model=ArtifactWorkspaceResponse,
)
def get_project_artifact(
    project_id: UUID,
    artifact_type: str,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> ArtifactWorkspaceResponse:
    try:
        artifact = slice_two_application(request).get_artifact(
            actor_user_id=context.user.id,
            project_id=project_id,
            artifact_type=artifact_type,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    return _artifact_workspace_response(artifact)


@router.patch(
    "/projects/{project_id}/artifacts/{artifact_type}",
    response_model=ArtifactWorkspaceResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_project_artifact(
    project_id: UUID,
    artifact_type: str,
    payload: ArtifactUpdateRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8, max_length=200),
    ],
) -> ArtifactWorkspaceResponse:
    try:
        artifact, run = slice_two_application(request).update_artifact(
            actor_user_id=context.user.id,
            project_id=project_id,
            artifact_type=artifact_type,
            content=payload.content.model_dump(),
            expected_version=payload.expected_version,
            key=idempotency_key,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except SliceTwoArtifactConflict as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ARTIFACT_VERSION_CONFLICT",
        ) from error
    return _artifact_workspace_response(artifact, run)


@router.post(
    "/projects/{project_id}/issues/{issue_id}/answers",
    response_model=StartAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def answer_project_issue(
    project_id: UUID,
    issue_id: str,
    payload: IssueAnswerRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
    idempotency_key: Annotated[
        str,
        Header(alias="Idempotency-Key", min_length=8, max_length=200),
    ],
) -> StartAnalysisResponse:
    try:
        run = slice_two_application(request).answer_issue(
            actor_user_id=context.user.id,
            project_id=project_id,
            issue_id=issue_id,
            answer=payload.answer,
            key=idempotency_key,
        )
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error
    except SliceTwoIssueNotAnswerable as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISSUE_NOT_ANSWERABLE",
        ) from error
    return _start_response(run)


@router.post("/workspaces/{workspace_id}/orientation-seen", status_code=status.HTTP_204_NO_CONTENT)
def mark_orientation_seen(
    workspace_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
) -> None:
    try:
        slice_two_application(request).mark_orientation_seen(
            actor_user_id=context.user.id,
            workspace_id=workspace_id,
        )
    except SliceTwoPermissionDenied as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error


def _format_sse(event: AnalysisEvent) -> str:
    payload = {
        "schema_version": "1",
        "run_id": str(event.run_id),
        "sequence": event.sequence,
        "status": event.status,
        "phase": event.phase.value if event.phase else None,
        "occurred_at": event.occurred_at.isoformat(),
        "error": (
            {"code": event.error_code, "retryable": event.retryable}
            if event.error_code
            else None
        ),
    }
    return (
        f"id: {event.sequence}\n"
        f"event: {event.event_type}\n"
        "retry: 3000\n"
        f"data: {json.dumps(payload, separators=(',', ':'))}\n\n"
    )


@router.get("/analysis-runs/{run_id}/events")
def stream_analysis_events(
    run_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    request: Request,
    last_event_id: Annotated[int, Header(alias="Last-Event-ID", ge=0)] = 0,
) -> StreamingResponse:
    application = slice_two_application(request)
    try:
        application.get_run(actor_user_id=context.user.id, run_id=run_id)
    except (SliceTwoPermissionDenied, SliceTwoNotFound) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from error

    def event_stream():
        sequence = last_event_id
        while True:
            events = application.wait_for_events(
                actor_user_id=context.user.id,
                run_id=run_id,
                sequence=sequence,
                timeout=15,
            )
            if not events:
                yield ": keepalive\n\n"
                continue
            for event in events:
                sequence = event.sequence
                yield _format_sse(event)
                if event.event_type in {
                    "analysis.completed",
                    "analysis.failed",
                    "analysis.cancelled",
                }:
                    return

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )

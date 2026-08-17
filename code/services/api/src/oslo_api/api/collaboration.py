from __future__ import annotations

import re
from datetime import datetime, time
from typing import Annotated, Literal
from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.collaboration.asana import HttpAsanaGateway
from oslo_api.collaboration.pdf import (
    render_full_plan_pdf,
    render_report_pdf,
    render_snapshot_pdf,
)
from oslo_api.collaboration.service import CollaborationError, DatabaseCollaborationService
from oslo_api.email import PostmarkReportMailer, SmtpReportMailer
from oslo_api.settings import Settings
from oslo_api.slice_two import SliceTwoApplication

router = APIRouter(prefix="/v1", tags=["collaboration"])


def collaboration_service(request: Request) -> DatabaseCollaborationService:
    service = request.app.state.collaboration
    if service is None:
        settings = Settings()
        if settings.postmark_server_token:
            report_mailer = PostmarkReportMailer(
                server_token=settings.postmark_server_token.get_secret_value(),
                sender=settings.email_from,
                sender_name=settings.from_name,
            )
        else:
            report_mailer = SmtpReportMailer(
                host=settings.smtp_host,
                port=settings.smtp_port,
                sender=settings.email_sender,
            )
        service = DatabaseCollaborationService(
            create_engine(settings.database_url, pool_pre_ping=True),
            settings.web_url,
            report_mailer,
            report_mailer,
            (
                HttpAsanaGateway(
                    access_token=settings.asana_access_token.get_secret_value(),
                    destination_gid=settings.asana_project_gid,
                )
                if settings.asana_access_token and settings.asana_project_gid
                else None
            ),
        )
        request.app.state.collaboration = service
    return service


def slice_two_application(request: Request) -> SliceTwoApplication:
    application = request.app.state.slice_two
    if application is None:
        from oslo_api.analysis.service import build_slice_two_application

        application = build_slice_two_application()
        request.app.state.slice_two = application
    return application


def guarded(call):
    try:
        return call()
    except CollaborationError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail={"code": error.code, "message": error.message},
        ) from error


class CommentRequest(BaseModel):
    body: str = Field(min_length=1, max_length=5_000)
    mentions: list[str] = Field(default_factory=list, max_length=20)


class ReviewRequest(BaseModel):
    issue_id: str = Field(min_length=1, max_length=200)
    reviewer_name: str = Field(min_length=1, max_length=120)
    reviewer_email: EmailStr | None = None
    question: str = Field(min_length=1, max_length=1_000)
    source_ref: str = Field(min_length=1, max_length=1_000)
    source_excerpt: str = Field(min_length=1, max_length=5_000)


class SnapshotShareRequest(BaseModel):
    recipient_name: str = Field(min_length=1, max_length=120)
    recipient_email: EmailStr | None = None


class ReviewResponseRequest(BaseModel):
    kind: Literal["comment", "approve", "reject", "suggest_alternative"]
    body: str = Field(min_length=1, max_length=5_000)


class ScopedReviewSource(BaseModel):
    reference: str = Field(min_length=1, max_length=1_000)
    excerpt: str = Field(min_length=1, max_length=5_000)


class ScopedReviewResponse(BaseModel):
    id: str
    reviewer_name: str
    project_name: str
    expires_at: datetime
    question: str
    source: ScopedReviewSource
    response_kind: str | None = None


class ReportSectionRequest(BaseModel):
    id: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9_-]+$")
    title: str = Field(min_length=1, max_length=160)
    body: list[str] = Field(min_length=1, max_length=100)


class ReportContentRequest(BaseModel):
    sections: list[ReportSectionRequest] = Field(min_length=7, max_length=20)


class ReportDraftRequest(BaseModel):
    snapshot_id: UUID
    content: ReportContentRequest
    recipient_class: Literal["exec-sponsor", "team", "board"] = "exec-sponsor"
    composition_depth: Literal["summary", "full"] = "full"
    included: dict[str, bool] = Field(default_factory=dict)
    revision: int = Field(default=1, ge=1)


class ReportDeliveryRequest(ReportDraftRequest):
    recipient_email: EmailStr
    recipient_label: str = Field(min_length=1, max_length=120)
    subject: str = Field(min_length=1, max_length=200)
    scheduled_for: datetime | None = None
    confirm_previous_analysis: bool = False


class ReportScheduleRequest(BaseModel):
    recipient_email: EmailStr
    recipient_class: Literal["exec-sponsor", "team", "board"]
    weekday: int = Field(ge=0, le=6)
    local_time: time
    timezone: str = Field(min_length=1, max_length=80)


class ReportScheduleStateRequest(BaseModel):
    state: Literal["enabled", "paused"]


class ReportExportRecordRequest(BaseModel):
    format: Literal["pdf", "excel", "csv", "text", "copy-summary", "asana"]
    content_checksum: str | None = Field(default=None, max_length=128)
    surface: Literal["report", "full_plan"] = "report"


def download_disposition(project_name: str, suffix: str) -> str:
    filename = f"{project_name}-{suffix}.pdf"
    ascii_name = re.sub(r"[^A-Za-z0-9._-]+", "-", filename).strip("-")
    return (
        f'attachment; filename="{ascii_name or suffix + ".pdf"}"; '
        f"filename*=UTF-8''{quote(filename)}"
    )


@router.get("/projects/{project_id}/collaboration")
def get_collaboration(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.state(actor_user_id=context.user.id, project_id=project_id))


@router.get("/projects/{project_id}/collaboration/roll-up")
def get_collaboration_roll_up(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.roll_up(actor_user_id=context.user.id, project_id=project_id))


@router.get("/projects/{project_id}/collaboration/grounding-map")
def get_collaboration_grounding_map(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.grounding_map(actor_user_id=context.user.id, project_id=project_id)
    )


@router.get("/projects/{project_id}/report")
def get_report(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.report_state(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    )


@router.put("/projects/{project_id}/report")
def save_report(
    project_id: UUID,
    payload: ReportDraftRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.save_report(
            actor_user_id=context.user.id,
            project_id=project_id,
            snapshot_id=payload.snapshot_id,
            content=payload.content.model_dump(),
            recipient_class=payload.recipient_class,
            composition_depth=payload.composition_depth,
            included=payload.included,
            revision=payload.revision,
        )
    )


@router.post("/projects/{project_id}/report/deliveries", status_code=201)
def deliver_report(
    project_id: UUID,
    payload: ReportDeliveryRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.deliver_report(
            actor_user_id=context.user.id,
            project_id=project_id,
            snapshot_id=payload.snapshot_id,
            recipient_email=str(payload.recipient_email),
            recipient_label=payload.recipient_label,
            subject=payload.subject,
            content=payload.content.model_dump(),
            scheduled_for=payload.scheduled_for,
            confirm_previous_analysis=payload.confirm_previous_analysis,
        )
    )


@router.get("/projects/{project_id}/reports/pdf")
def export_report(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> Response:
    report = guarded(
        lambda: service.report_state(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    )
    if not report["content"]:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "REPORT_NOT_SAVED",
                "message": "Save the report before exporting.",
            },
        )
    pdf = render_report_pdf(
        report["project_name"],
        report["content"],
        analysis_completed_at=report["analysis_completed_at"],
    )
    return Response(
        pdf,
        media_type="application/pdf",
        headers={
            "content-disposition": download_disposition(
                report["project_name"],
                "readout",
            )
        },
    )


@router.post("/projects/{project_id}/issues/{issue_id}/comments", status_code=201)
def add_comment(
    project_id: UUID,
    issue_id: str,
    payload: CommentRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.add_comment(
            actor_user_id=context.user.id,
            project_id=project_id,
            issue_id=issue_id,
            body=payload.body,
            mentions=payload.mentions,
        )
    )


@router.post("/projects/{project_id}/share-links", status_code=201)
def create_share_link(
    project_id: UUID,
    payload: SnapshotShareRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.create_snapshot_link(
            actor_user_id=context.user.id,
            project_id=project_id,
            recipient_name=payload.recipient_name,
            recipient_email=(str(payload.recipient_email) if payload.recipient_email else None),
        )
    )


@router.delete("/projects/{project_id}/share-links/{link_id}", status_code=204)
def revoke_share_link(
    project_id: UUID,
    link_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> None:
    guarded(
        lambda: service.revoke_share_link(
            actor_user_id=context.user.id, project_id=project_id, link_id=link_id
        )
    )


@router.post("/projects/{project_id}/review-grants", status_code=201)
def create_review_grant(
    project_id: UUID,
    payload: ReviewRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.create_review_grant(
            actor_user_id=context.user.id,
            project_id=project_id,
            issue_id=payload.issue_id,
            reviewer_name=payload.reviewer_name,
            reviewer_email=str(payload.reviewer_email) if payload.reviewer_email else None,
            question=payload.question,
            source_ref=payload.source_ref,
            source_excerpt=payload.source_excerpt,
        )
    )


@router.delete("/projects/{project_id}/review-grants/{grant_id}", status_code=204)
def revoke_review_grant(
    project_id: UUID,
    grant_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> None:
    guarded(
        lambda: service.revoke_review_grant(
            actor_user_id=context.user.id, project_id=project_id, grant_id=grant_id
        )
    )


@router.get("/projects/{project_id}/report/schedules")
def get_report_schedules(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> list[dict]:
    return guarded(
        lambda: service.report_schedules(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    )


@router.post("/projects/{project_id}/report/schedules", status_code=201)
def create_report_schedule(
    project_id: UUID,
    payload: ReportScheduleRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.create_report_schedule(
            actor_user_id=context.user.id,
            project_id=project_id,
            recipient_email=str(payload.recipient_email),
            recipient_class=payload.recipient_class,
            weekday=payload.weekday,
            local_time=payload.local_time,
            timezone=payload.timezone,
        )
    )


@router.patch("/projects/{project_id}/report/schedules/{schedule_id}")
def update_report_schedule(
    project_id: UUID,
    schedule_id: UUID,
    payload: ReportScheduleStateRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.update_report_schedule(
            actor_user_id=context.user.id,
            project_id=project_id,
            schedule_id=schedule_id,
            state=payload.state,
        )
    )


@router.delete(
    "/projects/{project_id}/report/schedules/{schedule_id}", status_code=204
)
def delete_report_schedule(
    project_id: UUID,
    schedule_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> Response:
    guarded(
        lambda: service.delete_report_schedule(
            actor_user_id=context.user.id,
            project_id=project_id,
            schedule_id=schedule_id,
        )
    )
    return Response(status_code=204)


@router.post("/projects/{project_id}/report/exports", status_code=201)
def record_report_export(
    project_id: UUID,
    payload: ReportExportRecordRequest,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.record_report_export(
            actor_user_id=context.user.id,
            project_id=project_id,
            export_format=payload.format,
            content_checksum=payload.content_checksum,
            surface=payload.surface,
        )
    )


@router.get("/projects/{project_id}/report/asana")
def get_asana_handoff_state(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.asana_handoff_state(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    )


@router.post("/projects/{project_id}/report/asana", status_code=201)
def import_asana_handoff(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.import_asana_handoff(
            actor_user_id=context.user.id,
            project_id=project_id,
        )
    )


@router.post("/projects/{project_id}/review-grants/{grant_id}/deliveries/manual")
def mark_review_delivered_manually(
    project_id: UUID,
    grant_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.mark_review_delivered(
            actor_user_id=context.user.id,
            project_id=project_id,
            grant_id=grant_id,
        )
    )


@router.get("/projects/{project_id}/exports/pdf")
def export_project(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> Response:
    snapshot = guarded(
        lambda: service.record_export(actor_user_id=context.user.id, project_id=project_id)
    )
    pdf = render_snapshot_pdf(
        snapshot["project_name"],
        snapshot["snapshot_json"],
        analysis_completed_at=snapshot["published_at"],
    )
    return Response(
        pdf,
        media_type="application/pdf",
        headers={
            "content-disposition": download_disposition(
                snapshot["project_name"],
                "snapshot",
            )
        },
    )


@router.get("/projects/{project_id}/full-plan/export/pdf")
def export_full_plan(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> Response:
    snapshot = guarded(
        lambda: service.record_export(
            actor_user_id=context.user.id,
            project_id=project_id,
            surface="full_plan",
        )
    )
    pdf = render_full_plan_pdf(
        snapshot["project_name"],
        snapshot["snapshot_json"],
        analysis_completed_at=snapshot["published_at"],
    )
    return Response(
        pdf,
        media_type="application/pdf",
        headers={
            "content-disposition": download_disposition(
                snapshot["project_name"],
                "full-plan",
            )
        },
    )
@router.get("/public/share/{token}")
def public_snapshot(
    token: str,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.resolve_snapshot(token))


@router.get("/public/review/{token}", response_model=ScopedReviewResponse)
def public_review(
    token: str,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.resolve_review(token))


@router.post("/public/review/{token}/responses", status_code=201)
def respond_to_review(
    token: str,
    payload: ReviewResponseRequest,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
    application: Annotated[SliceTwoApplication, Depends(slice_two_application)],
) -> dict:
    response = guarded(
        lambda: service.respond_to_review(token=token, kind=payload.kind, body=payload.body)
    )
    response_id = UUID(response["id"])
    if payload.kind in {"approve", "reject"}:
        run = application.apply_reviewer_attestation(
            actor_user_id=UUID(response["created_by"]),
            project_id=UUID(response["project_id"]),
            issue_id=response["issue_id"],
            reviewer_name=response["reviewer_name"],
            response_kind=response["response_kind"],
            body=response["body"],
            key=f"review:{response_id}",
        )
        service.link_review_run(response_id=response_id, run_id=run.id)
        return {
            "response_id": response["id"],
            "analysis_run_id": str(run.id),
            "status": run.status,
        }

    # Comments and alternatives remain discussion-only. They are retained but
    # cannot become evidence or change the read without an explicit verdict.
    service.link_review_run(response_id=response_id, run_id=None)
    return {
        "response_id": response["id"],
        "analysis_run_id": None,
        "status": "recorded",
    }


@router.post(
    "/projects/{project_id}/review-responses/{response_id}/evidence",
    status_code=202,
)
def promote_review_response(
    project_id: UUID,
    response_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
    application: Annotated[SliceTwoApplication, Depends(slice_two_application)],
) -> dict:
    response = guarded(
        lambda: service.review_response_for_evidence(
            actor_user_id=context.user.id,
            project_id=project_id,
            response_id=response_id,
        )
    )
    run = application.apply_reviewer_attestation(
        actor_user_id=context.user.id,
        project_id=project_id,
        issue_id=response["issue_id"],
        reviewer_name=response["reviewer_name"],
        response_kind=response["response_kind"],
        body=response["body"],
        key=f"review:{response_id}",
    )
    service.link_review_run(response_id=response_id, run_id=run.id)
    return {
        "response_id": str(response_id),
        "analysis_run_id": str(run.id),
        "status": run.status,
    }

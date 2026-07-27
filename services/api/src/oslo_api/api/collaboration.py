from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine

from oslo_api.api.invitations import InvitationRequestContext, invitation_request_context
from oslo_api.collaboration.pdf import render_snapshot_pdf
from oslo_api.collaboration.service import CollaborationError, DatabaseCollaborationService
from oslo_api.settings import Settings
from oslo_api.slice_two import SliceTwoApplication

router = APIRouter(prefix="/v1", tags=["collaboration"])


def collaboration_service(request: Request) -> DatabaseCollaborationService:
    service = request.app.state.collaboration
    if service is None:
        settings = Settings()
        service = DatabaseCollaborationService(
            create_engine(settings.database_url, pool_pre_ping=True),
            settings.web_url,
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
    issue_id: str | None = Field(default=None, max_length=200)
    reviewer_name: str = Field(min_length=1, max_length=120)
    reviewer_email: EmailStr | None = None


class ReviewResponseRequest(BaseModel):
    kind: Literal["comment", "approve", "reject", "suggest_alternative"]
    body: str = Field(min_length=1, max_length=5_000)


@router.get("/projects/{project_id}/collaboration")
def get_collaboration(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.state(actor_user_id=context.user.id, project_id=project_id))


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
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(
        lambda: service.create_snapshot_link(
            actor_user_id=context.user.id, project_id=project_id
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


@router.get("/projects/{project_id}/exports/pdf")
def export_project(
    project_id: UUID,
    context: Annotated[InvitationRequestContext, Depends(invitation_request_context)],
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> Response:
    snapshot = guarded(
        lambda: service.record_export(actor_user_id=context.user.id, project_id=project_id)
    )
    pdf = render_snapshot_pdf(snapshot["project_name"], snapshot["snapshot_json"])
    return Response(
        pdf,
        media_type="application/pdf",
        headers={
            "content-disposition": f'attachment; filename="{snapshot["project_name"]}-snapshot.pdf"'
        },
    )


@router.get("/public/share/{token}")
def public_snapshot(
    token: str,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.resolve_snapshot(token))


@router.get("/public/review/{token}")
def public_review(
    token: str,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    return guarded(lambda: service.resolve_review(token))


@router.post("/public/review/{token}/responses", status_code=201)
def respond_to_review(
    token: str,
    payload: ReviewResponseRequest,
    request: Request,
    service: Annotated[DatabaseCollaborationService, Depends(collaboration_service)],
) -> dict:
    response = guarded(
        lambda: service.respond_to_review(token=token, kind=payload.kind, body=payload.body)
    )
    application = slice_two_application(request)
    run = application.apply_reviewer_attestation(
        actor_user_id=UUID(response["created_by"]),
        project_id=UUID(response["project_id"]),
        issue_id=response["issue_id"],
        reviewer_name=response["reviewer_name"],
        response_kind=response["response_kind"],
        body=response["body"],
        key=response["id"],
    )
    service.link_review_run(response_id=UUID(response["id"]), run_id=run.id)
    run_status = run.status.value if hasattr(run.status, "value") else str(run.status)
    return {
        "response_id": response["id"],
        "analysis_run_id": str(run.id),
        "status": run_status,
    }

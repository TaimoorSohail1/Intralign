"""Project-command + evidence/artifact-intake router (DTM-0034) — start of the flow.

The WRITE counterpart to the DTM-0018 GET projects read router (which stays
GET-only). Each command wires an EXISTING seam — it invents no persistence and
re-implements no intake/admission:

- ``POST /projects`` → ``project_repo.create`` a ``created`` project, emit
  ``project_created``, return the ``Project`` DTO.
- ``PATCH /projects/{pid}`` → ``project_repo.update`` the metadata, emit
  ``project_updated``.
- ``POST /projects/{pid}:archive`` → ``project_repo.update_lifecycle('archived')``,
  emit ``project_archived`` — **owner/admin only** (Principal.role; 403 otherwise).
- ``POST /projects/{pid}/evidence`` → the EXISTING ``submit_artifact`` intake seam
  (body → Storage; metadata + provenance → the append-only ``artifact`` anchor +
  ``promotion_candidate``), emit ``evidence_added``.
- ``POST /projects/{pid}/artifacts`` → same intake seam, emit ``artifact_created``.
- ``POST /artifacts/{aid}/versions`` → a re-submission of the parent artifact's
  source (the intake seam appends a NEW artifact version — ``version+1`` /
  ``supersedes_id``), emit ``artifact_version_created``.

Epistemic boundary (code/CLAUDE.md hard rules): the command persists the PLATFORM
``project`` row (project_repo) or the intake ``artifact``/``promotion_candidate``
rows (intake seam) ONLY. The canonical ``attested_assertion`` append happens INSIDE
admission (the frozen retain ``admit_candidate`` path) on the DOWNSTREAM promotion /
recompute — this transport touches NO canonical store and appends NO CHR. Evidence
intake does NOT auto-run analysis here (API §5: ``evidence_added`` is a Fast
precondition / Deep trigger, NOT a mandate); the user triggers analysis via the
DTM-0032 command (slices kept separate). ``Idempotency-Key`` returns the same
resource on retry (§10); every path is workspace-scoped (401 unauth / 404
cross-workspace, §3/§12).
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

from backend.api.deps import (
    Principal,
    get_body_store,
    get_event_emitter,
    get_idempotency_store,
    get_intake_store,
    get_project_repo,
    get_projection_reader,
    idempotency_key,
    require_principal,
)
from backend.api.v1.schemas.projects import (
    AddEvidenceRequest,
    CreateArtifactRequest,
    CreateArtifactVersionRequest,
    CreateProjectRequest,
    UpdateProjectRequest,
)
from backend.responsibilities.perceive.intake import IntakeSubmission, submit_artifact
from backend.services.render import ProjectionReader, project_to_dto
from shared.entities import Project

router = APIRouter(tags=["project_commands"])

# Archive requires an elevated role (API Contract §3); members get 403.
_ARCHIVE_ROLES = frozenset({"owner", "admin"})


def _require_project_in_workspace(
    project_id: str, principal: Principal, reader: ProjectionReader
) -> dict[str, Any]:
    """Resolve a project in the caller's workspace, or 404 (existence not leaked)."""
    project = reader.get_project(project_id)
    if project is None or str(project.get("workspace_id")) != principal.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "project not found"}},
        )
    return project


# --- project create / patch / archive ----------------------------------------

@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    body: CreateProjectRequest = Body(default_factory=CreateProjectRequest),
    principal: Principal = Depends(require_principal),
    repo: Any = Depends(get_project_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Project:
    """Create a project → Project(created) + ``project_created`` (workspace-scoped)."""
    route = "projects:create"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return project_to_dto(cached)

    row = repo.create(
        {
            "project_id": str(uuid.uuid4()),
            "workspace_id": principal.workspace_id,  # scoped from the Principal (§3)
            "created_by_user_id": principal.user_id,
            "title": body.title,
            "description": body.description,
            "lifecycle_state": "created",
        }
    )
    emitter.emit(
        "project_created",
        {"project_id": str(row["project_id"]), "workspace_id": principal.workspace_id},
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, row)
    return project_to_dto(row)


@router.patch("/projects/{project_id}", response_model=Project)
def update_project(
    project_id: str,
    body: UpdateProjectRequest = Body(default_factory=UpdateProjectRequest),
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    repo: Any = Depends(get_project_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Project:
    """Patch project metadata → Project + ``project_updated`` (none = no-op patch)."""
    _require_project_in_workspace(project_id, principal, reader)

    route = "projects:update"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return project_to_dto(cached)

    patch = body.model_dump(exclude_none=True)
    row = repo.update(project_id, patch)
    emitter.emit("project_updated", {"project_id": project_id})
    if idem_key is not None:
        idem_store.put(idem_key, route, row)
    return project_to_dto(row)


@router.post("/projects/{project_id}:archive", response_model=Project)
def archive_project(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    repo: Any = Depends(get_project_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Project:
    """Archive a project → Project(archived) + ``project_archived`` (owner/admin only)."""
    _require_project_in_workspace(project_id, principal, reader)

    # RBAC (§3): only owner/admin may archive — checked AFTER the 404 so a member
    # learns nothing about projects outside their workspace.
    if principal.role not in _ARCHIVE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "forbidden",
                    "message": "archiving a project requires the owner or admin role (§3)",
                }
            },
        )

    route = "projects:archive"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return project_to_dto(cached)

    row = repo.update_lifecycle(project_id, "archived")
    emitter.emit("project_archived", {"project_id": project_id})
    if idem_key is not None:
        idem_store.put(idem_key, route, row)
    return project_to_dto(row)


# --- evidence / artifact intake (the EXISTING submit_artifact seam) -----------

def _run_intake(
    *,
    project_id: str,
    source: str,
    content: str,
    submitted_by: str,
    store: Any,
    bodies: Any,
) -> dict[str, Any]:
    """Wire ``submit_artifact`` (intake) and return the persisted artifact row.

    The seam preserves the body to Storage, appends the ``artifact`` anchor +
    ``promotion_candidate``, and is idempotent on ``dedup_key`` — an identical
    re-submission returns the EXISTING artifact (no second persist). The router
    re-implements none of this and writes NO canonical row.
    """
    result = submit_artifact(
        IntakeSubmission(
            project_id=project_id,
            source=source,
            submitted_by=submitted_by,
            content=content,
        ),
        store=store,
        bodies=bodies,
    )
    return dict(result.artifact)


@router.post(
    "/projects/{project_id}/evidence",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def add_evidence(
    project_id: str,
    body: AddEvidenceRequest,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_intake_store),
    bodies: Any = Depends(get_body_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> dict[str, Any]:
    """Add evidence → the intake artifact (evidence anchor) + ``evidence_added``.

    No auto-analysis (API §5): ``evidence_added`` is a Fast precondition / Deep
    trigger; the user runs analysis via the DTM-0032 command.
    """
    _require_project_in_workspace(project_id, principal, reader)

    route = "evidence:add"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return cached

    artifact = _run_intake(
        project_id=project_id,
        source=body.source_type,
        content=body.content_ref,
        submitted_by=principal.user_id,
        store=store,
        bodies=bodies,
    )
    emitter.emit(
        "evidence_added",
        {
            "project_id": project_id,
            "artifact_id": str(artifact["artifact_id"]),
            "source_type": body.source_type,
        },
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, artifact)
    return artifact


@router.post(
    "/projects/{project_id}/artifacts",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def create_artifact(
    project_id: str,
    body: CreateArtifactRequest,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_intake_store),
    bodies: Any = Depends(get_body_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> dict[str, Any]:
    """Create an artifact → the intake artifact + ``artifact_created``."""
    _require_project_in_workspace(project_id, principal, reader)

    route = "artifacts:create"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return cached

    artifact = _run_intake(
        project_id=project_id,
        source=body.artifact_type,
        content=body.content,
        submitted_by=principal.user_id,
        store=store,
        bodies=bodies,
    )
    emitter.emit(
        "artifact_created",
        {
            "project_id": project_id,
            "artifact_id": str(artifact["artifact_id"]),
            "artifact_type": body.artifact_type,
        },
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, artifact)
    return artifact


@router.post(
    "/artifacts/{artifact_id}/versions",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
def create_artifact_version(
    artifact_id: str,
    response: Response,
    body: CreateArtifactVersionRequest = Body(...),
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_intake_store),
    bodies: Any = Depends(get_body_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> dict[str, Any]:
    """Append an artifact version → a NEW intake artifact version + ``artifact_version_created``.

    Resubmits the parent artifact's source with new content; the intake seam
    appends ``version+1`` with ``supersedes_id`` (LDM §5.1 append-only chain).
    """
    parent = store.get_artifact(artifact_id)
    # 404 when the parent is absent OR its project is outside the caller's
    # workspace (existence not leaked, §12).
    if parent is not None:
        self_project = str(parent.get("project_id"))
        self_source = parent.get("provenance", {}).get("source") or parent.get(
            "provenance", {}
        ).get("from_where")
        try:
            _require_project_in_workspace(self_project, principal, reader)
        except HTTPException:
            parent = None
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "artifact not found"}},
        )

    route = "artifacts:version"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return cached

    artifact = _run_intake(
        project_id=self_project,
        source=str(self_source),
        content=body.content,
        submitted_by=principal.user_id,
        store=store,
        bodies=bodies,
    )
    emitter.emit(
        "artifact_version_created",
        {
            "project_id": self_project,
            "artifact_id": str(artifact["artifact_id"]),
            "supersedes_artifact_id": artifact_id,
            "version": artifact.get("version"),
        },
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, artifact)
    return artifact

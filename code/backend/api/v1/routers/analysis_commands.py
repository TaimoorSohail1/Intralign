"""Analysis-command router (DTM-0032) — POST :fast / :deep / :cancel.

The WRITE counterpart to the DTM-0018 GET read router (which stays GET-only).
Each command wires the EXISTING ``submit_trigger`` orchestration seam — it
invents no orchestration and re-implements no run:

- ``POST /projects/{pid}/analysis-runs:fast`` → persist a ``fast_analysis_pass``
  run (``queued``), build a ``TriggerClaim`` + call ``submit_trigger`` with the
  DTM-0030 ``ProjectionMaterializer`` injected, emit ``fast_analysis_requested``,
  return the ``AnalysisRun`` DTO.
- ``POST /projects/{pid}/analysis-runs:deep`` (``{trigger_source}``) → same, a
  ``deep_analysis_pass`` run, emit ``deep_analysis_requested``.
- ``POST /analysis-runs/{rid}:cancel`` → transition a ``queued``/``running`` run
  to ``cancelled`` via the repo, emit ``analysis_cancelled``.

Epistemic boundary (code/CLAUDE.md hard rules): the command persists the PLATFORM
``analysis_run`` row ONLY. The canonical CHR append happens INSIDE the durable run
(the frozen retain path), never from the transport — this module touches no CHR
repo and no canonical store. ``Idempotency-Key`` returns the same run on retry
(§10); every path is workspace-scoped (401 unauth / 404 cross-workspace / 409
illegal transition, §9).
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

from backend.api.deps import (
    Principal,
    get_analysis_run_repo,
    get_event_emitter,
    get_idempotency_store,
    get_materializer,
    get_projection_reader,
    get_trigger_submitter,
    idempotency_key,
    require_principal,
)
from backend.api.v1.schemas.analysis import DeepAnalysisRequest
from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.services.render import ProjectionReader, analysis_run_to_dto
from shared.entities import AnalysisRun

router = APIRouter(tags=["analysis_commands"])

# R1 registers one durable graph; both passes run through it (the run_type on the
# persisted row distinguishes fast vs deep for the read surface).
_GRAPH_NAME = "deep_pass"


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


def _start_analysis(
    *,
    project_id: str,
    run_type: str,
    trigger_source: str,
    event_name: str,
    principal: Principal,
    reader: ProjectionReader,
    repo: Any,
    submit_trigger: Any,
    materializer: Any,
    emitter: Any,
    idem_key: str | None,
    idem_store: Any,
    route: str,
) -> AnalysisRun:
    """Persist a queued run, fire submit_trigger (materializer injected), emit."""
    _require_project_in_workspace(project_id, principal, reader)

    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return analysis_run_to_dto(cached)

    run_id = str(uuid.uuid4())
    row = repo.create(
        {
            "analysis_run_id": run_id,
            "project_id": project_id,
            "run_type": run_type,
            "run_status": "queued",
        }
    )

    claim = TriggerClaim(
        trigger_type=TriggerType.REANALYSIS,
        project_id=project_id,
        information_changed=True,  # an analysis request IS an assessment-changing event (A4.6)
        source=trigger_source,
    )
    # Wire the EXISTING seam — materializer injected so derived.*_current fills.
    submit_trigger(_GRAPH_NAME, claim, materializer=materializer)

    emitter.emit(
        event_name,
        {
            "project_id": project_id,
            "analysis_run_id": run_id,
            "run_type": run_type,
            "trigger_source": trigger_source,
        },
    )

    if idem_key is not None:
        idem_store.put(idem_key, route, row)
    return analysis_run_to_dto(row)


@router.post(
    "/projects/{project_id}/analysis-runs:fast",
    response_model=AnalysisRun,
    status_code=status.HTTP_201_CREATED,
)
def start_fast_analysis(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    repo: Any = Depends(get_analysis_run_repo),
    submit_trigger: Any = Depends(get_trigger_submitter),
    materializer: Any = Depends(get_materializer),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> AnalysisRun:
    """Start a Fast Analysis pass → AnalysisRun(queued) + ``fast_analysis_requested``."""
    return _start_analysis(
        project_id=project_id,
        run_type="fast_analysis_pass",
        trigger_source="fast_analysis",
        event_name="fast_analysis_requested",
        principal=principal,
        reader=reader,
        repo=repo,
        submit_trigger=submit_trigger,
        materializer=materializer,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="analysis-runs:fast",
    )


@router.post(
    "/projects/{project_id}/analysis-runs:deep",
    response_model=AnalysisRun,
    status_code=status.HTTP_201_CREATED,
)
def start_deep_analysis(
    project_id: str,
    body: DeepAnalysisRequest = Body(default_factory=DeepAnalysisRequest),
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    repo: Any = Depends(get_analysis_run_repo),
    submit_trigger: Any = Depends(get_trigger_submitter),
    materializer: Any = Depends(get_materializer),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> AnalysisRun:
    """Start a Deep Analysis pass → AnalysisRun(queued) + ``deep_analysis_requested``."""
    return _start_analysis(
        project_id=project_id,
        run_type="deep_analysis_pass",
        trigger_source=body.trigger_source,
        event_name="deep_analysis_requested",
        principal=principal,
        reader=reader,
        repo=repo,
        submit_trigger=submit_trigger,
        materializer=materializer,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="analysis-runs:deep",
    )


_CANCELLABLE = frozenset({"queued", "running"})


@router.post("/analysis-runs/{analysis_run_id}:cancel", response_model=AnalysisRun)
def cancel_analysis(
    analysis_run_id: str,
    response: Response,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    repo: Any = Depends(get_analysis_run_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> AnalysisRun:
    """Cancel a queued/running run → AnalysisRun(cancelled) + ``analysis_cancelled``."""
    route = "analysis-runs:cancel"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return analysis_run_to_dto(cached)

    run = repo.get(analysis_run_id)
    # 404 when absent OR the parent project is outside the caller's workspace
    # (existence not leaked, §12).
    if run is not None:
        _require_project_in_workspace(str(run.get("project_id")), principal, reader)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "analysis run not found"}},
        )

    if run.get("run_status") not in _CANCELLABLE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "illegal_transition",
                    "message": (
                        f"run {analysis_run_id} is {run.get('run_status')!r} — only a "
                        "queued/running run can be cancelled (§9)"
                    ),
                }
            },
        )

    updated = repo.update_status(analysis_run_id, "cancelled")
    emitter.emit(
        "analysis_cancelled",
        {
            "project_id": str(run.get("project_id")),
            "analysis_run_id": analysis_run_id,
        },
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, updated)
    return analysis_run_to_dto(updated)

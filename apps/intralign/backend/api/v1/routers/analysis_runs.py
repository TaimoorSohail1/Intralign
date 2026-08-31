"""Analysis-runs read router (DTM-0018) — GET list/detail (read-mostly; ADR-0003).

Presents AnalysisRun rows as Data Model v1.2 ``AnalysisRun`` DTOs. ``GET
/analysis-runs/{rid}`` is the async-job poll target (§11). Consumed by the
Analysis Progress + Deep Analysis Results surfaces (UI_SCREEN_INVENTORY). GET
ONLY — start/cancel stay on the existing command seam; the read surface starts
no analysis.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import Principal, get_projection_reader, require_principal
from backend.services.render import ProjectionReader, analysis_run_to_dto
from shared.entities import AnalysisRun

router = APIRouter(tags=["analysis_runs"])


@router.get("/projects/{project_id}/analysis-runs", response_model=list[AnalysisRun])
def list_analysis_runs(
    project_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> list[AnalysisRun]:
    """List the project's analysis runs, newest first."""
    return [analysis_run_to_dto(row) for row in reader.list_analysis_runs(project_id)]


@router.get("/analysis-runs/{analysis_run_id}", response_model=AnalysisRun)
def get_analysis_run(
    analysis_run_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
) -> AnalysisRun:
    """Get one analysis run (the async-job poll target, §11)."""
    row = reader.get_analysis_run(analysis_run_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "analysis run not found"}},
        )
    return analysis_run_to_dto(row)

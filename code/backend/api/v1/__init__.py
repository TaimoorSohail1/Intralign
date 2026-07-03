"""Release 1 API surface (/v1).

Aggregates every resource router under the canonical /v1 prefix (API Contract
Spec §15). Resources = Data Model v1.2 entities; commands use the :verb
convention; analysis is async (returns AnalysisRun queued, client polls).
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1")

# Resource routers are included here as their contracts are approved, e.g.:
#   from backend.api.v1.routers import projects
#   router.include_router(projects.router)
# Catalog: projects, artifacts, evidence, analysis_runs, findings,
#          recommendations, reports, comments, shares, notifications.

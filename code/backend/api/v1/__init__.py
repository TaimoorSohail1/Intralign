"""Release 1 API surface (/v1).

Aggregates every resource router under the canonical /v1 prefix (API Contract
Spec §15). Resources = Data Model v1.2 entities; the Disclose read surface
(DTM-0018, IC-WE-DISCLOSE) exposes READ-MOSTLY GET endpoints that present the
governed objects Waves A–U produced, mapped by ``services.render`` into Data
Model v1.2 DTOs (exposed verbatim per ADR-0003). Commands (create/accept/start)
stay on their existing seams — the read surface mutates nothing.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1.routers import (
    acceptance,
    analysis_runs,
    confidence,
    findings,
    notifications,
    projects,
    recommendations,
)

router = APIRouter(prefix="/v1")

# DTM-0018 — the Disclose read routers (GET list/detail per governed object).
router.include_router(projects.router)
router.include_router(analysis_runs.router)
router.include_router(findings.router)
router.include_router(recommendations.router)
router.include_router(confidence.router)
router.include_router(acceptance.router)
router.include_router(notifications.router)

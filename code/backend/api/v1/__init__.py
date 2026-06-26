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
    acceptance_commands,
    analysis_commands,
    analysis_runs,
    confidence,
    findings,
    notifications,
    project_commands,
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

# DTM-0032 — the analysis command router (POST :fast/:deep/:cancel). Additive
# and separate from the GET read surface (decision #3/#4); it wires the existing
# submit_trigger seam and never mutates a canonical store.
router.include_router(analysis_commands.router)

# DTM-0033 — the acceptance command router (POST recommendations
# :accept/:reject/:defer/:implement). Additive and separate from the GET
# recommendations read router; it wires the existing ``record_acceptance`` retain
# seam (UAR always; plan fact on accept only) and never marks the rec world-true.
router.include_router(acceptance_commands.router)

# DTM-0034 — the project-command + evidence/artifact-intake router (POST /projects,
# PATCH /projects/{pid}, POST /projects/{pid}:archive, POST .../evidence,
# POST .../artifacts, POST /artifacts/{aid}/versions). Additive and separate from
# the GET projects read router; project writes wire the DTM-0031 project_repo and
# evidence/artifacts wire the existing ``submit_artifact`` intake seam — the
# transport writes NO canonical store (admission appends the attested assertion
# downstream). Archive is owner/admin only (§3).
router.include_router(project_commands.router)

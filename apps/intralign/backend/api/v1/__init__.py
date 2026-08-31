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
    chat,
    confidence,
    finding_commands,
    findings,
    history,
    issues,
    notification_commands,
    notifications,
    overview,
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

# DTM-0038 — the read-shape additions that close the Wave E read-surface flags
# with first-class reads (all GET-only, workspace-scoped, labels preserved):
#  - issues: the first-class Issue (Derived ``issue_current``) + its source-Finding
#    lineage (mirrors the findings reader);
#  - overview: counts of the governed lists + the Derived Outcome-Confidence/CAF
#    aggregates (a PRESENTATION of governed objects — NEVER a health/probability
#    score; the Wave E not-project-health rule);
#  - history: the append-only Cognition-History trail (the "what OSLO said when",
#    CHR-only, Derived-labelled, append-order). The append-only write path stays
#    the Retain-owned ChrRepository — these reads mutate nothing.
router.include_router(issues.router)
router.include_router(overview.router)
router.include_router(history.router)

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

# DTM-0035 — the finding-lifecycle command router (POST findings
# :acknowledge/:address/:reopen) + the notification-state command router (POST
# notifications :view/:dismiss). Additive and separate from the GET findings/
# notifications read routers. Finding lifecycle updates the DERIVED projection
# status (State Model §10 — a status attribute, NOT a UAR) via the projection
# store; notification state transitions the PLATFORM (non-canonical) awareness
# state via the DTM-0031 notification_repo. Neither writes a canonical store,
# appends a CHR, or changes any assessment.
router.include_router(finding_commands.router)
router.include_router(notification_commands.router)

# DTM-0037 — the OSLO Chat router (POST /projects/{pid}/chat). Additive and
# separate from the read surface. A Disclose-class interaction surface (DL-047
# CHAT-01…04): Explain/Clarify/Resolve CONSUME existing cognition (read + an
# LLM-phrased response via the fixture-backed seam); Improve TRIGGERS cognition
# (the existing submit_trigger seam, materializer injected). It returns a
# NON-CANONICAL ChatExchange and emits the non-canonical ``chat_exchange`` event.
# CRITICAL: the chat writes NO canonical (no AttestedAssertion/CHR/UAR), mutates
# NO artifact, and changes NO assessment — it only consumes + triggers.
router.include_router(chat.router)

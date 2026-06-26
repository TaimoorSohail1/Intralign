"""Notification-state command router (DTM-0035) — POST :view / :dismiss.

The WRITE counterpart to the DTM-0018 GET notifications read router (which stays
GET-only). Each command transitions the PLATFORM awareness state via the DTM-0031
``notification_repo`` (``mark_viewed`` / ``mark_dismissed``) and emits the Event-Model
§12 event (``notification_viewed`` / ``notification_dismissed``).

Epistemic class — PLATFORM / NON-CANONICAL (code/CLAUDE.md hard rule #2; State Model
§12 clarification; negative-proven): a notification is commodity awareness state. It
NEVER drives analysis, changes NO assessment, alters NO Finding/Recommendation, writes
NO Derived projection, and appends NO Cognition History Record. The ``notification``
table is the only surface this command touches (mark_viewed/mark_dismissed are legitimate
awareness-state UPDATEs); the referenced object is untouched.

``Idempotency-Key`` returns the SAME Notification DTO on retry (no second mark, §10);
every path is workspace-scoped via ``current_principal`` (401 unauth / 404 cross-
workspace, §9/§12 — existence not leaked).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import (
    Principal,
    get_event_emitter,
    get_idempotency_store,
    get_notification_repo,
    idempotency_key,
    require_principal,
)
from backend.services.render import notification_to_dto
from shared.entities import Notification

router = APIRouter(tags=["notification_commands"])


def _resolve_notification(
    notification_id: str, principal: Principal, repo: Any
) -> dict[str, Any]:
    """Resolve a notification in the caller's workspace, or 404 (§12).

    Existence is NOT leaked: a missing notification, or one in another workspace,
    is an indistinguishable 404.
    """
    row = repo.get(notification_id)
    if row is None or str(row.get("workspace_id")) != principal.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "notification not found"}},
        )
    return row


@router.post("/notifications/{notification_id}:view", response_model=Notification)
def view_notification(
    notification_id: str,
    principal: Principal = Depends(require_principal),
    repo: Any = Depends(get_notification_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Notification:
    """View → created→viewed (platform awareness state) + ``notification_viewed``."""
    route = "notifications:view"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return notification_to_dto(cached)

    _resolve_notification(notification_id, principal, repo)
    stored = repo.mark_viewed(notification_id, datetime.now(UTC).isoformat())
    emitter.emit(
        "notification_viewed",
        {"notification_id": notification_id, "user_id": principal.user_id},
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, stored)
    return notification_to_dto(stored)


@router.post("/notifications/{notification_id}:dismiss", response_model=Notification)
def dismiss_notification(
    notification_id: str,
    principal: Principal = Depends(require_principal),
    repo: Any = Depends(get_notification_repo),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Notification:
    """Dismiss → dismissed (platform awareness state) + ``notification_dismissed``."""
    route = "notifications:dismiss"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return notification_to_dto(cached)

    _resolve_notification(notification_id, principal, repo)
    stored = repo.mark_dismissed(notification_id, datetime.now(UTC).isoformat())
    emitter.emit(
        "notification_dismissed",
        {"notification_id": notification_id, "user_id": principal.user_id},
    )
    if idem_key is not None:
        idem_store.put(idem_key, route, stored)
    return notification_to_dto(stored)

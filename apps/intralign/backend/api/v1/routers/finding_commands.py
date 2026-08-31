"""Finding-lifecycle command router (DTM-0035) — POST :acknowledge / :address / :reopen.

The WRITE counterpart to the DTM-0018 GET findings read router (which stays GET-only).
Each command advances the finding's WORKFLOW STATUS — and nothing else.

Status ownership (grounded, not invented): per the **State Model §10** the finding
lifecycle (Detected→Acknowledged→Addressed→Closed→Reopened) is a ``Finding.status``
ATTRIBUTE (Data Model §11), NOT a user-attested record. In the R1 runtime model the
Finding lives as a **Derived** live-projection (``derived.finding_current``; LDM §3.1),
so its status is a field in the projection's ``current_payload``. This command therefore:

- reads the finding projection via the SELECT-only read seam (workspace-scoped; 404),
- validates the §10 transition (e.g. :acknowledge requires ``detected``; an invalid
  transition is a 409 ``conflict`` per API Contract §5/§9 — never a silent mutation),
- advances ``current_payload.status`` and UPSERTs the row back through the DTM-0030
  projection store (``upsert_projection`` — the Derived layer is mutable/recomputable),
- emits the Event-Model §10 event verbatim. Per API Contract §5 + the endpoint catalog,
  :acknowledge and :address both carry ``finding_updated`` (the resulting status rides
  the payload — the granular ``finding_acknowledged``/``finding_addressed`` are status
  FACETS of this canonical event, NOT new event types), and :reopen carries
  ``finding_reopened``.

Epistemic boundary (code/CLAUDE.md hard rules #2/#3/#5; negative-proven): this is a
Derived-projection status update ONLY. It writes NO canonical row, appends NO Cognition
History Record, and is NOT an acceptance (no UserAcceptanceRecord) — the finding's
content/confidence/CHR lineage are unchanged (no cognition change, no recompute). The
projection store has no canonical surface by construction (hard rule #2).

``Idempotency-Key`` returns the SAME Finding DTO on retry (no second upsert, §10); every
path is workspace-scoped via ``current_principal`` (401 unauth / 404 cross-workspace, §12).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import (
    Principal,
    get_event_emitter,
    get_idempotency_store,
    get_projection_reader,
    get_projection_store,
    idempotency_key,
    require_principal,
)
from backend.services.render import ProjectionReader, finding_to_dto
from shared.entities import Finding

router = APIRouter(tags=["finding_commands"])

# The §10 transition table THIS command surface owns (the user workflow actions).
# Each entry: action → (required current status, resulting status, EM §10 event).
# ``finding_created``/``finding_closed``/``finding_superseded`` are engine/`:close`
# emissions (API §5 note) and are NOT in this command surface.
_TRANSITIONS: dict[str, tuple[str, str, str]] = {
    # acknowledge/address advance via finding_updated (status rides the payload).
    "acknowledge": ("detected", "acknowledged", "finding_updated"),
    "address": ("acknowledged", "addressed", "finding_updated"),
    # reopen returns a Closed finding to active via finding_reopened.
    "reopen": ("closed", "reopened", "finding_reopened"),
}


def _resolve_finding(
    finding_id: str, principal: Principal, reader: ProjectionReader
) -> dict[str, Any]:
    """Resolve a finding projection in the caller's workspace, or 404 (§12).

    Existence is NOT leaked: a missing projection, or one whose project is outside
    the caller's workspace, is an indistinguishable 404.
    """
    row = reader.get_projection("finding", finding_id)
    if row is not None:
        project = reader.get_project(str(row.get("project_id")))
        if project is None or str(project.get("workspace_id")) != principal.workspace_id:
            row = None
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "finding not found"}},
        )
    return row


def _transition(
    *,
    finding_id: str,
    action: str,
    principal: Principal,
    reader: ProjectionReader,
    store: Any,
    emitter: Any,
    idem_key: str | None,
    idem_store: Any,
) -> Finding:
    """Validate + apply the §10 status transition on the Derived projection."""
    route = f"findings:{action}"
    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return finding_to_dto(cached)

    row = _resolve_finding(finding_id, principal, reader)
    required, resulting, event_name = _TRANSITIONS[action]

    payload = dict(row.get("current_payload") or {})
    current = str(payload.get("status") or "detected")
    if current != required:
        # API §5/§9 — an invalid lifecycle transition is a 409 conflict; nothing is
        # mutated (no silent advance, no partial write).
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "conflict",
                    "message": (
                        f"finding {finding_id} is not in '{required}'; "
                        f"cannot {action}."
                    ),
                    "details": [{"current_status": current}],
                }
            },
        )

    # Advance the STATUS attribute ONLY — the cognition snapshot (summary, type,
    # evidence) and the envelope (CHR lineage, confidence) are preserved verbatim.
    # This is a Derived-projection update, never a canonical write / CHR append.
    payload["status"] = resulting
    updated = dict(row)
    updated["current_payload"] = payload
    stored = store.upsert_projection("finding", updated)

    emitter.emit(
        event_name,
        {
            "finding_id": finding_id,
            "project_id": str(row.get("project_id")),
            "status": resulting,
            "user_id": principal.user_id,
        },
    )

    if idem_key is not None:
        idem_store.put(idem_key, route, stored)
    return finding_to_dto(stored)


@router.post("/findings/{finding_id}:acknowledge", response_model=Finding)
def acknowledge_finding(
    finding_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_projection_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Finding:
    """Acknowledge → detected→acknowledged (Derived status) + ``finding_updated``."""
    return _transition(
        finding_id=finding_id, action="acknowledge", principal=principal,
        reader=reader, store=store, emitter=emitter,
        idem_key=idem_key, idem_store=idem_store,
    )


@router.post("/findings/{finding_id}:address", response_model=Finding)
def address_finding(
    finding_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_projection_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Finding:
    """Address → acknowledged→addressed (Derived status) + ``finding_updated``."""
    return _transition(
        finding_id=finding_id, action="address", principal=principal,
        reader=reader, store=store, emitter=emitter,
        idem_key=idem_key, idem_store=idem_store,
    )


@router.post("/findings/{finding_id}:reopen", response_model=Finding)
def reopen_finding(
    finding_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_projection_store),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Finding:
    """Reopen → closed→reopened (Derived status) + ``finding_reopened``."""
    return _transition(
        finding_id=finding_id, action="reopen", principal=principal,
        reader=reader, store=store, emitter=emitter,
        idem_key=idem_key, idem_store=idem_store,
    )

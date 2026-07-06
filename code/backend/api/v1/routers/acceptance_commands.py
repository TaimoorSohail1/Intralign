"""Acceptance-command router (DTM-0033) — POST :accept / :reject / :defer / :implement.

The WRITE counterpart to the DTM-0018 GET recommendations read router (which stays
GET-only). Each command persists the Recommendation Panel's accept/reject/defer/
implement affordance (DTM-0022) by wiring the EXISTING ``record_acceptance`` retain
seam — it invents NO acceptance logic and re-implements no UAR/plan-fact write:

- resolve the recommendation's CURRENT CHR (its projection ``current_chr_ref``) as
  the MANDATORY ``version_pin`` (no UAR without it — the existing
  ``AcceptanceRecordingError`` path),
- build the acceptance capture (action + ``target_kind="recommendation"`` + the
  authenticated user as actor + version_pin),
- call ``record_acceptance`` — which writes the UAR ALWAYS, and the plan fact on
  ``accept`` ONLY (``reject``/``defer``/``implement`` write the UAR alone),
- emit the Event-Model §8 event verbatim
  (``recommendation_accepted/rejected/deferred/implemented``),
- return the affected ``Recommendation`` DTO (state per DL-055).

``:implement`` ALSO triggers a Deep recompute via the EXISTING ``submit_trigger``
seam (materializer injected, like DTM-0032) — the implementation is new evidence
⇒ recompute (DL-055).

Epistemic boundary (code/CLAUDE.md hard rule #5 — OSLO NEVER self-accepts): the
actor is ALWAYS ``Principal.user_id`` — there is no server-initiated/auto accept,
and the command marks the recommendation NOTHING true/world-truth (the UAR records
a human decision, nothing more). ``Idempotency-Key`` returns the SAME UAR on retry
(§10); every path is workspace-scoped (401 unauth / 404 cross-workspace, §9/§12).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.deps import (
    Principal,
    get_acceptance_chr_reader,
    get_event_emitter,
    get_idempotency_store,
    get_materializer,
    get_projection_reader,
    get_retention_store,
    get_trigger_submitter,
    idempotency_key,
    require_principal,
)
from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.responsibilities.perceive.acceptance_capture import AcceptanceCapture
from backend.responsibilities.retain.acceptance import (
    AcceptanceRecordingError,
    record_acceptance,
)
from backend.services.render import ProjectionReader, recommendation_to_dto
from shared.entities import Recommendation, RecommendationStatus

router = APIRouter(tags=["acceptance_commands"])

# The valid AcceptanceCapture actions (the Perceive handoff vocabulary). ``implement``
# is a DL-055 user action recorded as a UAR but is NOT a capture action (and writes
# no plan fact) — it is passed to ``record_acceptance`` as a Mapping (the seam accepts
# either an AcceptanceCapture or a Mapping).
_CAPTURE_ACTIONS = frozenset({"accept", "reject", "defer"})

# The durable graph the :implement recompute runs through (mirrors DTM-0032).
_GRAPH_NAME = "deep_pass"


def _resolve_recommendation(
    recommendation_id: str, principal: Principal, reader: ProjectionReader
) -> dict[str, Any]:
    """Resolve a recommendation projection in the caller's workspace, or 404.

    Existence is NOT leaked (§12): a missing projection, or one whose project is
    outside the caller's workspace, is an indistinguishable 404.
    """
    row = reader.get_projection("recommendation", recommendation_id)
    if row is not None:
        project = reader.get_project(str(row.get("project_id")))
        if project is None or str(project.get("workspace_id")) != principal.workspace_id:
            row = None
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "recommendation not found"}},
        )
    return row


def _record(
    *,
    recommendation_id: str,
    action: str,
    dto_status: str,
    event_name: str,
    recompute: bool,
    principal: Principal,
    reader: ProjectionReader,
    store: Any,
    chr_reader: Any,
    submit_trigger: Any,
    materializer: Any,
    emitter: Any,
    idem_key: str | None,
    idem_store: Any,
    route: str,
) -> Recommendation:
    """Resolve the pin, wire ``record_acceptance``, emit, (optionally) recompute."""
    row = _resolve_recommendation(recommendation_id, principal, reader)

    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return _to_dto(cached, dto_status)

    project_id = str(row["project_id"])
    # The MANDATORY version_pin is the recommendation's CURRENT CHR (LDM §3.1
    # ``current_chr_ref``). A recommendation with no current CHR has no version to
    # pin — record_acceptance rejects it (no unpinned UAR ever exists).
    version_pin = row.get("current_chr_ref")

    fields: dict[str, Any] = {
        "user_id": principal.user_id,  # the actor is the user — OSLO never self-accepts
        "target_kind": "recommendation",
        "version_pin": version_pin,
        "action": action,
        "project_id": project_id,
        "captured_at": datetime.now(UTC),
    }
    # accept/reject/defer are valid AcceptanceCapture actions; ``implement`` is a
    # DL-055 user action recorded as a UAR via the Mapping form (no plan fact).
    capture: AcceptanceCapture | dict[str, Any]
    if action in _CAPTURE_ACTIONS and version_pin is not None:
        capture = AcceptanceCapture(**fields)
    else:
        capture = fields

    try:
        record_acceptance(
            capture,
            project_id=project_id,
            store=store,
            emitter=emitter,
            chr_reader=chr_reader,
        )
    except AcceptanceRecordingError as exc:
        # The mandatory-pin (and related) guard — no unpinned/incomplete UAR is
        # ever written. Surfaced as 422 (the recommendation carries no version to
        # pin), never a silent partial write.
        raise HTTPException(
            status_code=422,  # Unprocessable — the recommendation carries no version to pin
            detail={"error": {"code": "version_pin_required", "message": str(exc)}},
        ) from exc

    # DL-055: implementing a recommendation is new evidence → a Deep recompute,
    # via the EXISTING submit_trigger seam (materializer injected, like DTM-0032).
    if recompute:
        claim = TriggerClaim(
            trigger_type=TriggerType.REANALYSIS,
            project_id=project_id,
            information_changed=True,  # an implementation IS new evidence (A4.6)
            source="recommendation_implemented",
        )
        submit_trigger(_GRAPH_NAME, claim, materializer=materializer)

    emitter.emit(
        event_name,
        {
            "recommendation_id": recommendation_id,
            "project_id": project_id,
            "version_pin": str(version_pin),
            "user_id": principal.user_id,
        },
    )

    if idem_key is not None:
        idem_store.put(idem_key, route, row)
    return _to_dto(row, dto_status)


def _to_dto(row: dict[str, Any], dto_status: str) -> Recommendation:
    """Present the affected Recommendation DTO with the user-action state (DL-055).

    The DTO reflects the action JUST recorded (the UAR is the source of truth for
    the user-action lifecycle); the underlying Derived projection is NOT mutated
    (the recommendation stays recomputable — OSLO never promotes it).
    """
    dto = recommendation_to_dto(row)
    return dto.model_copy(update={"status": RecommendationStatus(dto_status)})


@router.post("/recommendations/{recommendation_id}:accept", response_model=Recommendation)
def accept_recommendation(
    recommendation_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_retention_store),
    chr_reader: Any = Depends(get_acceptance_chr_reader),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Recommendation:
    """Accept → UAR + plan fact (version-pinned, user-attested) + ``recommendation_accepted``."""
    return _record(
        recommendation_id=recommendation_id,
        action="accept",
        dto_status="accepted",
        event_name="recommendation_accepted",
        recompute=False,
        principal=principal,
        reader=reader,
        store=store,
        chr_reader=chr_reader,
        submit_trigger=None,
        materializer=None,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="recommendations:accept",
    )


@router.post("/recommendations/{recommendation_id}:reject", response_model=Recommendation)
def reject_recommendation(
    recommendation_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_retention_store),
    chr_reader: Any = Depends(get_acceptance_chr_reader),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Recommendation:
    """Reject → UAR only (NO plan fact) + ``recommendation_rejected``."""
    return _record(
        recommendation_id=recommendation_id,
        action="reject",
        dto_status="rejected",
        event_name="recommendation_rejected",
        recompute=False,
        principal=principal,
        reader=reader,
        store=store,
        chr_reader=chr_reader,
        submit_trigger=None,
        materializer=None,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="recommendations:reject",
    )


@router.post("/recommendations/{recommendation_id}:defer", response_model=Recommendation)
def defer_recommendation(
    recommendation_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_retention_store),
    chr_reader: Any = Depends(get_acceptance_chr_reader),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Recommendation:
    """Defer → UAR only (NO plan fact) + ``recommendation_deferred``."""
    return _record(
        recommendation_id=recommendation_id,
        action="defer",
        dto_status="deferred",
        event_name="recommendation_deferred",
        recompute=False,
        principal=principal,
        reader=reader,
        store=store,
        chr_reader=chr_reader,
        submit_trigger=None,
        materializer=None,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="recommendations:defer",
    )


@router.post("/recommendations/{recommendation_id}:implement", response_model=Recommendation)
def implement_recommendation(
    recommendation_id: str,
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    store: Any = Depends(get_retention_store),
    chr_reader: Any = Depends(get_acceptance_chr_reader),
    submit_trigger: Any = Depends(get_trigger_submitter),
    materializer: Any = Depends(get_materializer),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> Recommendation:
    """Implement → UAR + (DL-055) a Deep recompute + ``recommendation_implemented``."""
    return _record(
        recommendation_id=recommendation_id,
        action="implement",
        dto_status="implemented",
        event_name="recommendation_implemented",
        recompute=True,
        principal=principal,
        reader=reader,
        store=store,
        chr_reader=chr_reader,
        submit_trigger=submit_trigger,
        materializer=materializer,
        emitter=emitter,
        idem_key=idem_key,
        idem_store=idem_store,
        route="recommendations:implement",
    )

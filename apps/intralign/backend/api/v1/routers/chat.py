"""OSLO Chat router (DTM-0037; DL-047 CHAT-01…04) — POST /projects/{pid}/chat.

The interaction surface backend (frontend DTM-0029). It is additive and separate
from the GET read surface. One endpoint:

- ``POST /projects/{pid}/chat`` ``{message, context?, intent?}`` →
  a NON-CANONICAL ``ChatExchange`` (interaction record). Intent
  **Explain/Clarify/Resolve** CONSUMES existing cognition (the router READS the
  governed projections via the SELECT-only read seam and the responder phrases a
  response over them via the fixture-backed LLM seam); intent **Improve**
  TRIGGERS cognition (the responder calls the EXISTING ``submit_trigger`` seam,
  materializer injected — the frozen recompute owns its CHR append). Emits the
  non-canonical ``chat_exchange`` event.

Epistemic boundary (DL-047 Critical; code/CLAUDE.md hard rules): the chat writes
NO canonical receipt (no attested-assertion / history-record / acceptance-record),
mutates NO artifact, and changes NO assessment. This router depends ONLY on the
read seam (consume) + the chat responder (which holds the LLM seam +
``submit_trigger`` + the materializer) — NO write-store / retention / intake /
history collaborator is wired in. The ``ChatExchange`` is returned to the
frontend (ephemeral — NO migration in this slice; a durable chat-session/
chat-exchange table is a flagged follow-up).

``Idempotency-Key`` returns the SAME exchange on retry (no second trigger, §10);
every path is workspace-scoped (401 unauth / 404 cross-workspace, §9/§12).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status

from backend.api.deps import (
    Principal,
    get_chat_responder,
    get_event_emitter,
    get_idempotency_store,
    get_projection_reader,
    idempotency_key,
    require_principal,
)
from backend.api.v1.schemas.chat import ChatRequest
from backend.services.render import ProjectionReader
from shared.epistemic import ChatExchange

router = APIRouter(tags=["chat"])

# The governed output kinds the chat CONSUMES for context (read-only). These are
# the derived live-projection kinds the read seam exposes — the chat reads them
# to phrase an Explain/Clarify/Resolve; it never writes them.
_CONSUMED_KINDS = (
    "finding",
    "recommendation",
    "confidence",
    "caf",
    "outcome_confidence",
)


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


def _read_governed(
    project_id: str, reader: ProjectionReader
) -> dict[str, list[dict[str, Any]]]:
    """CONSUME the governed projections for the project (SELECT-only, read-mostly).

    A read of each consumed output kind through the SELECT-only seam — no write,
    no mutation. Returns a read-only snapshot the responder phrases over.
    """
    return {kind: reader.list_projection(project_id, kind) for kind in _CONSUMED_KINDS}


@router.post(
    "/projects/{project_id}/chat",
    response_model=ChatExchange,
    status_code=status.HTTP_201_CREATED,
)
def chat(
    project_id: str,
    body: ChatRequest = Body(...),
    principal: Principal = Depends(require_principal),
    reader: ProjectionReader = Depends(get_projection_reader),
    responder: Any = Depends(get_chat_responder),
    emitter: Any = Depends(get_event_emitter),
    idem_key: str | None = Depends(idempotency_key),
    idem_store: Any = Depends(get_idempotency_store),
) -> ChatExchange:
    """Chat over a project → a NON-CANONICAL ChatExchange + ``chat_exchange``.

    Explain/Clarify/Resolve CONSUME (read + phrase); Improve TRIGGERS the frozen
    Deep-Pass recompute (the responder calls ``submit_trigger``). No canonical
    write, no artifact mutation, no assessment change happens on this path.
    """
    route = "chat"
    _require_project_in_workspace(project_id, principal, reader)

    if idem_key is not None:
        cached = idem_store.get(idem_key, route)
        if cached is not None:
            return ChatExchange.model_validate(cached)

    # CONSUME the governed cognition (read-only) so the responder can phrase over
    # it (Explain/Clarify/Resolve). Improve also reads it for context but its
    # effect is to TRIGGER a recompute, not to read it.
    governed = _read_governed(project_id, reader)

    exchange = responder.respond(
        project_id=project_id,
        message=body.message,
        intent=body.intent,
        governed=governed,
        context=body.context,
    )

    emitter.emit(
        "chat_exchange",
        {
            "project_id": project_id,
            "exchange_id": exchange.exchange_id,
            "intent": exchange.intent,
            "triggered_run": exchange.triggered_run,
        },
    )

    if idem_key is not None:
        idem_store.put(idem_key, route, exchange.model_dump(mode="json"))
    return exchange

"""OSLO Chat request body (DTM-0037; DL-047 CHAT-01…04; API Contract §"Chat").

Only the INPUT shape lives here. The response is the NON-CANONICAL
``ChatExchange`` interaction record (``shared.epistemic``) returned verbatim —
it is neither Attested nor Derived cognition, so it is NOT a Data Model entity
(``shared.entities``); it is an interaction record, like a notification.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from shared.epistemic import ChatContext, ChatIntent


class ChatRequest(BaseModel):
    """``POST /projects/{pid}/chat`` body — ``{message, context?, intent?}``.

    - ``message`` — the user's message (required).
    - ``intent`` — Explain/Clarify/Resolve (CONSUME existing cognition) or Improve
      (TRIGGER a Deep Pass). Defaults to ``explain`` (the read-only default — the
      safest intent, it triggers nothing).
    - ``context`` — the launching object (issue/recommendation/artifact/finding/
      CRR) whose context the exchange inherits (CHAT-01); optional.
    """

    message: str = Field(..., min_length=1, description="The user's chat message.")
    intent: ChatIntent = Field(
        default="explain",
        description="Explain/Clarify/Resolve (consume) | Improve (trigger).",
    )
    context: ChatContext | None = Field(
        default=None, description="The launching object's context to inherit (CHAT-01)."
    )

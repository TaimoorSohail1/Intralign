"""OSLO Chat responder (DTM-0037; DL-047 CHAT-01…04) — Disclose-class.

OSLO Chat is a Disclose-class INTERACTION surface (CONTEXT.md). It is a
**consumer/trigger**, never a producer:

- Intent **Explain / Clarify / Resolve** = CONSUME existing cognition. The router
  reads the governed projections through the SELECT-only read seam and hands them
  here as ``governed`` (a read-only snapshot); this responder phrases a response
  over them via the EXISTING fixture-backed LLM seam (``services/llm_provider`` —
  a recorded model-response fixture in CI, ADR-0004; internal gemma live in dev,
  the ``advise`` routing stage, DL-069 — no new model/routing).
- Intent **Improve** = TRIGGER cognition. It builds a ``TriggerClaim`` and calls
  the INJECTED ``submit_trigger("deep_pass", …, materializer=…)`` seam (the
  DTM-0032 pattern). The FROZEN Deep-Pass recompute appends its own CHRs via the
  frozen retain path — that is COGNITION's write, NEVER the chat's.

THE CRITICAL EPISTEMIC BOUNDARY (DL-047; Wave I QA negatives): the chat writes
NO canonical receipt (no attested-assertion / history-record / acceptance-record),
mutates NO artifact, and changes NO assessment. This responder is constructed
with NO canonical-write collaborator at all — it holds only the LLM provider +
the ``submit_trigger`` seam + the injected materializer. There is structurally
nothing here that could write canonical or mutate an artifact (the negatives
prove it: fake exploding stores are never wired in, and a source scan finds no
write seam named).

The product is a NON-CANONICAL ``ChatExchange`` (interaction record, like a
notification) — returned to the frontend, never persisted in this slice (no
migration; a durable ``chat_session``/``chat_exchange`` table is a flagged
follow-up).
"""

from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.services.llm_provider import LLMProvider
from shared.epistemic import ChatContext, ChatExchange, ChatIntent

# The model/prompt/rule version stamp for chat phrasing (audit + determinism).
# Chat answer text is AI-text → SEMANTIC tier (never byte-pinned); the exchange
# SURFACE (intent, inherited context, triggered-run id) is record-exact.
CHAT_VERSION = "wi-chat-v0"

# R1 registers one durable graph; the Improve intent triggers the deep_pass graph
# (the same FROZEN recompute DTM-0032 wires) — chat invents no orchestration.
_GRAPH_NAME = "deep_pass"

# The consume intents READ + phrase; only Improve TRIGGERS a recompute.
_TRIGGER_INTENTS = frozenset({"improve"})

_EXPLAIN_INSTRUCTIONS = (
    "You are OSLO Chat, an interaction surface over a project's EXISTING "
    "understanding. EXPLAIN the project's current governed cognition to the user "
    "in plain language. You may ONLY describe what is already there — you do NOT "
    "decide anything, accept anything, change any assessment, or write anything. "
    "Make clear that OSLO's findings are its derived reading, surfaced (not "
    "settled). Return a short plain-text answer."
)

_CLARIFY_INSTRUCTIONS = (
    "You are OSLO Chat. CLARIFY the meaning of an existing governed object "
    "(a finding/recommendation/confidence) for the user. Describe only what is "
    "already there; do NOT accept, resolve, score, or change any assessment. "
    "Return a short plain-text answer."
)

_RESOLVE_INSTRUCTIONS = (
    "You are OSLO Chat. Help the user understand HOW they could move a blocking "
    "ambiguity forward, by describing what input OSLO would need. You do NOT "
    "resolve it yourself, accept anything, or change any assessment — only the "
    "user's attested input + a recompute can. Return a short plain-text answer."
)

_IMPROVE_INSTRUCTIONS = (
    "You are OSLO Chat. The user asked OSLO to IMPROVE its understanding, so a "
    "deeper analysis pass has been TRIGGERED. Acknowledge that the recompute is "
    "running and that the assessment changes ONLY when it completes — this chat "
    "itself changes nothing. Return a short plain-text answer."
)

_INTENT_INSTRUCTIONS: dict[ChatIntent, str] = {
    "explain": _EXPLAIN_INSTRUCTIONS,
    "clarify": _CLARIFY_INSTRUCTIONS,
    "resolve": _RESOLVE_INSTRUCTIONS,
    "improve": _IMPROVE_INSTRUCTIONS,
}


def _exchange_id(project_id: str, intent: str, message: str, run: str | None) -> str:
    """A stable structural identity for an exchange turn (idempotency key basis).

    Hash over (project, intent, message, triggered-run) so the SAME structural
    input re-derives the SAME id — the router's Idempotency-Key cache returns the
    same exchange on retry without re-triggering.
    """
    basis = json.dumps(
        [project_id, intent, message.strip(), run or ""],
        sort_keys=True,
        ensure_ascii=False,
    )
    return "chatx-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def _summarize_governed(governed: Mapping[str, Sequence[Mapping[str, Any]]]) -> str:
    """A compact, READ-ONLY digest of the governed projections for the prompt.

    Consumes the projection rows the router read through the SELECT-only seam —
    it copies fields into the prompt and NEVER mutates them. Empty governed state
    yields an explicit 'nothing yet' note so the model never invents cognition.
    """
    lines: list[str] = []
    for kind, rows in governed.items():
        for row in rows:
            payload = row.get("current_payload", row) if isinstance(row, Mapping) else {}
            ident = payload.get(f"{kind}_id") or payload.get("projection_id") or row.get("projection_id")
            summary = payload.get("summary") or payload.get("band") or ""
            lines.append(f"- {kind} {ident}: {summary}".rstrip())
    return "\n".join(lines) if lines else "(no governed cognition for this project yet)"


@dataclass
class ChatResponder:
    """Phrases a chat response (consume) and triggers a recompute (Improve).

    Collaborators — DELIBERATELY only these (NO canonical-write handle exists on
    this object; the negatives assert the absence):

    - ``provider`` — the LLM seam (a recorded-fixture model in CI; the ``advise``
      routing stage, internal gemma primary, DL-069).
    - ``submit_trigger`` — the EXISTING orchestration seam (Improve only); the
      frozen recompute owns its CHR append, never the chat.
    - ``materializer`` — the DTM-0030 ProjectionMaterializer, injected into
      ``submit_trigger`` so a successful Improve materializes derived.*_current.
    - ``prompt_suffix_for`` — the recorded-fixture harness directive (empty live).
    """

    provider: LLMProvider
    submit_trigger: Any
    materializer: Any
    prompt_suffix_for: Any = field(default=None)  # Callable[[str], str] | None

    def _suffix(self, intent: str) -> str:
        if self.prompt_suffix_for is None:
            return ""
        return self.prompt_suffix_for(intent) or ""

    def _phrase(self, *, intent: ChatIntent, prompt: str) -> str:
        """Run one LLM phrasing pass over the read-only context (no write)."""
        from pydantic_ai import Agent

        suffix = self._suffix(intent)
        full = f"{prompt}\n{suffix}" if suffix else prompt
        model = self.provider.model_for(tier="free", stage="advise")
        result = Agent(
            model, output_type=str, instructions=_INTENT_INSTRUCTIONS[intent]
        ).run_sync(full)
        return str(result.output).strip()

    def _trigger_improve(self, *, project_id: str) -> str:
        """Improve → call the EXISTING submit_trigger seam (materializer injected).

        Returns the triggered run id (non-canonical bookkeeping). The recompute
        appends its own CHRs via the FROZEN retain path — never the chat.
        """
        run_id = str(uuid.uuid4())
        claim = TriggerClaim(
            trigger_type=TriggerType.REANALYSIS,
            project_id=project_id,
            information_changed=True,  # a user-requested improve IS an assessment-relevant event
            source="oslo_chat_improve",
        )
        self.submit_trigger(_GRAPH_NAME, claim, materializer=self.materializer)
        return run_id

    def respond(
        self,
        *,
        project_id: str,
        message: str,
        intent: ChatIntent,
        governed: Mapping[str, Sequence[Mapping[str, Any]]],
        context: ChatContext | Mapping[str, Any] | None,
    ) -> ChatExchange:
        """Produce a NON-CANONICAL ChatExchange for one turn.

        Consume intents (Explain/Clarify/Resolve) phrase over the governed
        cognition the router READ. Improve TRIGGERS the frozen Deep-Pass recompute
        (then acknowledges). NO canonical write, NO artifact mutation, NO
        assessment change happens here — the exchange is an interaction record.
        """
        inherited = _coerce_context(context)

        triggered_run: str | None = None
        if intent in _TRIGGER_INTENTS:
            triggered_run = self._trigger_improve(project_id=project_id)

        prompt = self._build_prompt(
            intent=intent, message=message, governed=governed, context=inherited
        )
        response = self._phrase(intent=intent, prompt=prompt)

        return ChatExchange(
            project_id=project_id,
            exchange_id=_exchange_id(project_id, intent, message, triggered_run),
            intent=intent,
            user_message=message,
            response=response,
            context=inherited,
            triggered_run=triggered_run,
            model_or_rule_version=CHAT_VERSION,
        )

    @staticmethod
    def _build_prompt(
        *,
        intent: ChatIntent,
        message: str,
        governed: Mapping[str, Sequence[Mapping[str, Any]]],
        context: ChatContext | None,
    ) -> str:
        ctx = (
            f"\nLaunched-from context: {context.object_type} {context.object_id}"
            if context is not None
            else ""
        )
        return (
            f"User message ({intent}): {message}{ctx}\n"
            f"Project's current governed cognition (read-only):\n"
            f"{_summarize_governed(governed)}"
        )


def _coerce_context(
    context: ChatContext | Mapping[str, Any] | None,
) -> ChatContext | None:
    """Normalize an inherited-context input to a ChatContext (or None)."""
    if context is None:
        return None
    if isinstance(context, ChatContext):
        return context
    if isinstance(context, Mapping) and context.get("object_type") and context.get("object_id"):
        return ChatContext(
            object_type=str(context["object_type"]),
            object_id=str(context["object_id"]),
        )
    return None

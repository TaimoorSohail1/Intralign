"""Pydantic AI adapter — the single LLM seam (DL-054 §5; DL-048 §4c routing).

PRIMARY = internal gemma on a local Llama runtime (OpenAI-compatible endpoint),
reached via pydantic-ai's ``OpenAIChatModel`` against an env ``base_url`` — no
new dependency (DL-069 / ADR-0007). OpenAI/Anthropic are a defined-but-disabled
fallback. Tier-keyed routing comes from config. This is the ONLY place a
provider is constructed, preserving routing/quota/audit (DL-054 cond. 3).

Determinism / cost discipline (ADR-0004; decisions #2/#11): a **real provider
call happens ONLY when the live env flag is set** (``OSLO_LLM_LIVE=1`` — dev +
the nightly baseline-update job). In PR CI the flag is unset, and the provider
is driven by an injected **recorded model-response fixture** (a pydantic-ai
``FunctionModel`` built by the tests/ harness). PR CI therefore makes ZERO
provider calls — it is deterministic, free, and offline.

Guardrail (DTM-0009 manual check): the provider SDK classes
(``OpenAIChatModel`` / ``AnthropicModel``) are imported **lazily, inside the
live branch only**. Importing this module — or running ``pytest`` — never
imports a provider SDK and never constructs a client.

Naming guard (reserved-term): the injected double is a *recorded model-response
fixture*, never a "replay"/"cassette" — ``replay`` is reserved for event-log
reconstruction (CONTEXT.md Register; ADR-0004).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from backend.services.llm_provider.config import (
    ModelRef,
    RoutingStage,
    Tier,
    routing_for_tier,
)

if TYPE_CHECKING:  # pragma: no cover - typing only, never imported at runtime
    from pydantic_ai.models import Model

# The env flag that authorizes a real provider call (dev + nightly only).
LIVE_ENV_FLAG = "OSLO_LLM_LIVE"
_TRUTHY = {"1", "true", "yes", "on"}

# The internal (primary) LLM endpoint config (DL-069 / ADR-0007). The local
# Llama runtime's OpenAI-compatible base_url is read from env — never hardcoded
# (ANTI_ASSUMPTION); the owner sets the live value (placeholder in .env.example).
INTERNAL_BASE_URL_ENV = "OSLO_LLM_BASE_URL"
INTERNAL_API_KEY_ENV = "OSLO_LLM_API_KEY"  # optional; the local server ignores it


def live_calls_enabled() -> bool:
    """True iff the live env flag authorizes real provider calls (dev/nightly)."""
    return os.environ.get(LIVE_ENV_FLAG, "").strip().lower() in _TRUTHY


class LiveCallsDisabledError(RuntimeError):
    """Raised when a real provider call is attempted with the live flag unset.

    This is the offline guard: in PR CI (flag unset) the engine must be driven
    by an injected recorded model-response fixture, never a live model.
    """


@dataclass(frozen=True)
class ResolvedModel:
    """The routing decision for a (tier, stage): which ModelRef serves it."""

    tier: Tier
    stage: RoutingStage
    model_ref: ModelRef

    @property
    def model_name(self) -> str:
        return self.model_ref.model

    @property
    def provider(self) -> str:
        return self.model_ref.provider


class LLMProvider:
    """The LLM seam: resolves tier-keyed routing and yields a pydantic-ai Model.

    In tests, construct with ``recorded_model=<FunctionModel>`` (the harness
    builds it from a recorded fixture) — no flag, no network. In dev/nightly,
    set ``OSLO_LLM_LIVE=1`` and leave ``recorded_model`` unset; the adapter
    lazily constructs the routed provider model.
    """

    def __init__(self, *, recorded_model: Model | None = None) -> None:
        # An injected recorded-model-response fixture model (FunctionModel /
        # TestModel). When present it serves EVERY routed stage offline.
        self._recorded_model = recorded_model

    def resolve(self, *, tier: Tier, stage: RoutingStage) -> ResolvedModel:
        """Resolve tier-keyed routing for a stage (DL-048 §4c) — pure, no I/O."""
        model_ref = routing_for_tier(tier).model_for(stage)
        return ResolvedModel(tier=tier, stage=stage, model_ref=model_ref)

    def model_for(self, *, tier: Tier, stage: RoutingStage) -> Model:
        """Return the pydantic-ai Model serving (tier, stage).

        Offline (default / PR CI): returns the injected recorded-fixture model
        if one was provided; otherwise raises ``LiveCallsDisabledError`` — the
        engine must never reach a provider in CI. Live (flag set): lazily
        constructs the routed provider model (OpenAI primary / Anthropic
        fallback).
        """
        if self._recorded_model is not None:
            return self._recorded_model
        if not live_calls_enabled():
            raise LiveCallsDisabledError(
                "no recorded model-response fixture was injected and "
                f"{LIVE_ENV_FLAG} is not set — PR CI must drive the LLM from a "
                "recorded fixture (ADR-0004); a real provider call is refused "
                "offline."
            )
        return self._build_live_model(self.resolve(tier=tier, stage=stage).model_ref)

    @staticmethod
    def _build_live_model(model_ref: ModelRef) -> Model:
        """Construct the routed provider model — LIVE ONLY (flag-gated, lazy import).

        The provider SDK is imported HERE so neither importing this module nor
        running pytest pulls in a provider SDK (DTM-0009 guardrail).
        """
        provider = model_ref.provider
        if provider == "internal":
            # PRIMARY (DL-069 / ADR-0007): the internal gemma model on a local
            # Llama runtime exposed over an OpenAI-compatible endpoint. We reuse
            # pydantic-ai's OpenAIChatModel against a local base_url (read from
            # env) — NO new dependency. The base_url is config, never hardcoded
            # (ANTI_ASSUMPTION); api_key is a dummy the local server ignores.
            from pydantic_ai.models.openai import OpenAIChatModel
            from pydantic_ai.providers.openai import OpenAIProvider

            base_url = os.environ.get(INTERNAL_BASE_URL_ENV, "").strip()
            if not base_url:
                raise LiveCallsDisabledError(
                    f"{INTERNAL_BASE_URL_ENV} is not set — the internal LLM "
                    "(local Llama runtime, OpenAI-compatible) needs its base_url "
                    "from env before a live call (DL-069; .env.example documents "
                    "the placeholder)."
                )
            return OpenAIChatModel(
                model_ref.model,
                provider=OpenAIProvider(
                    base_url=base_url,
                    api_key=os.environ.get(INTERNAL_API_KEY_ENV, "").strip() or "not-needed",
                ),
            )
        if provider == "openai":
            from pydantic_ai.models.openai import OpenAIChatModel

            return OpenAIChatModel(model_ref.model)
        if provider == "anthropic":
            from pydantic_ai.models.anthropic import AnthropicModel

            return AnthropicModel(model_ref.model)
        raise ValueError(
            f"unknown provider {provider!r} — routing is internal (primary, "
            "DL-069) with OpenAI/Anthropic a disabled fallback (DL-054)"
        )


def usage_tokens(usage: Any) -> tuple[int, int]:
    """Extract (tokens_in, tokens_out) from a pydantic-ai run usage object.

    Shape-robust across pydantic-ai versions so token accounting (DL-048 /
    DL-069 cond.2) never silently zeroes on a version drift: 1.x exposes
    ``input_tokens``/``output_tokens``; older lines used
    ``request_tokens``/``response_tokens``. We read the 1.x names first, then
    fall back to the legacy names (the dependency is pinned to 1.x in
    pyproject; this fallback is defence-in-depth so CI can never under-count).
    """

    def _first(*names: str) -> int:
        for name in names:
            value = getattr(usage, name, None)
            if value:
                return int(value)
        return 0

    tokens_in = _first("input_tokens", "request_tokens", "prompt_tokens")
    tokens_out = _first("output_tokens", "response_tokens", "completion_tokens")
    return tokens_in, tokens_out

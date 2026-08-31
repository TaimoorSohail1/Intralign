"""LLM provider abstraction (DL-054 §5): Pydantic AI + adapter; PRIMARY = internal gemma on a local Llama runtime (OpenAI-compatible), OpenAI/Anthropic a disabled fallback (DL-069 / ADR-0007). Preserves routing/quota/audit (DL-054 cond. 3).

Public surface (DTM-0009 / Wave S):

- ``LLMProvider`` — the seam; resolves tier-keyed routing and yields a
  pydantic-ai Model (a recorded model-response fixture offline, a live model
  only behind ``OSLO_LLM_LIVE``).
- ``RunBudget`` / ``spend_event_payload`` — per-run token-budget accounting +
  the ``ai_spend_recorded`` payload (DL-048 cost governance).
- ``config`` — tier-keyed routing + budgets + cost basis (Calibration §4c).
"""

from backend.services.llm_provider.adapter import (
    INTERNAL_BASE_URL_ENV,
    LIVE_ENV_FLAG,
    LiveCallsDisabledError,
    LLMProvider,
    ResolvedModel,
    live_calls_enabled,
    usage_tokens,
)
from backend.services.llm_provider.budget import RunBudget, spend_event_payload
from backend.services.llm_provider.config import (
    DEFAULT_INTERNAL_MODEL,
    INTERNAL_MODEL_ENV,
    PRIMARY_PROVIDER_ENV,
    PRIMARY_PROVIDER_INTERNAL,
    PRIMARY_PROVIDER_OPENAI,
    ModelRef,
    budget_for_tier,
    estimate_cost_usd,
    internal_model_id,
    primary_provider_id,
    routing_for_tier,
)

__all__ = [
    "DEFAULT_INTERNAL_MODEL",
    "INTERNAL_BASE_URL_ENV",
    "INTERNAL_MODEL_ENV",
    "LIVE_ENV_FLAG",
    "LLMProvider",
    "LiveCallsDisabledError",
    "ModelRef",
    "PRIMARY_PROVIDER_ENV",
    "PRIMARY_PROVIDER_INTERNAL",
    "PRIMARY_PROVIDER_OPENAI",
    "ResolvedModel",
    "RunBudget",
    "budget_for_tier",
    "estimate_cost_usd",
    "internal_model_id",
    "live_calls_enabled",
    "primary_provider_id",
    "routing_for_tier",
    "spend_event_payload",
    "usage_tokens",
]

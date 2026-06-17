"""LLM provider abstraction (DL-054 §5): Pydantic AI + adapter; OpenAI primary / Anthropic fallback. Preserves routing/quota/audit (DL-054 cond. 3).

Public surface (DTM-0009 / Wave S):

- ``LLMProvider`` — the seam; resolves tier-keyed routing and yields a
  pydantic-ai Model (a recorded model-response fixture offline, a live model
  only behind ``OSLO_LLM_LIVE``).
- ``RunBudget`` / ``spend_event_payload`` — per-run token-budget accounting +
  the ``ai_spend_recorded`` payload (DL-048 cost governance).
- ``config`` — tier-keyed routing + budgets + cost basis (Calibration §4c).
"""

from backend.services.llm_provider.adapter import (
    LIVE_ENV_FLAG,
    LiveCallsDisabledError,
    LLMProvider,
    ResolvedModel,
    live_calls_enabled,
    usage_tokens,
)
from backend.services.llm_provider.budget import RunBudget, spend_event_payload
from backend.services.llm_provider.config import (
    ModelRef,
    budget_for_tier,
    estimate_cost_usd,
    routing_for_tier,
)

__all__ = [
    "LIVE_ENV_FLAG",
    "LLMProvider",
    "LiveCallsDisabledError",
    "ModelRef",
    "ResolvedModel",
    "RunBudget",
    "budget_for_tier",
    "estimate_cost_usd",
    "live_calls_enabled",
    "routing_for_tier",
    "spend_event_payload",
    "usage_tokens",
]

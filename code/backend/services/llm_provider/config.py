"""Tier-keyed LLM routing + cost-governance config (DL-048 §4c; DL-054 cond. 3).

These are *dials, not architecture* (Calibration Defaults §4c): the owner may
retune any value without a new Decision. They are transcribed here verbatim
from ``RELEASE_1_CALIBRATION_DEFAULTS_V1.md`` §4c (Free tier) — the binding
source. Paid-tier rows are owner-deferred (Open-TBD A1/E3); add tier rows, not
code, when defined (we expose only what §4c pins).

What this module fixes:

- **Routing is tier-keyed** (§4c "Model routing"): Free routes
  ``extraction -> nano``, ``synthesis/generation -> mini``, with a Haiku
  fallback. The engine must HONOR routing — wrong-tier routing (e.g. Free
  generation on a full-quality model) is a contracted negative (DL-048 QA).
- **Per-run token budgets** (§4c): Free Fast 150,000 / run, Deep 600,000 / run.
  Over a per-run budget -> graceful degradation (partial model from the
  highest-priority evidence + defer), never silent overspend.
- **Per-user rollups** (§4c): daily 500,000, monthly 4,000,000 (the binding
  governor).
- **Cost basis** (§4c "Cost basis", June 2026 verified pricing) — used to
  estimate ``est_cost`` on the ``ai_spend_recorded`` event. USD per 1M tokens
  (input, output).

NO live provider import happens here — this is pure config. The numbers are
config the owner tunes; the *enforcement* is contracted (DL-048).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

# The internal model id (the local Llama runtime's gemma model). Owner-given
# default is ``gemma4`` (DL-059 / ADR-0007); read from env so the exact id is
# config, not a hardcoded constant (ANTI_ASSUMPTION). The live base_url is read
# in the adapter from ``OSLO_LLM_BASE_URL`` (placeholder in .env.example).
INTERNAL_MODEL_ENV = "OSLO_LLM_MODEL"
DEFAULT_INTERNAL_MODEL = "gemma4"


def internal_model_id() -> str:
    """The internal (gemma) model id from env, defaulting to ``gemma4``."""
    return os.environ.get(INTERNAL_MODEL_ENV, "").strip() or DEFAULT_INTERNAL_MODEL

# The model-routing *stages* the engine routes (Wave S: extraction +
# synthesis/generation). Each maps to a routed model per tier.
RoutingStage = Literal["extraction", "synthesis", "generation"]

# Subscription tier (Free is the only §4c-pinned tier; paid is owner-deferred).
Tier = Literal["free", "paid", "internal"]

# DL-046 modes (the per-run token cap is keyed by mode).
Mode = Literal["fast", "deep"]


@dataclass(frozen=True)
class ModelRef:
    """A routed model identity: provider + model name (no client constructed)."""

    provider: str
    model: str

    def as_dict(self) -> dict[str, str]:
        return {"provider": self.provider, "model": self.model}


@dataclass(frozen=True)
class TierBudget:
    """Per-tier token budgets (Calibration §4c) — per-run caps + rollups."""

    fast_per_run: int
    deep_per_run: int
    daily_per_user: int
    monthly_per_user: int

    def per_run_cap(self, mode: Mode) -> int:
        """The per-run token cap for ``mode`` (the degrade trigger, §4c)."""
        return self.fast_per_run if mode == "fast" else self.deep_per_run


@dataclass(frozen=True)
class TierRouting:
    """Per-tier model routing: which model serves each stage + the fallback."""

    extraction: ModelRef
    synthesis: ModelRef
    generation: ModelRef
    fallback: ModelRef

    def model_for(self, stage: RoutingStage) -> ModelRef:
        return getattr(self, stage)


# Cost basis (Calibration §4c "Cost basis", June 2026 verified) — USD per 1M
# tokens, (input, output). Used to estimate est_cost for ai_spend_recorded.
COST_PER_MILLION: dict[str, tuple[float, float]] = {
    # Internal gemma on the local Llama runtime — local inference is un-metered,
    # so est_cost is 0 (tokens are still recorded). DL-059 / ADR-0007.
    DEFAULT_INTERNAL_MODEL: (0.0, 0.0),
    "gpt-4.1": (2.0, 8.0),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    "claude-sonnet-4.6": (3.0, 15.0),
    "claude-haiku-4.5": (1.0, 5.0),
}

# Internal/primary routing (DL-059 / ADR-0007): all stages route to the internal
# gemma model on the local Llama runtime (OpenAI-compatible). This is the PRIMARY
# routing the engines resolve. The internal model id is config (env, default
# ``gemma4``) — built lazily so an env change at run time is honored. The OpenAI
# fallback ModelRef is kept defined but non-primary (disabled-by-default).
def _internal_routing() -> TierRouting:
    internal = ModelRef("internal", internal_model_id())
    return TierRouting(
        extraction=internal,
        synthesis=internal,
        generation=internal,
        fallback=ModelRef("openai", "gpt-4.1-mini"),
    )


# OpenAI/Anthropic routing — the DEMOTED, disabled-by-default fallback (DL-059):
# kept defined (the §4c Free routing) so a config flip can re-enable it, but it
# is NOT the primary the engines resolve. (Was the primary pre-DL-059.)
_OPENAI_FALLBACK_ROUTING = TierRouting(
    extraction=ModelRef("openai", "gpt-4.1-nano"),
    synthesis=ModelRef("openai", "gpt-4.1-mini"),
    generation=ModelRef("openai", "gpt-4.1-mini"),
    fallback=ModelRef("anthropic", "claude-haiku-4.5"),
)

# Free-tier budgets (Calibration §4c): Fast 150k/run, Deep 600k/run,
# daily 500k, monthly 4M.
_FREE_BUDGET = TierBudget(
    fast_per_run=150_000,
    deep_per_run=600_000,
    daily_per_user=500_000,
    monthly_per_user=4_000_000,
)

# Budgets stay §4c-pinned (Free). The internal tier reuses the Free TierBudget
# as a soft/observability bound — local inference is un-metered, so we do NOT
# invent new budget numbers (ANTI_ASSUMPTION; DL-059 cond. budget). Paid rows
# remain owner-deferred (Open-TBD A1/E3).
_BUDGET_BY_TIER: dict[str, TierBudget] = {"free": _FREE_BUDGET, "internal": _FREE_BUDGET}


def routing_for_tier(tier: Tier) -> TierRouting:
    """The model routing for ``tier``.

    PRIMARY (DL-059 / ADR-0007): the internal gemma model on the local Llama
    runtime serves every tier/stage — ``free``, ``internal``, and any unknown
    tier all resolve to the internal routing (the default). OpenAI/Anthropic are
    a defined-but-disabled fallback (``_OPENAI_FALLBACK_ROUTING``), not the
    primary the engines resolve. Built fresh so an env change to the model id is
    honored without a reimport.
    """
    return _internal_routing()


def budget_for_tier(tier: Tier) -> TierBudget:
    """The token budgets for ``tier`` (Free §4c; internal reuses the Free bound)."""
    return _BUDGET_BY_TIER.get(tier, _FREE_BUDGET)


def estimate_cost_usd(model: str, tokens_in: int, tokens_out: int) -> float:
    """Estimate run cost in USD from the §4c cost basis (0.0 if model unknown).

    An unknown model yields 0.0 rather than guessing a price (ANTI_ASSUMPTION):
    the spend event still records the real token counts; only the dollar
    estimate is unavailable until the owner adds the model to the cost basis.
    """
    rate = COST_PER_MILLION.get(model)
    if rate is None:
        return 0.0
    rate_in, rate_out = rate
    return round((tokens_in / 1_000_000) * rate_in + (tokens_out / 1_000_000) * rate_out, 6)

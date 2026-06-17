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

from dataclasses import dataclass
from typing import Literal

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
    "gpt-4.1": (2.0, 8.0),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    "claude-sonnet-4.6": (3.0, 15.0),
    "claude-haiku-4.5": (1.0, 5.0),
}

# Free-tier routing (Calibration §4c): extraction -> nano, synthesis/generation
# -> mini, Haiku fallback. OpenAI primary / Anthropic fallback (DL-054).
_FREE_ROUTING = TierRouting(
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

# Only the Free tier is owner-pinned in §4c. Paid/internal rows are
# owner-deferred (Open-TBD A1/E3) — DO NOT invent their numbers
# (ANTI_ASSUMPTION). They fall back to the Free config until the owner sets
# them; a wrong-tier-routing test asserts Free never routes a full model.
_ROUTING_BY_TIER: dict[str, TierRouting] = {"free": _FREE_ROUTING}
_BUDGET_BY_TIER: dict[str, TierBudget] = {"free": _FREE_BUDGET}


def routing_for_tier(tier: Tier) -> TierRouting:
    """The model routing for ``tier`` (Free is the only §4c-pinned tier)."""
    return _ROUTING_BY_TIER.get(tier, _FREE_ROUTING)


def budget_for_tier(tier: Tier) -> TierBudget:
    """The token budgets for ``tier`` (Free is the only §4c-pinned tier)."""
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

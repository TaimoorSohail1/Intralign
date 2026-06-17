"""Per-run token-budget accounting + the ``ai_spend_recorded`` payload (DL-048).

Cost governance (decision #7; Calibration §4c): synthesis/generation run within
the per-tier per-run token budget. Over-budget is NOT a silent overspend and
NOT a runaway re-analysis — it is a *graceful degradation*: synthesize a
partial model from the highest-priority evidence within budget, defer the rest
to a coalesced Deep Pass, and EMIT ``ai_spend_recorded`` so over-budget is a
visible trust signal.

This module is pure accounting — it does NOT call a provider. The engine asks
the ``RunBudget`` "may I spend ~N more tokens?" before each provider call;
when the answer is no, the engine degrades. After each call it records the
actual usage. ``spend_event_payload`` builds the single shared
``ai_spend_recorded`` shape (decision #9; OBS §3): tokens_in/out, est_cost,
tier, user, mode, model — plus the mode/confidence_stage attributes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.services.llm_provider.config import (
    Mode,
    Tier,
    budget_for_tier,
    estimate_cost_usd,
)


@dataclass
class RunBudget:
    """Mutable per-run token accountant bound to a (tier, mode) budget cap.

    ``cap`` is the per-run token cap for this (tier, mode) from Calibration §4c.
    The engine calls :meth:`can_afford` before a provider call and
    :meth:`record` after it. ``over_budget`` flips True the moment recorded
    spend reaches the cap (the degrade trigger). The accountant NEVER blocks a
    call by raising — it returns a boolean so the engine degrades gracefully
    rather than crashing (DL-048: never silent overspend, never runaway).
    """

    tier: Tier
    mode: Mode
    cap: int
    tokens_in: int = 0
    tokens_out: int = 0
    per_call: list[tuple[int, int, str]] = field(default_factory=list)

    @classmethod
    def for_run(cls, *, tier: Tier, mode: Mode) -> RunBudget:
        """Build a RunBudget from the §4c per-tier per-run cap for ``mode``."""
        cap = budget_for_tier(tier).per_run_cap(mode)
        return cls(tier=tier, mode=mode, cap=cap)

    @property
    def spent(self) -> int:
        return self.tokens_in + self.tokens_out

    @property
    def remaining(self) -> int:
        return max(self.cap - self.spent, 0)

    @property
    def over_budget(self) -> bool:
        """True once recorded spend has reached/exceeded the per-run cap."""
        return self.spent >= self.cap

    def can_afford(self, estimated_tokens: int) -> bool:
        """True iff an estimated ``estimated_tokens`` call still fits the cap.

        The engine asks this BEFORE each provider call; a False answer is the
        degrade signal (synthesize partial + defer) — never an overspend.
        """
        if self.over_budget:
            return False
        return self.spent + max(estimated_tokens, 0) <= self.cap

    def record(self, *, tokens_in: int, tokens_out: int, model: str) -> None:
        """Record the ACTUAL usage of one provider call (post-call accounting)."""
        self.tokens_in += max(tokens_in, 0)
        self.tokens_out += max(tokens_out, 0)
        self.per_call.append((tokens_in, tokens_out, model))

    def est_cost_usd(self) -> float:
        """Total estimated USD spend across all recorded calls (§4c cost basis)."""
        return round(
            sum(estimate_cost_usd(m, ti, to) for ti, to, m in self.per_call), 6
        )


def spend_event_payload(
    budget: RunBudget,
    *,
    user: str,
    model: str,
    confidence_stage: str,
    understanding_state: str,
    degraded: bool,
) -> dict[str, Any]:
    """Build the single shared ``ai_spend_recorded`` payload (decision #9; DL-048 OBS).

    Carries tokens_in/out, est_cost, tier, user, mode, model (the DL-048 fields)
    plus the mode/confidence_stage/understanding_state attributes (decision #6)
    and a ``degraded``/``over_budget`` trust signal (over-budget is a trust
    signal, not just a metric — DL-048 OBS).
    """
    return {
        "tokens_in": budget.tokens_in,
        "tokens_out": budget.tokens_out,
        "est_cost": budget.est_cost_usd(),
        "tier": budget.tier,
        "user": user,
        "mode": budget.mode,
        "model": model,
        "confidence_stage": confidence_stage,
        "understanding_state": understanding_state,
        "over_budget": budget.over_budget,
        "degraded": degraded,
    }

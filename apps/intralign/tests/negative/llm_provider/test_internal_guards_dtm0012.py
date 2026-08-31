"""DTM-0012 negatives — the offline discipline still holds for the internal primary.

The internal gemma primary does NOT relax the ADR-0004 offline guard: with no
recorded fixture injected and ``OSLO_LLM_LIVE`` unset, an internal-routed live
call is still refused (``LiveCallsDisabledError``). With the flag set but the
internal ``base_url`` env unset, the adapter refuses rather than guessing a URL
(ANTI_ASSUMPTION). An external full-quality model is still wrong-tier for Free.
No test here makes a real provider call.
"""

from __future__ import annotations

import pytest

from backend.services.llm_provider import (
    INTERNAL_BASE_URL_ENV,
    LIVE_ENV_FLAG,
    LiveCallsDisabledError,
    LLMProvider,
    ModelRef,
    internal_model_id,
    live_calls_enabled,
    routing_for_tier,
)


def test_offline_guard_refuses_internal_live_call_with_flag_unset(monkeypatch) -> None:
    """No recorded fixture + flag unset → internal live call refused (PR CI premise)."""
    monkeypatch.delenv(LIVE_ENV_FLAG, raising=False)
    assert not live_calls_enabled()
    with pytest.raises(LiveCallsDisabledError):
        LLMProvider().model_for(tier="free", stage="synthesis")


def test_internal_branch_refuses_when_base_url_env_is_unset(monkeypatch) -> None:
    """ANTI_ASSUMPTION — no base_url env → refuse rather than guess a URL."""
    monkeypatch.delenv(INTERNAL_BASE_URL_ENV, raising=False)
    with pytest.raises(LiveCallsDisabledError):
        LLMProvider._build_live_model(ModelRef("internal", internal_model_id()))


def test_external_full_model_is_still_wrong_tier_for_free() -> None:
    """Free never routes to an external full-quality model (gpt-4.1)."""
    routing = routing_for_tier("free")
    assert routing.synthesis.model != "gpt-4.1"
    assert routing.synthesis.provider != "openai"  # primary is internal, not external
    assert routing.generation.model != "gpt-4.1"

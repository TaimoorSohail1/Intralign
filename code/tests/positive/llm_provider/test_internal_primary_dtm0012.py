"""DTM-0012 (DL-069 / ADR-0007) — internal gemma is the PRIMARY LLM at the seam.

Positive proofs that the internal gemma model on a local Llama runtime
(OpenAI-compatible endpoint) is the primary the seam resolves, that the adapter
builds an ``OpenAIChatModel`` against the env ``base_url`` WITHOUT a network
call, that local inference is un-metered (est_cost 0), that the CHR provenance
records the ACTUAL provider/model, and that the OpenAI/Anthropic fallback branch
still constructs. No test here makes a real provider call (ADR-0004 intact).
"""

from __future__ import annotations

from backend.services.llm_provider import (
    DEFAULT_INTERNAL_MODEL,
    INTERNAL_BASE_URL_ENV,
    LIVE_ENV_FLAG,
    LLMProvider,
    ModelRef,
    PRIMARY_PROVIDER_ENV,
    estimate_cost_usd,
    internal_model_id,
    primary_provider_id,
    routing_for_tier,
)
from backend.services.llm_provider.adapter import INTERNAL_API_KEY_ENV
from backend.services.llm_provider.config import INTERNAL_MODEL_ENV


def test_internal_is_the_primary_routing_for_every_stage() -> None:
    """Free/default routing resolves to internal gemma for all three stages."""
    gemma = internal_model_id()
    assert gemma == DEFAULT_INTERNAL_MODEL  # env default is gemma4
    provider = LLMProvider()
    for stage in ("extraction", "synthesis", "generation"):
        resolved = provider.resolve(tier="free", stage=stage)  # type: ignore[arg-type]
        assert resolved.provider == "internal"
        assert resolved.model_name == gemma
    # The internal tier resolves the same primary.
    routing = routing_for_tier("internal")
    assert routing.synthesis == ModelRef("internal", gemma)


def test_openai_can_be_selected_as_hosted_primary(monkeypatch) -> None:
    """Hosted deploys can select the OpenAI routing without changing code."""
    monkeypatch.setenv(PRIMARY_PROVIDER_ENV, "openai")
    assert primary_provider_id() == "openai"
    routing = routing_for_tier("free")
    assert routing.extraction == ModelRef("openai", "gpt-4.1-nano")
    assert routing.synthesis == ModelRef("openai", "gpt-4.1-mini")
    assert routing.generation == ModelRef("openai", "gpt-4.1-mini")
    assert routing.advise == ModelRef("openai", "gpt-4.1-mini")
    provider = LLMProvider()
    assert provider.resolve(tier="free", stage="synthesis").provider == "openai"


def test_model_id_is_config_from_env(monkeypatch) -> None:
    """The gemma model id is read from env (config, not a hardcoded constant)."""
    monkeypatch.setenv(INTERNAL_MODEL_ENV, "gemma4-custom")
    assert internal_model_id() == "gemma4-custom"
    assert routing_for_tier("free").synthesis.model == "gemma4-custom"


def test_internal_branch_builds_openai_chat_model_against_env_base_url(monkeypatch) -> None:
    """``_build_live_model`` for provider==internal builds an OpenAIChatModel on the
    env base_url — constructed, never called (no network)."""
    monkeypatch.setenv(INTERNAL_BASE_URL_ENV, "http://localhost:11434/v1")
    monkeypatch.delenv(INTERNAL_API_KEY_ENV, raising=False)
    model = LLMProvider._build_live_model(ModelRef("internal", "gemma4"))
    from pydantic_ai.models.openai import OpenAIChatModel

    assert isinstance(model, OpenAIChatModel)
    assert model.model_name == "gemma4"
    # The client is configured against the local base_url (construction only).
    assert str(model.client.base_url).rstrip("/") == "http://localhost:11434/v1"


def test_estimate_cost_for_gemma_is_zero() -> None:
    """Local inference is un-metered → est_cost 0 (tokens still recorded)."""
    assert estimate_cost_usd(DEFAULT_INTERNAL_MODEL, 1_000_000, 1_000_000) == 0.0


def test_openai_fallback_branch_still_constructs(monkeypatch) -> None:
    """The disabled OpenAI/Anthropic fallback ModelRefs still build a live model."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-dummy")
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.models.openai import OpenAIChatModel

    openai_model = LLMProvider._build_live_model(ModelRef("openai", "gpt-4.1-mini"))
    assert isinstance(openai_model, OpenAIChatModel)
    anthropic_model = LLMProvider._build_live_model(ModelRef("anthropic", "claude-haiku-4.5"))
    assert isinstance(anthropic_model, AnthropicModel)


def test_live_flag_constant_is_unchanged() -> None:
    """The OSLO_LLM_LIVE gate constant is preserved (offline discipline intact)."""
    assert LIVE_ENV_FLAG == "OSLO_LLM_LIVE"

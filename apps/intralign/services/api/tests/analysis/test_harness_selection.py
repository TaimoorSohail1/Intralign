import pytest

from oslo_api.analysis import DeterministicAgentHarness
from oslo_api.analysis.openai_harness import OpenAIAgentHarness
from oslo_api.analysis.service import build_agent_harness
from oslo_api.settings import Settings


def settings(**overrides) -> Settings:
    return Settings(
        _env_file=None,
        supabase_secret_key="x" * 20,
        **overrides,
    )


def test_auto_mode_requires_openai_key_instead_of_fabricating_analysis() -> None:
    with pytest.raises(
        RuntimeError,
        match="OPENAI_API_KEY_REQUIRED_FOR_OPENAI_HARNESS",
    ):
        build_agent_harness(settings(analysis_harness="auto", openai_api_key=None))


def test_auto_mode_uses_openai_directly_when_key_exists() -> None:
    harness = build_agent_harness(
        settings(
            analysis_harness="auto",
            openai_api_key="sk-test-only-not-a-real-key",
            openai_fast_model="gpt-fast",
            openai_extended_model="gpt-deep",
        )
    )

    assert isinstance(harness, OpenAIAgentHarness)


def test_deterministic_harness_requires_explicit_configuration() -> None:
    harness = build_agent_harness(
        settings(analysis_harness="deterministic", openai_api_key=None)
    )

    assert isinstance(harness, DeterministicAgentHarness)

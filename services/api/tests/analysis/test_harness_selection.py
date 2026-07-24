from oslo_api.analysis import DeterministicAgentHarness, FallbackAgentHarness
from oslo_api.analysis.service import build_agent_harness
from oslo_api.settings import Settings


def settings(**overrides) -> Settings:
    return Settings(
        _env_file=None,
        supabase_secret_key="x" * 20,
        **overrides,
    )


def test_auto_mode_uses_deterministic_harness_when_no_key_exists() -> None:
    harness = build_agent_harness(
        settings(analysis_harness="auto", openai_api_key=None)
    )

    assert isinstance(harness, DeterministicAgentHarness)


def test_auto_mode_enables_resilient_openai_harness_when_key_exists() -> None:
    harness = build_agent_harness(
        settings(
            analysis_harness="auto",
            openai_api_key="sk-test-only-not-a-real-key",
            openai_fast_model="gpt-fast",
            openai_extended_model="gpt-deep",
        )
    )

    assert isinstance(harness, FallbackAgentHarness)

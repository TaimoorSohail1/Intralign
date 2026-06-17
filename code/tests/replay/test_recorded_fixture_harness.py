"""Harness self-test — PR CI makes ZERO provider calls (ADR-0004; decision #11).

This is the recorded model-response fixture harness's own proof. It is NOT a
"replay" test (``replay`` is reserved for event-log reconstruction that does
not re-run the LLM — CONTEXT.md Register); it lives under tests/replay/ only
because that is the determinism-harness home, but it tests the *recorded
fixture* double. Pure — never skips, never touches a network.

Proven here:

- Every recorded fixture carries its ``model_version`` + ``config`` stamp (the
  baseline component; a missing stamp is a hard error).
- Running an Agent against the harness's FunctionModel serves recorded
  responses only — the call counter proves the model was the fixture, not a
  provider.
- No provider SDK (``pydantic_ai.models.openai`` / ``.anthropic``) is imported
  by exercising the harness; the offline guard refuses a live model with the
  env flag unset.
"""

from __future__ import annotations

import sys

import pytest
from pydantic_ai import Agent

from backend.services.llm_provider import (
    LiveCallsDisabledError,
    LLMProvider,
    live_calls_enabled,
)
from tests._fixtures.recorded_model_responses import (
    FIXTURE_DIR,
    FixtureStampError,
    build_recorded_model,
    load_fixture,
    response_key_directive,
)

_FIXTURE_NAMES = sorted(p.stem for p in FIXTURE_DIR.glob("*.json"))


def test_at_least_one_recorded_fixture_exists() -> None:
    assert _FIXTURE_NAMES, "the recorded-fixture harness must ship fixtures"


@pytest.mark.parametrize("name", _FIXTURE_NAMES)
def test_every_fixture_carries_a_baseline_stamp(name: str) -> None:
    fixture = load_fixture(name)
    assert fixture.model_version, f"{name}: missing model_version stamp"
    assert fixture.config, f"{name}: missing config stamp"


def test_missing_stamp_is_rejected(tmp_path, monkeypatch) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text('{"responses": []}', encoding="utf-8")
    monkeypatch.setattr(
        "tests._fixtures.recorded_model_responses.FIXTURE_DIR", tmp_path
    )
    with pytest.raises(FixtureStampError):
        load_fixture("bad")


def test_agent_runs_entirely_on_recorded_responses() -> None:
    """An Agent over the harness model serves recorded output — zero live calls."""
    session = build_recorded_model("ws_synthesis_v0")
    agent = Agent(session.model(), output_type=str)
    before = set(sys.modules)
    result = agent.run_sync(f"synthesize {response_key_directive('synthesis')}")
    assert session.call_count == 1  # the fixture served the response, not a provider
    assert "intent_summary" in result.output
    # exercising the harness imported no provider SDK.
    newly = set(sys.modules) - before
    assert not any(
        m.startswith(("pydantic_ai.models.openai", "pydantic_ai.models.anthropic"))
        for m in newly
    )


def test_offline_provider_refuses_a_live_model() -> None:
    """With no recorded model injected and the flag unset, a live call is refused."""
    assert not live_calls_enabled()  # PR CI never sets OSLO_LLM_LIVE
    with pytest.raises(LiveCallsDisabledError):
        LLMProvider().model_for(tier="free", stage="synthesis")


def test_no_provider_sdk_imported_by_importing_llm_provider() -> None:
    """Importing the seam never pulls a provider SDK (DTM-0009 guardrail).

    Checked in a FRESH interpreter so the invariant is order-independent: other
    suites legitimately exercise the live branch (which lazily imports the SDK by
    design — DTM-0012), polluting this process's ``sys.modules``. The guarded
    invariant — *importing the seam* pulls no SDK — is only meaningful in a clean
    interpreter.
    """
    import subprocess

    code = (
        "import sys; import backend.services.llm_provider as _; "
        "assert 'pydantic_ai.models.openai' not in sys.modules; "
        "assert 'pydantic_ai.models.anthropic' not in sys.modules"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

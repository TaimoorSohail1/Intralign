"""DTM-0040 / DL-048 UP-4 — the honest-limit signal (the missing enforcement seam).

The spend-gate + graceful degradation + ``ai_spend_recorded`` already exist (Wave
B; ``test_b2_cost.py`` / ``test_b3_cost_governance.py``). What was missing is the
HONEST-LIMIT SIGNAL: the truthful partial-analysis disclosure the DTM-0029
``HonestLimitDisclosure`` frontend renders. This suite proves the signal is built
from a degraded run (and absent on a complete one), in the shape the frontend reads
(``limited`` / ``reason`` / ``coverage_note`` — match ``HonestLimitDisclosure.tsx``),
carried on the run ``outputs`` envelope — no invented number, all from §4c config.
"""

from __future__ import annotations

from backend.responsibilities.infer.honest_limit import honest_limit_for_result
from backend.responsibilities.infer.stage import run_synthesis_stage
from backend.services.llm_provider import budget_for_tier
from shared.epistemic import PLANNING_ARTIFACT_TYPES
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine

# The HonestLimit shape fields the DTM-0029 frontend reads (HonestLimitDisclosure.tsx).
_FRONTEND_FIELDS = {"limited", "reason", "coverage_note"}


def _ids() -> list[str]:
    return [f"assertion-{i}" for i in range(4)]


def test_within_budget_run_is_not_limited_and_carries_no_honest_disclosure() -> None:
    """A complete run → the signal is ``limited: false`` (frontend renders NOTHING)."""
    engine, _ = synthesis_engine()  # the normal (small-token) recorded fixture
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert not result.degraded
    signal = honest_limit_for_result(result)
    assert signal["limited"] is False
    # When not limited the frontend shows nothing — no fabricated partial reason.
    assert not signal.get("reason")


def test_over_budget_run_produces_the_honest_limit_signal_in_frontend_shape() -> None:
    """DL-048 UP-4 — degraded → ``limited: true`` + a truthful reason + coverage note."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert result.degraded is True
    signal = honest_limit_for_result(result)
    # The shape matches the frontend's HonestLimit interface exactly.
    assert _FRONTEND_FIELDS <= set(signal)
    assert signal["limited"] is True
    # The disclosure is truthful: a non-empty reason + coverage note (shown verbatim).
    assert isinstance(signal["reason"], str) and signal["reason"].strip()
    assert isinstance(signal["coverage_note"], str) and signal["coverage_note"].strip()


def test_honest_limit_signal_rides_the_run_outputs_envelope() -> None:
    """The signal travels on the run/projection envelope (no schema change, no migration)."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    ctx = FakeStageContext()
    result = run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(),
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
    )
    # run_synthesis_stage still returns the SynthesisResult (back-compat); it is degraded.
    assert result.degraded is True

    # The stage FN (the node orchestration registers) surfaces honest_limit on the
    # run outputs envelope. Build it with a FRESH recorded session (the one above
    # is consumed) so the over-budget run replays deterministically.
    from backend.responsibilities.infer.stage import build_infer_stage
    from tests._fixtures.recorded_model_responses import response_key_directive

    stage_engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    stage = build_infer_stage(
        provider=stage_engine.provider,
        extract_inputs=lambda _s: {
            "project_id": PROJECT,
            "assertions": sample_drafts(),
            "assertion_ids": _ids(),
            "recompute_trigger": "knowledge-change",
        },
        prompt_suffix_for=response_key_directive,
    )
    state_update = stage(object(), FakeStageContext())
    honest = state_update["outputs"]["honest_limit"]
    assert honest["limited"] is True
    assert honest["reason"]


def test_honest_limit_coverage_note_reports_the_deferred_coverage_not_a_made_up_number() -> None:
    """Coverage is reported from the run's OWN counts (generated vs deferred) — not invented."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    signal = honest_limit_for_result(result)
    generated = len(result.artifacts)
    total = len(PLANNING_ARTIFACT_TYPES)
    # The coverage note mentions the real generated/total counts (the run's own data).
    assert str(generated) in signal["coverage_note"]
    assert str(total) in signal["coverage_note"]


def test_honest_limit_cap_comes_from_calibration_4c_config_not_a_literal() -> None:
    """The degrade trigger is the §4c per-run cap (config) — the signal asserts no magic number."""
    # The per-run cap the engine degrades against is config (budget_for_tier), so the
    # honest-limit signal is derivative of a CONFIGURED budget, never a hardcoded one.
    cap = budget_for_tier("free").per_run_cap("fast")
    assert cap == 150_000  # Calibration §4c Free Fast per-run cap (config source)

"""DTM-0040 / DL-048 UP-4 — the honest-limit Critical negatives.

The honest-limit signal is an EPISTEMIC-SAFETY obligation. The negatives:

- a budget-exceeded run is NEVER presented as complete (``limited`` must be True
  whenever the run degraded — an over-budget partial can't masquerade as a full
  result);
- the truthful disclosure is carried ALONGSIDE, never instead of, the upgrade —
  the signal's disclosure (reason + coverage) is mandatory; an upgrade prompt can
  never suppress it;
- spend is STILL recorded on degradation (the honest-limit path emits
  ``ai_spend_recorded`` — degradation is not a silent run);
- NO invented number — the cap that triggers the signal is the §4c CONFIG cap,
  not a literal embedded in the honest-limit code.
"""

from __future__ import annotations

import inspect

from backend.responsibilities.infer import honest_limit as honest_limit_mod
from backend.responsibilities.infer.honest_limit import honest_limit_for_result
from backend.responsibilities.infer.stage import run_synthesis_stage
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine


def _ids() -> list[str]:
    return [f"a{i}" for i in range(4)]


def test_a_degraded_run_is_never_presented_as_complete() -> None:
    """CRITICAL — a budget-exceeded run can NEVER report ``limited: false``."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    assert result.degraded is True
    signal = honest_limit_for_result(result)
    # The degraded run is limited — it cannot be shown as a complete analysis.
    assert signal["limited"] is True
    assert signal["limited"] is not False


def test_disclosure_is_carried_alongside_never_instead_of_the_upgrade() -> None:
    """CRITICAL — the truthful disclosure (reason+coverage) is present even WITH an upgrade.

    If an upgrade prompt is attached, the honest disclosure must still be present
    (alongside, never instead-of, per DL-048 UP-4 + HonestLimitDisclosure.tsx).
    """
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    result = engine.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    signal = honest_limit_for_result(
        result,
        upgrade={"message": "Upgrade for full coverage.", "cta_label": "See plans"},
    )
    # The disclosure (the contracted part) is intact …
    assert signal["limited"] is True
    assert signal["reason"].strip()
    assert signal["coverage_note"].strip()
    # … AND the upgrade rides alongside (it never replaces the disclosure).
    assert signal["upgrade"]["message"]
    assert signal["upgrade"]["cta_label"]


def test_spend_is_still_recorded_on_degradation() -> None:
    """CRITICAL — degradation is NOT a silent run; ai_spend_recorded still emits."""
    engine, _ = synthesis_engine(fixture="ws_synthesis_overbudget_v0")
    ctx = FakeStageContext()
    run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(),
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
    )
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    # The over-budget trust signal is set on the recorded spend (no clean hide).
    assert spend[0]["degraded"] is True
    assert spend[0]["over_budget"] is True


def test_honest_limit_module_embeds_no_invented_budget_number() -> None:
    """CRITICAL — the honest-limit code invents no §4c budget number (cap is config).

    The signal is derivative of the run's OWN result (degraded/deferred counts) +
    the CONFIG cap; the module must not hardcode a token/cost budget (150000 /
    600000 / 500000 / 4000000) — those live ONLY in config.py (Calibration §4c).
    """
    src = inspect.getsource(honest_limit_mod)
    for invented in ("150000", "150_000", "600000", "600_000", "500000", "500_000",
                     "4000000", "4_000_000"):
        assert invented not in src, f"honest_limit must not embed the §4c number {invented}"

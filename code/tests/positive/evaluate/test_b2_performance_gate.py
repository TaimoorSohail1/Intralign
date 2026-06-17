"""QA-WB-EVAL B2 — the PERFORMANCE GATE: Time-to-First-MRI < 60 s (DL-046 §F).

This asserts the RATIFIED <60s BOUND on the supported-project-size envelope. The
envelope VALUE (project size) and the p50/p95 distribution are owner-TBD
(A1/A2) — per ANTI_ASSUMPTION_BUILD_PROTOCOL this test does NOT invent them: it
runs the Fast-Pass Evaluate over a representative fixture envelope and asserts
only the <60s ceiling (the gate is scaffolded; the envelope number is the
owner's). The latency is also surfaced on the ``ai_spend_recorded`` event
(over-budget latency = trust signal).
"""

from __future__ import annotations

import time

from backend.responsibilities.evaluate.stage import run_evaluate_stage
from tests.positive.evaluate.helpers import (
    PROJECT,
    alignment_gap,
    conflict,
    coverage_gap,
    engine,
    risk,
    synthesized_model,
)
from tests.positive.synthesis.fakes import FakeStageContext

# The ratified Time-to-First-MRI ceiling (DL-046 / Master Spec §20 / M1). The
# ONLY owner-approved numeric target; assert the BOUND, not an invented envelope.
TIME_TO_FIRST_MRI_CEILING_SECONDS = 60.0


def _envelope_findings():
    """A representative Fast-Pass finding set (the supported envelope is owner-TBD)."""
    return [coverage_gap(), alignment_gap(), conflict(), risk()]


def test_b2_fast_pass_evaluate_under_60s_ceiling() -> None:
    ctx = FakeStageContext()
    started = time.perf_counter()
    run_evaluate_stage(
        engine=engine(mode="fast", confidence_stage="orientation"),
        project_id=PROJECT,
        findings=_envelope_findings(),
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
        model=synthesized_model(),
        mode="fast",
    )
    elapsed = time.perf_counter() - started
    # The RATIFIED bound (envelope value owner-TBD; only the ceiling is asserted).
    assert elapsed < TIME_TO_FIRST_MRI_CEILING_SECONDS


def test_b2_fast_pass_emits_time_to_first_mri_latency_within_ceiling() -> None:
    ctx = FakeStageContext()
    run_evaluate_stage(
        engine=engine(mode="fast"),
        project_id=PROJECT,
        findings=_envelope_findings(),
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
        model=synthesized_model(),
        mode="fast",
    )
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    latency_ms = spend[0]["time_to_first_mri_ms"]
    assert latency_ms >= 0
    assert latency_ms < TIME_TO_FIRST_MRI_CEILING_SECONDS * 1000.0

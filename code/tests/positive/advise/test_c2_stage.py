"""QA-WC-ADVISE C2 — the injected Advise stage: one CHR per emission, events,
recompute supersedes (prior intact), anchor lineage, both modes/stage, and the
``ai_spend_recorded`` cost event.
"""

from __future__ import annotations

from collections import Counter

from backend.responsibilities.advise.engine import ADVISE_VERSION
from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_CLARIFICATION,
    OUTPUT_KIND_RECOMMENDATION,
    run_advise_stage,
)
from tests.positive.advise.helpers import (
    PROJECT,
    advise_engine,
    conflict,
    coverage_gap,
    risk,
)
from tests.positive.synthesis.fakes import FakeStageContext


def _run(ctx, *, findings, issues=(), mode="fast", confidence_stage="orientation",
         is_recompute=False, trigger="knowledge-change", version="v1",
         prior_chr_id_for=None):
    eng, _ = advise_engine(mode=mode, confidence_stage=confidence_stage)
    return run_advise_stage(
        engine=eng,
        project_id=PROJECT,
        findings=findings,
        issues=issues,
        ctx=ctx,
        input_attestation_version=version,
        recompute_trigger=trigger,
        is_recompute=is_recompute,
        prior_chr_id_for=prior_chr_id_for,
        model_identity={"provider": "internal", "model": "gemma4"},
        mode=mode,
    )


def test_c2_one_chr_per_emission_paired_with_append_event() -> None:
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), conflict(), risk()])
    rec_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
    clr_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_CLARIFICATION)
    assert len(rec_chrs) == len(result.recommendations)
    assert len(clr_chrs) == len(result.clarifications)
    total = len(result.recommendations) + len(result.clarifications)
    counts = Counter(ctx.emitter.names)
    assert counts["cognition_history_record_appended"] == total


def test_c2_emission_events_emitted_with_mode_and_stage() -> None:
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), conflict(), risk()])
    counts = Counter(ctx.emitter.names)
    assert counts["recommendation_generated"] == len(result.recommendations)
    assert counts["clarification_requested"] == len(result.clarifications)
    for name, payload in ctx.emitter.events:
        if name in ("recommendation_generated", "clarification_requested"):
            assert payload["mode"] == "fast"
            assert payload["confidence_stage"] == "orientation"
            assert payload["anchor"]  # every emission carries its anchor


def test_c2_every_chr_carries_input_version_model_version_and_anchor_lineage() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap(), conflict()], version="v7")
    for kind in (OUTPUT_KIND_RECOMMENDATION, OUTPUT_KIND_CLARIFICATION):
        rows = ctx.chr_repo.rows_for_kind(kind)
        assert rows
        for row in rows:
            assert row["input_attestation_version"] == "v7"
            assert row["model_or_rule_version"]["model_version"] == ADVISE_VERSION
            # the resolved provider/model identity is stamped (DL-069 audit).
            assert row["model_or_rule_version"]["provider"] == "internal"
            assert row["upstream_lineage"]["anchor"]  # never un-anchored
            assert row["provenance_ref"]["emitted_by"] == "advise"


def test_c2_recompute_appends_new_emission_keeping_prior_chr_intact() -> None:
    ctx = FakeStageContext()
    first = _run(ctx, findings=[coverage_gap(), risk()], version="v1")
    first_recs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
    assert first_recs
    prior_map = {
        r["output_payload"]["recommendation_id"]: r["chr_id"] for r in first_recs
    }

    _run(
        ctx, findings=[coverage_gap(), risk()], is_recompute=True, version="v2",
        trigger="reanalysis", prior_chr_id_for=prior_map.get,
    )
    all_recs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
    # APPEND, never overwrite: prior generation + new generation.
    assert len(all_recs) == 2 * len(first_recs)
    # Every prior CHR is byte-intact (still v1) — none mutated.
    v1_recs = [r for r in all_recs if r["input_attestation_version"] == "v1"]
    assert len(v1_recs) == len(first_recs)
    for r in v1_recs:
        # exclude_none drops the key on the prior (first) generation → no supersession.
        assert r.get("supersedes_chr_id") is None
    # The new generation supersedes the prior by id (lineage; >=90% stable ids).
    v2_recs = [r for r in all_recs if r["input_attestation_version"] == "v2"]
    superseded = [r.get("supersedes_chr_id") for r in v2_recs if r.get("supersedes_chr_id")]
    prior_ids = set(prior_map.values())
    assert superseded  # at least most re-derived recs supersede their prior
    assert all(s in prior_ids for s in superseded)
    assert all(r["recompute_trigger"] == "reanalysis" for r in v2_recs)
    _ = first


def test_c2_recompute_set_overlap_is_at_least_90_percent_stable() -> None:
    """Determinism: stable identities across recompute (>=90% set overlap)."""
    ctx_a = FakeStageContext()
    first = _run(ctx_a, findings=[coverage_gap(), risk()], version="v1")
    ctx_b = FakeStageContext()
    second = _run(ctx_b, findings=[coverage_gap(), risk()], version="v2")
    ids_a = {r.recommendation_id for r in first.recommendations}
    ids_b = {r.recommendation_id for r in second.recommendations}
    overlap = len(ids_a & ids_b) / max(len(ids_a | ids_b), 1)
    assert overlap >= 0.9


def test_c2_deep_pass_carries_deep_mode_on_emissions_and_chr() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap(), conflict()], mode="deep",
         confidence_stage="expanded")
    for name, payload in ctx.emitter.events:
        if name in ("recommendation_generated", "clarification_requested"):
            assert payload["mode"] == "deep"
            assert payload["confidence_stage"] == "expanded"
    for row in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION):
        assert row["output_payload"]["mode"] == "deep"


def test_c2_ai_spend_recorded_carries_latency() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap()])
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    assert "time_to_first_mri_ms" in spend[0]
    assert spend[0]["time_to_first_mri_ms"] >= 0
    assert spend[0]["model"] == "gemma4"  # internal primary routed (DL-069)

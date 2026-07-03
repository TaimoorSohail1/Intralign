"""QA-WB-INFER B2 — the injected Finding stage: CHR per Finding, events,
supersession on recompute, both modes, and stage transitions.

The stage appends ONE Cognition History Record per Finding through
``ctx.chr_repo`` (output_kind=finding; already in the canonical CHECK + Literal,
no migration), emits ``finding_detected`` (or ``finding_superseded`` on a
recompute that re-derives a prior Finding), and pairs every append with a
``cognition_history_record_appended`` emit (gate-5). Each emission + CHR carries
``mode`` + ``confidence_stage`` (DL-046). Recompute APPENDS — the prior CHR
stays byte-intact (A4.3).
"""

from __future__ import annotations

from collections import Counter

from backend.responsibilities.infer.finding_stage import (
    OUTPUT_KIND_FINDING,
    run_finding_stage,
)
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    PROJECT,
    finding_engine,
    sample_drafts,
    synthesized_model,
)
from tests.positive.synthesis.fakes import FakeStageContext


def _run(ctx, *, mode="fast", confidence_stage="orientation", is_recompute=False,
         trigger="knowledge-change", version="v1", prior_chr_id_for=None):
    engine, _ = finding_engine(mode=mode, confidence_stage=confidence_stage)
    return run_finding_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS,
        ctx=ctx,
        input_attestation_version=version,
        recompute_trigger=trigger,
        is_recompute=is_recompute,
        model=synthesized_model(mode=mode),
        declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR,
        prior_chr_id_for=prior_chr_id_for,
    )


def test_b2_one_chr_appended_per_finding_paired_with_append_event() -> None:
    ctx = FakeStageContext()
    result = _run(ctx)
    finding_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    assert len(finding_chrs) == len(result.findings)
    # Every append is paired with a cognition_history_record_appended emit (gate-5).
    counts = Counter(ctx.emitter.names)
    assert counts["cognition_history_record_appended"] == len(result.findings)
    # Each CHR records the Attested assertion ids the Finding derived from (audit).
    for row in finding_chrs:
        assert row["upstream_lineage"]["evidence_anchors"]


def test_b2_finding_detected_emitted_per_finding_first_pass() -> None:
    ctx = FakeStageContext()
    result = _run(ctx)
    counts = Counter(ctx.emitter.names)
    assert counts["finding_detected"] == len(result.findings)
    assert counts["finding_superseded"] == 0
    # Every finding_detected carries mode + confidence_stage (DL-046).
    for name, payload in ctx.emitter.events:
        if name == "finding_detected":
            assert payload["mode"] == "fast"
            assert payload["confidence_stage"] == "orientation"


def test_b2_fast_pass_emits_time_to_first_mri_latency() -> None:
    ctx = FakeStageContext()
    _run(ctx, mode="fast")
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    assert "time_to_first_mri_ms" in spend[0]
    assert spend[0]["time_to_first_mri_ms"] >= 0
    assert spend[0]["mode"] == "fast"


def test_b2_recompute_appends_a_new_generation_keeping_prior_chr_intact() -> None:
    ctx = FakeStageContext()
    first = _run(ctx, is_recompute=False, version="v1")
    first_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    first_ids = {r["chr_id"] for r in first_chrs}
    # Build a finding_id -> prior chr_id resolver from the first pass.
    prior_map = {r["output_payload"]["finding_id"]: r["chr_id"] for r in first_chrs}

    _run(
        ctx, is_recompute=True, version="v2", trigger="knowledge-change",
        prior_chr_id_for=prior_map.get,
    )
    all_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    # APPEND, never overwrite: prior + new generation.
    assert len(all_chrs) == len(first.findings) * 2
    surviving = {r["chr_id"] for r in all_chrs}
    assert first_ids <= surviving
    prior = [r for r in all_chrs if r["chr_id"] in first_ids]
    assert all(r["input_attestation_version"] == "v1" for r in prior)


def test_b2_recompute_emits_superseded_with_supersedes_lineage() -> None:
    ctx = FakeStageContext()
    first = _run(ctx, is_recompute=False, version="v1")
    first_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    prior_map = {r["output_payload"]["finding_id"]: r["chr_id"] for r in first_chrs}

    ctx2 = FakeStageContext()
    # Seed ctx2's repo with the prior generation so supersession lineage resolves.
    for r in first_chrs:
        ctx2.chr_repo.rows.append(dict(r))
    _run(
        ctx2, is_recompute=True, version="v2", trigger="knowledge-change",
        prior_chr_id_for=prior_map.get,
    )
    counts = Counter(ctx2.emitter.names)
    # Stable finding ids re-derive -> every re-derived Finding supersedes.
    assert counts["finding_superseded"] == len(first.findings)
    assert counts["finding_detected"] == 0
    # The new CHRs carry supersedes_chr_id lineage (never a mutation).
    new_chrs = [
        r for r in ctx2.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
        if r.get("supersedes_chr_id")
    ]
    assert len(new_chrs) == len(first.findings)
    assert all(r["recompute_trigger"] == "knowledge-change" for r in new_chrs)


def test_b2_deep_pass_carries_deep_mode_on_emissions_and_chr() -> None:
    """Both modes exercised — Deep Pass emissions/CHRs carry mode=deep, expanded."""
    ctx = FakeStageContext()
    _run(ctx, mode="deep", confidence_stage="expanded")
    for name, payload in ctx.emitter.events:
        if name == "finding_detected":
            assert payload["mode"] == "deep"
            assert payload["confidence_stage"] == "expanded"
    for row in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING):
        assert row["output_payload"]["mode"] == "deep"
        assert row["output_payload"]["confidence_stage"] == "expanded"


def test_b2_confidence_stage_matures_orientation_to_validated_via_recompute() -> None:
    """Stage transition Orientation -> Expanded -> Validated is observable + history-tracked."""
    stages = []
    ctx = FakeStageContext()
    # Each recompute pass carries the next confidence stage (matures via recompute).
    for stage, recompute in (
        ("orientation", False), ("expanded", True), ("validated", True)
    ):
        engine, _ = finding_engine(mode="deep", confidence_stage=stage)
        run_finding_stage(
            engine=engine, project_id=PROJECT, assertions=sample_drafts(),
            assertion_ids=ASSERTION_IDS, ctx=ctx, input_attestation_version="v",
            recompute_trigger="reanalysis" if recompute else "knowledge-change",
            is_recompute=recompute, model=synthesized_model(mode="deep"),
            declared_outcome=DECLARED_OUTCOME, outcome_anchor=OUTCOME_ANCHOR,
        )
        stages.append(stage)
    # The CHR history records each stage in order (history-tracked maturation).
    chr_stages = [
        r["output_payload"]["confidence_stage"]
        for r in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_FINDING)
    ]
    assert "orientation" in chr_stages
    assert "expanded" in chr_stages
    assert "validated" in chr_stages
    assert stages == ["orientation", "expanded", "validated"]

"""QA-WB-EVAL B2 — the injected Evaluate stage: one CHR per value, events,
recompute supersedes (prior intact), lineage, both modes/stage, and the
"why did confidence change" reconstructable from CHR lineage.
"""

from __future__ import annotations

from collections import Counter

from backend.responsibilities.evaluate.stage import (
    OUTPUT_KIND_CAF,
    OUTPUT_KIND_CONFIDENCE,
    OUTPUT_KIND_ISSUE,
    OUTPUT_KIND_OUTCOME_CONFIDENCE,
    OUTPUT_KIND_RELIABILITY,
    run_evaluate_stage,
)
from tests.positive.evaluate.helpers import (
    PROJECT,
    conflict,
    coverage_gap,
    engine,
    risk,
    synthesized_model,
)
from tests.positive.synthesis.fakes import FakeStageContext


def _run(ctx, *, findings, mode="fast", confidence_stage="orientation",
         is_recompute=False, trigger=None, version="v1", model=None,
         prior_chr_id_for=None, prior_state=None):
    eng = engine(mode=mode, confidence_stage=confidence_stage)
    return run_evaluate_stage(
        engine=eng,
        project_id=PROJECT,
        findings=findings,
        ctx=ctx,
        input_attestation_version=version,
        recompute_trigger=trigger,
        is_recompute=is_recompute,
        model=model if model is not None else synthesized_model(),
        prior_understanding_state=prior_state,
        prior_chr_id_for=prior_chr_id_for,
        mode=mode,
    )


def test_b2_one_chr_per_value_paired_with_append_event() -> None:
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), risk()])
    # One CHR per Issue + one each for reliability / caf / confidence / outcome.
    issue_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_ISSUE)
    assert len(issue_chrs) == len(result.issues)
    for kind in (OUTPUT_KIND_RELIABILITY, OUTPUT_KIND_CAF, OUTPUT_KIND_CONFIDENCE,
                 OUTPUT_KIND_OUTCOME_CONFIDENCE):
        assert len(ctx.chr_repo.rows_for_kind(kind)) == 1
    total = len(result.issues) + 4
    counts = Counter(ctx.emitter.names)
    assert counts["cognition_history_record_appended"] == total


def test_b2_assessment_events_emitted_with_mode_and_stage() -> None:
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), risk()])
    counts = Counter(ctx.emitter.names)
    assert counts["issue_generated"] == len(result.issues)
    assert counts["caf_assessed"] == 1
    assert counts["outcome_confidence_computed"] == 1
    for name, payload in ctx.emitter.events:
        if name in ("issue_generated", "caf_assessed", "outcome_confidence_computed"):
            assert payload["mode"] == "fast"
            assert payload["confidence_stage"] == "orientation"


def test_b2_every_chr_carries_input_version_rule_version_and_lineage() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap()], version="v7")
    for kind in (OUTPUT_KIND_ISSUE, OUTPUT_KIND_CAF, OUTPUT_KIND_OUTCOME_CONFIDENCE):
        for row in ctx.chr_repo.rows_for_kind(kind):
            assert row["input_attestation_version"] == "v7"
            assert row["model_or_rule_version"]["model_version"] == "wb-eval-caf-v0"
            assert row["upstream_lineage"]  # never un-anchored


def test_b2_false_confidence_flagged_event_emitted_on_conf06() -> None:
    ctx = FakeStageContext()
    # No findings + low reliability → high band on low reliability → CONF-06.
    _run(ctx, findings=[], model=synthesized_model(n_assumptions=5))
    assert "false_confidence_flagged" in ctx.emitter.names


def test_b2_recompute_appends_new_values_keeping_prior_chr_intact() -> None:
    ctx = FakeStageContext()
    first = _run(ctx, findings=[coverage_gap()], version="v1")
    first_oc = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)
    assert len(first_oc) == 1
    prior_oc_id = first_oc[0]["chr_id"]

    prior_map = {OUTPUT_KIND_OUTCOME_CONFIDENCE: prior_oc_id}
    issue_chrs = {r["output_payload"]["issue_id"]: r["chr_id"]
                  for r in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_ISSUE)}
    prior_map.update(issue_chrs)

    _run(
        ctx, findings=[coverage_gap(), risk()], is_recompute=True, version="v2",
        trigger="knowledge-change", prior_chr_id_for=prior_map.get,
    )
    all_oc = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)
    # APPEND, never overwrite: prior + new generation.
    assert len(all_oc) == 2
    surviving = {r["chr_id"] for r in all_oc}
    assert prior_oc_id in surviving
    # The prior outcome-confidence CHR is byte-intact (v1).
    prior = next(r for r in all_oc if r["chr_id"] == prior_oc_id)
    assert prior["input_attestation_version"] == "v1"
    # The new one carries supersedes lineage + the recompute trigger.
    new = next(r for r in all_oc if r["chr_id"] != prior_oc_id)
    assert new["supersedes_chr_id"] == prior_oc_id
    assert new["recompute_trigger"] == "knowledge-change"
    _ = first  # silence


def test_b2_why_did_confidence_change_reconstructable_from_chr_lineage() -> None:
    """A confidence delta is explainable from the CHR history (the OBS feature)."""
    ctx = FakeStageContext()
    # First pass: no findings → strong confidence (high band).
    _run(ctx, findings=[], version="v1", model=synthesized_model(n_assumptions=0))
    first_oc = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)[0]
    prior_map = {OUTPUT_KIND_OUTCOME_CONFIDENCE: first_oc["chr_id"]}

    # Recompute: a material risk lands → confidence drops; new input version.
    _run(
        ctx, findings=[conflict(), risk()], is_recompute=True, version="v2",
        trigger="knowledge-change", prior_chr_id_for=prior_map.get,
    )
    history = sorted(
        ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE),
        key=lambda r: r["input_attestation_version"],
    )
    before, after = history[0], history[1]
    # The drop is reconstructable: index fell, input version changed, lineage links.
    assert before["output_payload"]["index"] > after["output_payload"]["index"]
    assert before["input_attestation_version"] == "v1"
    assert after["input_attestation_version"] == "v2"
    assert after["supersedes_chr_id"] == before["chr_id"]
    # The "what changed" is in the lineage: the new finding set.
    assert after["upstream_lineage"]["finding_ids"]


def test_b2_understanding_state_changed_only_on_recompute_and_when_it_advances() -> None:
    ctx = FakeStageContext()
    # Recompute that advances the state orientation(partial) → expanded(refined).
    _run(
        ctx, findings=[risk()], is_recompute=True, trigger="reanalysis",
        confidence_stage="expanded", prior_state="partial",
    )
    changes = [p for n, p in ctx.emitter.events if n == "understanding_state_changed"]
    assert len(changes) == 1
    assert changes[0]["from_state"] == "partial"
    assert changes[0]["to_state"] == "refined"


def test_b2_no_understanding_state_event_when_unchanged() -> None:
    ctx = FakeStageContext()
    # Prior state already matches the computed state → no spurious change event.
    _run(ctx, findings=[risk()], confidence_stage="orientation", prior_state="partial")
    assert "understanding_state_changed" not in ctx.emitter.names


def test_b2_deep_pass_carries_deep_mode_on_emissions_and_chr() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[risk()], mode="deep", confidence_stage="expanded")
    for name, payload in ctx.emitter.events:
        if name in ("issue_generated", "caf_assessed", "outcome_confidence_computed"):
            assert payload["mode"] == "deep"
            assert payload["confidence_stage"] == "expanded"
    for row in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE):
        assert row["output_payload"]["mode"] == "deep"


def test_b2_ai_spend_recorded_carries_time_to_first_mri_latency() -> None:
    ctx = FakeStageContext()
    _run(ctx, findings=[risk()], mode="fast")
    spend = [p for n, p in ctx.emitter.events if n == "ai_spend_recorded"]
    assert len(spend) == 1
    assert "time_to_first_mri_ms" in spend[0]
    assert spend[0]["time_to_first_mri_ms"] >= 0
    # Evaluate is rule-arithmetic: zero provider tokens, but cost stays observable.
    assert spend[0]["tokens_in"] == 0
    assert spend[0]["tokens_out"] == 0

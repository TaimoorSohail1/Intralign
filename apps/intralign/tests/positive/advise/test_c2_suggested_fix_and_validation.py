"""QA-WC-ADVISE C2 (DL-047 Additions) — SuggestedFix (REC-04) + Validation (REC-05).

DTM-0015, additive to DTM-0014:

- A **SuggestedFix** (REC-04) is generated as a Derived, Finding-anchored
  candidate edit to a NAMED artifact; it persists on the EXISTING
  ``recommendation`` CHR output_kind with a payload ``type=suggested_fix``
  discriminator (NO new kind), and ``suggested_fix_offered`` is emitted per fix.
- A **Validation** recommendation (REC-05) rides the ``recommendation`` output
  (``recommendation_type=validation``) → ``recommendation_generated``.

(The Critical "OSLO never autonomously writes a fix" negative is proven in the
negative suite — both AST/grep and behavioral.)
"""

from __future__ import annotations

from collections import Counter

from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_RECOMMENDATION,
    SUGGESTED_FIX_PAYLOAD_TYPE,
    run_advise_stage,
)
from shared.epistemic import EpistemicState, Recommendation, SuggestedFix
from tests.positive.advise.helpers import (
    COVERAGE_GAP_ID,
    PROJECT,
    RISK_ID,
    advise_engine,
    coverage_gap,
    risk,
)
from tests.positive.synthesis.fakes import FakeStageContext


# -- engine: SuggestedFix (REC-04) --------------------------------------------


def test_c2_suggested_fix_generated_derived_and_anchored_to_its_finding() -> None:
    engine, session = advise_engine()
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap(), risk()])
    assert result.suggested_fixes  # generated
    for fix in result.suggested_fixes:
        assert isinstance(fix, SuggestedFix)
        # ANCHORED to a real Finding — never standalone (REC-04).
        assert fix.anchor in (COVERAGE_GAP_ID, RISK_ID)
        # Names the artifact it proposes an edit FOR (a reference, not a write).
        assert fix.target_artifact
        assert fix.candidate_edit  # a proposed edit (AI-text)
        assert fix.epistemic_state == EpistemicState.DERIVED
        assert not fix.is_canonical
    assert session.call_count >= 1


def test_c2_suggested_fix_id_is_stable_for_same_structural_input() -> None:
    """Determinism: the SAME structural input re-derives the SAME fix id."""
    e1, _ = advise_engine()
    e2, _ = advise_engine()
    ids1 = {f.suggested_fix_id
            for f in e1.derive(project_id=PROJECT, findings=[coverage_gap()]).suggested_fixes}
    ids2 = {f.suggested_fix_id
            for f in e2.derive(project_id=PROJECT, findings=[coverage_gap()]).suggested_fixes}
    assert ids1 == ids2
    assert ids1  # at least one admitted


# -- engine: Validation (REC-05) ----------------------------------------------


def test_c2_validation_recommendation_rides_recommendation_with_type_validation() -> None:
    engine, _ = advise_engine()
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap(), risk()])
    validations = [
        r for r in result.recommendations if r.recommendation_type == "validation"
    ]
    assert validations  # generated
    for rec in validations:
        assert isinstance(rec, Recommendation)
        assert rec.anchor in (COVERAGE_GAP_ID, RISK_ID)  # anchored, never standalone
        assert rec.epistemic_state == EpistemicState.DERIVED
        assert rec.state == "generated"  # DL-055: not self-accepted


# -- stage: SuggestedFix persists on the existing 'recommendation' kind --------


def _run(ctx, *, findings, issues=(), is_recompute=False, trigger="knowledge-change",
         version="v1", prior_chr_id_for=None):
    eng, _ = advise_engine()
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
        mode="fast",
    )


def _fix_rows(ctx):
    return [
        r for r in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
        if r["output_payload"].get("type") == SUGGESTED_FIX_PAYLOAD_TYPE
    ]


def test_c2_suggested_fix_persists_on_recommendation_kind_with_type_discriminator() -> None:
    """REC-04 rides the EXISTING 'recommendation' output_kind — NO new kind."""
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), risk()])
    fix_rows = _fix_rows(ctx)
    assert len(fix_rows) == len(result.suggested_fixes)
    assert fix_rows  # something was offered
    for row in fix_rows:
        assert row["output_kind"] == "recommendation"  # NOT a new kind
        assert row["output_payload"]["type"] == "suggested_fix"
        assert row["output_payload"]["target_artifact"]
        assert row["output_payload"]["candidate_edit"]
        assert row["upstream_lineage"]["anchor"]  # never un-anchored
        assert row["provenance_ref"]["emitted_by"] == "advise"


def test_c2_suggested_fix_offered_emitted_one_per_fix() -> None:
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), risk()])
    counts = Counter(ctx.emitter.names)
    assert counts["suggested_fix_offered"] == len(result.suggested_fixes)
    assert counts["suggested_fix_offered"] >= 1
    for name, payload in ctx.emitter.events:
        if name == "suggested_fix_offered":
            assert payload["anchor"]
            assert payload["target_artifact"]
            assert payload["suggested_fix_id"]


def test_c2_validation_emitted_as_recommendation_generated_type_validation() -> None:
    """REC-05 rides recommendation_generated with recommendation_type=validation."""
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap(), risk()])
    validation_events = [
        p for n, p in ctx.emitter.events
        if n == "recommendation_generated" and p.get("recommendation_type") == "validation"
    ]
    assert validation_events
    for payload in validation_events:
        assert payload["anchor"]
        assert payload["state"] == "generated"


def test_c2_every_emission_pairs_with_a_chr_append_including_fixes() -> None:
    """One CHR append per emission — recommendations + clarifications + fixes."""
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap(), risk()])
    total = (
        len(result.recommendations)
        + len(result.clarifications)
        + len(result.suggested_fixes)
    )
    counts = Counter(ctx.emitter.names)
    assert counts["cognition_history_record_appended"] == total


def test_c2_suggested_fix_recompute_appends_keeping_prior_chr_intact() -> None:
    """Recompute appends a fresh fix CHR + supersedes by id; prior byte-intact."""
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap(), risk()], version="v1")
    first_fixes = _fix_rows(ctx)
    assert first_fixes
    prior_map = {
        r["output_payload"]["suggested_fix_id"]: r["chr_id"] for r in first_fixes
    }
    _run(
        ctx, findings=[coverage_gap(), risk()], is_recompute=True, version="v2",
        trigger="reanalysis", prior_chr_id_for=prior_map.get,
    )
    all_fixes = _fix_rows(ctx)
    assert len(all_fixes) == 2 * len(first_fixes)  # append, never overwrite
    v1 = [r for r in all_fixes if r["input_attestation_version"] == "v1"]
    assert len(v1) == len(first_fixes)
    for r in v1:
        assert r.get("supersedes_chr_id") is None  # prior generation intact
    v2 = [r for r in all_fixes if r["input_attestation_version"] == "v2"]
    superseded = [r.get("supersedes_chr_id") for r in v2 if r.get("supersedes_chr_id")]
    assert superseded
    assert all(s in set(prior_map.values()) for s in superseded)

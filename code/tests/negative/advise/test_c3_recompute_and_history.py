"""QA-WC-ADVISE C2 (negative) — only-recompute-changes + history-overwrite-impossible.

- a Recommendation changing WITHOUT recompute is impossible (the model is frozen;
  ``mode``/``confidence_stage`` change only on a re-derivation) — Critical.
- history OVERWRITE is impossible: the append-only repo has no mutation surface;
  a recompute APPENDS a superseding CHR and the prior stays byte-intact — Critical.
- Advise NEVER passes a bare dict to the repo (DTM-0013): it constructs a
  CognitionHistoryRecord MODEL (the append-only fake rejects a dict, mirroring
  the real repo).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.responsibilities.advise.stage import (
    OUTPUT_KIND_RECOMMENDATION,
    run_advise_stage,
)
from shared.epistemic import Recommendation
from tests.positive.advise.helpers import PROJECT, advise_engine, coverage_gap, risk
from tests.positive.synthesis.fakes import FakeStageContext


def _run(ctx, **kw):
    eng, _ = advise_engine()
    return run_advise_stage(
        engine=eng, project_id=PROJECT, ctx=ctx,
        model_identity={"provider": "internal", "model": "gemma4"}, **kw,
    )


def _recommendation_rows(ctx):
    """Recommendation CHRs excluding SuggestedFix rows (DTM-0015 rides the same
    'recommendation' output_kind with a payload type=suggested_fix)."""
    return [
        r for r in ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
        if r["output_payload"].get("type") != "suggested_fix"
    ]


def test_c3_recommendation_is_frozen_no_change_outside_recompute() -> None:
    """CRITICAL — a Recommendation cannot be mutated in place (frozen model).

    The only way mode/confidence_stage/state changes is a NEW derivation
    (recompute) producing a NEW record — never an in-place edit.
    """
    rec = Recommendation(
        project_id=PROJECT, recommendation_id="r",
        recommendation_type="suggested_action", anchor="finding-1",
        summary="x", model_or_rule_version="wc-advise-v0", mode="fast",
    )
    with pytest.raises(ValidationError):
        rec.confidence_stage = "validated"  # frozen → no in-place change
    with pytest.raises(ValidationError):
        rec.state = "accepted"
    with pytest.raises(ValidationError):
        rec.summary = "changed without recompute"


def test_c3_history_overwrite_is_impossible_recompute_appends() -> None:
    """CRITICAL — a recompute APPENDS; the prior CHR is byte-intact (never overwritten)."""
    ctx = FakeStageContext()
    _run(ctx, findings=[coverage_gap(), risk()],
         input_attestation_version="v1", recompute_trigger="knowledge-change",
         is_recompute=False)
    first_rows = _recommendation_rows(ctx)
    first_snapshot = {r["output_payload"]["recommendation_id"]: dict(r)
                      for r in first_rows}
    prior_map = {rid: r["chr_id"] for rid, r in first_snapshot.items()}

    _run(ctx, findings=[coverage_gap(), risk()],
         input_attestation_version="v2", recompute_trigger="reanalysis",
         is_recompute=True, prior_chr_id_for=prior_map.get)

    all_rows = _recommendation_rows(ctx)
    # Append-only: count strictly grew (no row replaced).
    assert len(all_rows) == 2 * len(first_rows)
    # Each original v1 row is still present, byte-for-byte (chr_id + payload).
    v1_rows = {r["output_payload"]["recommendation_id"]: r
               for r in all_rows if r["input_attestation_version"] == "v1"}
    for rid, original in first_snapshot.items():
        assert v1_rows[rid]["chr_id"] == original["chr_id"]
        assert v1_rows[rid]["output_payload"] == original["output_payload"]


def test_c3_append_only_fake_repo_has_no_mutation_surface() -> None:
    """The repo the advise stage writes through exposes append + read only."""
    ctx = FakeStageContext()
    for forbidden in ("update", "upsert", "delete", "overwrite", "set"):
        assert not hasattr(ctx.chr_repo, forbidden)


def test_c3_advise_stage_passes_a_model_not_a_dict_dtm0013() -> None:
    """DTM-0013 — the stage constructs a CHR MODEL; a bare dict would be rejected.

    The append-only fake raises TypeError on a dict (mirroring the real repo's
    record.model_dump). A successful run proves the stage passes a model.
    """
    ctx = FakeStageContext()
    result = _run(ctx, findings=[coverage_gap()],
                  input_attestation_version="v1",
                  recompute_trigger="knowledge-change", is_recompute=False)
    # No TypeError raised → the stage passed CognitionHistoryRecord models.
    assert ctx.chr_repo.rows_for_kind(OUTPUT_KIND_RECOMMENDATION)
    assert result.recommendations

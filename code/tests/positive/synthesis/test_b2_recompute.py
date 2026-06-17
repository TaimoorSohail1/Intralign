"""QA-WS-SYNTH B2 — user-edit -> new Attested input -> recompute -> supersede.

A user edit to a generated artifact is NOT an in-place mutation: it is a new
Attested input through the existing Retain admission path that triggers a 00R
recompute, which RE-SYNTHESIZES and supersedes the prior model/artifacts (live
replaced; history APPENDED — the prior CHR stays intact, A5/A4.3).

Here we exercise the Infer half: a recompute run over the SAME append-only CHR
repo appends a NEW generation of CHRs (it never overwrites the prior ones) and
emits ``planning_artifact_regenerated`` rather than ``..._generated``. The
"user edit admitted as a new Attested input" half lives in the Retain admission
path (DTM-0008) — this slice does not invent a new admission path (decision #5).
"""

from __future__ import annotations

from collections import Counter

from backend.responsibilities.infer.stage import (
    OUTPUT_KIND_PLANNING_ARTIFACT,
    OUTPUT_KIND_SYNTHESIZED_MODEL,
    run_synthesis_stage,
)
from tests.positive.synthesis.fakes import FakeStageContext
from tests.positive.synthesis.helpers import (
    PROJECT,
    sample_drafts,
    synthesis_engine,
)


def _ids() -> list[str]:
    return [f"assertion-{i}" for i in range(4)]


def _run(ctx, *, is_recompute, version, trigger=None):
    engine, _ = synthesis_engine()
    return run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=_ids(),
        ctx=ctx,
        input_attestation_version=version,
        recompute_trigger=trigger,
        is_recompute=is_recompute,
    )


def test_b2_recompute_appends_a_new_generation_keeping_the_prior_chr_intact() -> None:
    ctx = FakeStageContext()
    # First synthesis (the initial generation).
    _run(ctx, is_recompute=False, version="v1")
    first_artifact_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)
    first_ids = {r["chr_id"] for r in first_artifact_chrs}
    assert len(first_artifact_chrs) == 7

    # A recompute (the user edit was admitted as a new Attested input -> 00R).
    _run(ctx, is_recompute=True, version="v2", trigger="knowledge-change")

    all_artifact_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)
    all_model_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_SYNTHESIZED_MODEL)
    # APPEND, never overwrite: 7 prior + 7 new artifacts, 1 prior + 1 new model.
    assert len(all_artifact_chrs) == 14
    assert len(all_model_chrs) == 2
    # The prior CHRs are still present, byte-intact (append-only; hard rule #3).
    surviving = {r["chr_id"] for r in all_artifact_chrs}
    assert first_ids <= surviving
    prior = [r for r in all_artifact_chrs if r["chr_id"] in first_ids]
    assert all(r["input_attestation_version"] == "v1" for r in prior)


def test_b2_recompute_emits_regenerated_not_generated() -> None:
    ctx = FakeStageContext()
    _run(ctx, is_recompute=True, version="v2", trigger="knowledge-change")
    counts = Counter(ctx.emitter.names)
    assert counts["planning_artifact_regenerated"] == 7
    assert counts["planning_artifact_generated"] == 0
    # The recompute trigger is recorded on the appended CHRs (audit lineage).
    artifact_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)
    assert all(r["recompute_trigger"] == "knowledge-change" for r in artifact_chrs)

"""QA-WS-SYNTH B2 (Infer generation) — the seven Derived PlanningArtifact types,
each with a CHR appended per generation (A3.4; A6).

Generation produces the seven artifact types (Intent / Context / Scope /
Requirements / WBS / Resources / Schedule) from the model, each Derived
(``epistemic_state=derived``), each carrying lineage + the flagged assumptions
it relied on, and each paired with exactly one appended Cognition History
Record routed through the Retain-owned repo. The model+artifacts run as the
injected ``infer`` stage; ``planning_artifact_generated`` fires per artifact and
``cognition_history_record_appended`` pairs every append (gate-5).
"""

from __future__ import annotations

from collections import Counter

from shared.epistemic import (
    PLANNING_ARTIFACT_TYPES,
    EpistemicState,
    PlanningArtifact,
)
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


def _run_stage(*, is_recompute: bool = False, recompute_trigger=None):
    engine, session = synthesis_engine()
    ctx = FakeStageContext()
    drafts = sample_drafts()
    ids = [f"assertion-{i}" for i in range(len(drafts))]
    result = run_synthesis_stage(
        engine=engine,
        project_id=PROJECT,
        assertions=drafts,
        assertion_ids=ids,
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger=recompute_trigger,
        is_recompute=is_recompute,
    )
    return result, ctx, session


def test_b2_generation_produces_all_seven_derived_artifact_types() -> None:
    result, _, _ = _run_stage()
    produced = {a.artifact_type for a in result.artifacts}
    assert produced == set(PLANNING_ARTIFACT_TYPES)
    for a in result.artifacts:
        assert isinstance(a, PlanningArtifact)
        assert a.epistemic_state == EpistemicState.DERIVED
        assert a.is_canonical is False  # never Attested-as-truth (A4.2)
        assert a.project_id == PROJECT
        assert a.title and a.body
        # Artifact lineage: the assertions + the model version it was built from.
        assert a.derived_from_assertions
        assert a.synthesized_model_version == result.model.model_version


def test_b2_generation_appends_one_chr_per_generation() -> None:
    """A CHR is appended for the model AND for each of the seven artifacts."""
    result, ctx, _ = _run_stage()
    model_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_SYNTHESIZED_MODEL)
    artifact_chrs = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)
    assert len(model_chrs) == 1
    assert len(artifact_chrs) == 7
    # Each artifact CHR carries the contracted Wave-S output_kind + payload.
    for row in artifact_chrs:
        assert row["output_kind"] == OUTPUT_KIND_PLANNING_ARTIFACT
        assert row["output_payload"]["epistemic_state"] == "derived"
        assert row["input_attestation_version"] == "v1"
        assert "assertion_ids" in row["upstream_lineage"]


def test_b2_generation_pairs_every_append_with_its_event_gate5() -> None:
    result, ctx, _ = _run_stage()
    counts = Counter(ctx.emitter.names)
    # 1 model + 7 artifacts = 8 CHR appends, each paired with its append event.
    assert counts["cognition_history_record_appended"] == 8
    assert counts["planning_artifact_generated"] == 7
    assert counts["synthesized_model_updated"] == 1
    # Every emission carries the mode/stage attributes (decision #6).
    for name, payload in ctx.emitter.events:
        if name in ("planning_artifact_generated", "synthesized_model_updated"):
            assert payload["mode"] == "fast"
            assert payload["confidence_stage"] == "orientation"
            assert payload["understanding_state"] == "initial"


def test_b2_generation_runs_offline_zero_provider_calls() -> None:
    _, _, session = _run_stage()
    assert session.call_count == 8  # 1 synthesis + 7 generations, all recorded

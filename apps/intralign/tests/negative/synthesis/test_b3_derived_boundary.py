"""QA-WS-SYNTH B3 (generative boundary) — the Critical negatives that guard
Derived-not-Attested, no-silent-gap-fill, and immutable history.

Each is a Critical contract negative (A4.2/A4.3/A4.4):
- a generated model/artifact CANNOT be written as Attested-as-truth;
- an inferred assumption CANNOT pose as an evidence-attested fact (silent gap-fill);
- a generated artifact CANNOT be changed in place (frozen) — a change is a new
  generation via recompute, not a mutation;
- a Cognition History Record CANNOT be overwritten (the append-only repo has no
  mutation surface).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from shared.epistemic import (
    EpistemicState,
    FlaggedAssumption,
    PlanningArtifact,
    SynthesizedPlanningModel,
)
from backend.responsibilities.infer.stage import (
    OUTPUT_KIND_PLANNING_ARTIFACT,
    run_synthesis_stage,
)
from backend.responsibilities.retain import CognitionHistoryRecord
from tests.positive.synthesis.fakes import AppendOnlyFakeChrRepo, FakeStageContext
from tests.positive.synthesis.helpers import PROJECT, sample_drafts, synthesis_engine


def _chr(**overrides) -> CognitionHistoryRecord:
    """A valid CHR model (the real ChrRepository.append contract — DTM-0013)."""
    fields: dict = {
        "project_id": PROJECT,
        "output_kind": OUTPUT_KIND_PLANNING_ARTIFACT,
        "output_payload": {"body": "original"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"model_version": "v0"},
        "upstream_lineage": {},
        "recompute_trigger": "knowledge-change",
        "provenance_ref": {"emitted_by": "test"},
    }
    fields.update(overrides)
    return CognitionHistoryRecord(**fields)


def _artifact(**overrides):
    base = dict(
        project_id=PROJECT,
        artifact_type="scope",
        title="Scope",
        body="b",
        model_version="v",
        derived_from_assertions=("a",),
        synthesized_model_version="v",
        mode="fast",
    )
    base.update(overrides)
    return PlanningArtifact(**base)


def test_b3_generated_artifact_cannot_be_attested_as_truth() -> None:
    """CRITICAL — a PlanningArtifact is pinned Derived; Attested is rejected."""
    for attested in (
        EpistemicState.ATTESTED_EVIDENCE,
        EpistemicState.ATTESTED_OSLO,
        EpistemicState.ATTESTED_USER,
    ):
        with pytest.raises(ValidationError):
            _artifact(epistemic_state=attested)


def test_b3_synthesized_model_cannot_be_attested_as_truth() -> None:
    """CRITICAL — the SynthesizedPlanningModel is pinned Derived."""
    with pytest.raises(ValidationError):
        SynthesizedPlanningModel(
            project_id=PROJECT,
            model_version="v",
            intent_summary="i",
            scope_summary="s",
            derived_from_assertions=("a",),
            mode="fast",
            epistemic_state=EpistemicState.ATTESTED_OSLO,
        )


def test_b3_inferred_assumption_cannot_pose_as_attested_fact() -> None:
    """CRITICAL (silent gap-fill) — a FlaggedAssumption is pinned Derived."""
    with pytest.raises(ValidationError):
        FlaggedAssumption(
            statement="Headcount stays flat.",
            covers_gap="no staffing evidence",
            epistemic_state=EpistemicState.ATTESTED_EVIDENCE,
        )


def test_b3_generated_artifact_cannot_be_changed_in_place() -> None:
    """CRITICAL (change-without-recompute) — the artifact is frozen; mutation fails."""
    artifact = _artifact()
    with pytest.raises(ValidationError):
        artifact.body = "edited without recompute"  # type: ignore[misc]


def test_b3_synthesized_model_cannot_be_changed_in_place() -> None:
    model = SynthesizedPlanningModel(
        project_id=PROJECT,
        model_version="v",
        intent_summary="i",
        scope_summary="s",
        derived_from_assertions=("a",),
        mode="fast",
    )
    with pytest.raises(ValidationError):
        model.intent_summary = "mutated"  # type: ignore[misc]


def test_b3_chr_repo_has_no_overwrite_surface() -> None:
    """CRITICAL (CHR overwrite) — the append-only repo exposes no mutation method."""
    repo = AppendOnlyFakeChrRepo()
    for mutator in ("update", "delete", "upsert", "overwrite", "set", "replace"):
        assert not hasattr(repo, mutator)


def test_b3_appended_chr_cannot_be_overwritten_via_a_returned_row() -> None:
    """The returned record is independent — mutating it never touches storage.

    The real repo re-validates a NEW model from the stored row (independent of
    the persisted row); the fake mirrors that. Mutating the returned model's
    payload must not reach the stored row.
    """
    repo = AppendOnlyFakeChrRepo()
    persisted = repo.append(_chr(output_payload={"body": "original"}))
    persisted.output_payload["body"] = "tampered"
    stored = repo.rows_for_kind(OUTPUT_KIND_PLANNING_ARTIFACT)[0]
    assert stored["output_payload"]["body"] == "original"  # storage is intact


def test_b3_stage_appends_never_reduce_history_on_recompute() -> None:
    """CRITICAL — recompute APPENDS; the prior CHR count never shrinks."""
    engine, _ = synthesis_engine()
    ctx = FakeStageContext()
    ids = [f"a{i}" for i in range(4)]
    run_synthesis_stage(
        engine=engine, project_id=PROJECT, assertions=sample_drafts(),
        assertion_ids=ids, ctx=ctx, input_attestation_version="v1",
        recompute_trigger="knowledge-change", is_recompute=False,
    )
    before = len(ctx.chr_repo.rows)
    run_synthesis_stage(
        engine=engine, project_id=PROJECT, assertions=sample_drafts(),
        assertion_ids=ids, ctx=ctx, input_attestation_version="v2",
        recompute_trigger="knowledge-change", is_recompute=True,
    )
    assert len(ctx.chr_repo.rows) == before * 2  # appended, never replaced

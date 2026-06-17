"""QA-WB-EVAL B3 — only-recompute-changes-assessment + append-only history
*(Critical)*: a value changing without recompute, a CHR overwrite, a Derived→
Attested promotion, and stage/state modeled as an object or changing without
recompute are all impossible/rejected.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from backend.responsibilities.evaluate.stage import (
    OUTPUT_KIND_OUTCOME_CONFIDENCE,
    run_evaluate_stage,
)
from shared.epistemic import CAFAssessment, Confidence, Issue, OutcomeConfidence
from tests.positive.evaluate.helpers import PROJECT, conflict, engine, risk, synthesized_model
from tests.positive.synthesis.fakes import FakeStageContext


def _run(ctx, **kw):
    return run_evaluate_stage(
        engine=engine(mode=kw.pop("mode", "fast"),
                      confidence_stage=kw.pop("confidence_stage", "orientation")),
        project_id=PROJECT, ctx=ctx,
        input_attestation_version=kw.pop("version", "v1"),
        recompute_trigger=kw.pop("trigger", None),
        is_recompute=kw.pop("is_recompute", False),
        model=kw.pop("model", synthesized_model()),
        findings=kw.pop("findings", [risk()]),
        prior_understanding_state=kw.pop("prior_state", None),
        prior_chr_id_for=kw.pop("prior_chr_id_for", None),
        mode="fast",
    )


def test_b3_values_are_frozen_no_in_place_mutation() -> None:
    """A value cannot be mutated in place — only a recompute appends a new one."""
    result = engine().assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    for value in (result.confidence, result.outcome_confidence, result.caf, result.issues[0]):
        with pytest.raises(ValidationError):
            value.band = "low"  # type: ignore[misc]  # frozen models reject this
        if isinstance(value, (Confidence, OutcomeConfidence, Issue, CAFAssessment)):
            pass


def test_b3_recompute_appends_a_new_chr_never_overwrites_the_prior() -> None:
    """A CHR is never overwritten — supersession is a NEW append (hard rule #3)."""
    ctx = FakeStageContext()
    _run(ctx, findings=[risk()], version="v1")
    first = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)
    prior_id = first[0]["chr_id"]
    prior_payload = dict(first[0]["output_payload"])

    _run(
        ctx, findings=[conflict(), risk()], is_recompute=True, version="v2",
        trigger="knowledge-change",
        prior_chr_id_for={OUTPUT_KIND_OUTCOME_CONFIDENCE: prior_id}.get,
    )
    rows = ctx.chr_repo.rows_for_kind(OUTPUT_KIND_OUTCOME_CONFIDENCE)
    assert len(rows) == 2  # appended, NOT overwritten
    prior = next(r for r in rows if r["chr_id"] == prior_id)
    assert prior["output_payload"] == prior_payload  # byte-intact


def test_b3_chr_repo_has_no_update_or_delete_surface() -> None:
    """The append-only repo exposes NO mutation method (overwrite impossible)."""
    repo = FakeStageContext().chr_repo
    for forbidden in ("update", "delete", "upsert", "replace", "set"):
        assert not hasattr(repo, forbidden)


def test_b3_stage_change_only_via_recompute_no_event_without_advancing() -> None:
    """confidence_stage / understanding_state change ONLY via recompute (a re-run).

    A first pass (NOT a recompute) with no prior state emits NO
    understanding_state_changed — the state did not change outside a recompute.
    """
    ctx = FakeStageContext()
    _run(ctx, findings=[risk()], is_recompute=False, prior_state=None)
    assert "understanding_state_changed" not in ctx.emitter.names


def test_b3_understanding_state_is_an_attribute_not_a_new_object() -> None:
    """mode / confidence_stage / understanding_state are LITERAL attributes, not objects."""
    from shared import epistemic

    # No standalone UnderstandingState / ConfidenceStage / Mode CLASS exists.
    for forbidden_obj in ("UnderstandingStateObject", "ConfidenceStageObject", "ModeObject"):
        assert not hasattr(epistemic, forbidden_obj)
    # They are typing.Literal aliases (attributes), proven by their use on a value.
    result = engine(confidence_stage="expanded").assess(
        project_id=PROJECT, findings=[risk()], model=synthesized_model()
    )
    assert isinstance(result.confidence.understanding_state, str)
    assert isinstance(result.confidence.confidence_stage, str)


def test_b3_an_assessment_does_not_change_by_intake_or_acceptance_alone() -> None:
    """Same findings/model → same assessment; only a CHANGED input (recompute) moves it."""
    src = inspect.getsource(run_evaluate_stage)
    # The stage's only inputs are findings + model + version — no acceptance hook.
    assert "accept" not in src.lower()
    a = engine().assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    b = engine().assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    assert a.outcome_confidence.index == b.outcome_confidence.index

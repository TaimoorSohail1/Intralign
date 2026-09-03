"""QA-WS-SYNTH B2 — the PS-03 Understanding-Evaluation seed seam is exercised.

Evaluate (DTM-0011) seeds its initial CAF/Confidence FROM the
``SynthesizedPlanningModel`` (PS-03). Evaluate is not built in this slice, so the
seam under test is the DATA CONTRACT: the synthesized model surfaces exactly the
shape an Evaluate seed consumes — a Derived interpretation with intent/scope, the
Attested lineage it derived from, the flagged assumptions (the basis a Confidence
"reduces to"), and the mode/confidence_stage attributes. This slice introduces NO
Evaluate producer (one producer per output) — it only proves the seed is readable.
"""

from __future__ import annotations

from shared.epistemic import EpistemicState
from tests.positive.synthesis.helpers import (
    PROJECT,
    sample_drafts,
    synthesis_engine,
)


def _model():
    engine, _ = synthesis_engine()
    return engine.synthesize_and_generate(
        project_id=PROJECT,
        assertions=sample_drafts(),
        assertion_ids=[f"assertion-{i}" for i in range(4)],
    ).model


def test_ps03_seed_seam_exposes_the_fields_evaluate_consumes() -> None:
    model = _model()
    # A Derived interpretation Evaluate can seed CAF/Confidence from.
    assert model.epistemic_state == EpistemicState.DERIVED
    assert model.intent_summary
    assert model.scope_summary
    # The Attested basis (lineage) — a Confidence reduces to its basis.
    assert model.derived_from_assertions
    # The flagged assumptions are the explicit uncertainty an Evaluate seed reads.
    assert model.flagged_assumptions
    # The mode/stage attributes carry into the Evaluate seed (decision #6).
    assert model.mode == "fast"
    assert model.confidence_stage == "orientation"
    assert model.understanding_state == "initial"


def test_ps03_seed_seam_carries_no_evaluate_output() -> None:
    """The seam is read-only for Evaluate: synthesis emits NO Confidence/CAF/Issue."""
    model = _model()
    dumped = model.model_dump()
    for evaluate_owned in ("confidence", "caf", "issue", "outcome_confidence", "score"):
        assert evaluate_owned not in dumped

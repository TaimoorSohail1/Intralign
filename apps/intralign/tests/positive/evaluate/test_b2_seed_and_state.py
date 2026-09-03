"""QA-WB-EVAL B2 — PS-03 seed from the SynthesizedPlanningModel + AE-04
understanding-state classification (Initial → Partial → Refined → Validated →
Mature), changing ONLY via recompute (a stage carries it).
"""

from __future__ import annotations

from tests.positive.evaluate.helpers import (
    PROJECT,
    conflict,
    coverage_gap,
    engine,
    risk,
    synthesized_model,
)


def test_b2_ps03_seeds_confidence_from_the_synthesized_model() -> None:
    """PS-03 — the model is Evaluate's seed input; its basis surfaces in Confidence."""
    eng = engine()
    model = synthesized_model(n_assumptions=2)
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=model)
    # The seed model is recorded in the basis (the audit lineage of the seed).
    assert any("seeded_from_model=ws-synth-llm-v0" in b for b in result.confidence.basis)
    # The model's assumptions feed the reliability qualifier (PS-03 seed signal).
    assert result.reliability.level in ("low", "moderate")


def test_b2_ps03_without_a_model_cannot_be_past_initial() -> None:
    eng = engine()
    result = eng.assess(project_id=PROJECT, findings=[coverage_gap()], model=None)
    # Never Unknown → Final-Truth: with no model we are still Initial.
    assert result.understanding_state == "initial"


def test_b2_understanding_state_orientation_with_model_is_partial() -> None:
    eng = engine(confidence_stage="orientation")
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    assert result.understanding_state == "partial"


def test_b2_understanding_state_expanded_stage_is_refined() -> None:
    eng = engine(confidence_stage="expanded")
    result = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    assert result.understanding_state == "refined"


def test_b2_understanding_state_validated_stage_matures() -> None:
    # Validated stage, no unresolved conflict → Mature.
    eng = engine(confidence_stage="validated")
    mature = eng.assess(project_id=PROJECT, findings=[risk()], model=synthesized_model())
    assert mature.understanding_state == "mature"
    # Validated stage WITH an unresolved conflict → Validated (not yet Mature).
    validated = eng.assess(
        project_id=PROJECT, findings=[conflict()], model=synthesized_model()
    )
    assert validated.understanding_state == "validated"


def test_b2_state_progression_matures_across_stages_never_skipping_to_truth() -> None:
    """The state advances Initial→Partial→Refined→Mature as the stage matures."""
    states = []
    for stage in ("orientation", "expanded", "validated"):
        eng = engine(confidence_stage=stage)
        states.append(
            eng.assess(
                project_id=PROJECT, findings=[risk()], model=synthesized_model()
            ).understanding_state
        )
    assert states == ["partial", "refined", "mature"]
    # Never an Unknown → Final-Truth jump.
    assert "final" not in states

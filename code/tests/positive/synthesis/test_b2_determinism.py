"""QA-WS-SYNTH B2 (determinism tiers) — explicit attributions EXACT, AI-synthesized
content SEMANTIC-equivalent, set-level >=90% stable sections.

Determinism tier (QA §2; decision #10): extraction of EXPLICIT attributions is
exact-if-rule (byte-identical across runs over the same fixture); AI-synthesized
model/artifacts are semantic-equivalence (same plan identity/intent — here the
same artifact-type identity set and the same model version), with set-level
>=90% stable-identity overlap of generated sections. Driven entirely by the
recorded fixture (the model-version x fixture baseline component), so CI is
offline-deterministic.
"""

from __future__ import annotations

from shared.epistemic import PLANNING_ARTIFACT_TYPES
from tests.positive.synthesis.helpers import (
    ARTIFACT,
    PROJECT,
    SAMPLE,
    SOURCE,
    extractor_session,
    sample_drafts,
    synthesis_engine,
)


def _ids() -> list[str]:
    return [f"assertion-{i}" for i in range(4)]


def _extract_propositions() -> list[tuple[str, str]]:
    extractor, _ = extractor_session()
    drafts = extractor.extract(
        artifact_id=ARTIFACT,
        normalized_form={"text": SAMPLE, "sections": [{"index": 0, "lines": SAMPLE.splitlines()}]},
        attesting_source=SOURCE,
    )
    return [(d.content_type, d.proposition) for d in drafts]


def test_explicit_attribution_extraction_is_byte_identical_across_runs() -> None:
    """EXACT tier: the same fixture yields byte-identical typed propositions."""
    first = _extract_propositions()
    second = _extract_propositions()
    assert first == second  # exact, in order


def test_synthesized_content_is_semantically_stable_across_runs() -> None:
    """SEMANTIC tier: same plan identity/intent (model version + section identities)."""
    engine_a, _ = synthesis_engine()
    engine_b, _ = synthesis_engine()
    a = engine_a.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    b = engine_b.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    )
    # Same plan identity: same model version + same intent/scope summaries.
    assert a.model.model_version == b.model.model_version
    assert a.model.intent_summary == b.model.intent_summary
    assert a.model.scope_summary == b.model.scope_summary


def test_generated_section_set_is_at_least_90_percent_stable() -> None:
    """Set-level >=90% stable-identity overlap of generated sections (decision #10)."""
    engine_a, _ = synthesis_engine()
    engine_b, _ = synthesis_engine()
    types_a = {a.artifact_type for a in engine_a.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    ).artifacts}
    types_b = {a.artifact_type for a in engine_b.synthesize_and_generate(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=_ids()
    ).artifacts}
    overlap = len(types_a & types_b) / len(set(PLANNING_ARTIFACT_TYPES))
    assert overlap >= 0.90
    assert types_a == types_b  # the recorded baseline is fully stable here


def test_determinism_baseline_is_stamped_on_the_fixture() -> None:
    """The fixture carries the model_version baseline stamp (DT-5/DT-10)."""
    _, session = synthesis_engine()
    assert session.fixture.model_version
    assert session.fixture.config

"""QA-WA-001 B3 negative suite — each forbidden behavior PROVABLY impossible.

Structural impossibility is shown by introspection/AST where the contract is
structural (B3.1/B3.2/B3.3/B3.5/B3.7) and by runtime rejection where it is
behavioral (B3.4/B3.6). Pure — never skips. (DB-level enforcement for the
artifact anchor is proven live in test_artifact_append_only_live.py.)
"""

from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

import pydantic
import pytest

import backend.responsibilities.perceive.acceptance_capture as acceptance_capture
import backend.responsibilities.perceive.extraction as extraction
import backend.responsibilities.perceive.intake as intake
import backend.responsibilities.perceive.staleness as staleness
from backend.responsibilities.perceive.acceptance_capture import (
    AcceptanceCapture,
    capture_acceptance,
)
from backend.responsibilities.perceive.extraction import (
    AssertionDraft,
    RuleBasedExtractor,
)
from backend.responsibilities.perceive.intake import (
    AttributionMissingError,
    submit_artifact,
)
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.perceive_intake.fakes import (
    DuplicateDedupKeyError,
    InMemoryBodyStore,
    InMemoryIntakeStore,
)

PROJECT = "11111111-1111-1111-1111-111111111111"
PERCEIVE_MODULES = (intake, extraction, acceptance_capture, staleness)
PERCEIVE_DIR = Path(inspect.getfile(intake)).parent


def _submission(**overrides) -> dict:
    fields = {
        "project_id": PROJECT,
        "source": "evidence-source-7",
        "submitted_by": "user-42",
        "content": "The deadline is 2026-09-01.\n",
    }
    return {**fields, **overrides}


# --- B3.1 upload != Attested -------------------------------------------------


def test_b3_1_intake_writes_no_attested_assertion_row() -> None:
    """Upload is never canonical-as-true: intake touches ONLY the artifact
    anchor + the candidate — no attested_assertion, no admission (Retain's)."""
    store, bodies = InMemoryIntakeStore(), InMemoryBodyStore()
    submit_artifact(_submission(), store=store, bodies=bodies)
    assert set(store.tables_written) == {"artifact", "promotion_candidate"}
    assert "attested_assertion" not in store.tables_written


def test_b3_1_perceive_never_imports_the_retain_writer() -> None:
    """Structural: no perceive module can reach ChrRepository/retain writes."""
    for py_file in sorted(PERCEIVE_DIR.glob("*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "retain" not in (node.module or ""), (
                    f"{py_file.name} imports from retain — admission is "
                    "Retain's own step (A4.1)"
                )
            if isinstance(node, ast.Import):
                assert not any("retain" in a.name for a in node.names)


# --- B3.2 no cognition surface ----------------------------------------------

_COGNITION_NAME = re.compile(
    r"finding|issue|confidence|recommendation|clarification|severity|assessment",
    re.IGNORECASE,
)


def test_b3_2_perceive_exports_no_cognition_producer() -> None:
    for module in PERCEIVE_MODULES:
        offenders = [n for n in dir(module) if _COGNITION_NAME.search(n)]
        assert offenders == [], (
            f"{module.__name__} exposes cognition-shaped surface {offenders} "
            "— Perceive never infers/evaluates/advises (A4.2; DL-047)"
        )


def test_b3_2_drafts_carry_no_score_fields_and_reject_extras() -> None:
    field_names = set(AssertionDraft.model_fields)
    assert field_names == {
        "content_type",
        "proposition",
        "attesting_source",
        "source_ref",
        "re_derivable",
        "epistemic_state",
    }
    with pytest.raises(pydantic.ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="x.",
            attesting_source="s",
            source_ref={},
            severity="high",  # closed shape: extra='forbid'
        )
    with pytest.raises(pydantic.ValidationError):
        AssertionDraft(
            content_type="fact",
            proposition="x.",
            attesting_source="s",
            source_ref={},
            confidence=0.9,
        )


# --- B3.3 no governance/authorization step (none exists in R1) ----------------


def test_b3_3_no_authorization_surface_anywhere_in_perceive() -> None:
    pattern = re.compile(r"authoriz|governance_decision", re.IGNORECASE)
    for py_file in sorted(PERCEIVE_DIR.glob("*.py")):
        source = py_file.read_text(encoding="utf-8")
        assert not pattern.search(source), (
            f"{py_file.name} mentions an authorization step — no such step "
            "exists in R1 (A4.3; gate-4 backstops the token scan)"
        )
    for module in PERCEIVE_MODULES:
        assert not [n for n in dir(module) if pattern.search(n)]


# --- B3.4 capture-not-accept ---------------------------------------------------


def test_b3_4_capture_marks_nothing_true_or_approved() -> None:
    emitter = CollectingEventEmitter()
    capture = capture_acceptance(
        {
            "user_id": "user-42",
            "target_kind": "recommendation",
            "version_pin": "33333333-3333-3333-3333-333333333333",
            "action": "accept",
        },
        emitter=emitter,
    )
    # The handoff shape CANNOT carry a truth/approval marker.
    assert set(AcceptanceCapture.model_fields) == {
        "user_id",
        "target_kind",
        "version_pin",
        "action",
        "project_id",
        "captured_at",
    }
    with pytest.raises(pydantic.ValidationError):
        AcceptanceCapture(
            user_id="u",
            target_kind="finding",
            version_pin="v",
            action="accept",
            captured_at=capture.captured_at,
            approved=True,  # extra='forbid'
        )
    # Frozen: even the captured action cannot be flipped after the fact.
    with pytest.raises(pydantic.ValidationError):
        capture.action = "reject"  # type: ignore[misc]
    # Capture emits its event and ONLY its event — no admission, no marking.
    assert emitter.names == ["user_acceptance_captured"]


def test_b3_4_perceive_writes_no_user_acceptance_record() -> None:
    """The UAR row is Retain's (DTM-0008): capture has no store seam at all."""
    assert "store" not in inspect.signature(capture_acceptance).parameters
    for py_file in sorted(PERCEIVE_DIR.glob("*.py")):
        assert "user_acceptance_record" not in py_file.read_text(encoding="utf-8")


# --- B3.5 no assessment change from intake -------------------------------------


def test_b3_5_perceive_never_calls_into_orchestration() -> None:
    """Static: intake constructs the TriggerClaim but can NEVER run it —
    no orchestration import, no submit_trigger/invoke call (A4.5/A9)."""
    forbidden_calls = {"submit_trigger", "invoke", "run"}
    for py_file in sorted(PERCEIVE_DIR.glob("*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names]
                module = getattr(node, "module", "") or ""
                assert "orchestration" not in module, f"{py_file.name}: {module}"
                assert not any("orchestration" in n for n in names)
            if isinstance(node, ast.Call):
                name = (
                    node.func.attr
                    if isinstance(node.func, ast.Attribute)
                    else node.func.id
                    if isinstance(node.func, ast.Name)
                    else None
                )
                assert name not in forbidden_calls, (
                    f"{py_file.name}:{node.lineno} calls {name} — intake alone "
                    "never changes assessment (A4.5)"
                )


def test_b3_5_intake_emits_no_recompute_events() -> None:
    """Behavioral: a full intake run emits intake events ONLY — nothing from
    the recompute vocabulary appears (only recompute changes assessment)."""
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    submit_artifact(_submission(), store=store, bodies=bodies, emitter=emitter)
    submit_artifact(
        _submission(content="changed content.\n"),
        store=store,
        bodies=bodies,
        emitter=emitter,
    )
    recompute_events = {
        "recompute_started",
        "recompute_completed",
        "recompute_failed",
        "reanalysis_triggered",
        "cognition_history_record_appended",
        "state_transition_occurred",
    }
    assert not recompute_events & set(emitter.names)


# --- B3.6 provenance mandatory; idempotency enforced ---------------------------


@pytest.mark.parametrize("missing_field", ["submitted_by", "source", "project_id"])
def test_b3_6_submission_without_attribution_is_rejected(missing_field: str) -> None:
    store, bodies, emitter = InMemoryIntakeStore(), InMemoryBodyStore(), CollectingEventEmitter()
    with pytest.raises(AttributionMissingError):
        submit_artifact(
            _submission(**{missing_field: "   "}),
            store=store,
            bodies=bodies,
            emitter=emitter,
        )
    # Rejected BEFORE anything moved: nothing stored, nothing emitted.
    assert store.artifacts == []
    assert store.candidates == []
    assert bodies.objects == {}
    assert emitter.events == []


def test_b3_6_non_idempotent_admission_is_impossible() -> None:
    """Double admission of the same dedup_key cannot happen: the pipeline
    short-circuits, and the store's UNIQUE constraint backstops it."""
    store, bodies = InMemoryIntakeStore(), InMemoryBodyStore()
    first = submit_artifact(_submission(), store=store, bodies=bodies)
    again = submit_artifact(_submission(), store=store, bodies=bodies)
    assert again.created is False
    assert len(store.artifacts) == 1
    # Even bypassing the pipeline, the constraint refuses a second admission.
    with pytest.raises(DuplicateDedupKeyError):
        store.save_artifact({**store.artifacts[0], "dedup_key": first.dedup_key})


# --- B3.7 inferred-as-Attested impossible --------------------------------------


def test_b3_7_a_draft_cannot_claim_derived_content() -> None:
    """epistemic_state is Literal-pinned: 'derived' (or anything else) is a
    validation error — Perceive carries only evidence-attested drafts (A4.7)."""
    base = {
        "content_type": "fact",
        "proposition": "x.",
        "attesting_source": "evidence-source-7",
        "source_ref": {"artifact_id": "a", "locus": {"section": 0, "line": 0}},
    }
    with pytest.raises(pydantic.ValidationError):
        AssertionDraft(**base, epistemic_state="derived")
    with pytest.raises(pydantic.ValidationError):
        AssertionDraft(**base, epistemic_state="attested-oslo")  # never self-attested
    with pytest.raises(pydantic.ValidationError):
        AssertionDraft(**base, re_derivable=False)  # re-derivability is pinned too


def test_b3_7_extractor_output_is_always_evidence_attested() -> None:
    from backend.responsibilities.perceive.intake import normalize_content

    drafts = RuleBasedExtractor().extract(
        artifact_id="a",
        normalized_form=normalize_content("- It must hold.\n- It depends on X.\n"),
        attesting_source="evidence-source-7",
    )
    assert drafts
    assert {d.epistemic_state for d in drafts} == {"attested-evidence"}
    assert all(d.re_derivable is True for d in drafts)

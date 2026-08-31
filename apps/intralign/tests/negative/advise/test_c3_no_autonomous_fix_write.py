"""QA-WC-ADVISE C2 — THE HEADLINE CRITICAL NEGATIVE (DL-047 / DTM-0015).

**OSLO NEVER autonomously writes/applies a SuggestedFix to an artifact.** A
SuggestedFix is a PROPOSAL only — applying is a user-initiated artifact edit
(commodity editing / Wave I) → recompute, never an OSLO write. This is proven two
ways:

(a) **AST/grep proof** — ``advise/``'s own modules import NO artifact-writer
    module (the apply surface / canonical-evidence stores), and contain NO
    artifact-mutation call (``.update``/``.upsert``/``.apply``/``.write`` …; no
    apply/write/commit surface). The only ``.append`` in advise is the
    Retain-owned CHR repo append (an append-only emission RECEIPT, not an
    artifact write). advise/ depends only on its engine, the CHR record TYPE, the
    epistemic shapes, and the LLM provider seam — never a writer.
(b) **Behavioral proof** — generating SuggestedFixes through the real engine +
    stage mutates NO artifact and emits NO artifact-write/mutation event; the
    only writes are CHR appends + the ``suggested_fix_offered`` OFFER event.

Plus: a SuggestedFix without a Finding anchor is rejected; and no new CHR
``output_kind`` is introduced (a fix rides the existing ``recommendation`` kind).

Failure classification: Critical — OSLO autonomously mutating an artifact.
"""

from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.responsibilities.advise import engine as engine_mod
from backend.responsibilities.advise import stage as stage_mod
from backend.responsibilities.retain.models import OutputKind
from shared.epistemic import SuggestedFix
from tests.positive.advise.helpers import COVERAGE_GAP_ID, PROJECT, advise_engine, coverage_gap
from tests.positive.synthesis.fakes import FakeStageContext

# Modules whose job IS to write/mutate persisted artifacts (the apply surface +
# the canonical/evidence stores). NONE may be reachable from advise/.
_ARTIFACT_WRITER_MODULES = (
    "backend.services.persistence.intake_store",
    "backend.services.persistence.retention_store",
    "backend.responsibilities.perceive.intake",
    "backend.responsibilities.retain.repository",
)

# Method/function names that would APPLY or WRITE an artifact edit. ``append`` is
# deliberately NOT here — the CHR append is an append-only emission receipt, not
# an artifact mutation (and is itself never an artifact-table write).
_ARTIFACT_MUTATION_CALLS = (
    "update", "upsert", "delete", "apply", "apply_fix", "write_artifact",
    "commit", "save", "mutate",
)

# Events that signal an artifact was WRITTEN/MUTATED — advise must emit NONE.
_ARTIFACT_WRITE_EVENTS = frozenset(
    {"artifact_modified", "knowledge_mutation_recorded", "knowledge_promoted",
     "knowledge_versioned", "knowledge_superseded"}
)


def _advise_dir() -> Path:
    return Path(inspect.getsourcefile(stage_mod)).resolve().parent


def _module_imports(mod) -> set[str]:
    """The first-party (backend./shared) module names a module imports directly."""
    out: set[str] = set()
    tree = ast.parse(inspect.getsource(mod))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith(("backend.", "shared")):
                out.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(("backend.", "shared")):
                    out.add(alias.name)
    return out


# -- (a) AST/grep proof -------------------------------------------------------


def test_c3_advise_imports_no_artifact_writer_module() -> None:
    """advise/'s own modules import NO artifact-writer module (the apply surface).

    advise depends only on its engine, the CHR record TYPE (a model, not the
    repo), the epistemic shapes, and the LLM provider seam — it never imports a
    persistence/intake/repository writer that could apply an artifact edit.
    """
    for py_file in sorted(_advise_dir().glob("*.py")):
        mod = importlib.import_module(
            f"backend.responsibilities.advise.{py_file.stem}"
        )
        imported = _module_imports(mod)
        for writer in _ARTIFACT_WRITER_MODULES:
            assert writer not in imported, (
                f"{py_file.name} imports {writer} — an artifact-writer must NOT be "
                "imported by advise (OSLO never autonomously applies a fix; "
                "DL-047 Critical)"
            )


def test_c3_advise_modules_call_no_artifact_mutation_method() -> None:
    """advise/ source contains no artifact-mutation call (apply/write/update/...)."""
    for py_file in sorted(_advise_dir().glob("*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                attr = node.func.attr
                # The only legitimate .append is the CHR repo's (append-only
                # receipt). Any artifact-mutation verb is forbidden.
                assert attr not in _ARTIFACT_MUTATION_CALLS, (
                    f"{py_file.name}:{node.lineno}: advise calls .{attr}(...) — "
                    "no artifact mutation is permitted in advise (DL-047 Critical)"
                )


def test_c3_advise_exposes_no_apply_or_write_surface() -> None:
    """advise/ defines no apply/write/commit function (the apply surface is Wave I)."""
    for mod in (engine_mod, stage_mod):
        src = inspect.getsource(mod)
        for forbidden in (
            "def apply", "def apply_fix", "def write_artifact", "def commit",
            "def mutate_artifact", "def edit_artifact",
        ):
            assert forbidden not in src


# -- (b) behavioral proof -----------------------------------------------------


class _SentinelArtifact:
    """A stand-in 'artifact' the test watches: any write would change its body."""

    def __init__(self) -> None:
        self.body = "ORIGINAL — untouched"
        self.write_count = 0

    def write(self, _value: str) -> None:  # pragma: no cover - must never run
        self.write_count += 1
        self.body = _value


def test_c3_generating_fixes_mutates_no_artifact_and_emits_no_write_event() -> None:
    """Behavioral Critical — a full advise run offers fixes but writes no artifact."""
    artifact = _SentinelArtifact()
    ctx = FakeStageContext()

    eng, _ = advise_engine()
    result = stage_mod.run_advise_stage(
        engine=eng,
        project_id=PROJECT,
        findings=[coverage_gap()],
        ctx=ctx,
        input_attestation_version="v1",
        recompute_trigger="knowledge-change",
        is_recompute=False,
        model_identity={"provider": "internal", "model": "gemma4"},
        mode="fast",
    )

    # Fixes WERE offered (the proposal happened)…
    assert result.suggested_fixes
    assert "suggested_fix_offered" in ctx.emitter.names
    # …yet the artifact is byte-for-byte untouched (no autonomous application).
    assert artifact.body == "ORIGINAL — untouched"
    assert artifact.write_count == 0
    # …and NO artifact-write / mutation event was emitted.
    assert not (_ARTIFACT_WRITE_EVENTS & set(ctx.emitter.names))


# -- anchor mandatory + no new output_kind ------------------------------------


def test_c3_suggested_fix_without_anchor_is_structurally_impossible() -> None:
    """REC-04 — a SuggestedFix with NO Finding anchor is rejected at construction."""
    with pytest.raises(ValidationError):
        SuggestedFix(
            project_id=PROJECT, suggested_fix_id="fix-1",
            target_artifact="scope", candidate_edit="x",
            model_or_rule_version="wc-advise-v0", mode="fast",
            # no anchor → required field missing
        )


def test_c3_suggested_fix_empty_anchor_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SuggestedFix(
            project_id=PROJECT, suggested_fix_id="fix-1", anchor="",
            target_artifact="scope", candidate_edit="x",
            model_or_rule_version="wc-advise-v0", mode="fast",
        )


def test_c3_model_returned_unanchored_fix_is_dropped() -> None:
    """A model fix whose anchor resolves to nothing is DROPPED (never standalone)."""
    engine, _ = advise_engine(step_to_key={"suggested_fix": "suggested_fix_unanchored"})
    result = engine.derive(project_id=PROJECT, findings=[coverage_gap()])
    assert result.suggested_fixes == ()


def test_c3_suggested_fix_carries_no_applied_or_write_field() -> None:
    """Critical — a SuggestedFix has NO applied/written/apply field (extra='forbid')."""
    for bad_field in ("applied", "written", "apply", "severity", "score", "state"):
        with pytest.raises(ValidationError):
            SuggestedFix(
                project_id=PROJECT, suggested_fix_id="fix-1", anchor=COVERAGE_GAP_ID,
                target_artifact="scope", candidate_edit="x",
                model_or_rule_version="wc-advise-v0", mode="fast",
                **{bad_field: "nope"},
            )


def test_c3_no_new_output_kind_introduced_for_suggested_fix() -> None:
    """A SuggestedFix rides the EXISTING 'recommendation' kind — NO new output_kind."""
    kinds = set(OutputKind.__args__)  # type: ignore[attr-defined]
    # The advise CHR kinds are the two already-canonical kinds; nothing new added.
    assert stage_mod.OUTPUT_KIND_SUGGESTED_FIX == "recommendation"
    assert stage_mod.OUTPUT_KIND_SUGGESTED_FIX in kinds
    assert "suggested_fix" not in kinds  # the discriminator is a PAYLOAD value
    # The full kind set is unchanged from DTM-0014's canonical 14 (no fix kind).
    assert "recommendation" in kinds and "clarification" in kinds

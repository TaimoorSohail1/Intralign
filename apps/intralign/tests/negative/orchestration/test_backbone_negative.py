"""DTM-0005 negative orchestration suite — backbone forbidden behavior (QA-WA-00R B3).

Proves impossibility, not just absence of calls:

- B3.1 no API to change an assessment without recompute (introspection of the
  adapt/perceive/orchestration export surfaces — no set/update/overwrite mutators).
- B3.2 CHR overwrite impossible — the repository surface is re-asserted at the
  backbone level (DB REVOKE+trigger already proven in DTM-0002/0004 suites).
- B3.4 placeholder stages produce NO cognition (output == input, no CHR, no event).
- B3.5 no Derived->Attested path — AST scan: orchestration/adapt/perceive contain
  no direct table mutation calls; canonical writes go ONLY through retain.
- invalid trigger rejected before any run; unknown event names rejected at the seam.

Pure / static — never skips.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

import backend.orchestration.checkpointer as orch_checkpointer
import backend.orchestration.registry as orch_registry
import backend.orchestration.runner as orch_runner
import backend.orchestration.stages as orch_stages
import backend.orchestration.state as orch_state
import backend.responsibilities.adapt.states as adapt_states
import backend.responsibilities.adapt.triggers as adapt_triggers
import backend.responsibilities.perceive.staleness as perceive_staleness
from backend.orchestration import runner
from backend.orchestration.graphs import deep_pass
from backend.orchestration.stages import StageContext, default_stages
from backend.orchestration.state import GraphState
from backend.responsibilities.adapt.triggers import TriggerValidationError
from backend.responsibilities.retain import ChrRepository
from backend.services.observability.events import (
    EVENT_NAMES_WA00R,
    CollectingEventEmitter,
    UnknownEventError,
)

_BACKBONE_MODULES = (
    orch_checkpointer,
    orch_registry,
    orch_runner,
    orch_stages,
    orch_state,
    deep_pass,
    adapt_states,
    adapt_triggers,
    perceive_staleness,
)

# Verbs that would constitute an assessment-mutation API (B3.1).
_MUTATOR_PREFIXES = (
    "set_",
    "update_",
    "overwrite_",
    "mutate_",
    "delete_",
    "patch_",
    "edit_",
)
_MUTATOR_EXACT = {"set_assessment", "update_projection", "update_assessment"}


def _public_callables(module) -> list[str]:
    names: list[str] = []
    for name, value in vars(module).items():
        if name.startswith("_") or not callable(value):
            continue
        if getattr(value, "__module__", None) != module.__name__:
            continue  # re-exports/imports are checked in their defining module
        names.append(name)
        if inspect.isclass(value):
            names.extend(
                f"{name}.{attr}"
                for attr in vars(value)
                if not attr.startswith("_") and callable(getattr(value, attr))
            )
    return names


def test_b3_1_no_assessment_mutation_api_exists() -> None:
    """B3.1 — no exported callable can change an assessment without recompute."""
    for module in _BACKBONE_MODULES:
        for qualname in _public_callables(module):
            leaf = qualname.rsplit(".", maxsplit=1)[-1]
            assert leaf not in _MUTATOR_EXACT, (
                f"{module.__name__}.{qualname} is an assessment mutator — "
                "only recompute changes assessment (IC-WA-00R A4.1)"
            )
            assert not leaf.startswith(_MUTATOR_PREFIXES), (
                f"{module.__name__}.{qualname} looks like a mutation API — "
                "only recompute changes assessment (IC-WA-00R A4.1)"
            )


def test_b3_2_chr_overwrite_surface_absent_at_backbone_level() -> None:
    """B3.2 — the repository the backbone appends through has NO mutation surface.

    (Overwrite/delete are additionally DB-impossible — proven live in
    tests/negative/persistence and tests/negative/retain.)
    """
    for name in ("update", "delete", "upsert", "overwrite", "remove", "purge"):
        assert not hasattr(ChrRepository, name)
    public = {
        n
        for n in vars(ChrRepository)
        if not n.startswith("_") and callable(getattr(ChrRepository, n))
    }
    # DTM-0017 adds ``latest_acceptance_impact_for_uar`` — a SELECT-only READ for
    # the Acceptance-Impact supersede lookup (no mutation path is introduced).
    assert public == {
        "append",
        "get",
        "latest_for_output",
        "lineage_chain",
        "latest_acceptance_impact_for_uar",
    }


def test_b3_3_intake_alone_trigger_rejected_before_any_run() -> None:
    """B3.3 — submit-level: no information-change claim -> rejected, nothing runs."""
    emitter = CollectingEventEmitter()
    with pytest.raises(TriggerValidationError):
        runner.submit_trigger(
            "deep_pass",
            {
                "trigger_type": "user-action",
                "project_id": "66666666-6666-6666-6666-666666666666",
                "information_changed": False,  # intake/acceptance-capture alone
            },
            emitter=emitter,
        )
    assert emitter.events == []  # no recompute_started, no state move, nothing


def test_invalid_trigger_name_rejected_before_any_run() -> None:
    emitter = CollectingEventEmitter()
    with pytest.raises(TriggerValidationError):
        runner.submit_trigger(
            "deep_pass",
            {
                "trigger_type": "governance-sync",
                "project_id": "66666666-6666-6666-6666-666666666666",
                "information_changed": True,
            },
            emitter=emitter,
        )
    assert emitter.events == []


def test_b3_4_placeholder_stages_produce_no_cognition() -> None:
    """B3.4 / A4.3 — infer/evaluate/advise placeholders: output==input, no CHR."""

    class _ExplodingRepo:
        def append(self, record):  # pragma: no cover - failure is the assertion
            raise AssertionError("placeholder stage attempted a CHR append")

    emitter = CollectingEventEmitter()
    ctx = StageContext(emitter=emitter, chr_repo=_ExplodingRepo())
    state = GraphState(
        project_id="77777777-7777-7777-7777-777777777777",
        run_id="run-1",
        trigger={"trigger_type": "promotion"},
        emissions=[{"output_kind": "finding", "output_payload": {"summary": "x"}}],
        outputs={"prior": "untouched"},
        cognition_state="reanalyzing",
    )

    stages = default_stages()
    for name, expected_wave in (
        ("infer", "WAVE_B_PLACEHOLDER"),
        ("evaluate", "WAVE_B_PLACEHOLDER"),
        ("advise", "WAVE_C_PLACEHOLDER"),
    ):
        stage = stages[name]
        before = state.model_dump()
        result = stage(state, ctx)
        # Pass-through: NO state updates — the input is returned unchanged.
        assert result == {}, f"{name} placeholder must not produce updates"
        assert state.model_dump() == before
        # Clearly marked placeholder, in name AND docstring.
        assert expected_wave.lower() in stage.__name__.lower()
        assert expected_wave in (stage.__doc__ or "")
    # No event, no CHR append came out of any placeholder.
    assert emitter.events == []


def test_b3_4_retain_stage_is_the_only_real_chain_stage() -> None:
    """The backbone's only real stage is retain (append receipts) — A4.3."""
    stages = default_stages()
    assert set(stages) == {"retain", "infer", "evaluate", "advise"}
    assert "placeholder" not in stages["retain"].__name__.lower()


def _mutation_calls(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"insert", "update", "upsert", "delete", "table"}
        ):
            found.append(f"line {node.lineno}: .{node.func.attr}(...)")
    return found


def test_b3_5_no_derived_to_attested_write_path_static_scan() -> None:
    """B3.5 — orchestration/adapt/perceive never touch canonical tables directly.

    AST scan: no ``.table(...)``/``.insert(...)``/mutation calls and no raw
    Supabase client acquisition outside retain — the backbone writes canonical
    receipts ONLY via ``retain.ChrRepository.append`` (one-way flow, A4.4/A4.5).
    """
    code_root = Path(__file__).resolve().parents[3]
    scan_roots = (
        code_root / "backend" / "orchestration",
        code_root / "backend" / "responsibilities" / "adapt",
        code_root / "backend" / "responsibilities" / "perceive",
    )
    for root in scan_roots:
        assert root.is_dir(), f"missing scan root {root}"
        for py_file in sorted(root.rglob("*.py")):
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(py_file))
            offenders = _mutation_calls(tree)
            assert offenders == [], (
                f"{py_file.relative_to(code_root)} performs direct table access "
                f"({offenders}) — canonical writes go through retain only (B3.5)"
            )
            assert "get_supabase_client" not in source
            assert "create_client" not in source


def test_event_seam_rejects_unknown_event_names() -> None:
    """A6 — the backbone contract set is exactly these 7; nothing invented
    (DTM-0007: pinned per contract as EVENT_NAMES_WA00R; emitters accept the
    union, but an unknown name is still rejected loudly)."""
    assert EVENT_NAMES_WA00R == (
        "stale_detected",
        "reanalysis_triggered",
        "recompute_started",
        "cognition_history_record_appended",
        "recompute_completed",
        "recompute_failed",
        "state_transition_occurred",
    )
    emitter = CollectingEventEmitter()
    with pytest.raises(UnknownEventError):
        emitter.emit("assessment_changed", {})
    assert emitter.events == []

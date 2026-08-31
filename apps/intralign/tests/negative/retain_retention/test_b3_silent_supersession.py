"""QA-WA-002 B3.7 — silent supersession is structurally impossible (pure).

The ONLY public surface that creates a superseding ``attested_assertion`` row
is ``version_assertion``, and that function ALWAYS appends both history
entries and emits both events — proven three ways: AST introspection (no other
retain module ever writes a ``supersedes_id``), event-sequence assertion (the
events cannot be skipped), and rejection-path checks (a failed mutation writes
and emits nothing).
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

import backend.responsibilities.retain.admission as admission_module
from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.versioning import (
    PriorAssertionNotFoundError,
    version_assertion,
)
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate

RETAIN_DIR = Path(inspect.getfile(admission_module)).parent


def _insert_assertion_call_modules() -> dict[str, list[str]]:
    """Map module name -> source segments of its insert_assertion call args."""
    found: dict[str, list[str]] = {}
    for py_file in sorted(RETAIN_DIR.glob("*.py")):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        calls: list[str] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "insert_assertion"
            ):
                calls.append(ast.unparse(node))
        if calls:
            found[py_file.name] = calls
    return found


def test_b3_7_only_versioning_writes_a_supersedes_link() -> None:
    """AST: across ALL retain modules, the only insert_assertion call that
    carries a supersedes_id is the one inside version_assertion."""
    calls = _insert_assertion_call_modules()
    # The insert_assertion surfaces are admission (v1), versioning (vN+1), and
    # acceptance (the DTM-0016 plan fact — a NEW append-only row, never a
    # supersession).
    assert set(calls) == {"admission.py", "versioning.py", "acceptance.py"}
    for source in calls["admission.py"]:
        assert "supersedes_id" not in source, (
            "admission must never write a superseding row — initial versions "
            "only (B3.7: supersession has exactly one, evented, path)"
        )
    for source in calls["acceptance.py"]:
        assert "supersedes_id" not in source, (
            "the plan-fact write must never carry a supersedes_id — a plan fact "
            "is an append-only NEW row, never an overwrite (DTM-0016; B3.7: "
            "supersession has exactly one, evented, path)"
        )
    assert any("supersedes_id" in source for source in calls["versioning.py"])


def test_b3_7_versioning_module_always_pairs_write_with_both_events() -> None:
    """AST: versioning.py contains the explicit knowledge_versioned AND
    knowledge_superseded emit CALLS (not docstring mentions)."""
    tree = ast.parse((RETAIN_DIR / "versioning.py").read_text(encoding="utf-8"))
    emitted: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "emit"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            emitted.add(str(node.args[0].value))
    assert {
        "knowledge_versioned",
        "knowledge_superseded",
        "knowledge_mutation_recorded",
    } <= emitted


def test_b3_7_a_successful_mutation_cannot_skip_the_supersession_event() -> None:
    """Behavioral: every version_assertion call emits BOTH events, in order."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )

    version_assertion(
        admitted.assertion_ids[0],
        {"proposition": "revised."},
        store=store,
        emitter=emitter,
    )

    assert emitter.names == [
        "knowledge_versioned",
        "knowledge_superseded",
        "knowledge_mutation_recorded",
    ]
    # ... and both history entries exist (recorded, not just emitted).
    kinds = [h["event_type"] for h in store.history]
    assert kinds.count("superseded") == 1
    assert kinds.count("knowledge-versioned") == 2  # v1 (admission) + v2


def test_b3_7_failed_mutation_writes_nothing_and_emits_nothing() -> None:
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    with pytest.raises(PriorAssertionNotFoundError):
        version_assertion(
            "00000000-0000-0000-0000-000000000000",
            {"proposition": "x."},
            store=store,
            emitter=emitter,
        )
    assert store.assertions == []
    assert store.history == []
    assert emitter.events == []

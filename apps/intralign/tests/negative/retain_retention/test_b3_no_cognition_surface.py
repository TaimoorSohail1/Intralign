"""QA-WA-002 B3.4/B3.5/B3.6 — Retain is not a cognition role (pure introspection).

The new retain modules expose NO cognition surface (no Finding/Issue/
Recommendation/Clarification/Confidence producers, no severity/score fields)
and can NEVER run the recompute cascade themselves (no orchestration import,
no submit_trigger/invoke call) — a knowledge change becomes assessment-
relevant ONLY when orchestration runs the cascade (A10.7).
"""

from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

import backend.responsibilities.retain.acceptance as acceptance_module
import backend.responsibilities.retain.admission as admission_module
import backend.responsibilities.retain.archival as archival_module
import backend.responsibilities.retain.versioning as versioning_module
from backend.responsibilities.retain.admission import admit_candidate
from backend.responsibilities.retain.versioning import version_assertion
from backend.services.observability.events import CollectingEventEmitter
from tests.positive.retain_retention.fakes import InMemoryRetentionStore
from tests.positive.retain_retention.helpers import draft, ready_candidate

NEW_RETAIN_MODULES = (
    admission_module,
    versioning_module,
    archival_module,
    acceptance_module,
)
RETAIN_DIR = Path(inspect.getfile(admission_module)).parent
NEW_MODULE_FILES = ("admission.py", "versioning.py", "archival.py", "acceptance.py")

_COGNITION_NAME = re.compile(
    r"finding|issue|confidence|recommendation|clarification|severity|assessment",
    re.IGNORECASE,
)


def test_b3_4_b3_5_no_cognition_producer_exported() -> None:
    for module in NEW_RETAIN_MODULES:
        offenders = [n for n in dir(module) if _COGNITION_NAME.search(n)]
        assert offenders == [], (
            f"{module.__name__} exposes cognition-shaped surface {offenders} "
            "— Retain stores and triggers, it never reasons (IC-WA-002 A4.2/"
            "A4.3; QA B3.4/B3.5)"
        )


def test_b3_6_retain_never_calls_into_orchestration() -> None:
    """Static: retain CONSTRUCTS TriggerClaims but can NEVER run one — no
    orchestration import, no submit_trigger/invoke call (A3.10/A10.7)."""
    forbidden_calls = {"submit_trigger", "invoke"}
    for name in NEW_MODULE_FILES:
        tree = ast.parse((RETAIN_DIR / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names]
                module = getattr(node, "module", "") or ""
                assert "orchestration" not in module, f"{name}: {module}"
                assert not any("orchestration" in n for n in names)
            if isinstance(node, ast.Call):
                called = (
                    node.func.attr
                    if isinstance(node.func, ast.Attribute)
                    else node.func.id
                    if isinstance(node.func, ast.Name)
                    else None
                )
                assert called not in forbidden_calls, (
                    f"{name}:{node.lineno} calls {called} — Retain emits the "
                    "trigger and never runs the cascade (A3.10)"
                )


def test_b3_6_mutations_emit_no_recompute_event() -> None:
    """Behavioral: a full admit+version pass emits retention events ONLY —
    nothing from the recompute vocabulary (only recompute changes assessment)."""
    store, emitter = InMemoryRetentionStore(), CollectingEventEmitter()
    candidate = store.seed_candidate(ready_candidate())
    admitted = admit_candidate(candidate, [draft()], store=store, emitter=emitter)
    version_assertion(
        admitted.assertion_ids[0],
        {"proposition": "revised."},
        store=store,
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


def test_admitted_rows_carry_no_score_or_assessment_field() -> None:
    """The persisted assertion shape is the LDM §2.1 field set — nothing
    cognition-shaped can ride along."""
    store = InMemoryRetentionStore()
    candidate = store.seed_candidate(ready_candidate())
    admit_candidate(
        candidate, [draft()], store=store, emitter=CollectingEventEmitter()
    )
    row = store.assertions[0]
    offenders = [k for k in row if _COGNITION_NAME.search(k)]
    assert offenders == []

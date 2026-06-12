"""Gate 5 — observability gate, REAL (Deployment Governance §4 gate 5; DTM-0006).

A governed emission without its event must fail the build (DL-054 condition 1).
Three static checks (exit 0 pass / 1 fail, every violation printed):

a. **Append↔event pairing** — every CHR-append call-site under ``code/backend``
   must live in a module that also emits ``cognition_history_record_appended``.
   Detection approach (documented; simple text/AST hybrid by design):
   a module is a CHR-append call-site iff its source contains an
   ``<receiver>.append(...)`` call whose receiver mentions the CHR repository
   (``chr_repo`` / ``ChrRepository``, AST-resolved), **or** it calls
   ``retain_stage(...)`` directly. The repository definition module itself
   (``backend/responsibilities/retain/repository.py`` — the storage layer, not
   a call-site) is excluded. A flagged module passes iff it contains an actual
   ``*.emit("cognition_history_record_appended", ...)`` CALL (AST-checked —
   a docstring/comment mention of the event name does NOT count; red-proven).
   Plain ``list.append`` receivers never match — only CHR-repo receivers do.

b. **A6 vocabulary pinned** — ``backend/services/observability/events.py``
   must define ``EVENT_NAMES`` as EXACTLY the seven IC-WA-00R A6 names, in
   contract order. Any rename/addition/removal fails (events are contract
   surface; the OBS-WA-00R C2 list == A6).

c. **Replay harness present** — ``tests/replay/`` exists and contains at least
   one ``test_*.py`` (the two-axis determinism harness, OBS-WA-00R C5). The
   workflow step additionally RUNS ``pytest tests/replay`` (live axes skip
   without a local Supabase stack; the pure tamper-detection axes always run).
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections.abc import Sequence
from pathlib import Path

# (b) The IC-WA-00R A6 vocabulary — verbatim, in contract order (C2 == A6).
EXPECTED_EVENT_NAMES: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

APPEND_EVENT = "cognition_history_record_appended"
EVENTS_MODULE_RELPATH = "backend/services/observability/events.py"
REPLAY_DIR_RELPATH = "tests/replay"

# The repository definition module — the storage layer, not an emission
# call-site (its .append IS the persistence primitive the others pair with).
REPOSITORY_DEFINITION_RELPATH = "backend/responsibilities/retain/repository.py"

# Receiver markers identifying a CHR-repo append (vs a plain list.append).
_CHR_RECEIVER_MARKERS = ("chr_repo", "chrrepository")


def _receiver_mentions_chr_repo(func: ast.Attribute) -> bool:
    """True when the ``.append`` receiver expression names the CHR repository."""
    receiver = ast.unparse(func.value).lower()
    return any(marker in receiver for marker in _CHR_RECEIVER_MARKERS)


def _is_chr_append_call(node: ast.Call) -> bool:
    return (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "append"
        and _receiver_mentions_chr_repo(node.func)
    )


def _is_retain_stage_call(node: ast.Call) -> bool:
    func = node.func
    name = func.id if isinstance(func, ast.Name) else (
        func.attr if isinstance(func, ast.Attribute) else None
    )
    return name == "retain_stage"


def module_chr_append_lines(source: str) -> list[int]:
    """Line numbers of CHR-append / retain_stage call-sites in ``source``."""
    tree = ast.parse(source)
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (_is_chr_append_call(node) or _is_retain_stage_call(node))
    ]


def module_emits_append_event(source: str) -> bool:
    """True iff the module contains an ACTUAL ``*.emit(APPEND_EVENT, ...)`` call.

    AST-checked: a docstring or comment merely mentioning the event name does
    not satisfy the pairing (proven red by removing the emit call while the
    module docstring still names the event).
    """
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else (
            func.id if isinstance(func, ast.Name) else None
        )
        first = node.args[0]
        if (
            name == "emit"
            and isinstance(first, ast.Constant)
            and first.value == APPEND_EVENT
        ):
            return True
    return False


def check_append_event_pairing(code_root: Path) -> list[str]:
    """(a) Every CHR-append call-site module must emit the append event."""
    backend = code_root / "backend"
    if not backend.is_dir():
        return [f"{backend}: backend/ tree missing — nothing to gate"]
    violations: list[str] = []
    for py_file in sorted(backend.rglob("*.py")):
        relpath = py_file.relative_to(code_root).as_posix()
        if relpath == REPOSITORY_DEFINITION_RELPATH:
            continue  # the storage layer itself, not a call-site
        source = py_file.read_text(encoding="utf-8")
        try:
            lines = module_chr_append_lines(source)
            paired = module_emits_append_event(source) if lines else True
        except SyntaxError as exc:  # gate 1 owns syntax; report, don't crash
            violations.append(f"{relpath}: unparseable ({exc.msg}, line {exc.lineno})")
            continue
        if lines and not paired:
            violations.append(
                f"{relpath}:{lines[0]}: CHR append call-site without a paired "
                f"'{APPEND_EVENT}' emit CALL in the module — a governed "
                "emission must emit its event (OBS-WA-00R C2; DL-054 cond.1)"
            )
    return violations


def _event_names_value_node(tree: ast.Module) -> ast.expr | None:
    """The value expression assigned to EVENT_NAMES (Assign or AnnAssign form)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "EVENT_NAMES" for t in node.targets
        ):
            return node.value
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "EVENT_NAMES"
            and node.value is not None
        ):
            return node.value
    return None


def check_event_vocabulary(code_root: Path) -> list[str]:
    """(b) EVENT_NAMES in events.py == the seven A6 names, exactly, in order."""
    events_path = code_root / EVENTS_MODULE_RELPATH
    if not events_path.is_file():
        return [f"{EVENTS_MODULE_RELPATH}: missing — the A6 event seam is mandatory"]
    value = _event_names_value_node(ast.parse(events_path.read_text(encoding="utf-8")))
    if value is None:
        return [
            f"{EVENTS_MODULE_RELPATH}: EVENT_NAMES not found — the A6 "
            "vocabulary must be pinned"
        ]
    try:
        actual = tuple(ast.literal_eval(value))
    except (ValueError, TypeError):
        return [
            f"{EVENTS_MODULE_RELPATH}: EVENT_NAMES is not a literal tuple of "
            "names — the vocabulary must be statically pinned"
        ]
    if actual != EXPECTED_EVENT_NAMES:
        return [
            f"{EVENTS_MODULE_RELPATH}: EVENT_NAMES != the IC-WA-00R A6 "
            f"vocabulary — expected {EXPECTED_EVENT_NAMES}, found {actual} "
            "(invent no event types; Event Model names verbatim)"
        ]
    return []


def check_replay_harness(code_root: Path) -> list[str]:
    """(c) tests/replay/ exists and holds at least one test module."""
    replay_dir = code_root / REPLAY_DIR_RELPATH
    if not replay_dir.is_dir():
        return [
            f"{REPLAY_DIR_RELPATH}/: missing — the two-axis replay harness "
            "(OBS-WA-00R C5) is a gate-5 requirement"
        ]
    if not sorted(replay_dir.rglob("test_*.py")):
        return [
            f"{REPLAY_DIR_RELPATH}/: contains no test_*.py — the replay "
            "harness must be present AND non-empty (OBS-WA-00R C5)"
        ]
    return []


def run_all_checks(code_root: Path) -> list[str]:
    """Run checks (a)+(b)+(c); empty list == gate passes."""
    return [
        *check_append_event_pairing(code_root),
        *check_event_vocabulary(code_root),
        *check_replay_harness(code_root),
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--code-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="App root (the code/ directory). Default: parent of ci/.",
    )
    args = parser.parse_args(argv)

    violations = run_all_checks(args.code_root)
    if violations:
        print(
            f"[gate-5 observability] FAIL — {len(violations)} violation(s) "
            "(Deployment Governance §4 gate 5; OBS-WA-00R):"
        )
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print(
        "[gate-5 observability] PASS: every CHR-append call-site emits "
        f"'{APPEND_EVENT}', the A6 vocabulary is pinned verbatim, and the "
        "two-axis replay harness is present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

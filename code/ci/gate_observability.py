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

b. **A6 vocabularies pinned per contract** (DTM-0007, decision #1; DTM-0008) —
   ``backend/services/observability/events.py`` must define
   ``EVENT_NAMES_WA00R`` as EXACTLY the seven IC-WA-00R A6 names,
   ``EVENT_NAMES_WA001`` as EXACTLY the eight IC-WA-001 A6 names, and
   ``EVENT_NAMES_WA002`` as EXACTLY the five IC-WA-002 A6 names,
   ``EVENT_NAMES_WS`` as EXACTLY the four IC/OBS-WS-SYNTH A6 names,
   ``EVENT_NAMES_WB_INFER`` as EXACTLY the two IC/OBS-WB-INFER A6 names,
   ``EVENT_NAMES_WB_EVAL`` as EXACTLY the five IC/OBS-WB-EVAL A6 names,
   ``EVENT_NAMES_WC_ADVISE`` as EXACTLY the two IC/OBS-WC-ADVISE A6 names,
   ``EVENT_NAMES_WC_FIX`` as EXACTLY the one DL-047 SuggestedFix OBS name,
   ``EVENT_NAMES_WU_ACCEPT`` as EXACTLY the three IC-WU-ACCEPT C3 names, and
   ``EVENT_NAMES_COST`` as EXACTLY the one DL-048 cost event, each a
   literal tuple in contract order, plus ``EVENT_NAMES`` as their consistent
   union (the literal concatenation, or the ``WA00R + WA001 + WA002 + WS +
   WB_INFER + WB_EVAL + WC_ADVISE + WC_FIX + WU_ACCEPT + COST`` name
   concatenation). Any rename/addition/removal fails (events are
   contract surface; OBS C2 lists == A6 lists; ``stale_detected`` lives in
   WA00R only).

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

# (b) The per-contract A6 vocabularies — verbatim, in contract order (C2 == A6).
EXPECTED_EVENT_NAMES_WA00R: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

# IC-WA-001 A6 (stale_detected is in the WA00R set, never duplicated).
EXPECTED_EVENT_NAMES_WA001: tuple[str, ...] = (
    "artifact_received",
    "artifact_normalizing",
    "artifact_normalized",
    "promotion_candidate_ready",
    "promotion_readiness_failed",
    "user_acceptance_captured",
    "context_signal_received",
    "artifact_modified",
)

# IC-WA-002 A6 (DTM-0008 — the five retention events, contract order).
EXPECTED_EVENT_NAMES_WA002: tuple[str, ...] = (
    "knowledge_promoted",
    "knowledge_versioned",
    "knowledge_superseded",
    "knowledge_archived",
    "knowledge_mutation_recorded",
)

# IC/OBS-WS-SYNTH A6 (DTM-0009 — the four synthesis-engine events, decision #9).
EXPECTED_EVENT_NAMES_WS: tuple[str, ...] = (
    "claim_extracted",
    "planning_artifact_generated",
    "planning_artifact_regenerated",
    "synthesized_model_updated",
)

# IC/OBS-WB-INFER A6 (DTM-0010 — the two Finding events, decision #9).
EXPECTED_EVENT_NAMES_WB_INFER: tuple[str, ...] = (
    "finding_detected",
    "finding_superseded",
)

# IC/OBS-WB-EVAL A6 (DTM-0011 — the five Evaluate events, decision #9).
EXPECTED_EVENT_NAMES_WB_EVAL: tuple[str, ...] = (
    "issue_generated",
    "caf_assessed",
    "outcome_confidence_computed",
    "understanding_state_changed",
    "false_confidence_flagged",
)

# IC/OBS-WC-ADVISE A6 (DTM-0014 — the two Advise events, decision #11).
EXPECTED_EVENT_NAMES_WC_ADVISE: tuple[str, ...] = (
    "recommendation_generated",
    "clarification_requested",
)

# DL-047 SuggestedFix OBS (DTM-0015 — the single "Suggested Fix Offered" event).
EXPECTED_EVENT_NAMES_WC_FIX: tuple[str, ...] = (
    "suggested_fix_offered",
)

# IC/OBS-WU-ACCEPT C3 (DTM-0016 + DTM-0017 — the three acceptance events).
EXPECTED_EVENT_NAMES_WU_ACCEPT: tuple[str, ...] = (
    "user_acceptance_record_appended",
    "plan_fact_recorded",
    "acceptance_impact_assessed",
)

# DL-048 cost-governance — the single shared spend event (DTM-0009; decision #9).
EXPECTED_EVENT_NAMES_COST: tuple[str, ...] = ("ai_spend_recorded",)

# Event Model §8.8 analysis-command events (DTM-0032 — :fast/:deep/:cancel).
EXPECTED_EVENT_NAMES_ANALYSIS: tuple[str, ...] = (
    "fast_analysis_requested",
    "deep_analysis_requested",
    "analysis_cancelled",
)

# The union the emitters must accept (back-compat alias in events.py).
EXPECTED_EVENT_NAMES: tuple[str, ...] = (
    EXPECTED_EVENT_NAMES_WA00R
    + EXPECTED_EVENT_NAMES_WA001
    + EXPECTED_EVENT_NAMES_WA002
    + EXPECTED_EVENT_NAMES_WS
    + EXPECTED_EVENT_NAMES_WB_INFER
    + EXPECTED_EVENT_NAMES_WB_EVAL
    + EXPECTED_EVENT_NAMES_WC_ADVISE
    + EXPECTED_EVENT_NAMES_WC_FIX
    + EXPECTED_EVENT_NAMES_WU_ACCEPT
    + EXPECTED_EVENT_NAMES_COST
    + EXPECTED_EVENT_NAMES_ANALYSIS
)

# (contract-tuple variable name, expected value, contract label) for check (b).
_CONTRACT_VOCABULARIES: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("EVENT_NAMES_WA00R", EXPECTED_EVENT_NAMES_WA00R, "IC-WA-00R A6"),
    ("EVENT_NAMES_WA001", EXPECTED_EVENT_NAMES_WA001, "IC-WA-001 A6"),
    ("EVENT_NAMES_WA002", EXPECTED_EVENT_NAMES_WA002, "IC-WA-002 A6"),
    ("EVENT_NAMES_WS", EXPECTED_EVENT_NAMES_WS, "IC-WS-SYNTH A6"),
    ("EVENT_NAMES_WB_INFER", EXPECTED_EVENT_NAMES_WB_INFER, "IC-WB-INFER A6"),
    ("EVENT_NAMES_WB_EVAL", EXPECTED_EVENT_NAMES_WB_EVAL, "IC-WB-EVAL A6"),
    ("EVENT_NAMES_WC_ADVISE", EXPECTED_EVENT_NAMES_WC_ADVISE, "IC-WC-ADVISE A6"),
    ("EVENT_NAMES_WC_FIX", EXPECTED_EVENT_NAMES_WC_FIX, "DL-047 SuggestedFix"),
    ("EVENT_NAMES_WU_ACCEPT", EXPECTED_EVENT_NAMES_WU_ACCEPT, "IC-WU-ACCEPT C3"),
    ("EVENT_NAMES_COST", EXPECTED_EVENT_NAMES_COST, "DL-048 cost"),
    ("EVENT_NAMES_ANALYSIS", EXPECTED_EVENT_NAMES_ANALYSIS, "EM §8.8 analysis"),
)

# The union must be the per-contract names concatenated in this exact order.
_UNION_NAME_ORDER: tuple[str, ...] = (
    "EVENT_NAMES_WA00R",
    "EVENT_NAMES_WA001",
    "EVENT_NAMES_WA002",
    "EVENT_NAMES_WS",
    "EVENT_NAMES_WB_INFER",
    "EVENT_NAMES_WB_EVAL",
    "EVENT_NAMES_WC_ADVISE",
    "EVENT_NAMES_WC_FIX",
    "EVENT_NAMES_WU_ACCEPT",
    "EVENT_NAMES_COST",
    "EVENT_NAMES_ANALYSIS",
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


def _assigned_value_node(tree: ast.Module, name: str) -> ast.expr | None:
    """The value expression assigned to ``name`` (Assign or AnnAssign form)."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return node.value
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
            and node.value is not None
        ):
            return node.value
    return None


def _check_contract_tuple(
    tree: ast.Module, name: str, expected: tuple[str, ...], contract: str
) -> list[str]:
    """One per-contract tuple: present, literal, and verbatim in contract order."""
    value = _assigned_value_node(tree, name)
    if value is None:
        return [
            f"{EVENTS_MODULE_RELPATH}: {name} not found — the {contract} "
            "vocabulary must be pinned"
        ]
    try:
        actual = tuple(ast.literal_eval(value))
    except (ValueError, TypeError):
        return [
            f"{EVENTS_MODULE_RELPATH}: {name} is not a literal tuple of "
            "names — the vocabulary must be statically pinned"
        ]
    if actual != expected:
        return [
            f"{EVENTS_MODULE_RELPATH}: {name} != the {contract} "
            f"vocabulary — expected {expected}, found {actual} "
            "(invent no event types; Event Model names verbatim)"
        ]
    return []


def _flatten_name_concatenation(value: ast.expr) -> tuple[str, ...] | None:
    """Flatten a left-folded ``Name + Name + ...`` expression to its name chain."""
    if isinstance(value, ast.Name):
        return (value.id,)
    if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
        left = _flatten_name_concatenation(value.left)
        right = _flatten_name_concatenation(value.right)
        if left is not None and right is not None:
            return left + right
    return None


def _union_is_consistent(value: ast.expr) -> bool:
    """EVENT_NAMES is the per-contract concatenation (by name) or the literal union."""
    if _flatten_name_concatenation(value) == _UNION_NAME_ORDER:
        return True
    try:
        return tuple(ast.literal_eval(value)) == EXPECTED_EVENT_NAMES
    except (ValueError, TypeError):
        return False


def check_event_vocabulary(code_root: Path) -> list[str]:
    """(b) Per-contract vocabularies verbatim + EVENT_NAMES union consistency."""
    events_path = code_root / EVENTS_MODULE_RELPATH
    if not events_path.is_file():
        return [f"{EVENTS_MODULE_RELPATH}: missing — the A6 event seam is mandatory"]
    tree = ast.parse(events_path.read_text(encoding="utf-8"))
    violations: list[str] = []
    for name, expected, contract in _CONTRACT_VOCABULARIES:
        violations.extend(_check_contract_tuple(tree, name, expected, contract))
    union_value = _assigned_value_node(tree, "EVENT_NAMES")
    if union_value is None:
        violations.append(
            f"{EVENTS_MODULE_RELPATH}: EVENT_NAMES not found — the union "
            "vocabulary (back-compat alias) must be pinned"
        )
    elif not _union_is_consistent(union_value):
        violations.append(
            f"{EVENTS_MODULE_RELPATH}: EVENT_NAMES != the union of the "
            "per-contract vocabularies (EVENT_NAMES_WA00R + EVENT_NAMES_WA001 "
            "+ EVENT_NAMES_WA002) — the emitters must accept exactly the "
            "contract sets"
        )
    return violations


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
        f"'{APPEND_EVENT}', the per-contract A6 vocabularies are pinned "
        "verbatim (union consistent), and the replay harness is present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

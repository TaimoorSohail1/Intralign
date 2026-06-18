"""DTM-0006 negative — gate-5 catches suppressed observability (red-proof in unit form).

Synthetic trees prove each failure mode independently:
- a CHR append call-site whose module does NOT emit the append event;
- a direct retain_stage() call in an event-less module;
- a missing / empty tests/replay harness;
- a tampered A6 vocabulary (renamed, extra, or non-literal EVENT_NAMES) across
  every per-contract tuple — WA00R / WA001 / WA002 / WS / WB_INFER (DTM-0010) /
  WB_EVAL (DTM-0011) / WC_ADVISE (DTM-0014) / WC_FIX (DTM-0015) / COST — plus a
  drifted or short 9-way union.
"""

from __future__ import annotations

from pathlib import Path

from ci.gate_observability import (
    check_append_event_pairing,
    check_event_vocabulary,
    check_replay_harness,
    main,
    run_all_checks,
)

GOOD_EVENTS_PY = '''
EVENT_NAMES_WA00R: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
)

EVENT_NAMES_WA001: tuple[str, ...] = (
    "artifact_received",
    "artifact_normalizing",
    "artifact_normalized",
    "promotion_candidate_ready",
    "promotion_readiness_failed",
    "user_acceptance_captured",
    "context_signal_received",
    "artifact_modified",
)

EVENT_NAMES_WA002: tuple[str, ...] = (
    "knowledge_promoted",
    "knowledge_versioned",
    "knowledge_superseded",
    "knowledge_archived",
    "knowledge_mutation_recorded",
)

EVENT_NAMES_WS: tuple[str, ...] = (
    "claim_extracted",
    "planning_artifact_generated",
    "planning_artifact_regenerated",
    "synthesized_model_updated",
)

EVENT_NAMES_WB_INFER: tuple[str, ...] = (
    "finding_detected",
    "finding_superseded",
)

EVENT_NAMES_WB_EVAL: tuple[str, ...] = (
    "issue_generated",
    "caf_assessed",
    "outcome_confidence_computed",
    "understanding_state_changed",
    "false_confidence_flagged",
)

EVENT_NAMES_WC_ADVISE: tuple[str, ...] = (
    "recommendation_generated",
    "clarification_requested",
)

EVENT_NAMES_WC_FIX: tuple[str, ...] = (
    "suggested_fix_offered",
)

EVENT_NAMES_COST: tuple[str, ...] = ("ai_spend_recorded",)

EVENT_NAMES: tuple[str, ...] = (
    EVENT_NAMES_WA00R
    + EVENT_NAMES_WA001
    + EVENT_NAMES_WA002
    + EVENT_NAMES_WS
    + EVENT_NAMES_WB_INFER
    + EVENT_NAMES_WB_EVAL
    + EVENT_NAMES_WC_ADVISE
    + EVENT_NAMES_WC_FIX
    + EVENT_NAMES_COST
)
'''

PAIRED_MODULE = '''
def retain(state, ctx):
    persisted = ctx.chr_repo.append(record)
    ctx.emitter.emit("cognition_history_record_appended", {"chr_id": "x"})
'''

UNPAIRED_MODULE = '''
def sneaky(state, ctx):
    return ctx.chr_repo.append(record)  # governed emission, NO event
'''


def _make_tree(
    tmp_path: Path,
    *,
    module_src: str = PAIRED_MODULE,
    events_src: str = GOOD_EVENTS_PY,
    with_replay: bool = True,
) -> Path:
    root = tmp_path / "code"
    (root / "backend/orchestration").mkdir(parents=True)
    (root / "backend/orchestration/stages.py").write_text(module_src)
    obs = root / "backend/services/observability"
    obs.mkdir(parents=True)
    (obs / "events.py").write_text(events_src)
    if with_replay:
        replay = root / "tests/replay"
        replay.mkdir(parents=True)
        (replay / "test_record_exact_replay.py").write_text("def test_ok():\n    pass\n")
    return root


def test_synthetic_good_tree_passes(tmp_path) -> None:
    """The fixture tree itself is green — failures below are real signal."""
    assert run_all_checks(_make_tree(tmp_path)) == []


def test_unpaired_chr_append_fails(tmp_path) -> None:
    root = _make_tree(tmp_path, module_src=UNPAIRED_MODULE)
    violations = check_append_event_pairing(root)
    assert len(violations) == 1
    assert "without a paired 'cognition_history_record_appended'" in violations[0]
    assert "backend/orchestration/stages.py" in violations[0]
    assert main(["--code-root", str(root)]) == 1


def test_docstring_mention_does_not_satisfy_the_pairing(tmp_path) -> None:
    """Red-proven: naming the event in a docstring is NOT emitting it."""
    docstring_only = (
        '"""Appends CHRs. Emits cognition_history_record_appended per receipt."""\n'
        "def sneaky(state, ctx):\n"
        "    return ctx.chr_repo.append(record)\n"
    )
    root = _make_tree(tmp_path, module_src=docstring_only)
    violations = check_append_event_pairing(root)
    assert len(violations) == 1
    assert "emit CALL" in violations[0]


def test_unpaired_retain_stage_call_fails(tmp_path) -> None:
    root = _make_tree(
        tmp_path,
        module_src="def run(state, ctx):\n    return retain_stage(state, ctx)\n",
    )
    violations = check_append_event_pairing(root)
    assert len(violations) == 1
    assert "backend/orchestration/stages.py" in violations[0]


def test_missing_replay_dir_fails(tmp_path) -> None:
    root = _make_tree(tmp_path, with_replay=False)
    violations = check_replay_harness(root)
    assert len(violations) == 1
    assert "tests/replay/: missing" in violations[0]
    assert main(["--code-root", str(root)]) == 1


def test_empty_replay_dir_fails(tmp_path) -> None:
    root = _make_tree(tmp_path, with_replay=False)
    (root / "tests/replay").mkdir(parents=True)  # exists but holds no tests
    violations = check_replay_harness(root)
    assert len(violations) == 1
    assert "no test_*.py" in violations[0]


def test_renamed_wa00r_event_fails_vocabulary_check(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace("recompute_failed", "recompute_errored")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WA00R != the IC-WA-00R A6 vocabulary" in violations[0]


def test_renamed_wa001_event_fails_vocabulary_check(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace("artifact_modified", "artifact_changed")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WA001 != the IC-WA-001 A6 vocabulary" in violations[0]


def test_extra_event_fails_vocabulary_check(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace(
        '"state_transition_occurred",',
        '"state_transition_occurred",\n    "free_form_event",',
    )
    root = _make_tree(tmp_path, events_src=tampered)
    assert check_event_vocabulary(root) != []


def test_duplicated_stale_detected_in_wa001_fails(tmp_path) -> None:
    """stale_detected belongs to WA00R; duplicating it in WA001 is a tamper."""
    tampered = GOOD_EVENTS_PY.replace(
        '"artifact_modified",',
        '"artifact_modified",\n    "stale_detected",',
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WA001" in v for v in violations)


def test_renamed_wa002_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0008 — tampering the IC-WA-002 A6 vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("knowledge_superseded", "knowledge_replaced")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WA002 != the IC-WA-002 A6 vocabulary" in violations[0]


def test_missing_wa002_tuple_fails_vocabulary_check(tmp_path) -> None:
    """Dropping the WA002 tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WA002: tuple[str, ...] = (\n'
        '    "knowledge_promoted",\n'
        '    "knowledge_versioned",\n'
        '    "knowledge_superseded",\n'
        '    "knowledge_archived",\n'
        '    "knowledge_mutation_recorded",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WA002\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WA002 not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_renamed_ws_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0009 — tampering the IC-WS-SYNTH A6 vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace(
        "synthesized_model_updated", "synthesized_model_changed"
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WS != the IC-WS-SYNTH A6 vocabulary" in violations[0]


def test_renamed_cost_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0009 — renaming the DL-048 cost event fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("ai_spend_recorded", "ai_cost_logged")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_COST != the DL-048 cost vocabulary" in violations[0]


def test_missing_ws_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0009 — dropping the WS tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WS: tuple[str, ...] = (\n'
        '    "claim_extracted",\n'
        '    "planning_artifact_generated",\n'
        '    "planning_artifact_regenerated",\n'
        '    "synthesized_model_updated",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WS\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WS not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_missing_cost_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0009 — dropping the COST tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_COST: tuple[str, ...] = ("ai_spend_recorded",)\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_COST\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_COST not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_renamed_wb_infer_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0010 — tampering the IC-WB-INFER A6 vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("finding_superseded", "finding_replaced")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WB_INFER != the IC-WB-INFER A6 vocabulary" in violations[0]


def test_missing_wb_infer_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0010 — dropping the WB_INFER tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WB_INFER: tuple[str, ...] = (\n'
        '    "finding_detected",\n'
        '    "finding_superseded",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WB_INFER\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WB_INFER not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_renamed_wb_eval_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0011 — tampering the IC-WB-EVAL A6 vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("outcome_confidence_computed", "outcome_confidence_done")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WB_EVAL != the IC-WB-EVAL A6 vocabulary" in violations[0]


def test_missing_wb_eval_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0011 — dropping the WB_EVAL tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WB_EVAL: tuple[str, ...] = (\n'
        '    "issue_generated",\n'
        '    "caf_assessed",\n'
        '    "outcome_confidence_computed",\n'
        '    "understanding_state_changed",\n'
        '    "false_confidence_flagged",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WB_EVAL\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WB_EVAL not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_renamed_wc_advise_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0014 — tampering the IC-WC-ADVISE A6 vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("clarification_requested", "clarification_asked")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WC_ADVISE != the IC-WC-ADVISE A6 vocabulary" in violations[0]


def test_missing_wc_advise_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0014 — dropping the WC_ADVISE tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WC_ADVISE: tuple[str, ...] = (\n'
        '    "recommendation_generated",\n'
        '    "clarification_requested",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WC_ADVISE\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WC_ADVISE not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_renamed_wc_fix_event_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0015 — tampering the DL-047 SuggestedFix OBS vocabulary fails the gate."""
    tampered = GOOD_EVENTS_PY.replace("suggested_fix_offered", "fix_applied")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES_WC_FIX != the DL-047 SuggestedFix vocabulary" in violations[0]


def test_missing_wc_fix_tuple_fails_vocabulary_check(tmp_path) -> None:
    """DTM-0015 — dropping the WC_FIX tuple (and its union leg) fails both checks."""
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WC_FIX: tuple[str, ...] = (\n'
        '    "suggested_fix_offered",\n'
        ')\n\n',
        "",
    ).replace(
        "    + EVENT_NAMES_WC_FIX\n",
        "",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert any("EVENT_NAMES_WC_FIX not found" in v for v in violations)
    assert any("union of the per-contract vocabularies" in v for v in violations)


def test_missing_event_names_assignment_fails(tmp_path) -> None:
    root = _make_tree(tmp_path, events_src="OTHER = 1\n")
    violations = check_event_vocabulary(root)
    # all nine contract tuples (WA00R/WA001/WA002/WS/WB_INFER/WB_EVAL/WC_ADVISE/
    # WC_FIX/COST) AND the union.
    assert len(violations) == 10
    assert any("EVENT_NAMES_WA00R not found" in v for v in violations)
    assert any("EVENT_NAMES_WA001 not found" in v for v in violations)
    assert any("EVENT_NAMES_WA002 not found" in v for v in violations)
    assert any("EVENT_NAMES_WS not found" in v for v in violations)
    assert any("EVENT_NAMES_WB_INFER not found" in v for v in violations)
    assert any("EVENT_NAMES_WB_EVAL not found" in v for v in violations)
    assert any("EVENT_NAMES_WC_ADVISE not found" in v for v in violations)
    assert any("EVENT_NAMES_WC_FIX not found" in v for v in violations)
    assert any("EVENT_NAMES_COST not found" in v for v in violations)
    assert any("EVENT_NAMES not found" in v for v in violations)


def test_non_literal_contract_vocabulary_fails(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace(
        'EVENT_NAMES_WA001: tuple[str, ...] = (\n'
        '    "artifact_received",',
        'EVENT_NAMES_WA001: tuple[str, ...] = tuple(sorted((\n'
        '    "artifact_received",',
    ).replace(
        '    "artifact_modified",\n)',
        '    "artifact_modified",\n)))',
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "statically pinned" in violations[0]


def test_inconsistent_union_fails(tmp_path) -> None:
    """EVENT_NAMES must be the exact 5-way concatenation — a drifted alias fails."""
    tampered = GOOD_EVENTS_PY.replace(
        "    EVENT_NAMES_WA00R\n    + EVENT_NAMES_WA001\n",
        "    EVENT_NAMES_WA001\n    + EVENT_NAMES_WA00R\n",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "union of the per-contract vocabularies" in violations[0]


def test_union_dropping_ws_and_cost_legs_fails(tmp_path) -> None:
    """DTM-0015 — a union that omits the WS/WB_INFER/WB_EVAL/WC_ADVISE/WC_FIX/COST legs (an old form) fails."""
    tampered = GOOD_EVENTS_PY.replace(
        "EVENT_NAMES: tuple[str, ...] = (\n"
        "    EVENT_NAMES_WA00R\n"
        "    + EVENT_NAMES_WA001\n"
        "    + EVENT_NAMES_WA002\n"
        "    + EVENT_NAMES_WS\n"
        "    + EVENT_NAMES_WB_INFER\n"
        "    + EVENT_NAMES_WB_EVAL\n"
        "    + EVENT_NAMES_WC_ADVISE\n"
        "    + EVENT_NAMES_WC_FIX\n"
        "    + EVENT_NAMES_COST\n"
        ")",
        "EVENT_NAMES: tuple[str, ...] = (\n"
        "    EVENT_NAMES_WA00R + EVENT_NAMES_WA001 + EVENT_NAMES_WA002\n"
        ")",
    )
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "union of the per-contract vocabularies" in violations[0]

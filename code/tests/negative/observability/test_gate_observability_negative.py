"""DTM-0006 negative — gate-5 catches suppressed observability (red-proof in unit form).

Synthetic trees prove each failure mode independently:
- a CHR append call-site whose module does NOT emit the append event;
- a direct retain_stage() call in an event-less module;
- a missing / empty tests/replay harness;
- a tampered A6 vocabulary (renamed, extra, or non-literal EVENT_NAMES).
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
EVENT_NAMES: tuple[str, ...] = (
    "stale_detected",
    "reanalysis_triggered",
    "recompute_started",
    "cognition_history_record_appended",
    "recompute_completed",
    "recompute_failed",
    "state_transition_occurred",
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


def test_renamed_event_fails_vocabulary_check(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace("recompute_failed", "recompute_errored")
    root = _make_tree(tmp_path, events_src=tampered)
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES != the IC-WA-00R A6 vocabulary" in violations[0]


def test_extra_event_fails_vocabulary_check(tmp_path) -> None:
    tampered = GOOD_EVENTS_PY.replace(
        '"state_transition_occurred",',
        '"state_transition_occurred",\n    "free_form_event",',
    )
    root = _make_tree(tmp_path, events_src=tampered)
    assert check_event_vocabulary(root) != []


def test_missing_event_names_assignment_fails(tmp_path) -> None:
    root = _make_tree(tmp_path, events_src="OTHER = 1\n")
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "EVENT_NAMES not found" in violations[0]


def test_non_literal_vocabulary_fails(tmp_path) -> None:
    root = _make_tree(
        tmp_path, events_src="EVENT_NAMES = tuple(sorted(build_names()))\n"
    )
    violations = check_event_vocabulary(root)
    assert len(violations) == 1
    assert "statically pinned" in violations[0]

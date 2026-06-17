"""DTM-0006 positive — gate-5 script passes the REAL tree (ci.gate_observability).

The actual code/ tree satisfies all three checks: every CHR-append call-site
emits its event, the A6 vocabulary is pinned verbatim, and the two-axis replay
harness is present and non-empty. Also pins the detection logic itself on
known-good real modules.
"""

from __future__ import annotations

from pathlib import Path

from ci.gate_observability import (
    EXPECTED_EVENT_NAMES,
    EXPECTED_EVENT_NAMES_COST,
    EXPECTED_EVENT_NAMES_WA00R,
    EXPECTED_EVENT_NAMES_WA001,
    EXPECTED_EVENT_NAMES_WA002,
    EXPECTED_EVENT_NAMES_WB_INFER,
    EXPECTED_EVENT_NAMES_WS,
    check_append_event_pairing,
    check_event_vocabulary,
    check_replay_harness,
    main,
    module_chr_append_lines,
    module_emits_append_event,
    run_all_checks,
)
from backend.services.observability.events import (
    EVENT_NAMES,
    EVENT_NAMES_COST,
    EVENT_NAMES_WA00R,
    EVENT_NAMES_WA001,
    EVENT_NAMES_WA002,
    EVENT_NAMES_WB_INFER,
    EVENT_NAMES_WS,
)

CODE_ROOT = Path(__file__).resolve().parents[3]


def test_real_tree_passes_every_check() -> None:
    assert check_append_event_pairing(CODE_ROOT) == []
    assert check_event_vocabulary(CODE_ROOT) == []
    assert check_replay_harness(CODE_ROOT) == []
    assert run_all_checks(CODE_ROOT) == []


def test_cli_exits_zero_on_real_tree(capsys) -> None:
    assert main(["--code-root", str(CODE_ROOT)]) == 0
    assert "[gate-5 observability] PASS" in capsys.readouterr().out


def test_expected_vocabulary_matches_the_live_seam() -> None:
    """The gate's pinned lists and the runtime seam can never drift apart."""
    assert EXPECTED_EVENT_NAMES_WA00R == EVENT_NAMES_WA00R
    assert EXPECTED_EVENT_NAMES_WA001 == EVENT_NAMES_WA001
    assert EXPECTED_EVENT_NAMES_WA002 == EVENT_NAMES_WA002
    assert EXPECTED_EVENT_NAMES_WS == EVENT_NAMES_WS
    assert EXPECTED_EVENT_NAMES_WB_INFER == EVENT_NAMES_WB_INFER
    assert EXPECTED_EVENT_NAMES_COST == EVENT_NAMES_COST
    assert EXPECTED_EVENT_NAMES == EVENT_NAMES
    # Union consistency: the alias is exactly the 6-way per-contract concatenation
    # (DTM-0010 — WB_INFER added between WS and COST; the union grows, never reorders).
    assert EVENT_NAMES == (
        EVENT_NAMES_WA00R
        + EVENT_NAMES_WA001
        + EVENT_NAMES_WA002
        + EVENT_NAMES_WS
        + EVENT_NAMES_WB_INFER
        + EVENT_NAMES_COST
    )
    # stale_detected lives in the WA00R set only — referenced, never duplicated.
    assert "stale_detected" in EVENT_NAMES_WA00R
    assert "stale_detected" not in EVENT_NAMES_WA001
    assert "stale_detected" not in EVENT_NAMES_WA002


def test_ws_and_cost_vocabularies_are_the_a6_names_verbatim() -> None:
    """DTM-0009 — the four IC-WS-SYNTH A6 names + the one DL-048 cost event."""
    assert EVENT_NAMES_WS == (
        "claim_extracted",
        "planning_artifact_generated",
        "planning_artifact_regenerated",
        "synthesized_model_updated",
    )
    assert EVENT_NAMES_COST == ("ai_spend_recorded",)
    # cognition_history_record_appended is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" in EVENT_NAMES_WA00R
    assert "cognition_history_record_appended" not in EVENT_NAMES_WS


def test_wb_infer_vocabulary_is_the_two_ic_wb_infer_a6_names_verbatim() -> None:
    """DTM-0010 — the IC-WB-INFER A6 list, exactly, in contract order."""
    assert EVENT_NAMES_WB_INFER == ("finding_detected", "finding_superseded")
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_WB_INFER
    # finding events live in the WB_INFER set only — never leaking into WS/COST.
    assert "finding_detected" not in EVENT_NAMES_WS
    assert "finding_detected" not in EVENT_NAMES_COST


def test_wa002_vocabulary_is_the_five_ic_wa_002_a6_names_verbatim() -> None:
    """DTM-0008 — the IC-WA-002 A6 list, exactly, in contract order."""
    assert EVENT_NAMES_WA002 == (
        "knowledge_promoted",
        "knowledge_versioned",
        "knowledge_superseded",
        "knowledge_archived",
        "knowledge_mutation_recorded",
    )


def test_detection_finds_the_real_retain_stage_call_site() -> None:
    """stages.py (ctx.chr_repo.append) IS detected — the pairing is not vacuous."""
    stages_src = (CODE_ROOT / "backend/orchestration/stages.py").read_text()
    assert module_chr_append_lines(stages_src) != []
    assert module_emits_append_event(stages_src)  # the paired emit CALL


def test_plain_list_append_is_not_flagged() -> None:
    src = "def f(xs):\n    out = []\n    out.append(xs)\n    return out\n"
    assert module_chr_append_lines(src) == []

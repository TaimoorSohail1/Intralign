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
    EXPECTED_EVENT_NAMES_ANALYSIS,
    EXPECTED_EVENT_NAMES_ARTIFACT,
    EXPECTED_EVENT_NAMES_COST,
    EXPECTED_EVENT_NAMES_EVIDENCE,
    EXPECTED_EVENT_NAMES_PROJECT,
    EXPECTED_EVENT_NAMES_WA00R,
    EXPECTED_EVENT_NAMES_WA001,
    EXPECTED_EVENT_NAMES_WA002,
    EXPECTED_EVENT_NAMES_WB_EVAL,
    EXPECTED_EVENT_NAMES_WB_INFER,
    EXPECTED_EVENT_NAMES_RECOMMENDATION,
    EXPECTED_EVENT_NAMES_WC_ADVISE,
    EXPECTED_EVENT_NAMES_WC_FIX,
    EXPECTED_EVENT_NAMES_WS,
    EXPECTED_EVENT_NAMES_WU_ACCEPT,
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
    EVENT_NAMES_ANALYSIS,
    EVENT_NAMES_ARTIFACT,
    EVENT_NAMES_COST,
    EVENT_NAMES_EVIDENCE,
    EVENT_NAMES_PROJECT,
    EVENT_NAMES_WA00R,
    EVENT_NAMES_WA001,
    EVENT_NAMES_WA002,
    EVENT_NAMES_WB_EVAL,
    EVENT_NAMES_WB_INFER,
    EVENT_NAMES_RECOMMENDATION,
    EVENT_NAMES_WC_ADVISE,
    EVENT_NAMES_WC_FIX,
    EVENT_NAMES_WS,
    EVENT_NAMES_WU_ACCEPT,
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
    assert EXPECTED_EVENT_NAMES_WB_EVAL == EVENT_NAMES_WB_EVAL
    assert EXPECTED_EVENT_NAMES_WC_ADVISE == EVENT_NAMES_WC_ADVISE
    assert EXPECTED_EVENT_NAMES_WC_FIX == EVENT_NAMES_WC_FIX
    assert EXPECTED_EVENT_NAMES_WU_ACCEPT == EVENT_NAMES_WU_ACCEPT
    assert EXPECTED_EVENT_NAMES_COST == EVENT_NAMES_COST
    assert EXPECTED_EVENT_NAMES_ANALYSIS == EVENT_NAMES_ANALYSIS
    assert EXPECTED_EVENT_NAMES_RECOMMENDATION == EVENT_NAMES_RECOMMENDATION
    assert EXPECTED_EVENT_NAMES_PROJECT == EVENT_NAMES_PROJECT
    assert EXPECTED_EVENT_NAMES_ARTIFACT == EVENT_NAMES_ARTIFACT
    assert EXPECTED_EVENT_NAMES_EVIDENCE == EVENT_NAMES_EVIDENCE
    assert EXPECTED_EVENT_NAMES == EVENT_NAMES
    # Union consistency: the alias is exactly the 15-way per-contract concatenation
    # (DTM-0034 — PROJECT/ARTIFACT/EVIDENCE appended after RECOMMENDATION; the union
    # grows, never reorders).
    assert EVENT_NAMES == (
        EVENT_NAMES_WA00R
        + EVENT_NAMES_WA001
        + EVENT_NAMES_WA002
        + EVENT_NAMES_WS
        + EVENT_NAMES_WB_INFER
        + EVENT_NAMES_WB_EVAL
        + EVENT_NAMES_WC_ADVISE
        + EVENT_NAMES_WC_FIX
        + EVENT_NAMES_WU_ACCEPT
        + EVENT_NAMES_COST
        + EVENT_NAMES_ANALYSIS
        + EVENT_NAMES_RECOMMENDATION
        + EVENT_NAMES_PROJECT
        + EVENT_NAMES_ARTIFACT
        + EVENT_NAMES_EVIDENCE
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
    # finding events live in the WB_INFER set only — never leaking into WS/EVAL/COST.
    assert "finding_detected" not in EVENT_NAMES_WS
    assert "finding_detected" not in EVENT_NAMES_WB_EVAL
    assert "finding_detected" not in EVENT_NAMES_COST


def test_wb_eval_vocabulary_is_the_five_ic_wb_eval_a6_names_verbatim() -> None:
    """DTM-0011 — the IC-WB-EVAL A6 list, exactly, in contract order."""
    assert EVENT_NAMES_WB_EVAL == (
        "issue_generated",
        "caf_assessed",
        "outcome_confidence_computed",
        "understanding_state_changed",
        "false_confidence_flagged",
    )
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_WB_EVAL
    # Evaluate events live in the WB_EVAL set only — never leaking into WS/INFER/COST.
    for name in EVENT_NAMES_WB_EVAL:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_COST
    # The single ai_spend_recorded is the COST event, reused — not a WB_EVAL event.
    assert "ai_spend_recorded" not in EVENT_NAMES_WB_EVAL


def test_wc_advise_vocabulary_is_the_two_ic_wc_advise_a6_names_verbatim() -> None:
    """DTM-0014 — the IC-WC-ADVISE A6 list, exactly, in contract order."""
    assert EVENT_NAMES_WC_ADVISE == (
        "recommendation_generated",
        "clarification_requested",
    )
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_WC_ADVISE
    # Advise events live in the WC_ADVISE set only — never leaking into other sets.
    for name in EVENT_NAMES_WC_ADVISE:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_WB_EVAL
        assert name not in EVENT_NAMES_COST
    # The single ai_spend_recorded is the COST event, reused — not a WC_ADVISE event.
    assert "ai_spend_recorded" not in EVENT_NAMES_WC_ADVISE
    # DTM-0015 — the SuggestedFix event lives in WC_FIX, not WC_ADVISE.
    assert "suggested_fix_offered" not in EVENT_NAMES_WC_ADVISE


def test_wc_fix_vocabulary_is_the_one_dl047_suggested_fix_name_verbatim() -> None:
    """DTM-0015 — the DL-047 SuggestedFix OBS list, exactly: 'suggested_fix_offered'."""
    assert EVENT_NAMES_WC_FIX == ("suggested_fix_offered",)
    # The per-emission append event is REUSED from WA00R, never duplicated here
    # (a SuggestedFix rides the existing 'recommendation' output_kind).
    assert "cognition_history_record_appended" not in EVENT_NAMES_WC_FIX
    # The fix event lives in the WC_FIX set only — never leaking into other sets.
    for other in (
        EVENT_NAMES_WS, EVENT_NAMES_WB_INFER, EVENT_NAMES_WB_EVAL,
        EVENT_NAMES_WC_ADVISE, EVENT_NAMES_COST,
    ):
        assert "suggested_fix_offered" not in other
    # The single ai_spend_recorded is the COST event, reused — not a WC_FIX event.
    assert "ai_spend_recorded" not in EVENT_NAMES_WC_FIX


def test_wu_accept_vocabulary_is_the_three_ic_wu_accept_c3_names_verbatim() -> None:
    """DTM-0016 + DTM-0017 — the IC-WU-ACCEPT C3 list, exactly, in contract order."""
    assert EVENT_NAMES_WU_ACCEPT == (
        "user_acceptance_record_appended",
        "plan_fact_recorded",
        "acceptance_impact_assessed",
    )
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_WU_ACCEPT
    # The capture event lives in WA001 (Perceive's), reused — not a WU_ACCEPT event.
    assert "user_acceptance_captured" in EVENT_NAMES_WA001
    assert "user_acceptance_captured" not in EVENT_NAMES_WU_ACCEPT
    # The acceptance-recording events live in WU_ACCEPT only — never leaking elsewhere.
    for name in EVENT_NAMES_WU_ACCEPT:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_WB_EVAL
        assert name not in EVENT_NAMES_WC_ADVISE
        assert name not in EVENT_NAMES_WC_FIX
        assert name not in EVENT_NAMES_COST
    # The single ai_spend_recorded is the COST event, reused — not a WU_ACCEPT event.
    assert "ai_spend_recorded" not in EVENT_NAMES_WU_ACCEPT


def test_analysis_vocabulary_is_the_three_em_8_8_names_verbatim() -> None:
    """DTM-0032 — the Event Model §8.8 analysis-command list, exactly, in order."""
    assert EVENT_NAMES_ANALYSIS == (
        "fast_analysis_requested",
        "deep_analysis_requested",
        "analysis_cancelled",
    )
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_ANALYSIS
    # Analysis-command events live in the ANALYSIS set only — never leaking elsewhere.
    for name in EVENT_NAMES_ANALYSIS:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_WB_EVAL
        assert name not in EVENT_NAMES_WC_ADVISE
        assert name not in EVENT_NAMES_WC_FIX
        assert name not in EVENT_NAMES_WU_ACCEPT
        assert name not in EVENT_NAMES_COST
    # The run lifecycle (started/completed) rides the recompute backbone (WA00R),
    # not a command event — those names are NOT in this command vocabulary.
    assert "fast_analysis_started" not in EVENT_NAMES
    assert "deep_analysis_completed" not in EVENT_NAMES


def test_recommendation_vocabulary_is_the_four_em_8_11_names_verbatim() -> None:
    """DTM-0033 — the Event Model §8.11 recommendation-command list, exactly, in order."""
    assert EVENT_NAMES_RECOMMENDATION == (
        "recommendation_accepted",
        "recommendation_rejected",
        "recommendation_deferred",
        "recommendation_implemented",
    )
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    assert "cognition_history_record_appended" not in EVENT_NAMES_RECOMMENDATION
    # Recommendation-command events live in the RECOMMENDATION set only.
    for name in EVENT_NAMES_RECOMMENDATION:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_WB_EVAL
        assert name not in EVENT_NAMES_WC_ADVISE
        assert name not in EVENT_NAMES_WC_FIX
        assert name not in EVENT_NAMES_WU_ACCEPT
        assert name not in EVENT_NAMES_COST
        assert name not in EVENT_NAMES_ANALYSIS
    # ``recommendation_generated`` (the engine emission) lives in WC_ADVISE, not here.
    assert "recommendation_generated" in EVENT_NAMES_WC_ADVISE
    assert "recommendation_generated" not in EVENT_NAMES_RECOMMENDATION


def test_project_artifact_evidence_command_vocabularies_are_verbatim() -> None:
    """DTM-0034 — the EM §5/§6/§7 command vocabularies, exactly, in contract order."""
    assert EVENT_NAMES_PROJECT == (
        "project_created",
        "project_updated",
        "project_archived",
    )
    assert EVENT_NAMES_ARTIFACT == ("artifact_created", "artifact_version_created")
    assert EVENT_NAMES_EVIDENCE == ("evidence_added",)
    # The per-emission append event is REUSED from WA00R, never duplicated here.
    for s in (EVENT_NAMES_PROJECT, EVENT_NAMES_ARTIFACT, EVENT_NAMES_EVIDENCE):
        assert "cognition_history_record_appended" not in s
    # These command events live in their own sets only — never leaking elsewhere.
    for name in EVENT_NAMES_PROJECT + EVENT_NAMES_ARTIFACT + EVENT_NAMES_EVIDENCE:
        assert name not in EVENT_NAMES_WS
        assert name not in EVENT_NAMES_WB_INFER
        assert name not in EVENT_NAMES_WB_EVAL
        assert name not in EVENT_NAMES_WC_ADVISE
        assert name not in EVENT_NAMES_WU_ACCEPT
        assert name not in EVENT_NAMES_ANALYSIS
        assert name not in EVENT_NAMES_RECOMMENDATION
    # The engine-produced artifact_received/artifact_modified (WA001) and
    # context_item_* (extraction) are NOT these command events.
    assert "artifact_received" in EVENT_NAMES_WA001
    assert "artifact_received" not in EVENT_NAMES_ARTIFACT
    assert "artifact_updated" not in EVENT_NAMES  # a later state-command slice


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

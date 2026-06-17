"""QA-WB-INFER B3 (recompute + mode/stage invariants) — the Critical negatives.

- a Cognition History Record CANNOT be overwritten (append-only repo, Critical);
- a Finding CANNOT change outside recompute / its CHR CANNOT be overwritten
  (Critical) — a recompute APPENDS, it never shrinks/mutates history;
- ``confidence_stage`` CANNOT regress or change without recompute (Critical);
- the Deep Pass CANNOT block the user (orientation Findings produced first);
- ``mode``/``confidence_stage`` are ATTRIBUTES, never new objects (Critical).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.responsibilities.infer.finding_stage import (
    OUTPUT_KIND_FINDING,
    run_finding_stage,
)
from backend.responsibilities.retain import CognitionHistoryRecord
from shared.epistemic import Finding
from tests.positive.infer_finding.helpers import (
    ASSERTION_IDS,
    DECLARED_OUTCOME,
    OUTCOME_ANCHOR,
    PROJECT,
    finding_engine,
    sample_drafts,
    synthesized_model,
)
from tests.positive.synthesis.fakes import AppendOnlyFakeChrRepo, FakeStageContext


def _run(ctx, **kw):
    engine, _ = finding_engine(
        mode=kw.pop("mode", "fast"),
        confidence_stage=kw.pop("confidence_stage", "orientation"),
    )
    return run_finding_stage(
        engine=engine, project_id=PROJECT, assertions=sample_drafts(),
        assertion_ids=ASSERTION_IDS, ctx=ctx, input_attestation_version=kw.pop("version", "v"),
        recompute_trigger=kw.pop("trigger", "knowledge-change"), is_recompute=kw.pop("is_recompute", False),
        model=synthesized_model(), declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR, **kw,
    )


def test_b3_chr_repo_has_no_overwrite_surface() -> None:
    """CRITICAL (CHR overwrite) — the append-only repo exposes no mutation method."""
    repo = AppendOnlyFakeChrRepo()
    for mutator in ("update", "delete", "upsert", "overwrite", "set", "replace"):
        assert not hasattr(repo, mutator)


def test_b3_recompute_appends_never_reduces_history() -> None:
    """CRITICAL — a recompute APPENDS; the prior CHR count never shrinks."""
    ctx = FakeStageContext()
    _run(ctx, is_recompute=False, version="v1")
    before = len(ctx.chr_repo.rows)
    assert before > 0
    _run(ctx, is_recompute=True, version="v2", trigger="knowledge-change")
    assert len(ctx.chr_repo.rows) == before * 2  # appended, never replaced


def test_b3_appended_finding_chr_cannot_be_overwritten_via_returned_row() -> None:
    """The returned record is independent — mutating it never touches storage.

    The real repo (and the fake) re-validate a NEW model from the stored row;
    mutating the returned model's payload must not reach the stored row.
    """
    repo = AppendOnlyFakeChrRepo()
    persisted = repo.append(
        CognitionHistoryRecord(
            project_id=PROJECT,
            output_kind=OUTPUT_KIND_FINDING,
            output_payload={"summary": "original"},
            input_attestation_version="v1",
            model_or_rule_version={"model_version": "v0"},
            upstream_lineage={},
            recompute_trigger="knowledge-change",
            provenance_ref={"emitted_by": "test"},
        )
    )
    persisted.output_payload["summary"] = "tampered"
    stored = repo.rows_for_kind(OUTPUT_KIND_FINDING)[0]
    assert stored["output_payload"]["summary"] == "original"


def test_b3_confidence_stage_cannot_change_on_a_frozen_finding() -> None:
    """CRITICAL — stage changes only via recompute (a new emission), never in place."""
    finding = Finding(
        project_id="p", finding_type="gap", finding_id="g", summary="s",
        evidence_anchors=("a",), model_or_rule_version="v", mode="fast",
        confidence_stage="orientation",
    )
    with pytest.raises(ValidationError):
        finding.confidence_stage = "expanded"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        finding.mode = "deep"  # type: ignore[misc]


def test_b3_deep_pass_does_not_block_orientation_findings() -> None:
    """The Fast Pass produces orientation Findings without waiting on Deep expansion.

    Modeled here as: even when the (Deep) AI passes are deferred under budget,
    the Fast-Pass rule-structural Findings are returned immediately — the user is
    never blocked on the Deep continuation.
    """
    from backend.services.llm_provider import RunBudget

    engine, session = finding_engine(mode="fast")
    result = engine.derive(
        project_id=PROJECT, assertions=sample_drafts(), assertion_ids=ASSERTION_IDS,
        model=synthesized_model(), declared_outcome=DECLARED_OUTCOME,
        outcome_anchor=OUTCOME_ANCHOR, budget=RunBudget(tier="free", mode="fast", cap=1),
    )
    assert result.degraded  # deep expansion deferred
    assert result.of_type("gap") or result.of_type("conflict")  # orientation produced
    assert session.call_count == 0  # the user did not wait on any model call


def test_b3_mode_and_stage_are_attributes_not_objects() -> None:
    """CRITICAL — mode/confidence_stage are plain string attributes, never entities."""
    finding = Finding(
        project_id="p", finding_type="risk", finding_id="r", summary="s",
        evidence_anchors=("a",), model_or_rule_version="v", mode="deep",
        confidence_stage="expanded",
    )
    assert isinstance(finding.mode, str)
    assert isinstance(finding.confidence_stage, str)
    # No "Mode"/"ConfidenceStage" object is exported as a constructable entity.
    import shared.epistemic as epistemic

    for symbol in ("Mode", "ConfidenceStage", "UnderstandingState", "FindingType"):
        obj = getattr(epistemic, symbol)
        # These are typing Literals (aliases), not BaseModel subclasses.
        assert not (isinstance(obj, type) and hasattr(obj, "model_fields"))


def test_b3_unknown_finding_event_is_rejected_by_the_emitter() -> None:
    """An event name outside the WB-INFER A6 vocabulary is rejected (events are contract surface)."""
    from backend.services.observability.events import (
        CollectingEventEmitter,
        UnknownEventError,
    )

    emitter = CollectingEventEmitter()
    with pytest.raises(UnknownEventError):
        emitter.emit("finding_resolved", {})  # not a contract event

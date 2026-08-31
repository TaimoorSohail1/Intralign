"""DTM-0006 positive — LangSmith run linkage on retained CHRs (DL-054 cond.1). Pure.

When LANGSMITH_TRACING=true and a run id exists, the retain stage merges
``langsmith_run_id`` into ``model_or_rule_version`` on every CHR it appends.
Uses a stub repository — linkage is wiring, not persistence.
"""

from __future__ import annotations

import uuid

from backend.orchestration.stages import StageContext, retain_stage
from backend.orchestration.state import GraphState
from backend.services.observability.events import CollectingEventEmitter
from backend.services.observability.langsmith_linkage import (
    langsmith_run_linkage,
    langsmith_tracing_enabled,
)


class _CapturingRepo:
    def __init__(self) -> None:
        self.appended = []

    def append(self, record):
        self.appended.append(record)
        return record


def _state(run_id: str | None) -> GraphState:
    return GraphState(
        project_id=str(uuid.uuid4()),
        run_id=run_id,
        trigger={"trigger_type": "reanalysis"},
        emissions=[
            {
                "output_kind": "finding",
                "output_payload": {"summary": "linkage test"},
                "input_attestation_version": "v1",
                "model_or_rule_version": {"provider": "openai", "model": "gpt-x"},
                "upstream_lineage": {"chr_ids": []},
                "provenance_ref": {"emitted_by": "dtm-0006-tests"},
            }
        ],
        cognition_state="reanalyzing",
    )


def test_linkage_helper_emits_key_only_when_enabled_and_run_id(monkeypatch) -> None:
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    assert langsmith_tracing_enabled() is True
    assert langsmith_run_linkage("run-1") == {"langsmith_run_id": "run-1"}
    assert langsmith_run_linkage(None) == {}  # run id absent — allowed (A3)

    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    assert langsmith_tracing_enabled() is False
    assert langsmith_run_linkage("run-1") == {}


def test_retained_chr_carries_langsmith_run_id_when_tracing(monkeypatch) -> None:
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    repo = _CapturingRepo()
    run_id = str(uuid.uuid4())

    updates = retain_stage(
        _state(run_id), StageContext(emitter=CollectingEventEmitter(), chr_repo=repo)
    )

    assert len(updates["appended_chr_ids"]) == 1
    (record,) = repo.appended
    # Provider/model identity preserved; linkage key ADDED inside it (LDM §2.2).
    assert record.model_or_rule_version == {
        "provider": "openai",
        "model": "gpt-x",
        "langsmith_run_id": run_id,
    }


def test_dev_without_langsmith_appends_chr_without_key(monkeypatch) -> None:
    """A3: tracing disabled (or key absent) is a legitimate dev configuration."""
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    repo = _CapturingRepo()

    retain_stage(
        _state(str(uuid.uuid4())),
        StageContext(emitter=CollectingEventEmitter(), chr_repo=repo),
    )

    (record,) = repo.appended
    assert record.model_or_rule_version == {"provider": "openai", "model": "gpt-x"}
    assert "langsmith_run_id" not in record.model_or_rule_version

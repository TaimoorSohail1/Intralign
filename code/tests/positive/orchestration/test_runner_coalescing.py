"""DTM-0005 positive orchestration suite — trigger coalescing (DL-046: Deep Pass coalesced).

Locked decision: a trigger arriving while a project is Reanalyzing marks it
stale-again with AT MOST ONE queued follow-up (no unbounded queue). The guard is
in-memory, keyed by project_id, for this increment (Redis is the Phase-II-A
follow-up). Runs WITHOUT a database: in-memory checkpointer (explicitly requested
by this test) + a collecting fake repository; never skips.
"""

from __future__ import annotations

import uuid

from backend.orchestration import runner
from backend.orchestration.checkpointer import build_checkpointer
from backend.orchestration.stages import default_stages
from backend.services.observability.events import CollectingEventEmitter


class _CollectingRepo:
    """Append-echo fake standing in for ChrRepository (coalescing needs no DB)."""

    def __init__(self) -> None:
        self.appended = []

    def append(self, record):
        self.appended.append(record)
        return record


def _emission() -> dict:
    return {
        "output_kind": "finding",
        "output_payload": {"summary": "coalescing test"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0005-tests"},
    }


def _trigger(project_id: str, trigger_type: str = "reanalysis") -> dict:
    return {
        "trigger_type": trigger_type,
        "project_id": project_id,
        "information_changed": True,
        "source": "dtm-0005-tests",
        "emissions": [_emission()],
    }


def test_b2_1_burst_of_three_triggers_coalesces_to_one_followup() -> None:
    """Burst of 3 triggers while Reanalyzing -> exactly ONE queued follow-up run."""
    runner.reset_coalescing_guard()
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()
    repo = _CollectingRepo()
    checkpointer = build_checkpointer(in_memory=True)
    burst_outcomes: list = []
    fired = {"done": False}

    def bursting_infer(state, ctx):
        """Simulate 3 triggers arriving while this project is Reanalyzing."""
        if not fired["done"]:
            fired["done"] = True
            for n in range(3):
                burst_outcomes.append(
                    runner.submit_trigger(
                        "deep_pass",
                        _trigger(project_id, "knowledge-change"),
                        checkpointer=checkpointer,
                        emitter=emitter,
                        chr_repo=repo,
                    )
                )
        return {}

    stages = default_stages()
    stages["infer"] = bursting_infer

    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "promotion"),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
        stages=stages,
    )

    # All three burst triggers were coalesced (queued, never run concurrently).
    assert [o.status for o in burst_outcomes] == ["queued", "queued", "queued"]
    # The original run completed, then EXACTLY ONE follow-up ran — and no more.
    assert outcome.status == "completed"
    assert outcome.followup is not None
    assert outcome.followup.status == "completed"
    assert outcome.followup.followup is None
    # Two real runs total (original + single coalesced follow-up).
    assert emitter.names.count("recompute_started") == 2
    assert emitter.names.count("recompute_completed") == 2
    assert len(repo.appended) == 2


def test_triggers_for_other_projects_are_not_coalesced() -> None:
    """The guard is keyed by project_id — an idle project runs immediately."""
    runner.reset_coalescing_guard()
    project_a = str(uuid.uuid4())
    project_b = str(uuid.uuid4())
    emitter = CollectingEventEmitter()
    repo = _CollectingRepo()
    checkpointer = build_checkpointer(in_memory=True)

    first = runner.submit_trigger(
        "deep_pass",
        _trigger(project_a),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    second = runner.submit_trigger(
        "deep_pass",
        _trigger(project_b),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert first.status == "completed"
    assert second.status == "completed"
    assert first.followup is None
    assert second.followup is None

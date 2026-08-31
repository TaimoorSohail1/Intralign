"""C5 trigger/lineage axis — reconstruct trigger -> emissions -> CHRs -> outcome.

Positive (live): a real Deep Pass run is reconstructed from its collected A6
events + the repository; the reconstruction matches what actually happened,
including a resolvable supersession chain (via repo.lineage_chain).

Negative:
- a failed run reconstructs with outcome="failed" and zero emissions (live);
- a broken supersession link (pure, stub repo) raises a Critical-class
  ReplayMismatchError naming supersedes_chr_id.
"""

from __future__ import annotations

import uuid

import pytest

from backend.orchestration import runner
from backend.services.observability.events import CollectingEventEmitter
from tests.replay.conftest import live
from tests.replay.harness import ReplayMismatchError, reconstruct_recompute


def _emission(**overrides) -> dict:
    fields: dict = {
        "output_kind": "finding",
        "output_payload": {"summary": "lineage replay emission"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0006-replay"},
    }
    fields.update(overrides)
    return fields


def _trigger(project_id: str, trigger_type: str, emissions: list[dict]) -> dict:
    return {
        "trigger_type": trigger_type,
        "project_id": project_id,
        "information_changed": True,
        "source": "dtm-0006-replay",
        "emissions": emissions,
    }


@live
def test_full_run_reconstruction_matches_what_happened(repo, checkpointer) -> None:
    """Two chained runs; the second reconstructs exactly, lineage resolvable."""
    project_id = str(uuid.uuid4())

    # Run 1: establishes the prior CHR.
    first = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "promotion", [_emission()]),
        checkpointer=checkpointer,
        emitter=CollectingEventEmitter(),
        chr_repo=repo,
    )
    assert first.status == "completed"
    prior_chr_id = first.state.appended_chr_ids[0]

    # Run 2: supersedes run 1's emission + adds an independent one.
    emitter = CollectingEventEmitter()
    second = runner.submit_trigger(
        "deep_pass",
        _trigger(
            project_id,
            "knowledge-change",
            [
                _emission(supersedes_chr_id=prior_chr_id),
                _emission(output_kind="risk", output_payload={"summary": "risk"}),
            ],
        ),
        base_state=first.state,
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert second.status == "completed"

    rebuilt = reconstruct_recompute(emitter.events, repo)

    # trigger -> emissions -> appended CHR ids -> outcome, all matching reality.
    assert rebuilt.trigger_type == "knowledge-change"
    assert rebuilt.trigger_source == "dtm-0006-replay"
    assert rebuilt.audit.project_id == project_id
    assert rebuilt.audit.run_id == second.state.run_id
    assert rebuilt.appended_chr_ids == second.state.appended_chr_ids
    assert rebuilt.outcome == "completed"
    assert rebuilt.audit.failure is None
    assert [e.output_kind for e in rebuilt.audit.emissions] == ["finding", "risk"]

    # Supersession lineage resolves through repo.lineage_chain: new -> prior.
    superseding_id = second.state.appended_chr_ids[0]
    assert rebuilt.lineage[superseding_id] == [superseding_id, prior_chr_id]
    # Append-not-overwrite auditable: the prior record is still intact.
    assert rebuilt.audit.emissions[0].prior_intact is True


@live
def test_failed_run_reconstructs_with_failed_outcome(repo, checkpointer) -> None:
    project_id = str(uuid.uuid4())
    emitter = CollectingEventEmitter()
    outcome = runner.submit_trigger(
        "deep_pass",
        _trigger(project_id, "reanalysis", [_emission(output_kind="not-a-kind")]),
        checkpointer=checkpointer,
        emitter=emitter,
        chr_repo=repo,
    )
    assert outcome.status == "failed"

    rebuilt = reconstruct_recompute(emitter.events, repo)
    assert rebuilt.outcome == "failed"
    assert rebuilt.audit.failure is not None
    assert rebuilt.audit.failure["stage"] == "retain"
    assert rebuilt.appended_chr_ids == []  # nothing appended by the failed run
    assert rebuilt.trigger_type == "reanalysis"


def test_unresolvable_supersession_is_a_critical_lineage_failure() -> None:
    """Pure negative: a chain that cannot reach the declared predecessor."""
    import tests.replay.test_record_exact_replay as rec

    missing_prior = uuid.uuid4()
    record = rec._record(supersedes_chr_id=missing_prior)

    class _BrokenLineageRepo(rec._StubRepo):
        def lineage_chain(self, chr_id):
            r = self.get(chr_id)
            return [r] if r is not None else []  # predecessor unreachable

    repo = _BrokenLineageRepo(record)
    events = [
        ("reanalysis_triggered", {
            "project_id": str(record.project_id), "run_id": "r1",
            "trigger": "reanalysis", "source": "pure-test",
        }),
        ("recompute_started", {"run_id": "r1"}),
        ("cognition_history_record_appended", {
            "run_id": "r1", "chr_id": str(record.chr_id),
        }),
        ("recompute_completed", {"run_id": "r1"}),
    ]

    with pytest.raises(ReplayMismatchError) as excinfo:
        reconstruct_recompute(events, repo)
    assert excinfo.value.severity == "Critical"
    assert "supersedes_chr_id" in excinfo.value.fields

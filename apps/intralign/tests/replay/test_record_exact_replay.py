"""C5 record-exact axis — append, snapshot, re-read, byte-exact (DTM-0006 D).

Positive (live): a freshly appended CHR replays byte-exactly against its
snapshot (REPLAY_RECORD_TOLERANCE=0).

Negative:
- tamper detection (pure, never skips): a mutated SNAPSHOT (the DB untouched)
  raises a Critical-class ReplayMismatchError naming the differing field;
- a non-zero record tolerance is rejected (the record tier is exact);
- a missing record is itself a Critical replay failure.
"""

from __future__ import annotations

import json
import uuid

import pytest

from backend.responsibilities.retain.models import CognitionHistoryRecord
from tests.replay.conftest import live
from tests.replay.harness import (
    ReplayMismatchError,
    canonical_chr_bytes,
    record_tolerance,
    replay_chr_record,
    snapshot_chr,
)


def _record(**overrides) -> CognitionHistoryRecord:
    fields: dict = {
        "project_id": uuid.uuid4(),
        "recompute_trigger": "reanalysis",
        "output_kind": "finding",
        "output_payload": {"summary": "replay harness emission"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "provenance_ref": {"emitted_by": "dtm-0006-replay"},
    }
    fields.update(overrides)
    return CognitionHistoryRecord(**fields)


class _StubRepo:
    """Pure in-memory get/lineage stand-in for tamper tests (no DB touched)."""

    def __init__(self, *records: CognitionHistoryRecord) -> None:
        self._by_id = {r.chr_id: r for r in records}

    def get(self, chr_id: uuid.UUID) -> CognitionHistoryRecord | None:
        return self._by_id.get(chr_id)


@live
def test_appended_chr_replays_record_exact(repo) -> None:
    """Append -> snapshot -> re-read: canonical bytes identical (tolerance 0)."""
    persisted = repo.append(_record())
    snapshot = snapshot_chr(persisted.chr_id, repo)
    # Byte-exact replay: any diff would raise; None return == exact match.
    assert replay_chr_record(persisted.chr_id, repo, snapshot) is None
    # The snapshot really is the canonical serialization of the stored row.
    assert snapshot == canonical_chr_bytes(repo.get(persisted.chr_id))


def test_default_record_tolerance_is_zero(monkeypatch) -> None:
    monkeypatch.delenv("REPLAY_RECORD_TOLERANCE", raising=False)
    assert record_tolerance() == 0
    monkeypatch.setenv("REPLAY_RECORD_TOLERANCE", "0")
    assert record_tolerance() == 0


def test_tampered_snapshot_reports_critical_mismatch_naming_field() -> None:
    """Negative: mutate the SNAPSHOT (not the store) -> Critical, field named."""
    record = _record()
    repo = _StubRepo(record)
    snapshot = canonical_chr_bytes(record)

    tampered = json.loads(snapshot)
    tampered["output_payload"] = {"summary": "tampered-after-capture"}
    tampered_bytes = json.dumps(
        tampered, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

    with pytest.raises(ReplayMismatchError) as excinfo:
        replay_chr_record(record.chr_id, repo, tampered_bytes)

    err = excinfo.value
    assert err.severity == "Critical"
    assert "Critical" in str(err)
    assert "output_payload" in err.fields  # the differing field is NAMED
    assert "output_payload" in str(err)
    assert err.chr_id == str(record.chr_id)


def test_nonzero_record_tolerance_rejected(monkeypatch) -> None:
    """The record tier is exact — a loosened tolerance is a misconfiguration."""
    monkeypatch.setenv("REPLAY_RECORD_TOLERANCE", "5")
    with pytest.raises(ValueError, match="record tier is exact"):
        record_tolerance()
    record = _record()
    with pytest.raises(ValueError, match="record tier is exact"):
        replay_chr_record(record.chr_id, _StubRepo(record), canonical_chr_bytes(record))


def test_missing_record_is_a_replay_failure() -> None:
    repo = _StubRepo()  # empty store
    with pytest.raises(ReplayMismatchError, match="does not exist"):
        snapshot_chr(uuid.uuid4(), repo)

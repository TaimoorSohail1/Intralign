"""QA-WA-002 §B+ negatives 3/4 — UAR guards (pure).

A User Acceptance Record without its version pin is rejected (B4 Major), and
acceptance-recording can NEVER assert truth: the row shape carries attribution
only, the accepted item is never touched, and the module emits nothing (the
capture event already fired in Perceive).
"""

from __future__ import annotations

import inspect
import uuid

import pytest

from backend.responsibilities.retain.acceptance import (
    AcceptanceRecordingError,
    record_acceptance,
)
from tests.positive.retain_retention.fakes import (
    InMemoryChrReader,
    InMemoryRetentionStore,
)

USER = str(uuid.uuid4())
PIN = str(uuid.uuid4())
PROJECT = str(uuid.uuid4())


def _reader() -> InMemoryChrReader:
    reader = InMemoryChrReader()
    reader.seed(PIN, {"summary": "Confirmed planning content."})
    return reader

# Every field a persisted UAR row may carry — attribution + universals ONLY.
_ALLOWED_UAR_FIELDS = {
    "uar_id",
    "user_id",
    "confirmed_at",
    "action",
    "target_kind",
    "version_pin",
    "rationale",
    "project_id",
    "created_at",
    "created_by",
    "epistemic_state",
    "provenance_ref",
    "version",
    "supersedes_id",
}

# Tokens that would constitute a truth/approval marker (DL-043 amendment 4).
_TRUTH_MARKERS = ("true", "approved", "canonical_as_truth", "valid", "truth")


def _capture_fields(**overrides) -> dict:
    fields = {
        "user_id": USER,
        "target_kind": "recommendation",
        "version_pin": PIN,
        "action": "accept",
        "captured_at": None,
    }
    fields.update(overrides)
    return fields


@pytest.mark.parametrize("pin", [None, "", "   "])
def test_b_plus_4_uar_without_version_pin_rejected(pin) -> None:
    store = InMemoryRetentionStore()
    with pytest.raises(AcceptanceRecordingError, match="version_pin"):
        record_acceptance(
            _capture_fields(version_pin=pin), project_id=PROJECT, store=store
        )
    # Rejected BEFORE anything was written.
    assert store.acceptances == []
    assert store.history == []
    assert store.tables_written == []


def test_uar_without_project_id_rejected() -> None:
    store = InMemoryRetentionStore()
    with pytest.raises(AcceptanceRecordingError, match="project_id"):
        record_acceptance(_capture_fields(), project_id="  ", store=store)
    assert store.tables_written == []


def test_b_plus_3_acceptance_recording_is_never_truth_assertion() -> None:
    """The persisted row carries attribution fields ONLY — no truth/approval
    marker exists anywhere in it (Critical: acceptance-as-truth, C6)."""
    store = InMemoryRetentionStore()
    result = record_acceptance(
        _capture_fields(), project_id=PROJECT, store=store, chr_reader=_reader()
    )
    row = store.get_acceptance(result.uar_id)
    assert set(row) <= _ALLOWED_UAR_FIELDS
    for marker in _TRUTH_MARKERS:
        assert marker not in row, (
            f"UAR row carries truth/approval marker {marker!r} — acceptance "
            "recording is a recorded human decision, never a truth assertion"
        )
    # The recorded action stays the user's ACTION — recording 'reject' or
    # 'defer' goes through the identical path (no approval semantics).
    deferred = record_acceptance(
        _capture_fields(action="defer"), project_id=PROJECT, store=store
    )
    assert store.get_acceptance(deferred.uar_id)["action"] == "defer"


def test_b_plus_3_accepted_item_is_never_mutated() -> None:
    """§B+ negative 3 — the accepted item (assertion/CHR) is decoupled and
    untouched. A reject records the UAR only (DTM-0016: no plan fact), so the
    write footprint is exactly the two UAR tables — the accepted item is never
    mutated by acceptance recording."""
    store = InMemoryRetentionStore()
    record_acceptance(_capture_fields(action="reject"), project_id=PROJECT, store=store)
    assert store.tables_written == ["user_acceptance_record", "history_record"]
    assert store.assertions == []


def test_acceptance_path_takes_an_optional_emitter() -> None:
    """DTM-0016 — the acceptance path now emits its own OBS-WU-ACCEPT events, so
    it takes an OPTIONAL emitter (additive; existing callers keep working)."""
    sig = inspect.signature(record_acceptance)
    assert "emitter" in sig.parameters
    # Optional: default None so Wave-A callers that pass no emitter still work.
    assert sig.parameters["emitter"].default is None

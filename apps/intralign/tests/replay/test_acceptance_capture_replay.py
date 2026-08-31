"""OBS-WA-001 C5 — record-exact replay for acceptance-capture events.

The acceptance capture is a record (tier: exact, tolerance 0): its canonical
serialization must reproduce byte-for-byte, and the emitted
``user_acceptance_captured`` payload must replay byte-identically from the
capture object. Tamper detection mirrors the CHR record-exact axis. Pure —
never skips.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from backend.responsibilities.perceive.acceptance_capture import (
    AcceptanceCapture,
    capture_acceptance,
)
from backend.services.observability.events import CollectingEventEmitter

CAPTURED_AT = datetime(2026, 6, 12, 10, 30, tzinfo=UTC)


def canonical_capture_bytes(capture: AcceptanceCapture) -> bytes:
    """Canonical JSON serialization (sorted keys, compact, UTF-8) — same
    convention as the CHR record-exact axis in tests/replay/harness.py."""
    payload = capture.model_dump(mode="json")
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _capture(emitter=None) -> AcceptanceCapture:
    return capture_acceptance(
        {
            "user_id": "user-42",
            "target_kind": "recommendation",
            "version_pin": "33333333-3333-3333-3333-333333333333",
            "action": "accept",
            "project_id": "11111111-1111-1111-1111-111111111111",
            "captured_at": CAPTURED_AT,
        },
        emitter=emitter if emitter is not None else CollectingEventEmitter(),
    )


def test_acceptance_capture_replays_record_exact() -> None:
    """Same action captured twice -> byte-identical canonical records."""
    snapshot = canonical_capture_bytes(_capture())
    replayed = canonical_capture_bytes(_capture())
    assert replayed == snapshot  # tolerance 0 — the record tier is exact


def test_acceptance_event_payload_replays_from_the_capture() -> None:
    """The emitted event is reconstructable byte-exactly from the record."""
    emitter = CollectingEventEmitter()
    capture = _capture(emitter)
    [(event_name, payload)] = emitter.events
    assert event_name == "user_acceptance_captured"
    rebuilt = {
        "user_id": capture.user_id,
        "target_kind": capture.target_kind,
        "version_pin": capture.version_pin,
        "action": capture.action,
        "project_id": capture.project_id,
        "captured_at": capture.captured_at.isoformat(),
    }
    emitted_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    rebuilt_bytes = json.dumps(rebuilt, sort_keys=True, separators=(",", ":")).encode()
    assert emitted_bytes == rebuilt_bytes


def test_tampered_capture_record_is_detected() -> None:
    """Any field drift between snapshot and replay is visible (Critical, C6)."""
    snapshot = json.loads(canonical_capture_bytes(_capture()))
    tampered = {**snapshot, "version_pin": "00000000-0000-0000-0000-000000000000"}
    assert tampered != snapshot
    differing = [k for k in sorted(snapshot) if snapshot[k] != tampered[k]]
    assert differing == ["version_pin"]  # the drifted field is NAMED

"""QA-WA-001 B2.5 — user-acceptance action CAPTURED with item + version pin.

The capture is a handoff object routed toward Retain (which writes the UAR in
DTM-0008) — Perceive records the action and emits its event, nothing more.
"""

from __future__ import annotations

from backend.responsibilities.perceive.acceptance_capture import (
    AcceptanceCapture,
    capture_acceptance,
)
from backend.services.observability.events import CollectingEventEmitter

PROJECT = "11111111-1111-1111-1111-111111111111"
PINNED_CHR = "33333333-3333-3333-3333-333333333333"


def test_b2_5_acceptance_captured_with_item_and_version_pin() -> None:
    emitter = CollectingEventEmitter()
    capture = capture_acceptance(
        {
            "user_id": "user-42",
            "target_kind": "recommendation",
            "version_pin": PINNED_CHR,
            "action": "accept",
            "project_id": PROJECT,
        },
        emitter=emitter,
    )

    # The handoff object carries the accepted item + the EXACT version pinned.
    assert isinstance(capture, AcceptanceCapture)
    assert capture.target_kind == "recommendation"
    assert capture.version_pin == PINNED_CHR
    assert capture.action == "accept"
    assert capture.captured_at is not None  # time-attributed (A3.8)

    # Evented for OBS C3: item + version reference ride on the event.
    assert emitter.names == ["user_acceptance_captured"]
    payload = emitter.events[0][1]
    assert payload["target_kind"] == "recommendation"
    assert payload["version_pin"] == PINNED_CHR
    assert payload["user_id"] == "user-42"
    assert payload["action"] == "accept"


def test_b2_5_every_acceptance_action_kind_captures() -> None:
    for action in ("accept", "reject", "defer", "direct_edit"):
        capture = capture_acceptance(
            {
                "user_id": "user-42",
                "target_kind": "finding",
                "version_pin": PINNED_CHR,
                "action": action,
            },
            emitter=CollectingEventEmitter(),
        )
        assert capture.action == action

"""QA-WA-001 B4 (Major) — acceptance captured WITHOUT a version reference: rejected.

The capture must name the specific emission/version accepted (A3.5); a pin-less
action is refused before any event is emitted.
"""

from __future__ import annotations

import pytest

from backend.responsibilities.perceive.acceptance_capture import (
    VersionPinMissingError,
    capture_acceptance,
)
from backend.services.observability.events import CollectingEventEmitter


@pytest.mark.parametrize("pin", [None, "", "   "])
def test_b4_major_capture_without_version_pin_is_rejected(pin) -> None:
    emitter = CollectingEventEmitter()
    fields = {
        "user_id": "user-42",
        "target_kind": "recommendation",
        "action": "accept",
        "version_pin": pin,
    }
    if pin is None:
        del fields["version_pin"]
    with pytest.raises(VersionPinMissingError):
        capture_acceptance(fields, emitter=emitter)
    assert emitter.events == []  # nothing emitted on the rejection path


def test_unknown_action_kind_is_rejected() -> None:
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        capture_acceptance(
            {
                "user_id": "user-42",
                "target_kind": "recommendation",
                "version_pin": "33333333-3333-3333-3333-333333333333",
                "action": "approve-as-truth",  # not an LDM §2.4 action
            },
            emitter=CollectingEventEmitter(),
        )

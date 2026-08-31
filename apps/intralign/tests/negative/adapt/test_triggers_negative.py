"""DTM-0005 negative adapt suite — trigger rejections (IC-WA-00R A4.6; QA B3.3).

Anything outside the exact 5-value trigger vocabulary is rejected, and a trigger
WITHOUT an information-change claim is rejected on a dedicated path: intake or
acceptance-capture ALONE never changes an assessment (A4.6) — recompute is the
only assessment-changing event. Pure — never skips.
"""

from __future__ import annotations

import pytest

from backend.responsibilities.adapt.triggers import (
    InvalidTriggerTypeError,
    NoInformationChangeError,
    TriggerValidationError,
    validate_trigger,
)

_PROJECT = "44444444-4444-4444-4444-444444444444"


def _claim(**overrides) -> dict:
    fields: dict = {
        "trigger_type": "promotion",
        "project_id": _PROJECT,
        "information_changed": True,
        "source": "test-suite",
    }
    fields.update(overrides)
    return fields


@pytest.mark.parametrize(
    "bad_type",
    [
        "intake",                 # intake alone is NOT a trigger (A4.6)
        "acceptance-capture",     # acceptance-capture alone is NOT a trigger (A4.6)
        "manual-overwrite",
        "Promotion",              # exact values only — no case folding
        "knowledge_change",       # exact values only — no synonym spelling
        "",
    ],
)
def test_b3_3_invalid_trigger_name_rejected(bad_type: str) -> None:
    """A3.2 — only the 5 contract triggers exist; everything else is rejected."""
    with pytest.raises(InvalidTriggerTypeError):
        validate_trigger(_claim(trigger_type=bad_type))


@pytest.mark.parametrize(
    "trigger_type",
    ["promotion", "knowledge-change", "clarification", "user-action", "reanalysis"],
)
def test_b3_3_trigger_without_information_change_rejected(trigger_type: str) -> None:
    """B3.3 / A4.6 — no information-change claim -> dedicated rejection path.

    A trigger built from intake/acceptance-capture alone carries
    ``information_changed=False`` and MUST be rejected before any recompute.
    """
    with pytest.raises(NoInformationChangeError):
        validate_trigger(_claim(trigger_type=trigger_type, information_changed=False))


def test_information_change_rejection_is_a_distinct_path() -> None:
    """The A4.6 rejection is its own error type (not a generic invalid-trigger)."""
    assert issubclass(NoInformationChangeError, TriggerValidationError)
    assert issubclass(InvalidTriggerTypeError, TriggerValidationError)
    assert not issubclass(NoInformationChangeError, InvalidTriggerTypeError)


def test_missing_information_change_field_rejected() -> None:
    """The information-change claim is mandatory — absence is rejection, not default-True."""
    fields = _claim()
    del fields["information_changed"]
    with pytest.raises(TriggerValidationError):
        validate_trigger(fields)

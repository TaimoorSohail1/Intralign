"""DTM-0005 positive adapt suite — the 5 valid recompute triggers (IC-WA-00R A3.2).

The trigger vocabulary is EXACTLY the five values of the CHR ``recompute_trigger``
CHECK constraint (LDM §2.2); a trigger is only valid when it carries an
information-change claim (A4.6: intake/acceptance-capture alone never triggers).
Pure validation — no database; never skips.
"""

from __future__ import annotations

from typing import get_args

import pytest

from backend.responsibilities.adapt.triggers import (
    VALID_TRIGGER_VALUES,
    TriggerClaim,
    TriggerType,
    validate_trigger,
)
from backend.responsibilities.retain.models import RecomputeTrigger

_PROJECT = "22222222-2222-2222-2222-222222222222"

_ALL_FIVE = ["promotion", "knowledge-change", "clarification", "user-action", "reanalysis"]


def test_trigger_type_enum_is_exactly_the_five_contract_triggers() -> None:
    """A3.2 — exactly five triggers, values matching the CHR CHECK list."""
    assert sorted(t.value for t in TriggerType) == sorted(_ALL_FIVE)
    assert VALID_TRIGGER_VALUES == frozenset(_ALL_FIVE)


def test_trigger_values_match_retain_recompute_trigger_literal() -> None:
    """The adapt trigger vocabulary and the CHR column vocabulary are ONE list."""
    assert {t.value for t in TriggerType} == set(get_args(RecomputeTrigger))


@pytest.mark.parametrize("trigger_value", _ALL_FIVE)
def test_b2_1_each_valid_trigger_validates(trigger_value: str) -> None:
    """B2.1 (validation leg) — each of the 5 valid triggers is accepted."""
    claim = validate_trigger(
        {
            "trigger_type": trigger_value,
            "project_id": _PROJECT,
            "information_changed": True,
            "source": "test-suite",
        }
    )
    assert isinstance(claim, TriggerClaim)
    assert claim.trigger_type is TriggerType(trigger_value)
    assert claim.project_id == _PROJECT
    assert claim.information_changed is True


def test_validate_trigger_accepts_an_already_built_claim() -> None:
    claim = TriggerClaim(
        trigger_type=TriggerType.REANALYSIS,
        project_id=_PROJECT,
        information_changed=True,
    )
    assert validate_trigger(claim) is claim


def test_trigger_claim_carries_declared_emissions() -> None:
    """Emission flow is explicit: the trigger payload declares the emissions."""
    emission = {"output_kind": "finding", "output_payload": {"summary": "s"}}
    claim = validate_trigger(
        {
            "trigger_type": "promotion",
            "project_id": _PROJECT,
            "information_changed": True,
            "emissions": [emission],
        }
    )
    assert claim.emissions == [emission]

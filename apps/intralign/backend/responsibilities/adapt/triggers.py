"""Recompute triggers — the ONLY events allowed to change assessment (IC-WA-00R A3.2).

EXACTLY five valid triggers, values matching the CHR ``recompute_trigger`` CHECK
constraint (LDM §2.2) — adapt's trigger vocabulary and retain's receipt
vocabulary are one list by construction.

A4.6 rule, encoded structurally: intake or acceptance-capture ALONE is NOT a
trigger. Constructing a valid trigger requires an information-change claim
(``information_changed=True``); a claim without it is rejected on a dedicated
path (:class:`NoInformationChangeError`) before any recompute can start.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class TriggerType(str, Enum):
    """The five valid recompute triggers (A3.2; values = CHR CHECK list)."""

    PROMOTION = "promotion"                # promotion of new Attested knowledge
    KNOWLEDGE_CHANGE = "knowledge-change"  # knowledge-changing modification
    CLARIFICATION = "clarification"        # clarification answered
    USER_ACTION = "user-action"            # information-changing user action
    REANALYSIS = "reanalysis"              # explicit/auto reanalysis


VALID_TRIGGER_VALUES: frozenset[str] = frozenset(t.value for t in TriggerType)


class TriggerValidationError(ValueError):
    """Base rejection for anything that is not a valid recompute trigger."""


class InvalidTriggerTypeError(TriggerValidationError):
    """The trigger name is outside the exact five-value vocabulary (A3.2)."""


class NoInformationChangeError(TriggerValidationError):
    """Dedicated A4.6 rejection: no information-change claim.

    Intake/acceptance-capture alone are info capture, not an assessment change —
    recompute is the only assessment-changing event.
    """


class TriggerClaim(BaseModel):
    """A validated request to recompute: trigger type + information-change claim.

    ``emissions`` makes emission flow explicit: the declared emission specs this
    recompute is expected to append receipts for (Wave A: handed to the real
    retain stage; Waves B/C will have Infer/Evaluate/Advise produce them).
    """

    trigger_type: TriggerType
    project_id: str
    information_changed: bool  # mandatory claim — no default (A4.6)
    source: str | None = None
    emissions: list[dict] = Field(default_factory=list)


def validate_trigger(trigger: TriggerClaim | Mapping[str, Any]) -> TriggerClaim:
    """Validate a trigger; return the claim or raise a TriggerValidationError.

    Rejections (must happen BEFORE any state move or recompute):
    - unknown/missing ``trigger_type`` -> :class:`InvalidTriggerTypeError`;
    - ``information_changed`` is not ``True`` -> :class:`NoInformationChangeError`
      (the A4.6 intake/acceptance-alone path);
    - any other malformed claim -> :class:`TriggerValidationError`.
    """
    if isinstance(trigger, TriggerClaim):
        claim = trigger
    else:
        raw_type = trigger.get("trigger_type")
        if raw_type not in VALID_TRIGGER_VALUES:
            raise InvalidTriggerTypeError(
                f"invalid recompute trigger {raw_type!r} — the only valid triggers "
                f"are (A3.2): {', '.join(sorted(VALID_TRIGGER_VALUES))}"
            )
        try:
            claim = TriggerClaim(**dict(trigger))
        except ValidationError as exc:
            raise TriggerValidationError(
                f"malformed trigger claim: {exc}"
            ) from exc
    if claim.information_changed is not True:
        raise NoInformationChangeError(
            "trigger carries no information-change claim — intake/acceptance-"
            "capture alone never changes an assessment (IC-WA-00R A4.6); only "
            "an information-changing event may trigger recompute"
        )
    return claim

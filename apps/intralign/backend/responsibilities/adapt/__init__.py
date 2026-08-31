"""Adapt — act/adapt. Recompute triggers + user-applied changes. A stakeholder response is evidence that triggers a Deep Pass."""

from backend.responsibilities.adapt.states import (
    LEGAL_TRANSITIONS,
    CognitionState,
    CognitionStateMachine,
    IllegalStateTransitionError,
    StateTransitionEvent,
)
from backend.responsibilities.adapt.triggers import (
    VALID_TRIGGER_VALUES,
    InvalidTriggerTypeError,
    NoInformationChangeError,
    TriggerClaim,
    TriggerType,
    TriggerValidationError,
    validate_trigger,
)

__all__ = [
    "LEGAL_TRANSITIONS",
    "VALID_TRIGGER_VALUES",
    "CognitionState",
    "CognitionStateMachine",
    "IllegalStateTransitionError",
    "InvalidTriggerTypeError",
    "NoInformationChangeError",
    "StateTransitionEvent",
    "TriggerClaim",
    "TriggerType",
    "TriggerValidationError",
    "validate_trigger",
]

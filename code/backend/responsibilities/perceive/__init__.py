"""Perceive — intake & perception (IC-WA-00R A3.1 staleness; IC-WA-001 intake).

Captures what was submitted, by whom, when; normalizes meaning-preservingly;
establishes promotion-readiness + integrity; extracts source-attributed
assertion DRAFTS (DL-047 EI-02); captures user-acceptance actions. It never
infers, evaluates, advises, governs, or accepts (A4) — admission is Retain's.
"""

from backend.responsibilities.perceive.acceptance_capture import (
    AcceptanceCapture,
    VersionPinMissingError,
    capture_acceptance,
)
from backend.responsibilities.perceive.extraction import (
    AssertionDraft,
    ClaimExtractor,
    RuleBasedExtractor,
)
from backend.responsibilities.perceive.intake import (
    AttributionMissingError,
    ContextSignal,
    IntakeResult,
    IntakeSubmission,
    compute_dedup_key,
    normalize_content,
    receive_context_signal,
    submit_artifact,
)
from backend.responsibilities.perceive.staleness import (
    StalenessDescriptor,
    StaleSignal,
    detect_staleness,
    is_stale,
)

__all__ = [
    "AcceptanceCapture",
    "AssertionDraft",
    "AttributionMissingError",
    "ClaimExtractor",
    "ContextSignal",
    "IntakeResult",
    "IntakeSubmission",
    "RuleBasedExtractor",
    "StaleSignal",
    "StalenessDescriptor",
    "VersionPinMissingError",
    "capture_acceptance",
    "compute_dedup_key",
    "detect_staleness",
    "is_stale",
    "normalize_content",
    "receive_context_signal",
    "submit_artifact",
]

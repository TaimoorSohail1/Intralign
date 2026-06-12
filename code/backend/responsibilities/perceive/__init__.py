"""Perceive — intake & perception. Produces attested intake provenance (AttestedAssertion)."""

from backend.responsibilities.perceive.staleness import (
    StalenessDescriptor,
    StaleSignal,
    detect_staleness,
    is_stale,
)

__all__ = [
    "StaleSignal",
    "StalenessDescriptor",
    "detect_staleness",
    "is_stale",
]

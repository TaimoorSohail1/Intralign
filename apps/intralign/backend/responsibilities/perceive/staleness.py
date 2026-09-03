"""Stale detection — perceive decides WHEN understanding is out of date (IC-WA-00R A3.1).

Pure functions over input descriptors: a project is stale when canonical
(Attested) knowledge or evidence/inputs changed since the last analysis. The
descriptors arrive in the trigger payload — there is no DB polling here (intake
does not exist yet; DTM-0005 scope). Trigger detection belongs to Perceive
(contract A1); what to DO about staleness is adapt/orchestration.
"""

from __future__ import annotations

from pydantic import BaseModel

# Reason vocabulary for a stale signal (A3.1's two change sources).
REASON_ATTESTED_KNOWLEDGE_CHANGE = "attested-knowledge-change"
REASON_EVIDENCE_CHANGE = "evidence-change"


class StalenessDescriptor(BaseModel):
    """Markers comparing the last analysis against the current inputs.

    A "marker" is an opaque version/watermark string (attestation version,
    content hash, …); equality means unchanged. ``None`` on a last-analyzed
    marker means never analyzed; ``None`` on a current marker means the source
    does not exist (nothing to be stale against).
    """

    project_id: str
    last_analyzed_attested_marker: str | None = None
    current_attested_marker: str | None = None
    last_analyzed_evidence_marker: str | None = None
    current_evidence_marker: str | None = None


class StaleSignal(BaseModel):
    """The Perceive output: this project's cognition is stale, and why."""

    project_id: str
    reasons: list[str]


def _marker_moved(last: str | None, current: str | None) -> bool:
    """A source changed when it exists now and differs from what was analyzed."""
    return current is not None and current != last


def detect_staleness(descriptor: StalenessDescriptor) -> StaleSignal | None:
    """Return a StaleSignal when inputs changed since the last analysis, else None.

    Pure and repeatable — same descriptor, same answer (A3.1).
    """
    reasons: list[str] = []
    if _marker_moved(
        descriptor.last_analyzed_attested_marker, descriptor.current_attested_marker
    ):
        reasons.append(REASON_ATTESTED_KNOWLEDGE_CHANGE)
    if _marker_moved(
        descriptor.last_analyzed_evidence_marker, descriptor.current_evidence_marker
    ):
        reasons.append(REASON_EVIDENCE_CHANGE)
    if not reasons:
        return None
    return StaleSignal(project_id=descriptor.project_id, reasons=reasons)


def is_stale(descriptor: StalenessDescriptor) -> bool:
    """Boolean convenience over :func:`detect_staleness`."""
    return detect_staleness(descriptor) is not None

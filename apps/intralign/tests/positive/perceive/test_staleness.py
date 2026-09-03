"""DTM-0005 positive perceive suite — pure stale detection (IC-WA-00R A3.1; QA-WA-00R B2.5).

Staleness is decided from input descriptors only (last-analyzed markers vs the
current attested-knowledge / evidence markers carried by the trigger payload).
Pure functions — no database, no polling (intake does not exist yet); never skips.
"""

from __future__ import annotations

from backend.responsibilities.perceive.staleness import (
    REASON_ATTESTED_KNOWLEDGE_CHANGE,
    REASON_EVIDENCE_CHANGE,
    StalenessDescriptor,
    StaleSignal,
    detect_staleness,
    is_stale,
)

_PROJECT = "11111111-1111-1111-1111-111111111111"


def _descriptor(**overrides) -> StalenessDescriptor:
    fields: dict = {
        "project_id": _PROJECT,
        "last_analyzed_attested_marker": "att-v1",
        "current_attested_marker": "att-v1",
        "last_analyzed_evidence_marker": "ev-v1",
        "current_evidence_marker": "ev-v1",
    }
    fields.update(overrides)
    return StalenessDescriptor(**fields)


def test_b2_5_stale_detected_on_attested_knowledge_change() -> None:
    """B2.5 / A3.1 — attested-knowledge marker moved since last analysis -> stale."""
    signal = detect_staleness(_descriptor(current_attested_marker="att-v2"))
    assert isinstance(signal, StaleSignal)
    assert signal.project_id == _PROJECT
    assert REASON_ATTESTED_KNOWLEDGE_CHANGE in signal.reasons


def test_b2_5_stale_detected_on_evidence_change() -> None:
    """B2.5 / A3.1 — evidence/input marker moved since last analysis -> stale."""
    signal = detect_staleness(_descriptor(current_evidence_marker="ev-v2"))
    assert signal is not None
    assert signal.reasons == [REASON_EVIDENCE_CHANGE]


def test_b2_5_both_changes_reported_together() -> None:
    signal = detect_staleness(
        _descriptor(current_attested_marker="att-v9", current_evidence_marker="ev-v9")
    )
    assert signal is not None
    assert set(signal.reasons) == {
        REASON_ATTESTED_KNOWLEDGE_CHANGE,
        REASON_EVIDENCE_CHANGE,
    }


def test_no_change_is_not_stale() -> None:
    """Unchanged markers -> no stale signal (recompute is not free-running)."""
    assert detect_staleness(_descriptor()) is None
    assert is_stale(_descriptor()) is False


def test_never_analyzed_with_attested_knowledge_present_is_stale() -> None:
    """No prior analysis marker but attested knowledge exists -> stale."""
    descriptor = _descriptor(
        last_analyzed_attested_marker=None,
        last_analyzed_evidence_marker=None,
        current_evidence_marker=None,
    )
    assert is_stale(descriptor) is True


def test_nothing_to_analyze_is_not_stale() -> None:
    """No markers at all (empty project) -> nothing is stale."""
    descriptor = StalenessDescriptor(project_id=_PROJECT)
    assert detect_staleness(descriptor) is None


def test_detection_is_pure_and_repeatable() -> None:
    """Same descriptor -> same answer; detection holds no state."""
    descriptor = _descriptor(current_attested_marker="att-v2")
    first = detect_staleness(descriptor)
    second = detect_staleness(descriptor)
    assert first is not None and second is not None
    assert first.model_dump() == second.model_dump()

"""DTM-0006 negative — audit assembly refuses an unreconstructable story (C3). Pure.

An event stream that cannot support the C3 audit record (missing trigger,
missing start, missing outcome, ambiguous runs, or an appended CHR that does
not resolve) raises AuditAssemblyError — never a silently-partial record.
"""

from __future__ import annotations

import uuid

import pytest

from backend.services.observability.audit import AuditAssemblyError, audit_view


class _EmptyRepo:
    def get(self, chr_id):
        return None


def _triggered(run_id: str = "r1") -> tuple[str, dict]:
    return (
        "reanalysis_triggered",
        {"project_id": "p1", "run_id": run_id, "trigger": "reanalysis",
         "source": "negative-tests"},
    )


def test_stream_without_trigger_event_rejected() -> None:
    events = [("recompute_started", {"run_id": "r1"}),
              ("recompute_completed", {"run_id": "r1"})]
    with pytest.raises(AuditAssemblyError, match="reanalysis_triggered"):
        audit_view(events, _EmptyRepo())


def test_stream_without_start_event_rejected() -> None:
    events = [_triggered(), ("recompute_completed", {"run_id": "r1"})]
    with pytest.raises(AuditAssemblyError, match="recompute_started"):
        audit_view(events, _EmptyRepo())


def test_stream_without_outcome_rejected() -> None:
    events = [_triggered(), ("recompute_started", {"run_id": "r1"})]
    with pytest.raises(AuditAssemblyError, match="outcome"):
        audit_view(events, _EmptyRepo())


def test_multi_run_stream_without_run_id_rejected() -> None:
    events = [_triggered("r1"), _triggered("r2")]
    with pytest.raises(AuditAssemblyError, match="pass run_id="):
        audit_view(events, _EmptyRepo())


def test_appended_chr_that_does_not_resolve_rejected() -> None:
    """Emission claimed by event but absent from the repo: Major (B4) — loud."""
    events = [
        _triggered(),
        ("recompute_started", {"run_id": "r1"}),
        ("cognition_history_record_appended",
         {"run_id": "r1", "chr_id": str(uuid.uuid4())}),
        ("recompute_completed", {"run_id": "r1"}),
    ]
    with pytest.raises(AuditAssemblyError, match="does not resolve"):
        audit_view(events, _EmptyRepo())

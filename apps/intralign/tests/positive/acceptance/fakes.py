"""In-memory fakes for the DTM-0017 Acceptance-Impact reconcile suites.

The reconcile (``backend.orchestration.wave_u.reconcile_acceptance_impact``)
reads two seams:

- the retention store's ``acceptances_for_project`` (the active UARs), and
- a ``ChrRepository``-shaped CHR seam: ``get`` / ``latest_for_output`` /
  ``append`` / ``latest_acceptance_impact_for_uar``.

These fakes mirror the real append-only behaviour: rows are deep-copied on append
and on read, and the CHR seam has NO update/delete (a recompute APPENDS a new
``acceptance_impact`` CHR carrying ``supersedes_chr_id``; it never mutates the
prior). The accepted item (its UAR + plan-fact rows) is NEVER mutated by the
reconcile — the negative suite proves this against these fakes.
"""

from __future__ import annotations

import copy
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from backend.responsibilities.retain.models import CognitionHistoryRecord


class InMemoryAcceptanceStore:
    """Append-only UAR rows + the ``acceptances_for_project`` read (SELECT only)."""

    def __init__(self) -> None:
        self.acceptances: list[dict[str, Any]] = []

    def add_uar(
        self,
        *,
        version_pin: str,
        action: str = "accept",
        user_id: str | None = None,
        project_id: str,
        target_kind: str = "outcome_confidence",
    ) -> dict[str, Any]:
        """Test setup: place one user_acceptance_record row (append-only)."""
        row = {
            "uar_id": str(uuid.uuid4()),
            "user_id": user_id or str(uuid.uuid4()),
            "action": action,
            "target_kind": target_kind,
            "version_pin": version_pin,
            "project_id": project_id,
            "epistemic_state": "attested-user",
            "created_at": datetime.now(UTC).isoformat(),
        }
        self.acceptances.append(row)
        return copy.deepcopy(row)

    def acceptances_for_project(self, project_id: str) -> list[dict[str, Any]]:
        return [
            copy.deepcopy(r) for r in self.acceptances if r["project_id"] == project_id
        ]


class InMemoryChrRepo:
    """Append-only CHR seam mirroring ``ChrRepository`` (the reconcile's reads).

    Has NO update/delete/upsert — append + read surfaces only. ``seed`` places a
    pre-existing emission (the pinned/latest values the reconcile compares);
    ``append`` records a new CHR and returns it (server fields populated).
    """

    def __init__(self) -> None:
        self.records: list[CognitionHistoryRecord] = []
        self.append_calls: list[CognitionHistoryRecord] = []

    # -- seeding (test setup; not part of the repo surface) -------------------

    def seed(
        self,
        *,
        project_id: str,
        output_kind: str,
        output_payload: Mapping[str, Any],
        chr_id: str | None = None,
        emitted_at: datetime | None = None,
    ) -> CognitionHistoryRecord:
        record = CognitionHistoryRecord(
            chr_id=uuid.UUID(chr_id) if chr_id else uuid.uuid4(),
            project_id=uuid.UUID(project_id),
            output_kind=output_kind,  # type: ignore[arg-type]
            output_payload=dict(output_payload),
            emitted_at=emitted_at or datetime.now(UTC),
            input_attestation_version="v1",
            model_or_rule_version={"provider": "rule", "model_version": "caf-v0"},
            upstream_lineage={},
            recompute_trigger="knowledge-change",
            provenance_ref={"emitted_by": "evaluate"},
        )
        self.records.append(record)
        return record

    # -- the ChrRepository-shaped surface the reconcile uses ------------------

    def get(self, chr_id: Any) -> CognitionHistoryRecord | None:
        for r in self.records:
            if str(r.chr_id) == str(chr_id):
                return r
        return None

    def latest_for_output(
        self, project_id: Any, output_kind: str
    ) -> CognitionHistoryRecord | None:
        matches = [
            r
            for r in self.records
            if str(r.project_id) == str(project_id) and r.output_kind == output_kind
        ]
        if not matches:
            return None
        return max(matches, key=lambda r: (r.emitted_at or datetime.min, str(r.chr_id)))

    def latest_acceptance_impact_for_uar(
        self, project_id: Any, uar_id: str
    ) -> CognitionHistoryRecord | None:
        matches = [
            r
            for r in self.records
            if str(r.project_id) == str(project_id)
            and r.output_kind == "acceptance_impact"
            and str(r.upstream_lineage.get("uar_id")) == str(uar_id)
        ]
        if not matches:
            return None
        return max(matches, key=lambda r: (r.emitted_at or datetime.min, str(r.chr_id)))

    def append(self, record: CognitionHistoryRecord) -> CognitionHistoryRecord:
        # Mirror the real repo: persisted record carries a server emitted_at.
        persisted = record.model_copy(
            update={"emitted_at": record.emitted_at or datetime.now(UTC)}
        )
        self.records.append(persisted)
        self.append_calls.append(persisted)
        return persisted

"""Append-only CHR repository — retain stores receipts, it does not reason (A4.3).

Constraints (IC-WA-00R A3.5/A4.2; LDM §5.1; hard rule #3):
- APPEND-ONLY by construction: this class has NO update/delete/upsert methods —
  not "never called", NOT PRESENT. The negative suite introspects this, and the
  database enforces it underneath (DTM-0002 REVOKE + trigger) for anything that
  bypasses the repository.
- Supersession = ``append`` of a new record carrying ``supersedes_chr_id``.
- No cognition logic here: no payload interpretation, no scoring, no derivation —
  the repository persists and retrieves emission receipts, nothing else.
- Transport is the supabase-py client from ``backend.services.persistence``;
  repositories never construct ad-hoc clients.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from backend.responsibilities.retain.models import CognitionHistoryRecord, OutputKind
from backend.services.persistence import get_supabase_client

if TYPE_CHECKING:
    from supabase import Client

_TABLE = "cognition_history_record"


class ChrRepository:
    """Append + read access to ``cognition_history_record``. Nothing mutates."""

    def __init__(self, client: Client | None = None) -> None:
        """Use the given supabase-py client, or obtain one from the environment."""
        self._client = client if client is not None else get_supabase_client()

    def append(self, record: CognitionHistoryRecord) -> CognitionHistoryRecord:
        """Persist a NEW CHR row and return it with server-assigned fields populated.

        Fields left ``None`` (``emitted_at``, ``created_at``) are omitted so the
        database defaults apply; the returned record reflects the stored row.
        """
        row = record.model_dump(mode="json", exclude_none=True)
        resp = self._client.table(_TABLE).insert(row).execute()
        return CognitionHistoryRecord.model_validate(resp.data[0])

    def get(self, chr_id: uuid.UUID) -> CognitionHistoryRecord | None:
        """Return the CHR with this id, or ``None`` if no such record exists."""
        resp = (
            self._client.table(_TABLE)
            .select("*")
            .eq("chr_id", str(chr_id))
            .limit(1)
            .execute()
        )
        if not resp.data:
            return None
        return CognitionHistoryRecord.model_validate(resp.data[0])

    def latest_for_output(
        self, project_id: uuid.UUID, output_kind: OutputKind
    ) -> CognitionHistoryRecord | None:
        """Return the most recently emitted CHR for (project, output_kind), if any.

        "Most recent" is by ``emitted_at`` (LDM §2.2 emission time) — this is the
        record a live Derived projection should reflect (LDM §3.1
        ``current_chr_ref``), not a mutation target.
        """
        resp = (
            self._client.table(_TABLE)
            .select("*")
            .eq("project_id", str(project_id))
            .eq("output_kind", output_kind)
            .order("emitted_at", desc=True)
            .limit(1)
            .execute()
        )
        if not resp.data:
            return None
        return CognitionHistoryRecord.model_validate(resp.data[0])

    def lineage_chain(self, chr_id: uuid.UUID) -> list[CognitionHistoryRecord]:
        """Walk the ``supersedes_chr_id`` ancestry, most recent first.

        Starts at the given record and follows supersession links until a root
        (``supersedes_chr_id`` is null) or a missing/already-seen id (the seen-set
        guard makes a malformed self-reference terminate instead of looping).
        Returns ``[]`` when the starting id does not exist.
        """
        chain: list[CognitionHistoryRecord] = []
        seen: set[uuid.UUID] = set()
        cursor: uuid.UUID | None = chr_id
        while cursor is not None and cursor not in seen:
            record = self.get(cursor)
            if record is None:
                break
            chain.append(record)
            seen.add(cursor)
            cursor = record.supersedes_chr_id
        return chain

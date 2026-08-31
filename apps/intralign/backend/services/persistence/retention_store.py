"""Supabase-backed retention records (DTM-0008; IC-WA-002) — INSERT/SELECT only.

The Postgres side of canonical retention: ``attested_assertion``,
``user_acceptance_record`` and ``history_record`` (all DTM-0002 append-only
tables), plus read access to ``promotion_candidate`` (admission consumes the
candidate; it never writes one — that is intake's, DTM-0007). This module is
the CONCRETE implementation of the store seam that the retain modules
(``admission`` / ``versioning`` / ``archival`` / ``acceptance``) consume by
injection — retain holds the work, persistence holds the transport.

Append-only discipline (IC-WA-002 A4.7/A4.8; LDM §5.1): this store exposes
INSERT and SELECT surfaces ONLY — no update, no delete, no upsert; NOT PRESENT,
not merely unused (the negative suite introspects this), and the DB REVOKE +
trigger forbids mutation underneath for anything that bypasses it. A new
version is a NEW ``attested_assertion`` row carrying ``supersedes_id``;
archival is a NEW ``history_record`` row — never a row mutation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

ASSERTION_TABLE = "attested_assertion"
ACCEPTANCE_TABLE = "user_acceptance_record"
HISTORY_TABLE = "history_record"
CANDIDATE_TABLE = "promotion_candidate"


class SupabaseRetentionStore:
    """attested_assertion / user_acceptance_record / history_record persistence.

    Insert + select only — canonical retention is append-only by construction.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- promotion candidate (READ only — intake owns the writes) ------------

    def get_candidate(self, candidate_id: str) -> dict[str, Any] | None:
        """The promotion candidate with this id, or None (admission input)."""
        resp = (
            self._client.table(CANDIDATE_TABLE)
            .select("*")
            .eq("candidate_id", candidate_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    # -- attested_assertion (append-only canonical store) --------------------

    def insert_assertion(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Append one attested_assertion row (INSERT only — append-only store)."""
        resp = self._client.table(ASSERTION_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def get_assertion(self, assertion_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(ASSERTION_TABLE)
            .select("*")
            .eq("assertion_id", assertion_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    # -- user_acceptance_record (append-only canonical store) ----------------

    def insert_acceptance(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Append one user_acceptance_record row (INSERT only)."""
        resp = self._client.table(ACCEPTANCE_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def get_acceptance(self, uar_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(ACCEPTANCE_TABLE)
            .select("*")
            .eq("uar_id", uar_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def acceptances_for_project(self, project_id: str) -> list[dict[str, Any]]:
        """All user_acceptance_record rows for a project, oldest first (SELECT only).

        The READ the DTM-0017 reconcile scans for ACTIVE version-pinned UARs after
        a recompute (IC-WU-ACCEPT U1.3). It is a SELECT — the append-only surface
        is unchanged (no update/delete/upsert added); the reconcile is read-only
        over the UAR (it never mutates a row).
        """
        resp = (
            self._client.table(ACCEPTANCE_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .order("created_at", desc=False)
            .execute()
        )
        return list(resp.data)

    # -- history_record (append-only audit trail) ----------------------------

    def insert_history(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Append one history_record row (INSERT only)."""
        resp = self._client.table(HISTORY_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def history_for_assertion(self, assertion_id: str) -> list[dict[str, Any]]:
        """All history entries whose subject is this assertion, oldest first.

        Drives archival-status derivation and the OBS-WA-002 C3/C5 audit
        reconstruction: the lifecycle of any assertion is readable from its
        ordered history entries alone.
        """
        resp = (
            self._client.table(HISTORY_TABLE)
            .select("*")
            .eq("subject_ref->>assertion_id", assertion_id)
            .order("at", desc=False)
            .order("created_at", desc=False)
            .execute()
        )
        return list(resp.data)

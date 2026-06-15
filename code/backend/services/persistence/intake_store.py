"""Supabase-backed intake records (DTM-0007; IC-WA-001) — artifact + candidate.

The Postgres side of intake persistence: the append-only ``artifact`` evidence
anchor and the mutable ``promotion_candidate`` (migration
``20260612100000_intake_artifact_candidate.sql``). This module is the CONCRETE
implementation of the store seam that ``perceive.intake`` consumes by
injection — the perceive responsibility holds the work (pipeline decisions),
persistence holds the transport (hard separation; the B3.5 static scan keeps
direct table access out of responsibility modules).

Append-only discipline: this store only ever INSERTS artifact rows (the DB
REVOKE + trigger forbids mutation anyway); a changed re-submission is a NEW
artifact row with ``version + 1`` and ``supersedes_id`` (LDM §5.1).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

ARTIFACT_TABLE = "artifact"
CANDIDATE_TABLE = "promotion_candidate"


class SupabaseIntakeStore:
    """artifact/promotion_candidate persistence over the Supabase client."""

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- artifact (append-only evidence anchor) ------------------------------

    def find_artifact_by_dedup_key(self, dedup_key: str) -> dict[str, Any] | None:
        """The already-admitted artifact for this dedup_key, or None (A3.3)."""
        resp = (
            self._client.table(ARTIFACT_TABLE)
            .select("*")
            .eq("dedup_key", dedup_key)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def latest_artifact_for_source(
        self, project_id: str, source: str
    ) -> dict[str, Any] | None:
        """The newest artifact this project+source pair admitted, or None.

        Drives change/stale detection (A3.7): a re-submission from the same
        source with different content supersedes this row.
        """
        resp = (
            self._client.table(ARTIFACT_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .eq("provenance->>source", source)
            .order("version", desc=True)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def save_artifact(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Append one artifact row (INSERT only — the anchor is append-only)."""
        resp = self._client.table(ARTIFACT_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def get_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(ARTIFACT_TABLE)
            .select("*")
            .eq("artifact_id", artifact_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    # -- promotion candidate (transient-but-audited, mutable) ----------------

    def save_candidate(self, row: Mapping[str, Any]) -> dict[str, Any]:
        resp = self._client.table(CANDIDATE_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def candidate_for_artifact(self, artifact_id: str) -> dict[str, Any] | None:
        """The newest promotion candidate produced for this artifact, or None."""
        resp = (
            self._client.table(CANDIDATE_TABLE)
            .select("*")
            .eq("artifact_ref", artifact_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

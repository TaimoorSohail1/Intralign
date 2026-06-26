"""Supabase-backed Notification repository (DTM-0031; Data Model v1.2 §13) — read + write.

The Postgres side of the PLATFORM ``notification`` table (migration
``20260626120000_platform_tables.sql``). Mirrors the persistence-service style;
a Supabase client is injected; each method is one PostgREST call.

Epistemic class — PLATFORM awareness, not canonical (code/CLAUDE.md hard rule
#2): notifications are commodity awareness state — they never drive analysis,
carry no epistemic cognition label, and this repo has NO canonical-table surface
and never appends a CHR. ``notification`` is mutable (the view/dismiss state
transitions): ``mark_viewed`` / ``mark_dismissed`` are legitimate UPDATEs.

Workspace scoping (API Contract §3): ``list_for_workspace`` filters by
``workspace_id``. The write methods are consumed by the DTM-0035 notification-
state command slice (``:view`` / ``:dismiss``); this slice provides them.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

NOTIFICATION_TABLE = "notification"


class SupabaseNotificationRepository:
    """``notification`` persistence over the Supabase client — read + write (mutable)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- write (DTM-0035 command slice) -------------------------------------

    def create(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Insert one notification row (workspace-scoped by ``workspace_id`` in ``row``)."""
        resp = self._client.table(NOTIFICATION_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def mark_viewed(self, notification_id: str, viewed_at: str | None = None) -> dict[str, Any]:
        """Transition mutable awareness state ``created`` -> ``viewed`` (platform table)."""
        patch: dict[str, Any] = {"state": "viewed"}
        if viewed_at is not None:
            patch["viewed_at"] = viewed_at
        resp = (
            self._client.table(NOTIFICATION_TABLE)
            .update(patch)
            .eq("notification_id", notification_id)
            .execute()
        )
        return resp.data[0] if resp.data else {}

    def mark_dismissed(
        self, notification_id: str, dismissed_at: str | None = None
    ) -> dict[str, Any]:
        """Transition mutable awareness state -> ``dismissed`` (platform table)."""
        patch: dict[str, Any] = {"state": "dismissed"}
        if dismissed_at is not None:
            patch["dismissed_at"] = dismissed_at
        resp = (
            self._client.table(NOTIFICATION_TABLE)
            .update(patch)
            .eq("notification_id", notification_id)
            .execute()
        )
        return resp.data[0] if resp.data else {}

    # -- read ----------------------------------------------------------------

    def get(self, notification_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(NOTIFICATION_TABLE)
            .select("*")
            .eq("notification_id", notification_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def list_for_workspace(self, workspace_id: str) -> list[dict[str, Any]]:
        """All notifications in a workspace, newest first (workspace-scoped read)."""
        resp = (
            self._client.table(NOTIFICATION_TABLE)
            .select("*")
            .eq("workspace_id", workspace_id)
            .order("created_at", desc=True)
            .execute()
        )
        return list(resp.data)

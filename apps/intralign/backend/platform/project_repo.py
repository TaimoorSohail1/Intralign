"""Supabase-backed Project repository (DTM-0031; Data Model v1.2 §7) — read + write.

The Postgres side of the PLATFORM ``project`` table (migration
``20260626120000_platform_tables.sql``). Mirrors the persistence-service style
(``SupabaseRetentionStore`` / ``SupabaseProjectionStore``): a Supabase client is
injected; every method is one PostgREST call.

Epistemic class — PLATFORM, not canonical (code/CLAUDE.md hard rule #2):

- This repo writes the ``project`` table ONLY. It has NO surface onto a canonical
  table (``attested_assertion`` / ``cognition_history_record`` /
  ``user_acceptance_record`` / ``history_record``) and never appends a CHR — by
  construction, not merely unused (the negative suite introspects this).
- ``project`` is mutable (the lifecycle transitions): ``update_lifecycle`` is a
  legitimate UPDATE — the append-only rule is for the canonical store only.

Workspace scoping (API Contract §3): ``list_for_workspace`` filters by
``workspace_id``; single-row reads are by ``project_id``. The write methods are
consumed by the DTM-0034 project-CRUD command slice; this slice provides them.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from backend.platform import project_fallback

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

PROJECT_TABLE = "project"


class SupabaseProjectRepository:
    """``project`` persistence over the Supabase client — read + write (mutable)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- write (DTM-0034 command slice) -------------------------------------

    def create(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Insert one project row (workspace-scoped by ``workspace_id`` in ``row``)."""
        try:
            resp = self._client.table(PROJECT_TABLE).insert(dict(row)).execute()
            return resp.data[0]
        except Exception as exc:
            if project_fallback.is_missing_project_table(exc):
                return project_fallback.create_project(row)
            raise

    def update_lifecycle(self, project_id: str, lifecycle_state: str) -> dict[str, Any]:
        """Transition the mutable ``lifecycle_state`` (platform table — not append-only)."""
        try:
            resp = (
                self._client.table(PROJECT_TABLE)
                .update({"lifecycle_state": lifecycle_state})
                .eq("project_id", project_id)
                .execute()
            )
            return resp.data[0] if resp.data else {}
        except Exception as exc:
            if project_fallback.is_missing_project_table(exc):
                return project_fallback.update_project(
                    project_id, {"lifecycle_state": lifecycle_state}
                )
            raise

    def update(self, project_id: str, patch: Mapping[str, Any]) -> dict[str, Any]:
        """Patch arbitrary mutable project fields (title/description/etc.)."""
        try:
            resp = (
                self._client.table(PROJECT_TABLE)
                .update(dict(patch))
                .eq("project_id", project_id)
                .execute()
            )
            return resp.data[0] if resp.data else {}
        except Exception as exc:
            if project_fallback.is_missing_project_table(exc):
                return project_fallback.update_project(project_id, patch)
            raise

    # -- read ----------------------------------------------------------------

    def get(self, project_id: str) -> dict[str, Any] | None:
        try:
            resp = (
                self._client.table(PROJECT_TABLE)
                .select("*")
                .eq("project_id", project_id)
                .limit(1)
                .execute()
            )
            return resp.data[0] if resp.data else None
        except Exception as exc:
            if project_fallback.is_missing_project_table(exc):
                return project_fallback.get_project(project_id)
            raise

    def list_for_workspace(self, workspace_id: str) -> list[dict[str, Any]]:
        """All projects in a workspace, newest first (workspace-scoped read)."""
        try:
            resp = (
                self._client.table(PROJECT_TABLE)
                .select("*")
                .eq("workspace_id", workspace_id)
                .order("created_at", desc=True)
                .execute()
            )
            return list(resp.data)
        except Exception as exc:
            if project_fallback.is_missing_project_table(exc):
                return project_fallback.list_projects(workspace_id)
            raise

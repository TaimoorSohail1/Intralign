"""Supabase-backed AnalysisRun repository (DTM-0031; Data Model v1.2 §10) — read + write.

The Postgres side of the PLATFORM ``analysis_run`` table (migration
``20260626120000_platform_tables.sql``). Mirrors the persistence-service style;
a Supabase client is injected; each method is one PostgREST call.

Epistemic class — PLATFORM, not canonical (code/CLAUDE.md hard rule #2): this
repo writes ``analysis_run`` ONLY — no canonical-table surface, never appends a
CHR. ``analysis_run`` is mutable (the run status transitions): ``update_status``
is a legitimate UPDATE (the append-only rule is for the canonical store only).

Project scoping: ``list_for_project`` filters by ``project_id`` (the parent
project carries the workspace; the read seam orders by ``started_at``). The
write methods are consumed by the DTM-0032 analysis-trigger command slice, which
wires them to the existing ``submit_trigger`` orchestration seam.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

ANALYSIS_RUN_TABLE = "analysis_run"


class SupabaseAnalysisRunRepository:
    """``analysis_run`` persistence over the Supabase client — read + write (mutable)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- write (DTM-0032 command slice) -------------------------------------

    def create(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """Insert one analysis_run row (project-scoped by ``project_id`` in ``row``)."""
        resp = self._client.table(ANALYSIS_RUN_TABLE).insert(dict(row)).execute()
        return resp.data[0]

    def update_status(
        self, analysis_run_id: str, run_status: str, **fields: Any
    ) -> dict[str, Any]:
        """Transition the mutable ``run_status`` (+ optional ``completed_at`` etc.).

        Platform table — UPDATE is legitimate here (NOT the append-only canon).
        """
        patch: dict[str, Any] = {"run_status": run_status, **fields}
        resp = (
            self._client.table(ANALYSIS_RUN_TABLE)
            .update(patch)
            .eq("analysis_run_id", analysis_run_id)
            .execute()
        )
        return resp.data[0] if resp.data else {}

    # -- read ----------------------------------------------------------------

    def get(self, analysis_run_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(ANALYSIS_RUN_TABLE)
            .select("*")
            .eq("analysis_run_id", analysis_run_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def list_for_project(self, project_id: str) -> list[dict[str, Any]]:
        """All analysis runs of a project, most-recently started first (scoped read)."""
        resp = (
            self._client.table(ANALYSIS_RUN_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .order("started_at", desc=True)
            .execute()
        )
        return list(resp.data)

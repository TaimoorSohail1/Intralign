"""SELECT-only read seam for the Disclose REST surface (DTM-0018; ADR-0003).

The Disclose read endpoints present the GOVERNED objects Waves A–U produced.
They are read via the EXISTING persistence — never a new write path, never a
mutation, never a migration:

- **Derived cognition** (Finding / Issue / Recommendation / Confidence / CAF /
  Outcome-Confidence / Acceptance-Impact) lives in the live-projection tables
  ``derived.*_current`` (LDM §3.1; migration 20260612090100). Each row carries
  the cognition snapshot (``current_payload``) PLUS the epistemic-safety envelope
  the Disclose contract requires on every object — ``epistemic_label`` /
  ``confidence_value`` / ``confidence_band`` / ``conflict_state`` /
  ``current_chr_ref`` (the lineage to the Cognition History version presented).
  These tables are the DESIGNED read model for presentation (non-canonical,
  rebuildable; Render reads, never writes).
- **Canonical receipts** (UserAcceptanceRecord / Plan Fact) are read through the
  existing append-only retention seam (``user_acceptance_record`` /
  ``attested_assertion``).
- **History** is the Cognition-History supersession chain, read via the existing
  ``ChrRepository.lineage_chain`` / ``get`` (the Retain-owned read methods).

This module exposes a SELECT surface ONLY — no insert/update/delete/upsert. It
is read-mostly transport for presentation; it produces no cognition and appends
no CHR (one-producer / CHR discipline preserved). Every read is workspace-scoped
upstream (``api.deps``) and project-scoped here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

# The ``derived.<kind>_current`` projection table per LDM §2.2 output_kind.
_DERIVED_TABLE = {
    "finding": "finding_current",
    "issue": "issue_current",
    "recommendation": "recommendation_current",
    "clarification": "clarification_current",
    "confidence": "confidence_current",
    "caf": "caf_current",
    "outcome_confidence": "outcome_confidence_current",
    "acceptance_impact": "acceptance_impact_current",
}

ASSERTION_TABLE = "attested_assertion"
ACCEPTANCE_TABLE = "user_acceptance_record"

# Platform tables (Data Model §7/§10/§13). NOTE: these are NOT yet created by a
# migration in this branch (the ``platform`` module is a stub — see the DTM-0018
# worker report escalation). The SELECT surface is defined here so the contract
# (OpenAPI/Orval) is complete and the reads work the moment the platform tables
# land; tests inject a fake reader. No table is invented in SQL by this task.
PROJECT_TABLE = "project"
ANALYSIS_RUN_TABLE = "analysis_run"
NOTIFICATION_TABLE = "notification"


@runtime_checkable
class ProjectionReader(Protocol):
    """The SELECT-only read seam the render mappers + routers depend on.

    Satisfied by :class:`SupabaseProjectionReader` in production and by an
    in-memory fake in tests. It exposes reads ONLY — there is no write method on
    this surface (the read-mostly invariant is structural, not merely unused).
    """

    def list_projection(self, project_id: str, output_kind: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol

    def get_projection(self, output_kind: str, projection_id: str) -> dict[str, Any] | None:
        ...  # pragma: no cover - protocol

    def list_acceptances(self, project_id: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol

    def list_plan_facts(self, project_id: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol

    def list_projects(self, workspace_id: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol

    def get_project(self, project_id: str) -> dict[str, Any] | None:
        ...  # pragma: no cover - protocol

    def list_analysis_runs(self, project_id: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol

    def get_analysis_run(self, analysis_run_id: str) -> dict[str, Any] | None:
        ...  # pragma: no cover - protocol

    def list_notifications(self, workspace_id: str) -> list[dict[str, Any]]:
        ...  # pragma: no cover - protocol


class SupabaseProjectionReader:
    """Concrete SELECT-only reader over the ``derived`` schema + retention tables.

    Uses the single Supabase transport from ``backend.services.persistence``
    (never an ad-hoc client). Every method is a ``select(...)`` — no mutation
    surface exists on this class (read-mostly by construction).
    """

    def __init__(self, client: Client) -> None:
        self._client = client

    # -- derived live-projection reads (LDM §3.1) ----------------------------

    def list_projection(self, project_id: str, output_kind: str) -> list[dict[str, Any]]:
        """All current derived projections of a kind for a project (SELECT only)."""
        table = _DERIVED_TABLE[output_kind]
        resp = (
            self._client.schema("derived")
            .table(table)
            .select("*")
            .eq("project_id", project_id)
            .order("recomputed_at", desc=True)
            .execute()
        )
        return list(resp.data)

    def get_projection(self, output_kind: str, projection_id: str) -> dict[str, Any] | None:
        """One derived projection by id, or None (SELECT only)."""
        table = _DERIVED_TABLE[output_kind]
        resp = (
            self._client.schema("derived")
            .table(table)
            .select("*")
            .eq("projection_id", projection_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    # -- canonical receipts (append-only retention; SELECT only) -------------

    def list_acceptances(self, project_id: str) -> list[dict[str, Any]]:
        """All user_acceptance_record rows for a project, newest first (SELECT only)."""
        resp = (
            self._client.table(ACCEPTANCE_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .order("created_at", desc=True)
            .execute()
        )
        return list(resp.data)

    def list_plan_facts(self, project_id: str) -> list[dict[str, Any]]:
        """User-attested plan facts (attested_assertion, attested-user) for a project."""
        resp = (
            self._client.table(ASSERTION_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .eq("epistemic_state", "attested-user")
            .order("created_at", desc=True)
            .execute()
        )
        return list(resp.data)

    # -- platform reads (project / analysis_run / notification; SELECT only) --
    # See the module note: the platform tables are not yet migrated in this
    # branch — these reads are the contract surface, exercised via the fake in
    # tests, ready for the platform tables (DTM-0018 worker-report escalation).

    def list_projects(self, workspace_id: str) -> list[dict[str, Any]]:
        resp = (
            self._client.table(PROJECT_TABLE)
            .select("*")
            .eq("workspace_id", workspace_id)
            .order("created_at", desc=True)
            .execute()
        )
        return list(resp.data)

    def get_project(self, project_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(PROJECT_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def list_analysis_runs(self, project_id: str) -> list[dict[str, Any]]:
        resp = (
            self._client.table(ANALYSIS_RUN_TABLE)
            .select("*")
            .eq("project_id", project_id)
            .order("started_at", desc=True)
            .execute()
        )
        return list(resp.data)

    def get_analysis_run(self, analysis_run_id: str) -> dict[str, Any] | None:
        resp = (
            self._client.table(ANALYSIS_RUN_TABLE)
            .select("*")
            .eq("analysis_run_id", analysis_run_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def list_notifications(self, workspace_id: str) -> list[dict[str, Any]]:
        resp = (
            self._client.table(NOTIFICATION_TABLE)
            .select("*")
            .eq("workspace_id", workspace_id)
            .order("created_at", desc=True)
            .execute()
        )
        return list(resp.data)

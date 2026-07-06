"""Supabase-backed Derived live-projection store (DTM-0030; LDM §3.1) — UPSERT/SELECT.

The Postgres side of the **Derived** read model: the eight ``derived.*_current``
tables (migration ``20260612090100_derived_projection_tables.sql``). This module
is the CONCRETE implementation of the projection-write seam the DTM-0030
materializer consumes by injection — the materializer holds the work (CHR →
projection mapping), persistence holds the transport (hard separation, mirroring
``SupabaseRetentionStore`` / ``SupabaseIntakeStore``).

Epistemic boundary (code/CLAUDE.md hard rules #2/#3; LDM §3.1/§5.6):

- This store writes the **Derived** layer ONLY. It has NO surface onto a
  canonical table (``attested_assertion`` / ``cognition_history_record`` /
  ``user_acceptance_record`` / ``history_record``) — by construction, not merely
  unused. A Derived projection ``carries no authority``; losing it loses nothing
  canonical (it is rebuildable from the latest CHR).
- The ``derived.*_current`` tables are NON-canonical and updatable: a recompute
  appends a NEW canonical CHR (elsewhere, via ``ChrRepository.append``) and
  REPLACES the matching projection row here. That replacement is an ``upsert``
  keyed on ``projection_id`` — never a mutation of a CHR, never a write that
  promotes Derived → Attested (``epistemic_label`` is pinned ``'derived'`` by the
  table CHECK and never set otherwise).
- ``upsert`` is transactionally a single row write (PostgREST ``upsert`` with
  ``on_conflict='projection_id'``): a failed write leaves the prior row intact
  (last-known-good; no partial corruption).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # import-time dependency only for type checkers
    from supabase import Client

# The ``derived.<output_kind>_current`` table per LDM §2.2 output_kind. This is
# the exact set the read seam (``SupabaseProjectionReader``) SELECTs from; the
# store writes the same eight tables and no others (kinds without a derived
# projection table — reliability/alignment/feasibility/risk/… — are not written).
DERIVED_SCHEMA = "derived"
DERIVED_TABLE: dict[str, str] = {
    "finding": "finding_current",
    "issue": "issue_current",
    "recommendation": "recommendation_current",
    "clarification": "clarification_current",
    "confidence": "confidence_current",
    "caf": "caf_current",
    "outcome_confidence": "outcome_confidence_current",
    "acceptance_impact": "acceptance_impact_current",
}


class SupabaseProjectionStore:
    """``derived.*_current`` projection persistence over the Supabase client.

    UPSERT + SELECT only — the Derived layer is a recomputable cache (LDM §3.1).
    There is intentionally NO method on this class that touches a canonical table:
    the write surface is the derived schema alone (hard rule #2 — the boundary is
    structural).
    """

    def __init__(self, client: Client) -> None:
        self._client = client

    @staticmethod
    def supports(output_kind: str) -> bool:
        """True iff ``output_kind`` has a ``derived.*_current`` projection table."""
        return output_kind in DERIVED_TABLE

    def upsert_projection(self, output_kind: str, row: Mapping[str, Any]) -> dict[str, Any]:
        """Replace (or insert) the ``derived.<kind>_current`` row for ``projection_id``.

        Keyed on ``projection_id`` (``on_conflict``): a recompute that recomputes
        the same (project, output_kind, subject) produces the SAME deterministic
        ``projection_id`` and so REPLACES the current row with the new CHR's
        snapshot + envelope — the projection is superseded, the CHR log (canonical,
        elsewhere) grows. A single-row write; a failure leaves the prior row.

        Raises:
            KeyError: if ``output_kind`` has no derived projection table (the
                materializer never calls with an unsupported kind — guard).
        """
        table = DERIVED_TABLE[output_kind]
        resp = (
            self._client.schema(DERIVED_SCHEMA)
            .table(table)
            .upsert(dict(row), on_conflict="projection_id")
            .execute()
        )
        return resp.data[0] if resp.data else dict(row)

    def list_for_project(self, output_kind: str, project_id: str) -> list[dict[str, Any]]:
        """All current projection rows of a kind for a project (SELECT only).

        Used by the rebuild path to find/replace existing rows; the read surface
        for presentation is ``SupabaseProjectionReader`` (a separate SELECT-only
        seam — this store never serves presentation reads).
        """
        table = DERIVED_TABLE[output_kind]
        resp = (
            self._client.schema(DERIVED_SCHEMA)
            .table(table)
            .select("*")
            .eq("project_id", project_id)
            .execute()
        )
        return list(resp.data)

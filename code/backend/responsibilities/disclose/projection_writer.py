"""Projection materializer (DTM-0030; LDM §3.1) — appended CHRs → ``derived.*_current``.

After a wave run appends its Cognition History Records (the canonical receipts,
via the append-only ``ChrRepository``), this materializer **upserts** the live
Derived projection rows the Disclose read seam SELECTs. Per LDM §3.1 — *"recompute
appends a CHR; the live projection is updated in sync; rebuildable from the latest
CHR per (project, output_kind, subject); carries no authority"* — the projection
is a recomputable cache: lose it and ``rebuild_for_project`` restores it from the
CHR log; nothing canonical is lost.

Epistemic boundary (code/CLAUDE.md hard rules #2/#3; LDM §5.6; gate-4):

- Writes the **Derived** layer ONLY, through ``SupabaseProjectionStore``. It NEVER
  writes/mutates a canonical row (``attested_assertion`` /
  ``cognition_history_record`` / ``user_acceptance_record`` / ``history_record``),
  NEVER mutates or re-appends a CHR (it only ``get``s them — read-only over the
  append-only log), and NEVER promotes Derived → Attested: every row it writes
  carries ``epistemic_label='derived'`` (the only value the table CHECK allows).
- It produces NO cognition and appends NO CHR (one-producer discipline): it maps
  an already-emitted CHR snapshot onto the projection shape. The mapping is the
  CHR's ``output_payload`` (``current_payload``) plus the epistemic-safety envelope
  the read seam requires (``confidence_value`` / ``confidence_band`` /
  ``conflict_state`` / ``current_chr_ref``), derived from that same payload.
- The projection row is keyed by a **deterministic** ``projection_id`` —
  ``uuid5(project_id, output_kind, subject)`` — so a recompute of the same
  (project, output_kind, subject) UPSERTs (replaces) the current row with the new
  CHR, while the CHR log grows append-only. List-kinds (finding / issue /
  recommendation / clarification) key on the per-item subject id; singletons
  (confidence / caf / outcome_confidence) key on one row per project;
  ``acceptance_impact`` keys per accepted item (``uar_ref``).
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from backend.responsibilities.evaluate.scoring import band_for
from backend.services.persistence.projection_store import (
    DERIVED_TABLE,
    SupabaseProjectionStore,
)

if TYPE_CHECKING:  # import-time only; runtime never needs these concrete imports
    from backend.responsibilities.retain import ChrRepository
    from backend.responsibilities.retain.models import CognitionHistoryRecord

# Stable namespace for the deterministic projection_id (a fixed UUID — the same
# (project, kind, subject) always yields the same projection_id, so a recompute
# replaces rather than duplicates the live row).
_PROJECTION_NAMESPACE = uuid.UUID("0a5e0b2e-0d30-5d30-8d30-000000000030")

# Output kinds materialized as a SINGLE row per project (one current value), vs
# list-kinds (one row per subject item). acceptance_impact is per accepted item.
_SINGLETON_KINDS = frozenset({"confidence", "caf", "outcome_confidence"})

# The per-kind payload field that identifies the subject of a list-kind row.
_SUBJECT_KEY: dict[str, str] = {
    "finding": "finding_id",
    "issue": "issue_id",
    "recommendation": "recommendation_id",
    "clarification": "clarification_id",
    "acceptance_impact": "uar_ref",
}


def projection_subject(output_kind: str, payload: dict[str, Any]) -> str:
    """The subject identity of a projection row (the upsert key's third part).

    Singletons collapse to one row per project (subject == output_kind). List
    kinds use their per-item id; acceptance_impact uses the accepted item ref.
    Falls back to the output_kind when an id is absent (degenerate single row),
    so a malformed payload never crashes the materialize step.
    """
    if output_kind in _SINGLETON_KINDS:
        return output_kind
    key = _SUBJECT_KEY.get(output_kind, output_kind)
    value = payload.get(key)
    return str(value) if value is not None else output_kind


def projection_id_for(project_id: str, output_kind: str, subject: str) -> str:
    """Deterministic projection_id for (project, output_kind, subject) — uuid5.

    The same triple ALWAYS yields the same id, so a recompute UPSERTs the current
    row (supersession), never appends a duplicate live projection (LDM §3.1).
    """
    name = f"{project_id}|{output_kind}|{subject}"
    return str(uuid.uuid5(_PROJECTION_NAMESPACE, name))


def _confidence_value(payload: dict[str, Any]) -> float | None:
    """The 0–100 index a CHR payload carries (explainability only), if any."""
    for key in ("index", "confidence_value", "value"):
        raw = payload.get(key)
        if isinstance(raw, (int, float)):
            return float(raw)
    return None


def _confidence_band(payload: dict[str, Any], value: float | None) -> str | None:
    """The user-facing band — the payload's own band, else derived from the index.

    Reuses the EVALUATE-owned ``band_for`` (the single band authority; ±3 edge
    guard) so the projection never invents a band the cognition layer would not.
    """
    band = payload.get("band") or payload.get("confidence_band")
    if isinstance(band, str) and band in ("low", "medium", "high"):
        return band
    if value is not None:
        return band_for(value)
    return None


def _conflict_state(payload: dict[str, Any]) -> str:
    """``contested`` iff the snapshot marks a conflict, else ``none`` (LDM §3.1)."""
    explicit = payload.get("conflict_state")
    if isinstance(explicit, str) and explicit in ("none", "contested"):
        return explicit
    finding_type = payload.get("finding_type")
    if finding_type == "conflict" or payload.get("contested") is True:
        return "contested"
    return "none"


def chr_to_projection_row(record: CognitionHistoryRecord) -> dict[str, Any] | None:
    """Map one appended CHR → a ``derived.<kind>_current`` row, or None to skip.

    Returns None when the CHR's ``output_kind`` has no projection table (e.g.
    ``reliability`` / ``risk`` / ``synthesized_planning_model`` — not presented as
    a live projection). The returned row matches the read seam's SELECT shape
    EXACTLY: ``projection_id, project_id, output_kind, current_payload,
    current_chr_ref, epistemic_label, confidence_value, confidence_band,
    conflict_state`` (``recomputed_at`` defaults server-side to ``now()``).
    """
    output_kind = record.output_kind
    if output_kind not in DERIVED_TABLE:
        return None  # kind carries no live projection — nothing to materialize
    payload = dict(record.output_payload)
    project_id = str(record.project_id)
    subject = projection_subject(output_kind, payload)
    value = _confidence_value(payload)
    return {
        "projection_id": projection_id_for(project_id, output_kind, subject),
        "project_id": project_id,
        "output_kind": output_kind,
        "current_payload": payload,
        "current_chr_ref": str(record.chr_id),
        "epistemic_label": "derived",  # PINNED — never attested (hard rule #2)
        "confidence_value": value,
        "confidence_band": _confidence_band(payload, value),
        "conflict_state": _conflict_state(payload),
    }


class ProjectionMaterializer:
    """Upsert ``derived.*_current`` rows from appended CHRs (LDM §3.1).

    Holds the CHR → projection mapping (the work); delegates the write to an
    injected ``SupabaseProjectionStore`` (the transport). The CHR repository is
    READ-only here (``get`` / a project-scoped lister) — the materializer never
    appends or mutates a CHR.
    """

    def __init__(
        self,
        store: SupabaseProjectionStore,
        chr_repo: ChrRepository,
    ) -> None:
        self._store = store
        self._chr_repo = chr_repo

    # -- in-sync materialize (called after a run's CHRs are appended) ---------

    def materialize_chr_ids(self, chr_ids: list[str]) -> list[dict[str, Any]]:
        """Upsert the projection row for each appended CHR id; return the rows written.

        For each id, read the (immutable) CHR and upsert its projection row. A CHR
        whose kind has no projection table is skipped. The whole step is downstream
        of the canonical appends — if it fails, the CHR log and the last-known-good
        projection are intact (no partial cognition was produced here).
        """
        written: list[dict[str, Any]] = []
        for chr_id in chr_ids:
            record = self._chr_repo.get(uuid.UUID(str(chr_id)))
            if record is None:
                continue
            row = chr_to_projection_row(record)
            if row is None:
                continue
            written.append(self._store.upsert_projection(row["output_kind"], row))
        return written

    # -- rebuild (LDM §3.1 "rebuildable from the latest CHR") ----------------

    def rebuild_for_project(self, project_id: str) -> list[dict[str, Any]]:
        """Repopulate ``derived.*_current`` for a project from its latest CHRs.

        Supports the LDM §3.1 "rebuildable" clause and a one-shot backfill: scans
        the append-only CHR log for the project, reduces to the LATEST CHR per
        (output_kind, subject), and upserts each — so a lost/empty projection store
        is restored exactly (and the seeded dev harness can be replaced by real
        data). Read-only over the CHR log; writes the Derived layer only.
        """
        latest = self._latest_chr_per_subject(project_id)
        written: list[dict[str, Any]] = []
        for record in latest:
            row = chr_to_projection_row(record)
            if row is None:
                continue
            written.append(self._store.upsert_projection(row["output_kind"], row))
        return written

    def _latest_chr_per_subject(
        self, project_id: str
    ) -> list[CognitionHistoryRecord]:
        """Latest CHR per (output_kind, subject) for a project, newest emission wins.

        Reads via the injected repository's project-scoped lister when present
        (``chrs_for_project``), else falls back to ``latest_for_output`` per
        materializable kind (covers singletons + the most-recent list item). The
        log is read-only — no append, no mutation."""
        lister = getattr(self._chr_repo, "chrs_for_project", None)
        if callable(lister):
            records: list[CognitionHistoryRecord] = list(lister(project_id))
            by_subject: dict[tuple[str, str], CognitionHistoryRecord] = {}
            for record in sorted(records, key=_emission_sort_key):
                if record.output_kind not in DERIVED_TABLE:
                    continue
                subject = projection_subject(
                    record.output_kind, dict(record.output_payload)
                )
                by_subject[(record.output_kind, subject)] = record  # newest wins
            return list(by_subject.values())

        # Fallback: the frozen ChrRepository exposes latest_for_output per kind.
        latest: list[CognitionHistoryRecord] = []
        for output_kind in DERIVED_TABLE:
            record = self._chr_repo.latest_for_output(
                uuid.UUID(str(project_id)), output_kind  # type: ignore[arg-type]
            )
            if record is not None:
                latest.append(record)
        return latest


def _emission_sort_key(record: CognitionHistoryRecord) -> Any:
    """Sort CHRs oldest→newest so the last write per subject is the newest one."""
    return (record.emitted_at or record.created_at or record.version, record.version)

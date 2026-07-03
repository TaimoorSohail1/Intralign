"""Two-axis replay harness (OBS-WA-00R C5; DTM-0006 part D) — THE determinism harness.

Reusable functions/fixtures the replay tests (and later waves) drive:

- **Record-exact axis** — ``snapshot_chr`` captures a CHR's canonical JSON
  serialization; ``replay_chr_record`` re-reads the record and **byte-compares**
  it against the snapshot. Tier: record/rule = exact (Calibration Defaults,
  ``REPLAY_RECORD_TOLERANCE=0``); ANY diff raises :class:`ReplayMismatchError`
  with ``severity="Critical"`` naming the differing field(s) (determinism drift
  is a trust failure, C6).

- **Trigger/lineage axis** — ``reconstruct_recompute`` rebuilds, from a run's
  collected A6 events plus the repository, the story
  ``trigger -> emissions -> appended CHR ids -> outcome`` (assembled through
  the C3 ``audit_view``) and verifies every supersession link resolves through
  ``repo.lineage_chain`` (append-not-overwrite is auditable AND replayable).

Outcome Drift across the history stream is deliberately NOT failed here — it is
a surfaced product feature (C5/A9), distinct from the determinism-drift trust
failures this harness raises.
"""

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from backend.services.observability.audit import (
    EventStream,
    RecomputeAuditRecord,
    audit_view,
)

ENV_RECORD_TOLERANCE = "REPLAY_RECORD_TOLERANCE"
CRITICAL = "Critical"


class ReplayMismatchError(AssertionError):
    """Critical-class determinism failure: replay does not reproduce the record."""

    severity = CRITICAL

    def __init__(self, message: str, *, chr_id: str | None = None,
                 fields: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.chr_id = chr_id
        self.fields = fields


def record_tolerance() -> int:
    """The record-tier replay tolerance (env ``REPLAY_RECORD_TOLERANCE``; default 0).

    The record/rule tier is EXACT by governance — a non-zero value is a
    misconfiguration and is rejected loudly rather than silently loosening the
    byte-compare.
    """
    raw = os.environ.get(ENV_RECORD_TOLERANCE, "0").strip() or "0"
    tolerance = int(raw)
    if tolerance != 0:
        raise ValueError(
            f"{ENV_RECORD_TOLERANCE}={tolerance} — the record tier is exact "
            "(Calibration Defaults): only 0 is a legal record tolerance"
        )
    return tolerance


def canonical_chr_bytes(record: Any) -> bytes:
    """Canonical JSON serialization of a CHR (sorted keys, compact, UTF-8)."""
    payload = record.model_dump(mode="json")
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def snapshot_chr(chr_id: uuid.UUID | str, repo: Any) -> bytes:
    """Capture the canonical byte snapshot of the CHR with this id."""
    record = repo.get(uuid.UUID(str(chr_id)))
    if record is None:
        raise ReplayMismatchError(
            f"CHR {chr_id} does not exist — nothing to snapshot",
            chr_id=str(chr_id),
        )
    return canonical_chr_bytes(record)


def _diff_fields(expected: bytes, actual: bytes) -> tuple[str, ...]:
    """Name the top-level fields that differ between two canonical snapshots."""
    try:
        left: Mapping[str, Any] = json.loads(expected)
        right: Mapping[str, Any] = json.loads(actual)
    except (ValueError, TypeError):
        return ("<unparseable snapshot>",)
    keys = sorted(set(left) | set(right))
    return tuple(k for k in keys if left.get(k, ...) != right.get(k, ...))


def replay_chr_record(chr_id: uuid.UUID | str, repo: Any, snapshot: bytes) -> None:
    """Record-exact replay: re-read the CHR; byte-compare against ``snapshot``.

    Raises:
        ReplayMismatchError: (Critical) the record no longer reproduces the
            snapshot — message names the differing field(s) — or the record
            cannot be re-read at all.
    """
    record_tolerance()  # enforce the exact tier before comparing
    current = snapshot_chr(chr_id, repo)
    if current == snapshot:
        return
    fields = _diff_fields(snapshot, current)
    raise ReplayMismatchError(
        f"Critical determinism failure: CHR {chr_id} is not record-exact on "
        f"replay (REPLAY_RECORD_TOLERANCE=0) — differing field(s): "
        f"{', '.join(fields) or '<byte-level>'}",
        chr_id=str(chr_id),
        fields=fields,
    )


@dataclass(frozen=True)
class ReconstructedRecompute:
    """Trigger/lineage replay result: what triggered what, and what it appended."""

    audit: RecomputeAuditRecord
    lineage: dict[str, list[str]] = field(default_factory=dict)  # chr_id -> chain ids

    @property
    def trigger_type(self) -> str:
        return self.audit.trigger_type

    @property
    def trigger_source(self) -> str:
        return self.audit.trigger_source

    @property
    def appended_chr_ids(self) -> list[str]:
        return self.audit.appended_chr_ids

    @property
    def outcome(self) -> str:
        return self.audit.outcome


def reconstruct_recompute(
    events: EventStream, repo: Any, *, run_id: str | None = None
) -> ReconstructedRecompute:
    """Trigger/lineage replay: rebuild trigger -> emissions -> CHRs -> outcome.

    Assembles the C3 audit record from the events, then verifies every appended
    CHR's supersession lineage resolves via ``repo.lineage_chain`` (the chain
    starts at the record itself and reaches its declared predecessor).

    Raises:
        ReplayMismatchError: (Critical) a supersession link that does not
            resolve — history would not be reconstructable.
    """
    audit = audit_view(events, repo, run_id=run_id)
    lineage: dict[str, list[str]] = {}
    for entry in audit.emissions:
        chain = repo.lineage_chain(uuid.UUID(entry.chr_id))
        chain_ids = [str(r.chr_id) for r in chain]
        if not chain_ids or chain_ids[0] != entry.chr_id:
            raise ReplayMismatchError(
                f"Critical lineage failure: CHR {entry.chr_id} does not head "
                f"its own lineage chain (got {chain_ids})",
                chr_id=entry.chr_id,
                fields=("supersedes_chr_id",),
            )
        if entry.supersedes_chr_id is not None and entry.supersedes_chr_id not in chain_ids:
            raise ReplayMismatchError(
                f"Critical lineage failure: CHR {entry.chr_id} declares "
                f"supersedes_chr_id={entry.supersedes_chr_id} but the chain "
                f"{chain_ids} does not resolve it (append-not-overwrite broken?)",
                chr_id=entry.chr_id,
                fields=("supersedes_chr_id",),
            )
        lineage[entry.chr_id] = chain_ids
    return ReconstructedRecompute(audit=audit, lineage=lineage)

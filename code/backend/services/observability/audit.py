"""C3 audit assembly (OBS-WA-00R §3 C3; DTM-0006 part B).

Per recompute, the audit story must be reconstructable: **trigger source**,
**inputs/versions consumed** (``input_attestation_version`` + the full
``model_or_rule_version`` — provider/model identity plus the optional
``langsmith_run_id``), **emissions produced** (→ which CognitionHistoryRecords
were appended), and **outcome** (completed/failed). The append-not-overwrite
property is auditable: every ``supersedes_chr_id`` a record carries must still
resolve to the intact prior record.

``audit_view`` assembles that record from a run's collected A6 events plus the
CHR repository (DTM-0004). It is read-only assembly — no interpretation, no
scoring, no mutation; an event stream that cannot support the C3 story raises
:class:`AuditAssemblyError` loudly instead of returning a partial record.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

# A run's events as collected through the seam: (event_name, payload) pairs —
# exactly the shape CollectingEventEmitter.events holds.
EventStream = Sequence[tuple[str, Mapping[str, Any]]]


class AuditAssemblyError(Exception):
    """The event stream / repository cannot support the C3 audit story."""


@dataclass(frozen=True)
class EmissionAuditEntry:
    """One emission produced by the recompute → the CHR it appended (C3)."""

    chr_id: str
    output_kind: str
    input_attestation_version: str  # which Attested set was consumed
    model_or_rule_version: dict[str, Any]  # provider/model (+ optional langsmith_run_id)
    supersedes_chr_id: str | None
    prior_intact: bool | None  # supersedes target re-read OK (append-not-overwrite)


@dataclass(frozen=True)
class RecomputeAuditRecord:
    """The assembled C3 audit record for one recompute run."""

    project_id: str
    run_id: str
    trigger_type: str  # what triggered the recompute (A3.2 vocabulary)
    trigger_source: str  # who/what raised it (TriggerClaim.source)
    emissions: list[EmissionAuditEntry] = field(default_factory=list)
    appended_chr_ids: list[str] = field(default_factory=list)
    state_transitions: list[tuple[str, str]] = field(default_factory=list)
    outcome: str = "completed"  # "completed" | "failed"
    failure: dict[str, Any] | None = None


def _events_for_run(events: EventStream, run_id: str) -> list[tuple[str, Mapping[str, Any]]]:
    return [(n, p) for n, p in events if p.get("run_id") == run_id]


def _single_run_id(events: EventStream) -> str:
    run_ids = [
        p.get("run_id") for n, p in events if n == "reanalysis_triggered" and p.get("run_id")
    ]
    if not run_ids:
        raise AuditAssemblyError(
            "no 'reanalysis_triggered' event in the stream — a recompute audit "
            "needs its trigger event (C3: trigger source)"
        )
    if len(set(run_ids)) > 1:
        raise AuditAssemblyError(
            f"stream contains {len(set(run_ids))} runs ({sorted(set(run_ids))}) — "
            "pass run_id= to select which recompute to audit"
        )
    return str(run_ids[0])


def audit_view(
    events: EventStream,
    repo: Any,
    *,
    run_id: str | None = None,
) -> RecomputeAuditRecord:
    """Assemble the C3 audit record for one recompute run.

    Args:
        events: collected ``(event_name, payload)`` pairs (seam order preserved).
        repo: the DTM-0004 ``ChrRepository`` (or equivalent ``get(chr_id)``
            provider) the appended records are re-read through.
        run_id: which run to audit; optional when the stream holds exactly one.

    Raises:
        AuditAssemblyError: missing trigger/start/outcome events, an appended
            CHR id that does not resolve, or an ambiguous multi-run stream.
    """
    rid = run_id or _single_run_id(events)
    run_events = _events_for_run(events, rid)

    triggered = [p for n, p in run_events if n == "reanalysis_triggered"]
    if not triggered:
        raise AuditAssemblyError(
            f"run {rid}: no 'reanalysis_triggered' event — trigger source is a "
            "mandatory C3 field"
        )
    trigger = triggered[0]

    if not any(n == "recompute_started" for n, _ in run_events):
        raise AuditAssemblyError(f"run {rid}: no 'recompute_started' event")

    completed = [p for n, p in run_events if n == "recompute_completed"]
    failed = [p for n, p in run_events if n == "recompute_failed"]
    if not completed and not failed:
        raise AuditAssemblyError(
            f"run {rid}: neither 'recompute_completed' nor 'recompute_failed' "
            "observed — outcome is a mandatory C3 field"
        )

    appended_ids = [
        str(p["chr_id"])
        for n, p in run_events
        if n == "cognition_history_record_appended"
    ]

    entries: list[EmissionAuditEntry] = []
    for chr_id in appended_ids:
        record = repo.get(uuid.UUID(chr_id))
        if record is None:
            raise AuditAssemblyError(
                f"run {rid}: appended CHR {chr_id} does not resolve in the "
                "repository — emission without its history record (Major, B4)"
            )
        prior_intact: bool | None = None
        if record.supersedes_chr_id is not None:
            prior_intact = repo.get(record.supersedes_chr_id) is not None
        entries.append(
            EmissionAuditEntry(
                chr_id=chr_id,
                output_kind=record.output_kind,
                input_attestation_version=record.input_attestation_version,
                model_or_rule_version=dict(record.model_or_rule_version),
                supersedes_chr_id=(
                    str(record.supersedes_chr_id) if record.supersedes_chr_id else None
                ),
                prior_intact=prior_intact,
            )
        )

    transitions = [
        (str(p["from_state"]), str(p["to_state"]))
        for n, p in run_events
        if n == "state_transition_occurred"
    ]

    return RecomputeAuditRecord(
        project_id=str(trigger.get("project_id")),
        run_id=rid,
        trigger_type=str(trigger.get("trigger")),
        trigger_source=str(trigger.get("source")),
        emissions=entries,
        appended_chr_ids=appended_ids,
        state_transitions=transitions,
        outcome="failed" if failed else "completed",
        failure=dict(failed[0].get("failure") or {}) if failed else None,
    )

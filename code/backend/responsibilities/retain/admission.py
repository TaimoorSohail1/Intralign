"""Integrity-gated admission (DTM-0008; IC-WA-002 A3.1–A3.3) — Retain owns this.

``admit_candidate`` admits a ready, integrity-cleared Promotion Candidate as
one or more ``attested_assertion`` rows (Knowledge Promoted, initial version).
The gate is INTEGRITY, nothing else (DL-043): admission requires exactly

    (a) ``readiness_state == 'ready'``  AND  (b) ``integrity_clearance`` present

on the candidate — any other state is rejected with
:class:`AdmissionRejectedError` BEFORE anything is written or emitted. There
is no governance gate anywhere in R1 (the governance plane is specified but
inactive); Retain still never self-promotes arbitrary content (only attested
drafts from an integrity-cleared candidate enter).

Provenance is preserved on every admitted row (A3.3/A4.10): ``source_ref``
carries the draft's origin artifact + locus; ``provenance_ref`` carries the
origin artifact, the candidate reference, and the integrity-clearance
reference. Nothing is dropped.

History (A3.6) — admission appends TWO history_record entries (documented
choice: dual events, most faithful to the A6/A7 lifecycle):

- one ``integrity-clearance`` entry per admission, recording WHICH clearance
  admitted WHICH assertions (the C3 integrity-clearance reference);
- one ``knowledge-versioned`` entry per admitted assertion, recording the
  v1 creation (versioning starts at admission — A7 ``Active (v1)``).

Events (A6): ``knowledge_promoted`` then ``knowledge_mutation_recorded``.

Recompute (A3.10): admission CONSTRUCTS a valid 00R ``promotion``
TriggerClaim and hands it back — Retain emits the trigger signal, it never
runs the cascade; only orchestration may submit it (``runner.submit_trigger``).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.responsibilities.perceive.extraction import AssertionDraft
from backend.services.observability.events import CollectingEventEmitter, EventEmitter


class AdmissionRejectedError(ValueError):
    """A3.1 (as amended) guard: admission without readiness + integrity
    clearance is rejected BEFORE anything is persisted or emitted."""


@runtime_checkable
class RetentionStore(Protocol):
    """Postgres seam (INSERT/SELECT only) the retain modules consume.

    The concrete implementation is
    ``backend.services.persistence.retention_store.SupabaseRetentionStore`` —
    append-only by construction: no update/delete surface exists.
    """

    def get_candidate(self, candidate_id: str) -> Mapping[str, Any] | None:
        ...  # pragma: no cover - protocol

    def insert_assertion(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        ...  # pragma: no cover - protocol

    def get_assertion(self, assertion_id: str) -> Mapping[str, Any] | None:
        ...  # pragma: no cover - protocol

    def insert_acceptance(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        ...  # pragma: no cover - protocol

    def insert_history(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        ...  # pragma: no cover - protocol

    def history_for_assertion(self, assertion_id: str) -> list[Mapping[str, Any]]:
        ...  # pragma: no cover - protocol


class AdmissionResult(BaseModel):
    """What one admission produced: the admitted rows + the constructed trigger."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    assertion_ids: list[str]
    assertions: list[dict]
    candidate_id: str
    promotion_trigger: TriggerClaim = Field(
        ...,
        description=(
            "Constructed (NOT submitted) 00R promotion claim — Retain emits "
            "the trigger signal, only orchestration may run it (A3.10)."
        ),
    )


def _resolve_candidate(
    candidate: str | Mapping[str, Any], store: RetentionStore
) -> Mapping[str, Any]:
    if isinstance(candidate, str):
        row = store.get_candidate(candidate)
        if row is None:
            raise AdmissionRejectedError(
                f"admission rejected — promotion candidate {candidate!r} does "
                "not exist (IC-WA-002 A3.1: knowledge enters only after a "
                "Promotion Candidate exists)"
            )
        return row
    return candidate


def _check_integrity_gate(candidate: Mapping[str, Any]) -> dict:
    """The R1 admission gate (DL-043): readiness + integrity clearance, only."""
    readiness = candidate.get("readiness_state")
    if readiness != "ready":
        raise AdmissionRejectedError(
            f"admission rejected — candidate readiness_state is {readiness!r}, "
            "not 'ready': promotion-readiness criteria are not met "
            "(IC-WA-002 A3.1 as amended by DL-043; QA B3.3)"
        )
    clearance = candidate.get("integrity_clearance")
    if not clearance:
        raise AdmissionRejectedError(
            "admission rejected — candidate carries no integrity_clearance: "
            "admission is integrity-gated and must reference the clearance "
            "(IC-WA-002 A3.1 as amended by DL-043; QA B+ negative 6)"
        )
    return dict(clearance)


def admit_candidate(
    candidate: str | Mapping[str, Any],
    drafts: Sequence[AssertionDraft],
    *,
    store: RetentionStore,
    emitter: EventEmitter | None = None,
) -> AdmissionResult:
    """Admit a ready, integrity-cleared candidate as attested_assertion rows.

    One INSERT per draft (initial version, A7 ``Active (v1)``), each carrying
    full provenance + the integrity-clearance reference; dual history entries
    (``integrity-clearance`` once + ``knowledge-versioned`` per assertion);
    ``knowledge_promoted`` + ``knowledge_mutation_recorded`` emitted; a valid
    00R ``promotion`` TriggerClaim constructed and returned (never submitted).

    Raises:
        AdmissionRejectedError: candidate missing, ``readiness_state`` not
            ``'ready'``, ``integrity_clearance`` absent, or no drafts —
            rejected BEFORE any write or event.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    row = _resolve_candidate(candidate, store)
    clearance = _check_integrity_gate(row)
    if not drafts:
        raise AdmissionRejectedError(
            "admission rejected — no assertion drafts to admit: only Attested "
            "Assertions are admitted (IC-WA-002 A3.1); an empty admission "
            "would be a write without content"
        )

    candidate_id = str(row["candidate_id"])
    artifact_ref = str(row.get("artifact_ref"))
    project_id = str(row["project_id"])

    admitted: list[dict] = []
    for draft in drafts:
        persisted = store.insert_assertion(
            {
                "content_type": draft.content_type,
                "proposition": draft.proposition,
                "attesting_source": draft.attesting_source,
                # A3.3: origin artifact + locus (the draft's evidence locus).
                "source_ref": dict(draft.source_ref),
                "re_derivable": draft.re_derivable,
                "version": 1,
                "project_id": project_id,
                "created_by": draft.attesting_source,
                "epistemic_state": draft.epistemic_state,
                # A3.3: candidate ref + integrity-clearance ref — preserved.
                "provenance_ref": {
                    "origin_artifact": artifact_ref,
                    "candidate_ref": candidate_id,
                    "integrity_clearance": clearance,
                    "attesting_source": draft.attesting_source,
                },
            }
        )
        admitted.append(dict(persisted))

    assertion_ids = [str(a["assertion_id"]) for a in admitted]

    # History (A3.6) — dual entries, documented in the module docstring.
    store.insert_history(
        {
            "event_type": "integrity-clearance",
            "subject_ref": {
                "candidate_id": candidate_id,
                "artifact_ref": artifact_ref,
                "assertion_ids": assertion_ids,
                "integrity_clearance": clearance,
            },
            "actor": "retain",
            "project_id": project_id,
            "created_by": "retain",
            "epistemic_state": "attested-evidence",
            "provenance_ref": {"candidate_ref": candidate_id},
        }
    )
    for assertion in admitted:
        store.insert_history(
            {
                "event_type": "knowledge-versioned",
                "subject_ref": {
                    "assertion_id": str(assertion["assertion_id"]),
                    "version": 1,
                    "candidate_id": candidate_id,
                },
                "actor": "retain",
                "project_id": project_id,
                "created_by": "retain",
                "epistemic_state": str(assertion["epistemic_state"]),
                "provenance_ref": dict(assertion["provenance_ref"]),
            }
        )

    audit = {
        "project_id": project_id,
        "candidate_id": candidate_id,
        "artifact_ref": artifact_ref,
        "assertion_ids": assertion_ids,
        "integrity_clearance": clearance,  # C3 integrity-clearance reference
    }
    seam.emit("knowledge_promoted", audit)
    seam.emit(
        "knowledge_mutation_recorded",
        {**audit, "mutation": "promotion", "version": 1},
    )

    # Constructed only — Retain never runs the cascade itself (A3.10).
    promotion_trigger = TriggerClaim(
        trigger_type=TriggerType.PROMOTION,
        project_id=project_id,
        information_changed=True,
        source=f"candidate:{candidate_id}",
    )
    return AdmissionResult(
        assertion_ids=assertion_ids,
        assertions=admitted,
        candidate_id=candidate_id,
        promotion_trigger=promotion_trigger,
    )

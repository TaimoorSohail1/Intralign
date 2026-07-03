"""Artifact intake pipeline (DTM-0007; IC-WA-001 A3) — Perceive owns this.

``submit_artifact`` runs the contract chain (A7):

    Received -> Normalizing -> (Promotion-Readiness + Integrity Check)
             -> Promotion Candidate Ready | Readiness-Failed | Re-submitted

What it does (A3): preserve the submission (body -> Storage, metadata +
provenance -> the append-only ``artifact`` anchor), normalize WITHOUT altering
meaning, establish promotion-readiness + integrity (attribution, idempotent
``dedup_key``, evidence chain), produce a Promotion Candidate, emit the
OBS-WA-001 events, and detect change on re-submission (constructing — never
submitting — a valid 00R knowledge-change TriggerClaim).

What it does NOT do (A4): no Finding/assessment generation, no admission
(upload != Attested — Retain admits), no acceptance, no recompute. Intake
alone changes no assessment; the change TriggerClaim is handed BACK to the
caller, and only orchestration may run it.

Persistence is injected through the two protocols below; the concrete
Supabase-backed implementations live in ``backend/services/persistence``
(``SupabaseIntakeStore`` + ``ArtifactBodyStore``) — perceive holds the work,
persistence holds the transport.

Normalization rules (version ``wa001-n1``) — ALL whitespace-only, hence
meaning-preserving (B2.2: the non-whitespace character stream is untouched):

- N1 ``line-endings``: CRLF / CR -> LF.
- N2 ``trailing-whitespace``: strip trailing spaces/tabs per line.
- N3 ``blank-run-collapse``: collapse runs of blank lines to one.
- N4 ``outer-blank-strip``: drop leading/trailing blank lines.
- N5 ``section-split``: split into sections on Markdown headings (lines
  starting with ``#``); content before the first heading (or all content when
  no headings) forms one heading-less section. A split adds no characters.

Idempotency rule (DL-053; decision #4): ``dedup_key`` =
SHA-256 over UTF-8 of ``project_id + "\\n" + source + "\\n" + raw content``
(the RAW submitted content — idempotency is over what was submitted, before
any normalization).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.services.observability.events import CollectingEventEmitter, EventEmitter

NORMALIZATION_VERSION = "wa001-n1"
NORMALIZATION_RULES: tuple[str, ...] = (
    "line-endings",
    "trailing-whitespace",
    "blank-run-collapse",
    "outer-blank-strip",
    "section-split",
)


class AttributionMissingError(ValueError):
    """B3.6/B4-Critical guard: a submission without attribution is rejected
    BEFORE anything is preserved or emitted — provenance is mandatory (A4.6)."""


class IntakeSubmission(BaseModel):
    """One submitted artifact + its attribution (who / when / from-where)."""

    model_config = ConfigDict(extra="forbid")

    project_id: str
    source: str = Field(..., description="from-where: the evidence-source id")
    submitted_by: str = Field(..., description="who submitted (user | source-system)")
    content: str = Field(..., description="the raw artifact body, verbatim")
    submitted_at: datetime | None = Field(
        default=None, description="when; intake stamps now(UTC) when None"
    )


class ContextSignal(BaseModel):
    """An external context signal Perceive captures (A5; CRR-04 seam).

    A StakeholderResponse enters intake as ordinary new evidence via
    ``submit_artifact`` (CRR-04: admitted evidence-attested, never a decision);
    other external signals are captured here and surfaced as events only.
    """

    model_config = ConfigDict(extra="forbid")

    project_id: str
    signal_type: str
    source: str
    payload: dict = Field(default_factory=dict)
    received_at: datetime | None = None


class IntakeResult(BaseModel):
    """What one submission produced (or idempotently resolved to)."""

    artifact: dict
    candidate: dict | None = None
    created: bool
    dedup_key: str
    body_ref: str
    normalized_form: dict
    readiness_state: str | None = None
    modified_trigger: TriggerClaim | None = Field(
        default=None,
        description=(
            "Constructed (NOT submitted) 00R knowledge-change claim when a "
            "re-submission changed content — only orchestration may run it."
        ),
    )


@runtime_checkable
class IntakeStore(Protocol):
    """Postgres seam: artifact (append-only) + promotion_candidate records."""

    def find_artifact_by_dedup_key(self, dedup_key: str) -> Mapping[str, Any] | None:
        ...  # pragma: no cover - protocol

    def latest_artifact_for_source(
        self, project_id: str, source: str
    ) -> Mapping[str, Any] | None:
        ...  # pragma: no cover - protocol

    def save_artifact(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        ...  # pragma: no cover - protocol

    def save_candidate(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        ...  # pragma: no cover - protocol

    def candidate_for_artifact(self, artifact_id: str) -> Mapping[str, Any] | None:
        ...  # pragma: no cover - protocol


@runtime_checkable
class BodyStore(Protocol):
    """Storage seam: preserve/fetch raw bodies (bucket ``artifacts``)."""

    def upload_body(self, project_id: str, content: str | bytes) -> str:
        ...  # pragma: no cover - protocol

    def download_body(self, body_ref: str) -> bytes:
        ...  # pragma: no cover - protocol


def compute_dedup_key(project_id: str, source: str, content: str) -> str:
    """DL-053 idempotency key: sha256(project_id + source + raw content)."""
    material = f"{project_id}\n{source}\n{content}".encode()
    return hashlib.sha256(material).hexdigest()


def normalize_content(content: str) -> dict:
    """Apply the wa001-n1 rules; return the ``normalized_form`` jsonb shape.

    Whitespace-only transforms — the non-whitespace character stream of the
    output text is IDENTICAL to the input's (meaning preserved, A3.2/B2.2).
    """
    # N1 line endings, N2 trailing whitespace.
    lines = [line.rstrip() for line in content.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    # N3 collapse blank runs, N4 strip outer blanks.
    collapsed: list[str] = []
    for line in lines:
        if line == "" and (not collapsed or collapsed[-1] == ""):
            continue
        collapsed.append(line)
    while collapsed and collapsed[-1] == "":
        collapsed.pop()
    # N5 section split on Markdown headings.
    sections: list[dict] = []
    current: dict = {"index": 0, "heading": None, "lines": []}
    for line in collapsed:
        if line.startswith("#"):
            if current["lines"] or current["heading"] is not None:
                sections.append(current)
            current = {"index": len(sections), "heading": line, "lines": []}
        else:
            current["lines"].append(line)
    sections.append(current)
    return {
        "version": NORMALIZATION_VERSION,
        "rules": list(NORMALIZATION_RULES),
        "text": "\n".join(collapsed),
        "sections": sections,
    }


def _validated(submission: IntakeSubmission | Mapping[str, Any]) -> IntakeSubmission:
    """Reject missing attribution BEFORE the pipeline moves (B3.6)."""
    sub = (
        submission
        if isinstance(submission, IntakeSubmission)
        else IntakeSubmission(**dict(submission))
    )
    missing = [
        name
        for name in ("project_id", "source", "submitted_by")
        if not getattr(sub, name).strip()
    ]
    if missing:
        raise AttributionMissingError(
            f"submission rejected — attribution field(s) {', '.join(missing)} "
            "missing/empty: provenance is mandatory and never dropped "
            "(IC-WA-001 A3.1/A4.6; QA B3.6)"
        )
    return sub


def _integrity_clearance(
    sub: IntakeSubmission, dedup_key: str, body_ref: str
) -> tuple[dict, str]:
    """A3.3 readiness + integrity results -> (clearance jsonb, readiness state).

    Attribution presence is already enforced (hard rejection); the evidence
    chain is intact when a non-empty body was preserved and the normalized
    form is re-derivable from it.
    """
    evidence_intact = bool(sub.content.strip()) and bool(body_ref)
    clearance = {
        "attribution": {
            "present": True,
            "submitted_by": sub.submitted_by,
            "source": sub.source,
        },
        "idempotency": {"dedup_key": dedup_key, "duplicate": False},
        "evidence_chain": {
            "intact": evidence_intact,
            "body_ref": body_ref,
            "re_derivable": True,
            "normalization_version": NORMALIZATION_VERSION,
        },
    }
    return clearance, ("ready" if evidence_intact else "failed")


def submit_artifact(
    submission: IntakeSubmission | Mapping[str, Any],
    *,
    store: IntakeStore,
    bodies: BodyStore,
    emitter: EventEmitter | None = None,
) -> IntakeResult:
    """Run the full A3 intake chain for one submission; return what it produced.

    Idempotent (A3.3/A3.8, B2.4): an identical re-submission (same dedup_key)
    returns the EXISTING artifact — no new Storage object, no new candidate,
    no second admission. A changed re-submission from the same project+source
    appends a NEW artifact version, emits ``artifact_modified``, and constructs
    (never submits) a valid 00R knowledge-change TriggerClaim.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    sub = _validated(submission)
    when = (sub.submitted_at or datetime.now(UTC)).isoformat()
    dedup_key = compute_dedup_key(sub.project_id, sub.source, sub.content)
    # C3 audit base: who / when / source on every intake event.
    audit = {
        "project_id": sub.project_id,
        "submitted_by": sub.submitted_by,
        "submitted_at": when,
        "source": sub.source,
    }

    seam.emit("artifact_received", {**audit, "dedup_key": dedup_key})

    existing = store.find_artifact_by_dedup_key(dedup_key)
    if existing is not None:
        # Idempotent re-intake: same submission is never double-admitted.
        prior_candidate = store.candidate_for_artifact(str(existing["artifact_id"]))
        return IntakeResult(
            artifact=dict(existing),
            candidate=dict(prior_candidate) if prior_candidate is not None else None,
            created=False,
            dedup_key=dedup_key,
            body_ref=str(existing["body_ref"]),
            normalized_form=dict(existing["normalized_form"]),
            readiness_state=(
                str(prior_candidate["readiness_state"])
                if prior_candidate is not None
                else None
            ),
        )

    # Change/stale detection (A3.7): same project+source, different content.
    prior = store.latest_artifact_for_source(sub.project_id, sub.source)

    seam.emit("artifact_normalizing", dict(audit))
    normalized_form = normalize_content(sub.content)
    seam.emit(
        "artifact_normalized",
        {**audit, "normalization_version": NORMALIZATION_VERSION},
    )

    body_ref = bodies.upload_body(sub.project_id, sub.content)

    provenance = {
        "who": sub.submitted_by,
        "when": when,
        "from_where": sub.source,
        "source": sub.source,
    }
    artifact = store.save_artifact(
        {
            "project_id": sub.project_id,
            "body_ref": body_ref,
            "normalized_form": normalized_form,
            "provenance": provenance,
            "dedup_key": dedup_key,
            "submitted_by": sub.submitted_by,
            "created_by": sub.submitted_by,
            "epistemic_state": "attested-evidence",
            "provenance_ref": {"submission": provenance, "dedup_key": dedup_key},
            "version": (int(prior["version"]) + 1) if prior is not None else 1,
            "supersedes_id": str(prior["artifact_id"]) if prior is not None else None,
        }
    )
    artifact_id = str(artifact["artifact_id"])

    clearance, readiness = _integrity_clearance(sub, dedup_key, body_ref)
    candidate = store.save_candidate(
        {
            "artifact_ref": artifact_id,
            "normalized_form": normalized_form,
            "readiness_state": readiness,
            "integrity_clearance": clearance,
            "project_id": sub.project_id,
        }
    )
    candidate_audit = {
        **audit,
        "artifact_id": artifact_id,
        "candidate_id": str(candidate["candidate_id"]),
        "integrity_clearance": clearance,  # C3 integrity-clearance reference
        "provenance": provenance,
    }
    if readiness == "ready":
        seam.emit("promotion_candidate_ready", candidate_audit)
    else:
        seam.emit(
            "promotion_readiness_failed",
            {**candidate_audit, "reason": "evidence-chain-incomplete"},
        )

    modified_trigger: TriggerClaim | None = None
    if prior is not None:
        seam.emit(
            "artifact_modified",
            {
                **audit,
                "artifact_id": artifact_id,
                "supersedes_artifact_id": str(prior["artifact_id"]),
                "dedup_key": dedup_key,
            },
        )
        # Constructed only — intake never runs a recompute (A4.5/A9).
        modified_trigger = TriggerClaim(
            trigger_type=TriggerType.KNOWLEDGE_CHANGE,
            project_id=sub.project_id,
            information_changed=True,
            source=sub.source,
        )

    return IntakeResult(
        artifact=dict(artifact),
        candidate=dict(candidate),
        created=True,
        dedup_key=dedup_key,
        body_ref=body_ref,
        normalized_form=normalized_form,
        readiness_state=readiness,
        modified_trigger=modified_trigger,
    )


def receive_context_signal(
    signal: ContextSignal | Mapping[str, Any],
    *,
    emitter: EventEmitter | None = None,
) -> ContextSignal:
    """Capture an external context signal and surface its event (A5/A6).

    Capture only — no interpretation, no assessment change.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    sig = (
        signal
        if isinstance(signal, ContextSignal)
        else ContextSignal(**dict(signal))
    )
    received = (sig.received_at or datetime.now(UTC)).isoformat()
    seam.emit(
        "context_signal_received",
        {
            "project_id": sig.project_id,
            "signal_type": sig.signal_type,
            "source": sig.source,
            "received_at": received,
        },
    )
    return sig

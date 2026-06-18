"""User Acceptance Record + Plan Fact recording (DTM-0008 + DTM-0016).

``record_acceptance`` turns the Perceive handoff (``AcceptanceCapture``,
DTM-0007) into the canonical, user-attested confirm record(s):

- ALWAYS — one ``user_acceptance_record`` row (DTM-0008; IC-WA-002 §B+):
  "User U, at time T, took action A on item I at version_pin V". It records a
  HUMAN DECISION, nothing more (DL-043 amendment 4): no field marks the accepted
  item true/approved/canonical-as-truth, and the accepted item itself is never
  touched (decoupled — it stays recomputable if Derived). ``version_pin`` is
  MANDATORY (:class:`AcceptanceRecordingError`).
- ON ``accept`` / ``direct_edit`` ONLY (DTM-0016; IC-WU-ACCEPT U1.2) — ALSO one
  ``attested_assertion`` **plan fact**: the confirmed content recorded as
  "factual in the plan, attributed to the user" (``attesting_source=<user_id>``,
  ``epistemic_state=attested-user``). The USER authors it; OSLO never
  auto-promotes its own Derived recommendation and **never self-accepts**
  (hard rule #5). It marks NOTHING world-true/approved/governed/applied.
  Content: for ``accept`` it is the pinned CHR's ``output_payload`` (a DATA read
  via ``chr_reader`` — NO LLM); for ``direct_edit`` it is the capture's
  ``edit_content`` (the user's words). On ``reject`` / ``defer`` NO plan fact is
  written (the UAR records the action, nothing is confirmed as factual).

Events (DTM-0016; OBS-WU-ACCEPT C3): the UAR write emits
``user_acceptance_record_appended``; a plan-fact write emits
``plan_fact_recorded`` (accept/direct-edit only). The capture event
(``user_acceptance_captured``) already fired in Perceive (IC-WA-001 A6) and is
not re-emitted here. The ``emitter`` is OPTIONAL (a default collecting emitter
is used when absent), so existing callers keep working.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel

from backend.responsibilities.perceive.acceptance_capture import AcceptanceCapture
from backend.responsibilities.retain.admission import RetentionStore
from backend.services.observability.events import CollectingEventEmitter, EventEmitter
from shared.epistemic import PlanFact

# The user-confirm actions that ALSO record a plan fact (IC-WU-ACCEPT U1.2). On
# reject/defer the UAR records the action, but nothing is confirmed as factual.
_PLAN_FACT_ACTIONS: frozenset[str] = frozenset({"accept", "direct_edit"})


class AcceptanceRecordingError(ValueError):
    """B4-Major guard: a UAR/plan fact without its mandatory fields is rejected."""


@runtime_checkable
class ChrReader(Protocol):
    """Minimal READ seam for the pinned CHR an ``accept`` confirms.

    Satisfied by ``backend.responsibilities.retain.repository.ChrRepository``
    (its ``get`` returns the CHR carrying ``output_payload``). The plan-fact
    content for an accepted recommendation is a DATA read of that payload — no
    interpretation, no LLM (decision #10; ANTI_ASSUMPTION).
    """

    def get(self, chr_id: Any) -> Any:
        ...  # pragma: no cover - protocol


class AcceptanceRecordResult(BaseModel):
    """What one acceptance recording produced: the UAR row + its history entry,
    and (on accept/direct-edit) the plan-fact row it also wrote."""

    uar_id: str
    record: dict
    history_id: str
    # DTM-0016 — set ONLY on accept/direct_edit; None on reject/defer.
    plan_fact_id: str | None = None
    plan_fact: dict | None = None


def _plan_fact_proposition(
    *,
    action: str,
    fields: Mapping[str, Any],
    pin: str,
    chr_reader: ChrReader | None,
) -> str:
    """Derive the confirmed content for the plan fact (no LLM — a data read/edit).

    - ``direct_edit``: the user's ``edit_content`` from the capture.
    - ``accept``: the pinned CHR's ``output_payload`` (read via ``chr_reader``),
      rendered to the confirmed-content text. The accepted Derived recommendation
      STAYS Derived in history — OSLO never promotes it; the USER's confirmation
      is what authors the plan fact (hard rule #5).
    """
    if action == "direct_edit":
        edit = fields.get("edit_content")
        if edit is None or not str(edit).strip():
            raise AcceptanceRecordingError(
                "plan-fact recording rejected — a direct_edit must carry "
                "edit_content (the user-authored confirmed content): a plan "
                "fact has no source otherwise (IC-WU-ACCEPT U1.2)"
            )
        return str(edit)

    # action == "accept": derive from the pinned CHR payload (a DATA read).
    if chr_reader is None:
        raise AcceptanceRecordingError(
            "plan-fact recording rejected — accepting a recommendation needs a "
            "chr_reader to read the pinned CHR's output_payload (the confirmed "
            "content is a data read of the accepted emission; no LLM) "
            "(IC-WU-ACCEPT U1.2; decision #10)"
        )
    record = chr_reader.get(pin)
    if record is None:
        raise AcceptanceRecordingError(
            f"plan-fact recording rejected — no Cognition History Record at the "
            f"pinned version {pin!r}: the accepted emission must exist to confirm "
            "its content (IC-WU-ACCEPT U1.2)"
        )
    payload = (
        record.get("output_payload")
        if isinstance(record, Mapping)
        else getattr(record, "output_payload", None)
    )
    if not payload:
        raise AcceptanceRecordingError(
            f"plan-fact recording rejected — the pinned CHR {pin!r} carries no "
            "output_payload to confirm (IC-WU-ACCEPT U1.2)"
        )
    # The confirmed content is the accepted emission's payload, recorded as
    # factual-in-the-plan. Common payloads carry a 'summary'/'proposition'; fall
    # back to the rendered payload so nothing is silently dropped.
    if isinstance(payload, Mapping):
        text = payload.get("summary") or payload.get("proposition")
        return str(text) if text is not None and str(text).strip() else str(dict(payload))
    return str(payload)


def record_acceptance(
    capture: AcceptanceCapture | Mapping[str, Any],
    *,
    project_id: str,
    store: RetentionStore,
    emitter: EventEmitter | None = None,
    chr_reader: ChrReader | None = None,
) -> AcceptanceRecordResult:
    """Record a captured user-confirm action: the UAR always, the plan fact on confirm.

    INSERTS one ``user_acceptance_record`` row (version-pinned, decoupled,
    user-attested) + one ``acceptance-recorded`` history entry, and emits
    ``user_acceptance_record_appended``. On ``accept`` / ``direct_edit`` ALSO
    INSERTS one ``attested_assertion`` plan fact (user-attested, the confirmed
    content) + one ``plan-fact-recorded`` history entry, and emits
    ``plan_fact_recorded``. On ``reject`` / ``defer`` NO plan fact is written.

    Marks nothing true/approved; mutates the accepted item nothing; OSLO never
    authors a plan fact without the user's action (hard rule #5).

    Raises:
        AcceptanceRecordingError: missing/empty ``version_pin`` (B4 Major /
            B+ negative 4), missing ``project_id``, or (on confirm) no
            plan-fact content source — rejected before any write.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    fields = (
        dict(capture)
        if isinstance(capture, Mapping)
        else capture.model_dump()
    )
    pin = fields.get("version_pin")
    if pin is None or not str(pin).strip():
        raise AcceptanceRecordingError(
            "acceptance recording rejected — version_pin is mandatory: a User "
            "Acceptance Record must pin the exact emission/version accepted "
            "(DL-043; IC-WA-002 §B+ negative 4; QA B4 Major)"
        )
    if not str(project_id).strip():
        raise AcceptanceRecordingError(
            "acceptance recording rejected — project_id is mandatory: the UAR "
            "is a canonical project record (LDM §1 universal fields)"
        )

    user_id = str(fields["user_id"])
    action = str(fields["action"])
    target_kind = str(fields["target_kind"])
    pin = str(pin)
    captured_at = fields.get("captured_at")
    confirmed_at = (
        captured_at.isoformat() if hasattr(captured_at, "isoformat") else captured_at
    )

    # ---- plan fact content resolved BEFORE any write (confirm actions only) --
    # On reject/defer no plan fact is written: nothing is confirmed as factual.
    plan_fact_obj: PlanFact | None = None
    if action in _PLAN_FACT_ACTIONS:
        proposition = _plan_fact_proposition(
            action=action, fields=fields, pin=pin, chr_reader=chr_reader
        )
        plan_fact_obj = PlanFact(
            project_id=str(project_id),
            proposition=proposition,
            content_type="fact",  # LDM §2.1 default (worker decision #10)
            attested_by_user=user_id,
            version_pin=pin,
            provenance_ref={
                "capture_event": "user_acceptance_captured",  # fired in Perceive
                "user_id": user_id,
                "version_pin": pin,
                "action": action,
                "target_kind": target_kind,
                "captured_at": confirmed_at,
            },
        )

    # ---- (1) the UAR write (always) -----------------------------------------
    row: dict[str, Any] = {
        "user_id": user_id,
        "action": action,
        "target_kind": target_kind,
        "version_pin": pin,
        "project_id": str(project_id),
        "created_by": user_id,
        "epistemic_state": "attested-user",
        "version": 1,
        "provenance_ref": {
            "capture_event": "user_acceptance_captured",  # fired in Perceive
            "user_id": user_id,
            "version_pin": pin,
            "captured_at": confirmed_at,
        },
    }
    if confirmed_at is not None:
        row["confirmed_at"] = confirmed_at
    persisted = dict(store.insert_acceptance(row))

    entry = store.insert_history(
        {
            "event_type": "acceptance-recorded",
            "subject_ref": {
                "uar_id": str(persisted["uar_id"]),
                "version_pin": pin,
                "target_kind": target_kind,
                "action": action,
            },
            "actor": user_id,
            "project_id": str(project_id),
            "created_by": user_id,
            "epistemic_state": "attested-user",
            "provenance_ref": dict(persisted["provenance_ref"]),
        }
    )
    # OBS-WU-ACCEPT C3: the UAR append + its acceptance→emission linkage audit.
    seam.emit(
        "user_acceptance_record_appended",
        {
            "uar_id": str(persisted["uar_id"]),
            "user_id": user_id,
            "action": action,
            "target_kind": target_kind,
            "version_pin": pin,  # the version reference (audit)
            "project_id": str(project_id),
        },
    )

    # ---- (2) the plan-fact write (accept / direct_edit only) ----------------
    plan_fact_id: str | None = None
    plan_fact_row: dict | None = None
    if plan_fact_obj is not None:
        plan_fact_row = dict(
            store.insert_assertion(
                {
                    "content_type": plan_fact_obj.content_type,
                    "proposition": plan_fact_obj.proposition,
                    # The USER is the attesting source — OSLO never self-accepts.
                    "attesting_source": user_id,
                    "source_ref": {
                        "version_pin": pin,
                        "action": action,
                        "target_kind": target_kind,
                    },
                    "re_derivable": False,  # a user-attested plan fact is not OSLO-derivable
                    "version": 1,
                    "project_id": str(project_id),
                    "created_by": user_id,
                    "epistemic_state": "attested-user",
                    "provenance_ref": dict(plan_fact_obj.provenance_ref),
                }
            )
        )
        plan_fact_id = str(plan_fact_row["assertion_id"])

        # History audit entry for the plan-fact write. Reuses the existing
        # ``acceptance-recorded`` event_type (the history_record CHECK admits no
        # ``plan-fact-recorded`` value, and DTM-0016 adds NO migration): the
        # plan fact is recorded AS PART OF recording the acceptance. The
        # ``record`` discriminator + ``assertion_id`` in subject_ref distinguish
        # it from the UAR's entry; the contract event ``plan_fact_recorded``
        # carries the distinct OBS signal.
        store.insert_history(
            {
                "event_type": "acceptance-recorded",
                "subject_ref": {
                    "record": "plan_fact",
                    "assertion_id": plan_fact_id,
                    "uar_id": str(persisted["uar_id"]),
                    "version_pin": pin,
                    "action": action,
                },
                "actor": user_id,
                "project_id": str(project_id),
                "created_by": user_id,
                "epistemic_state": "attested-user",
                "provenance_ref": dict(plan_fact_obj.provenance_ref),
            }
        )
        # OBS-WU-ACCEPT C3: the plan-fact record + its user attribution + pin.
        seam.emit(
            "plan_fact_recorded",
            {
                "assertion_id": plan_fact_id,
                "uar_id": str(persisted["uar_id"]),
                "attested_by_user": user_id,  # the plan fact's user attribution
                "version_pin": pin,
                "content_type": plan_fact_obj.content_type,
                "project_id": str(project_id),
            },
        )

    return AcceptanceRecordResult(
        uar_id=str(persisted["uar_id"]),
        record=persisted,
        history_id=str(entry["history_id"]),
        plan_fact_id=plan_fact_id,
        plan_fact=plan_fact_row,
    )

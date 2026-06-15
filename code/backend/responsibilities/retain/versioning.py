"""Versioning + explicit supersession (DTM-0008; IC-WA-002 A3.4/A3.5/A4.7–A4.9).

A knowledge mutation NEVER touches the prior row: ``version_assertion`` INSERTS
a new ``attested_assertion`` row with ``version = prior + 1`` and
``supersedes_id = prior`` — the prior row stays fully intact (the DB append-only
belt + braces enforce this underneath). Supersession is EXPLICIT (A4.9 — no
silent supersession): every call appends BOTH history entries
(``knowledge-versioned`` for the new row AND ``superseded`` for the prior) and
emits BOTH events (``knowledge_versioned`` + ``knowledge_superseded``) plus
``knowledge_mutation_recorded`` — this function is the ONLY public surface that
creates a superseding row, so a supersession without its recorded events is
structurally impossible (the negative suite introspects this).

Provenance is carried forward, never dropped (A4.10): the new row keeps the
prior's provenance reference chain and adds the versioned-from link.

``version_chain`` mirrors the DTM-0004 ``lineage_chain`` read pattern
(seen-set guard included) so the full ordered version history is
reconstructable from the rows alone (A3.7; OBS C5 version-chain replay).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.responsibilities.adapt.triggers import TriggerClaim, TriggerType
from backend.responsibilities.perceive.extraction import AssertionDraft
from backend.responsibilities.retain.admission import RetentionStore
from backend.services.observability.events import CollectingEventEmitter, EventEmitter


class PriorAssertionNotFoundError(ValueError):
    """A mutation must name an existing prior version — nothing to supersede."""


class VersioningResult(BaseModel):
    """What one mutation produced: the new version row + the constructed trigger."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    assertion_id: str
    version: int
    supersedes_id: str
    assertion: dict
    change_trigger: TriggerClaim = Field(
        ...,
        description=(
            "Constructed (NOT submitted) 00R knowledge-change claim — Retain "
            "emits the trigger signal, only orchestration may run it (A3.10)."
        ),
    )


def _new_content_fields(
    new_content: AssertionDraft | Mapping[str, Any],
) -> dict[str, Any]:
    """The content fields a mutation may change (everything else is carried)."""
    if isinstance(new_content, AssertionDraft):
        return {
            "content_type": new_content.content_type,
            "proposition": new_content.proposition,
            "attesting_source": new_content.attesting_source,
            "source_ref": dict(new_content.source_ref),
        }
    allowed = ("content_type", "proposition", "attesting_source", "source_ref")
    return {k: new_content[k] for k in allowed if k in new_content}


def version_assertion(
    prior_assertion_id: str,
    new_content: AssertionDraft | Mapping[str, Any],
    *,
    store: RetentionStore,
    emitter: EventEmitter | None = None,
    actor: str = "retain",
) -> VersioningResult:
    """Create the next version of an assertion with explicit supersession.

    INSERTS a new row (prior untouched), appends ``knowledge-versioned`` AND
    ``superseded`` history entries, emits ``knowledge_versioned`` +
    ``knowledge_superseded`` + ``knowledge_mutation_recorded``, and returns
    the new row plus a constructed (never submitted) ``knowledge-change``
    TriggerClaim.

    Raises:
        PriorAssertionNotFoundError: ``prior_assertion_id`` does not resolve —
            rejected BEFORE any write or event.
    """
    seam = emitter if emitter is not None else CollectingEventEmitter()
    prior = store.get_assertion(str(prior_assertion_id))
    if prior is None:
        raise PriorAssertionNotFoundError(
            f"knowledge mutation rejected — prior assertion "
            f"{prior_assertion_id!r} does not exist: a new version must "
            "supersede an existing one (IC-WA-002 A3.4)"
        )

    prior_id = str(prior["assertion_id"])
    project_id = str(prior["project_id"])
    new_version = int(prior["version"]) + 1
    changes = _new_content_fields(new_content)

    new_row = store.insert_assertion(
        {
            "content_type": changes.get("content_type", prior["content_type"]),
            "proposition": changes.get("proposition", prior["proposition"]),
            "attesting_source": changes.get(
                "attesting_source", prior["attesting_source"]
            ),
            "source_ref": changes.get("source_ref", dict(prior["source_ref"])),
            "re_derivable": prior["re_derivable"],
            "version": new_version,
            "supersedes_id": prior_id,
            "project_id": project_id,
            "created_by": actor,
            "epistemic_state": str(prior["epistemic_state"]),
            # A4.10: provenance carried forward, plus the versioned-from link.
            "provenance_ref": {
                **dict(prior["provenance_ref"]),
                "versioned_from": prior_id,
            },
        }
    )
    new_id = str(new_row["assertion_id"])

    # A4.9 — explicit, recorded supersession: BOTH history entries, always.
    store.insert_history(
        {
            "event_type": "knowledge-versioned",
            "subject_ref": {
                "assertion_id": new_id,
                "version": new_version,
                "supersedes_id": prior_id,
            },
            "actor": actor,
            "project_id": project_id,
            "created_by": actor,
            "epistemic_state": str(new_row["epistemic_state"]),
            "provenance_ref": dict(new_row["provenance_ref"]),
        }
    )
    store.insert_history(
        {
            "event_type": "superseded",
            "subject_ref": {
                "assertion_id": prior_id,
                "version": int(prior["version"]),
                "superseded_by": new_id,
            },
            "actor": actor,
            "project_id": project_id,
            "created_by": actor,
            "epistemic_state": str(prior["epistemic_state"]),
            "provenance_ref": dict(prior["provenance_ref"]),
        }
    )

    audit = {
        "project_id": project_id,
        "assertion_id": new_id,
        "version": new_version,
        "supersedes_id": prior_id,
    }
    seam.emit("knowledge_versioned", audit)
    seam.emit(
        "knowledge_superseded",
        {
            "project_id": project_id,
            "assertion_id": prior_id,
            "superseded_by": new_id,
        },
    )
    seam.emit("knowledge_mutation_recorded", {**audit, "mutation": "version"})

    # Constructed only — Retain never runs the cascade itself (A3.10).
    change_trigger = TriggerClaim(
        trigger_type=TriggerType.KNOWLEDGE_CHANGE,
        project_id=project_id,
        information_changed=True,
        source=f"assertion:{new_id}",
    )
    return VersioningResult(
        assertion_id=new_id,
        version=new_version,
        supersedes_id=prior_id,
        assertion=dict(new_row),
        change_trigger=change_trigger,
    )


def version_chain(
    assertion_id: str, *, store: RetentionStore
) -> list[dict[str, Any]]:
    """Walk the ``supersedes_id`` ancestry, most recent first (C5 replay read).

    Mirrors the DTM-0004 ``lineage_chain`` pattern: starts at the given row and
    follows supersession links until a root (``supersedes_id`` is null) or a
    missing/already-seen id (the seen-set guard makes a malformed
    self-reference terminate instead of looping). Returns ``[]`` when the
    starting id does not exist.
    """
    chain: list[dict[str, Any]] = []
    seen: set[str] = set()
    cursor: str | None = str(assertion_id)
    while cursor is not None and cursor not in seen:
        row = store.get_assertion(cursor)
        if row is None:
            break
        chain.append(dict(row))
        seen.add(cursor)
        parent = row.get("supersedes_id")
        cursor = str(parent) if parent else None
    return chain

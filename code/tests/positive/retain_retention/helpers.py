"""Shared builders for the QA-WA-002 suites (pure; no database).

A "ready" candidate here mirrors EXACTLY what DTM-0007's intake persists
(``promotion_candidate`` row shape + integrity_clearance jsonb), and drafts
mirror the DTM-0007 extraction handoff — Retain consumes both as-is.
"""

from __future__ import annotations

import uuid
from typing import Any

from backend.responsibilities.perceive.extraction import AssertionDraft


def integrity_clearance(**overrides) -> dict[str, Any]:
    """The DTM-0007 integrity_clearance jsonb shape (A3.3 of IC-WA-001)."""
    clearance: dict[str, Any] = {
        "attribution": {
            "present": True,
            "submitted_by": "user-42",
            "source": "evidence-source-7",
        },
        "idempotency": {"dedup_key": "deadbeef" * 8, "duplicate": False},
        "evidence_chain": {
            "intact": True,
            "body_ref": "artifacts/p/deadbeef.txt",
            "re_derivable": True,
            "normalization_version": "wa001-n1",
        },
    }
    clearance.update(overrides)
    return clearance


def ready_candidate(**overrides) -> dict[str, Any]:
    """A promotion_candidate row in the ready, integrity-cleared state."""
    row: dict[str, Any] = {
        "artifact_ref": str(uuid.uuid4()),
        "normalized_form": {"version": "wa001-n1", "text": "The launch must hold."},
        "readiness_state": "ready",
        "integrity_clearance": integrity_clearance(),
        "project_id": str(uuid.uuid4()),
    }
    row.update(overrides)
    return row


def draft(**overrides) -> AssertionDraft:
    """One evidence-attested assertion draft (the DTM-0007 handoff object)."""
    fields: dict[str, Any] = {
        "content_type": "constraint",
        "proposition": "The launch must hold.",
        "attesting_source": "evidence-source-7",
        "source_ref": {
            "artifact_id": str(uuid.uuid4()),
            "locus": {"section": 0, "line": 0},
        },
    }
    fields.update(overrides)
    return AssertionDraft(**fields)

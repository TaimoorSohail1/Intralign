"""DTM-0004 negative retain suite — no mutation surface; invalid records rejected.

Covers (task DTM-0004 / IC-WA-00R A4.2 / QA-WA-00R B3.2):
- The repository class exposes NO update/delete/upsert capability — the methods
  are not merely "never called", they are NOT PRESENT on the class
  (introspection; runs WITHOUT any database environment, never skips).
- Pydantic rejects a CHR with a ``recompute_trigger`` or ``output_kind``
  outside the LDM §2.2 exact value lists, and any ``epistemic_state`` other
  than ``attested-oslo`` (no database needed).
- DB-level (live Supabase only, skipif env unset): a raw UPDATE on
  ``cognition_history_record`` via the supabase client fails with permission
  denied — the DTM-0002 belt (REVOKE) holds underneath the repository.
"""

from __future__ import annotations

import os
import uuid

import pytest
from pydantic import ValidationError

from backend.responsibilities.retain import ChrRepository, CognitionHistoryRecord

try:
    from supabase import create_client
except ImportError:  # Phase I CI venv has no supabase-py installed
    create_client = None  # type: ignore[assignment]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

_live_db = pytest.mark.skipif(
    create_client is None or not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL and "
        "SUPABASE_SERVICE_ROLE_KEY from `supabase status` (Phase I CI has no "
        "Supabase; this suite runs locally only)"
    ),
)

# Method names that would constitute a mutation surface (A4.2: append-only).
_MUTATION_NAMES = ("update", "delete", "upsert", "remove", "overwrite", "purge")

# The ONLY public surface the repository may expose (task DTM-0004 locked list;
# DTM-0017 adds ``latest_acceptance_impact_for_uar`` — a SELECT-only READ for the
# Acceptance-Impact supersede lookup, not a mutation path).
_ALLOWED_PUBLIC = {
    "append",
    "get",
    "latest_for_output",
    "lineage_chain",
    "latest_acceptance_impact_for_uar",
}


def _valid_fields() -> dict:
    """A fully valid CHR field set (LDM §2.2) to mutate per negative case."""
    return {
        "output_kind": "finding",
        "output_payload": {"summary": "x"},
        "input_attestation_version": "v1",
        "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
        "upstream_lineage": {"chr_ids": []},
        "recompute_trigger": "promotion",
        "project_id": uuid.uuid4(),
        "provenance_ref": {"emitted_by": "test-suite"},
    }


def test_repository_has_no_update_delete_or_upsert_attribute() -> None:
    """A4.2 — mutation methods are NOT PRESENT on the class (not just unused)."""
    for name in _MUTATION_NAMES:
        assert not hasattr(ChrRepository, name), (
            f"ChrRepository must not expose '{name}' — CHRs are append-only "
            "(IC-WA-00R A4.2; LDM §5.1)"
        )


def test_repository_public_surface_is_exactly_the_locked_read_append_set() -> None:
    """No public attribute may smuggle in a mutation path under another name."""
    public = {
        name
        for name in vars(ChrRepository)
        if not name.startswith("_") and callable(getattr(ChrRepository, name))
    }
    assert public == _ALLOWED_PUBLIC


def test_invalid_recompute_trigger_rejected_by_model() -> None:
    """LDM §2.2 — recompute_trigger outside the exact 5-value list rejected."""
    fields = _valid_fields()
    fields["recompute_trigger"] = "manual-overwrite"  # NOT in LDM §2.2 list
    with pytest.raises(ValidationError) as excinfo:
        CognitionHistoryRecord(**fields)
    assert "recompute_trigger" in str(excinfo.value)


def test_unknown_output_kind_rejected_by_model() -> None:
    """LDM §2.2 — output_kind outside the exact 12-value list rejected."""
    fields = _valid_fields()
    fields["output_kind"] = "governance_note"  # NOT in LDM §2.2 list
    with pytest.raises(ValidationError) as excinfo:
        CognitionHistoryRecord(**fields)
    assert "output_kind" in str(excinfo.value)


def test_epistemic_state_pinned_to_attested_oslo() -> None:
    """LDM §2.2 — a CHR is OSLO-self-attested; any other state rejected."""
    fields = _valid_fields()
    fields["epistemic_state"] = "derived"  # a CHR is never Derived
    with pytest.raises(ValidationError) as excinfo:
        CognitionHistoryRecord(**fields)
    assert "epistemic_state" in str(excinfo.value)


@_live_db
def test_raw_update_on_chr_table_denied_at_database() -> None:
    """B3.2 — even bypassing the repository, the DB refuses UPDATE (REVOKE belt)."""
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    with pytest.raises(Exception) as excinfo:
        (
            client.table("cognition_history_record")
            .update({"output_payload": {"summary": "tampered"}})
            .eq("chr_id", str(uuid.uuid4()))
            .execute()
        )
    assert "permission denied" in str(excinfo.value)

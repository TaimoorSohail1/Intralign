"""DTM-0002 negative persistence suite — append-only enforcement at the database.

Runs LIVE against the local Supabase stack only (Phase I CI has no Supabase, so
these tests SKIP unless the environment is configured). To run locally:

    cd code && supabase start          # then read keys from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key from `supabase status`>

Covers (task DTM-0002 / LDM §5.1 / DL-043 / hard rule #3) — belt AND braces:
- Belt: UPDATE and DELETE on each canonical table are REVOKED from every API
  role (anon, authenticated, service_role) — PostgREST requests fail with
  permission denied even for the service_role (app) connection.
- Braces: the BEFORE UPDATE OR DELETE trigger raises for owner-privileged
  connections too — verified via the local-only SECURITY DEFINER probe
  ``public.test_probe_append_only`` (seeded by ``supabase db reset``), which
  attempts the mutation as the table owner so the only guard left is the
  trigger itself.
- CHECK constraints reject values outside the LDM's exact lists
  (``recompute_trigger``, LDM §2.2).
"""

from __future__ import annotations

import os
import uuid

import pytest

try:
    from supabase import create_client
except ImportError:  # Phase I CI venv has no supabase-py installed
    create_client = None  # type: ignore[assignment]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

pytestmark = pytest.mark.skipif(
    create_client is None or not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL and "
        "SUPABASE_SERVICE_ROLE_KEY from `supabase status` (Phase I CI has no "
        "Supabase; this suite runs locally only)"
    ),
)

CANONICAL_TABLES = (
    "attested_assertion",
    "cognition_history_record",
    "user_acceptance_record",
    "history_record",
)

# Primary-key column per canonical table (needed for PostgREST filters).
PK = {
    "attested_assertion": "assertion_id",
    "cognition_history_record": "chr_id",
    "user_acceptance_record": "uar_id",
    "history_record": "history_id",
}


@pytest.fixture(scope="module")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@pytest.mark.parametrize("table", CANONICAL_TABLES)
def test_update_revoked_for_app_role(client, table: str) -> None:
    """Belt: UPDATE privilege is revoked — even service_role gets 42501."""
    with pytest.raises(Exception) as excinfo:
        (
            client.table(table)
            .update({"version": 2})
            .eq(PK[table], str(uuid.uuid4()))
            .execute()
        )
    assert "permission denied" in str(excinfo.value)


@pytest.mark.parametrize("table", CANONICAL_TABLES)
def test_delete_revoked_for_app_role(client, table: str) -> None:
    """Belt: DELETE privilege is revoked — even service_role gets 42501."""
    with pytest.raises(Exception) as excinfo:
        client.table(table).delete().eq(PK[table], str(uuid.uuid4())).execute()
    assert "permission denied" in str(excinfo.value)


@pytest.mark.parametrize("table", CANONICAL_TABLES)
@pytest.mark.parametrize("op", ("update", "delete"))
def test_trigger_blocks_owner_privileged_mutation(client, table: str, op: str) -> None:
    """Braces: the append-only trigger fires even past role privileges.

    The probe runs SECURITY DEFINER as the table owner, so REVOKE no longer
    applies — the returned message must be the trigger's exception.
    """
    resp = client.rpc(
        "test_probe_append_only", {"p_table": table, "p_op": op}
    ).execute()
    message = resp.data
    assert message != "NO ERROR RAISED", (
        f"{op.upper()} on {table} was not blocked by the append-only trigger"
    )
    assert "append-only" in message
    assert "DL-043" in message


def test_invalid_recompute_trigger_rejected(client) -> None:
    """LDM §2.2 CHECK: recompute_trigger outside the exact value list rejected."""
    with pytest.raises(Exception) as excinfo:
        (
            client.table("cognition_history_record")
            .insert(
                {
                    "output_kind": "finding",
                    "output_payload": {"summary": "x"},
                    "input_attestation_version": "v1",
                    "model_or_rule_version": {"provider": "test", "model": "rule-v1"},
                    "upstream_lineage": [],
                    "recompute_trigger": "manual-overwrite",  # NOT in LDM §2.2 list
                    "project_id": str(uuid.uuid4()),
                    "provenance_ref": {"emitted_by": "test-suite"},
                }
            )
            .execute()
        )
    assert "recompute_trigger" in str(excinfo.value)


def test_invalid_uar_action_rejected(client) -> None:
    """LDM §2.4 CHECK: action outside accept|reject|defer|direct_edit rejected."""
    with pytest.raises(Exception) as excinfo:
        (
            client.table("user_acceptance_record")
            .insert(
                {
                    "user_id": str(uuid.uuid4()),
                    "action": "approve",  # NOT in LDM §2.4 list
                    "target_kind": "recommendation",
                    "version_pin": str(uuid.uuid4()),
                    "project_id": str(uuid.uuid4()),
                    "created_by": "user",
                    "provenance_ref": {},
                }
            )
            .execute()
        )
    assert "action" in str(excinfo.value)

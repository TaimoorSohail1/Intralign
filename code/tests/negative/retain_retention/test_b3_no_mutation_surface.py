"""QA-WA-002 B3.1/B3.2 + §B+ negative 2 — overwrite/deletion impossible.

Three independent layers, each proven:

- the retention store class exposes NO update/delete/upsert capability — the
  methods are NOT PRESENT, not merely unused (introspection; pure, never skips);
- the in-memory fake used by the pure suites honors the same surface (so the
  pure suites cannot accidentally rely on a mutation path the real store lacks);
- the DATABASE refuses UPDATE/DELETE on all three canonical retention tables
  even when the store is bypassed entirely (live; DTM-0002 REVOKE belt).
"""

from __future__ import annotations

import os
import uuid

import pytest

from backend.services.persistence.retention_store import SupabaseRetentionStore
from tests.positive.retain_retention.fakes import InMemoryRetentionStore

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

_live_db = pytest.mark.skipif(
    create_client is None or not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL and "
        "SUPABASE_SERVICE_ROLE_KEY from `supabase status`; this DB-level "
        "re-proof runs locally only"
    ),
)

# Method names that would constitute a mutation surface (A4.7/A4.8).
_MUTATION_NAMES = ("update", "delete", "upsert", "remove", "overwrite", "purge")

# The ONLY public surface the retention store may expose (DTM-0008 locked).
_ALLOWED_PUBLIC = {
    "get_candidate",
    "insert_assertion",
    "get_assertion",
    "insert_acceptance",
    "get_acceptance",
    "insert_history",
    "history_for_assertion",
}


def test_retention_store_has_no_mutation_method() -> None:
    """A4.7/A4.8 — mutation methods are NOT PRESENT on the class."""
    for name in _MUTATION_NAMES:
        assert not hasattr(SupabaseRetentionStore, name), (
            f"SupabaseRetentionStore must not expose '{name}' — canonical "
            "retention is append-only (IC-WA-002 A4.7/A4.8; LDM §5.1)"
        )


def test_retention_store_public_surface_is_exactly_insert_plus_select() -> None:
    """No public attribute may smuggle in a mutation path under another name."""
    public = {
        name
        for name in vars(SupabaseRetentionStore)
        if not name.startswith("_")
        and callable(getattr(SupabaseRetentionStore, name))
    }
    assert public == _ALLOWED_PUBLIC


def test_in_memory_fake_honors_the_same_append_only_surface() -> None:
    """The pure suites cannot lean on a mutation path the real store lacks
    (seed_candidate is test setup for the READ-only candidate input)."""
    for name in _MUTATION_NAMES:
        assert not hasattr(InMemoryRetentionStore, name)
    public = {
        name
        for name in vars(InMemoryRetentionStore)
        if not name.startswith("_")
        and callable(getattr(InMemoryRetentionStore, name))
    }
    assert public == _ALLOWED_PUBLIC | {"seed_candidate"}


@_live_db
@pytest.mark.parametrize(
    "table",
    ["attested_assertion", "user_acceptance_record", "history_record"],
)
def test_raw_update_on_retention_tables_denied_at_database(table: str) -> None:
    """B3.1 — even bypassing the store, the DB refuses UPDATE (REVOKE belt)."""
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    pk = {"attested_assertion": "assertion_id", "user_acceptance_record": "uar_id",
          "history_record": "history_id"}[table]
    with pytest.raises(Exception, match="permission denied"):
        (
            client.table(table)
            .update({"created_by": "tampered"})
            .eq(pk, str(uuid.uuid4()))
            .execute()
        )


@_live_db
@pytest.mark.parametrize(
    "table",
    ["attested_assertion", "user_acceptance_record", "history_record"],
)
def test_raw_delete_on_retention_tables_denied_at_database(table: str) -> None:
    """B3.2 — no path destroys knowledge or history (REVOKE belt holds)."""
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    pk = {"attested_assertion": "assertion_id", "user_acceptance_record": "uar_id",
          "history_record": "history_id"}[table]
    with pytest.raises(Exception, match="permission denied"):
        client.table(table).delete().eq(pk, str(uuid.uuid4())).execute()

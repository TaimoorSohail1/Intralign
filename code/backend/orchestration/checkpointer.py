"""Durable-run wiring (env profile §1: checkpointing/resumability mandatory).

The LangGraph checkpointer persists workflow state so a run is resumable after
interruption, deploy, or failure, and its execution history is auditable.

Binding (DL-054): durable workflow state -> Supabase Postgres, reached directly
via ``SUPABASE_DB_URL`` (the `supabase status` DB URL locally;
``postgresql://postgres:postgres@127.0.0.1:54332/postgres`` for the local stack).
LangGraph OWNS its checkpoint tables (``checkpoints``, ``checkpoint_blobs``,
``checkpoint_writes``, ``checkpoint_migrations``): they are workflow metadata
per DL-054 — NOT canonical content, NOT part of the append-only canonical
schema, and not governed by the canonical-migration linter. ``setup()`` is
idempotent (the saver tracks its own migrations table).

Durable-by-default: callers get the Postgres saver unless a test EXPLICITLY
requests the in-memory fallback (``in_memory=True``).
"""

from __future__ import annotations

import os

ENV_DB_URL = "SUPABASE_DB_URL"


def build_checkpointer(*, in_memory: bool = False):
    """Return a LangGraph checkpointer (Supabase Postgres; durable by default).

    Args:
        in_memory: ONLY for tests that explicitly request a non-durable saver
            (e.g. coalescing tests that need no database). Production and
            default paths always checkpoint to Postgres.

    Raises:
        RuntimeError: if ``SUPABASE_DB_URL`` is unset when a durable saver is
            requested (locally: ``cd code && supabase start``, then export the
            DB URL from ``supabase status``).
    """
    if in_memory:
        from langgraph.checkpoint.memory import InMemorySaver

        return InMemorySaver()

    db_url = os.environ.get(ENV_DB_URL)
    if not db_url:
        raise RuntimeError(
            f"durable checkpointer not configured — missing environment "
            f"variable {ENV_DB_URL}. Locally: `cd code && supabase start`, then "
            f"export {ENV_DB_URL} with the DB URL from `supabase status`."
        )

    # Lazy imports: app modules stay importable without the PG driver installed.
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg import Connection
    from psycopg.rows import dict_row

    conn = Connection.connect(
        db_url, autocommit=True, prepare_threshold=0, row_factory=dict_row
    )
    saver = PostgresSaver(conn)
    saver.setup()  # idempotent — guarded by checkpoint_migrations
    return saver

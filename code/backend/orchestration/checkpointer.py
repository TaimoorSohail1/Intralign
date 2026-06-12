"""Durable-run wiring (env profile §1: checkpointing/resumability mandatory).

The LangGraph checkpointer persists workflow state so a run is resumable after
interruption, deploy, or failure, and its execution history is auditable.

Binding (DL-054): durable workflow state -> Supabase Postgres (workflow metadata
+ snapshots as jsonb). Transient/session state -> Redis. The raw connections come
from services.persistence; this module only adapts them into a LangGraph saver.
"""

from __future__ import annotations


def build_checkpointer():
    """Return a LangGraph checkpointer backed by Supabase Postgres.

    Stub — wired in Phase II against services.persistence once the IC-WA-00R
    backbone contract is approved. Prime Directive: no contract, no build.
    """
    raise NotImplementedError("Wire PostgresSaver(Supabase) under IC-WA-00R (Phase II).")

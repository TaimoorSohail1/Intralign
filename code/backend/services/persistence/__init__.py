"""Persistence — repository interfaces over Supabase (PG/Storage/pgvector), Neo4j, Redis. Canonical stores append-only."""

from backend.services.persistence.client import get_supabase_client

__all__ = ["get_supabase_client"]

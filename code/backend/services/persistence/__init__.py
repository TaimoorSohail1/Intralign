"""Persistence — repository interfaces over Supabase (PG/Storage/pgvector), Neo4j, Redis. Canonical stores append-only."""

from backend.services.persistence.client import get_supabase_client
from backend.services.persistence.intake_store import SupabaseIntakeStore
from backend.services.persistence.retention_store import SupabaseRetentionStore
from backend.services.persistence.storage import ARTIFACTS_BUCKET, ArtifactBodyStore

__all__ = [
    "ARTIFACTS_BUCKET",
    "ArtifactBodyStore",
    "SupabaseIntakeStore",
    "SupabaseRetentionStore",
    "get_supabase_client",
]

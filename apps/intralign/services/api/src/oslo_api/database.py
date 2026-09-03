from sqlalchemy import Engine, create_engine


def create_database_engine(database_url: str) -> Engine:
    """Create a bounded pool safe for Supabase's session-mode connection limit."""

    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_recycle=300,
        pool_use_lifo=True,
    )

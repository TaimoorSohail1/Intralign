import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import NullPool


def create_database_engine(
    database_url: str,
    *,
    serverless: bool | None = None,
) -> Engine:
    """Create an engine suitable for a persistent or serverless runtime."""

    if serverless is None:
        serverless = bool(os.environ.get("VERCEL"))
    if serverless:
        return create_engine(
            database_url,
            pool_pre_ping=True,
            poolclass=NullPool,
        )

    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_recycle=300,
        pool_use_lifo=True,
    )

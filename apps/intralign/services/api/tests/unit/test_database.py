from unittest.mock import patch

from oslo_api.database import create_database_engine


def test_create_database_engine_uses_bounded_production_pool() -> None:
    with patch("oslo_api.database.create_engine") as create_engine:
        create_database_engine("postgresql+psycopg://example")

    create_engine.assert_called_once_with(
        "postgresql+psycopg://example",
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_recycle=300,
        pool_use_lifo=True,
    )

from unittest.mock import patch

from sqlalchemy.pool import NullPool

from oslo_api.database import create_database_engine


def test_create_database_engine_uses_bounded_pool_for_persistent_runtime() -> None:
    with patch("oslo_api.database.create_engine") as create_engine:
        create_database_engine(
            "postgresql+psycopg://example",
            serverless=False,
        )

    create_engine.assert_called_once_with(
        "postgresql+psycopg://example",
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_recycle=300,
        pool_use_lifo=True,
    )


def test_create_database_engine_uses_null_pool_for_serverless_runtime() -> None:
    with patch("oslo_api.database.create_engine") as create_engine:
        create_database_engine(
            "postgresql+psycopg://example",
            serverless=True,
        )

    create_engine.assert_called_once_with(
        "postgresql+psycopg://example",
        pool_pre_ping=True,
        poolclass=NullPool,
    )


def test_create_database_engine_detects_vercel_runtime(monkeypatch) -> None:
    monkeypatch.setenv("VERCEL", "1")
    with patch("oslo_api.database.create_engine") as create_engine:
        create_database_engine("postgresql+psycopg://example")

    assert create_engine.call_args.kwargs["poolclass"] is NullPool
    assert "pool_size" not in create_engine.call_args.kwargs

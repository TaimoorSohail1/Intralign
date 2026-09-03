"""Shared live fixtures for the replay suite (same skip contract as DTM-0005).

Live axes need the local Supabase stack:

    cd code && supabase start          # then read values from `supabase status`
    export SUPABASE_URL=http://127.0.0.1:54331
    export SUPABASE_SERVICE_ROLE_KEY=<service_role key>
    export SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54332/postgres

Pure tests (tamper detection with a stub repo) never skip.
"""

from __future__ import annotations

import os

import pytest

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - CI venv without supabase-py
    create_client = None  # type: ignore[assignment]

from backend.orchestration import runner
from backend.responsibilities.retain import ChrRepository

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

live = pytest.mark.skipif(
    create_client is None
    or not SUPABASE_URL
    or not SUPABASE_SERVICE_ROLE_KEY
    or not SUPABASE_DB_URL,
    reason=(
        "local Supabase stack not configured — set SUPABASE_URL, "
        "SUPABASE_SERVICE_ROLE_KEY and SUPABASE_DB_URL (DB URL from "
        "`supabase status`); live replay axes run locally only"
    ),
)


@pytest.fixture(scope="session")
def client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@pytest.fixture(scope="session")
def repo(client) -> ChrRepository:
    return ChrRepository(client=client)


@pytest.fixture(scope="session")
def checkpointer():
    from backend.orchestration.checkpointer import build_checkpointer

    return build_checkpointer()


@pytest.fixture(autouse=True)
def _fresh_guard():
    runner.reset_coalescing_guard()
    yield
    runner.reset_coalescing_guard()

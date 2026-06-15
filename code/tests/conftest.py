"""Root test conftest — network hygiene for the whole suite (DTM-0006 FIX-1).

Tests must NEVER ship data to an external service. Some tests monkeypatch
``LANGSMITH_TRACING=true`` (the DTM-0006 linkage flag), and langchain/langgraph's
global tracer reads the same flag — without a guard it POSTs real run payloads
to ``https://api.smith.langchain.com`` (seen as repeated 401 "Failed to
multipart ingest runs" spam during the suite).

``os.environ.setdefault`` is not enough once a test monkeypatches the tracing
flag, so an autouse session fixture hard-points every LangSmith/LangChain
endpoint at an unroutable local address (port 9 — discard; connection fails
instantly and locally) and disables tracing v2 by default.

The DTM-0006 linkage code (``backend/services/observability/langsmith_linkage``)
reads only ``LANGSMITH_TRACING`` + the run id — none of the variables set here —
so linkage tests are unaffected.
"""

from __future__ import annotations

import os

import pytest

_UNROUTABLE_LOCAL_ENDPOINT = "http://127.0.0.1:9"


@pytest.fixture(autouse=True, scope="session")
def _langsmith_offline() -> None:
    """Point any accidental tracer at localhost so it fails fast, off-network."""
    os.environ["LANGSMITH_ENDPOINT"] = _UNROUTABLE_LOCAL_ENDPOINT
    os.environ["LANGCHAIN_ENDPOINT"] = _UNROUTABLE_LOCAL_ENDPOINT
    os.environ["LANGCHAIN_TRACING_V2"] = "false"

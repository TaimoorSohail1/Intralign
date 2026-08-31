"""DTM-0003 smoke test (positive): app boots with observability ENABLED.

Note: tests/positive/observability/ is reserved for DTM-0006 governed-output
events — OTel bring-up tests live here under observability_setup/.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.services.observability.setup import configure_observability


def _make_app() -> FastAPI:
    app = FastAPI()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


def test_health_ok_with_observability_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "oslo-backend")

    app = _make_app()
    enabled = configure_observability(app)
    assert enabled is True  # tracer provider + FastAPI instrumentation wired

    resp = TestClient(app).get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

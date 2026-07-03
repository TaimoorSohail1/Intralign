"""DTM-0003 smoke tests (negative): observability failure must NEVER stop boot.

Degrade-gracefully contract: OTLP endpoint unset OR unreachable -> app boots,
/health returns 200, a warning is logged. A suite without negatives is invalid.
"""

import logging

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


def test_health_ok_with_endpoint_unset(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)

    app = _make_app()
    with caplog.at_level(logging.WARNING, logger="backend.services.observability.setup"):
        enabled = configure_observability(app)

    assert enabled is False  # disabled, not crashed
    assert any(
        "OTEL_EXPORTER_OTLP_ENDPOINT not set" in record.message
        for record in caplog.records
    )

    resp = TestClient(app).get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_ok_with_dead_otlp_endpoint(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    # Nothing listens on this port — the exporter must degrade, never crash boot.
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:59999")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "oslo-backend")

    app = _make_app()
    with caplog.at_level(logging.WARNING, logger="backend.services.observability.setup"):
        configure_observability(app)

    assert any("unreachable" in record.message for record in caplog.records)

    resp = TestClient(app).get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

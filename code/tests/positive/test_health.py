"""Phase I infra smoke test (positive). No domain behavior yet."""

from fastapi.testclient import TestClient

from backend.api.app import app

client = TestClient(app)


def test_health_ok() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

"""Phase I infra smoke test (negative). A suite without negatives is invalid."""

from fastapi.testclient import TestClient

from backend.api.app import app

client = TestClient(app)


def test_unknown_route_404() -> None:
    resp = client.get("/no-such-endpoint")
    assert resp.status_code == 404

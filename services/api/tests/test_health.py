from fastapi.testclient import TestClient

from oslo_api.main import create_app


def test_health_reports_ready() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "service": "oslo-api"}

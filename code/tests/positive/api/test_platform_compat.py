from __future__ import annotations

import jwt
from fastapi.testclient import TestClient

from backend.api.app import app


def test_health_services_exposes_ui_compat_shape(monkeypatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon")
    monkeypatch.delenv("SUPABASE_DB_URL", raising=False)
    monkeypatch.setenv("LLM_PRIMARY_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    client = TestClient(app)
    response = client.get("/health/services")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"up", "down"}
    assert payload["backend"]["status"] == "up"
    assert payload["llmProvider"]["status"] == "up"
    assert [service["name"] for service in payload["services"]] == [
        "Backend",
        "Supabase Auth",
        "Supabase Postgres",
        "LLM Provider",
    ]


def test_demo_login_mints_backend_verifiable_token(monkeypatch) -> None:
    secret = "test-jwt-secret-with-at-least-32-characters"
    monkeypatch.setenv("SUPABASE_JWT_SECRET", secret)
    monkeypatch.setenv("OSLO_DEMO_LOGIN_EMAIL", "admin@oslo.com")
    monkeypatch.setenv("OSLO_DEMO_LOGIN_PASSWORD", "oslo123456")
    monkeypatch.setenv("OSLO_DEMO_USER_ID", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    monkeypatch.setenv("OSLO_DEMO_WORKSPACE_ID", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    client = TestClient(app)
    response = client.post(
        "/auth/login",
        json={"email": "admin@oslo.com", "password": "oslo123456"},
    )

    assert response.status_code == 200
    payload = response.json()
    decoded = jwt.decode(
        payload["access_token"],
        secret,
        algorithms=["HS256"],
        audience="authenticated",
    )
    assert decoded["sub"] == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    assert decoded["app_metadata"] == {
        "workspace_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "role": "owner",
    }

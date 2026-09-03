"""DTM-0036 auth seam — negatives (every failure ⇒ a single 401 unauthenticated).

Missing/blank bearer, malformed header, bad signature, expired token, wrong
audience, an out-of-range role, and each missing required claim
(``sub``/``workspace_id``/``role``) all reject with 401 — the verifier never
leaks *why* (existence/validity not disclosed; API Contract Spec §9, §12).

The dependency-override path is also asserted intact: a test that injects a fixed
Principal still authenticates without any token (the existing command/read suites
rely on this — proven here against the same protected route).
"""

from __future__ import annotations

import time

import jwt
import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import Principal, current_principal, get_projection_reader
from backend.platform.auth import AuthError, verify_token
from tests.positive.api.conftest import PROJECT, WORKSPACE, FakeReader

TEST_SECRET = "test-only-jwt-secret-not-a-real-credential"  # noqa: S105 — ephemeral test value
AUDIENCE = "authenticated"


def _sign(claims: dict, *, secret: str = TEST_SECRET) -> str:
    return jwt.encode(claims, secret, algorithm="HS256")


def _valid_claims(**overrides) -> dict:
    base = {
        "sub": "u-1",
        "aud": AUDIENCE,
        "exp": int(time.time()) + 3600,
        "app_metadata": {"workspace_id": WORKSPACE, "role": "member"},
    }
    base.update(overrides)
    return base


@pytest.fixture
def _jwt_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_JWT_SECRET", TEST_SECRET)


# ---- verifier-level negatives (AuthError) -----------------------------------

def test_bad_signature_rejected(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(), secret="a-different-wrong-secret")
    with pytest.raises(AuthError):
        verify_token(token)


def test_expired_token_rejected(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(exp=int(time.time()) - 10))
    with pytest.raises(AuthError):
        verify_token(token)


def test_wrong_audience_rejected(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(aud="some-other-audience"))
    with pytest.raises(AuthError):
        verify_token(token)


def test_tampered_token_rejected(_jwt_secret: None) -> None:
    token = _sign(_valid_claims())
    tampered = token[:-3] + ("AAA" if not token.endswith("AAA") else "BBB")
    with pytest.raises(AuthError):
        verify_token(tampered)


@pytest.mark.parametrize("missing", ["sub", "workspace_id", "role"])
def test_missing_required_claim_rejected(_jwt_secret: None, missing: str) -> None:
    claims = _valid_claims()
    if missing == "sub":
        claims.pop("sub")
    else:
        claims["app_metadata"].pop(missing)
    with pytest.raises(AuthError):
        verify_token(_sign(claims))


def test_unrecognised_role_rejected(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(app_metadata={"workspace_id": WORKSPACE, "role": "superadmin"}))
    with pytest.raises(AuthError):
        verify_token(token)


def test_secret_not_configured_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_JWT_SECRET", raising=False)
    with pytest.raises(AuthError):
        verify_token(_sign(_valid_claims()))


# ---- transport-level negatives (HTTP 401) -----------------------------------

def _get_projects(headers: dict | None = None) -> int:
    with TestClient(app, raise_server_exceptions=False) as c:
        resp = c.get("/v1/projects", headers=headers or {})
    return resp.status_code


def test_missing_bearer_is_401() -> None:
    assert _get_projects() == 401


def test_blank_bearer_is_401() -> None:
    assert _get_projects({"Authorization": "   "}) == 401


def test_non_bearer_scheme_is_401(_jwt_secret: None) -> None:
    token = _sign(_valid_claims())
    assert _get_projects({"Authorization": f"Basic {token}"}) == 401


def test_bad_signature_over_http_is_401(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(), secret="wrong-secret")
    assert _get_projects({"Authorization": f"Bearer {token}"}) == 401


def test_expired_over_http_is_401(_jwt_secret: None) -> None:
    token = _sign(_valid_claims(exp=int(time.time()) - 10))
    assert _get_projects({"Authorization": f"Bearer {token}"}) == 401


def test_missing_claim_over_http_is_401(_jwt_secret: None) -> None:
    claims = _valid_claims()
    claims["app_metadata"].pop("workspace_id")
    assert _get_projects({"Authorization": f"Bearer {_sign(claims)}"}) == 401


# ---- the override path stays intact -----------------------------------------

def test_dependency_override_authenticates_without_a_token() -> None:
    """Existing suites inject a fixed Principal via dependency_overrides — unchanged."""
    reader = FakeReader()
    reader.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE, "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    })
    app.dependency_overrides[current_principal] = lambda: Principal(
        user_id="u-1", workspace_id=WORKSPACE, role="member")
    app.dependency_overrides[get_projection_reader] = lambda: reader
    try:
        with TestClient(app) as c:
            resp = c.get("/v1/projects")  # NO Authorization header — override supplies the Principal
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200

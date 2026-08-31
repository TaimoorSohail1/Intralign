"""DTM-0036 auth seam — positive path (valid Supabase-style JWT → Principal).

A token signed with a TEST ``SUPABASE_JWT_SECRET`` (NEVER a real secret; this is
an ephemeral per-test value) carrying valid claims verifies and maps to the R1
single-workspace Principal: ``sub`` → ``user_id``; ``workspace_id`` + RBAC
``role`` from ``app_metadata`` (API Contract Spec §3, 51–59; Runtime Env §4).

These tests exercise the REAL verification path — ``current_principal`` is NOT
overridden here (the override path is covered by the existing command/read
suites, which keep injecting a fixed Principal unchanged).
"""

from __future__ import annotations

import time

import jwt
import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.api.deps import get_projection_reader
from backend.platform.auth import VerifiedClaims, verify_token
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


def test_verify_token_maps_claims_to_principal(_jwt_secret: None) -> None:
    """``sub``→user_id, ``app_metadata.workspace_id``/``role`` → workspace_id/role."""
    claims = verify_token(_sign(_valid_claims()))
    assert claims == VerifiedClaims(user_id="u-1", workspace_id=WORKSPACE, role="member")


def test_top_level_workspace_claim_accepted(_jwt_secret: None) -> None:
    """``workspace_id`` may be a top-level custom claim (not only in app_metadata)."""
    token = _sign(_valid_claims(workspace_id=WORKSPACE, app_metadata={"role": "admin"}))
    claims = verify_token(token)
    assert claims.workspace_id == WORKSPACE
    assert claims.role == "admin"


def test_app_metadata_role_wins_over_reserved_top_level_role(_jwt_secret: None) -> None:
    """Supabase reserves top-level ``role`` (=authenticated); RBAC role is in app_metadata."""
    token = _sign(_valid_claims(role="authenticated"))  # reserved Postgres role top-level
    claims = verify_token(token)
    assert claims.role == "member"  # the app_metadata RBAC role, not "authenticated"


def test_valid_token_authenticates_a_protected_read(_jwt_secret: None) -> None:
    """End-to-end over HTTP: a valid bearer scopes the read to its workspace."""
    reader = FakeReader()
    reader.projects.append({
        "project_id": PROJECT, "workspace_id": WORKSPACE, "title": "Demo",
        "lifecycle_state": "oriented", "created_at": "2026-06-25T00:00:00Z",
    })
    app.dependency_overrides[get_projection_reader] = lambda: reader
    token = _sign(_valid_claims())
    try:
        with TestClient(app) as c:
            resp = c.get("/v1/projects", headers={"Authorization": f"Bearer {token}"})
    finally:
        app.dependency_overrides.clear()
    assert resp.status_code == 200
    body = resp.json()
    rows = body["projects"] if isinstance(body, dict) and "projects" in body else body
    assert any(str(r.get("project_id")) == PROJECT for r in rows)

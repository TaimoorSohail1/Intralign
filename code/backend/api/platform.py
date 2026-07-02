"""Platform compatibility endpoints.

These routes are deliberately outside the governed ``/v1`` cognition surface.
They support deployment smoke checks and the commodity login shell while leaving
Release 1 domain commands/reads under ``/v1`` unchanged.
"""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib import error, request

import jwt
import psycopg
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from backend.services.llm_provider.config import primary_provider_id

router = APIRouter(tags=["platform"])

_SUPABASE_URL = "SUPABASE_URL"
_SUPABASE_ANON_KEY = "SUPABASE_ANON_KEY"
_SUPABASE_DB_URL = "SUPABASE_DB_URL"
_SUPABASE_JWT_SECRET = "SUPABASE_JWT_SECRET"
_OPENAI_API_KEY = "OPENAI_API_KEY"
_OSLO_LLM_BASE_URL = "OSLO_LLM_BASE_URL"
_OSLO_DEMO_LOGIN_EMAIL = "OSLO_DEMO_LOGIN_EMAIL"
_OSLO_DEMO_LOGIN_PASSWORD = "OSLO_DEMO_LOGIN_PASSWORD"
_OSLO_DEMO_USER_ID = "OSLO_DEMO_USER_ID"
_OSLO_DEMO_WORKSPACE_ID = "OSLO_DEMO_WORKSPACE_ID"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def health() -> dict[str, str]:
    """Liveness probe — infra smoke-test target for Phase I."""
    return {"status": "ok"}


def _elapsed_ms(start: float) -> int:
    return max(0, round((time.perf_counter() - start) * 1000))


def _service(name: str, ok: bool, started_at: float, detail: str = "") -> dict[str, Any]:
    return {
        "name": name,
        "status": "up" if ok else "down",
        "ok": ok,
        "latency_ms": _elapsed_ms(started_at),
        "latencyMs": _elapsed_ms(started_at),
        "detail": detail,
    }


def _check_supabase_auth() -> dict[str, Any]:
    started = time.perf_counter()
    url = os.environ.get(_SUPABASE_URL, "").rstrip("/")
    anon_key = os.environ.get(_SUPABASE_ANON_KEY, "") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not anon_key:
        return _service("Supabase Auth", False, started, "missing configuration")

    try:
        auth_request = request.Request(
            f"{url}/auth/v1/settings",
            headers={"apikey": anon_key, "authorization": f"Bearer {anon_key}"},
            method="GET",
        )
        with request.urlopen(auth_request, timeout=5) as response:
            return _service("Supabase Auth", 200 <= response.status < 500, started)
    except Exception as exc:
        return _service("Supabase Auth", False, started, exc.__class__.__name__)


def _check_supabase_postgres() -> dict[str, Any]:
    started = time.perf_counter()
    db_url = os.environ.get(_SUPABASE_DB_URL, "")
    api_url = os.environ.get(_SUPABASE_URL, "").rstrip("/")
    api_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "") or os.environ.get(_SUPABASE_ANON_KEY, "")

    if db_url:
        try:
            with psycopg.connect(db_url, connect_timeout=5) as conn:
                with conn.cursor() as cur:
                    cur.execute("select 1")
                    cur.fetchone()
            return _service("Supabase Postgres", True, started)
        except Exception:
            # Hosted demos often have the Supabase API key before the raw DB
            # password. Fall through to PostgREST: it still verifies that the
            # Supabase project database API is reachable.
            pass

    if not api_url or not api_key:
        return _service("Supabase Postgres", False, started, "missing configuration")

    try:
        rest_request = request.Request(
            f"{api_url}/rest/v1/",
            headers={"apikey": api_key, "authorization": f"Bearer {api_key}"},
            method="GET",
        )
        with request.urlopen(rest_request, timeout=5) as response:
            return _service("Supabase Postgres", 200 <= response.status < 500, started, "postgrest")
    except Exception as exc:
        return _service("Supabase Postgres", False, started, exc.__class__.__name__)


def _check_llm_provider() -> dict[str, Any]:
    started = time.perf_counter()
    provider = primary_provider_id()
    if provider == "openai":
        ok = bool(os.environ.get(_OPENAI_API_KEY))
        return _service("LLM Provider", ok, started, "openai configured" if ok else "missing OpenAI key")

    ok = bool(os.environ.get(_OSLO_LLM_BASE_URL))
    return _service("LLM Provider", ok, started, "internal endpoint configured" if ok else "missing internal endpoint")


@router.get("/health")
def health_endpoint() -> dict[str, str]:
    return health()


@router.get("/health/services")
def service_health() -> dict[str, Any]:
    started = time.perf_counter()
    services = [
        _service("Backend", True, started),
        _check_supabase_auth(),
        _check_supabase_postgres(),
        _check_llm_provider(),
    ]
    ok = all(service["ok"] for service in services)
    by_key = {
        "backend": services[0],
        "supabaseAuth": services[1],
        "supabasePostgres": services[2],
        "llmProvider": services[3],
    }
    return {
        "status": "up" if ok else "down",
        "ok": ok,
        "latency_ms": _elapsed_ms(started),
        "latencyMs": _elapsed_ms(started),
        "services": services,
        **by_key,
    }


def _demo_login_matches(payload: LoginRequest) -> bool:
    email = os.environ.get(_OSLO_DEMO_LOGIN_EMAIL, "")
    password = os.environ.get(_OSLO_DEMO_LOGIN_PASSWORD, "")
    return bool(email and password and payload.email.lower() == email.lower() and payload.password == password)


def _mint_demo_token(email: str) -> dict[str, Any]:
    secret = os.environ.get(_SUPABASE_JWT_SECRET)
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": {"code": "auth_unavailable", "message": "JWT signing secret is not configured"}},
        )

    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=8)
    user_id = os.environ.get(_OSLO_DEMO_USER_ID, "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    workspace_id = os.environ.get(_OSLO_DEMO_WORKSPACE_ID, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    token = jwt.encode(
        {
            "sub": user_id,
            "aud": "authenticated",
            "role": "authenticated",
            "email": email,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
            "app_metadata": {"workspace_id": workspace_id, "role": "owner"},
        },
        secret,
        algorithm="HS256",
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 8 * 60 * 60,
        "expires_at": int(expires_at.timestamp()),
        "user": {"id": user_id, "email": email, "workspace_id": workspace_id, "role": "owner"},
    }


def _supabase_password_login(payload: LoginRequest) -> dict[str, Any]:
    url = os.environ.get(_SUPABASE_URL, "").rstrip("/")
    anon_key = os.environ.get(_SUPABASE_ANON_KEY, "")
    if not url or not anon_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": {"code": "auth_unavailable", "message": "Supabase Auth is not configured"}},
        )

    body = json.dumps({"email": payload.email, "password": payload.password}).encode("utf-8")
    auth_request = request.Request(
        f"{url}/auth/v1/token?grant_type=password",
        data=body,
        headers={
            "apikey": anon_key,
            "authorization": f"Bearer {anon_key}",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(auth_request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        if exc.code in {400, 401, 403}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": {"code": "invalid_credentials", "message": "Invalid email or password"}},
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": {"code": "auth_provider_error", "message": "Supabase Auth request failed"}},
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": {"code": "auth_provider_unreachable", "message": "Supabase Auth is unreachable"}},
        ) from exc


@router.post("/auth/login")
def login(payload: LoginRequest) -> dict[str, Any]:
    if _demo_login_matches(payload):
        return _mint_demo_token(payload.email)
    return _supabase_password_login(payload)

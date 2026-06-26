"""Supabase-Auth JWT verification (the DTM-0036 auth seam).

The Supabase Auth (GoTrue) access token is a **HS256 JWT signed with the project
JWT secret** (Runtime Env §4; API Contract Spec §3, 51–59). This module verifies
that token *offline* — signature + expiry — and extracts the claims the app needs:

- ``sub`` → the caller's ``user_id``.
- ``workspace_id`` + ``role`` → the single workspace scope + RBAC role
  (owner/admin/member). Per the Supabase model these are project-issued **custom
  claims** carried in ``app_metadata`` (GoTrue copies ``app_metadata`` into the
  access-token claims); we also accept them as top-level claims for flexibility.

Why offline HS256 (PyJWT) and not the SDK ``get_user``:
``supabase_auth.SyncGoTrueClient.get_user`` validates a token via a **network
round-trip to the Auth server**, which needs a live Supabase instance + network
on every request (unsuitable for the read/command hot path and for offline CI).
Verifying the HS256 signature locally with the env-injected JWT secret is the
conventional, dependency-free (PyJWT already ships transitively with
``supabase``) and testable approach.

**No secret in the repo** (Deployment Governance §7): the signing secret is read
from the environment (``SUPABASE_JWT_SECRET``); a clearly-commented placeholder
lives in ``.env.example`` only. Nothing here prints or embeds a secret value.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import jwt  # PyJWT — ships transitively with `supabase` (supabase_auth requires pyjwt[crypto]>=2.12).

# Supabase GoTrue stamps every access token with ``aud="authenticated"`` for a
# signed-in user. We pin the algorithm to HS256 (the Supabase default) so a
# token cannot be downgraded to ``alg:none`` or coerced to an asymmetric alg.
_ALGORITHMS = ["HS256"]
_AUDIENCE = "authenticated"
_ENV_JWT_SECRET = "SUPABASE_JWT_SECRET"

# Required claims for an R1 Principal (single workspace + RBAC role).
_REQUIRED_ROLES = {"owner", "admin", "member"}


class AuthError(Exception):
    """Raised when a token is missing/blank/tampered/expired or lacks a claim.

    The transport (``current_principal``) maps every ``AuthError`` to a single
    ``401 unauthenticated`` — the verifier never leaks *why* a token failed.
    """


@dataclass(frozen=True)
class VerifiedClaims:
    """The minimal claim set an R1 Principal is built from."""

    user_id: str
    workspace_id: str
    role: str


def _jwt_secret() -> str:
    secret = os.environ.get(_ENV_JWT_SECRET)
    if not secret:
        # Env not provisioned (Deployment Governance §7 — secret comes from the
        # platform store). Treated as an auth failure, not a 500: an
        # unverifiable request is unauthenticated.
        raise AuthError("signing secret not configured")
    return secret


def extract_bearer(authorization: str | None) -> str:
    """Pull the raw token out of an ``Authorization: Bearer <token>`` header."""
    if not authorization or not authorization.strip():
        raise AuthError("missing bearer token")
    parts = authorization.strip().split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise AuthError("malformed authorization header")
    return parts[1].strip()


def _claim(payload: dict, key: str, *, prefer_metadata: bool = False) -> str:
    """Read a required string claim from the token or its ``app_metadata``.

    Supabase carries project-issued custom claims in ``app_metadata``; some
    deployments mint them top-level. Accept either; the value must be a
    non-empty string.

    ``prefer_metadata`` reads ``app_metadata`` *first*. This matters for the
    RBAC ``role``: Supabase reserves a top-level ``role`` claim for the Postgres
    role (``authenticated``), so the application's owner/admin/member role is the
    one in ``app_metadata`` and must win over the reserved top-level value.
    """
    meta = payload.get("app_metadata")
    meta = meta if isinstance(meta, dict) else {}
    if prefer_metadata:
        value = meta.get(key)
        if value in (None, ""):
            value = payload.get(key)
    else:
        value = payload.get(key)
        if value in (None, ""):
            value = meta.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AuthError(f"missing required claim: {key}")
    return value.strip()


def verify_token(token: str, *, secret: str | None = None) -> VerifiedClaims:
    """Verify the HS256 signature + expiry, then extract the R1 claims.

    Raises ``AuthError`` on bad signature, expiry, wrong audience/algorithm, a
    missing required claim, or an out-of-range role — every failure is one 401.
    """
    key = secret if secret is not None else _jwt_secret()
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=_ALGORITHMS,
            audience=_AUDIENCE,
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError as exc:  # expired / bad-sig / bad-aud / malformed
        raise AuthError("invalid token") from exc

    user_id = _claim(payload, "sub")
    workspace_id = _claim(payload, "workspace_id")
    role = _claim(payload, "role", prefer_metadata=True)
    if role not in _REQUIRED_ROLES:
        raise AuthError("unrecognised role claim")

    return VerifiedClaims(user_id=user_id, workspace_id=workspace_id, role=role)

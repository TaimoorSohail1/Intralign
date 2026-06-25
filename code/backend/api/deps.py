"""Shared FastAPI dependencies for the /v1 surface (API Contract Spec §3, §10, §12).

- **Authentication:** a bearer token (Supabase Auth JWT) identifies the caller and
  resolves the single ``workspace_id`` (Data Model §6 — single-workspace per user
  in R1). A missing/blank bearer ⇒ 401 (API Contract Spec §9 ``unauthenticated``).
- **Workspace scoping:** every read resolves to the caller's ``workspace_id``; the
  read seam filters by it (in-app AND Supabase RLS). A resource outside the scope
  is 404 (existence not leaked, §12).
- **Read seam:** ``get_projection_reader`` provides the SELECT-only
  ``ProjectionReader`` (the Disclose read model) — overridable in tests via
  ``app.dependency_overrides`` (the house pattern), wired to Supabase in prod.

Read-mostly: these dependencies expose NO write/accept/compute path. JWT-claim
verification (signature/exp) is the Supabase-Auth seam wired under deployment;
this module establishes the contract surface the routers depend on.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status

from backend.services.render import ProjectionReader, SupabaseProjectionReader


@dataclass(frozen=True)
class Principal:
    """The authenticated caller, scoped to a single workspace (R1)."""

    user_id: str
    workspace_id: str
    role: str  # owner | admin | member (Data Model §6)


def current_principal(
    authorization: str | None = Header(default=None),
) -> Principal:
    """Resolve the bearer token → Principal (401 when absent/blank).

    R1 single-workspace: the verified token carries ``user_id`` + ``workspace_id``
    + ``role``. The signature/exp verification is the Supabase-Auth seam wired at
    deployment; here we require a bearer (the §3 contract) and reject its absence.
    Tests override this dependency to inject a fixed Principal.
    """
    if not authorization or not authorization.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "unauthenticated", "message": "missing bearer token"}},
        )
    raise HTTPException(  # pragma: no cover - replaced by the Supabase-Auth seam / test override
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": {"code": "unauthenticated", "message": "token verification not configured"}},
    )


def get_projection_reader() -> ProjectionReader:
    """Provide the SELECT-only read seam (Supabase in prod; overridden in tests)."""
    from backend.services.persistence import get_supabase_client

    return SupabaseProjectionReader(get_supabase_client())


def require_principal(principal: Principal = Depends(current_principal)) -> Principal:
    """Router-facing auth dependency (a single import point for the routers)."""
    return principal

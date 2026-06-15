"""Shared FastAPI dependencies for the /v1 surface (API Contract Spec §3, §10).

- Authentication: bearer JWT (Supabase Auth) resolves the caller's user_id.
- Workspace scoping: every request resolves to the caller's single workspace_id;
  reads/writes are filtered by it (enforced in-app AND by Supabase RLS).
- Idempotency: commands accept an `Idempotency-Key` header.

Stubs — wired in Phase II under the relevant Wave contract. No un-contracted auth
logic is implemented here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    """The authenticated caller, scoped to a single workspace (R1)."""

    user_id: str
    workspace_id: str
    role: str  # owner | admin | member (Data Model §6)


def current_principal() -> Principal:
    """Resolve the Supabase JWT → Principal. Stub (Phase II)."""
    raise NotImplementedError("Wire Supabase JWT verification + workspace scoping (Phase II).")

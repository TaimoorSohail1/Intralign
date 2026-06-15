"""API error model (API Contract Spec §3, §10, State Model §).

Canonical failure shapes for the /v1 surface:
- 401/403 — unauthenticated / outside workspace scope.
- 404 — resource not in caller's workspace.
- 409 — illegal state transition (source state isn't current) or idempotency conflict.
- 422 — request schema validation failure (FastAPI/Pydantic default).

Concrete handlers are registered on the app under the relevant Wave contract.
"""

from __future__ import annotations


class IllegalTransition(Exception):
    """Raised when a :verb command is issued from a non-current source state (→ 409)."""


class WorkspaceScopeError(Exception):
    """Raised when a request addresses a resource outside the caller's workspace (→ 404/403)."""

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

import threading
from dataclasses import dataclass
from typing import Any

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


# --- Command-surface seams (DTM-0032) ----------------------------------------
# The command routers (analysis :fast/:deep/:cancel, …) consume these provider
# dependencies. Each is overridable via ``app.dependency_overrides`` in tests so
# the transport can be exercised over HTTP without a backing store, and wired to
# the real Supabase-backed seams in production. The command transport invents NO
# orchestration: it calls the existing ``submit_trigger`` seam (materializer
# injected, DTM-0030) and persists the platform ``analysis_run`` via the repo.


def get_analysis_run_repo() -> Any:
    """Provide the platform ``analysis_run`` repo (DTM-0031; Supabase in prod)."""
    from backend.platform.analysis_run_repo import SupabaseAnalysisRunRepository
    from backend.services.persistence import get_supabase_client

    return SupabaseAnalysisRunRepository(get_supabase_client())


def get_trigger_submitter() -> Any:
    """Provide the orchestration ``submit_trigger`` seam (runner; DTM-0030)."""
    from backend.orchestration.runner import submit_trigger

    return submit_trigger


def get_materializer() -> Any:
    """Provide the DTM-0030 ``ProjectionMaterializer`` (so derived.*_current fills).

    Injected into ``submit_trigger`` so a successful deep pass upserts the
    ``derived.*_current`` projection rows the read surfaces read (LDM §3.1).
    """
    from backend.responsibilities.disclose.projection_writer import ProjectionMaterializer
    from backend.responsibilities.retain.repository import ChrRepository
    from backend.services.persistence import get_supabase_client
    from backend.services.persistence.projection_store import SupabaseProjectionStore

    client = get_supabase_client()
    return ProjectionMaterializer(SupabaseProjectionStore(client), ChrRepository(client))


def get_event_emitter() -> Any:
    """Provide the observed event emitter (the A6 seam; collecting by default)."""
    from backend.services.observability.emitters import ObservedEventEmitter
    from backend.services.observability.events import CollectingEventEmitter

    return ObservedEventEmitter.wrap(CollectingEventEmitter())


# --- Project-CRUD + evidence/artifact-intake seams (DTM-0034) -----------------
# The project-command + evidence/artifact-intake router consumes these providers.
# The transport invents NO persistence: project writes go through the DTM-0031
# ``project_repo`` (the platform ``project`` table); evidence/artifact go through
# the EXISTING ``submit_artifact`` intake seam (the append-only ``artifact``
# anchor + ``promotion_candidate`` via the intake store, body via Storage). Each
# provider is overridable via ``app.dependency_overrides`` in tests and wired to
# the real Supabase-backed seams in production.


def get_project_repo() -> Any:
    """Provide the platform ``project`` repo (DTM-0031; Supabase in prod)."""
    from backend.platform.project_repo import SupabaseProjectRepository
    from backend.services.persistence import get_supabase_client

    return SupabaseProjectRepository(get_supabase_client())


def get_intake_store() -> Any:
    """Provide the intake ``artifact``/``promotion_candidate`` store (DTM-0007)."""
    from backend.services.persistence import SupabaseIntakeStore, get_supabase_client

    return SupabaseIntakeStore(get_supabase_client())


def get_body_store() -> Any:
    """Provide the artifact-body Storage seam (bucket ``artifacts``; DTM-0007)."""
    from backend.services.persistence import ArtifactBodyStore, get_supabase_client

    return ArtifactBodyStore(get_supabase_client())


# --- Acceptance-command seams (DTM-0033) -------------------------------------
# The acceptance command router (recommendations :accept/:reject/:defer/:implement)
# consumes these providers. The transport invents NO acceptance logic: it resolves
# the recommendation's current CHR as the mandatory version_pin, builds the capture,
# and calls the EXISTING ``record_acceptance`` retain seam (UAR always; plan fact on
# accept only). Each provider is overridable via ``app.dependency_overrides`` in
# tests and wired to the real Supabase-backed seams in production.


def get_retention_store() -> Any:
    """Provide the append-only retention store (UAR/plan-fact INSERT; Supabase)."""
    from backend.services.persistence import get_supabase_client
    from backend.services.persistence.retention_store import SupabaseRetentionStore

    return SupabaseRetentionStore(get_supabase_client())


def get_acceptance_chr_reader() -> Any:
    """Provide the CHR reader ``record_acceptance`` uses to read the pinned CHR.

    On ``accept`` the plan-fact content is a DATA read of the pinned CHR's
    ``output_payload`` (no LLM) — the existing ``ChrRepository`` satisfies the
    ``ChrReader`` protocol.
    """
    from backend.responsibilities.retain.repository import ChrRepository
    from backend.services.persistence import get_supabase_client

    return ChrRepository(get_supabase_client())


class _IdempotencyStore:
    """In-process Idempotency-Key → response cache (API Contract §10).

    A repeated command with the same key returns the first run unchanged — no
    second persist, no second trigger. R1 single-dyno scope; the durable
    cross-dyno store (Redis) is the flagged follow-up. Keyed by (key, route) so
    the same key on different commands does not collide.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: dict[tuple[str, str], dict[str, Any]] = {}

    def get(self, key: str, route: str) -> dict[str, Any] | None:
        with self._lock:
            return self._records.get((key, route))

    def put(self, key: str, route: str, value: dict[str, Any]) -> None:
        with self._lock:
            self._records[(key, route)] = value


_IDEMPOTENCY_STORE = _IdempotencyStore()


def reset_idempotency_store() -> None:
    """Replace the process-wide idempotency store (test isolation seam)."""
    global _IDEMPOTENCY_STORE
    _IDEMPOTENCY_STORE = _IdempotencyStore()


def get_idempotency_store() -> _IdempotencyStore:
    """Provide the Idempotency-Key cache (overridable in tests)."""
    return _IDEMPOTENCY_STORE


def idempotency_key(
    idempotency_key: str | None = Header(default=None),
) -> str | None:
    """Read the optional ``Idempotency-Key`` header (API Contract §10)."""
    return idempotency_key

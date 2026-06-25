"""Disclose read-surface negatives (DTM-0018) — the Critical invariants.

- Unauthenticated read ⇒ 401 (auth enforced).
- Out-of-workspace project ⇒ 404 (scoping; existence not leaked, §12).
- **No mutation/accept/compute path is reachable from the /v1 read surface**
  (Critical) — every DTM-0018 route is a GET; there is NO POST/PATCH/PUT/DELETE.
- **No internal ``shared.epistemic`` cognition type is serialized verbatim**
  (Critical) — the OpenAPI schema exposes only the external Data-Model DTOs.
"""

from __future__ import annotations

import inspect

import pytest
from fastapi.testclient import TestClient

import shared.epistemic as epistemic
from backend.api.app import app
from backend.api.deps import current_principal, get_projection_reader
from backend.api.v1 import router as v1_router
from tests.positive.api.conftest import PROJECT, FakeReader, Principal


# ---- auth + scoping ----------------------------------------------------------

def test_unauthenticated_read_is_401() -> None:
    """No bearer token ⇒ 401 (the §3 auth contract; current_principal NOT overridden)."""
    with TestClient(app) as c:
        resp = c.get("/v1/projects")
    assert resp.status_code == 401


def test_out_of_workspace_project_is_404() -> None:
    """A project in another workspace is 404 — existence is not leaked (§12)."""
    reader = FakeReader()
    reader.projects.append({
        "project_id": "p-other", "workspace_id": "ws-OTHER",
        "lifecycle_state": "created", "title": "secret",
    })
    app.dependency_overrides[current_principal] = lambda: Principal(
        user_id="u-1", workspace_id="ws-1", role="member")
    app.dependency_overrides[get_projection_reader] = lambda: reader
    try:
        with TestClient(app) as c:
            resp = c.get("/v1/projects/p-other", headers={"Authorization": "Bearer t"})
        assert resp.status_code == 404
    finally:
        app.dependency_overrides.clear()


# ---- read-mostly: NO mutation reachable from the read surface (Critical) -----

def _dtm0018_routes():
    """The routes the DTM-0018 read surface adds (everything under /v1 here)."""
    return [r for r in v1_router.routes if getattr(r, "path", "").startswith("/v1")]


def test_no_mutating_method_on_the_read_surface() -> None:
    """Every DTM-0018 /v1 route is read-only — GET (and HEAD) ONLY (Critical)."""
    mutating = {"POST", "PUT", "PATCH", "DELETE"}
    for route in _dtm0018_routes():
        methods = set(getattr(route, "methods", set()))
        assert not (methods & mutating), (
            f"{route.path} exposes a mutating method {methods & mutating} — the "
            "Disclose read surface must be read-mostly (decision #3/#4)"
        )


def test_read_surface_only_uses_get() -> None:
    """Positively assert the read methods are GET (no accept/compute verb route)."""
    for route in _dtm0018_routes():
        methods = {m for m in getattr(route, "methods", set()) if m not in {"HEAD", "OPTIONS"}}
        assert methods <= {"GET"}, f"{route.path} is not GET-only: {methods}"


def test_no_accept_or_verb_command_path_in_read_surface() -> None:
    """No ``:accept`` / ``:verb`` command path leaks into the DTM-0018 surface."""
    for route in _dtm0018_routes():
        assert ":" not in route.path.rsplit("/", 1)[-1], (
            f"{route.path} looks like a :verb command — acceptance/capture stay on "
            "the existing Wave U seam (decision #3)"
        )


# ---- no internal cognition type serialized verbatim (Critical) ---------------

def test_openapi_does_not_expose_internal_cognition_schemas() -> None:
    """The OpenAPI schema names only external DTOs — never the internal types.

    A faithful proof: the internal cognition classes carry internal-only fields
    (``model_or_rule_version`` / ``understanding_state`` / ``confidence_stage`` /
    ``evidence_anchors``) that must NOT appear as response-schema properties.
    """
    schema = app.openapi()
    components = schema.get("components", {}).get("schemas", {})
    # The external Finding/Recommendation DTOs are present...
    assert "Finding" in components
    assert "Recommendation" in components
    # ...and they carry NONE of the internal-cognition-only fields verbatim.
    internal_only = {"model_or_rule_version", "understanding_state", "confidence_stage"}
    for name in ("Finding", "Recommendation", "ConfidenceState"):
        props = set(components.get(name, {}).get("properties", {}))
        leaked = props & internal_only
        assert not leaked, f"{name} schema leaks internal cognition fields: {leaked}"


def test_entities_module_does_not_reexport_epistemic_types() -> None:
    """shared.entities defines its own DTOs and never imports the internal types."""
    import shared.entities as entities

    assert "from shared.epistemic import" not in inspect.getsource(entities)
    # The DTO classes are distinct from the internal cognition classes.
    assert entities.Finding is not epistemic.Finding
    assert entities.Recommendation is not epistemic.Recommendation


@pytest.mark.parametrize("path", [
    f"/v1/projects/{PROJECT}/findings",
    f"/v1/projects/{PROJECT}/recommendations",
    f"/v1/projects/{PROJECT}/confidence",
])
def test_read_seam_has_no_write_method(path: str) -> None:
    """The ProjectionReader the routers depend on exposes no write surface."""
    from backend.services.render import SupabaseProjectionReader

    write_verbs = {"insert", "update", "delete", "upsert", "append"}
    methods = {m for m in dir(SupabaseProjectionReader) if not m.startswith("_")}
    assert not (methods & write_verbs), (
        f"the read seam exposes a write method {methods & write_verbs} — it must be "
        "SELECT-only (read-mostly)"
    )

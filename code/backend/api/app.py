"""OSLO backend composition root (FastAPI).

Assembles the app, mounts the /v1 router, and serves the OpenAPI schema at
/openapi.json — the single source the frontend's Orval client is generated from.
The transport layer owns NO cognition (Prime Directive: nothing un-contracted).

Run:  uvicorn backend.api.app:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.v1 import router as v1_router
from backend.services.observability.setup import configure_observability

app = FastAPI(
    title="OSLO Release 1 API",
    version="0.1.0",
    description="REST command/query surface over the Release 1 architecture (Data Model v1.2 entities).",
)

configure_observability(app)  # env-driven (DTM-0003); degrades to a warning when OTLP is off

app.include_router(v1_router)


@app.get("/health", tags=["platform"])
def health() -> dict[str, str]:
    """Liveness probe — infra smoke-test target for Phase I (no domain behavior)."""
    return {"status": "ok"}

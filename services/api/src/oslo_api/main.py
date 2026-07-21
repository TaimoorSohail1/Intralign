from fastapi import FastAPI

from oslo_api.api.invitations import router as invitations_router
from oslo_api.api.projects import router as projects_router
from oslo_api.slice_one import SliceOneApplication


def create_app(*, slice_one: SliceOneApplication | None = None) -> FastAPI:
    app = FastAPI(
        title="OSLO Product Grill API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
    )
    app.state.slice_one = slice_one
    app.include_router(invitations_router)
    app.include_router(projects_router)

    @app.get("/health", tags=["operations"])
    def health() -> dict[str, str]:
        return {"status": "ready", "service": "oslo-api"}

    return app


app = create_app()

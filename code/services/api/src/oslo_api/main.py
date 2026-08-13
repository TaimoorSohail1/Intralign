from fastapi import FastAPI

from oslo_api.analysis.advisor import ProjectAdvisor
from oslo_api.api.analysis import router as analysis_router
from oslo_api.api.billing import router as billing_router
from oslo_api.api.collaboration import router as collaboration_router
from oslo_api.api.invitations import router as invitations_router
from oslo_api.api.outcomes import router as outcomes_router
from oslo_api.api.projects import router as projects_router
from oslo_api.api.session import router as session_router
from oslo_api.slice_four import SliceFourApplication
from oslo_api.slice_one import SliceOneApplication
from oslo_api.slice_two import SliceTwoApplication


def create_app(
    *,
    slice_one: SliceOneApplication | None = None,
    slice_two: SliceTwoApplication | None = None,
    project_advisor: ProjectAdvisor | None = None,
    collaboration=None,
    slice_four: SliceFourApplication | None = None,
) -> FastAPI:
    app = FastAPI(
        title="OSLO Product Grill API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
    )
    app.state.slice_one = slice_one
    app.state.slice_two = slice_two
    app.state.project_advisor = project_advisor
    app.state.collaboration = collaboration
    app.state.slice_four = slice_four
    app.include_router(invitations_router)
    app.include_router(projects_router)
    app.include_router(session_router)
    app.include_router(analysis_router)
    app.include_router(collaboration_router)
    app.include_router(billing_router)
    app.include_router(outcomes_router)

    @app.get("/health", tags=["operations"])
    def health() -> dict[str, str]:
        return {"status": "ready", "service": "oslo-api"}

    return app


app = create_app()

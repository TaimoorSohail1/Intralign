/**
 * ProjectOverviewRoute — the thin route element that adapts the TanStack route params
 * into the presentational `ProjectOverview`. It mounts at the project Orientation
 * route (`/projects/$projectId/orientation`), replacing the DTM-0019 placeholder.
 *
 * UI_SCREEN_INVENTORY maps the "60-Second Orientation" screen to "first
 * understanding: confidence, CAF, top findings/recs" — exactly the project-level
 * understanding summary the Project Overview presents. The project Workspace root
 * (`/projects/$projectId/`) is already the MRI umbrella (DTM-0020), so the Overview
 * mounts at the orientation route. The surface takes `projectId` as a prop so it
 * stays trivially testable.
 */
import { getRouteApi } from "@tanstack/react-router";
import { ProjectOverview } from "./ProjectOverview";

const routeApi = getRouteApi("/projects/$projectId/orientation");

export function ProjectOverviewRoute() {
  const { projectId } = routeApi.useParams();
  return <ProjectOverview projectId={projectId} />;
}

export default ProjectOverviewRoute;

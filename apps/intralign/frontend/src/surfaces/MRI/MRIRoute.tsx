/**
 * MRIRoute — the thin route element that adapts the TanStack route param into the
 * presentational `MRIWorkspace`. It mounts at the Project Workspace route
 * (`/projects/$projectId/`), replacing the DTM-0019 placeholder. The workspace
 * itself takes `projectId` as a prop so it stays trivially testable.
 */
import { getRouteApi } from "@tanstack/react-router";
import { MRIWorkspace } from "./MRIWorkspace";

const routeApi = getRouteApi("/projects/$projectId/");

export function MRIRoute() {
  const { projectId } = routeApi.useParams();
  return <MRIWorkspace projectId={projectId} />;
}

export default MRIRoute;

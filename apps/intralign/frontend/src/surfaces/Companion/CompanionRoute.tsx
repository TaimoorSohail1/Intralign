/**
 * CompanionRoute — the thin route element that adapts the TanStack route params into
 * the presentational `Companion`. It mounts at the Companion route
 * (`/projects/$projectId/companion`), replacing the DTM-0019 placeholder. The
 * surface itself takes `projectId` as a prop so it stays trivially testable and
 * decoupled from the router.
 */
import { getRouteApi } from "@tanstack/react-router";
import { Companion } from "./Companion";

const routeApi = getRouteApi("/projects/$projectId/companion");

export function CompanionRoute() {
  const { projectId } = routeApi.useParams();
  return <Companion projectId={projectId} />;
}

export default CompanionRoute;

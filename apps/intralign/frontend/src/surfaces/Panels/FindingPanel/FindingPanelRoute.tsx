/**
 * FindingPanelRoute — the thin route element that adapts the TanStack route params
 * into the presentational `FindingPanel`. It mounts at the Finding-detail route
 * (`/projects/$projectId/findings/$findingId/`), replacing the DTM-0019
 * placeholder. The panel itself takes `projectId` + `findingId` as props so it
 * stays trivially testable.
 */
import { getRouteApi } from "@tanstack/react-router";
import { FindingPanel } from "./FindingPanel";

const routeApi = getRouteApi("/projects/$projectId/findings/$findingId/");

export function FindingPanelRoute() {
  const { projectId, findingId } = routeApi.useParams();
  return <FindingPanel projectId={projectId} findingId={findingId} />;
}

export default FindingPanelRoute;

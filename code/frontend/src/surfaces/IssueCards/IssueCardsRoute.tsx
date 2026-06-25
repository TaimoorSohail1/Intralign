/**
 * IssueCardsRoute — the thin route element that adapts the TanStack route params
 * into the presentational `IssueCards`. It mounts at the project Findings-Workspace
 * route (`/projects/$projectId/findings`), replacing the DTM-0019 placeholder.
 *
 * There is no dedicated "Issues" screen in UI_SCREEN_INVENTORY.md — issues are
 * presented within the project's findings context (`GET /projects/{pid}/findings`),
 * so Issue Cards (prioritized findings) mount at that route. The surface itself
 * takes `projectId` as a prop so it stays trivially testable.
 */
import { getRouteApi } from "@tanstack/react-router";
import { IssueCards } from "./IssueCards";

const routeApi = getRouteApi("/projects/$projectId/findings");

export function IssueCardsRoute() {
  const { projectId } = routeApi.useParams();
  return <IssueCards projectId={projectId} />;
}

export default IssueCardsRoute;

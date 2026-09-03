/**
 * NotificationsRoute — the thin route element that mounts the presentational
 * `Notifications` surface at the top-level `/notifications` route, replacing the
 * DTM-0019 placeholder.
 *
 * The notifications feed is workspace-level (`GET /v1/notifications`). The
 * Acceptance-Impact read is project-scoped, so the route reads an optional
 * `project_id` search param and hands it to the surface; without it, only the
 * workspace notifications feed is shown (the impact read is skipped). The surface
 * itself takes `projectId` as a prop so it stays trivially testable.
 */
import { getRouteApi } from "@tanstack/react-router";
import { Notifications } from "./Notifications";

const routeApi = getRouteApi("/notifications");

export function NotificationsRoute() {
  const search = routeApi.useSearch();
  return <Notifications projectId={search.project_id} />;
}

export default NotificationsRoute;

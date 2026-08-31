/**
 * TimelineRoute — the thin route element that adapts the TanStack route param into
 * the presentational `Timeline` surface. It mounts at the project History route
 * (`/projects/$projectId/history`), replacing the DTM-0019 placeholder. The surface
 * itself takes `projectId` as a prop so it stays trivially testable.
 *
 * History is a SECONDARY project-context surface (Companion-Surface-class) — it
 * lives under a project, never as a primary top-level destination (spec §D).
 */
import { getRouteApi } from "@tanstack/react-router";
import { Timeline } from "./Timeline";

const routeApi = getRouteApi("/projects/$projectId/history");

export function TimelineRoute() {
  const { projectId } = routeApi.useParams();
  return <Timeline projectId={projectId} />;
}

export default TimelineRoute;

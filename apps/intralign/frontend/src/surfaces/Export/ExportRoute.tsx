/**
 * ExportRoute — the thin route element that adapts the TanStack route param into the
 * presentational `Export` surface. It mounts at the project Export route
 * (`/projects/$projectId/export`). The surface takes `projectId` as a prop so it stays
 * trivially testable.
 *
 * Export & Share is a lightweight Companion-Surface-class ACTION (spec §D) — it lives
 * under a project, invoked in context; it is NOT a primary top-level destination and
 * NOT a reporting workspace.
 */
import { getRouteApi } from "@tanstack/react-router";
import { Export } from "./Export";

const routeApi = getRouteApi("/projects/$projectId/export");

export function ExportRoute() {
  const { projectId } = routeApi.useParams();
  return <Export projectId={projectId} />;
}

export default ExportRoute;

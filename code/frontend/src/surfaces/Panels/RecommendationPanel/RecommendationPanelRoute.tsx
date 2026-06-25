/**
 * RecommendationPanelRoute — the thin route element that adapts the TanStack route
 * params into the presentational `RecommendationPanel`. It mounts at the nested
 * recommendations route (`/projects/$projectId/findings/$findingId/recommendations`),
 * replacing the DTM-0019 placeholder.
 *
 * RP-C1 is enforced structurally by the route tree: this element resolves ONLY
 * under a Finding, so `findingId` is always present here. The panel itself accepts
 * `findingId` as an (optional) prop and renders a no-context guard when it is
 * absent, so a standalone mount stays a no-op presentation (a rejected negative).
 */
import { getRouteApi } from "@tanstack/react-router";
import { RecommendationPanel } from "./RecommendationPanel";

const routeApi = getRouteApi(
  "/projects/$projectId/findings/$findingId/recommendations",
);

export function RecommendationPanelRoute() {
  const { projectId, findingId } = routeApi.useParams();
  return <RecommendationPanel projectId={projectId} findingId={findingId} />;
}

export default RecommendationPanelRoute;

/**
 * TanStack Router tree (code-based) for the OSLO app shell.
 *
 * Routes are the Release 1 screens from UI_SCREEN_INVENTORY.md, scoped per the IA
 * in RELEASE_1_UI_SPECIFICATION_V1 §2. Every element is a PLACEHOLDER (DTM-0019
 * ships the shell only); the real surfaces mount here in DTM-0020+.
 *
 * RP-C1 is encoded structurally: the Recommendation Panel route lives ONLY under a
 * Finding (`/projects/$projectId/findings/$findingId/recommendations`), never as a
 * standalone top-level route — so "Recommendation-Panel-only-in-Finding-context" is
 * enforced by the route tree itself, not duplicated as a cognition rule.
 */
import {
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
} from "@tanstack/react-router";
import { AppShell } from "./AppShell";
import { PlaceholderSurface } from "./PlaceholderSurface";
import { MRIRoute } from "../surfaces/MRI/MRIRoute";
import { FindingPanelRoute } from "../surfaces/Panels/FindingPanel/FindingPanelRoute";
import { RecommendationPanelRoute } from "../surfaces/Panels/RecommendationPanel/RecommendationPanelRoute";

const rootRoute = createRootRoute({
  component: AppShell,
});

// ── Top-level screens ──────────────────────────────────────────────────────────
const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => (
    <PlaceholderSurface
      title="Projects"
      purpose="Orient on landing: active projects, current confidence, attention items."
    />
  ),
});

const projectsCreateRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/projects/new",
  component: () => (
    <PlaceholderSurface
      title="Create a project"
      purpose="Create a project; add first intent/evidence; trigger Fast Analysis."
    />
  ),
});

// Project workspace + its sub-surfaces (a layout route with a nested outlet).
const projectRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/projects/$projectId",
  component: () => <Outlet />,
});

// DTM-0020 — the MRI umbrella surface mounts at the Project Workspace route,
// replacing the DTM-0019 placeholder. It is the project's understanding view
// (Findings/CAF/Confidence + the four DL-047 sub-components), read-only.
const projectWorkspaceRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/",
  component: MRIRoute,
});

const orientationRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/orientation",
  component: () => (
    <PlaceholderSurface
      title="60-Second Orientation"
      purpose="First understanding: confidence, CAF, top findings/recs (not final)."
    />
  ),
});

const analysisRunRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/analysis-runs/$runId",
  component: () => (
    <PlaceholderSurface
      title="Analysis Progress"
      purpose="Async status while a fast/deep run executes."
    />
  ),
});

const projectFindingsRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/findings",
  component: () => (
    <PlaceholderSurface
      title="Findings Workspace"
      purpose="Triage and act on findings across their lifecycle."
    />
  ),
});

// Finding detail (the Finding Panel context). RP-C1: recommendations nest here.
const findingRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/findings/$findingId",
  component: () => <Outlet />,
});

// DTM-0021 — the Finding Panel mounts at the Finding-detail route, replacing the
// DTM-0019 placeholder. It presents one finding + its Attested evidence lineage +
// Derived confidence, and the RP-C1 affordance into the nested recommendations
// route. Read-only.
const findingDetailRoute = createRoute({
  getParentRoute: () => findingRoute,
  path: "/",
  component: FindingPanelRoute,
});

// DTM-0022 — the Recommendation Panel mounts at the nested recommendations route,
// replacing the DTM-0019 placeholder. RP-C1: it renders ONLY within a Finding
// context (this route lives only under a Finding). It presents the finding's
// Recommendations as OSLO Recommended + Resolution Paths (presentation grouping,
// no object) with the accept/reject/defer affordance that HANDS OFF to the Wave U
// capture (the project Recommendation Workspace below) — Disclose never accepts.
const findingRecommendationsRoute = createRoute({
  getParentRoute: () => findingRoute,
  path: "/recommendations",
  component: RecommendationPanelRoute,
});

const projectRecommendationsRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/recommendations",
  component: () => (
    <PlaceholderSurface
      title="Recommendation Workspace"
      purpose="Accept/reject/implement recommendations (routes to the Wave U capture)."
    />
  ),
});

const projectReportsRoute = createRoute({
  getParentRoute: () => projectRoute,
  path: "/reports",
  component: () => (
    <PlaceholderSurface
      title="Report Viewer"
      purpose="View, version, publish, archive, export reports."
    />
  ),
});

const artifactRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/artifacts/$artifactId",
  component: () => (
    <PlaceholderSurface
      title="Artifact Editor"
      purpose="View/edit a planning artifact and its versions."
    />
  ),
});

// Cross-project top-level entries (resolve within the active project at build-out).
const findingsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/findings",
  component: () => (
    <PlaceholderSurface
      title="Findings"
      purpose="Findings across the active project context."
    />
  ),
});

const recommendationsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/recommendations",
  component: () => (
    <PlaceholderSurface
      title="Recommendations"
      purpose="Recommendations across the active project context."
    />
  ),
});

const reportsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/reports",
  component: () => (
    <PlaceholderSurface title="Reports" purpose="Reports across the workspace." />
  ),
});

const sharedRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/shared",
  component: () => (
    <PlaceholderSurface
      title="Shared Artifacts"
      purpose="Scoped read (view/comment) of a shared object."
    />
  ),
});

const sharedDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/shared/$shareId",
  component: () => (
    <PlaceholderSurface
      title="Shared Artifact Viewer"
      purpose="Scoped read (view/comment) of a shared object."
    />
  ),
});

const notificationsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/notifications",
  component: () => (
    <PlaceholderSurface
      title="Notification Center"
      purpose="In-product awareness feed."
    />
  ),
});

const settingsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/settings",
  component: () => (
    <PlaceholderSurface title="User Settings" purpose="Profile and workspace basics." />
  ),
});

const routeTree = rootRoute.addChildren([
  dashboardRoute,
  projectsCreateRoute,
  projectRoute.addChildren([
    projectWorkspaceRoute,
    orientationRoute,
    analysisRunRoute,
    projectFindingsRoute,
    findingRoute.addChildren([findingDetailRoute, findingRecommendationsRoute]),
    projectRecommendationsRoute,
    projectReportsRoute,
  ]),
  artifactRoute,
  findingsRoute,
  recommendationsRoute,
  reportsRoute,
  sharedRoute,
  sharedDetailRoute,
  notificationsRoute,
  settingsRoute,
]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

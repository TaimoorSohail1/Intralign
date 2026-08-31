/**
 * Test harness for the Recommendation Panel — wraps the panel in the MUI
 * ThemeProvider, a fresh TanStack Query client, and a minimal in-memory TanStack
 * Router whose tree mirrors the real RP-C1 nesting: the finding-detail route with
 * a nested `recommendations` child (where the panel mounts).
 *
 * Two router builders:
 *  - `makeRouter` mounts the panel UNDER a finding (the only legitimate context),
 *    so the panel's accept/reject/defer affordance `<Link>`s resolve and a test
 *    can assert that activating "accept" navigates to the Wave U capture/confirm
 *    step — never a local state mutation.
 *  - `makeStandaloneRouter` mounts the SAME panel at a top-level `/recommendations`
 *    route with NO finding context, so a test can prove RP-C1: outside a finding
 *    context the panel renders no recommendations / no resolution paths.
 *
 * It is a *.tsx under src/ but is never imported by the app bundle — the surface
 * mounts via the real app router.
 */
import type { ReactElement } from "react";
import { render } from "@testing-library/react";
import { ThemeProvider } from "@mui/material/styles";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter,
  createMemoryHistory,
  Outlet,
} from "@tanstack/react-router";
import { theme } from "../../../theme";

/**
 * Build a router whose path shape matches the app: a project route, a finding
 * route under it, the finding-detail index, the nested recommendations child
 * (where `ui` mounts, RP-C1), and a stub Wave U capture target so the
 * accept/reject/defer hand-off `<Link>` can resolve and navigation be asserted.
 */
function makeRouter(ui: ReactElement, projectId: string, findingId: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });
  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
  const findingRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/findings/$findingId",
    component: () => <Outlet />,
  });
  const findingDetailRoute = createRoute({
    getParentRoute: () => findingRoute,
    path: "/",
    component: () => <div data-testid="finding-panel-target" />,
  });
  const recommendationsRoute = createRoute({
    getParentRoute: () => findingRoute,
    path: "/recommendations",
    component: () => ui,
  });
  // Stand-in for the EXISTING Wave U capture route (the hand-off destination). The
  // panel's accept/reject/defer affordance routes here; it performs NO acceptance.
  const recommendationsWorkspaceRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/recommendations",
    component: () => <div data-testid="wave-u-capture-target" />,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([
        findingRoute.addChildren([findingDetailRoute, recommendationsRoute]),
        recommendationsWorkspaceRoute,
      ]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/findings/${findingId}/recommendations`],
    }),
  });
}

/**
 * Build a router that mounts the panel at a STANDALONE top-level `/recommendations`
 * route — NO finding context. RP-C1: the panel must not render recommendations or
 * resolution paths here. (A standalone Recommendation Panel is a rejected negative.)
 */
function makeStandaloneRouter(ui: ReactElement) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });
  const standaloneRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/recommendations",
    component: () => ui,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([standaloneRoute]),
    history: createMemoryHistory({ initialEntries: ["/recommendations"] }),
  });
}

export interface RenderRecommendationPanelOptions {
  projectId?: string;
  findingId?: string;
  /** When false, mount the panel with NO finding context (RP-C1 negative). */
  inFindingContext?: boolean;
}

/**
 * Render the Recommendation Panel with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and the affordance `<Link>`s)
 * is present synchronously after `await`.
 */
export async function renderRecommendationPanel(
  ui: ReactElement,
  {
    projectId = "proj-001",
    findingId = "f-conflict-1",
    inFindingContext = true,
  }: RenderRecommendationPanelOptions = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = inFindingContext
    ? makeRouter(ui, projectId, findingId)
    : makeStandaloneRouter(ui);
  await router.load();
  const utils = render(
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ThemeProvider>,
  );
  return { ...utils, router };
}

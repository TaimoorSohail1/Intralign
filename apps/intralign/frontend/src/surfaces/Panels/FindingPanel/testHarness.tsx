/**
 * Test harness for the Finding Panel — wraps the panel in the MUI ThemeProvider, a
 * fresh TanStack Query client, and a minimal in-memory TanStack Router whose tree
 * mirrors the real RP-C1 nesting: the finding-detail route with a nested
 * `recommendations` child. This lets the panel's "view recommendations" `<Link>`
 * resolve AND lets a test assert that activating it navigates to the nested
 * recommendation route (and nowhere else). It is a *.tsx under src/ but is never
 * imported by the app bundle — the surface mounts via the real app router.
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
 * route under it, the finding-detail index (where `ui` mounts), and the nested
 * recommendations child (RP-C1). The recommendations child renders a stable
 * `data-testid` so navigation can be asserted.
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
    component: () => ui,
  });
  const recommendationsRoute = createRoute({
    getParentRoute: () => findingRoute,
    path: "/recommendations",
    component: () => <div data-testid="rec-panel-target" />,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([
        findingRoute.addChildren([findingDetailRoute, recommendationsRoute]),
      ]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/findings/${findingId}`],
    }),
  });
}

export interface RenderFindingPanelOptions {
  projectId?: string;
  findingId?: string;
}

/**
 * Render the Finding Panel with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and the "view
 * recommendations" `<Link>`) is present synchronously after `await`.
 */
export async function renderFindingPanel(
  ui: ReactElement,
  { projectId = "proj-001", findingId = "f-conflict-1" }: RenderFindingPanelOptions = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui, projectId, findingId);
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

/**
 * Test harness for the Overview surfaces (Dashboard + Project Overview). Wraps a
 * surface in the MUI ThemeProvider, a fresh TanStack Query client, and a minimal
 * in-memory TanStack Router whose tree mirrors the real paths:
 *   - the Dashboard at `/` (where the project list mounts), whose per-project
 *     "Open workspace" `<Link>` targets `/projects/$projectId`;
 *   - the project workspace target `/projects/$projectId` so that link resolves AND
 *     a test can assert navigation lands on the workspace (and nowhere else).
 *
 * The harness mounts the surface at `/` by default; pass `initialPath` to mount the
 * Project Overview under a project. It is a *.tsx under src/ but is never imported by
 * the app bundle — the surfaces mount via the real app router.
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
import { theme } from "../../theme";

function makeRouter(ui: ReactElement, initialPath: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });

  // Dashboard at `/` — where the project list mounts.
  const dashboardRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: () => ui,
  });

  // Project route + its workspace target (where each project's "Open workspace"
  // link lands) and an orientation child (where the Project Overview mounts).
  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
  const projectWorkspaceRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/",
    component: () => <div data-testid="project-workspace-target" />,
  });
  const projectOverviewRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/orientation",
    component: () => ui,
  });

  return createRouter({
    routeTree: rootRoute.addChildren([
      dashboardRoute,
      projectRoute.addChildren([projectWorkspaceRoute, projectOverviewRoute]),
    ]),
    history: createMemoryHistory({ initialEntries: [initialPath] }),
  });
}

export interface RenderOverviewOptions {
  initialPath?: string;
}

/**
 * Render an Overview surface with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and the surface's links) is
 * present synchronously after `await`.
 */
export async function renderOverview(
  ui: ReactElement,
  { initialPath = "/" }: RenderOverviewOptions = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui, initialPath);
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

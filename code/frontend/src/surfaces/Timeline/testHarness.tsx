/**
 * Test harness for the History / Timeline surface — wraps it in the MUI
 * ThemeProvider, a fresh TanStack Query client, and a minimal in-memory TanStack
 * Router whose tree mirrors the real app paths the surface routes into:
 *   - `/projects/$projectId/history` (where the surface mounts),
 *   - a project workspace route (a trail item → the project's current understanding).
 *
 * The History surface ROUTES to retained context but hosts NO structured actions
 * (Companion-Surface-class, spec §D). This lets each trail item's "view context"
 * `<Link>` resolve and lets a test assert it navigates to retained context (never
 * anywhere that would change an assessment). It is a *.tsx under src/ but is never
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
import { theme } from "../../theme";

function makeRouter(ui: ReactElement, projectId: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });
  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
  const projectWorkspaceRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/",
    component: () => <div data-testid="mri-target" />,
  });
  const historyRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/history",
    component: () => ui,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([projectWorkspaceRoute, historyRoute]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/history`],
    }),
  });
}

/**
 * Render the History / Timeline surface with theme + query + router context. Async:
 * the in-memory router is loaded first so route content (and each item's `<Link>`)
 * is present synchronously after `await`.
 */
export async function renderTimeline(ui: ReactElement, projectId = "proj-001") {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui, projectId);
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

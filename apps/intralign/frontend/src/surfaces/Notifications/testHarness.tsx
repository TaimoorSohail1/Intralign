/**
 * Test harness for the Notification / Awareness surface — wraps it in the MUI
 * ThemeProvider, a fresh TanStack Query client, and a minimal in-memory TanStack
 * Router whose tree mirrors the real app paths the surface routes into:
 *   - `/notifications` (where the surface mounts),
 *   - a Finding-detail route (a notification → its source Finding),
 *   - a project workspace route (a notification → Project Overview / MRI),
 *   - a finding route reached by an Acceptance-Impact item (the affected accepted
 *     item routes through its Finding, never to a standalone Recommendation Panel).
 *
 * This lets each awareness item's "open source" `<Link>` resolve AND lets a test
 * assert that activating it navigates to the source context (and nowhere that
 * would change an assessment). It is a *.tsx under src/ but is never imported by
 * the app bundle — the surface mounts via the real app router.
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

function makeRouter(ui: ReactElement) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });
  const notificationsRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/notifications",
    component: () => ui,
  });
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
  const orientationRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/orientation",
    component: () => <div data-testid="overview-target" />,
  });
  const findingDetailRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/findings/$findingId",
    component: () => <div data-testid="finding-panel-target" />,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      notificationsRoute,
      projectRoute.addChildren([
        projectWorkspaceRoute,
        orientationRoute,
        findingDetailRoute,
      ]),
    ]),
    history: createMemoryHistory({ initialEntries: ["/notifications"] }),
  });
}

/**
 * Render the Notifications surface with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and each item's source
 * `<Link>`) is present synchronously after `await`.
 */
export async function renderNotifications(ui: ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui);
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

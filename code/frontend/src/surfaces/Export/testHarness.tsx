/**
 * Test harness for the Export / Share-out surface — wraps it in the MUI
 * ThemeProvider, a fresh TanStack Query client, and a minimal in-memory TanStack
 * Router whose tree mirrors the real app path the surface mounts at:
 *   - `/projects/$projectId/export` (where the surface mounts).
 *
 * The Export surface is a lightweight Companion-Surface-class ACTION (spec §D) — it
 * packages existing understanding and offers a download/preview; it hosts NO
 * understanding-changing actions and routes nowhere that would change an assessment.
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
  const exportRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/export",
    component: () => ui,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([projectWorkspaceRoute, exportRoute]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/export`],
    }),
  });
}

export async function renderExport(ui: ReactElement, projectId = "proj-001") {
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

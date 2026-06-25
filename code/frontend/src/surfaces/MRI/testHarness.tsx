/**
 * Test harness for MRI surfaces — wraps a component in the MUI ThemeProvider, a
 * fresh TanStack Query client, and a minimal in-memory TanStack Router so that the
 * drill-down `<Link>`s in MRI (→ Finding Panel) have a router context. Used only
 * by the MRI Vitest suites (it is a *.tsx under src/ but never imported by the app
 * bundle — the surface mounts via the real app router).
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
  const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: () => ui,
  });
  // A catch-all so MRI drill-down links (to Finding Panel routes) resolve in tests.
  const catchAll = createRoute({
    getParentRoute: () => rootRoute,
    path: "$",
    component: () => <div data-testid="nav-target" />,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([indexRoute, catchAll]),
    history: createMemoryHistory({ initialEntries: ["/"] }),
  });
}

/**
 * Render an MRI component/surface with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and any drill-down `<Link>`s)
 * is present synchronously after `await`. Callers `await renderMRI(...)`.
 */
export async function renderMRI(ui: ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui);
  await router.load();
  return render(
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ThemeProvider>,
  );
}

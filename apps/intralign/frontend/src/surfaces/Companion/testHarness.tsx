/**
 * Test harness for the Understanding Companion — wraps it in the MUI ThemeProvider,
 * a fresh TanStack Query client, and a minimal in-memory TanStack Router whose tree
 * mirrors the real paths so the Companion's `<Link>`s resolve AND a test can assert
 * where navigation lands:
 *   - the Companion mount at `/projects/$projectId/companion`;
 *   - the **Finding Panel** target `/projects/$projectId/findings/$findingId` (where
 *     BOTH a Top Finding and — per Option B — a Top Recommendation must land);
 *   - the nested **Recommendation Panel** target
 *     `/projects/$projectId/findings/$findingId/recommendations` so a test can prove
 *     the Companion does NOT route there directly (RP-C1 preserved);
 *   - a **standalone** project Recommendation route `/projects/$projectId/recommendations`
 *     so a test can prove the Companion never routes to a standalone Recommendation
 *     Panel either;
 *   - an OSLO Chat target `/projects/$projectId/chat` for the Ask OSLO entry.
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
import { theme } from "../../theme";

function makeRouter(ui: ReactElement, projectId: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });

  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });

  // Where the Companion mounts.
  const companionRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/companion",
    component: () => ui,
  });

  // The Finding-detail context (the Finding Panel). Both Top Findings AND — via
  // Option B — Top Recommendations must navigate HERE.
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
  // The Recommendation Panel nested under a Finding — present so a test can prove
  // the Companion does NOT land here directly.
  const findingRecommendationsRoute = createRoute({
    getParentRoute: () => findingRoute,
    path: "/recommendations",
    component: () => <div data-testid="recommendation-panel-target" />,
  });

  // A standalone project-level Recommendation route — present so a test can prove
  // the Companion never routes to a standalone Recommendation Panel.
  const standaloneRecommendationsRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/recommendations",
    component: () => <div data-testid="standalone-recommendation-target" />,
  });

  // OSLO Chat (the Ask OSLO entry).
  const chatRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/chat",
    component: () => <div data-testid="chat-target" />,
  });

  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([
        companionRoute,
        findingRoute.addChildren([findingDetailRoute, findingRecommendationsRoute]),
        standaloneRecommendationsRoute,
        chatRoute,
      ]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/companion`],
    }),
  });
}

export interface RenderCompanionOptions {
  projectId?: string;
}

/**
 * Render the Companion with theme + query + router context. Async: the in-memory
 * router is loaded first so route content (and the surface's links) is present
 * synchronously after `await`.
 */
export async function renderCompanion(
  ui: ReactElement,
  { projectId = "proj-001" }: RenderCompanionOptions = {},
) {
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

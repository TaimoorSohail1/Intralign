/**
 * Test harness for the Assisted-Editing / Persistent-Intelligence panel — wraps it in
 * the MUI ThemeProvider, a fresh TanStack Query client, and a minimal in-memory router
 * whose tree mirrors the real routing TARGETS so the panel's assist `<Link>`s resolve
 * AND a test can assert WHERE an assist lands:
 *   - the panel mounts in the Artifact Editor at `/artifacts/$artifactId`;
 *   - the assist-to-Chat (B1) target `/projects/$projectId/chat`;
 *   - the assist-to-Suggested-Fix (B3) target — the Recommendation lives only in a
 *     Finding context (RP-C1), so the panel routes to the Finding Panel
 *     `/projects/$projectId/findings/$findingId` (never a standalone rec panel).
 *
 * Never imported by the app bundle — the surface mounts via the real app router.
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

function makeRouter(ui: ReactElement, artifactId: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });

  // Where the panel mounts (the Artifact Editor).
  const artifactRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/artifacts/$artifactId",
    component: () => ui,
  });

  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
  // B1 — assist routes to Chat (carrying inherited context as search params).
  const chatRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/chat",
    validateSearch: (
      search: Record<string, unknown>,
    ): { context_kind?: string; context_id?: string; context_label?: string } => ({
      context_kind:
        typeof search.context_kind === "string" ? search.context_kind : undefined,
      context_id: typeof search.context_id === "string" ? search.context_id : undefined,
      context_label:
        typeof search.context_label === "string" ? search.context_label : undefined,
    }),
    component: () => <div data-testid="chat-target" />,
  });
  // B3 — assist routes to a Suggested Fix, reached via its Finding (RP-C1).
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

  return createRouter({
    routeTree: rootRoute.addChildren([
      artifactRoute,
      projectRoute.addChildren([
        chatRoute,
        findingRoute.addChildren([findingDetailRoute]),
      ]),
    ]),
    history: createMemoryHistory({ initialEntries: [`/artifacts/${artifactId}`] }),
  });
}

export interface RenderAssistedEditingOptions {
  artifactId?: string;
}

export async function renderAssistedEditing(
  ui: ReactElement,
  { artifactId = "artf-001" }: RenderAssistedEditingOptions = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui, artifactId);
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

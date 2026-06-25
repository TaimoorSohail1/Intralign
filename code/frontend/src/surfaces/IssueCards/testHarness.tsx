/**
 * Test harness for the Issue Cards surface — wraps it in the MUI ThemeProvider, a
 * fresh TanStack Query client, and a minimal in-memory TanStack Router whose tree
 * mirrors the real path: the project Findings-Workspace route (where Issue Cards
 * mount) plus a finding-detail child (the Finding Panel context). This lets each
 * card's "view source finding" `<Link>` resolve AND lets a test assert that
 * activating it navigates to the source Finding (and nowhere else). It is a *.tsx
 * under src/ but is never imported by the app bundle — the surface mounts via the
 * real app router.
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

/**
 * Build a router whose path shape matches the app: a project route, the
 * findings-workspace index under it (where `ui` mounts), and a finding-detail
 * child (the source-Finding target each card links to). The detail child renders
 * a stable `data-testid` so navigation can be asserted.
 */
function makeRouter(ui: ReactElement, projectId: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });
  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
  const findingsRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/findings",
    component: () => ui,
  });
  const findingDetailRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/findings/$findingId",
    component: () => <div data-testid="finding-panel-target" />,
  });
  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([findingsRoute, findingDetailRoute]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/findings`],
    }),
  });
}

export interface RenderIssueCardsOptions {
  projectId?: string;
}

/**
 * Render the Issue Cards surface with theme + query + router context. Async: the
 * in-memory router is loaded first so route content (and each card's source-finding
 * `<Link>`) is present synchronously after `await`.
 */
export async function renderIssueCards(
  ui: ReactElement,
  { projectId = "proj-001" }: RenderIssueCardsOptions = {},
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

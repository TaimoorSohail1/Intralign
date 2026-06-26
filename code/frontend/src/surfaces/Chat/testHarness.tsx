/**
 * Test harness for OSLO Chat — wraps it in the MUI ThemeProvider, a fresh TanStack Query
 * client, and a minimal in-memory router whose tree mirrors the real paths so the Chat
 * surface's handoff `<Link>`s resolve AND a test can assert WHERE a handoff lands:
 *   - Chat mounts at `/projects/$projectId/chat`;
 *   - the Finding-Panel handoff target `/projects/$projectId/findings/$findingId`.
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

function makeRouter(ui: ReactElement, projectId: string, search: string) {
  const rootRoute = createRootRoute({ component: () => <Outlet /> });

  const projectRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/projects/$projectId",
    component: () => <Outlet />,
  });
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
    component: () => ui,
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

  return createRouter({
    routeTree: rootRoute.addChildren([
      projectRoute.addChildren([
        chatRoute,
        findingRoute.addChildren([findingDetailRoute]),
      ]),
    ]),
    history: createMemoryHistory({
      initialEntries: [`/projects/${projectId}/chat${search}`],
    }),
  });
}

export interface RenderChatOptions {
  projectId?: string;
  /** The search string appended to the chat URL (context-inheritance params). */
  search?: string;
}

export async function renderChat(
  ui: ReactElement,
  { projectId = "proj-001", search = "" }: RenderChatOptions = {},
) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  const router = makeRouter(ui, projectId, search);
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

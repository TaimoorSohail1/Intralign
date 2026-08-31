/**
 * DTM-0042 — Frontend navigation reconciliation.
 *
 * The nav model is active-project-aware: a GLOBAL group always renders; a
 * PROJECT-CONTEXT group renders only when the route is under `/projects/$projectId`,
 * with every link targeting the ACTIVE project's built Wave E surfaces. RP-C1 is
 * preserved (no standalone Recommendations entry) and Category-E commodity screens
 * (Reports, Shared) are NOT silent "Surface pending" dead-ends.
 *
 * These tests mount the REAL AppShell inside the REAL app router (a memory history),
 * so the nav, the active-project derivation, and the surface that resolves are all
 * exercised end to end.
 */
import { describe, it, expect, vi } from "vitest";
import { render, screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { ThemeProvider } from "@mui/material/styles";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider, createRouter, createMemoryHistory } from "@tanstack/react-router";
import { theme } from "../theme";
import { router as appRouter } from "./router";
import { GLOBAL_NAV, buildProjectNav, activeProjectIdFromPath } from "./navModel";

// The surfaces consume DTM-0018 generated hooks. We stub them with loading/empty
// states so the surfaces render their shells (the test asserts NAV + which surface
// resolves, not surface data). Every hook returns the React Query shape.
const empty = { data: undefined, isLoading: false, isError: false, error: null };
vi.mock("../api/generated/projects/projects", () => ({
  useListProjectsV1ProjectsGet: () => ({ ...empty, data: { data: [] } }),
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => empty,
  useCreateProjectV1ProjectsPost: () => ({ mutate: vi.fn(), isPending: false }),
}));
vi.mock("../api/generated/findings/findings", () => ({
  useListFindingsV1ProjectsProjectIdFindingsGet: () => ({ ...empty, data: { data: [] } }),
}));
vi.mock("../api/generated/confidence/confidence", () => ({
  useGetCafV1ProjectsProjectIdCafGet: () => empty,
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => empty,
}));
vi.mock("../api/generated/analysis-runs/analysis-runs", () => ({
  useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet: () => ({ ...empty, data: { data: [] } }),
}));

const PROJECT_ID = "proj-001";

async function renderAppAt(path: string) {
  // Build a fresh router instance over the SAME route tree, with a memory history
  // seeded at `path`. (We reuse the app router's tree via options.)
  const router = createRouter({
    routeTree: appRouter.routeTree,
    history: createMemoryHistory({ initialEntries: [path] }),
  });
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
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

describe("navModel (pure)", () => {
  it("derives the active project id from a project-scoped path", () => {
    expect(activeProjectIdFromPath("/projects/proj-001")).toBe("proj-001");
    expect(activeProjectIdFromPath("/projects/proj-001/findings")).toBe("proj-001");
    expect(activeProjectIdFromPath("/projects/proj-001/chat")).toBe("proj-001");
  });

  it("returns null for global / non-project paths (incl. /projects/new)", () => {
    expect(activeProjectIdFromPath("/")).toBeNull();
    expect(activeProjectIdFromPath("/notifications")).toBeNull();
    expect(activeProjectIdFromPath("/settings")).toBeNull();
    expect(activeProjectIdFromPath("/projects/new")).toBeNull();
  });

  it("builds project-context links against the active project (built surfaces only)", () => {
    const tos = buildProjectNav(PROJECT_ID).map((e) => e.to);
    expect(tos).toEqual([
      `/projects/${PROJECT_ID}`,
      `/projects/${PROJECT_ID}/orientation`,
      `/projects/${PROJECT_ID}/findings`,
      `/projects/${PROJECT_ID}/history`,
      `/projects/${PROJECT_ID}/export`,
      `/projects/${PROJECT_ID}/companion`,
      `/projects/${PROJECT_ID}/chat`,
    ]);
  });

  it("RP-C1: the project nav has NO standalone Recommendations entry", () => {
    const labels = buildProjectNav(PROJECT_ID).map((e) => e.label.toLowerCase());
    expect(labels).not.toContain("recommendations");
    expect(labels).not.toContain("recommendation");
    // and no link ends at a bare /recommendations
    const tos = buildProjectNav(PROJECT_ID).map((e) => e.to);
    expect(tos.some((t) => t.endsWith("/recommendations"))).toBe(false);
  });

  it("global nav has no Reports / Shared Artifacts entry (Category-E, no R1 surface)", () => {
    const labels = GLOBAL_NAV.map((e) => e.label.toLowerCase());
    expect(labels).not.toContain("reports");
    expect(labels).not.toContain("shared artifacts");
    expect(labels).not.toContain("recommendations");
  });
});

describe("AppShell nav — global group", () => {
  it("renders the global group on every route (Dashboard)", async () => {
    await renderAppAt("/");
    const global = screen.getByTestId("nav-global");
    expect(within(global).getByText("Projects")).toBeInTheDocument();
    expect(within(global).getByText("Notifications")).toBeInTheDocument();
    expect(within(global).getByText("Settings")).toBeInTheDocument();
  });

  it("on the Dashboard the project-context group is hidden (an open-a-project hint shows instead)", async () => {
    await renderAppAt("/");
    expect(screen.queryByTestId("nav-project")).not.toBeInTheDocument();
    expect(screen.getByTestId("nav-project-hint")).toBeInTheDocument();
  });

  it("Settings is shown DISABLED ('Not in Release 1'), never a silent dead-end", async () => {
    await renderAppAt("/");
    const deferred = screen.getByTestId("nav-deferred");
    expect(deferred).toHaveTextContent("Settings");
    expect(deferred).toHaveTextContent(/not in release 1/i);
    // a disabled MUI ListItemButton is not a link and is aria-disabled
    expect(deferred.querySelector("a")).toBeNull();
  });
});

describe("AppShell nav — project-context group", () => {
  it("renders the project group with links to the active project's built surfaces", async () => {
    await renderAppAt(`/projects/${PROJECT_ID}/findings`);
    const projectNav = screen.getByTestId("nav-project");
    const hrefs = within(projectNav)
      .getAllByRole("link")
      .map((a) => a.getAttribute("href"));
    for (const sub of ["", "/orientation", "/findings", "/history", "/export", "/companion", "/chat"]) {
      expect(hrefs).toContain(`/projects/${PROJECT_ID}${sub}`);
    }
  });

  it("RP-C1: the rendered project nav exposes no Recommendations link", async () => {
    await renderAppAt(`/projects/${PROJECT_ID}`);
    const projectNav = screen.getByTestId("nav-project");
    expect(within(projectNav).queryByText(/recommendation/i)).not.toBeInTheDocument();
  });

  it("clicking Findings in a project context lands on the Issue Cards surface (NOT a placeholder)", async () => {
    const { router } = await renderAppAt(`/projects/${PROJECT_ID}`);
    // sanity: we start on the MRI workspace, not Issue Cards
    const projectNav = screen.getByTestId("nav-project");
    fireEvent.click(within(projectNav).getByText("Findings"));
    await router.invalidate();
    // The Issue Cards surface titles itself "Issues" (src/surfaces/IssueCards).
    expect(await screen.findByTestId("issue-cards")).toBeInTheDocument();
    expect(screen.getByTestId("surface-title")).toHaveTextContent("Issues");
    // NEGATIVE: it is NOT the leftover "Surface pending" placeholder.
    expect(screen.queryByText(/surface pending/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Findings across the active project context/i)).not.toBeInTheDocument();
  });
});

describe("router reconciliation — no built-surface dead-ends", () => {
  it("the leftover top-level placeholder routes are gone (/findings is not a flatMatch)", () => {
    // The flat top-level routes were removed; the route tree should not contain a
    // child whose full path is exactly "/findings" / "/recommendations" / "/reports"
    // / "/shared" off the root.
    const topLevelPaths = appRouter.routeTree.children
      ? Object.values(appRouter.routeTree.children).map((r: any) => r.path)
      : [];
    expect(topLevelPaths).not.toContain("/findings");
    expect(topLevelPaths).not.toContain("/recommendations");
    expect(topLevelPaths).not.toContain("/reports");
    expect(topLevelPaths).not.toContain("/shared");
    expect(topLevelPaths).not.toContain("/shared/$shareId");
  });

  it("navigating directly to the OLD top-level /findings no longer resolves to a placeholder", async () => {
    // With the flat route removed, /findings is not matched (404/notFound). The key
    // assertion is the negative: it does NOT render the old "Surface pending" stub.
    await renderAppAt("/findings");
    expect(screen.queryByText(/Findings across the active project context/i)).not.toBeInTheDocument();
  });
});

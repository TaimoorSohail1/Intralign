/**
 * DTM-0024 — Dashboard / Project List (IC-WE-DISCLOSE E1).
 *
 * Presents the user's workspace projects, each with its **current Outcome
 * Confidence** as a Derived `EpistemicLabel` (banded, conflict-aware) and a **link
 * to its workspace**. Read-only; it PRESENTS, NEVER GENERATES — no
 * edit/score/accept/generate control, confidence never reads as project
 * health/readiness/probability/%, and the list never becomes a metrics cockpit.
 *
 * The DTM-0018 generated hooks are mocked with fixture DTOs:
 *   - `useListProjects…`  → the project set (GET /projects)
 *   - `useGetConfidence…` → the per-row current confidence (GET /projects/{pid}/confidence)
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderOverview } from "./testHarness";
import { projectsFixture, confidenceByProject } from "./fixtures";

// ── Mock the DTM-0018 reads (the surface consumes, never re-implements) ──────────
const projectsState = {
  data: { data: projectsFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../api/generated/projects/projects", () => ({
  useListProjectsV1ProjectsGet: () => projectsState,
}));

// Per-row confidence: keyed by the project id the hook is called with.
vi.mock("../../api/generated/confidence/confidence", () => ({
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: (projectId: string) => ({
    data: confidenceByProject[projectId]
      ? { data: confidenceByProject[projectId] }
      : undefined,
    isLoading: false,
    isError: false,
    error: null,
  }),
}));

// Imported AFTER the mocks (vi.mock is hoisted).
import { Dashboard } from "./Dashboard";

function mount() {
  return renderOverview(<Dashboard />);
}

beforeEach(() => {
  projectsState.isLoading = false;
  projectsState.isError = false;
  projectsState.error = null;
  projectsState.data = { data: projectsFixture };
});

describe("Dashboard — lists each project with current confidence + a workspace link", () => {
  it("renders one row per project", async () => {
    await mount();
    const surface = screen.getByTestId("dashboard");
    const rows = within(surface).getAllByTestId("project-row");
    expect(rows.length).toBe(projectsFixture.length);
  });

  it("each row shows the project name", async () => {
    await mount();
    expect(screen.getByText("Atlas platform migration")).toBeInTheDocument();
    expect(screen.getByText("Q3 onboarding revamp")).toBeInTheDocument();
    expect(screen.getByText("Compliance evidence pack")).toBeInTheDocument();
  });

  it("each analyzed project shows its current confidence as a Derived label (banded, never settled)", async () => {
    await mount();
    const rows = screen.getAllByTestId("project-row");
    // proj-001 has confidence → a Derived label with a band chip
    const row1 = rows[0];
    const label = within(row1).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "derived");
    expect(within(row1).getByTestId("confidence-band")).toBeInTheDocument();
  });

  it("a project without confidence yet shows a clean 'not yet available', not a fabricated value", async () => {
    await mount();
    const rows = screen.getAllByTestId("project-row");
    const row3 = rows[2]; // proj-003: created, no confidence
    expect(within(row3).getByTestId("confidence-unavailable")).toBeInTheDocument();
    expect(within(row3).queryByTestId("epistemic-label")).not.toBeInTheDocument();
  });

  it("each row links to the project's workspace", async () => {
    await mount();
    const rows = screen.getAllByTestId("project-row");
    const link = within(rows[0]).getByTestId("open-workspace");
    expect(link).toHaveAttribute("href", "/projects/proj-001");
  });

  it("activating a row's workspace link routes to that project's workspace", async () => {
    const { router } = await mount();
    const rows = screen.getAllByTestId("project-row");
    const link = within(rows[1]).getByTestId("open-workspace");
    fireEvent.click(link);
    await router.invalidate();
    expect(router.state.location.pathname).toBe("/projects/proj-002");
  });
});

describe("Dashboard — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    projectsState.isLoading = true;
    projectsState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("dashboard")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-loading")).toBeInTheDocument();
  });

  it("renders a clean, positive empty state when the workspace has no projects", async () => {
    projectsState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("dashboard")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-empty")).toBeInTheDocument();
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("Dashboard — NEGATIVES: presents, never generates; not project health", () => {
  it("exposes NO edit / score / accept / generate / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
    ];
    const forbidden =
      /\bedit\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("no project row ever renders confidence as settled / attested (it stays Derived)", async () => {
    await mount();
    const surface = screen.getByTestId("dashboard");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    for (const label of within(surface).getAllByTestId("epistemic-label")) {
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("confidence never reads as project health / readiness / probability / a bare score / %", async () => {
    await mount();
    const surface = screen.getByTestId("dashboard");
    expect(within(surface).queryByText(/\bhealth\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\breadiness\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bprobability\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bon[- ]?track\b/i)).not.toBeInTheDocument();
    // no bare numeric confidence value / percentage is rendered for a project
    expect(surface.textContent ?? "").not.toMatch(/\b82\b|\b34\b|%/);
  });

  it("the high-band project renders its band exactly as the governed value (no upgrade)", async () => {
    await mount();
    const rows = screen.getAllByTestId("project-row");
    const band = within(rows[0]).getByTestId("confidence-band");
    expect(band).toHaveAttribute(
      "data-band",
      confidenceByProject["proj-001"]!.label!.confidence_band,
    );
  });
});

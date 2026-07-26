import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

import { WorkspaceHome } from "./workspace-home";

const push = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

const workspace: WorkspaceSummary = {
  id: "workspace-1",
  name: "OSLO Alpha",
  role: "owner",
  plan: "free",
  active_project_limit: 1,
  projects: [
    {
      id: "project-1",
      name: "Active transformation",
      status: "active",
      archived: false,
      updated_at: "2026-07-26T10:00:00Z",
      analysis_status: "current",
      confidence_index: 62,
      confidence_band: "Moderate",
      reliability: "Moderate",
      open_issues: 4,
      artifact_count: 7,
    },
    {
      id: "project-2",
      name: "Archived launch",
      status: "active",
      archived: true,
      updated_at: "2026-07-25T10:00:00Z",
      analysis_status: "current",
      confidence_index: 70,
      confidence_band: "High",
      reliability: "High",
      open_issues: 1,
      artifact_count: 7,
    },
  ],
  notifications: [
    {
      key: "analysis:run-1",
      project_id: "project-1",
      project_name: "Active transformation",
      kind: "extended",
      status: "completed",
      title: "Extended Analysis complete",
      created_at: "2026-07-26T10:00:00Z",
      read: false,
    },
  ],
};

describe("WorkspaceHome", () => {
  beforeEach(() => {
    push.mockReset();
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("shows project awareness, activity and the free-plan limit prompt", () => {
    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);

    expect(screen.getByRole("heading", { name: "OSLO Alpha" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Active transformation" })).toBeInTheDocument();
    expect(screen.getByText("26 Jul 2026")).toBeInTheDocument();
    expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument();
    expect(screen.getByText(/There is no portfolio score, average, or ranking/)).toBeInTheDocument();
    expect(screen.getByText("1 active project included")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getByText("Your active project space is full")).toBeInTheDocument();
    expect(within(dialog).getByRole("button", { name: "Archive" })).toBeInTheDocument();
    expect(within(dialog).getByRole("link", { name: "Explore upgrade" })).toBeInTheDocument();
  });

  it("archives without deleting and exposes the retained project", async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 }));
    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);

    fireEvent.click(screen.getByRole("button", { name: "Archive Active transformation" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/projects/project-1/archive",
        { method: "POST" },
      );
    });

    fireEvent.click(screen.getByRole("button", { name: /Archived projects/ }));
    expect(screen.getAllByText("Read-only · retained safely")).toHaveLength(2);
  });

  it("creates a project and routes into intake when capacity is available", async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ id: "project-new" }), {
        status: 201,
        headers: { "content-type": "application/json" },
      }),
    );
    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, projects: workspace.projects.filter((project) => project.archived) }}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    await waitFor(() => {
      expect(push).toHaveBeenCalledWith("/intake?project=project-new");
    });
  });

  it("keeps legacy over-limit workspaces usable without rendering an unbounded dialog", () => {
    const legacyProjects = Array.from({ length: 8 }, (_, index) => ({
      ...workspace.projects[0],
      id: `legacy-${index}`,
      name: `Legacy project ${index + 1}`,
      updated_at: `2026-07-${String(10 + index).padStart(2, "0")}T10:00:00Z`,
    }));

    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, projects: legacyProjects }}
      />,
    );

    expect(
      screen.getByText("1 active project included · 8 existing projects retained"),
    ).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    const dialog = screen.getByRole("dialog");
    expect(within(dialog).getAllByRole("button", { name: "Archive" })).toHaveLength(5);
    expect(
      within(dialog).getByText(/5 most recently updated projects from 8 active projects/),
    ).toBeInTheDocument();
  });

  it("keeps legacy over-limit users in the capacity dialog after archiving one project", async () => {
    const legacyProjects = Array.from({ length: 3 }, (_, index) => ({
      ...workspace.projects[0],
      id: `legacy-${index}`,
      name: `Legacy project ${index + 1}`,
      updated_at: `2026-07-${String(20 + index).padStart(2, "0")}T10:00:00Z`,
    }));
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 }));

    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, projects: legacyProjects }}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "New project" }));
    fireEvent.click(within(screen.getByRole("dialog")).getAllByRole("button", { name: "Archive" })[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/projects/legacy-2/archive",
        { method: "POST" },
      );
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByText(/Archive 2 more active projects to create a new one/)).toBeInTheDocument();
  });
});

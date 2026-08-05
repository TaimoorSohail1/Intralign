import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
  plan_label: "Free",
  price_usd_monthly: 0,
  document_limit: 20,
  word_limit: 50_000,
  collaborator_seat_limit: 3,
  monthly_analysis_limit: null,
  monthly_analyses_used: 0,
  can_manage_plan: true,
  active_project_limit: 1,
  can_create_project: true,
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

  it("shows project awareness and creates another active project", async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ id: "project-new" }), {
        status: 201,
        headers: { "content-type": "application/json" },
      }),
    );
    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);

    expect(screen.getByRole("heading", { name: "OSLO Alpha" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Active transformation" })).toBeInTheDocument();
    expect(screen.getByText("26 Jul 2026")).toBeInTheDocument();
    expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument();
    expect(screen.getByText(/There is no portfolio score, average, or ranking/)).toBeInTheDocument();
    expect(screen.getByText("1 active project")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith("/api/projects/new", { method: "POST" });
      expect(push).toHaveBeenCalledWith("/intake?project=project-new");
    });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
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

  it("creates a project and routes into intake from an empty workspace", async () => {
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

  it("blocks new projects when the active-project allowance is exhausted", async () => {
    const existingProjects = Array.from({ length: 8 }, (_, index) => ({
      ...workspace.projects[0],
      id: `existing-${index}`,
      name: `Existing project ${index + 1}`,
      updated_at: `2026-07-${String(10 + index).padStart(2, "0")}T10:00:00Z`,
    }));
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ id: "project-nine" }), {
        status: 201,
        headers: { "content-type": "application/json" },
      }),
    );

    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, can_create_project: false, projects: existingProjects }}
      />,
    );
    expect(screen.getByRole("button", { name: "New project" })).toBeDisabled();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("restores an archived project while another project is active", async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 }));

    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);
    fireEvent.click(screen.getByRole("button", { name: /Archived projects/ }));
    fireEvent.click(screen.getByRole("button", { name: "Restore" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/projects/project-2/restore",
        { method: "POST" },
      );
    });
  });
});

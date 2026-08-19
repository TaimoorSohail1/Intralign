import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

import { WorkspaceHome } from "./workspace-home";

const push = vi.fn();
const workspaceStyles = readFileSync(resolve(process.cwd(), "src/app/globals.css"), "utf8");

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
      weakest_pillar: "Grounding",
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
      weakest_pillar: "Viability",
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

    expect(screen.getByRole("heading", { name: "Your project" })).toBeInTheDocument();
    expect(screen.getByText("Pick up where understanding stands.")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Active transformation" })).toBeInTheDocument();
    expect(screen.getByText(/No portfolio score across plans/)).toBeInTheDocument();
    expect(screen.getAllByText("New project")).not.toHaveLength(0);
    expect(screen.getByRole("link", { name: /Open the project/ })).toBeInTheDocument();
    expect(screen.getByText("Weakest pillar")).toBeInTheDocument();
    expect(screen.getByText("Grounding")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith("/api/projects/new", { method: "POST" });
      expect(push).toHaveBeenCalledWith("/intake?project=project-new&returning=1");
    });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("uses the prototype dark surface for the active-project capacity modal", () => {
    const modalStyles = workspaceStyles.match(/\.project-capacity-modal\s*\{(?<body>[^}]*)\}/)?.groups?.body;

    expect(modalStyles).toContain("background: #171c21");
    expect(modalStyles).toContain("color: #e8ecef");
    expect(modalStyles).not.toContain("#f7f7f5");
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

    expect(screen.getAllByText("Read-only · retained safely")).toHaveLength(2);
  });

  it("can create a new project immediately after archiving the active project", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ id: "project-new" }), {
          status: 201,
          headers: { "content-type": "application/json" },
        }),
      );
    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, can_create_project: false }}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Archive Active transformation" }));
    await waitFor(() => {
      expect(screen.getByText("Create your first plan")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole("button", { name: "New project" }));
    await waitFor(() => {
      expect(fetch).toHaveBeenLastCalledWith("/api/projects/new", { method: "POST" });
      expect(push).toHaveBeenCalledWith("/intake?project=project-new&returning=1");
    });
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
        initial={{ ...workspace, projects: [] }}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "New project" }));

    await waitFor(() => {
      expect(push).toHaveBeenCalledWith("/intake?project=project-new");
    });
  });

  it("explains the limit when the active-project allowance is exhausted", async () => {
    const existingProjects = Array.from({ length: 8 }, (_, index) => ({
      ...workspace.projects[0],
      id: `existing-${index}`,
      name: `Existing project ${index + 1}`,
      updated_at: `2026-07-${String(10 + index).padStart(2, "0")}T10:00:00Z`,
    }));
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ detail: { wall_key: "multiPlan" } }), {
        status: 422,
        headers: { "content-type": "application/json" },
      }),
    );

    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, can_create_project: false, projects: existingProjects }}
      />,
    );
    const newProject = screen.getByRole("button", { name: "New project" });
    expect(newProject).toBeEnabled();
    fireEvent.click(newProject);

    await waitFor(() => {
      expect(screen.getByRole("dialog", { name: "Run more than one plan" })).toBeInTheDocument();
      expect(fetch).toHaveBeenCalledWith("/api/projects/new", { method: "POST" });
    });

    fireEvent.click(screen.getByRole("button", { name: /Upgrade your plan/ }));
    expect(screen.getByRole("dialog", { name: "Your plan" })).toBeInTheDocument();
  });

  it("explains the limit when the project switcher requests a new project", async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ detail: { wall_key: "multiPlan" } }), {
        status: 422,
        headers: { "content-type": "application/json" },
      }),
    );
    render(
      <WorkspaceHome
        displayName="Taimoor"
        initial={{ ...workspace, can_create_project: false }}
        openNewProject
      />,
    );

    expect(await screen.findByRole("dialog", { name: "Run more than one plan" })).toBeInTheDocument();
    expect(screen.getByRole("dialog", { name: "Run more than one plan" })).toHaveTextContent(
      "Working several plans in your workspace",
    );
    expect(fetch).toHaveBeenCalledWith("/api/projects/new", { method: "POST" });
  });

  it("archives the current project from the capacity choice and continues into intake", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ detail: { wall_key: "multiPlan" } }), {
          status: 422,
          headers: { "content-type": "application/json" },
        }),
      )
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ id: "project-new" }), {
          status: 201,
          headers: { "content-type": "application/json" },
        }),
      );

    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);
    fireEvent.click(screen.getByRole("button", { name: "New project" }));
    const capacity = await screen.findByRole("dialog", { name: "Run more than one plan" });

    fireEvent.click(
      within(capacity).getByRole("button", { name: /Archive Active transformation to free the slot/ }),
    );

    await waitFor(() => {
      expect(fetch).toHaveBeenNthCalledWith(
        2,
        "/api/workspace/projects/project-1/archive",
        { method: "POST" },
      );
      expect(fetch).toHaveBeenNthCalledWith(3, "/api/projects/new", { method: "POST" });
      expect(push).toHaveBeenCalledWith("/intake?project=project-new&returning=1");
    });
  });

  it("creates only one project when New plan is clicked repeatedly while the request is pending", async () => {
    let resolveRequest: ((response: Response) => void) | undefined;
    vi.mocked(fetch).mockImplementation(() => new Promise<Response>((resolve) => {
      resolveRequest = resolve;
    }));

    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);
    const newProject = screen.getByRole("button", { name: "New project" });

    fireEvent.click(newProject);
    fireEvent.click(newProject);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(newProject).toBeDisabled();

    resolveRequest?.(new Response(JSON.stringify({ id: "project-new" }), {
      status: 201,
      headers: { "content-type": "application/json" },
    }));

    await waitFor(() => {
      expect(push).toHaveBeenCalledWith("/intake?project=project-new&returning=1");
    });
  });

  it("restores an archived project while another project is active", async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 }));

    render(<WorkspaceHome displayName="Taimoor" initial={workspace} />);
    fireEvent.click(screen.getByRole("button", { name: "Restore" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/projects/project-2/restore",
        { method: "POST" },
      );
    });
  });
});

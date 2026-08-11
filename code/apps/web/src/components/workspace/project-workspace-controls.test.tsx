import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

import { ProjectWorkspaceControls } from "./project-workspace-controls";

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
  projects: [
    {
      id: "project-1",
      name: "Transformation",
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
  ],
  notifications: [
    {
      key: "analysis:run-1",
      project_id: "project-1",
      project_name: "Transformation",
      kind: "extended",
      status: "completed",
      title: "Extended Analysis complete",
      created_at: "2026-07-26T10:00:00Z",
      read: false,
    },
  ],
};

describe("ProjectWorkspaceControls", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(workspace), {
          status: 200,
          headers: { "content-type": "application/json" },
        }),
      ),
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("opens the project switcher and closes it with Escape", async () => {
    render(<ProjectWorkspaceControls projectId="project-1" />);

    const switcher = await screen.findByRole("button", {
      name: "Transformation",
    });
    expect(switcher).toHaveAttribute("title", "Switch project");
    fireEvent.click(switcher);

    expect(screen.getByRole("menuitem", { name: /Workspace Home/ })).toHaveAttribute(
      "href",
      "/workspace",
    );
    expect(screen.getByRole("menuitem", { name: /New project/ })).toHaveAttribute(
      "href",
      "/workspace?new=1",
    );

    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
  });

  it("shows durable notifications and marks them read", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(JSON.stringify(workspace), {
          status: 200,
          headers: { "content-type": "application/json" },
        }),
      )
      .mockResolvedValueOnce(new Response(null, { status: 204 }));

    render(<ProjectWorkspaceControls projectId="project-1" />);
    await waitFor(() => expect(screen.getByLabelText("Notifications")).toHaveTextContent("1"));

    fireEvent.click(screen.getByLabelText("Notifications"));
    expect(screen.getByRole("dialog", { name: "Notifications" })).toBeInTheDocument();
    expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Mark all read" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenLastCalledWith("/api/workspace/notifications/read", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ keys: ["analysis:run-1"] }),
      });
    });
    expect(screen.getByText("0 unread")).toBeInTheDocument();
    expect(screen.getByText(/Awareness only/)).toBeInTheDocument();
  });

  it("shows one unread notification for one event even when the API repeats it", async () => {
    const duplicateWorkspace: WorkspaceSummary = {
      ...workspace,
      notifications: [
        workspace.notifications[0],
        { ...workspace.notifications[0] },
      ],
    };
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify(duplicateWorkspace), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    );

    render(<ProjectWorkspaceControls projectId="project-1" />);
    await waitFor(() => expect(screen.getByLabelText("Notifications")).toHaveTextContent("1"));

    fireEvent.click(screen.getByLabelText("Notifications"));
    expect(screen.getAllByText("Extended Analysis complete")).toHaveLength(1);
  });

  it("distinguishes notifications from separate unnamed projects", async () => {
    const unnamedWorkspace: WorkspaceSummary = {
      ...workspace,
      notifications: [
        {
          ...workspace.notifications[0],
          key: "analysis:run-a",
          project_id: "aaaaaaaa-1111-2222-3333-444444444444",
          project_name: "Untitled project",
        },
        {
          ...workspace.notifications[0],
          key: "analysis:run-b",
          project_id: "bbbbbbbb-1111-2222-3333-444444444444",
          project_name: "Untitled project",
        },
      ],
    };
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify(unnamedWorkspace), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    );

    render(<ProjectWorkspaceControls projectId="project-1" />);
    await waitFor(() => expect(screen.getByLabelText("Notifications")).toHaveTextContent("2"));

    fireEvent.click(screen.getByLabelText("Notifications"));
    expect(screen.getByText(/Untitled project · aaaaaaaa/)).toBeInTheDocument();
    expect(screen.getByText(/Untitled project · bbbbbbbb/)).toBeInTheDocument();
  });

  it("bounds a large project list and lets the user search it", async () => {
    const largeWorkspace: WorkspaceSummary = {
      ...workspace,
      projects: Array.from({ length: 14 }, (_, index) => ({
        ...workspace.projects[0],
        id: `project-${index + 1}`,
        name: index === 12 ? "Northstar transformation" : `Project ${index + 1}`,
        updated_at: `2026-07-${String(index + 1).padStart(2, "0")}T10:00:00Z`,
      })),
    };
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify(largeWorkspace), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    );

    render(<ProjectWorkspaceControls projectId="project-1" />);
    await screen.findByRole("button", { name: /Project 1/ });
    fireEvent.click(screen.getByRole("button", { name: /Project 1/ }));

    expect(screen.getAllByRole("menuitem")).toHaveLength(11);
    expect(screen.getByRole("menuitem", { name: /View all 14 projects/ })).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Find a project"), {
      target: { value: "Northstar" },
    });
    expect(screen.getByRole("menuitem", { name: /Northstar transformation/ })).toBeInTheDocument();
    expect(screen.queryByRole("menuitem", { name: /View all 14 projects/ })).not.toBeInTheDocument();
  });

  it("does not break the project when workspace awareness is unavailable", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("offline"));
    render(<ProjectWorkspaceControls projectId="project-1" />);

    expect(screen.getByRole("button", { name: "Project" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Project" }));
    expect(screen.getByRole("menuitem", { name: /Workspace Home/ })).toBeInTheDocument();
  });

  it("keeps a large notification history within a useful panel", async () => {
    const notificationWorkspace: WorkspaceSummary = {
      ...workspace,
      notifications: Array.from({ length: 14 }, (_, index) => ({
        ...workspace.notifications[0],
        key: `analysis:run-${index + 1}`,
        title: `Analysis update ${index + 1}`,
      })),
    };
    vi.mocked(fetch).mockResolvedValueOnce(
      new Response(JSON.stringify(notificationWorkspace), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    );

    render(<ProjectWorkspaceControls projectId="project-1" />);
    await waitFor(() => expect(screen.getByLabelText("Notifications")).toHaveTextContent("14"));
    fireEvent.click(screen.getByLabelText("Notifications"));

    expect(screen.getByText("Analysis update 1")).toBeInTheDocument();
    expect(screen.getByText("Analysis update 8")).toBeInTheDocument();
    expect(screen.queryByText("Analysis update 9")).not.toBeInTheDocument();
    expect(screen.getByText(/Notifications never start analysis/)).toBeInTheDocument();
  });

  it("places the governed plan control in the project sidebar footer", async () => {
    render(
      <>
        <div data-testid="sidebar-plan-slot" id="project-sidebar-plan" />
        <ProjectWorkspaceControls
          planPortalId="project-sidebar-plan"
          projectId="project-1"
        />
      </>,
    );

    const slot = screen.getByTestId("sidebar-plan-slot");
    await waitFor(() => {
      expect(within(slot).getByRole("button", { name: "Free" })).toBeInTheDocument();
    });
    expect(within(slot).getByText("Free plan")).toBeInTheDocument();
    expect(within(slot).getByText("Your plan")).toBeInTheDocument();

    fireEvent.click(within(slot).getByRole("button", { name: "Free" }));
    expect(
      await screen.findByRole("heading", { name: "Usage & limits" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Monthly analyses")).toBeInTheDocument();
    expect(screen.getByText("Active projects")).toBeInTheDocument();
  });

  it("starts a real refresh when Update now is selected", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(
        new Response(JSON.stringify(workspace), {
          status: 200,
          headers: { "content-type": "application/json" },
        }),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ run_id: "refresh-run-1" }), {
          status: 202,
          headers: { "content-type": "application/json" },
        }),
      );

    render(<ProjectWorkspaceControls projectId="project-1" />);
    fireEvent.click(await screen.findByRole("button", { name: "Free" }));
    fireEvent.click(screen.getByRole("button", { name: "Update now" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenLastCalledWith(
        "/api/projects/project-1/analysis-runs/refresh",
        { method: "POST" },
      );
    });
  });
});

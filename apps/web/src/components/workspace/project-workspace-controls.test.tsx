import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { WorkspaceSummary } from "@/lib/server/oslo-api";

import { ProjectWorkspaceControls } from "./project-workspace-controls";

const workspace: WorkspaceSummary = {
  id: "workspace-1",
  name: "OSLO Alpha",
  role: "owner",
  plan: "free",
  active_project_limit: 1,
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
    expect(screen.getByRole("link", { name: "View workspace activity" })).toBeInTheDocument();
  });
});

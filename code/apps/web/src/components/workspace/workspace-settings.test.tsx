import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { WorkspaceSettings } from "./workspace-settings";

const initial = {
  theme: "dark" as const,
  analysis_notifications: true,
  failure_notifications: true,
  stale_notifications: true,
  display_name: "Taimoor",
  role_title: "",
  workspace_name: "OSLO Alpha",
  actor_role: "owner" as const,
  mentions_notifications: true,
  reply_notifications: true,
  shared_notifications: true,
};

const workspace = {
  id: "workspace-1",
  name: "OSLO Alpha",
  role: "owner" as const,
  plan: "free" as const,
  plan_label: "Free",
  price_usd_monthly: 0,
  document_limit: 20,
  word_limit: 50_000,
  collaborator_seat_limit: 3,
  monthly_analysis_limit: 8,
  monthly_analyses_used: 3,
  can_manage_plan: true,
  member_count: 2,
  projects: [
    {
      id: "project-1",
      name: "Current project",
      status: "active",
      archived: false,
      updated_at: "2026-08-01T00:00:00Z",
      analysis_status: "completed",
      confidence_index: 3,
      confidence_band: "Moderate",
      reliability: "Moderate",
      open_issues: 2,
      artifact_count: 7,
    },
  ],
  notifications: [],
};

describe("WorkspaceSettings", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation((_url: string, init?: RequestInit) =>
        Promise.resolve(
          new Response(
            typeof init?.body === "string" ? init.body : JSON.stringify(initial),
            {
              status: 200,
              headers: { "content-type": "application/json" },
            },
          ),
        ),
      ),
    );
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({
        matches: false,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }),
    );
  });

  afterEach(() => {
    cleanup();
    document.documentElement.removeAttribute("data-theme");
    document.documentElement.removeAttribute("data-theme-preference");
    localStorage.clear();
    vi.unstubAllGlobals();
  });

  it("renders all settings sections and persists appearance choices", async () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        initial={initial}
        workspaceName="OSLO Alpha"
      />,
    );

    expect(screen.getByRole("navigation", { name: "Settings" }).querySelectorAll("a")).toHaveLength(12);
    expect(screen.getByRole("heading", { name: "Account & workspace" })).toBeInTheDocument();
    expect(screen.getByRole("searchbox", { name: "Search settings" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Light" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/preferences",
        expect.objectContaining({
          method: "PUT",
          body: expect.stringContaining('"theme":"light"'),
          keepalive: true,
        }),
      );
    });
    expect(document.documentElement.dataset.theme).toBe("light");
    expect(screen.getByRole("button", { name: "Light" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByText("Saved")).toBeInTheDocument();
  });

  it("persists notification preferences without starting analysis", async () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        initial={initial}
        workspaceName="OSLO Alpha"
      />,
    );

    const mentions = screen.getByRole("switch", { name: "Mentions" });
    expect(mentions).toHaveAttribute("aria-checked", "true");
    fireEvent.click(mentions);
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/preferences",
        expect.objectContaining({
          body: expect.stringContaining('"mentions_notifications":false'),
        }),
      );
    });
    fireEvent.click(screen.getByRole("switch", { name: /Analysis complete/ }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/preferences",
        expect.objectContaining({
          body: expect.stringContaining('"analysis_notifications":false'),
        }),
      );
    });
  });

  it("filters settings and exposes honest account and plan controls", () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        initial={initial}
        workspaceName="OSLO Alpha"
      />,
    );

    expect(screen.getByRole("button", { name: "Sign out" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Delete account" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Free vs Basic" })).toBeInTheDocument();

    fireEvent.change(screen.getByRole("searchbox", { name: "Search settings" }), {
      target: { value: "notifications" },
    });

    expect(screen.getByRole("heading", { name: "Notifications" })).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Profile" })).not.toBeInTheDocument();
  });

  it("persists profile fields and renders the sole Owner membership role", async () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        initial={{ ...initial, actor_role: "owner" }}
        workspaceName="OSLO Alpha"
      />,
    );

    const roleTitle = screen.getByRole("textbox", { name: "Role or title optional" });
    fireEvent.change(roleTitle, { target: { value: "Programme lead" } });
    fireEvent.blur(roleTitle);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/preferences",
        expect.objectContaining({
          body: expect.stringContaining('"role_title":"Programme lead"'),
        }),
      );
    });
    expect(screen.getByText("Owner")).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: /Manage invitations/ })).not.toHaveLength(0);
    expect(
      screen.getByRole("textbox", { name: /Workspace name/ }),
    ).toBeEnabled();
  });

  it("matches the GA access, membership, subscription, and later-version settings contract", () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        email="taimoor@example.com"
        initial={initial}
        workspace={workspace}
        workspaceName="OSLO Alpha"
      />,
    );

    expect(screen.getByRole("heading", { name: "Access & invites" })).toBeInTheDocument();
    expect(screen.getByText("GA")).toBeInTheDocument();
    expect(screen.getAllByText("Not capacity-gated")).toHaveLength(2);
    expect(screen.getByText(/Invitations and membership do not change/)).toBeInTheDocument();
    expect(
      screen.getAllByRole("link", { name: /Manage invitations/ }).every(
        (link) => link.getAttribute("href") === "/admin/invitations",
      ),
    ).toBe(true);

    expect(screen.getByRole("heading", { name: /Membership/ })).toBeInTheDocument();
    expect(screen.getByText("2 members")).toBeInTheDocument();
    expect(screen.getByText("2 active")).toBeInTheDocument();
    expect(screen.getByText("2 active · no plan cap")).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: /Subscription/ })).toBeInTheDocument();
    expect(screen.getByText("1 of 1 active project")).toBeInTheDocument();
    expect(screen.getByText("Uncapped on every plan")).toBeInTheDocument();
    expect(screen.getByText("~50k Free · ~100k Basic")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Free vs Basic" })).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: /Billing/ })).toBeInTheDocument();
    expect(screen.getByText("$29 / month · $290 / year")).toBeInTheDocument();
    expect(screen.getByText("Flat · never per seat")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /Integrations/ })).toBeInTheDocument();
    expect(screen.getByText("Arrives after this release")).toBeInTheDocument();
  });
});

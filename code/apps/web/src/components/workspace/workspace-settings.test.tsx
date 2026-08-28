import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { WorkspaceSettings, WorkspaceSettingsDialog } from "./workspace-settings";

const initial = {
  theme: "dark" as const,
  analysis_notifications: true,
  failure_notifications: true,
  stale_notifications: true,
  display_name: "Taimoor",
  role_title: "I run the plan",
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
  collaborator_seats_used: 2,
  active_project_limit: 1,
  projects: [{
    id: "project-1", name: "Current project", status: "active", archived: false,
    updated_at: "2026-08-01T00:00:00Z", analysis_status: "completed",
    confidence_index: 3, confidence_band: "Moderate", reliability: "Moderate",
    open_issues: 2, artifact_count: 7,
  }],
  notifications: [],
};

function renderSettings(initialSection: "profile" | "appearance" | "notifications" | "workspace" | "collaboration" | "access" | "membership" | "plan" | "billing" | "integrations" = "profile") {
  const onClose = vi.fn();
  render(<WorkspaceSettings displayName="Taimoor" email="taimoor@example.com" initial={initial} initialSection={initialSection} modal onClose={onClose} workspace={workspace} workspaceName="OSLO Alpha" />);
  return { onClose };
}

describe("WorkspaceSettings", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation((_url: string, init?: RequestInit) => Promise.resolve(new Response(typeof init?.body === "string" ? init.body : JSON.stringify(initial), { status: 200, headers: { "content-type": "application/json" } }))));
    vi.stubGlobal("matchMedia", vi.fn().mockReturnValue({ matches: false, addEventListener: vi.fn(), removeEventListener: vi.fn() }));
  });

  afterEach(() => {
    cleanup();
    document.documentElement.removeAttribute("data-theme");
    document.documentElement.removeAttribute("data-theme-preference");
    localStorage.clear();
    vi.unstubAllGlobals();
  });

  it("matches the prototype modal shell and exposes ten focused sections", () => {
    const { onClose } = renderSettings();
    const dialog = screen.getByRole("dialog", { name: "Settings" });
    expect(within(dialog).getByRole("navigation", { name: "Settings" }).querySelectorAll("button")).toHaveLength(10);
    expect(within(dialog).getByRole("heading", { name: "Profile" })).toBeInTheDocument();
    expect(within(dialog).queryByRole("heading", { name: "Appearance" })).not.toBeInTheDocument();
    fireEvent.click(within(dialog).getByRole("button", { name: "Close settings" }));
    expect(onClose).toHaveBeenCalledOnce();
  });

  it("recovers automatically when one settings request fails transiently", async () => {
    let preferenceAttempts = 0;
    vi.mocked(fetch).mockImplementation((input: RequestInfo | URL) => {
      const url = String(input);
      if (url === "/api/workspace/preferences") {
        preferenceAttempts += 1;
        return Promise.resolve(
          preferenceAttempts === 1
            ? Response.json({ message: "Settings are temporarily unavailable." }, { status: 502 })
            : Response.json(initial),
        );
      }
      if (url === "/api/workspace") return Promise.resolve(Response.json(workspace));
      return Promise.resolve(Response.json({ message: "Not found" }, { status: 404 }));
    });

    render(
      <WorkspaceSettingsDialog
        displayName="Taimoor"
        onClose={vi.fn()}
        open
      />,
    );

    expect(await screen.findByRole("heading", { name: "Profile" })).toBeInTheDocument();
    expect(preferenceAttempts).toBe(2);
    expect(screen.queryByText("Settings could not be loaded.")).not.toBeInTheDocument();
  });

  it("persists appearance choices and the local theme survives server lag", async () => {
    localStorage.setItem("oslo-theme", "light");
    renderSettings("appearance");
    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("light"));
    expect(screen.getByRole("button", { name: "Light" })).toHaveAttribute("aria-pressed", "true");
    fireEvent.click(screen.getByRole("button", { name: "Dark" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/workspace/preferences", expect.objectContaining({ method: "PUT", body: expect.stringContaining('"theme":"dark"'), keepalive: true })));
    expect(document.documentElement.dataset.theme).toBe("dark");
    expect(screen.getByText("Saved")).toBeInTheDocument();
  });

  it("persists notification preferences without starting analysis", async () => {
    renderSettings("notifications");
    fireEvent.click(screen.getByRole("switch", { name: "Mentions" }));
    fireEvent.click(screen.getByRole("switch", { name: "Analysis complete" }));
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith("/api/workspace/preferences", expect.objectContaining({ body: expect.stringContaining('"mentions_notifications":false') }));
      expect(fetch).toHaveBeenCalledWith("/api/workspace/preferences", expect.objectContaining({ body: expect.stringContaining('"analysis_notifications":false') }));
    });
  });

  it("persists profile role and workspace identity", async () => {
    renderSettings();
    fireEvent.click(screen.getByRole("button", { name: /I own the outcome/ }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/workspace/preferences", expect.objectContaining({ body: expect.stringContaining('"role_title":"I own the outcome"') })));
    fireEvent.click(screen.getByRole("button", { name: "Workspace" }));
    const workspaceName = screen.getByRole("textbox", { name: "Workspace name" });
    fireEvent.change(workspaceName, { target: { value: "OSLO Studio" } });
    fireEvent.blur(workspaceName);
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/workspace/preferences", expect.objectContaining({ body: expect.stringContaining('"workspace_name":"OSLO Studio"') })));
  });

  it("keeps access, membership, plan, billing and integrations honest", () => {
    renderSettings("access");
    expect(screen.getByRole("heading", { name: "Access & invites" })).toBeInTheDocument();
    expect(screen.getByText("GA")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Manage invitations/ })).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /Manage invitations/ })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /Membership/ }));
    expect(screen.getByText("2 members")).toBeInTheDocument();
    expect(screen.getByText("2 active")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Manage access & invitations/ }));
    expect(screen.getByRole("heading", { name: "Access & invites" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Plan & usage" }));
    expect(screen.getByText("1 in your workspace · 1 active")).toBeInTheDocument();
    expect(screen.getByText("Generous — fair-use")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Compare Free vs Basic" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Compare Free vs Basic" }));
    expect(screen.getByRole("dialog", { name: "Your plan" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Close plans" }));
    expect(screen.getByRole("dialog", { name: "Settings" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Billing" }));
    expect(screen.getByText("$29 / month · $290 / year")).toBeInTheDocument();
    expect(screen.getByText("Flat · never per seat")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /Integrations/ }));
    expect(screen.getByText("Arrives after this release")).toBeInTheDocument();
  });

  it("manages workspace invitations inside Settings without leaving the project", async () => {
    const invitations = [{
      id: "invite-1",
      email: "pending@example.com",
      role: "owner",
      status: "pending",
      expires_at: "2026-08-30T00:00:00Z",
    }];
    vi.mocked(fetch).mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url === "/api/workspace/invitations" && !init?.method) {
        return Promise.resolve(Response.json(invitations));
      }
      if (url === "/api/workspace/invitations" && init?.method === "POST") {
        const body = JSON.parse(String(init.body)) as { action: string; email?: string };
        if (body.action === "invite") {
          return Promise.resolve(Response.json({
            id: "invite-2",
            email: body.email,
            role: "owner",
            status: "pending",
            expires_at: "2026-08-30T00:00:00Z",
          }, { status: 201 }));
        }
        return Promise.resolve(new Response(null, { status: 204 }));
      }
      return Promise.resolve(Response.json(initial));
    });

    renderSettings("access");
    fireEvent.click(screen.getByRole("button", { name: /Manage invitations/ }));
    expect(await screen.findByRole("heading", { name: "Workspace invitations" })).toBeInTheDocument();
    expect(screen.getByText("pending@example.com")).toBeInTheDocument();

    fireEvent.change(screen.getByRole("textbox", { name: "Invitation email" }), {
      target: { value: "new.member@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send invitation" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(
      "/api/workspace/invitations",
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining('"action":"invite"'),
      }),
    ));
    expect(await screen.findByText("Invitation sent to new.member@example.com.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Revoke pending@example.com" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(
      "/api/workspace/invitations",
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining('"action":"revoke"'),
      }),
    ));
    expect(screen.queryByText("pending@example.com")).not.toBeInTheDocument();
  });

  it("shows a Delegate-PM only personal settings", () => {
    render(
      <WorkspaceSettings
        displayName="Amina"
        email="amina@example.com"
        initial={{ ...initial, actor_role: "delegate_pm" as const }}
        initialSection="profile"
        modal
        onClose={vi.fn()}
        workspace={{
          ...workspace,
          role: "delegate_pm" as const,
          can_manage_plan: false,
          projects: [workspace.projects[0]],
        }}
        workspaceName="OSLO Alpha"
      />,
    );

    const navigation = screen.getByRole("navigation", { name: "Settings" });
    expect(navigation.querySelectorAll("button")).toHaveLength(3);
    expect(within(navigation).getByRole("button", { name: "Profile" })).toBeInTheDocument();
    expect(within(navigation).getByRole("button", { name: "Appearance" })).toBeInTheDocument();
    expect(within(navigation).getByRole("button", { name: "Notifications" })).toBeInTheDocument();
    expect(within(navigation).queryByRole("button", { name: "Workspace" }))
      .not.toBeInTheDocument();
    expect(within(navigation).queryByRole("button", { name: "Access & invites" }))
      .not.toBeInTheDocument();
    expect(within(navigation).queryByRole("button", { name: "Plan & usage" }))
      .not.toBeInTheDocument();
  });
});

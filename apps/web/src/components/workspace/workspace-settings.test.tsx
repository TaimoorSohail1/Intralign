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

    expect(screen.getByRole("navigation", { name: "Settings" }).querySelectorAll("a")).toHaveLength(11);
    expect(screen.getByRole("heading", { name: "Account & workspace" })).toBeInTheDocument();
    expect(screen.getByRole("searchbox", { name: "Search settings" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Light" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/workspace/preferences",
        expect.objectContaining({
          method: "PUT",
          body: expect.stringContaining('"theme":"light"'),
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
    expect(screen.getByRole("button", { name: "See plans" })).toBeInTheDocument();

    fireEvent.change(screen.getByRole("searchbox", { name: "Search settings" }), {
      target: { value: "notifications" },
    });

    expect(screen.getByRole("heading", { name: "Notifications" })).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Profile" })).not.toBeInTheDocument();
  });

  it("persists profile fields and renders the backend membership role", async () => {
    render(
      <WorkspaceSettings
        displayName="Taimoor"
        initial={{ ...initial, actor_role: "collaborator" }}
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
    expect(screen.getByText("Collaborator")).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Manage invitations" })).not.toBeInTheDocument();
  });
});

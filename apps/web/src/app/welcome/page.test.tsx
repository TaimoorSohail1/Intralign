import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const redirect = vi.fn((path: string) => {
  throw new Error(`REDIRECT:${path}`);
});
const getWorkspace = vi.fn();
const readSession = vi.fn();

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ readSession }));
vi.mock("@/lib/server/oslo-api", () => ({ getWorkspace }));
vi.mock("@/components/layout/entry-shell", () => ({
  EntryShell: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe("WelcomePage", () => {
  it("keeps returning users in Workspace Home instead of offering a second first project", async () => {
    readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
      displayName: "Taimoor",
    });
    getWorkspace.mockResolvedValue({
      projects: [{ id: "project-1", archived: false }],
    });
    const { default: WelcomePage } = await import("./page");

    await expect(WelcomePage()).rejects.toThrow("REDIRECT:/workspace");
    expect(redirect).toHaveBeenCalledWith("/workspace");
  });

  it("shows onboarding when no active project exists", async () => {
    readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
      displayName: "Taimoor",
    });
    getWorkspace.mockResolvedValue({ projects: [] });
    const { default: WelcomePage } = await import("./page");

    render(await WelcomePage());

    expect(document.body).toHaveTextContent("Welcome to OSLO, Taimoor.");
    expect(document.body).toHaveTextContent("Start your first project");
  });
});

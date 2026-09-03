import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const redirect = vi.fn((path: string) => {
  throw new Error(`REDIRECT:${path}`);
});
const readSession = vi.fn();

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ readSession }));
vi.mock("@/lib/server/oslo-api", () => ({ createProject: vi.fn() }));
vi.mock("@/components/layout/entry-shell", () => ({
  EntryShell: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

describe("WelcomePage", () => {
  it("shows onboarding for a newly invited member even when another workspace member has a project", async () => {
    readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
      displayName: "Taimoor",
    });
    const { default: WelcomePage } = await import("./page");

    render(await WelcomePage());

    expect(document.body).toHaveTextContent("Welcome to Intralign, Taimoor.");
    expect(document.body).toHaveTextContent("Outcome-driven Strategic Lifecycle Orchestration");
    expect(document.body).toHaveTextContent("Start your first outcome");
  });
});

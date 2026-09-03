import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  getWorkspace: vi.fn(),
  readSession: vi.fn(),
  redirect: vi.fn((location: string) => {
    throw new Error(`redirect:${location}`);
  }),
  workspaceHome: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect: mocks.redirect }));
vi.mock("@/components/workspace/workspace-home", () => ({
  WorkspaceHome: mocks.workspaceHome,
}));
vi.mock("@/lib/server/oslo-api", () => ({ getWorkspace: mocks.getWorkspace }));
vi.mock("@/lib/server/session", () => ({ readSession: mocks.readSession }));

import WorkspacePage from "./page";

describe("WorkspacePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns platform administrators to their dedicated invitation workspace", async () => {
    mocks.readSession.mockResolvedValue({
      accessToken: "admin-access-token",
      workspaceId: "admin-workspace",
      accountRole: "admin",
      displayName: "OSLO Admin",
    });

    await expect(
      WorkspacePage({ searchParams: Promise.resolve({}) }),
    ).rejects.toThrow("redirect:/admin/invitations");

    expect(mocks.getWorkspace).not.toHaveBeenCalled();
  });

  it("loads the workspace for an owner", async () => {
    mocks.readSession.mockResolvedValue({
      accessToken: "owner-access-token",
      workspaceId: "owner-workspace",
      accountRole: "owner",
      displayName: "Owner",
    });
    mocks.getWorkspace.mockResolvedValue({ id: "owner-workspace" });
    mocks.workspaceHome.mockReturnValue(null);

    await WorkspacePage({ searchParams: Promise.resolve({}) });

    expect(mocks.getWorkspace).toHaveBeenCalledWith({
      accessToken: "owner-access-token",
      workspaceId: "owner-workspace",
    });
  });
});

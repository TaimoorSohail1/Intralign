import { beforeEach, describe, expect, it, vi } from "vitest";

const { completeWelcome, readSession, redirect, startProject } = vi.hoisted(() => ({
  completeWelcome: vi.fn(),
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
  readSession: vi.fn(),
  startProject: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ readSession }));
vi.mock("@/lib/server/oslo-api", () => ({
  OsloApiError: class OsloApiError extends Error {
    constructor(
      message: string,
      readonly status: number,
      readonly detail: unknown,
    ) {
      super(message);
    }
  },
  completeWelcome,
  startProject,
}));

describe("startFirstProject", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
    });
  });

  it("routes a newly created project to intake", async () => {
    startProject.mockResolvedValue({ id: "project-new" });
    const { startFirstProject } = await import("./actions");

    await expect(startFirstProject()).rejects.toThrow(
      "REDIRECT:/intake?project=project-new",
    );
  });

  it("completes onboarding and opens the workspace when its project limit is full", async () => {
    const { OsloApiError } = await import("@/lib/server/oslo-api");
    startProject.mockRejectedValue(
      new OsloApiError("Project limit reached", 422, {
        code: "CAPACITY_COMMITMENT_REQUIRED",
      }),
    );
    const { startFirstProject } = await import("./actions");

    await expect(startFirstProject()).rejects.toThrow("REDIRECT:/workspace");
    expect(completeWelcome).toHaveBeenCalledWith({
      accessToken: "access-token",
      workspaceId: "workspace-1",
    });
  });
});

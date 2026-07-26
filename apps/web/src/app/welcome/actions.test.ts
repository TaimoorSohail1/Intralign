import { beforeEach, describe, expect, it, vi } from "vitest";

const { OsloApiError, readSession, redirect, startProject } = vi.hoisted(() => ({
  OsloApiError: class OsloApiError extends Error {
    constructor(
      message: string,
      readonly status: number,
      readonly detail: unknown,
    ) {
      super(message);
    }
  },
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
  readSession: vi.fn(),
  startProject: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ readSession }));
vi.mock("@/lib/server/oslo-api", () => ({ OsloApiError, startProject }));

describe("startFirstProject", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
    });
  });

  it("routes a full workspace to the governed archive-or-upgrade choice", async () => {
    startProject.mockRejectedValue(
      new OsloApiError("Active project limit reached", 409, {
        code: "PROJECT_LIMIT_REACHED",
      }),
    );
    const { startFirstProject } = await import("./actions");

    await expect(startFirstProject()).rejects.toThrow(
      "REDIRECT:/workspace?new=1",
    );
  });

  it("routes a newly created project to intake", async () => {
    startProject.mockResolvedValue({ id: "project-new" });
    const { startFirstProject } = await import("./actions");

    await expect(startFirstProject()).rejects.toThrow(
      "REDIRECT:/intake?project=project-new",
    );
  });
});

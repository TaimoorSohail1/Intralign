import { beforeEach, describe, expect, it, vi } from "vitest";

const { readSession, redirect, startProject } = vi.hoisted(() => ({
  redirect: vi.fn((path: string) => {
    throw new Error(`REDIRECT:${path}`);
  }),
  readSession: vi.fn(),
  startProject: vi.fn(),
}));

vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/lib/server/session", () => ({ readSession }));
vi.mock("@/lib/server/oslo-api", () => ({ startProject }));

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
});

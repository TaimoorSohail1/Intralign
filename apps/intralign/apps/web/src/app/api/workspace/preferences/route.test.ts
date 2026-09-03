import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => {
  class TestOsloApiError extends Error {
    constructor(
      message: string,
      readonly status: number,
      readonly detail: unknown,
    ) {
      super(message);
    }
  }
  return {
    getWorkspacePreferences: vi.fn(),
    readSession: vi.fn(),
    TestOsloApiError,
  };
});

vi.mock("@/lib/server/oslo-api", () => ({
  getWorkspacePreferences: mocks.getWorkspacePreferences,
  OsloApiError: mocks.TestOsloApiError,
  updateWorkspacePreferences: vi.fn(),
}));

vi.mock("@/lib/server/session", () => ({ readSession: mocks.readSession }));

import { GET } from "./route";

describe("workspace preferences route", () => {
  beforeEach(() => {
    mocks.getWorkspacePreferences.mockReset();
    mocks.readSession.mockReset();
    mocks.readSession.mockResolvedValue({
      accessToken: "access-token",
      workspaceId: "workspace-1",
    });
  });

  it("preserves transient API statuses so the settings dialog can retry", async () => {
    mocks.getWorkspacePreferences.mockRejectedValue(
      new mocks.TestOsloApiError("OSLO API request failed", 503, null),
    );

    const response = await GET();

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({
      message: "Settings are temporarily unavailable.",
    });
  });

  it("maps unexpected server failures to a retryable gateway error", async () => {
    mocks.getWorkspacePreferences.mockRejectedValue(new Error("connection reset"));

    const response = await GET();

    expect(response.status).toBe(502);
  });
});

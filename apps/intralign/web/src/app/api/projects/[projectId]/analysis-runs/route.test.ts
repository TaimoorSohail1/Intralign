import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  after: vi.fn(),
  executeAnalysis: vi.fn(),
  readSession: vi.fn(),
  startAnalysis: vi.fn(),
}));

vi.mock("next/server", () => ({ after: mocks.after }));
vi.mock("@/lib/server/oslo-api", () => ({
  executeAnalysis: mocks.executeAnalysis,
  startAnalysis: mocks.startAnalysis,
}));
vi.mock("@/lib/server/session", () => ({ readSession: mocks.readSession }));

import { maxDuration, POST } from "./route";

describe("analysis start proxy route", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.readSession.mockResolvedValue({ accessToken: "access-token" });
    mocks.startAnalysis.mockResolvedValue({
      run_id: "run-1",
      project_id: "project-1",
      kind: "initial",
      status: "queued",
    });
  });

  it("returns the queued run before deferred analysis execution begins", async () => {
    let deferredWork: (() => Promise<void>) | undefined;
    mocks.after.mockImplementation((callback: () => Promise<void>) => {
      deferredWork = callback;
    });

    const response = await POST(
      new Request("http://localhost/api/projects/project-1/analysis-runs", {
        method: "POST",
        body: JSON.stringify({ description: "Plan", sourceNames: [], sourceDocumentIds: [] }),
      }),
      { params: Promise.resolve({ projectId: "project-1" }) },
    );

    expect(response.status).toBe(202);
    expect(mocks.startAnalysis).toHaveBeenCalledWith(
      expect.objectContaining({ deferExecution: true }),
    );
    expect(mocks.executeAnalysis).not.toHaveBeenCalled();
    expect(deferredWork).toBeTypeOf("function");

    await deferredWork?.();

    expect(mocks.executeAnalysis).toHaveBeenCalledWith({
      accessToken: "access-token",
      runId: "run-1",
    });
  });

  it("allows the complete deferred production runtime budget", () => {
    expect(maxDuration).toBe(800);
  });
});

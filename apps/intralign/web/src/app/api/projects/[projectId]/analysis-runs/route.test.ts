import { describe, expect, it, vi } from "vitest";

vi.mock("@/lib/server/oslo-api", () => ({ startAnalysis: vi.fn() }));
vi.mock("@/lib/server/session", () => ({ readSession: vi.fn() }));

import { maxDuration } from "./route";

describe("analysis start proxy route", () => {
  it("allows the complete production analysis runtime budget", () => {
    expect(maxDuration).toBe(800);
  });
});

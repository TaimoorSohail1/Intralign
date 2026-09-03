import { describe, it, expect } from "vitest";
import { resolveBand } from "./confidenceBand";

// CONTEXT.md / deep-task-0019: bands are 0–49 low / 50–74 medium / 75–100 high,
// with a ±3 CONSERVATIVE edge guard that rounds to the LOWER band. A value that
// sits just *above* a band boundary (50 or 75) by 1–2 points is pulled down into
// the lower band; the boundary value itself (50, 75) keeps the higher band.
//
// The locked boundary cases from the task:
//   48 -> low   (already low; near boundary, stays low)
//   52 -> low   (medium base, within guard above 50 -> drop to low)
//   74 -> medium (medium base, no boundary above it)
//   75 -> high   (boundary value keeps the higher band)
//   77 -> medium (high base, within guard above 75 -> drop to medium)
describe("resolveBand — ±3 conservative edge guard (round to lower band)", () => {
  it("maps the natural low range", () => {
    expect(resolveBand(0)).toBe("low");
    expect(resolveBand(40)).toBe("low");
    expect(resolveBand(49)).toBe("low");
  });

  it("48 reads low (the conservative edge guard, never medium)", () => {
    expect(resolveBand(48)).toBe("low");
  });

  it("50 reads medium — the boundary value keeps the higher band (symmetric with 75)", () => {
    expect(resolveBand(50)).toBe("medium");
  });

  it("52 reads low — within the guard just above the 50 boundary, drops to lower band", () => {
    expect(resolveBand(51)).toBe("low");
    expect(resolveBand(52)).toBe("low");
  });

  it("clears the guard above 50 by point 53 -> medium", () => {
    expect(resolveBand(53)).toBe("medium");
    expect(resolveBand(60)).toBe("medium");
  });

  it("74 reads medium", () => {
    expect(resolveBand(74)).toBe("medium");
  });

  it("75 reads high — the boundary value keeps the higher band", () => {
    expect(resolveBand(75)).toBe("high");
  });

  it("77 reads medium — within the guard just above the 75 boundary, drops to lower band", () => {
    expect(resolveBand(76)).toBe("medium");
    expect(resolveBand(77)).toBe("medium");
  });

  it("clears the guard above 75 by point 78 -> high", () => {
    expect(resolveBand(78)).toBe("high");
    expect(resolveBand(100)).toBe("high");
  });

  it("clamps out-of-range values conservatively", () => {
    expect(resolveBand(-5)).toBe("low");
    expect(resolveBand(150)).toBe("high");
  });
});

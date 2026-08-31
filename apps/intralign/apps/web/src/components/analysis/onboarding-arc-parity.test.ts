import { readFile } from "node:fs/promises";
import path from "node:path";

import { describe, expect, it } from "vitest";

const prototypePath = path.join(
  process.cwd(),
  "src",
  "test",
  "fixtures",
  "onboarding-arc-prototype.html",
);
const shippedPath = path.join(process.cwd(), "public", "r2", "onboarding-arc.html");

function between(source: string, start: string, end: string) {
  const startIndex = source.indexOf(start);
  const endIndex = source.indexOf(end, startIndex);
  expect(startIndex).toBeGreaterThanOrEqual(0);
  expect(endIndex).toBeGreaterThan(startIndex);
  return source.slice(startIndex, endIndex).replaceAll("\r\n", "\n");
}

describe("R2 onboarding arc prototype parity", () => {
  it("ships the prototype kinetic graph engine unchanged", async () => {
    const [prototype, shipped] = await Promise.all([
      readFile(prototypePath, "utf8"),
      readFile(shippedPath, "utf8"),
    ]);

    expect(
      between(shipped, "function buildGraph(){", "function addNode"),
    ).toBe(between(prototype, "function buildGraph(){", "function addNode"));
    expect(
      between(shipped, "function loop(now){", "var raf=requestAnimationFrame(loop)"),
    ).toBe(between(prototype, "function loop(now){", "var raf=requestAnimationFrame(loop)"));
  });

  it("retains every visible Slice 3 narration and decision state from the prototype", async () => {
    const shipped = await readFile(shippedPath, "utf8");
    [
      "Drafting your plan documents…",
      "Every project begins with an <b>outcome</b>.",
      "AI drafts a plan in seconds.",
      "A plan isn’t the outcome.",
      "<b>Grounded</b>? Evidence visible?",
      "Confirm your outcome",
      "✓ Yes — this is my outcome",
      "Close — I’ll refine it",
      "Not sure yet — keep it as OSLO’s inference →",
    ].forEach((copy) => expect(shipped).toContain(copy));
  });

  it("adds only production adapters for live progress, outcome persistence, embedding, and reduced motion", async () => {
    const shipped = await readFile(shippedPath, "utf8");
    expect(shipped).toContain("OARC_LIVE");
    expect(shipped).toContain("event.origin!==window.location.origin");
    expect(shipped).toContain("{oarc:'decision'");
    expect(shipped).toContain("d.oarc==='decision-result'");
    expect(shipped).toContain("html.embed .dev{display:none!important}");
    expect(shipped).toContain("oarcHandoff('confirm', OARC_OUTCOME)");
    expect(shipped).toContain("if(typeof OARC_FRAME_SYNC!=='undefined') OARC_FRAME_SYNC=''");
    expect(shipped).toContain("prefers-reduced-motion:reduce");
  });

  it("retains prototype playback controls while hiding them in the embedded production flow", async () => {
    const shipped = await readFile(shippedPath, "utf8");
    expect(shipped).toContain("OARC_MODE");
    expect(shipped).not.toContain("html.embed .modebtn{display:none!important}");
    expect(shipped).toContain("html.embed .dev{display:none!important}");
    expect(shipped).toContain("setEntry('first')");
    expect(shipped).toContain("setEntry('return')");
    expect(shipped).toContain("setPass(60000)");
    expect(shipped).toContain("setPass(15000)");
    expect(shipped).toContain("toggleGates()");
    expect(shipped).toContain("cls('d-first','act',entry==='first')");
    expect(shipped).toContain("cls('d-ret','act',entry==='return')");
    expect(shipped).toContain("onclick=\"restart()\"");
    expect(shipped).toContain("'Skip the intro →':'↺ Replay intro'");
  });

  it("hands a guided user to the explicit outcome decision instead of auto-confirming it", async () => {
    const shipped = await readFile(shippedPath, "utf8");
    const toggleMode = between(shipped, "function toggleMode(){", "function restart(){");

    expect(toggleMode).toContain("mode==='guided'");
    expect(toggleMode).toContain("OARC_EMBED");
    expect(toggleMode).toContain("handOff()");
    expect(toggleMode.indexOf("handOff()")).toBeLessThan(
      toggleMode.indexOf("mode=(mode==='guided')?'watch':'guided'"),
    );
  });
});

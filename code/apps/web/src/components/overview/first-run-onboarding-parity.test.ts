import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const styles = readFileSync(resolve(process.cwd(), "src/app/globals.css"), "utf8");

describe("R2 first-run onboarding prototype parity", () => {
  it("aligns the focused guidance with the left edge of the 820px issue queue", () => {
    expect(styles).toMatch(
      /\.is-r2-slice-one \.r2-first-run-focus-copy,[^{]*\.is-r2-slice-one \.project-main > \.r2-first-run-guide\s*\{[^}]*width:\s*min\(820px,\s*100%\)[^}]*margin-left:\s*max\(0px,\s*calc\(\(100%\s*-\s*900px\)\s*\/\s*2\)\)[^}]*margin-right:\s*auto/s,
    );
    expect(styles).toMatch(/\.is-r2-slice-one \.issue-list\s*\{[^}]*max-width:\s*820px/s);
  });
});

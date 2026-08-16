import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const styles = readFileSync(resolve(process.cwd(), "src/app/globals.css"), "utf8");

describe("R2 first-run onboarding prototype parity", () => {
  it("keeps the focused guidance aligned to the prototype's 820px read width", () => {
    expect(styles).toMatch(
      /\.is-r2-slice-one \.r2-first-run-focus-copy\s*\{[^}]*width:\s*min\(820px,\s*100%\)[^}]*margin-inline:\s*auto/s,
    );
  });
});

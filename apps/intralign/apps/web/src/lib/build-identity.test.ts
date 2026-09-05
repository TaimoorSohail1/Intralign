import { afterEach, describe, expect, it } from "vitest";

import { buildIdentity, shortBuildIdentity } from "./build-identity";

const VARIABLES = [
  "NEXT_PUBLIC_BUILD_SHA",
  "VERCEL_GIT_COMMIT_SHA",
  "HEROKU_SLUG_COMMIT",
  "SOURCE_VERSION",
] as const;

function clearAll() {
  for (const variable of VARIABLES) {
    delete process.env[variable];
  }
}

afterEach(clearAll);

describe("build identity (N-5)", () => {
  it.each(VARIABLES)("reads the commit from %s", (variable) => {
    clearAll();
    process.env[variable] = "0123456789abcdef";

    expect(buildIdentity()).toBe("0123456789abcdef");
  });

  it("reads unknown rather than guessing when nothing stamped the build", () => {
    clearAll();

    expect(buildIdentity()).toBe("unknown");
    expect(shortBuildIdentity()).toBe("unknown");
  });

  it("does not treat a blank platform variable as a build", () => {
    clearAll();
    process.env.VERCEL_GIT_COMMIT_SHA = "   ";

    expect(buildIdentity()).toBe("unknown");
  });

  it("shows the reader a short commit", () => {
    clearAll();
    process.env.NEXT_PUBLIC_BUILD_SHA = "0123456789abcdef";

    expect(shortBuildIdentity()).toBe("0123456");
  });
});

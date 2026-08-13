import { execFileSync } from "node:child_process";
import path from "node:path";
import { expect, test as base } from "@playwright/test";

function resetE2EFixtures() {
  // Every browser test mutates the shared synthetic workspace, so rebuild the
  // fixture before each test instead of leaking state between slices/devices.
  const repositoryRoot = path.resolve(__dirname, "../..");
  const packageManagerScript = process.env.npm_execpath;
  if (packageManagerScript) {
    execFileSync(process.execPath, [packageManagerScript, "seed:e2e"], {
      cwd: repositoryRoot,
      stdio: "inherit",
    });
    return;
  }
  if (process.platform === "win32") {
    execFileSync(process.env.ComSpec ?? "cmd.exe", ["/d", "/s", "/c", "pnpm.cmd seed:e2e"], {
      cwd: repositoryRoot,
      stdio: "inherit",
    });
    return;
  }
  execFileSync("pnpm", ["seed:e2e"], { cwd: repositoryRoot, stdio: "inherit" });
}

export const test = base.extend<{ resetE2EFixtures: void }>({
  resetE2EFixtures: [
    async ({}, use) => {
      resetE2EFixtures();
      await use();
    },
    { auto: true },
  ],
});

export { expect };

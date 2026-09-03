import { execFileSync } from "node:child_process";
import path from "node:path";

export default function globalSetup() {
  const repositoryRoot = path.resolve(__dirname, "../..");
  const packageManager = process.env.npm_execpath;
  if (!packageManager) throw new Error("Playwright needs npm_execpath to reset E2E fixtures.");
  execFileSync(process.execPath, [packageManager, "seed:e2e"], {
    cwd: repositoryRoot,
    stdio: "inherit",
  });
}

import { defineConfig, devices } from "@playwright/test";

// E2E smoke (DTM-0019): boots the Vite dev server and asserts the shell renders +
// a placeholder route resolves. Evergreen target = Chromium. Component/unit tests
// run under Vitest (see vitest.config.ts); Playwright owns only e2e/.
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: {
    baseURL: "http://localhost:5173",
    trace: "on-first-retry",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});

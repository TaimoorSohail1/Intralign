import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// Component/unit tests (DTM-0019). jsdom env + Testing Library. Playwright E2E is
// kept separate (see playwright.config.ts) and excluded here so the two runners
// never collide.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": "/src" },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.test.{ts,tsx}"],
    exclude: ["e2e/**", "node_modules/**"],
  },
});

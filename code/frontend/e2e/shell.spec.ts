import { test, expect } from "@playwright/test";

// DTM-0019 smoke: the app shell renders and a placeholder route resolves.
test("app shell renders with the primary nav", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("app-shell")).toBeVisible();
  // The wordmark + the primary nav rail (UI spec §2 IA).
  await expect(page.getByRole("heading", { name: "OSLO" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
  // The default (Projects) placeholder surface resolves.
  await expect(page.getByTestId("surface-title")).toHaveText("Projects");
});

test("a placeholder route resolves on navigation", async ({ page }) => {
  await page.goto("/notifications");
  await expect(page.getByTestId("surface-title")).toHaveText("Notification Center");
});

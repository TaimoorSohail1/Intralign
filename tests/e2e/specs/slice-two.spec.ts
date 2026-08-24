import { expect, test } from "@playwright/test";
import { dismissOrientation } from "../support/orientation";

test.setTimeout(180_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/admin\/invitations/);
}

test("Slice 2 survives refresh and publishes exactly seven artifacts", async ({ page }) => {
  await signIn(page);
  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first project/ }).click();
  await expect(page).toHaveURL(/\/intake\?project=/);

  await page.getByRole("button", { name: /sample project/i }).click();
  await expect(page.getByRole("button", { name: /See where I stand/ })).toBeEnabled();
  await page.getByRole("button", { name: /See where I stand/ }).click();
  await expect(page).toHaveURL(/\/projects\/.+\/(analysis\/.+|overview)/);

  if (page.url().includes("/analysis/")) {
    await page.reload();
    await expect(page.getByText(/Analyzing|Your progress is safe/).first()).toBeVisible();
  }
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
  await expect(page.locator(".confidence-read")).toBeVisible();

  await dismissOrientation(page);

  await expect(page.getByText(/provisional|current/).first()).toBeVisible();
  await expect(
    page
      .getByRole("complementary", { name: "Project navigation" })
      .locator('a[href*="/artifacts/"]'),
  ).toHaveCount(7);
  await expect(page.locator(".project-advisory")).toContainText("OSLO advises; you decide");
  await expect(page.getByRole("dialog", { name: "Issue details" })).toHaveCount(0);

  const hideAdvisor = page.getByRole("button", { name: "Hide the OSLO panel" });
  if (await hideAdvisor.isVisible()) {
    await hideAdvisor.click();
  }
  const issueRows = page.locator(".issue-row");
  await expect(issueRows).not.toHaveCount(0);
  await issueRows.first().click();
  await expect(page.getByRole("dialog", { name: "Issue details" })).toBeVisible();
  await page.getByRole("button", { name: "Close issue" }).click();
  await expect(page.getByRole("dialog", { name: "Issue details" })).toHaveCount(0);
});

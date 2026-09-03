import { expect, test } from "../fixtures";
import { unlockFirstRead } from "../helpers";

test.setTimeout(240_000);

async function dismissOrientation(page: import("@playwright/test").Page) {
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (!(await orientation.isVisible())) return;
  await orientation.getByRole("button", { name: "Skip", exact: true }).click();
  await expect(orientation).toBeHidden();
}

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

async function openFirstProject(page: import("@playwright/test").Page) {
  await page.goto("/workspace");
  const analyzedProject = page.getByRole("link", { name: /Open (?:the )?project/i }).last();
  if (await analyzedProject.count()) {
    await analyzedProject.click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/);
    await unlockFirstRead(page);
    await expect(page.getByRole("group", { name: "Project sharing and export" })).toBeVisible();
    return;
  }
  await page.getByRole("button", { name: "New project", exact: true }).click();
  await expect(page).toHaveURL(/\/intake\?project=/);
  await page.getByRole("button", { name: /sample (?:project|plan)/i }).click();
  await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
  await page.waitForURL(/\/projects\/[^/]+\/(?:analysis\/[^/]+|overview)/, { timeout: 120_000 });
  if (page.url().includes("/analysis/")) {
    const skipIntro = page.getByRole("button", { name: /Skip the intro/i });
    await skipIntro.waitFor({ state: "visible", timeout: 10_000 }).catch(() => undefined);
    if (await skipIntro.isVisible()) await skipIntro.click();
    const confirmOutcome = page
      .frameLocator('iframe[title="OSLO analysis and outcome confirmation"]')
      .getByRole("button", { name: /Yes.+this is my outcome/i });
    await expect(confirmOutcome).toBeVisible({ timeout: 120_000 });
    await confirmOutcome.click();
  }
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
  await unlockFirstRead(page);
  await expect(page.getByRole("group", { name: "Project sharing and export" })).toBeVisible();
}

test("Reports export and collaboration share a retained snapshot", async ({
  browser,
  page,
}) => {
  await signIn(page);
  await openFirstProject(page);

  await dismissOrientation(page);

  const projectId = new URL(page.url()).pathname.split("/")[2];
  await page.goto(`/projects/${projectId}/reports`);
  await expect(page.getByRole("heading", { name: "Reports" })).toBeVisible();
  await page.getByRole("tab", { name: /Generated Outcome Readiness/ }).click();
  await page.getByRole("button", { name: "Export this report" }).click();
  await expect(page.getByRole("status")).toContainText("TEXT export downloaded");

  const collaboration = page.getByRole("group", {
    name: "Project sharing and export",
  });
  await expect(collaboration.getByRole("button", { name: "Share" })).toBeVisible();

  await collaboration.getByRole("button", { name: "Share" }).click();
  const dialog = page.getByRole("dialog", { name: /^Share / });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByText("People on this project", { exact: true })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "External review request" })).toBeVisible();

  await dialog.getByLabel("Snapshot recipient name").fill("E2E executive sponsor");
  await dialog.getByRole("button", { name: "Create a view-only link" }).click();
  await expect(dialog.locator(".collaboration-success")).toContainText(
    "A view-only snapshot is ready to share.",
  );
  const snapshotUrl = await dialog.locator(".collaboration-created-link code").textContent();
  expect(snapshotUrl).toMatch(/\/share\/[^/]+$/);

  const publicContext = await browser.newContext();
  const publicPage = await publicContext.newPage();
  await publicPage.goto(snapshotUrl!);
  await expect(publicPage.getByText("Read-only project snapshot")).toBeVisible();
  await expect(publicPage.getByText("Shared with E2E executive sponsor")).toBeVisible();
  await expect(publicPage.getByText(/Read only/)).toBeVisible();
  await expect(publicPage.locator(".public-snapshot-grid article")).toHaveCount(7);
  await publicContext.close();
  await dialog.getByRole("button", { name: "Done" }).evaluate((button) => button.click());
  await expect(dialog).toBeHidden();
});

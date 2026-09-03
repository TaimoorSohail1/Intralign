import { expect, test } from "../fixtures";
import { unlockFirstRead } from "../helpers";

test.setTimeout(240_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

async function createAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");
  const analyzedProject = page.getByRole("link", { name: /Open (?:the )?project/i }).first();
  if (await analyzedProject.count()) {
    await analyzedProject.click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/);
    await unlockFirstRead(page);
    await expect(page.getByRole("group", { name: "Project sharing and export" })).toBeVisible();
    return;
  }
  await page.goto("/welcome");
  await page
    .getByRole("button", { name: /Start your first (?:outcome|project)/ })
    .click();
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

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
    await expect(orientation).toBeHidden();
  }
  await expect(page.getByRole("group", { name: "Project sharing and export" })).toBeVisible();
}

test("Slice 7 retains read-only history, snapshots, and category filters", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  if (!projectId) throw new Error(`Could not read a project id from ${page.url()}`);
  const historyLink = page.getByRole("link", { name: /^History/ });
  if (await historyLink.isVisible()) {
    await historyLink.click();
  } else {
    await page.goto(`/projects/${projectId}/history`);
  }
  await expect(page).toHaveURL(/\/history$/);
  await expect(page.getByRole("heading", { name: "History", exact: true })).toBeVisible();
  const timeline = page.locator(".history-runs");
  await expect(timeline.getByText("Extended Analysis complete").first()).toBeVisible({
    timeout: 120_000,
  });
  await expect(timeline.getByText("Initial Analysis complete").first()).toBeVisible();
  await expect(page.getByText(/Read-only · viewing history changes nothing/)).toBeVisible();

  const retainedVersion = page.getByText(/plan-artifact versions retained/).first();
  await expect(retainedVersion).toBeVisible();
  await page.getByRole("button", { name: /View snapshot/ }).first().click();
  const snapshot = page.getByRole("dialog", { name: "Historical snapshot" });
  await expect(snapshot).toBeVisible();
  await expect(snapshot.getByText("Read-only retained state")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(snapshot).toBeHidden();

  await page.getByRole("button", { name: "Analysis", exact: true }).click();
  await expect(timeline.getByText("Extended Analysis complete").first()).toBeVisible();
  await expect(timeline.getByText("Issue confirm recorded")).toHaveCount(0);

  await page.getByRole("button", { name: "Your decisions", exact: true }).click();
  await expect(timeline.getByText("Issue confirm recorded").first()).toBeVisible();
  await expect(timeline.getByText("Extended Analysis complete")).toHaveCount(0);

  await page.getByRole("button", { name: "All", exact: true }).click();
  await expect(timeline.getByText("Extended Analysis complete").first()).toBeVisible();
  await expect(timeline.getByText("Issue confirm recorded").first()).toBeVisible();
});

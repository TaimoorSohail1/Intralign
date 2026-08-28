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

test("Issues regression filters issues and persists a governed resolution selection", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  if (!projectId) throw new Error(`Could not read a project id from ${page.url()}`);
  const issuesLink = page.getByRole("link", { name: /^Issues/ });
  if (await issuesLink.isVisible()) {
    await issuesLink.click();
  } else {
    await page.goto(`/projects/${projectId}/issues`);
  }
  await expect(page).toHaveURL(/\/issues$/);
  await expect(page.getByRole("region", { name: "Exposure-ranked issue queue" })).toBeVisible();

  const issueCard = page.locator(".issue-row").first();
  await expect(issueCard).toBeVisible();
  const issueTitle = (await issueCard.locator(".r2-issue-copy strong").innerText()).trim();
  await issueCard.click();

  const dialog = page.getByRole("region", { name: "Issue details" });
  await expect(dialog).toBeVisible();
  const whyItMatters = dialog.getByRole("button", { name: "Why it matters" });
  await expect(whyItMatters).toHaveAttribute("aria-expanded", "false");
  await whyItMatters.click();
  await expect(dialog.getByRole("heading", { name: "What this weakens" })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "OSLO recommended" })).toBeVisible();

  const evidence = dialog.getByRole("button", { name: /^Evidence/ });
  await expect(evidence).toHaveAttribute("aria-expanded", "false");
  await evidence.click();
  await expect(evidence).toHaveAttribute("aria-expanded", "true");

  await dialog
    .getByRole("button", { name: /Other (?:ways to handle this|options \(\d+\))/ })
    .click();
  await dialog.getByRole("button", { name: "Select this path" }).click();

  const settlement = page
    .getByRole("region", { name: "Acted on, not yet closed" })
    .getByText(issueTitle, { exact: true });
  await expect(settlement).toBeVisible();
  await expect(
    page.getByRole("region", { name: "Acted on, not yet closed" }).getByText(
      "Waiting for reanalysis",
      { exact: true },
    ),
  ).toBeVisible();

  await page.reload();
  const persistedSettlement = page.getByRole("region", { name: "Acted on, not yet closed" });
  await expect(persistedSettlement.getByText(issueTitle, { exact: true })).toBeVisible();
  await persistedSettlement.getByRole("button", { name: `View ${issueTitle}` }).click();
  await expect(
    page.getByRole("region", { name: "Issue details" }).getByRole("heading", {
      name: "Confirmed by you",
    }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Close issue" }).click();
  await expect(page.getByRole("button", { name: new RegExp(issueTitle) })).toBeVisible();
});

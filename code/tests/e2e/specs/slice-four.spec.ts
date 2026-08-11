import { expect, test } from "@playwright/test";

test.setTimeout(180_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 20_000 });
}

async function createAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");

  const analyzedProject = page
    .locator("article.workspace-project-card")
    .filter({ hasText: "7 / 7" })
    .first();
  if (await analyzedProject.count()) {
    await analyzedProject.getByRole("link", { name: /Open project/ }).click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/);
    await expect(
      page.getByText("Project summary", { exact: true }),
    ).toBeVisible({ timeout: 120_000 });
    return;
  }

  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first project/ }).click();
  await page.getByRole("button", { name: /sample project/i }).click();
  await page.getByRole("button", { name: /See where I stand/ }).click();
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
    await expect(orientation).toBeHidden();
  }
  await expect(
    page.getByText("Project summary", { exact: true }),
  ).toBeVisible({ timeout: 120_000 });
}

test("Slice 4 renders the current-snapshot Attention Map and drills into findings", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  await page
    .getByRole("navigation", { name: "Workspace" })
    .getByRole("link", { name: /^Attention map/ })
    .click();
  await expect(page).toHaveURL(/\/attention/);
  await expect(page.getByRole("heading", { name: "Attention map" })).toBeVisible();
  await expect(
    page.getByText(/Brighter = more attention — not a health score\./),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Dimensions" })).toHaveCount(0);

  const activeCells = page.locator('[role="gridcell"][tabindex="0"]');
  await expect(activeCells.first()).toBeVisible();
  await activeCells.first().focus();
  await page.keyboard.press("Enter");

  const issueDialog = page.getByRole("dialog", { name: "Issue details" });
  await page.waitForTimeout(100);
  if (page.url().includes("/issues")) {
    await expect(page.getByRole("heading", { name: "Issues" })).toBeVisible();
    await page.goBack();
    await expect(page.getByRole("heading", { name: "Attention map" })).toBeVisible();
  } else {
    await expect(issueDialog).toBeVisible();
    await expect(issueDialog.getByText("Open", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Addressed", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Resolved", { exact: true })).toBeVisible();
    await expect
      .poll(() =>
        issueDialog.evaluate((element) => ({
          canScroll: element.scrollHeight > element.clientHeight,
          overflowY: getComputedStyle(element).overflowY,
        })),
      )
      .toEqual({ canScroll: true, overflowY: "auto" });
    await page.getByRole("button", { name: "Close issue" }).click();
  }

  await page.getByRole("button", { name: /Open Resources findings/ }).click();
  await expect(page).toHaveURL(/\/issues\?artifact=resources/);
  await expect(
    page.getByRole("button", { name: /Resources \d+/ }),
  ).toHaveAttribute("aria-pressed", "true");

  await page.goBack();
  await expect(page.getByRole("button", { name: /Ask OSLO about this map/ })).toBeVisible();
});

import { expect, test } from "@playwright/test";

test.setTimeout(180_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/admin\/invitations/, { timeout: 20_000 });
}

async function createAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");

  const existingProject = page.getByRole("link", { name: "Open project" }).first();
  if (await existingProject.isVisible()) {
    await existingProject.click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/);
    await expect(
      page.getByText("Current evidence-qualified read", { exact: true }),
    ).toBeVisible({ timeout: 120_000 });
    return;
  }

  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first project/ }).click();
  await page.getByRole("button", { name: /sample project/i }).click();
  await page.getByRole("button", { name: /See where I stand/ }).click();
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 90_000 });

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await page.getByRole("button", { name: "Get started" }).click();
    for (let step = 0; step < 4; step += 1) {
      await page.getByRole("button", { name: "Next", exact: true }).click();
    }
    await page.getByRole("button", { name: "Finish tour" }).click();
  }
  await expect(
    page.getByText("Current evidence-qualified read", { exact: true }),
  ).toBeVisible({ timeout: 120_000 });
}

test("Slice 4 renders the current-snapshot Attention Map and drills into findings", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  await page.getByRole("link", { name: /^Attention map/ }).click();
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

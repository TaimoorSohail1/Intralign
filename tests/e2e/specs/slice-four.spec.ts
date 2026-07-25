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
  const scopeDialog = page.getByRole("dialog", { name: "Scoped attention findings" });
  await expect(issueDialog.or(scopeDialog)).toBeVisible();

  if (await scopeDialog.isVisible()) {
    await scopeDialog.locator(".attention-scope-item").first().click();
    await expect(issueDialog).toBeVisible();
    await expect(issueDialog.getByText("Open", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Addressed", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Resolved", { exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Close issue" }).click();
    await expect(scopeDialog).toBeVisible();
    await page.getByRole("button", { name: "Close scoped findings" }).click();
  } else {
    await expect(issueDialog.getByText("Open", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Addressed", { exact: true })).toBeVisible();
    await expect(issueDialog.getByText("Resolved", { exact: true })).toBeVisible();
    await page.getByRole("button", { name: "Close issue" }).click();
  }

  await page.getByRole("button", { name: /Open Resources findings/ }).click();
  await expect(scopeDialog).toBeVisible();
  await expect(scopeDialog.getByText("Resources", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Close scoped findings" }).click();

  await expect(page.getByRole("button", { name: /Ask OSLO about this map/ })).toBeVisible();
});

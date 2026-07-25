import { expect, test } from "@playwright/test";

test.setTimeout(180_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  for (let attempt = 0; attempt < 2; attempt += 1) {
    await page.getByRole("button", { name: "Sign in" }).click();
    try {
      await page.waitForURL(/\/admin\/invitations/, { timeout: 15_000 });
      return;
    } catch {
      if (attempt === 1) throw new Error("Local admin sign-in did not recover");
    }
  }
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

test("Slice 3 exposes an evidence-qualified console and stable workspace routes", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  await expect(page.getByRole("navigation", { name: "Workspace" })).toBeVisible();
  await expect(page.getByRole("button", { name: "How confidence is calculated" })).toBeVisible();
  await page.getByRole("button", { name: "Why this confidence read" }).click();
  await expect(page.getByRole("region", { name: "Confidence calculation" })).toBeVisible();

  const issue = page.locator(".issue-row").first();
  await issue.focus();
  await issue.click();
  await expect(page.getByRole("dialog", { name: "Issue details" })).toBeVisible();
  await expect(page.getByLabel("OSLO project advisor")).toHaveCount(0);
  await page.getByRole("button", { name: "Close issue" }).click();
  await expect(issue).toBeFocused();

  const workspace = page.getByRole("navigation", { name: "Workspace" });
  await workspace.getByRole("link", { name: /^Attention map/ }).click();
  await expect(page).toHaveURL(/\/attention/);
  await expect(page.getByRole("heading", { name: "Attention map" })).toBeVisible();

  await workspace.getByRole("link", { name: /Issues/ }).click();
  await expect(page.getByText(/full issues workspace arrives in Slice 6/i)).toBeVisible();
  await page.getByRole("link", { name: "History" }).click();
  await expect(page.getByText(/full decision history arrives in Slice 7/i)).toBeVisible();
});

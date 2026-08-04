import { expect, test } from "@playwright/test";

test.setTimeout(240_000);

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
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await page.getByRole("button", { name: "Get started" }).click();
    for (let step = 0; step < 4; step += 1) {
      await page.getByRole("button", { name: "Next", exact: true }).click();
    }
    await page.getByRole("button", { name: "Finish tour" }).click();
  }
  await expect(
    page.getByText("Project summary", { exact: true }),
  ).toBeVisible({ timeout: 120_000 });
}

test("Slice 6 filters issues and persists a governed resolution selection", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  await page.getByRole("link", { name: /^Issues/ }).click();
  await expect(page).toHaveURL(/\/issues$/);
  await expect(page.getByRole("heading", { name: "Issues" })).toBeVisible();
  await expect(page.getByRole("button", { name: "By dimension" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await page.getByRole("button", { name: "By severity" }).click();
  await expect(page.getByRole("button", { name: "By severity" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );

  const issueCard = page.locator(".issue-workspace-card").first();
  await expect(issueCard).toBeVisible();
  const issueTitle = (await issueCard.locator("strong").innerText()).trim();
  await issueCard.click();

  const dialog = page.getByRole("dialog", { name: "Issue details" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "Why this matters" })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "What this weakens" })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "OSLO recommended" })).toBeVisible();

  const evidence = dialog.getByRole("button", { name: /^Evidence/ });
  await expect(evidence).toHaveAttribute("aria-expanded", "false");
  await evidence.click();
  await expect(evidence).toHaveAttribute("aria-expanded", "true");

  await dialog.getByRole("button", { name: "Select this path" }).click();
  await expect(dialog.getByRole("heading", { name: "Confirmed by you" })).toBeVisible();
  await expect(dialog.getByLabel("Issue status addressed")).toBeVisible();

  await page.reload();
  await page.getByRole("button", { name: new RegExp(issueTitle) }).click();
  await expect(
    page.getByRole("dialog", { name: "Issue details" }).getByRole("heading", {
      name: "Confirmed by you",
    }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Close issue" }).click();

  await page.getByRole("button", { name: "Addressed", exact: true }).click();
  await expect(page.getByRole("button", { name: new RegExp(issueTitle) })).toBeVisible();
});

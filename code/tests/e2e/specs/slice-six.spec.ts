import { expect, test } from "@playwright/test";

test.setTimeout(240_000);

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
    await expect(page.getByText("Project summary", { exact: true })).toBeVisible({
      timeout: 120_000,
    });
    return;
  }
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
  await expect
    .poll(() =>
      dialog.evaluate((element) => ({
        canScroll: element.scrollHeight > element.clientHeight,
        overflowY: getComputedStyle(element).overflowY,
      })),
    )
    .toEqual({ canScroll: true, overflowY: "auto" });
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

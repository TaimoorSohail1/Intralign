import { expect, type Page } from "@playwright/test";

export async function unlockFirstRead(page: Page) {
  const shell = page.locator(".project-shell");
  if (!(await shell.evaluate((element) => element.classList.contains("is-first-run-frozen")))) {
    return;
  }

  const confirm = page
    .getByRole("button", { name: "Confirm — it holds" })
    .first();
  const decision = page
    .getByRole("button", { name: "I’ve verified this directly" })
    .first();
  if (!(await decision.isVisible())) {
    await expect(confirm).toBeVisible();
    await confirm.click();
  }
  await expect(decision).toBeVisible();
  const actResponse = page.waitForResponse(
    (response) =>
      response.request().method() === "POST" && /\/issues\/.+\/acts$/.test(response.url()),
  );
  await decision.click();
  expect((await actResponse).ok()).toBeTruthy();
  await page.reload();
  await expect(shell).not.toHaveClass(/is-first-run-frozen/, { timeout: 30_000 });
  const closeIssue = page.getByRole("button", { name: "Close issue" });
  if (await closeIssue.isVisible()) await closeIssue.click();
}

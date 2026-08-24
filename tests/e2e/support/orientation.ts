import { expect, type Page } from "@playwright/test";

export async function dismissOrientation(page: Page) {
  let orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (!(await orientation.isVisible())) return;

  const getStarted = orientation.getByRole("button", { name: "Get started", exact: true });
  if (await getStarted.isVisible()) {
    await getStarted.click();
    await orientation.waitFor({ state: "hidden", timeout: 3_000 }).catch(() => undefined);
    orientation = page.getByRole("dialog", { name: "How OSLO works" });
    await orientation.waitFor({ state: "visible", timeout: 1_000 }).catch(() => undefined);
  }

  if (!(await orientation.isVisible())) return;
  const skip = orientation.getByRole("button", { name: /^(Skip|Skip tour)$/ });
  await skip.click();
  await expect(orientation).toBeHidden();
}

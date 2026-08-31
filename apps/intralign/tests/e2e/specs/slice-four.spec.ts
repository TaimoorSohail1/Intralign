import { expect, test } from "../fixtures";

test.setTimeout(300_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  for (let attempt = 0; attempt < 3; attempt += 1) {
    await page.getByRole("button", { name: "Sign in" }).click();
    try {
      await page.waitForURL(/\/(workspace|welcome)/, { timeout: 45_000 });
      return;
    } catch {
      if (attempt === 2) throw new Error("Local E2E owner sign-in did not recover");
    }
  }
}

async function unlockFirstRead(page: import("@playwright/test").Page) {
  const decision = page.getByRole("button", { name: /verified this directly/i });
  await decision.waitFor({ state: "visible", timeout: 2_000 }).catch(() => undefined);
  if (!(await decision.isVisible())) return;
  const actResponse = page.waitForResponse(
    (response) => response.request().method() === "POST" && /\/issues\/.+\/acts$/.test(response.url()),
  );
  await decision.click();
  expect((await actResponse).ok()).toBeTruthy();
  await page.reload();
  await expect(page.locator(".project-shell")).not.toHaveClass(/is-first-run-frozen/, {
    timeout: 30_000,
  });
  const closeIssue = page.getByRole("button", { name: "Close issue" });
  if (await closeIssue.isVisible()) await closeIssue.click();
}

async function createAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");

  const analyzedProject = page.getByRole("link", { name: /Open (?:the )?project/i }).first();
  if (await analyzedProject.count()) {
    await analyzedProject.click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/);
    await expect(page.getByRole("navigation", { name: "Workspace" })).toBeVisible();
    await unlockFirstRead(page);
    return;
  }

  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first (?:outcome|project)/i }).click();
  await page.getByRole("button", { name: /sample (?:plan|project)/i }).click();
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
}

test("Slice 4 removes the superseded Attention Map and keeps its URL compatible", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  if (!projectId) throw new Error(`Could not read a project id from ${page.url()}`);
  const workspace = page.getByRole("navigation", { name: "Workspace" });
  if (await workspace.isVisible()) {
    await expect(
      workspace.getByRole("link", { name: /^Attention map/ }),
    ).toHaveCount(0);
  }
  await page.goto(`/projects/${projectId}/attention`);
  await expect(page).toHaveURL(/\/issues$/, { timeout: 120_000 });
  await expect(page.getByRole("region", { name: "Exposure-ranked issue queue" })).toBeVisible();
});

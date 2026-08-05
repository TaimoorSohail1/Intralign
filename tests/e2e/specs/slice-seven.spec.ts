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

test("Slice 7 retains read-only history, snapshots, filters, and historical advisor context", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  await page.getByRole("link", { name: /^History/ }).click();
  await expect(page).toHaveURL(/\/history$/);
  await expect(page.getByRole("heading", { name: "History & timeline" })).toBeVisible();
  await expect(page.getByText("Extended Analysis complete").first()).toBeVisible({
    timeout: 120_000,
  });
  await expect(page.getByText("Initial Analysis complete").first()).toBeVisible();
  await expect(page.getByText(/Read-only · viewing history changes nothing/)).toBeVisible();

  await page.getByRole("button", { name: "Versions" }).click();
  const retainedVersion = page.getByText(/plan-artifact versions retained/).first();
  await expect(retainedVersion).toBeVisible();
  await page.getByRole("button", { name: /View snapshot/ }).first().click();
  const snapshot = page.getByRole("dialog", { name: "Historical snapshot" });
  await expect(snapshot).toBeVisible();
  await expect(snapshot.getByText("Read-only retained state")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(snapshot).toBeHidden();

  await page.getByRole("button", { name: "All" }).click();
  const extendedToggle = page.getByRole("button", {
    name: /Collapse Extended Analysis complete/,
  });
  await extendedToggle.click();
  await expect(
    page.getByRole("button", { name: /Expand Extended Analysis complete/ }),
  ).toBeVisible();

  let advisorBody: Record<string, unknown> | undefined;
  await page.route("**/api/projects/*/advisor", async (route) => {
    advisorBody = route.request().postDataJSON() as Record<string, unknown>;
    await route.fulfill({
      contentType: "application/json",
      json: {
        answer: "This answer is grounded in the selected retained run.",
        follow_up_questions: [],
      },
      status: 200,
    });
  });
  await page
    .getByRole("button", { name: /Ask OSLO about Extended Analysis complete/ })
    .click();
  await expect
    .poll(() => advisorBody?.historyRunId)
    .toMatch(/^[0-9a-f-]{36}$/);
});

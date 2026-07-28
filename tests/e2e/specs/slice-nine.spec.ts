import { expect, test } from "@playwright/test";

test.setTimeout(240_000);

async function dismissOrientation(page: import("@playwright/test").Page) {
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (!(await orientation.isVisible())) return;
  await orientation.getByRole("button", { name: "Get started" }).click();
  await orientation.getByRole("button", { name: "Skip tour" }).click();
  await expect(orientation).toBeHidden();
}

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/admin\/invitations/, { timeout: 20_000 });
}

async function openFirstProject(page: import("@playwright/test").Page) {
  await page.goto("/workspace");
  if (await page.getByRole("link", { name: /Open project/ }).count() === 0) {
    await page.getByRole("button", { name: /Create your first project/ }).click();
    await expect(page).toHaveURL(/\/intake\?project=/);
    await page.getByRole("button", { name: /sample project/i }).click();
    await page.getByRole("button", { name: /See where I stand/ }).click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 90_000 });
    await expect(page.getByText("Understanding is forming")).toBeVisible({ timeout: 120_000 });
    await dismissOrientation(page);
    await page.goto("/workspace");
  }
  const projectLink = page.getByRole("link", { name: /Open project/ }).first();
  await expect(projectLink).toBeVisible();
  const href = await projectLink.getAttribute("href");
  expect(href).toMatch(/^\/projects\/.+\/overview$/);
  await page.goto(href!);
}

test("Slice 9 exports, shares a retained snapshot, and records an external review", async ({
  browser,
  page,
}) => {
  await signIn(page);
  await openFirstProject(page);

  await dismissOrientation(page);

  const collaboration = page.getByRole("group", {
    name: "Project sharing and export",
  });
  await expect(collaboration.getByRole("button", { name: "Share" })).toBeVisible();
  await expect(collaboration.getByRole("button", { name: "Export" })).toBeVisible();

  await collaboration.getByRole("button", { name: "Export" }).click();
  let dialog = page.getByRole("dialog", { name: "Export project" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByText(/Exporting never runs analysis/)).toBeVisible();
  const download = dialog.getByRole("link", { name: "Download PDF" });
  const exportHref = await download.getAttribute("href");
  expect(exportHref).toMatch(/^\/api\/projects\/.+\/export$/);
  const exportResponse = await page.request.get(exportHref!);
  expect(exportResponse.status()).toBe(200);
  expect(exportResponse.headers()["content-type"]).toContain("application/pdf");
  expect((await exportResponse.body()).byteLength).toBeGreaterThan(1_000);
  await dialog.getByRole("button", { name: "Close" }).click();

  await collaboration.getByRole("button", { name: "Share" }).click();
  dialog = page.getByRole("dialog", { name: "Share project" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "People with workspace access" })).toBeVisible();
  await expect(dialog.getByRole("heading", { name: "External review" })).toBeVisible();

  await dialog.getByRole("button", { name: "Create snapshot link" }).click();
  await expect(
    dialog.getByText("A read-only snapshot is ready to share.", { exact: true }),
  ).toBeVisible();
  const snapshotUrl = await dialog.locator(".collaboration-created-link code").textContent();
  expect(snapshotUrl).toMatch(/\/share\/[^/]+$/);

  const publicContext = await browser.newContext();
  const publicPage = await publicContext.newPage();
  await publicPage.goto(snapshotUrl!);
  await expect(publicPage.getByText("Read-only project snapshot")).toBeVisible();
  await expect(publicPage.getByText(/Read only/)).toBeVisible();
  await expect(publicPage.locator(".public-snapshot-grid article")).toHaveCount(7);
  await publicContext.close();

  await dialog.getByLabel("Reviewer name").fill("E2E Architecture Reviewer");
  await dialog.getByLabel(/Reviewer email/).fill("reviewer.e2e@example.com");
  await dialog.getByRole("button", { name: "Create review link" }).click();
  await expect(
    dialog.getByText("The external review link is ready.", { exact: true }),
  ).toBeVisible();
  const reviewUrl = await dialog.locator(".collaboration-created-link code").textContent();
  expect(reviewUrl).toMatch(/\/review\/[^/]+$/);

  const reviewContext = await browser.newContext();
  const reviewPage = await reviewContext.newPage();
  await reviewPage.goto(reviewUrl!);
  await expect(reviewPage.getByText("Governed OSLO review")).toBeVisible();
  await expect(
    reviewPage.getByRole("heading", { name: "Respond to this project read" }),
  ).toBeVisible();
  await reviewPage.getByLabel("Approve").check();
  await reviewPage
    .getByLabel("Reviewer note")
    .fill("Approved for the retained evidence-qualified snapshot.");
  await reviewPage.getByRole("button", { name: "Submit review" }).click();
  await expect(reviewPage.getByRole("heading", { name: "Thank you for the review" })).toBeVisible();
  await expect(reviewPage.getByText("No account or workspace seat was created.")).toBeVisible();
  await reviewContext.close();

  await dialog.getByRole("button", { name: "Close" }).click();
  await page.getByRole("link", { name: /^History/ }).click();
  await expect(page).toHaveURL(/\/history$/);
  await page.getByRole("button", { name: "Collaboration & invites" }).click();
  await expect(page.getByText(/Reviewer approve/).first()).toBeVisible({
    timeout: 30_000,
  });
});

import { expect, test } from "../fixtures";
import { unlockFirstRead } from "../helpers";

test.setTimeout(360_000);

async function dismissOrientation(page: import("@playwright/test").Page) {
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (!(await orientation.isVisible())) return;
  await orientation.getByRole("button", { name: "Skip", exact: true }).click();
  await expect(orientation).toBeHidden();
}

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

test("Slice 10 explains equal judgment and governs workspace capacity without deleting data", async ({
  page,
}, testInfo) => {
  await signIn(page);
  await page.goto("/workspace");

  await expect(page.getByRole("heading", { name: "Your project" })).toBeVisible();
  await expect(page.getByText("Pick up where understanding stands.")).toBeVisible();

  let analyzedProject = page
    .locator("article.r2-current-plan")
    .filter({ hasText: /Analyzed.*7 (?:artifacts|plan artifacts)/i })
    .first();
  if (await analyzedProject.count() === 0) {
    await page.getByRole("button", { name: "New project" }).click();
    await expect(page).toHaveURL(/\/intake\?project=/);
    await page.getByRole("button", { name: /sample (?:project|plan)/i }).click();
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
    await dismissOrientation(page);
    await unlockFirstRead(page);
    await expect(page.getByRole("region", { name: "Outcome Integrity summary" })).toBeVisible({
      timeout: 120_000,
    });
    await page.goto("/workspace");
    analyzedProject = page
      .locator("article.r2-current-plan")
      .filter({ hasText: /Analyzed.*7 (?:artifacts|plan artifacts)/i })
      .first();
  }
  const analyzedProjectLink = analyzedProject.getByRole("link", { name: /Open the project/ });
  await expect(analyzedProjectLink).toBeVisible();
  const projectHref = await analyzedProjectLink.getAttribute("href");
  expect(projectHref).toMatch(/^\/projects\/.+\/overview$/);
  const analyzedProjectId = projectHref!.split("/")[2];
  const workspaceResponse = await page.request.get("/api/workspace");
  expect(workspaceResponse.ok()).toBeTruthy();
  const workspace = (await workspaceResponse.json()) as {
    projects: Array<{ id: string; archived: boolean }>;
  };
  for (const project of workspace.projects.filter(
    (candidate) => !candidate.archived && candidate.id !== analyzedProjectId,
  )) {
    const archiveResponse = await page.request.post(
      `/api/workspace/projects/${project.id}/archive`,
    );
    expect(archiveResponse.ok()).toBeTruthy();
  }
  await page.reload();

  let capacity = page.getByRole("dialog", { name: /Run more than one plan/ });
  for (let attempt = 0; attempt < 3 && !(await capacity.isVisible()); attempt += 1) {
    await page.getByRole("button", { name: "New project", exact: true }).click();
    await capacity.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
    if (await capacity.isVisible()) break;
    await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
    await page.goto("/workspace");
    capacity = page.getByRole("dialog", { name: /Run more than one plan/ });
  }
  await expect(capacity).toBeVisible();
  await expect(capacity.getByText(/gates capacity, never the quality/i)).toBeVisible();
  await capacity.getByRole("button", { name: /Upgrade your plan/ }).click();

  let plans = page.getByRole("dialog", { name: "Your plan" });
  await expect(plans).toBeVisible();
  await expect(plans.getByText("Every plan gets the same read.")).toBeVisible();
  await expect(
    plans.getByText(/Plans differ only on capacity/),
  ).toBeVisible();
  await expect(plans.getByText(/Judgment quality never changes/)).toBeVisible();
  await expect(plans.getByText(/Cancellation preserves every record/)).toBeVisible();
  await plans.getByRole("button", { name: "Done" }).click();

  await page.goto(projectHref!);
  await dismissOrientation(page);

  if (testInfo.project.name === "desktop") {
    const projectPlanBadge = page.getByRole("button", { name: "Basic", exact: true });
    await expect(projectPlanBadge).toBeVisible();
    await projectPlanBadge.click();
    const settings = page.getByRole("dialog", { name: "Settings" });
    await expect(settings.getByRole("heading", { name: "Plan & usage" })).toBeVisible();
    await expect(settings.getByText("Documents", { exact: true })).toBeVisible();
    await expect(settings.getByText("Unlimited", { exact: true })).toBeVisible();
    await expect(settings.getByText("History", { exact: true })).toBeVisible();
    await expect(settings.getByText("Full", { exact: true })).toBeVisible();
    await settings.getByRole("button", { name: "Close settings" }).click();
  }

  await page.goto(projectHref!.replace(/\/overview$/, "/reports"));
  await expect(page.getByRole("textbox", { name: "Edit readout" })).toBeVisible();
  if (testInfo.project.name === "desktop") {
    await expect(page.getByRole("button", { name: "Basic", exact: true })).toBeVisible();
    await expect(page.getByRole("link", { name: "Reports" })).toHaveAttribute(
      "aria-current",
      "page",
    );
  }
  const readout = page.getByRole("textbox", { name: "Edit readout" });
  await expect(readout).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Summary" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "What changed" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Key risks" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Assumptions" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Plan of action" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Decisions needed" })).toBeVisible();
  await expect(readout.getByRole("heading", { name: "Appendix" })).toBeVisible();
  await expect(page.getByText("Saved automatically to this workspace")).toBeVisible();

  await page.goto(projectHref!.replace(/\/overview$/, "/grounding"));
  await expect(page.getByRole("heading", { name: "Grounding map" })).toBeVisible();
  if (testInfo.project.name === "desktop") {
    await expect(page.getByRole("link", { name: "Grounding map" })).toHaveAttribute(
      "aria-current",
      "page",
    );
  }
  await expect(page.getByText("what your plan rests on — grounded vs still OSLO-inferred")).toBeVisible();
});

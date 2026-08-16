import { expect, test } from "../fixtures";

test.setTimeout(240_000);

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

  await expect(page.getByRole("heading", { name: "OSLO Product Grill" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Active projects" })).toBeVisible();

  let analyzedProject = page
    .locator("article.workspace-project-card")
    .filter({ hasText: /Analyzed.*7 artifacts/i })
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
    await expect(page.getByText("Project summary", { exact: true })).toBeVisible({
      timeout: 120_000,
    });
    await dismissOrientation(page);
    await page.goto("/workspace");
    analyzedProject = page
      .locator("article.workspace-project-card")
      .filter({ hasText: /Analyzed.*7 artifacts/i })
      .first();
  }
  const analyzedProjectLink = analyzedProject.getByRole("link", { name: /Open project/ });
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

  await page.getByRole("button", { name: /Compare plans/ }).click();
  let plans = page.getByRole("dialog", { name: "Your plan" });
  await expect(plans).toBeVisible();
  await expect(plans.getByText("Every plan gets the same read.")).toBeVisible();
  await expect(
    plans.getByText(/Plans differ on capacity, scope and collaboration/),
  ).toBeVisible();

  await expect(plans.getByRole("button", { name: "You’re on Basic" })).toBeDisabled();
  await plans.getByRole("button", { name: "Done" }).click();

  await page.getByRole("button", { name: "New project" }).click();
  await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
  await page.goto("/workspace");
  await expect(page.getByText("3 active projects", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: /Compare plans/ }).click();

  plans = page.getByRole("dialog", { name: "Your plan" });
  await expect(plans).toBeVisible();
  await expect(plans.getByRole("button", { name: "You’re on Basic" })).toBeDisabled();
  await plans.getByRole("button", { name: "Done" }).click();

  await page.goto("/settings#subscription");
  await expect(page.getByRole("heading", { name: "Subscription" })).toBeVisible();
  await expect(page.getByText("Basic", { exact: true })).toBeVisible();
  await expect(page.getByText("Not yet set", { exact: true })).toBeVisible();
  await expect(page.getByText("Never metered.", { exact: true })).toBeVisible();
  await expect(page.getByText("PDF · Copy summary · Export link", { exact: true })).toBeVisible();

  await page.goto(projectHref!);
  await dismissOrientation(page);

  if (testInfo.project.name !== "mobile") {
    const projectPlanBadge = page.getByRole("button", { name: "Basic", exact: true });
    await expect(projectPlanBadge).toBeVisible();
    await projectPlanBadge.click();
    const usage = page.getByRole("dialog", { name: "Usage & limits" });
    await expect(usage).toBeVisible();
    await expect(usage.getByText("What you are using, on Basic", { exact: true })).toBeVisible();
    await usage.getByRole("button", { name: "Close usage and limits" }).click();
  }

  await page.goto(projectHref!.replace(/\/overview$/, "/reports"));
  await expect(page.getByRole("textbox", { name: "Edit readout" })).toBeVisible();
  if (testInfo.project.name !== "mobile") {
    await expect(page.getByRole("button", { name: "Basic", exact: true })).toBeVisible();
  }
  await expect(page.getByRole("link", { name: "Reports" })).toHaveAttribute(
    "aria-current",
    "page",
  );
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

  await page.goto(projectHref!.replace(/\/overview$/, "/inference"));
  await expect(page.getByRole("heading", { name: "Inference map" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Inference map" })).toHaveAttribute(
    "aria-current",
    "page",
  );
  await expect(page.getByRole("heading", { name: "By artifact" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Assumptions" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Structure" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "This week" })).toBeVisible();
});

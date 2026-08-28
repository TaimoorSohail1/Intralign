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

test("Slice 2 survives refresh and publishes exactly seven artifacts", async ({ page }) => {
  await signIn(page);
  const workspaceResponse = await page.request.get("/api/workspace");
  expect(workspaceResponse.ok()).toBeTruthy();
  const workspace = (await workspaceResponse.json()) as {
    projects: Array<{ id: string; archived: boolean }>;
  };
  for (const project of workspace.projects.filter((candidate) => !candidate.archived)) {
    const archiveResponse = await page.request.post(
      `/api/workspace/projects/${project.id}/archive`,
    );
    expect(archiveResponse.ok()).toBeTruthy();
  }
  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first (?:outcome|project)/i }).click();
  await expect(page).toHaveURL(/\/intake\?project=/);

  await page.getByRole("button", { name: /sample (?:plan|project)/i }).click();
  await expect(page.getByRole("button", { name: /Get my analysis|See where I stand/i })).toBeEnabled();
  await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
  await expect(page).toHaveURL(/\/projects\/.+\/(analysis\/.+|overview)/, { timeout: 120_000 });

  if (page.url().includes("/analysis/")) {
    await page.reload();
    await expect(page.getByRole("status")).toContainText(
      /Your read is ready|Analyzing|Reading your inputs|Your progress is safe/i,
    );
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
  if (!(await page.locator(".confidence-read").isVisible())) {
    await page.getByRole("button", { name: "Expand Outcome Integrity" }).click();
  }
  await expect(page.locator(".confidence-read")).toBeVisible();

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
    await expect(orientation).toBeHidden();
  }

  await expect(page.locator(".r2-maturity-row > small")).toContainText(
    /as of this analysis.+live tracking begins at execution/i,
  );
  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  if (!projectId) throw new Error(`Could not read a project id from ${page.url()}`);
  const artifactLinks = page
    .getByRole("complementary", { name: "Project navigation" })
    .locator('a[href*="/artifacts/"]');
  if (await artifactLinks.first().isVisible()) {
    const artifactHrefs = await artifactLinks.evaluateAll((links) =>
      links.map((link) => link.getAttribute("href")),
    );
    expect(new Set(artifactHrefs).size).toBe(7);
  } else {
    const overviewResponse = await page.request.get(`/api/projects/${projectId}/overview`);
    expect(overviewResponse.ok()).toBeTruthy();
    const overview = (await overviewResponse.json()) as { artifacts: unknown[] };
    expect(overview.artifacts).toHaveLength(7);
  }
  await expect(page.locator(".project-advisory")).toContainText("OSLO advises; you decide");
  await expect(page.getByRole("dialog", { name: "Issue details" })).toHaveCount(0);

  const hideAdvisor = page.getByRole("button", { name: "Hide the OSLO panel" });
  if (await hideAdvisor.isVisible()) {
    await hideAdvisor.click();
  }
  const issueRows = page.locator(".issue-row");
  await expect(issueRows).not.toHaveCount(0);
  await issueRows.first().click();
  await expect(page.getByRole("region", { name: "Issue details" })).toBeVisible();
  await page.getByRole("button", { name: "Close issue" }).click();
  await expect(page.getByRole("region", { name: "Issue details" })).toHaveCount(0);
});

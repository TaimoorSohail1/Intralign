import { expect, test } from "../fixtures";

test.setTimeout(240_000);

type GovernedAct = "confirm" | "flag" | "route";

type OpenIssue = {
  id: string;
  title: string;
  status: string;
};

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

async function createAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/welcome");
  await page.getByRole("button", { name: /Start your first (?:outcome|project)/ }).click();
  await page.getByRole("button", { name: /sample (?:project|plan)/i }).click();
  await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
  await page.waitForURL(/\/projects\/[^/]+\/(?:analysis\/[^/]+|overview)/, {
    timeout: 120_000,
  });
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
  await page.waitForURL(/\/projects\/[^/]+\/overview/, { timeout: 120_000 });
  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  expect(projectId).toBeTruthy();
  return projectId!;
}

async function openIssue(
  page: import("@playwright/test").Page,
  projectId: string,
  issue: OpenIssue,
) {
  await page.goto(`/projects/${projectId}/issues`);
  const issueRow = page.locator(".issue-row").filter({ hasText: issue.title }).first();
  await expect(issueRow).toBeVisible();
  await issueRow.click();
  const panel = page.locator(".issue-panel");
  await expect(panel.getByRole("heading", { name: issue.title })).toBeVisible();
  return panel;
}

test("N-4 intercepts Confirm, Flag and Route failures without losing retry intent", async ({
  page,
}, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "One desktop transport proof covers this seam.");

  const projectId = await createAnalyzedProject(page);
  const overviewResponse = await page.request.get(`/api/projects/${projectId}/overview`);
  expect(overviewResponse.ok()).toBeTruthy();
  const overview = (await overviewResponse.json()) as {
    assessment: { issues: OpenIssue[] };
  };
  const issue = overview.assessment.issues.find((candidate) => candidate.status === "open");
  expect(issue, "The deterministic fixture needs one open issue").toBeTruthy();

  const intercepted: Array<{ act: GovernedAct; body: Record<string, unknown> }> = [];
  await page.route(/\/api\/projects\/[^/]+\/issues\/[^/]+\/acts$/, async (route) => {
    const body = route.request().postDataJSON() as Record<string, unknown>;
    intercepted.push({ act: body.act as GovernedAct, body });
    await route.abort("failed");
  });

  const attemptsFor = (act: GovernedAct) => intercepted.filter((entry) => entry.act === act);
  for (const act of ["confirm", "flag", "route"] as const) {
    const panel = await openIssue(page, projectId, issue!);
    if (act === "confirm") {
      await panel.getByRole("button", { name: "Confirm — it holds" }).click();
      await panel.getByRole("button", { name: "I have it documented in writing" }).click();
    } else if (act === "flag") {
      await panel.getByRole("button", { name: /It doesn't hold/ }).click();
    } else {
      await panel.getByRole("button", { name: /Ask for evidence/i }).click();
      await panel.getByRole("button", { name: /Project collaborator/i }).click();
    }

    // IC-WU-ACCEPT / N-4: prove the real round trip was intercepted before
    // accepting any UI observation as fault-injection evidence.
    await expect.poll(() => attemptsFor(act).length).toBe(1);
    const firstAttempt = attemptsFor(act)[0].body;
    expect(firstAttempt.idempotencyKey).toBeTruthy();
    if (act === "confirm") expect(firstAttempt.basis).toBe("documented");
    if (act === "route") {
      expect(firstAttempt.reviewer).toMatchObject({
        id: "project-collaborator",
        role: "collaborator",
      });
    }

    const alert = page.getByRole("alert");
    await expect(alert).toContainText("Your project data is unchanged.");
    await expect(page.getByText(/Failed to fetch/i)).toHaveCount(0);
    const retry = page.getByRole("button", { name: "Retry action" });
    await expect(retry).toBeEnabled();
    await retry.click();

    await expect.poll(() => attemptsFor(act).length).toBe(2);
    expect(attemptsFor(act)[1].body.idempotencyKey).toBe(firstAttempt.idempotencyKey);
    if (act === "confirm") expect(attemptsFor(act)[1].body.basis).toBe(firstAttempt.basis);
    if (act === "route") expect(attemptsFor(act)[1].body.reviewer).toEqual(firstAttempt.reviewer);

    const unchangedResponse = await page.request.get(`/api/projects/${projectId}/overview`);
    expect(unchangedResponse.ok()).toBeTruthy();
    const unchanged = (await unchangedResponse.json()) as {
      assessment: { issues: OpenIssue[] };
    };
    expect(unchanged.assessment.issues.find((candidate) => candidate.id === issue!.id)?.status)
      .toBe("open");
  }
});

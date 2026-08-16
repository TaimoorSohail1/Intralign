import { expect, test } from "../fixtures";

test.setTimeout(240_000);

type SliceTenIssue = {
  id: string;
  title: string;
  dimension: string;
  finding_type: string;
  finding_basis: "inference" | "structural" | "decision" | "model_gap";
  structural_target: "definition" | "edge" | "achievability" | "truth" | "coverage";
  primary_act: "verify" | "build" | "decide" | "";
  also_offered: Array<"verify" | "build" | "decide">;
  classification_state: "classified" | "escalated" | "unclassified";
  sensitivity_state: "calibrated" | "shadow" | "unavailable";
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
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 5_000 }).catch(() => undefined);
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip tour" }).click();
    await expect(orientation).toBeHidden();
  }
  return projectId!;
}

async function waitForCurrentRead(
  page: import("@playwright/test").Page,
  projectId: string,
) {
  await expect
    .poll(
      async () => {
        const response = await page.request.get(`/api/projects/${projectId}/overview`);
        if (!response.ok()) return "unavailable";
        const overview = (await response.json()) as { state: string };
        return overview.state;
      },
      { timeout: 120_000 },
    )
    .toBe("current");
}

test("Slice 10 classifies every finding and derives its governed primary act", async ({
  page,
}) => {
  const projectId = await createAnalyzedProject(page);

  const overviewResponse = await page.request.get(`/api/projects/${projectId}/overview`);
  expect(overviewResponse.ok()).toBeTruthy();
  const overview = (await overviewResponse.json()) as {
    assessment: { issues: SliceTenIssue[] };
  };
  expect(overview.assessment.issues.length).toBeGreaterThan(0);

  const dimensionByTarget = {
    definition: "Clarity",
    edge: "Alignment",
    achievability: "Feasibility",
    truth: "Grounding",
    coverage: "Adaptability",
  } as const;

  for (const issue of overview.assessment.issues) {
    expect(issue.finding_type, `${issue.id} must have a finding type`).not.toBe("");
    expect(issue.finding_basis, `${issue.id} must have a finding basis`).toBeTruthy();
    expect(issue.structural_target, `${issue.id} must have a structural target`).toBeTruthy();
    expect(["classified", "escalated"]).toContain(issue.classification_state);
    expect(issue.sensitivity_state).not.toBe("calibrated");

    if (issue.classification_state === "classified") {
      expect(["verify", "build", "decide"]).toContain(issue.primary_act);
      expect(issue.dimension).toBe(dimensionByTarget[issue.structural_target]);
      expect(issue.also_offered).not.toContain(issue.primary_act);
    } else {
      expect(issue.finding_basis).toBe("model_gap");
      expect(issue.primary_act).toBe("");
    }
  }
});

test("Slice 10 presents the derived build route and records the chosen resolution", async ({
  page,
}) => {
  const projectId = await createAnalyzedProject(page);
  await waitForCurrentRead(page, projectId);
  const overviewResponse = await page.request.get(`/api/projects/${projectId}/overview`);
  expect(overviewResponse.ok()).toBeTruthy();
  const overview = (await overviewResponse.json()) as {
    assessment: { issues: SliceTenIssue[] };
  };
  const issue = overview.assessment.issues.find(
    (candidate) =>
      candidate.classification_state === "classified" && candidate.primary_act === "build",
  );
  expect(issue, "The analyzed fixture needs a Build finding").toBeTruthy();

  await page.goto(`/projects/${projectId}/issues`);
  await expect(page.getByRole("region", { name: "Exposure-ranked issue queue" })).toBeVisible();
  const issueRow = page.locator(".issue-row").filter({ hasText: issue!.title }).first();
  await expect(issueRow).toBeVisible();
  await issueRow.evaluate((element: HTMLButtonElement) => element.click());

  const panel = page.locator(".issue-panel");
  await expect(panel.getByRole("heading", { name: issue!.title })).toBeVisible();
  await expect(panel.getByRole("button", { name: "Build this in the plan" })).toBeVisible();

  if (issue!.also_offered.includes("verify")) {
    await panel.getByRole("button", { name: "Verify with evidence" }).click();
    await expect(panel.getByRole("region", { name: "Ask for evidence" })).toBeVisible();
    await panel.getByRole("button", { name: "Cancel" }).click();
  }

  const saved = page.waitForResponse(
    (response) =>
      response.request().method() === "POST" &&
      response.url().includes(`/issues/${encodeURIComponent(issue!.id)}/actions`) &&
      response.ok(),
  );
  await panel.getByRole("button", { name: "Build this in the plan" }).click();
  await saved;
  await expect(panel.getByRole("heading", { name: "Confirmed by you" })).toBeVisible();

  await page.reload();
  const actedOn = page.getByRole("region", { name: "Acted on, not yet closed" });
  await expect(actedOn.getByText(issue!.title)).toBeVisible();
  await expect(actedOn.getByText("Waiting for reanalysis")).toBeVisible();
});

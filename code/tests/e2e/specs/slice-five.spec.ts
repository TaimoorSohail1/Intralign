import { expect, test } from "../fixtures";

test.setTimeout(300_000);
test.use({ trace: "retain-on-failure" });

const artifacts = [
  ["Intent", "intent"],
  ["Scope", "scope"],
  ["Requirements", "requirements"],
  ["Constraints", "constraints"],
  ["Work Breakdown", "work_breakdown"],
  ["Schedule", "schedule"],
  ["Resources", "resources"],
] as const;

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

async function ensureAnalyzedProject(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");
  const analyzedProject = page
    .locator("article")
    .filter({ hasText: /Analyzed.*7 artifacts|7 \/ 7/is })
    .first();

  if (await analyzedProject.count()) {
    await analyzedProject.getByRole("link", { name: /Open (?:project|now)/i }).click();
  } else {
    await page.goto("/welcome");
    await page.getByRole("button", { name: /Start your first outcome/i }).click();
    await expect(page).toHaveURL(/\/intake\?project=/);
    await page.getByRole("button", { name: /sample plan/i }).click();
    await page.getByRole("button", { name: /Get my analysis/i }).click();
  }

  await page.waitForURL(/\/projects\/[^/]+\/(?:analysis\/[^/]+|overview)/, {
    timeout: 30_000,
  });
  if (page.url().includes("/analysis/")) {
    const confirmOutcome = page
      .frameLocator('iframe[title="OSLO analysis and outcome confirmation"]')
      .getByRole("button", { name: /Yes.+this is my outcome/i });
    await expect(confirmOutcome).toBeVisible({ timeout: 120_000 });
    await confirmOutcome.click();
  }

  await expect(page).toHaveURL(/\/projects\/[^/]+\/overview/, { timeout: 120_000 });
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
    await expect(orientation).toBeHidden();
  }
  await expect(page.locator(".workspace-artifact-group")).toBeAttached({ timeout: 120_000 });

  const match = page.url().match(/\/projects\/([^/]+)\//);
  if (!match) throw new Error(`Project id was not present in ${page.url()}`);
  return match[1];
}

async function openArtifact(
  page: import("@playwright/test").Page,
  projectId: string,
  name: string,
  slug: string,
) {
  await page.goto(`/projects/${projectId}/artifacts/${slug}`);
  await expect(page.locator(".artifact-workspace h1")).toHaveText(
    name === "Work Breakdown" ? "Work breakdown" : name,
    { timeout: 30_000 },
  );
  await expect(page.getByText("Contents · you author, OSLO reads", { exact: true })).toBeVisible();
  await expect(page.getByText("Up to date", { exact: true })).toBeVisible({ timeout: 120_000 });
}

function normalizeStatement(value: string) {
  return value.normalize("NFKC").toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

test("Slice 5 renders all seven current artifacts once at every traced viewport", async ({
  page,
}, testInfo) => {
  const projectId = await ensureAnalyzedProject(page);

  for (const [name, slug] of artifacts) {
    await openArtifact(page, projectId, name, slug);

    const statementTexts = await page
      .locator(".r2-statement-row [contenteditable]")
      .allInnerTexts();
    const normalized = statementTexts.map(normalizeStatement).filter(Boolean);
    expect(normalized).toEqual([...new Set(normalized)]);

    const warningTexts = (await page.locator(".r2-row-warning").allInnerTexts())
      .map(normalizeStatement)
      .filter(Boolean);
    expect(warningTexts).toEqual([...new Set(warningTexts)]);

    const overflow = await page.locator("html").evaluate((element) =>
      Math.max(0, element.scrollWidth - element.clientWidth),
    );
    expect(overflow).toBeLessThanOrEqual(2);

    if (slug === "resources") {
      const summary = page.getByLabel("Resource summary");
      await expect(summary.locator("article")).toHaveCount(5);
      for (const label of ["People", "Budget", "Facility", "Vendors", "Equipment"]) {
        await expect(summary.getByText(label, { exact: true })).toBeVisible();
      }

      const resourceEvidence = page.getByLabel("Resource evidence");
      await expect(resourceEvidence.locator(".r2-statement-row").first()).toBeVisible();
      await expect(page.getByText("No task owner assignments are recorded yet.")).toBeVisible();
      await expect(page.locator('select[aria-label^="Owner for"]')).toHaveCount(0);
      await page.screenshot({
        path: testInfo.outputPath("resources-verified.png"),
        fullPage: false,
      });
    }
  }

});

test("Slice 5 view, edit, undo, and execution framing controls stay usable", async ({ page }) => {
  const projectId = await ensureAnalyzedProject(page);

  await openArtifact(page, projectId, "Intent", "intent");
  await page.getByRole("button", { name: "Narrative" }).click();
  await expect(page.getByLabel("Intent narrative")).toBeVisible();
  await expect(page.getByLabel("Intent narrative").locator("[contenteditable]"))
    .toHaveCount(0);
  await page.getByRole("button", { name: "Statements" }).click();
  await expect(page.locator(".r2-understanding-groups")).toBeVisible();

  await openArtifact(page, projectId, "Scope", "scope");
  const statement = page.locator(".r2-statement-row [contenteditable]").first();
  const original = await statement.innerText();
  await statement.fill(`${original} — E2E local review`);
  await expect(page.getByText("Changes not applied", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Undo" }).click();
  await expect(statement).toHaveText(original);
  await expect(page.getByText("Up to date", { exact: true })).toBeVisible();

  await openArtifact(page, projectId, "Work Breakdown", "work_breakdown");
  const backlog = page.getByRole("button", { name: "Backlog · agile" });
  await backlog.click();
  await expect(backlog).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator(".r2-wbs.is-backlog")).toBeVisible();
  const outline = page.getByRole("button", { name: "Outline · WBS" });
  await outline.click();
  await expect(outline).toHaveAttribute("aria-pressed", "true");

  const overflow = await page.locator("html").evaluate((element) =>
    Math.max(0, element.scrollWidth - element.clientWidth),
  );
  expect(overflow).toBeLessThanOrEqual(2);
});

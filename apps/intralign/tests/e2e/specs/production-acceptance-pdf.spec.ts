import path from "node:path";

import { expect, test } from "../fixtures";

test.setTimeout(180_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

test("PDF intake opens the progress page and keeps the first read truthful", async ({
  page,
}, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "One real-PDF pass is sufficient for this acceptance seam.");

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

  await page.goto("/workspace");
  await page.getByRole("button", { name: "New project", exact: true }).click();
  await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });

  const fixture = path.resolve(
    __dirname,
    "../../../output/pdf/devnorth-2026-venue-evidence.pdf",
  );
  await page.getByLabel("Attach documents").setInputFiles(fixture);
  await expect(page.getByText("devnorth-2026-venue-evidence.pdf")).toBeVisible();

  await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
  await expect(page).toHaveURL(/\/projects\/[^/]+\/analysis\/[^/]+/, {
    timeout: 60_000,
  });
  await expect(page.locator("main.r2-analysis-page")).toBeVisible();
  await expect(page.getByRole("status")).toContainText(/Stage \d of 8|Analysis complete/);

  const skipIntro = page.getByRole("button", { name: /Skip the intro/i });
  await skipIntro.waitFor({ state: "visible", timeout: 10_000 }).catch(() => undefined);
  if (await skipIntro.isVisible()) await skipIntro.click();
  const confirmOutcome = page
    .frameLocator('iframe[title="OSLO analysis and outcome confirmation"]')
    .getByRole("button", { name: /Yes.+this is my outcome/i });
  await expect(confirmOutcome).toBeVisible({ timeout: 120_000 });
  await confirmOutcome.click();

  await expect(page).toHaveURL(/\/projects\/[^/]+\/overview/, { timeout: 120_000 });
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
  }

  const integrity = page.getByRole("button", {
    name: /Outcome Integrity (Fragile|Weak|Developing|Solid|Sound), limited by (Viability|Grounding|Adaptability)/,
  });
  await expect(integrity).toBeVisible();
  const integrityLabel = await integrity.getAttribute("aria-label");
  const canonicalRead = integrityLabel?.match(
    /Outcome Integrity (Fragile|Weak|Developing|Solid|Sound), limited by (Viability|Grounding|Adaptability)/,
  );
  expect(canonicalRead).toBeTruthy();
  await expect(page.getByLabel("First run guidance")).toHaveText(
    /One call down|1 of 2/,
  );

  const projectId = new URL(page.url()).pathname.split("/")[2];
  await page.goto(`/projects/${projectId}/reports`);
  await expect(page).toHaveURL(/\/projects\/[^/]+\/reports/);
  const generateDraft = page.getByRole("button", { name: /Generate a draft/i });
  if (await generateDraft.isVisible()) await generateDraft.click();
  const readout = page.getByRole("textbox", { name: "Edit readout" });
  await expect(readout).toBeVisible();
  await expect(readout).toContainText(
    `Outcome Integrity is ${canonicalRead![1]}, limited by ${canonicalRead![2]}.`,
  );
  await expect(readout).toContainText("No changes to the plan since the last read.");
  await expect(readout).not.toContainText(/\b\d+\s+(?:issues\s+)?(?:opened|resolved)\b/i);
  await expect(readout).not.toContainText(/\[[a-z_]+:\d+\]/i);
});

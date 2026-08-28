import { expect, test } from "../fixtures";
import { unlockFirstRead } from "../helpers";

test.setTimeout(300_000);
test.use({ trace: "retain-on-failure" });

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

async function analyzedProjectId(page: import("@playwright/test").Page) {
  await signIn(page);
  await page.goto("/workspace");
  const projectLink = page.locator('a[href^="/projects/"][href$="/overview"]').first();
  if (await projectLink.count()) {
    await page.goto((await projectLink.getAttribute("href"))!);
  } else {
    await page.goto("/welcome");
    await page.getByRole("button", { name: /Start your first (?:outcome|project)/i }).click();
    await expect(page).toHaveURL(/\/intake\?project=/);
    await page.getByRole("button", { name: /sample (?:plan|project)/i }).click();
    await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
    await page.waitForURL(/\/projects\/[^/]+\/(?:analysis\/[^/]+|overview)/, {
      timeout: 120_000,
    });
    if (page.url().includes("/analysis/")) {
      const confirmOutcome = page
        .frameLocator('iframe[title="OSLO analysis and outcome confirmation"]')
        .getByRole("button", { name: /Yes.+this is my outcome/i });
      await expect(confirmOutcome).toBeVisible({ timeout: 120_000 });
      await confirmOutcome.click();
      await expect(page).toHaveURL(/\/projects\/[^/]+\/overview/, { timeout: 120_000 });
    }
  }
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 2_000 }).catch(() => undefined);
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
  }
  await unlockFirstRead(page);
  const projectId = page.url().match(/\/projects\/([^/]+)\//)?.[1];
  if (!projectId) throw new Error(`Could not read an analyzed project id from ${page.url()}`);
  return projectId;
}

async function openFirstIssue(page: import("@playwright/test").Page, projectId: string) {
  await page.goto(`/projects/${projectId}/issues`);
  const issueCards = page.locator(".issue-row");
  await expect(issueCards.first()).toBeVisible({ timeout: 30_000 });
  const count = await issueCards.count();
  const titles = await issueCards.locator(".r2-issue-copy strong").allTextContents();
  for (let index = 0; index < count; index += 1) {
    await issueCards.nth(index).click();
    const issue = page.getByRole("region", { name: "Issue details" });
    await expect(issue).toBeVisible();
    const citedEvidence = issue.getByRole("button", {
      name: /^Evidence .* [1-9]\d* sources?, traceable to inputs$/,
    });
    if (await citedEvidence.count()) {
      return {
        issue,
        issueTitle: titles[index]?.trim() ?? "",
        otherTitle: titles.find((title, titleIndex) => titleIndex !== index)?.trim(),
      };
    }
    await issue.getByRole("button", { name: "Close issue" }).first().click();
  }
  throw new Error("The analyzed fixture did not produce an issue with a cited source excerpt.");
}

test("R2 Slice 6 traces scoped review, projections, frozen sharing, and revocation", async ({
  browser,
  page,
}, testInfo) => {
  test.skip(testInfo.project.name === "tablet", "The release tracer is pinned at desktop and mobile widths.");
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
  const projectId = await analyzedProjectId(page);
  const { issue, otherTitle } = await openFirstIssue(page, projectId);

  await issue
    .getByRole("button", { name: /Ask for evidence|Verify with evidence/i })
    .click();
  await issue.getByRole("button", { name: /External evidence holder/i }).click();
  const scope = issue.getByLabel("External reviewer scope preview");
  await expect(scope).toBeVisible();
  const question = (await scope.locator("strong").innerText()).trim();
  const excerpt = (await scope.locator("p").innerText()).trim();
  await issue.getByLabel("Reviewer name").fill("Amina Khan");
  await issue.getByRole("button", { name: "Create secure review link" }).click();
  await expect(issue.getByText("Draft — copy the link to hand it off")).toBeVisible();
  const reviewUrl = (await issue.locator(".issue-review-link code").innerText()).trim();
  await issue.getByRole("button", { name: "Copy link" }).click();
  await expect(page.getByRole("region", { name: "Awaiting evidence" })).toBeVisible();

  const reviewerContext = await browser.newContext();
  const reviewer = await reviewerContext.newPage();
  await reviewer.goto(reviewUrl);
  await expect(reviewer.getByRole("heading", { name: question })).toBeVisible();
  await expect(reviewer.getByText(excerpt, { exact: true })).toBeVisible();
  await expect(reviewer.getByText("One question · one cited source")).toBeVisible();
  if (otherTitle && otherTitle !== question) {
    await expect(reviewer.getByText(otherTitle, { exact: true })).toHaveCount(0);
  }
  await expect(reviewer.getByRole("link")).toHaveCount(0);
  await reviewer.getByLabel("Confirm").check();
  await reviewer.getByLabel("Reviewer note").fill("I confirm the cited decision and own the evidence.");
  await reviewer.getByRole("button", { name: "Submit review" }).click();
  await expect(reviewer.getByRole("heading", { name: "Thank you for the review" })).toBeVisible();
  await expect(reviewer.getByText(/project read is updating/i)).toBeVisible();
  await reviewerContext.close();

  await page.reload();
  await page.getByLabel("Notifications").click();
  const notifications = page.getByRole("dialog", { name: "Notifications" });
  await expect(notifications.getByText(/Amina Khan confirmed the requested evidence/i)).toBeVisible({ timeout: 30_000 });
  await notifications.getByLabel("Close notifications").click();

  await page.goto(`/projects/${projectId}/roll-up`);
  await expect(page).toHaveURL(/\/outcome$/);
  await expect(page.getByRole("heading", { name: "Your Outcome" })).toBeVisible();
  await expect(page.getByText(/grounded by Amina Khan/i)).toBeVisible();

  await page.goto(`/projects/${projectId}/grounding`);
  const groundingMap = page.locator('[aria-labelledby="grounding-map-title"]');
  await expect(page.getByRole("heading", { name: "Grounding map" })).toBeVisible();
  await expect(page.getByText("what your plan rests on — grounded vs still OSLO-inferred")).toBeVisible();
  await expect(groundingMap.getByRole("button")).toHaveCount(0);
  await expect(groundingMap.getByRole("link").first()).toHaveAttribute("href", /\/issues\?issue=/);
  await expect(groundingMap.getByLabel("Additional grounding details")).toHaveCount(0);

  await page.goto(`/projects/${projectId}/overview`);
  await page.getByRole("group", { name: "Project sharing and export" }).getByRole("button", { name: "Share" }).click();
  const shareDialog = page.getByRole("dialog", { name: /^Share / });
  await shareDialog.getByLabel("Snapshot recipient name").fill("Executive sponsor");
  await shareDialog.getByRole("button", { name: "Create a view-only link" }).click();
  await expect(shareDialog.getByText("A view-only snapshot is ready to share.")).toBeVisible();
  const snapshotUrl = (await shareDialog.locator(".collaboration-created-link code").innerText()).trim();

  const viewerContext = await browser.newContext();
  const viewer = await viewerContext.newPage();
  await viewer.goto(snapshotUrl);
  await expect(viewer.getByText("Read-only project snapshot")).toBeVisible();
  await expect(viewer.getByText("Shared with Executive sponsor")).toBeVisible();
  await expect(viewer.getByText(/retained for 90 days/i)).toBeVisible();

  const shareRecord = shareDialog.locator(".collaboration-access-record").filter({ hasText: "Executive sponsor" });
  await shareRecord.getByRole("button", { name: "Revoke" }).click();
  await expect(shareDialog.getByText("The snapshot link was revoked.")).toBeVisible();
  await viewer.reload();
  await expect(viewer.getByRole("heading", { name: "This snapshot link is unavailable" })).toBeVisible();
  await viewerContext.close();

  expect(await page.locator("html").evaluate((element) => element.scrollWidth <= element.clientWidth + 1)).toBe(true);
});

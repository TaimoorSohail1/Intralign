import { expect, test } from "@playwright/test";

test.setTimeout(300_000);

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

async function openArtifact(
  page: import("@playwright/test").Page,
  name: string,
  slug: string,
) {
  const sidebarLink = page.getByRole("link", { name: new RegExp(`^${name}`) });
  if (await sidebarLink.isVisible()) {
    await sidebarLink.click();
  } else {
    await page.getByRole("button", { name: "Search project" }).click();
    await page.getByRole("option", { name, exact: true }).click();
  }
  await expect(page).toHaveURL(new RegExp(`/artifacts/${slug}$`));
  await expect(page.locator(".artifact-workspace h1")).toBeVisible({
    timeout: 20_000,
  });
}

test("Slice 5 exposes all seven editable artifacts and preserves a versioned edit", async ({
  page,
}) => {
  await createAnalyzedProject(page);

  const artifacts = [
    ["Intent", "intent"],
    ["Context", "context"],
    ["Scope", "scope"],
    ["Requirements", "requirements"],
    ["Work Breakdown", "work_breakdown"],
    ["Schedule", "schedule"],
    ["Resources", "resources"],
  ];
  for (const [name, slug] of artifacts) {
    await openArtifact(page, name, slug);
    await expect(page.locator(".artifact-workspace h1")).toBeVisible();
    await expect(page.getByText("Editable", { exact: true })).toBeVisible();
    await expect(page.getByText(/^v\d+$/)).toBeVisible();
  }

  await openArtifact(page, "Scope", "scope");
  await expect(page.locator(".artifact-workspace h1")).toBeVisible();
  await expect(page.getByText("Up to date", { exact: true })).toBeVisible({
    timeout: 120_000,
  });
  const editableParagraphs = page.locator(".artifact-copy");
  const target = editableParagraphs.last();
  const original = await target.innerText();
  const marker = ` Confirmed in Slice 5 E2E ${Date.now()}.`;
  await target.click();
  await target.evaluate((element) => {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(element);
    range.collapse(false);
    selection?.removeAllRanges();
    selection?.addRange(range);
  });
  await target.type(marker.slice(0, 1));
  await expect(target).toBeFocused();
  await target.type(marker.slice(1), { delay: 5 });
  await expect(target).toBeFocused();
  await expect(target).toContainText(`${original}${marker}`);
  await expect(page.getByText("Changes not applied")).toBeVisible();
  await target.hover();
  await expect(
    target.locator("xpath=..").getByText("Confirmed by you", { exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Apply changes" }).click();
  await expect(page.getByText("Reanalyzing…")).toBeVisible({ timeout: 20_000 });

  await page.reload();
  await expect(page.getByText(marker.trim(), { exact: false })).toBeVisible();
  const editedSection = page.locator(".artifact-section").filter({
    hasText: marker.trim(),
  });
  await editedSection.hover();
  await expect(
    editedSection.getByText("Confirmed by you", { exact: true }),
  ).toBeVisible();
  await expect(page.getByText(/^v[2-9]\d*$/)).toBeVisible();
  await expect(page.getByText("Up to date")).toBeVisible({ timeout: 90_000 });
});

test("Slice 5 issue annotations expose an honest evidence state and artifact controls", async ({
  page,
}) => {
  await createAnalyzedProject(page);
  const overviewUrl = page.url();
  await page.goto(overviewUrl.replace(/\/overview$/, "/history"));
  await expect(page.getByText("Extended Analysis complete", { exact: true }).first()).toBeVisible({
    timeout: 120_000,
  });
  await page.goto(overviewUrl);

  const countedArtifactLink = page
    .getByRole("link")
    .filter({ has: page.locator(".nav-count") })
    .filter({ hasText: /Intent|Context|Scope|Requirements|Work Breakdown|Schedule|Resources/ })
    .first();
  if (await countedArtifactLink.isVisible()) {
    await countedArtifactLink.click();
  } else {
    await openArtifact(page, "Resources", "resources");
  }

  await expect(page.getByRole("button", { name: "Previous issue" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Next issue" })).toBeVisible();
  await page.getByRole("button", { name: "Find in artifact" }).click();
  await expect(page.getByPlaceholder("Find in this artifact…")).toBeVisible();

  const inlineIssue = page.locator(".artifact-inline-issue").first();
  await expect(inlineIssue).toBeVisible();
  await inlineIssue.click();
  const dialog = page.getByRole("dialog", { name: "Issue details" });
  await expect(dialog).toBeVisible();
  const evidence = dialog.getByRole("button", { name: /^Evidence/ });
  await expect(evidence).toBeVisible();
  await expect(evidence).toHaveAttribute("aria-expanded", "false");
  await evidence.click();
  await expect(evidence).toHaveAttribute("aria-expanded", "true");
  await expect(
    dialog
      .getByText(/Readable evidence details are not available/)
      .or(dialog.getByText("Project description", { exact: true })),
  ).toBeVisible();
  await expect(dialog.getByText(/document:.*fragment:/)).toHaveCount(0);
  await expect(dialog.getByRole("textbox", { name: "Clarification answer" })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Submit & re-analyze" })).toBeDisabled();
});

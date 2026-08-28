import type { APIRequestContext } from "@playwright/test";
import { expect, test } from "../fixtures";

async function signInAsOwner(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  for (let attempt = 0; attempt < 3; attempt += 1) {
    await page.getByRole("button", { name: "Sign in" }).click();
    try {
      await page.waitForURL(/\/admin\/invitations/, { timeout: 15_000 });
      return;
    } catch {
      if (attempt === 2) throw new Error("Local E2E admin sign-in did not recover");
    }
  }
}

async function completeOrientationTour(page: import("@playwright/test").Page) {
  const dialog = page.getByRole("dialog", { name: "How OSLO works" });
  await dialog.waitFor({ state: "visible", timeout: 2_000 }).catch(() => undefined);
  if (!(await dialog.isVisible())) return;
  for (let step = 0; step < 10; step += 1) {
    const next = dialog.getByRole("button", { name: "Next", exact: true });
    if (!(await next.isVisible())) break;
    await next.click();
  }
  await dialog.getByRole("button", { name: "Done", exact: true }).click();
  await expect(dialog).toHaveCount(0);
}

async function activationMessageFor(
  request: APIRequestContext,
  email: string,
  excludedMessageId?: string,
) {
  let messageId: string | undefined;
  await expect
    .poll(async () => {
      const response = await request.get("http://127.0.0.1:55324/api/v1/messages");
      const payload = await response.json();
      const message = payload.messages.find(
        (candidate: { ID: string; To: Array<{ Address: string }> }) =>
          candidate.ID !== excludedMessageId
          && candidate.To.some((recipient) => recipient.Address === email),
      );
      messageId = message?.ID;
      return Boolean(messageId);
    })
    .toBe(true);
  const response = await request.get(`http://127.0.0.1:55324/api/v1/message/${messageId}`);
  const message = await response.json();
  const activationUrl = String(message.Text).match(
    /http:\/\/(?:localhost|127\.0\.0\.1):\d+\/activate\?token=\S+/,
  )?.[0];
  expect(activationUrl).toBeTruthy();
  return { messageId: messageId!, activationUrl: activationUrl! };
}

test("Owner invite to activated member intake", async ({ browser, page, request }, testInfo) => {
  test.setTimeout(300_000);
  if (testInfo.project.name !== "desktop") {
    await signInAsOwner(page);
    await expect(page.getByLabel("Email address")).toBeVisible();
    await expect(page.getByRole("button", { name: "Send invitation" })).toBeVisible();
    return;
  }
  const unique = Date.now();
  const email = `slice-one-${testInfo.project.name}-${unique}@example.com`;
  const password = "SliceOneMember123!";

  await signInAsOwner(page);

  await page.getByLabel("Email address").fill(email);
  await page.getByRole("button", { name: "Send invitation" }).click();
  await expect(page.getByText(`Invitation sent to ${email}`)).toBeVisible();

  const { activationUrl } = await activationMessageFor(request, email);

  const recipient = await browser.newPage();
  await recipient.goto(activationUrl!.replace("localhost", "127.0.0.1"));
  await expect(recipient.getByLabel("Email (from your invite)")).toHaveValue(email);
  await expect(recipient.getByLabel("Email (from your invite)")).toHaveAttribute("readonly", "");
  await recipient.getByLabel("Display name").fill("Slice One Member");
  await recipient.getByLabel("Choose a password").fill(password);
  for (let attempt = 0; attempt < 2; attempt += 1) {
    await recipient.getByRole("button", { name: "Create account & continue" }).click();
    try {
      await recipient.waitForURL(/\/welcome$/, { timeout: 30_000 });
      break;
    } catch {
      if (attempt === 1) throw new Error("Invitation activation did not recover");
    }
  }
  await expect(recipient.getByRole("heading", {
    name: /Welcome to (?:OSLO|Intralign), Slice One Member\./,
  })).toBeVisible();
  await expect(recipient.getByText(/OSLO advises; you decide/)).toBeVisible();
  await recipient.getByRole("button", { name: /Start your first (?:outcome|project)/i }).click();
  await expect(recipient).toHaveURL(/\/intake\?project=/);
  await expect(recipient.getByRole("heading", {
    name: /Optimize your plan for the outcome you.re after|See your plan like a strategic leader/i,
  })).toBeVisible();
  await expect(recipient.getByText(/OSLO advises; you decide/)).toBeVisible();
  await expect(recipient.getByRole("button", { name: /Get my analysis|See where I stand/i })).toBeDisabled();
  await recipient.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
  await recipient.keyboard.press("Tab");
  await expect(recipient.getByLabel("Describe your project")).toBeFocused();

  const sessionCookies = await recipient.context().cookies();
  expect(sessionCookies.find((cookie) => cookie.name === "oslo_session_lifetime")?.value).toBe("2592000");
  await recipient.reload();
  await expect(recipient).toHaveURL(/\/intake\?project=/);

  await recipient.getByRole("button", { name: /sample (?:plan|project)/i }).click();
  await expect(recipient.getByLabel("Describe your project")).toHaveValue(/DevNorth/);
  await expect(recipient.getByRole("button", { name: /Get my analysis|See where I stand/i })).toBeEnabled();
  await expect(recipient.getByRole("heading", { name: "Understanding is forming" })).toHaveCount(0);
  await recipient.emulateMedia({ reducedMotion: "reduce" });
  await recipient.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
  await expect(recipient).toHaveURL(/\/projects\/.+\/(analysis\/.+|overview)/, {
    timeout: 120_000,
  });
  if (recipient.url().includes("/analysis/")) {
    const skipIntro = recipient.getByRole("button", { name: /Skip the intro/i });
    await skipIntro.waitFor({ state: "visible", timeout: 10_000 }).catch(() => undefined);
    if (await skipIntro.isVisible()) await skipIntro.click();
    const confirmOutcome = recipient
      .frameLocator('iframe[title="OSLO analysis and outcome confirmation"]')
      .getByRole("button", { name: /Yes.+this is my outcome/i });
    await expect(confirmOutcome).toBeVisible({ timeout: 120_000 });
    await confirmOutcome.click();
  }
  await expect(recipient).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
  const firstReadDecision = recipient.getByRole("button", { name: /verified this directly/i });
  if (await firstReadDecision.isVisible()) {
    const actResponse = recipient.waitForResponse(
      (response) => response.request().method() === "POST" && /\/issues\/.+\/acts$/.test(response.url()),
    );
    await firstReadDecision.click();
    expect((await actResponse).ok()).toBeTruthy();
    await recipient.reload();
    await expect(recipient.locator(".project-shell")).not.toHaveClass(
      /is-first-run-frozen/,
      { timeout: 30_000 },
    );
    const closeIssue = recipient.getByRole("button", { name: "Close issue" });
    if (await closeIssue.isVisible()) await closeIssue.click();
  }
  await completeOrientationTour(recipient);
  if (!(await recipient.locator(".confidence-read").isVisible())) {
    await recipient.getByRole("button", { name: "Expand Outcome Integrity" }).click();
  }
  await expect(recipient.locator(".confidence-read")).toBeVisible();
  await expect(
    recipient.locator(".confidence-read").getByText("Outcome integrity", { exact: true }),
  ).toBeVisible();
  await expect(recipient.locator(".project-advisory")).toContainText(
    "OSLO advises; you decide",
  );

  await recipient.locator(".project-account summary").click();
  await recipient
    .locator(".project-account-menu")
    .getByRole("button", { name: "Take a quick tour", exact: true })
    .click();
  await completeOrientationTour(recipient);
  const account = recipient.locator(".project-account");
  if (!(await account.evaluate((element) => (element as HTMLDetailsElement).open))) {
    await recipient.locator(".project-account summary").click();
  }
  await recipient.getByRole("button", { name: "Log out" }).click();
  await expect(recipient).toHaveURL(/\/login/);
  await expect(recipient.getByRole("heading", { name: "Sign in to OSLO" })).toBeVisible();
  await recipient.close();
});

test("Existing account signs in from a new invitation", async ({ browser, page, request }, testInfo) => {
  if (testInfo.project.name !== "desktop") {
    await signInAsOwner(page);
    await expect(page.getByRole("heading", { name: "Invitations", exact: true })).toBeVisible();
    return;
  }
  const email = "e2e-existing@example.com";
  const password = "ExistingMember123!";
  await signInAsOwner(page);

  await page.getByLabel("Email address").fill(email);
  await page.getByRole("button", { name: "Send invitation" }).click();
  await expect(page.getByText(`Invitation sent to ${email}`)).toBeVisible();
  const message = await activationMessageFor(request, email);

  const existingMember = await browser.newPage();
  await existingMember.goto(message.activationUrl.replace("localhost", "127.0.0.1"));
  await expect(existingMember.getByRole("heading", { name: "Sign in to accept your invitation" })).toBeVisible();
  await existingMember.getByRole("link", { name: /Sign in & continue/ }).click();
  await expect(existingMember.getByLabel("Email")).toHaveValue(email);
  await expect(existingMember.getByLabel("Email")).toHaveAttribute("readonly", "");
  await existingMember.getByLabel("Password").fill(password);
  await existingMember.getByRole("button", { name: "Sign in" }).click();
  await existingMember.waitForURL(/\/(?:welcome|intake)(?:\?.*)?$/);
  const welcome = existingMember.getByRole("button", {
    name: /Start your first (?:outcome|project)/i,
  });
  if (await welcome.isVisible()) {
    await welcome.click();
  }
  await expect(existingMember).toHaveURL(/\/intake(?:\?project=.+)?$/);

  await existingMember.close();
});

test("Alpha routes reject anonymous access and invalid invitation links", async ({ browser }, testInfo) => {
  const anonymous = await browser.newPage();
  await anonymous.goto("/intake");
  await expect(anonymous).toHaveURL(/\/login/);

  await anonymous.goto(`/activate?token=modified-${testInfo.project.name}-${Date.now()}`);
  await expect(anonymous.getByRole("heading", { name: "This link can’t be used" })).toBeVisible();
  await anonymous.close();
});

test("Owner can resend and revoke a pending invitation", async ({ page }, testInfo) => {
  if (testInfo.project.name !== "desktop") {
    await signInAsOwner(page);
    await expect(page.getByText("Invitations", { exact: true })).toBeVisible();
    return;
  }
  const email = `invitation-actions-${testInfo.project.name}-${Date.now()}@example.com`;
  await signInAsOwner(page);
  await page.getByLabel("Email address").fill(email);
  await page.getByRole("button", { name: "Send invitation" }).click();
  await expect(page.getByText(`Invitation sent to ${email}`)).toBeVisible();

  let pendingRow = page
    .locator("article.invitation-row")
    .filter({ hasText: email })
    .filter({ hasText: "pending" });
  await pendingRow.getByRole("button", { name: "Resend" }).click();
  await expect(page.getByText("Invitation resent.")).toBeVisible();

  pendingRow = page
    .locator("article.invitation-row")
    .filter({ hasText: email })
    .filter({ hasText: "pending" });
  await pendingRow.getByRole("button", { name: "Revoke" }).click();
  await expect(page.getByText("Invitation revoked.")).toBeVisible();
  await expect(
    page
      .locator("article.invitation-row")
      .filter({ hasText: email })
      .filter({ hasText: "pending" }),
  ).toHaveCount(0);
});

import { expect, test, type APIRequestContext } from "@playwright/test";

async function signInAsOwner(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/admin\/invitations/);
}

async function completeOrientationTour(page: import("@playwright/test").Page) {
  await expect(page.getByRole("dialog", { name: "How OSLO works" })).toBeVisible();
  await page.getByRole("button", { name: "Get started" }).click();
  for (let step = 0; step < 4; step += 1) {
    await page.getByRole("button", { name: "Next", exact: true }).click();
  }
  await page.getByRole("button", { name: "Finish tour" }).click();
  await expect(page.getByRole("dialog", { name: "How OSLO works" })).toHaveCount(0);
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
  const activationUrl = String(message.Text).match(/http:\/\/localhost:3000\/activate\?token=\S+/)?.[0];
  expect(activationUrl).toBeTruthy();
  return { messageId: messageId!, activationUrl: activationUrl! };
}

test("Owner invite to activated member intake", async ({ browser, page, request }, testInfo) => {
  test.setTimeout(90_000);
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
  await recipient.getByLabel("Confirm password").fill(password);
  await recipient.getByRole("button", { name: "Create account & continue" }).click();
  await expect(recipient.getByRole("heading", { name: "Welcome to OSLO, Slice One Member." })).toBeVisible();
  await expect(recipient.getByText(/OSLO advises; you decide/)).toBeVisible();
  await recipient.getByRole("button", { name: "Start your first project" }).click();
  await expect(recipient).toHaveURL(/\/intake\?project=/);
  await expect(recipient.getByRole("heading", { name: "See your plan like a strategic leader." })).toBeVisible();
  await expect(recipient.getByText(/OSLO advises; you decide/)).toBeVisible();
  await expect(recipient.getByRole("button", { name: "See where I stand" })).toBeDisabled();
  await recipient.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
  await recipient.keyboard.press("Tab");
  await expect(recipient.getByLabel("Describe your project")).toBeFocused();

  const sessionCookies = await recipient.context().cookies();
  expect(sessionCookies.find((cookie) => cookie.name === "oslo_session_lifetime")?.value).toBe("2592000");
  await recipient.reload();
  await expect(recipient).toHaveURL(/\/intake\?project=/);

  await recipient.getByRole("button", { name: /sample project/i }).click();
  await expect(recipient.getByLabel("Describe your project")).toHaveValue(/DevNorth/);
  await expect(recipient.getByRole("button", { name: /See where I stand/ })).toBeEnabled();
  await expect(recipient.getByRole("heading", { name: "Understanding is forming" })).toHaveCount(0);
  await recipient.emulateMedia({ reducedMotion: "reduce" });
  await recipient.getByRole("button", { name: /See where I stand/ }).click();
  await expect(recipient).toHaveURL(/\/projects\/.+\/(analysis\/.+|overview)/);
  if (recipient.url().includes("/analysis/")) {
    await expect(recipient.locator(".analysis-scanner")).toHaveCSS("animation-name", "none");
  }
  await expect(recipient).toHaveURL(/\/projects\/.+\/overview/, { timeout: 65_000 });
  await expect(recipient.getByRole("heading", { name: "Understanding is forming" })).toBeVisible();
  await completeOrientationTour(recipient);
  await expect(recipient.locator(".project-advisory")).toContainText(
    "OSLO advises; you decide",
  );

  await recipient.locator(".project-account summary").click();
  await recipient.getByRole("button", { name: "How OSLO works" }).click();
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
  const email = `existing-${testInfo.project.name}-${Date.now()}@example.com`;
  const password = "ExistingMember123!";
  await signInAsOwner(page);

  await page.getByLabel("Email address").fill(email);
  await page.getByRole("button", { name: "Send invitation" }).click();
  const firstMessage = await activationMessageFor(request, email);

  const newMember = await browser.newPage();
  await newMember.goto(firstMessage.activationUrl.replace("localhost", "127.0.0.1"));
  await newMember.getByLabel("Display name").fill("Existing Member");
  await newMember.getByLabel("Choose a password").fill(password);
  await newMember.getByLabel("Confirm password").fill(password);
  await newMember.getByRole("button", { name: "Create account & continue" }).click();
  await expect(newMember.getByRole("heading", { name: "Welcome to OSLO, Existing Member." })).toBeVisible();

  await page.getByLabel("Email address").fill(email);
  await page.getByRole("button", { name: "Send invitation" }).click();
  const secondMessage = await activationMessageFor(request, email, firstMessage.messageId);

  const existingMember = await browser.newPage();
  await existingMember.goto(secondMessage.activationUrl.replace("localhost", "127.0.0.1"));
  await expect(existingMember.getByRole("heading", { name: "Sign in to accept your invitation" })).toBeVisible();
  await existingMember.getByRole("link", { name: /Sign in & continue/ }).click();
  await expect(existingMember.getByLabel("Email")).toHaveValue(email);
  await expect(existingMember.getByLabel("Email")).toHaveAttribute("readonly", "");
  await existingMember.getByLabel("Password").fill(password);
  await existingMember.getByRole("button", { name: "Sign in" }).click();
  await existingMember.waitForURL(/\/(?:welcome|intake)(?:\?.*)?$/);
  const welcome = existingMember.getByRole("button", { name: "Start your first project" });
  if (await welcome.isVisible()) {
    await welcome.click();
  }
  await expect(existingMember).toHaveURL(/\/intake(?:\?project=.+)?$/);

  await newMember.close();
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

import { expect, test } from "@playwright/test";

test.setTimeout(120_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@oslo.local");
  await page.getByLabel("Password").fill("OsloLocalAdmin123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/admin\/invitations/, { timeout: 20_000 });
}

test("Slice 8 provides workspace home, switching, awareness, settings, and safe capacity choices", async ({
  page,
}) => {
  await signIn(page);
  await page.goto("/workspace");

  await expect(page.getByRole("heading", { name: "OSLO Product Grill" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Active projects" })).toBeVisible();
  await expect(page.getByLabel("Search active projects")).toBeVisible();
  await expect(page.getByLabel("Notifications")).toBeVisible();
  await expect(page.getByLabel("Settings")).toBeVisible();
  await expect(page.getByRole("button", { name: /Archived projects/ })).toBeVisible();

  const analyzedProjects = page.locator('a[href^="/projects/"][href$="/overview"]');
  if (await analyzedProjects.count() === 0) {
    await page.getByRole("button", { name: /Create your first project/ }).click();
    await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
    await page.getByRole("button", { name: /sample project/i }).click();
    await page.getByRole("button", { name: /See where I stand/ }).click();
    await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
    await page.goto("/workspace");
  }

  const projectLink = page.locator('a[href^="/projects/"][href$="/overview"]').first();
  await expect(projectLink).toBeVisible();
  const projectHref = await projectLink.getAttribute("href");
  expect(projectHref).toMatch(/^\/projects\/.+\/overview$/);
  await page.goto(projectHref!);

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Get started" }).click();
    await orientation.getByRole("button", { name: "Skip tour" }).click();
    await expect(orientation).toBeHidden();
  }

  const switcher = page.getByTitle("Switch project");
  await expect(switcher).toBeVisible();
  await switcher.click();
  await expect(page.getByRole("menuitem", { name: /Workspace Home/ })).toBeVisible();
  await expect(page.getByRole("menuitem", { name: /New project/ })).toBeVisible();
  await page.keyboard.press("Escape");

  await page.getByLabel("Notifications").click();
  const notifications = page.getByRole("dialog", { name: "Notifications" });
  await expect(notifications).toBeVisible();
  await expect(notifications.getByText("Workspace awareness")).toBeVisible();
  await expect(notifications.getByText(/Awareness only/)).toBeVisible();
  const markAllRead = notifications.getByRole("button", { name: "Mark all read" });
  if (await markAllRead.isEnabled()) {
    await markAllRead.click();
    await expect(markAllRead).toBeDisabled();
  }
  await notifications.getByLabel("Notification settings").click();
  await expect(page).toHaveURL(/\/settings#notifications$/);

  await expect(page.getByRole("heading", { name: "Account & workspace" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Settings" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Appearance" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Notifications" })).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Workspace", exact: true }),
  ).toBeVisible();
  await expect(page.getByRole("heading", { name: "Subscription" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Dark" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Light" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Match system" })).toBeVisible();

  await page.goto("/workspace");
  while (await page.getByRole("link", { name: /Open project/ }).count() < 3) {
    await page.getByRole("button", { name: "New project" }).click();
    await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
    await page.goto("/workspace");
  }
  await page.getByRole("button", { name: "New project" }).click();
  await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
});

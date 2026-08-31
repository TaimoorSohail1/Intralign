import { expect, test } from "../fixtures";
import { unlockFirstRead } from "../helpers";

test.setTimeout(120_000);

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/(workspace|welcome)/, { timeout: 60_000 });
}

test("Prototype Slice 8 provides a coherent workspace, awareness, settings, and capacity flow", async ({
  page,
}) => {
  await signIn(page);
  await page.goto("/workspace");

  await expect(page.getByRole("heading", { name: "Your project" })).toBeVisible();
  await expect(page.getByText("Pick up where understanding stands.")).toBeVisible();
  await expect(page.getByRole("button", { name: "New project" })).toBeVisible();
  await expect(page.getByText(/No portfolio score across plans/)).toBeVisible();

  let projectLink = page.getByRole("link", { name: /Open the project/ });
  if (await projectLink.count() === 0) {
    await page.getByRole("button", { name: "New project" }).click();
    await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
    await page.getByRole("button", { name: /sample (?:project|plan)/i }).click();
    await page.getByRole("button", { name: /Get my analysis|See where I stand/i }).click();
    await page.waitForURL(/\/projects\/[^/]+\/(?:analysis\/[^/]+|overview)/, { timeout: 120_000 });
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
    await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
    await page.goto("/workspace");
    projectLink = page.getByRole("link", { name: /Open the project/ });
  }

  const projectHref = await projectLink.getAttribute("href");
  expect(projectHref).toMatch(/^\/projects\/.+\/overview$/);
  await page.goto(projectHref!);

  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  await orientation.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
  if (await orientation.isVisible()) await orientation.getByRole("button", { name: "Skip", exact: true }).click();

  await unlockFirstRead(page);

  const switcher = page.getByTitle("Switch project");
  await switcher.click();
  const menu = page.getByRole("menu");
  await expect(menu.getByRole("menuitem", { name: /Workspace Home/ })).toBeVisible();
  await expect(menu.getByRole("menuitem", { name: /New project/ })).toBeVisible();
  const currentItems = menu.getByRole("menuitem", { name: /current/i });
  const currentHrefs = await currentItems.evaluateAll((items) => items.map((item) => item.getAttribute("href")));
  expect(new Set(currentHrefs).size).toBe(currentHrefs.length);
  await switcher.press("ArrowDown");
  await expect(currentItems.first()).toBeFocused();
  await page.keyboard.press("Escape");
  await expect(switcher).toBeFocused();

  await page.getByLabel("Notifications").click();
  const notifications = page.getByRole("dialog", { name: "Notifications" });
  await expect(notifications).toBeVisible();
  await expect(notifications.getByText(/durable record, not alerts/).first()).toBeVisible();
  await expect(notifications.getByText(/routine changes never interrupt you/)).toBeVisible();
  await expect(notifications.getByRole("button", { name: "Mark all read" })).toHaveCount(0);
  await notifications.getByLabel("Close notifications").click();

  await page.goto("/settings");
  const settings = page.getByRole("dialog", { name: "Settings" });
  await expect(settings).toBeVisible();
  await expect(settings.getByRole("navigation", { name: "Settings" }).getByRole("button")).toHaveCount(10);
  await settings.getByRole("button", { name: "Appearance", exact: true }).click();
  await expect(settings.getByRole("heading", { name: "Appearance" })).toBeVisible();
  await settings.getByRole("button", { name: "Light" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect.poll(() => page.locator(".project-shell").evaluate((element) => getComputedStyle(element).backgroundColor)).toBe("rgb(251, 250, 247)");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await expect.poll(() => page.locator(".project-shell").evaluate((element) => getComputedStyle(element).backgroundColor)).toBe("rgb(251, 250, 247)");
  await page.goto("/settings");
  const reloadedSettings = page.getByRole("dialog", { name: "Settings" });
  await expect(reloadedSettings).toBeVisible();
  await reloadedSettings.getByRole("button", { name: "Appearance", exact: true }).click();
  await reloadedSettings.getByRole("button", { name: "Dark" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await reloadedSettings.getByRole("button", { name: "Collaboration", exact: true }).click();
  await expect(reloadedSettings.getByRole("heading", { name: "Collaboration" })).toBeVisible();
  await reloadedSettings.getByRole("button", { name: "Access & invites", exact: true }).click();
  await expect(reloadedSettings.getByRole("heading", { name: "Access & invites" })).toBeVisible();
  await reloadedSettings.getByRole("button", { name: /Manage invitations/ }).click();
  await expect(reloadedSettings.getByRole("heading", { name: "Workspace invitations" })).toBeVisible();
  await expect(page).toHaveURL(/\/projects\/.+\/overview/);
  await reloadedSettings.getByRole("button", { name: "Membership", exact: false }).click();
  await expect(reloadedSettings.getByRole("heading", { name: /Membership/ })).toBeVisible();
  await reloadedSettings.getByRole("button", { name: /Manage access & invitations/ }).click();
  await expect(reloadedSettings.getByRole("heading", { name: "Workspace invitations" })).toBeVisible();
  await reloadedSettings.getByRole("button", { name: "Plan & usage", exact: true }).click();
  await reloadedSettings.getByRole("button", { name: "Free vs Basic" }).click();
  await page.getByRole("dialog", { name: "Your plan" }).getByRole("button", { name: "Close plans" }).click();
  await expect(reloadedSettings).toBeVisible();
  await reloadedSettings.getByRole("button", { name: "Close settings" }).click();

  await page.goto("/workspace");
  for (let attempt = 0; attempt < 4; attempt += 1) {
    await page.getByRole("button", { name: "New project", exact: true }).click();
    const capacity = page.getByRole("dialog", { name: /Run more than one plan|Start another project/ });
    await capacity.waitFor({ state: "visible", timeout: 3_000 }).catch(() => undefined);
    if (await capacity.isVisible()) {
      await expect(capacity.getByRole("button", { name: /Upgrade your plan/ })).toBeVisible();
      await expect(capacity.getByRole("button", { name: /Archive .* to free the slot/ })).toBeVisible();
      await capacity.getByRole("button", { name: /Upgrade your plan/ }).click();
      await expect(page.getByRole("dialog", { name: "Your plan" })).toBeVisible();
      await page.getByRole("button", { name: "Close plans" }).click();
      break;
    }
    await expect(page).toHaveURL(/\/intake\?project=/, { timeout: 30_000 });
    await page.goto("/workspace");
  }
  await expect(page).toHaveURL(/\/workspace$/);
});

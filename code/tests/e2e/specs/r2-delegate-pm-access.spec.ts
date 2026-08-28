import { execFileSync } from "node:child_process";
import path from "node:path";

import { expect, test } from "../fixtures";

const ASSIGNED_PROJECT_ID = "018f9f7e-8de2-7000-8000-000000000021";
const UNASSIGNED_PROJECT_ID = "018f9f7e-8de2-7000-8000-000000000022";

test("Delegate-PM access is project-scoped and owner controls stay unavailable", async ({
  page,
}, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "One authenticated security measurement is sufficient.");

  const repositoryRoot = path.resolve(__dirname, "../..", "..");
  execFileSync(
    "uv",
    [
      "run",
      "--project",
      "services/api",
      "python",
      "services/api/scripts/seed_delegate_e2e.py",
    ],
    { cwd: repositoryRoot, stdio: "inherit" },
  );

  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-delegate@example.com");
  await page.getByLabel("Password").fill("E2EDelegate123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL(/\/workspace$/, { timeout: 60_000 });

  await expect(page.getByRole("heading", { name: "Delegate assignment" })).toBeVisible();
  await expect(page.getByText("Owner-only project", { exact: true })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "New project" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Create a new project" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Archive Delegate assignment" })).toHaveCount(0);

  const assigned = await page.request.get(
    `/api/projects/${ASSIGNED_PROJECT_ID}/collaboration`,
  );
  expect(assigned.status()).toBe(200);
  expect((await assigned.json()).actor_role).toBe("delegate_pm");

  const unassigned = await page.request.get(
    `/api/projects/${UNASSIGNED_PROJECT_ID}/collaboration`,
  );
  expect(unassigned.status()).toBe(403);

  const createProject = await page.request.post("/api/projects/new");
  expect(createProject.status()).toBe(403);

  await page.goto(`/projects/${UNASSIGNED_PROJECT_ID}/overview`);
  await page.waitForURL(/\/workspace$/, { timeout: 60_000 });
  await expect(page.getByRole("heading", { name: "Delegate assignment" })).toBeVisible();

  await page.goto(`/projects/${ASSIGNED_PROJECT_ID}/overview`);
  await page.waitForURL(
    new RegExp(`/intake\\?project=${ASSIGNED_PROJECT_ID}$`),
    { timeout: 60_000 },
  );
  await expect(
    page.getByRole("heading", { name: /Optimize your plan for the outcome/i }),
  ).toBeVisible();

  await page.goto("/settings");
  const settings = page.getByRole("navigation", { name: "Settings" });
  await expect(settings.getByRole("button", { name: "Profile" })).toBeVisible();
  await expect(settings.getByRole("button", { name: "Appearance" })).toBeVisible();
  await expect(settings.getByRole("button", { name: "Notifications" })).toBeVisible();
  await expect(settings.getByRole("button", { name: "Workspace" })).toHaveCount(0);
  await expect(settings.getByRole("button", { name: "Access & invites" })).toHaveCount(0);
  await expect(settings.getByRole("button", { name: "Plan & usage" })).toHaveCount(0);
});

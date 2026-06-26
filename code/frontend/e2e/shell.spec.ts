import { test, expect } from "@playwright/test";

// DTM-0019 smoke: the app shell renders and the global nav is present.
test("app shell renders with the global nav", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("app-shell")).toBeVisible();
  // The wordmark + the primary nav rail (UI spec §2 IA).
  await expect(page.getByRole("heading", { name: "OSLO" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
  // The global group is always present (Projects / Notifications / Settings).
  const globalNav = page.getByTestId("nav-global");
  await expect(globalNav.getByText("Projects")).toBeVisible();
  await expect(globalNav.getByText("Notifications")).toBeVisible();
  await expect(globalNav.getByText("Settings")).toBeVisible();
  // The default (Projects/Dashboard) surface resolves.
  await expect(page.getByTestId("surface-title")).toHaveText("Projects");
});

// DTM-0042 — on the Dashboard the project-context group is HIDDEN; instead an
// "open a project" hint shows. Reports/Shared are NOT in the nav (Category-E).
test("Dashboard: no project-context group; no Category-E / Recommendations entries", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByTestId("nav-project")).toHaveCount(0);
  await expect(page.getByTestId("nav-project-hint")).toBeVisible();
  // Honest Category-E handling: no Reports / Shared Artifacts nav entry.
  await expect(page.getByRole("navigation").getByText("Reports")).toHaveCount(0);
  await expect(
    page.getByRole("navigation").getByText("Shared Artifacts"),
  ).toHaveCount(0);
  // RP-C1: no standalone Recommendations nav entry.
  await expect(
    page.getByRole("navigation").getByText("Recommendations"),
  ).toHaveCount(0);
  // Settings is shown but disabled ("Not in Release 1"), never a dead-end.
  await expect(page.getByTestId("nav-deferred")).toContainText("Settings");
  await expect(page.getByTestId("nav-deferred")).toContainText("Not in Release 1");
});

// DTM-0042 — the project-context group is active-project-aware. Navigating under a
// project surfaces the project nav with links to that project's BUILT surfaces, and
// clicking Findings lands on the Issue Cards surface (NOT a "Surface pending" stub).
test("project context: nav appears and Findings opens Issue Cards (not a placeholder)", async ({
  page,
}) => {
  const pid = "proj-e2e-001";
  await page.goto(`/projects/${pid}`);
  const projectNav = page.getByTestId("nav-project");
  await expect(projectNav).toBeVisible();
  // Each link targets the ACTIVE project.
  await expect(projectNav.getByRole("link", { name: "Workspace" })).toHaveAttribute(
    "href",
    `/projects/${pid}`,
  );
  await expect(projectNav.getByRole("link", { name: "Findings" })).toHaveAttribute(
    "href",
    `/projects/${pid}/findings`,
  );
  // RP-C1: no Recommendations link in the project nav.
  await expect(projectNav.getByText("Recommendations")).toHaveCount(0);

  // Click Findings → the real Issue Cards surface resolves.
  await projectNav.getByRole("link", { name: "Findings" }).click();
  await expect(page).toHaveURL(new RegExp(`/projects/${pid}/findings$`));
  await expect(page.getByTestId("surface-title")).toHaveText("Issues");
  // NEGATIVE: never the leftover DTM-0019 "Surface pending" placeholder.
  await expect(page.getByText("Surface pending")).toHaveCount(0);
});

// `/settings` is a deferred (Category-E) stub — reachable by direct URL but marked
// honestly; it is never a silent dead-end in the nav (asserted above).
test("the /settings route resolves to the deferred User Settings stub", async ({
  page,
}) => {
  await page.goto("/settings");
  await expect(page.getByTestId("surface-title")).toHaveText("User Settings");
});

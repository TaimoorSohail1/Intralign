import { test, expect } from "@playwright/test";

// DTM-0024 Dashboard + Project Overview happy-path. The backend REST is unbuilt
// (DTM-0018 is additive but no projection data is served in this environment), so
// the project/confidence/CAF/findings/recommendations hooks resolve to
// loading/empty — both surfaces must still render their shell cleanly (never crash)
// and show clean, positive empty/not-yet-available states.

test("Dashboard mounts at the landing route", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("dashboard")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Projects/);
});

test("Project Overview mounts at the project orientation route", async ({ page }) => {
  await page.goto("/projects/demo-project/orientation");
  await expect(page.getByTestId("project-overview")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Project overview/i);
  // the aggregate sections + counts are present (counts read 0 with no data, not an error)
  await expect(page.getByTestId("overview-confidence")).toBeVisible();
  await expect(page.getByTestId("overview-caf")).toBeVisible();
  await expect(page.getByTestId("overview-counts")).toBeVisible();
});

// NEGATIVE (the Disclose spine): the Dashboard + Overview present, never generate —
// no edit / score / accept / generate affordance on either surface.
for (const [name, path] of [
  ["Dashboard", "/"],
  ["Project Overview", "/projects/demo-project/orientation"],
] as const) {
  test(`${name} exposes no edit/score/accept/generate control`, async ({ page }) => {
    await page.goto(path);
    const forbidden =
      /\bedit\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
    for (const role of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
      const controls = page.getByRole(role);
      const count = await controls.count();
      for (let i = 0; i < count; i++) {
        const text = ((await controls.nth(i).textContent()) ?? "").trim();
        expect(text).not.toMatch(forbidden);
      }
    }
  });

  test(`${name} never reads as project health / readiness / probability`, async ({
    page,
  }) => {
    await page.goto(path);
    const body = ((await page.locator("body").textContent()) ?? "").toLowerCase();
    expect(body).not.toMatch(/\bhealth\b/);
    expect(body).not.toMatch(/\breadiness\b/);
    expect(body).not.toMatch(/\bon[- ]?track\b/);
  });
}

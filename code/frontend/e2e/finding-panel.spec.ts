import { test, expect } from "@playwright/test";

// DTM-0021 Finding Panel happy-path: the panel mounts at the Finding-detail route.
// The backend REST is unbuilt (DTM-0018 is additive but no projection data is
// served in this environment), so the `useGetFinding…` hook resolves to
// loading/not-found — the panel must still render its shell cleanly (never crash)
// and surface the RP-C1 affordance into the nested recommendations route.
test("Finding Panel mounts at the finding-detail route", async ({ page }) => {
  await page.goto("/projects/demo-project/findings/demo-finding");

  await expect(page.getByTestId("finding-panel")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Finding/);
});

// RP-C1: the only path to recommendations is the affordance here, and it routes to
// the nested recommendations route (never an inline render). When finding data is
// present the affordance shows; with no data the panel shows a clean not-found
// state. Either way, NO inline recommendation list is rendered on the panel.
test("Finding Panel renders no inline recommendation list (RP-C1)", async ({ page }) => {
  await page.goto("/projects/demo-project/findings/demo-finding");
  await expect(page.getByTestId("finding-panel")).toBeVisible();
  await expect(page.getByTestId("recommendation-list")).toHaveCount(0);
  await expect(page.getByTestId("recommendation-item")).toHaveCount(0);
});

// NEGATIVE (the Disclose spine): the Finding Panel presents, never generates —
// no edit / accept / reject / resolve / generate affordance on the surface.
test("Finding Panel exposes no edit/accept/resolve/generate control", async ({ page }) => {
  await page.goto("/projects/demo-project/findings/demo-finding");
  await expect(page.getByTestId("finding-panel")).toBeVisible();

  const forbidden =
    /\bedit\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

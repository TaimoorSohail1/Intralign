import { test, expect } from "@playwright/test";

// DTM-0023 Issue Cards happy-path: the surface mounts at the project findings
// route. The backend REST is unbuilt (DTM-0018 is additive but no projection data
// is served in this environment), so the `useListFindings…` hook resolves to
// loading/empty — the surface must still render its shell cleanly (never crash)
// and show a clean, positive empty state.
test("Issue Cards mount at the project findings route", async ({ page }) => {
  await page.goto("/projects/demo-project/findings");

  await expect(page.getByTestId("issue-cards")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Issues/);
});

// NEGATIVE (the Disclose spine): Issue Cards present, never generate — no edit /
// score / accept / defer / prioritise / generate affordance on the surface.
test("Issue Cards expose no edit/score/accept/generate control", async ({ page }) => {
  await page.goto("/projects/demo-project/findings");
  await expect(page.getByTestId("issue-cards")).toBeVisible();

  const forbidden =
    /\bedit\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bprioriti[sz]e\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

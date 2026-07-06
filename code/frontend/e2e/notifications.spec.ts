import { test, expect } from "@playwright/test";

// DTM-0026 Notification / Awareness happy-path: the surface mounts at the
// top-level `/notifications` route. The backend REST is unbuilt in this
// environment (DTM-0018 is additive but serves no projection data), so the reads
// resolve to loading/empty — the surface must still render its shell cleanly
// (never crash) and show a clean, positive "all caught up" empty state.
test("Notification / Awareness mounts at /notifications", async ({ page }) => {
  await page.goto("/notifications");

  await expect(page.getByTestId("notifications")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Awareness/);
});

// NEGATIVE (the Disclose spine + the Category-E boundary): the awareness surface
// presents, never generates — and read/dismiss is platform state, not a governed
// action. There must be no generate / score / accept / resolve / approve / govern /
// reanalyze control on the surface.
test("Notification / Awareness exposes no generate/score/accept/resolve/govern control", async ({
  page,
}) => {
  await page.goto("/notifications");
  await expect(page.getByTestId("notifications")).toBeVisible();

  const forbidden =
    /\bgenerate\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e|run analysis|\bapply\b|\bassign\b/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

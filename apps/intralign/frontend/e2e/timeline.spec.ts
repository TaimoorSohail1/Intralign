import { test, expect } from "@playwright/test";

// DTM-0027 History / Timeline happy-path: the surface mounts at the project-scoped
// `/projects/$projectId/history` route. The backend REST is unbuilt in this
// environment (DTM-0018 is additive but serves no projection data), so the three
// reads (analysis runs / acceptances / plan facts) resolve to loading/empty — the
// surface must still render its shell cleanly (never crash) and show a clean
// "no history yet" empty state.
test("History / Timeline mounts at /projects/:id/history", async ({ page }) => {
  await page.goto("/projects/proj-001/history");

  await expect(page.getByTestId("timeline")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/History/);
});

// NEGATIVE (the Disclose spine + the append-only history boundary): the History
// surface presents, never generates, and is append-only — it hosts NO structured
// actions. There must be no edit / accept / generate / delete / restore / rollback /
// approve / govern / reanalyze control on the surface (spec §D, §J; HT-6/HT-12).
test("History / Timeline exposes no edit/accept/generate/restore/rollback/govern control", async ({
  page,
}) => {
  await page.goto("/projects/proj-001/history");
  await expect(page.getByTestId("timeline")).toBeVisible();

  const forbidden =
    /\bedit\b|\baccept\b|\breject\b|\bdefer\b|\bgenerate\b|\bdelete\b|\brestore\b|\brollback\b|roll back|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e|reanalyze|reanalyse|\bapply\b|\bscore\b|\bresolve\b/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

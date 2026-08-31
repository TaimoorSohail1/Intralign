import { test, expect } from "@playwright/test";

// DTM-0028 Export / Share-out happy-path: the surface mounts at the project-scoped
// `/projects/$projectId/export` route. The backend REST is unbuilt in this environment
// (DTM-0018 is additive but serves no projection data), so the eight reads resolve to
// loading/empty — the surface must still render its shell cleanly (never crash) and
// show a clean "nothing to export" empty state. The mandatory disclaimer / packaging
// affordances appear once there is understanding to package; with no data the surface
// presents the empty state honestly (it fabricates nothing).
test("Export / Share mounts at /projects/:id/export", async ({ page }) => {
  await page.goto("/projects/proj-001/export");

  await expect(page.getByTestId("export-surface")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Export/);
});

// NEGATIVE (the Disclose spine): Export PRESENTS, NEVER GENERATES. There must be no
// generate / score / accept / reject / defer / edit / govern / reanalyze control on the
// surface (spec §Q intentionally-absent; EX-1..EX-5). Only packaging/share affordances
// (download/copy) are allowed.
test("Export / Share exposes no generate/score/accept/edit/govern/reanalyze control", async ({
  page,
}) => {
  await page.goto("/projects/proj-001/export");
  await expect(page.getByTestId("export-surface")).toBeVisible();

  const forbidden =
    /\bgenerate\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bedit\b|\bgovern\b|\bapprove\b|recompute|re-?analy[sz]e|reanalyze|reanalyse|\bapply\b|\bresolve\b|\bdelete\b|\brollback\b/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

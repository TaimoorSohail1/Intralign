import { test, expect } from "@playwright/test";

// DTM-0022 Recommendation Panel happy-path: the panel mounts at the NESTED
// recommendations route, under a Finding (RP-C1). The backend REST is unbuilt
// (DTM-0018 is additive but no projection data is served in this environment), so
// the `useListRecommendationsForFinding…` hook resolves to loading/empty — the
// panel must still render its shell cleanly (never crash).
test("Recommendation Panel mounts at the nested (under-finding) recommendations route", async ({
  page,
}) => {
  await page.goto("/projects/demo-project/findings/demo-finding/recommendations");

  await expect(page.getByTestId("recommendation-panel")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Recommendations/);
});

// RP-C1 NEGATIVE: a STANDALONE Recommendation Panel is a rejected negative. The
// top-level `/recommendations` route is NOT the Recommendation Panel — it never
// renders the panel's recommendation content. The Recommendation Panel exists ONLY
// nested under a Finding.
test("Recommendation Panel does not render as a standalone destination (RP-C1)", async ({
  page,
}) => {
  await page.goto("/recommendations");
  // No Recommendation Panel surface, no recommendation items, no resolution paths
  // at the standalone top-level route.
  await expect(page.getByTestId("recommendation-panel")).toHaveCount(0);
  await expect(page.getByTestId("recommendation-item")).toHaveCount(0);
  await expect(page.getByTestId("resolution-paths")).toHaveCount(0);
});

// NEGATIVE (the Disclose spine — Disclose NEVER accepts/generates): the panel
// presents the accept/reject/defer affordance but exposes NO generate / score /
// recompute / resolve-finding / govern / approve / execute / apply control.
test("Recommendation Panel exposes no generate/score/recompute/govern control", async ({
  page,
}) => {
  await page.goto("/projects/demo-project/findings/demo-finding/recommendations");
  await expect(page.getByTestId("recommendation-panel")).toBeVisible();

  const forbidden =
    /\bgenerate\b|\bscore\b|recompute|re-?analy[sz]e|run analysis|resolve finding|\bgovern\b|\bapprove\b|\bexecute\b|run agent|automate/i;
  for (const name of ["button", "menuitem", "checkbox", "switch", "radio"] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

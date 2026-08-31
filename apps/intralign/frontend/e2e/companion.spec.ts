import { test, expect } from "@playwright/test";

// DTM-0025 Understanding Companion happy-path. The backend REST is unbuilt (DTM-0018
// is additive but no projection data is served in this environment), so the
// confidence / CAF / findings / recommendations / analysis-runs hooks resolve to
// loading/empty — the surface must still render its shell cleanly (never crash) and
// show clean, positive empty/not-yet-available states.
test("Companion mounts at the project companion route", async ({ page }) => {
  await page.goto("/projects/demo-project/companion");
  await expect(page.getByTestId("companion")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Understanding companion/i);
  await expect(page.getByTestId("companion-confidence")).toBeVisible();
  await expect(page.getByTestId("companion-caf")).toBeVisible();
  await expect(page.getByTestId("companion-findings")).toBeVisible();
  await expect(page.getByTestId("companion-recommendations")).toBeVisible();
  await expect(page.getByTestId("ask-oslo")).toBeVisible();
});

// NEGATIVE — Option B / RP-C1: the Companion never routes directly to a standalone
// Recommendation route. With no data there are no recommendation rows, so assert the
// invariant structurally: no anchor on the surface targets a `/recommendations`
// route, and there is no standalone-recommendation affordance.
test("Companion never hrefs a /recommendations route directly (Option B / RP-C1)", async ({
  page,
}) => {
  await page.goto("/projects/demo-project/companion");
  await expect(page.getByTestId("companion")).toBeVisible();
  // Scope to the Companion surface itself — the global app-shell nav is out of scope.
  const anchors = page.getByTestId("companion").locator("a[href]");
  const count = await anchors.count();
  for (let i = 0; i < count; i++) {
    const href = (await anchors.nth(i).getAttribute("href")) ?? "";
    expect(href).not.toMatch(/\/recommendations(\/|$)/);
  }
});

// NEGATIVE (the Disclose spine): the Companion presents, never generates — no
// edit / score / accept / generate affordance on the surface.
test("Companion exposes no edit/score/accept/generate control", async ({ page }) => {
  await page.goto("/projects/demo-project/companion");
  await expect(page.getByTestId("companion")).toBeVisible();
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

// NEGATIVE: never reads as project health / readiness / probability.
test("Companion never reads as project health / readiness / probability", async ({
  page,
}) => {
  await page.goto("/projects/demo-project/companion");
  await expect(page.getByTestId("companion")).toBeVisible();
  const body = ((await page.locator("body").textContent()) ?? "").toLowerCase();
  expect(body).not.toMatch(/\bhealth\b/);
  expect(body).not.toMatch(/\breadiness\b/);
  expect(body).not.toMatch(/\bprobability\b/);
  expect(body).not.toMatch(/\bon[- ]?track\b/);
});

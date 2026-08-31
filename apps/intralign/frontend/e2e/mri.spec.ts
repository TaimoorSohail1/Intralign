import { test, expect } from "@playwright/test";

// DTM-0020 MRI happy-path: the MRI umbrella surface mounts at the Project
// Workspace route. The backend REST is unbuilt (DTM-0018 is additive but no
// projection data is served in this environment), so the read hooks resolve to
// loading/empty — the surface must still render its shell + sub-component
// scaffolding cleanly (never crash). We assert the surface and its four DL-047
// sub-components are present.
test("MRI surface mounts at the project workspace route", async ({ page }) => {
  await page.goto("/projects/demo-project");

  // The umbrella surface and its heading render.
  await expect(page.getByTestId("mri-surface")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Understanding \(MRI\)/);

  // All four DL-047 sub-components are mounted (MRI-04…07).
  await expect(page.getByTestId("mri-heatmap")).toBeVisible();
  await expect(page.getByTestId("mri-caf-triangle")).toBeVisible();
  await expect(page.getByTestId("mri-timeline")).toBeVisible();
  await expect(page.getByTestId("mri-dependencies")).toBeVisible();
});

// NEGATIVE (the Disclose spine): MRI presents, never generates — there is no
// compute / recompute / score / accept / generate affordance on the surface.
test("MRI exposes no compute/recompute/accept control", async ({ page }) => {
  await page.goto("/projects/demo-project");
  await expect(page.getByTestId("mri-surface")).toBeVisible();

  const forbidden =
    /recompute|re-?analy[sz]e|\bcompute\b|\bscore\b|\baccept\b|\breject\b|\bapprove\b|\bgenerate\b|run analysis|\bapply\b/i;
  for (const name of [
    "button",
    "menuitem",
    "checkbox",
    "switch",
    "radio",
  ] as const) {
    const controls = page.getByRole(name);
    const count = await controls.count();
    for (let i = 0; i < count; i++) {
      const text = ((await controls.nth(i).textContent()) ?? "").trim();
      expect(text).not.toMatch(forbidden);
    }
  }
});

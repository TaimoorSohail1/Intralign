import { test, expect } from "@playwright/test";

// DTM-0029 Assisted Editing / Persistent Intelligence (AW-04/05). The backend REST is
// unbuilt, so the confidence/CAF/runs reads resolve to loading/empty — the always-visible
// panel must still render cleanly and route assists. It needs the project context via the
// `project_id` search param.
test("Artifact Editor mounts the always-visible Persistent-Intelligence panel", async ({
  page,
}) => {
  await page.goto("/artifacts/artf-1?project_id=demo-project&finding_id=f-1");
  await expect(page.getByTestId("artifact-editor")).toBeVisible();
  await expect(page.getByTestId("assisted-editing")).toBeVisible();
  await expect(page.getByTestId("ae-confidence")).toBeVisible();
  await expect(page.getByTestId("ae-caf")).toBeVisible();
  await expect(page.getByTestId("ae-understanding-state")).toBeVisible();
});

// The panel ROUTES assists — to Chat (B1) and to the Suggested Fix via its Finding (B3) —
// performing none. The affordances are routing links, not cognition controls.
test("Assisted-Editing routes assists to Chat (B1) and Suggested Fix via Finding (B3)", async ({
  page,
}) => {
  await page.goto("/artifacts/artf-1?project_id=demo-project&finding_id=f-1");
  await expect(page.getByTestId("assisted-editing")).toBeVisible();

  const chatLink = page.getByTestId("ae-route-chat");
  const chatHref = (await chatLink.getAttribute("href")) ?? "";
  expect(chatHref.startsWith("/projects/demo-project/chat")).toBeTruthy();

  const fixLink = page.getByTestId("ae-route-suggested-fix");
  await expect(fixLink).toHaveAttribute("href", "/projects/demo-project/findings/f-1");
  // B3 routes via the Finding (RP-C1) — never a standalone recommendation route.
  expect((await fixLink.getAttribute("href")) ?? "").not.toMatch(/\/recommendations(\/|$)/);
});

// DL-048 honest-limit disclosure — when the run is scope/budget-limited, the truthful
// partial disclosure renders on this same surface WITH the reason, and the upgrade prompt
// appears ALONGSIDE it, never INSTEAD OF it.
test("Honest-limit disclosure renders truthfully with the upgrade prompt ALONGSIDE", async ({
  page,
}) => {
  await page.goto("/artifacts/artf-1?project_id=demo-project&limited=true");
  const root = page.getByTestId("honest-limit");
  await expect(root).toBeVisible();
  // The honest disclosure is present (partial + reason)…
  await expect(page.getByTestId("honest-limit-disclosure")).toBeVisible();
  await expect(page.getByTestId("honest-limit-disclosure")).toContainText(/partial/i);
  await expect(page.getByTestId("honest-limit-reason")).toContainText(/exceeds the/i);
  // …and the upgrade prompt is ALONGSIDE it (both on the same surface), never instead.
  await expect(page.getByTestId("honest-limit-upgrade")).toBeVisible();
  // NEGATIVE: never presents the limited result as complete/final.
  const text = ((await root.textContent()) ?? "").toLowerCase();
  expect(text).not.toMatch(/\bcomplete analysis\b|\bfull analysis\b|\bfinal analysis\b/);
});

// NEGATIVE: when NOT limited, no partial disclosure is fabricated.
test("Honest-limit disclosure is absent when the run is not limited", async ({ page }) => {
  await page.goto("/artifacts/artf-1?project_id=demo-project");
  await expect(page.getByTestId("artifact-editor")).toBeVisible();
  await expect(page.getByTestId("honest-limit")).toHaveCount(0);
});

// NEGATIVE: the panel performs no cognition — no generate/score/accept/apply control.
test("Assisted-Editing exposes no generate / score / accept / apply control", async ({
  page,
}) => {
  await page.goto("/artifacts/artf-1?project_id=demo-project&finding_id=f-1");
  await expect(page.getByTestId("assisted-editing")).toBeVisible();
  const forbidden =
    /\bgenerate\b|\bscore\b|\baccept\b|\bapply\b|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e/i;
  const buttons = page.getByTestId("assisted-editing").getByRole("button");
  const count = await buttons.count();
  for (let i = 0; i < count; i++) {
    const text = ((await buttons.nth(i).textContent()) ?? "").trim();
    expect(text).not.toMatch(forbidden);
  }
});

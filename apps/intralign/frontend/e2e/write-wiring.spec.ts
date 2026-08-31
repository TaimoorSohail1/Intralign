import { test, expect } from "@playwright/test";

// DTM-0039 — frontend write-wiring happy-paths. Each Wave E surface affordance now calls
// its real command endpoint (TanStack useMutation). The dev server has no backend, so we
// STUB the reads (to populate the surface) and the command endpoints (to complete the
// flow) with Playwright route interception, and assert the command POST is the path.

const json = (body: unknown) => ({
  status: 200,
  contentType: "application/json",
  body: JSON.stringify(body),
});

// ── Recommendation Panel: Accept calls POST …:accept (the command records the UAR) ──
test("Recommendation Panel accept calls the accept command (Disclose never accepts locally)", async ({
  page,
}) => {
  const recommendation = {
    recommendation_id: "rec-1",
    project_id: "demo-project",
    finding_id: "demo-finding",
    title: "Confirm the go-live date with both stakeholders",
    recommendation_type: "validation",
    status: "generated",
    label: {
      epistemic_label: "derived",
      confidence_band: "medium",
      confidence_value: 55,
      conflict_state: "none",
      current_chr_ref: "chr-1",
    },
  };

  await page.route(/\/v1\/findings\/[^/]+\/recommendations(\?.*)?$/, (route) =>
    route.fulfill(json([recommendation])),
  );

  let acceptHit = false;
  await page.route(/\/v1\/recommendations\/[^/]+:accept$/, (route) => {
    acceptHit = true;
    return route.fulfill(json({ ...recommendation, status: "accepted" }));
  });

  await page.goto("/projects/demo-project/findings/demo-finding/recommendations");
  await expect(page.getByTestId("recommendation-panel")).toBeVisible();
  await page.getByTestId("affordance-accept").first().click();

  await expect.poll(() => acceptHit).toBe(true);

  // The SURFACE never flips the status locally — the card's status stays what the
  // governed read returned (the command, not the surface, records acceptance).
  await expect(page.getByTestId("recommendation-item-rec-1")).toHaveAttribute(
    "data-status",
    "generated",
  );
});

// ── Notifications: Dismiss calls POST …:dismiss (platform-state command) ─────────────
test("Notification dismiss calls the dismiss command (platform-state, non-canonical)", async ({
  page,
}) => {
  const notification = {
    notification_id: "ntf-1",
    project_id: "demo-project",
    source_object_type: "finding",
    source_object_id: "demo-finding",
    state: "created",
    created_at: "2026-06-01T10:00:00Z",
    dismissed_at: null,
    viewed_at: null,
  };

  await page.route(/\/v1\/notifications(\?.*)?$/, (route) => route.fulfill(json([notification])));

  let dismissHit = false;
  await page.route(/\/v1\/notifications\/[^/]+:dismiss$/, (route) => {
    dismissHit = true;
    return route.fulfill(json({ ...notification, state: "dismissed" }));
  });

  await page.goto("/notifications");
  await expect(page.getByTestId("notifications")).toBeVisible();
  await expect(page.getByTestId("notification-item")).toBeVisible();
  await page.getByTestId("dismiss-notification").first().click();

  await expect.poll(() => dismissHit).toBe(true);
});

// ── Dashboard create project + Overview trigger analysis (user-initiated commands) ──
test("Dashboard create project calls POST /projects", async ({ page }) => {
  await page.route(/\/v1\/projects$/, (route) => {
    if (route.request().method() === "POST") {
      return route.fulfill(
        json({
          project_id: "demo-new",
          workspace_id: "ws-1",
          title: "Atlas v2 migration",
          lifecycle_state: "created",
        }),
      );
    }
    return route.fulfill(json([]));
  });

  await page.goto("/");
  await expect(page.getByTestId("dashboard")).toBeVisible();

  let createHit = false;
  page.on("request", (req) => {
    if (req.method() === "POST" && /\/v1\/projects$/.test(req.url())) createHit = true;
  });

  await page.getByTestId("create-project-title").fill("Atlas v2 migration");
  await page.getByTestId("create-project-submit").click();
  await expect.poll(() => createHit).toBe(true);
});

test("Project Overview Start Fast Pass calls POST …/analysis-runs:fast", async ({ page }) => {
  // Stub the overview read so the surface renders; then assert the trigger command fires.
  await page.route(/\/v1\/projects\/[^/]+\/overview$/, (route) =>
    route.fulfill(json({ project_id: "demo-project", counts: [] })),
  );

  let fastHit = false;
  await page.route(/\/v1\/projects\/[^/]+\/analysis-runs:fast$/, (route) => {
    fastHit = true;
    return route.fulfill(
      json({
        analysis_run_id: "run-new",
        project_id: "demo-project",
        run_type: "fast_analysis_pass",
        run_status: "queued",
      }),
    );
  });

  await page.goto("/projects/demo-project/orientation");
  await expect(page.getByTestId("project-overview")).toBeVisible();
  await page.getByTestId("trigger-fast").click();
  await expect.poll(() => fastHit).toBe(true);
});

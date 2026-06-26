import { test, expect } from "@playwright/test";

// DTM-0029 OSLO Chat happy-path + the CRITICAL no-canonical-write negative. The backend
// REST is unbuilt (DTM-0018 is additive, no projection data served here), but Chat does
// not depend on any read for its core conversation UI — it renders the transcript, input,
// and Explain/Clarify/Improve affordances regardless, and writes nothing.
test("Chat mounts at the project chat route with input + affordances", async ({ page }) => {
  await page.goto("/projects/demo-project/chat");
  await expect(page.getByTestId("chat")).toBeVisible();
  await expect(page.getByTestId("surface-title")).toHaveText(/Ask OSLO/i);
  await expect(page.getByTestId("chat-input")).toBeVisible();
  await expect(page.getByTestId("chat-affordance-explain")).toBeVisible();
  await expect(page.getByTestId("chat-affordance-clarify")).toBeVisible();
  await expect(page.getByTestId("chat-affordance-improve")).toBeVisible();
});

// Context inheritance — launched from a Finding, Chat pre-scopes to it (read-only) and
// offers a contextual handoff into the Finding Panel.
test("Chat inherits a Finding context from the URL and offers the Finding Panel handoff", async ({
  page,
}) => {
  await page.goto(
    "/projects/demo-project/chat?context_kind=finding&context_id=f-1&context_label=Conflict",
  );
  const ctx = page.getByTestId("chat-context");
  await expect(ctx).toHaveAttribute("data-context-kind", "finding");
  await expect(ctx).toHaveAttribute("data-context-id", "f-1");
  await expect(page.getByTestId("chat-open-finding")).toHaveAttribute(
    "href",
    "/projects/demo-project/findings/f-1",
  );
});

// HAPPY-PATH + CRITICAL NEGATIVE (DTM-0039) — sending goes THROUGH the chat ENDPOINT
// (the non-canonical chat path). The ONLY write is `POST …/chat`; no canonical-write or
// governed-object mutation endpoint is hit, and the surface never claims an
// applied/accepted/resolved/saved change. The endpoint is stubbed so the flow completes.
test("Chat send goes through the chat endpoint (non-canonical) — no canonical write", async ({
  page,
}) => {
  const mutating: string[] = [];
  page.on("request", (req) => {
    const method = req.method();
    if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
      mutating.push(`${method} ${req.url()}`);
    }
  });

  // Stub the chat endpoint: it returns a NON-CANONICAL ChatExchange (OSLO's phrasing).
  await page.route(/\/v1\/projects\/[^/]+\/chat$/, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        exchange_id: "ex-srv-1",
        project_id: "demo-project",
        user_message: "Accept this recommendation",
        response: "OSLO explains from existing understanding; nothing changed.",
        intent: "explain",
        epistemic_state: "non-canonical",
        model_or_rule_version: "e2e",
        triggered_run: null,
      }),
    });
  });

  await page.goto("/projects/demo-project/chat");
  await expect(page.getByTestId("chat")).toBeVisible();

  await page.getByTestId("chat-input").getByRole("textbox").fill("Accept this recommendation");
  await page.getByTestId("chat-send").click();

  // The user message + OSLO's phrased response render in the transcript.
  await expect(page.getByTestId("chat-transcript")).toContainText(/accept this recommendation/i);
  await expect(page.getByTestId("chat-transcript")).toContainText(/oslo explains from existing/i);

  // The ONLY mutating request is the chat endpoint — no canonical-write / governed
  // mutation (accept / finding / notification / analysis) endpoint was hit.
  const nonChat = mutating.filter((m) => !/\/v1\/projects\/[^/]+\/chat$/.test(m));
  expect(nonChat, `unexpected non-chat mutating requests: ${nonChat.join(", ")}`).toHaveLength(0);
  expect(mutating.some((m) => /\/chat$/.test(m))).toBe(true);

  // The surface never claims an applied/accepted/resolved/saved change.
  const text = (await page.getByTestId("chat").textContent()) ?? "";
  expect(text).not.toMatch(/\bapplied\b|\baccepted\b|\bresolved\b|\bsaved\b|\bapproved\b/i);
});

// NEGATIVE (the Disclose spine): Chat exposes no accept/approve/govern/ratify control.
test("Chat exposes no accept / approve / govern control", async ({ page }) => {
  await page.goto("/projects/demo-project/chat");
  await expect(page.getByTestId("chat")).toBeVisible();
  const forbidden = /\baccept\b|\bapprove\b|\bgovern\b|\bratif/i;
  const buttons = page.getByRole("button");
  const count = await buttons.count();
  for (let i = 0; i < count; i++) {
    const text = ((await buttons.nth(i).textContent()) ?? "").trim();
    expect(text).not.toMatch(forbidden);
  }
});

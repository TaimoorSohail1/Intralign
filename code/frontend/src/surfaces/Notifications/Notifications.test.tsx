/**
 * DTM-0026 — Notification / Awareness (IC-WE-DISCLOSE E1).
 *
 * Presents Outcome-Drift / Acceptance-Impact alerts ("a decision you confirmed is
 * affected") + new emissions as AWARENESS, and routes each to its source context.
 * It PRESENTS, NEVER GENERATES — no generate/score/accept/resolve control.
 *
 * THE CRITICAL NEGATIVE (the spine of this slice): read/unread/dismiss is
 * **platform state (Category E), NON-canonical**. Marking a notification read or
 * dismissing it writes NO canonical, changes NO assessment, promotes nothing, and
 * does NOT resolve the underlying drift. The underlying governed alert object is
 * unchanged by dismiss. Acceptance-Impact is Derived and is NEVER shown as
 * settled or auto-resolved.
 *
 * The two DTM-0018 reads are mocked with fixture DTOs:
 *   - `useListNotifications…` (workspace-level platform state, NO label)
 *   - `useListAcceptanceImpact…` (project-scoped Derived drift, carries a label)
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderNotifications } from "./testHarness";
import {
  notificationsFixture,
  acceptanceImpactFixture,
  unreadFindingNotification,
  unreadCommentNotification,
  readAnalysisNotification,
  bandChangeImpactFixture,
  magnitudeImpactFixture,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the two DTM-0018 reads (the surface consumes, never re-implements) ──────
const notificationsState = {
  data: { data: notificationsFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};
const impactState = {
  data: { data: acceptanceImpactFixture },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../api/generated/notifications/notifications", () => ({
  useListNotificationsV1NotificationsGet: () => notificationsState,
}));
vi.mock("../../api/generated/acceptance/acceptance", () => ({
  useListAcceptanceImpactV1ProjectsProjectIdAcceptanceImpactGet: () => impactState,
}));

// Imported AFTER the mocks are declared (vi.mock is hoisted).
import { Notifications } from "./Notifications";

function mount(projectId: string | undefined = PROJECT_ID) {
  return renderNotifications(<Notifications projectId={projectId} />);
}

beforeEach(() => {
  notificationsState.isLoading = false;
  notificationsState.isError = false;
  notificationsState.error = null;
  notificationsState.data = { data: notificationsFixture };
  impactState.isLoading = false;
  impactState.isError = false;
  impactState.error = null;
  impactState.data = { data: acceptanceImpactFixture };
});

// ── POSITIVE: presents drift + Acceptance-Impact + new emissions as awareness ────
describe("Notifications — presents awareness (drift + Acceptance-Impact + emissions)", () => {
  it("renders one awareness item per notification", async () => {
    await mount();
    const surface = screen.getByTestId("notifications");
    const items = within(surface).getAllByTestId("notification-item");
    expect(items.length).toBe(notificationsFixture.length);
  });

  it("renders Acceptance-Impact alerts as 'a decision you confirmed is affected'", async () => {
    await mount();
    const surface = screen.getByTestId("notifications");
    const alerts = within(surface).getAllByTestId("acceptance-impact-alert");
    expect(alerts.length).toBe(acceptanceImpactFixture.length);
    // the canonical framing copy is present
    expect(
      within(surface).getAllByText(/a decision you confirmed is affected/i).length,
    ).toBeGreaterThan(0);
  });

  it("each Acceptance-Impact alert carries a Derived label (banded, never settled)", async () => {
    await mount();
    const alerts = screen.getAllByTestId("acceptance-impact-alert");
    for (const alert of alerts) {
      const label = within(alert).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(within(alert).getByTestId("confidence-band")).toBeInTheDocument();
    }
  });

  it("surfaces the conflict marker on a contested Acceptance-Impact (presented, not resolved)", async () => {
    await mount();
    const alerts = screen.getAllByTestId("acceptance-impact-alert");
    // magnitudeImpactFixture is contested → conflict marker; bandChange is not
    const contested = alerts.find((a) =>
      a.getAttribute("data-uar-ref") === magnitudeImpactFixture.uar_ref,
    )!;
    const clean = alerts.find((a) =>
      a.getAttribute("data-uar-ref") === bandChangeImpactFixture.uar_ref,
    )!;
    expect(within(contested).getByTestId("conflict-marker")).toBeInTheDocument();
    expect(within(clean).queryByTestId("conflict-marker")).not.toBeInTheDocument();
  });

  it("an unread notification shows an unread cue; a read one does not", async () => {
    await mount();
    const unread = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadFindingNotification.notification_id)!;
    const read = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === readAnalysisNotification.notification_id)!;
    expect(unread).toHaveAttribute("data-read", "false");
    expect(read).toHaveAttribute("data-read", "true");
  });

  it("a notification routes to its source context (open source link present)", async () => {
    await mount();
    const item = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadFindingNotification.notification_id)!;
    const link = within(item).getByTestId("open-source");
    expect(link).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${unreadFindingNotification.source_object_id}`,
    );
  });
});

// ── Read/dismiss = PLATFORM state (non-canonical) ────────────────────────────────
describe("Notifications — read/dismiss is platform state (a Category-E affordance)", () => {
  it("exposes a dismiss affordance as a platform action", async () => {
    await mount();
    const item = screen.getAllByTestId("notification-item")[0];
    expect(within(item).getByTestId("dismiss-notification")).toBeInTheDocument();
  });

  it("exposes a mark-read affordance as a platform action on an unread item", async () => {
    await mount();
    const unread = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadCommentNotification.notification_id)!;
    expect(within(unread).getByTestId("mark-read")).toBeInTheDocument();
  });

  it("marking read flips the LOCAL unread cue only (a presentation convenience)", async () => {
    await mount();
    let unread = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadCommentNotification.notification_id)!;
    expect(unread).toHaveAttribute("data-read", "false");
    fireEvent.click(within(unread).getByTestId("mark-read"));
    unread = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadCommentNotification.notification_id)!;
    expect(unread).toHaveAttribute("data-read", "true");
  });

  it("dismissing removes the item from the local feed (a presentation convenience)", async () => {
    await mount();
    const before = screen.getAllByTestId("notification-item").length;
    const item = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadFindingNotification.notification_id)!;
    fireEvent.click(within(item).getByTestId("dismiss-notification"));
    const after = screen.queryAllByTestId("notification-item").length;
    expect(after).toBe(before - 1);
    expect(
      screen
        .queryAllByTestId("notification-item")
        .some((n) => n.getAttribute("data-notification-id") === unreadFindingNotification.notification_id),
    ).toBe(false);
  });
});

// ── Loading / empty states ───────────────────────────────────────────────────────
describe("Notifications — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    notificationsState.isLoading = true;
    notificationsState.data = undefined as never;
    impactState.isLoading = true;
    impactState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("notifications")).toBeInTheDocument();
    expect(screen.getByTestId("notifications-loading")).toBeInTheDocument();
  });

  it("renders a clean, positive 'all caught up' empty state when there is nothing", async () => {
    notificationsState.data = { data: [] };
    impactState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("notifications")).toBeInTheDocument();
    expect(screen.getByTestId("notifications-empty")).toBeInTheDocument();
  });

  it("renders notifications even with no project scope (acceptance-impact read skipped)", async () => {
    impactState.data = { data: [] };
    await mount(undefined);
    const surface = screen.getByTestId("notifications");
    expect(within(surface).getAllByTestId("notification-item").length).toBe(
      notificationsFixture.length,
    );
  });
});

// ── THE CRITICAL NEGATIVES (fail review if absent) ───────────────────────────────
describe("Notifications — NEGATIVES: presents, never generates; state is non-canonical", () => {
  it("exposes NO generate / score / accept / resolve / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
    ];
    const forbidden =
      /\bgenerate\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|recompute|re-?analy[sz]e|run analysis|\bapply\b|reanalyze|reanalyse|\bassign\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("no Acceptance-Impact alert ever renders as settled / resolved / auto-resolved", async () => {
    await mount();
    const surface = screen.getByTestId("notifications");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bresolved\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/auto-?resolved/i)).not.toBeInTheDocument();
    for (const alert of within(surface).getAllByTestId("acceptance-impact-alert")) {
      const label = within(alert).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("CRITICAL: dismiss is LOCAL platform state — it does NOT mutate the governed notification object", async () => {
    // Snapshot the governed object identity + fields BEFORE the platform action.
    const before = JSON.parse(JSON.stringify(unreadFindingNotification));
    await mount();
    const item = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadFindingNotification.notification_id)!;
    fireEvent.click(within(item).getByTestId("dismiss-notification"));
    // The governed DTO object the surface was handed is byte-for-byte unchanged:
    // dismiss wrote no canonical, mutated no governed field (state stays `created`).
    expect(unreadFindingNotification).toEqual(before);
    expect(unreadFindingNotification.state).toBe("created");
    expect(unreadFindingNotification.dismissed_at).toBeNull();
  });

  it("CRITICAL: mark-read is LOCAL platform state — it does NOT mutate the governed notification object", async () => {
    const before = JSON.parse(JSON.stringify(unreadCommentNotification));
    await mount();
    const item = screen
      .getAllByTestId("notification-item")
      .find((n) => n.getAttribute("data-notification-id") === unreadCommentNotification.notification_id)!;
    fireEvent.click(within(item).getByTestId("mark-read"));
    expect(unreadCommentNotification).toEqual(before);
    expect(unreadCommentNotification.state).toBe("created");
    expect(unreadCommentNotification.viewed_at).toBeNull();
  });

  it("CRITICAL: dismissing a drift/impact-linked notification does NOT resolve the Acceptance-Impact", async () => {
    await mount();
    const impactBefore = screen.getAllByTestId("acceptance-impact-alert").length;
    // dismiss a notification…
    const item = screen.getAllByTestId("notification-item")[0];
    fireEvent.click(within(item).getByTestId("dismiss-notification"));
    // …the Derived Acceptance-Impact alerts are untouched (still surfaced, not resolved)
    const impactAfter = screen.getAllByTestId("acceptance-impact-alert").length;
    expect(impactAfter).toBe(impactBefore);
    expect(
      screen.getAllByText(/a decision you confirmed is affected/i).length,
    ).toBeGreaterThan(0);
  });

  it("notification state never reads as completion / approval / work / assessment status", async () => {
    await mount();
    const surface = screen.getByTestId("notifications");
    // read/unread must not imply governed status
    expect(within(surface).queryByText(/\bcompleted\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bapproved\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bdone\b/i)).not.toBeInTheDocument();
  });
});

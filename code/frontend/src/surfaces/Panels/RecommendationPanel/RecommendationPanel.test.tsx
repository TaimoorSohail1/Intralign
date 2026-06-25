/**
 * DTM-0022 — the Recommendation Panel (IC-WE-DISCLOSE E1; RP-C1).
 *
 * Presents the Recommendations anchored to ONE Finding, grouping multiple
 * alternatives as "Resolution Paths" (a PRESENTATION grouping — never an object),
 * each with its epistemic label + DL-055 state, and renders the accept/reject/defer
 * AFFORDANCE. It PRESENTS, NEVER GENERATES, and — critically — NEVER ACCEPTS: the
 * affordance hands off to the EXISTING Wave U capture; the panel mutates no state
 * and writes nothing.
 *
 * The DTM-0018 generated `useListRecommendationsForFinding…` hook is mocked with
 * fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderRecommendationPanel } from "./testHarness";
import {
  recommendationsForFinding,
  singleRecommendationForFinding,
  primaryRecommendationFixture,
  alternativeRecommendationFixture,
  PROJECT_ID,
  FINDING_ID,
} from "./fixtures";

// ── Mock the DTM-0018 recommendations-for-finding hook (consume, never re-build) ──
const recState = {
  data: { data: recommendationsForFinding },
  isLoading: false,
  isError: false,
  error: null as unknown,
};

vi.mock("../../../api/generated/recommendations/recommendations", () => ({
  useListRecommendationsForFindingV1FindingsFindingIdRecommendationsGet: () => recState,
}));

// Imported AFTER the mock is declared (vi.mock is hoisted).
import { RecommendationPanel } from "./RecommendationPanel";

function mount(findingId: string | undefined = FINDING_ID, inFindingContext = true) {
  // NOTE: when a test calls `mount(undefined, …)` the JS default re-applies
  // FINDING_ID; the no-context case is driven by `inFindingContext: false`, which
  // mounts the panel with `findingId={undefined}` explicitly.
  const componentFindingId = inFindingContext ? findingId : undefined;
  return renderRecommendationPanel(
    <RecommendationPanel projectId={PROJECT_ID} findingId={componentFindingId} />,
    { projectId: PROJECT_ID, findingId: findingId ?? FINDING_ID, inFindingContext },
  );
}

beforeEach(() => {
  recState.isLoading = false;
  recState.isError = false;
  recState.error = null;
  recState.data = { data: recommendationsForFinding };
});

describe("RecommendationPanel — presents the finding's recommendations", () => {
  it("renders a recommendation for the finding, each with its DL-055 state", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const items = within(panel).getAllByTestId("recommendation-item");
    expect(items.length).toBe(recommendationsForFinding.length);
    // each item surfaces its DL-055 status (read from the governed source as-is)
    const states = items.map((el) => el.getAttribute("data-status"));
    expect(states).toContain("generated");
    expect(states).toContain("deferred");
    expect(states).toContain("accepted");
    // the user-facing status is shown
    expect(within(panel).getAllByTestId("recommendation-status").length).toBe(
      recommendationsForFinding.length,
    );
  });

  it("renders each recommendation's Derived epistemic label (never Attested/settled)", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const labels = within(panel).getAllByTestId("epistemic-label");
    expect(labels.length).toBeGreaterThanOrEqual(recommendationsForFinding.length);
    for (const label of labels) {
      expect(label).toHaveAttribute("data-standing", "derived");
    }
  });

  it("groups multiple alternatives as Resolution Paths (presentation grouping)", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    // the grouping markup exists when there are alternatives…
    const group = within(panel).getByTestId("resolution-paths");
    expect(group).toBeInTheDocument();
    // …and contains the *other* recommendations (alternatives to OSLO Recommended)
    const paths = within(group).getAllByTestId("resolution-path");
    expect(paths.length).toBe(recommendationsForFinding.length - 1);
  });

  it("shows the no-alternatives state when only one recommendation exists (§O)", async () => {
    recState.data = { data: singleRecommendationForFinding };
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    // a single recommendation: no Resolution-Paths shell implying failure
    expect(within(panel).queryByTestId("resolution-path")).not.toBeInTheDocument();
    expect(within(panel).getByTestId("no-alternatives")).toBeInTheDocument();
  });

  it("renders the accept/reject/defer affordance for the primary recommendation", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    // every recommendation card carries the affordance; the primary's must be present
    const primary = within(panel).getByTestId(
      `recommendation-item-${primaryRecommendationFixture.recommendation_id}`,
    );
    expect(within(primary).getByTestId("affordance-accept")).toBeInTheDocument();
    expect(within(primary).getByTestId("affordance-reject")).toBeInTheDocument();
    expect(within(primary).getByTestId("affordance-defer")).toBeInTheDocument();
  });
});

describe("RecommendationPanel — RP-C1: only in a Finding context", () => {
  it("does NOT render recommendations / resolution paths outside a finding context", async () => {
    // No finding context: the panel is mounted standalone (a rejected negative).
    await mount(undefined, false);
    // The panel shell may render, but it must surface the RP-C1 guard and NOT the
    // recommendation content — no items, no resolution paths, no affordances.
    expect(screen.getByTestId("recommendation-panel-no-context")).toBeInTheDocument();
    expect(screen.queryByTestId("recommendation-item")).not.toBeInTheDocument();
    expect(screen.queryByTestId("resolution-paths")).not.toBeInTheDocument();
    expect(screen.queryByTestId("affordance-accept")).not.toBeInTheDocument();
  });
});

describe("RecommendationPanel — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    recState.isLoading = true;
    recState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("recommendation-panel")).toBeInTheDocument();
    expect(screen.getByTestId("recommendation-loading")).toBeInTheDocument();
  });

  it("renders an explicit none-exists empty state distinct from not-yet-generated", async () => {
    recState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("recommendation-panel")).toBeInTheDocument();
    expect(screen.getByTestId("recommendation-empty")).toBeInTheDocument();
  });
});

// ── The Disclose-never-accepts NEGATIVES (the spine; fail review if absent) ──
describe("RecommendationPanel — NEGATIVES: presents the affordance, NEVER accepts", () => {
  it("accept does NOT flip the recommendation to Accepted locally — it hands off to Wave U", async () => {
    const { router } = await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const primaryItem = within(panel).getByTestId("recommendation-item-rec-primary-1");
    // before: the primary is `generated` (read from the governed source)
    expect(primaryItem).toHaveAttribute("data-status", "generated");

    const accept = within(primaryItem).getByTestId("affordance-accept");
    fireEvent.click(accept);
    await router.invalidate();

    // The hand-off: navigation to the EXISTING Wave U capture — NOT a local mutation.
    expect(router.state.location.pathname).toMatch(/\/recommendations$/);
    expect(router.state.location.pathname).not.toContain("/findings/");
    // and the recommendation's status did NOT change client-side.
    expect(
      within(screen.queryByTestId("recommendation-panel") ?? document.body).queryByTestId(
        "recommendation-item-rec-primary-1",
      ),
    ).toBeNull();
  });

  it("does NOT construct or emit any Resolution-Path object (grouping markup only)", async () => {
    await mount();
    const group = screen.getByTestId("resolution-paths");
    // The grouping is pure markup over the SAME recommendation_ids — no synthesized
    // object id, no new entity. Each path is one of the source recommendations.
    const paths = within(group).getAllByTestId("resolution-path");
    const ids = paths.map((el) => el.getAttribute("data-recommendation-id"));
    expect(ids).toContain(alternativeRecommendationFixture.recommendation_id);
    // never a path keyed on a fabricated "resolution-path-*" object id
    for (const id of ids) {
      expect(id).not.toMatch(/^resolution-path/i);
    }
  });

  it("exposes NO generate / score / recompute / resolve-finding / apply control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
    ];
    const forbidden =
      /\bgenerate\b|\bscore\b|recompute|re-?analy[sz]e|run analysis|resolve finding|\bgovern\b|\bapprove\b|\bexecute\b|run agent|automate/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("never presents a recommendation as settled or a directive (advisory only)", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    expect(within(panel).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    // the primary's own label stays Derived (a projection, not settled truth)
    const primary = within(panel).getByTestId(
      `recommendation-item-${primaryRecommendationFixture.recommendation_id}`,
    );
    expect(within(primary).getByTestId("epistemic-label")).toHaveAttribute(
      "data-standing",
      "derived",
    );
  });
});

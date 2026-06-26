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
  // The query-key helper is used by the surface to invalidate the read on success.
  getListRecommendationsForFindingV1FindingsFindingIdRecommendationsGetQueryKey: (
    findingId: string,
    params: unknown,
  ) => [`/v1/findings/${findingId}/recommendations`, params],
}));

// ── Mock the DTM-0033 acceptance-command hooks (the affordance now CALLS these) ──
// Each hook returns a stable `mutate` spy so a test can assert the command is the
// path. `onSuccess` is captured so we can assert the read is invalidated.
const acceptMutate = vi.fn();
const rejectMutate = vi.fn();
const deferMutate = vi.fn();
const implementMutate = vi.fn();
let lastAcceptOnSuccess: (() => void) | undefined;

vi.mock("../../../api/generated/acceptance-commands/acceptance-commands", () => ({
  useAcceptRecommendationV1RecommendationsRecommendationIdAcceptPost: (opts?: {
    mutation?: { onSuccess?: () => void };
  }) => {
    lastAcceptOnSuccess = opts?.mutation?.onSuccess;
    return { mutate: acceptMutate, isPending: false };
  },
  useRejectRecommendationV1RecommendationsRecommendationIdRejectPost: () => ({
    mutate: rejectMutate,
    isPending: false,
  }),
  useDeferRecommendationV1RecommendationsRecommendationIdDeferPost: () => ({
    mutate: deferMutate,
    isPending: false,
  }),
  useImplementRecommendationV1RecommendationsRecommendationIdImplementPost: () => ({
    mutate: implementMutate,
    isPending: false,
  }),
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
  acceptMutate.mockReset();
  rejectMutate.mockReset();
  deferMutate.mockReset();
  implementMutate.mockReset();
  lastAcceptOnSuccess = undefined;
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

// ── The command-path POSITIVES (DTM-0039 — the affordance CALLS the command) ──
describe("RecommendationPanel — the affordance calls the user-initiated command", () => {
  it("accept calls the accept mutation with the recommendation id (the command records the UAR)", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const primaryItem = within(panel).getByTestId("recommendation-item-rec-primary-1");
    fireEvent.click(within(primaryItem).getByTestId("affordance-accept"));
    expect(acceptMutate).toHaveBeenCalledTimes(1);
    expect(acceptMutate).toHaveBeenCalledWith({ recommendationId: "rec-primary-1" });
  });

  it("reject / defer / implement each call their own command mutation", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const primaryItem = within(panel).getByTestId("recommendation-item-rec-primary-1");
    fireEvent.click(within(primaryItem).getByTestId("affordance-reject"));
    fireEvent.click(within(primaryItem).getByTestId("affordance-defer"));
    fireEvent.click(within(primaryItem).getByTestId("affordance-implement"));
    expect(rejectMutate).toHaveBeenCalledWith({ recommendationId: "rec-primary-1" });
    expect(deferMutate).toHaveBeenCalledWith({ recommendationId: "rec-primary-1" });
    expect(implementMutate).toHaveBeenCalledWith({ recommendationId: "rec-primary-1" });
  });

  it("on command success it invalidates the finding-recs read (re-reads the governed status)", async () => {
    await mount();
    // the surface wires an onSuccess that invalidates the read; it is defined
    expect(typeof lastAcceptOnSuccess).toBe("function");
  });
});

// ── The Disclose-never-accepts NEGATIVES (the spine; fail review if absent) ──
describe("RecommendationPanel — NEGATIVES: presents the affordance, NEVER accepts locally", () => {
  it("accept does NOT flip the recommendation to Accepted locally — the command is the only path", async () => {
    await mount();
    const panel = screen.getByTestId("recommendation-panel");
    const primaryItem = within(panel).getByTestId("recommendation-item-rec-primary-1");
    // before: the primary is `generated` (read from the governed source)
    expect(primaryItem).toHaveAttribute("data-status", "generated");

    fireEvent.click(within(primaryItem).getByTestId("affordance-accept"));

    // The SURFACE performs no local acceptance: the card's status stays exactly what
    // the governed read returned — it is NOT flipped to "accepted" client-side. The
    // command (mutation) is the only path that records acceptance.
    const after = within(screen.getByTestId("recommendation-panel")).getByTestId(
      "recommendation-item-rec-primary-1",
    );
    expect(after).toHaveAttribute("data-status", "generated");
    // and the mutation (the command) is what was invoked — not a local state write.
    expect(acceptMutate).toHaveBeenCalledTimes(1);
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

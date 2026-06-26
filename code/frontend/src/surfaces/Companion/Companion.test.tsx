/**
 * DTM-0025 — Understanding Companion (IC-WE-DISCLOSE E1).
 *
 * The persistent, contextual understanding surface: epistemic-safe summaries of the
 * current understanding (Outcome Confidence · CAF · Top Findings · Top
 * Recommendations · stale-analysis state · Ask OSLO). It PRESENTS, NEVER GENERATES,
 * and — the headline contract — it routes to a Recommendation **via its associated
 * Finding (Option B)**, NEVER to a standalone Recommendation Panel (RP-C1 preserved).
 *
 * THE STALE-STATE DATA FINDING (see fixtures.ts + the worker report): there is no
 * "companion"/"is_stale" DTO — the Companion presents "Previous Analysis" from the
 * governed `AnalysisRun.run_status === "superseded"`. The DTM-0018 generated hooks
 * are mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderCompanion } from "./testHarness";
import {
  PROJECT_ID,
  companionConfidenceFixture,
  companionCafFixture,
  companionFindingsFixture,
  companionRecommendationsFixture,
  companionRunsCurrentFixture,
  companionRunsStaleFixture,
} from "./fixtures";

// ── Mock the DTM-0018 reads (the surface consumes, never re-implements) ──────────
const confidenceState = { data: { data: companionConfidenceFixture }, isLoading: false };
const cafState = { data: { data: companionCafFixture }, isLoading: false };
const findingsState = { data: { data: companionFindingsFixture }, isLoading: false };
const recsState = { data: { data: companionRecommendationsFixture }, isLoading: false };
const runsState = { data: { data: companionRunsCurrentFixture }, isLoading: false };

vi.mock("../../api/generated/confidence/confidence", () => ({
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => confidenceState,
  useGetCafV1ProjectsProjectIdCafGet: () => cafState,
}));
vi.mock("../../api/generated/findings/findings", () => ({
  useListFindingsV1ProjectsProjectIdFindingsGet: () => findingsState,
}));
vi.mock("../../api/generated/recommendations/recommendations", () => ({
  useListRecommendationsV1ProjectsProjectIdRecommendationsGet: () => recsState,
}));
vi.mock("../../api/generated/analysis-runs/analysis-runs", () => ({
  useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet: () => runsState,
}));

// Imported AFTER the mocks (vi.mock is hoisted).
import { Companion } from "./Companion";

function mount(projectId = PROJECT_ID) {
  return renderCompanion(<Companion projectId={projectId} />, { projectId });
}

beforeEach(() => {
  confidenceState.data = { data: companionConfidenceFixture };
  confidenceState.isLoading = false;
  cafState.data = { data: companionCafFixture };
  cafState.isLoading = false;
  findingsState.data = { data: companionFindingsFixture };
  findingsState.isLoading = false;
  recsState.data = { data: companionRecommendationsFixture };
  recsState.isLoading = false;
  runsState.data = { data: companionRunsCurrentFixture };
  runsState.isLoading = false;
});

describe("Companion — contextual epistemic-safe summaries (each value labelled)", () => {
  it("renders the companion surface", async () => {
    await mount();
    expect(screen.getByTestId("companion")).toBeInTheDocument();
  });

  it("presents Outcome Confidence as a Derived label (banded, never settled)", async () => {
    await mount();
    const conf = screen.getByTestId("companion-confidence");
    const label = within(conf).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "derived");
    expect(within(conf).getByTestId("confidence-band")).toHaveAttribute(
      "data-band",
      companionConfidenceFixture.label!.confidence_band,
    );
  });

  it("presents CAF — three co-equal dimensions, each a Derived banded label", async () => {
    await mount();
    const caf = screen.getByTestId("companion-caf");
    expect(within(caf).getByTestId("caf-dimension-clarity")).toBeInTheDocument();
    expect(within(caf).getByTestId("caf-dimension-alignment")).toBeInTheDocument();
    expect(within(caf).getByTestId("caf-dimension-feasibility")).toBeInTheDocument();
    for (const dim of within(caf).getAllByTestId("caf-dimension")) {
      expect(within(dim).getByTestId("epistemic-label")).toHaveAttribute(
        "data-standing",
        "derived",
      );
    }
  });

  it("presents Top Findings, each with a Derived label and a link to its Finding Panel", async () => {
    await mount();
    const findings = screen.getByTestId("companion-findings");
    const items = within(findings).getAllByTestId("companion-finding");
    expect(items.length).toBe(companionFindingsFixture.length);
    for (const item of items) {
      expect(within(item).getByTestId("epistemic-label")).toHaveAttribute(
        "data-standing",
        "derived",
      );
    }
    // Each Top Finding links to the Finding Panel (Q5).
    const link = within(items[0]).getByTestId("open-finding");
    expect(link).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${companionFindingsFixture[0].finding_id}`,
    );
  });

  it("presents Top Recommendations, each with a Derived label", async () => {
    await mount();
    const recs = screen.getByTestId("companion-recommendations");
    const items = within(recs).getAllByTestId("companion-recommendation");
    expect(items.length).toBe(companionRecommendationsFixture.length);
    for (const item of items) {
      expect(within(item).getByTestId("epistemic-label")).toHaveAttribute(
        "data-standing",
        "derived",
      );
    }
  });

  it("includes an Ask OSLO entry (launches Chat, never embeds it)", async () => {
    await mount();
    expect(screen.getByTestId("ask-oslo")).toBeInTheDocument();
  });
});

// ── OPTION B (the headline): route to a Recommendation VIA its associated Finding ──
describe("Companion — Option B: Top Recommendation routes via its associated Finding (RP-C1)", () => {
  it("each Top Recommendation's affordance targets the ASSOCIATED FINDING Panel route", async () => {
    await mount();
    const recs = screen.getByTestId("companion-recommendations");
    const items = within(recs).getAllByTestId("companion-recommendation");
    const link = within(items[0]).getByTestId("see-recommendation");
    // Routes to the associated Finding (finding_id), NOT to a recommendation route.
    expect(link).toHaveAttribute(
      "href",
      `/projects/${PROJECT_ID}/findings/${companionRecommendationsFixture[0].finding_id}`,
    );
  });

  it("activating a Top Recommendation lands on the associated FINDING PANEL (and nowhere else)", async () => {
    const { router } = await mount();
    const items = within(screen.getByTestId("companion-recommendations")).getAllByTestId(
      "companion-recommendation",
    );
    const link = within(items[0]).getByTestId("see-recommendation");
    fireEvent.click(link);
    await router.invalidate();
    const path = router.state.location.pathname;
    // Lands ON the Finding Panel for the associated finding…
    expect(
      path.endsWith(`/findings/${companionRecommendationsFixture[0].finding_id}`),
    ).toBe(true);
    // …and is the Finding-panel target, not a recommendation target.
    expect(screen.getByTestId("finding-panel-target")).toBeInTheDocument();
  });

  it("NEGATIVE: never routes directly to a nested standalone Recommendation Panel", async () => {
    const { router } = await mount();
    const items = within(screen.getByTestId("companion-recommendations")).getAllByTestId(
      "companion-recommendation",
    );
    const link = within(items[0]).getByTestId("see-recommendation");
    fireEvent.click(link);
    await router.invalidate();
    // Did NOT land on /recommendations of any kind.
    expect(router.state.location.pathname).not.toMatch(/\/recommendations$/);
    expect(screen.queryByTestId("recommendation-panel-target")).not.toBeInTheDocument();
    expect(screen.queryByTestId("standalone-recommendation-target")).not.toBeInTheDocument();
  });

  it("NEGATIVE: no recommendation affordance hrefs a /recommendations route directly", async () => {
    const { container } = await mount();
    for (const a of Array.from(container.querySelectorAll("a[href]"))) {
      expect(a.getAttribute("href")).not.toMatch(/\/recommendations(\/|$)/);
    }
  });
});

describe("Companion — stale-analysis visibility (Q8 / COMP-11)", () => {
  it("surfaces NO 'Previous Analysis' marker when the latest run is current", async () => {
    await mount();
    expect(screen.queryByTestId("companion-stale")).not.toBeInTheDocument();
  });

  it("prominently surfaces 'Previous Analysis' when the latest run is superseded", async () => {
    runsState.data = { data: companionRunsStaleFixture };
    await mount();
    const stale = screen.getByTestId("companion-stale");
    expect(stale).toBeInTheDocument();
    expect(stale.textContent ?? "").toMatch(/previous analysis/i);
  });
});

describe("Companion — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    confidenceState.isLoading = true;
    confidenceState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("companion")).toBeInTheDocument();
    expect(screen.getByTestId("companion-loading")).toBeInTheDocument();
  });

  it("renders cleanly when confidence / CAF are not yet available", async () => {
    confidenceState.data = undefined as never;
    cafState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("companion-confidence-empty")).toBeInTheDocument();
    expect(screen.getByTestId("companion-caf-empty")).toBeInTheDocument();
  });

  it("renders clean empty states for no findings / no recommendations", async () => {
    findingsState.data = { data: [] };
    recsState.data = { data: [] };
    await mount();
    expect(screen.getByTestId("companion-findings-empty")).toBeInTheDocument();
    expect(screen.getByTestId("companion-recommendations-empty")).toBeInTheDocument();
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("Companion — NEGATIVES: presents, never generates", () => {
  it("exposes NO generate / score / accept / reject / defer / edit / govern control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
    ];
    const forbidden =
      /\bedit\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bresolve\b|\bapprove\b|\bgovern\b|\bgenerate\b|recompute|re-?analy[sz]e|run analysis|\bapply\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("no Derived value ever renders as settled / attested-truth", async () => {
    runsState.data = { data: companionRunsStaleFixture };
    await mount();
    const surface = screen.getByTestId("companion");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    for (const label of within(surface).getAllByTestId("epistemic-label")) {
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("confidence is NEVER overstated — every band is carried VERBATIM off the DTO", async () => {
    await mount();
    // The medium Outcome Confidence carries through as medium…
    const conf = screen.getByTestId("companion-confidence");
    expect(within(conf).getByTestId("confidence-band")).toHaveAttribute("data-band", "medium");
    // …and the band-LOW finding (f-2) is shown low, never upgraded.
    const findings = screen.getByTestId("companion-findings");
    const items = within(findings).getAllByTestId("companion-finding");
    const lowItem = items.find(
      (el) => el.getAttribute("data-finding-id") === "f-2",
    )!;
    expect(within(lowItem).getByTestId("confidence-band")).toHaveAttribute(
      "data-band",
      "low",
    );
  });

  it("never reads as project health / readiness / probability / a bare score / %", async () => {
    runsState.data = { data: companionRunsStaleFixture };
    await mount();
    const surface = screen.getByTestId("companion");
    expect(within(surface).queryByText(/\bhealth\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\breadiness\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bprobability\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bon[- ]?track\b/i)).not.toBeInTheDocument();
    const text = surface.textContent ?? "";
    expect(text).not.toMatch(/%/);
    // the raw 0–100 index values are never rendered
    expect(text).not.toMatch(/\b66\b|\b72\b|\b40\b|\b85\b|\b55\b|\b30\b/);
  });

  it("surfaces the conflict marker on a contested finding (presented, not resolved)", async () => {
    await mount();
    const items = within(screen.getByTestId("companion-findings")).getAllByTestId(
      "companion-finding",
    );
    const contested = items.find((el) => el.getAttribute("data-finding-id") === "f-1")!;
    expect(within(contested).getByTestId("conflict-marker")).toBeInTheDocument();
  });
});

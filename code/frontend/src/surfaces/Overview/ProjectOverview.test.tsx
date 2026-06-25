/**
 * DTM-0024 — Project Overview (IC-WE-DISCLOSE E1).
 *
 * A project-level UNDERSTANDING SUMMARY: aggregate Outcome Confidence + CAF
 * (Derived, banded) + counts (findings / issues / recommendations). Read-only; it
 * PRESENTS, NEVER GENERATES — no edit/score/accept/generate control, every Derived
 * value carries an `EpistemicLabel` and can never read as settled, confidence/the
 * overview never reads as project health/readiness/probability/%, and the counts are
 * presentation of governed objects, never a health metric.
 *
 * THE COUNTS-DATA FINDING (see fixtures.ts + the worker report): there is no
 * aggregate "overview"/counts DTO — the counts are the lengths of the governed list
 * reads (findings; issues = findings with a severity; recommendations). The DTM-0018
 * generated hooks are mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderOverview } from "./testHarness";
import {
  PROJECT_ID,
  overviewConfidenceFixture,
  overviewCafFixture,
  overviewFindingsFixture,
  overviewRecommendationsFixture,
} from "./fixtures";

// ── Mock the DTM-0018 reads (the surface consumes, never re-implements) ──────────
const confidenceState = { data: { data: overviewConfidenceFixture }, isLoading: false };
const cafState = { data: { data: overviewCafFixture }, isLoading: false };
const findingsState = { data: { data: overviewFindingsFixture }, isLoading: false };
const recsState = { data: { data: overviewRecommendationsFixture }, isLoading: false };

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

// Imported AFTER the mocks (vi.mock is hoisted).
import { ProjectOverview } from "./ProjectOverview";

function mount(projectId = PROJECT_ID) {
  return renderOverview(<ProjectOverview projectId={projectId} />, {
    initialPath: `/projects/${projectId}/orientation`,
  });
}

beforeEach(() => {
  confidenceState.data = { data: overviewConfidenceFixture };
  confidenceState.isLoading = false;
  cafState.data = { data: overviewCafFixture };
  cafState.isLoading = false;
  findingsState.data = { data: overviewFindingsFixture };
  findingsState.isLoading = false;
  recsState.data = { data: overviewRecommendationsFixture };
  recsState.isLoading = false;
});

describe("ProjectOverview — aggregate Outcome Confidence + CAF + counts", () => {
  it("renders the overview surface", async () => {
    await mount();
    expect(screen.getByTestId("project-overview")).toBeInTheDocument();
  });

  it("presents aggregate Outcome Confidence as a Derived label (banded, never settled)", async () => {
    await mount();
    const conf = screen.getByTestId("overview-confidence");
    const label = within(conf).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "derived");
    expect(within(conf).getByTestId("confidence-band")).toHaveAttribute(
      "data-band",
      overviewConfidenceFixture.label!.confidence_band,
    );
  });

  it("presents CAF — all three co-equal dimensions, each a Derived banded label", async () => {
    await mount();
    const caf = screen.getByTestId("overview-caf");
    // three co-equal dimensions present
    expect(within(caf).getByTestId("caf-dimension-clarity")).toBeInTheDocument();
    expect(within(caf).getByTestId("caf-dimension-alignment")).toBeInTheDocument();
    expect(within(caf).getByTestId("caf-dimension-feasibility")).toBeInTheDocument();
    // each carries a Derived banded label (never settled)
    for (const dim of within(caf).getAllByTestId("caf-dimension")) {
      const label = within(dim).getByTestId("epistemic-label");
      expect(label).toHaveAttribute("data-standing", "derived");
    }
  });

  it("presents the counts of governed objects: findings, issues, recommendations", async () => {
    await mount();
    const counts = screen.getByTestId("overview-counts");
    // findings = 3, issues = 2 (findings with a severity), recommendations = 2
    expect(within(counts).getByTestId("count-findings")).toHaveTextContent("3");
    expect(within(counts).getByTestId("count-issues")).toHaveTextContent("2");
    expect(within(counts).getByTestId("count-recommendations")).toHaveTextContent("2");
  });
});

describe("ProjectOverview — loading / empty states", () => {
  it("renders a clean loading state without crashing", async () => {
    confidenceState.isLoading = true;
    confidenceState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("project-overview")).toBeInTheDocument();
    expect(screen.getByTestId("overview-loading")).toBeInTheDocument();
  });

  it("renders cleanly when confidence/CAF are not yet available", async () => {
    confidenceState.data = undefined as never;
    cafState.data = undefined as never;
    await mount();
    expect(screen.getByTestId("overview-confidence-empty")).toBeInTheDocument();
    expect(screen.getByTestId("overview-caf-empty")).toBeInTheDocument();
  });

  it("counts read zero (not an error) when the lists are empty", async () => {
    findingsState.data = { data: [] };
    recsState.data = { data: [] };
    await mount();
    const counts = screen.getByTestId("overview-counts");
    expect(within(counts).getByTestId("count-findings")).toHaveTextContent("0");
    expect(within(counts).getByTestId("count-issues")).toHaveTextContent("0");
    expect(within(counts).getByTestId("count-recommendations")).toHaveTextContent("0");
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("ProjectOverview — NEGATIVES: presents, never generates; NOT project health", () => {
  it("exposes NO edit / score / accept / reject / defer / generate / govern control", async () => {
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
    await mount();
    const surface = screen.getByTestId("project-overview");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    for (const label of within(surface).getAllByTestId("epistemic-label")) {
      expect(label).toHaveAttribute("data-standing", "derived");
      expect(label).not.toHaveAttribute("data-standing", "attested");
    }
  });

  it("the overview never reads as project health / readiness / probability / on-track / a bare score / %", async () => {
    await mount();
    const surface = screen.getByTestId("project-overview");
    expect(within(surface).queryByText(/\bhealth\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\breadiness\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bprobability\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bon[- ]?track\b/i)).not.toBeInTheDocument();
    // the raw 0–100 confidence/CAF index values are NEVER rendered, nor a %
    const text = surface.textContent ?? "";
    expect(text).not.toMatch(/%/);
    expect(text).not.toMatch(/\b82\b|\b72\b|\b40\b|\b85\b|\b66\b/);
  });

  it("the counts are not framed as a project-health / score metric", async () => {
    await mount();
    const counts = screen.getByTestId("overview-counts");
    const text = counts.textContent ?? "";
    expect(text).not.toMatch(/\bhealth\b|\bscore\b|\breadiness\b|%/i);
    // they read as counts OF governed objects (findings / issues / recommendations)
    expect(text).toMatch(/finding/i);
    expect(text).toMatch(/issue/i);
    expect(text).toMatch(/recommendation/i);
  });
});

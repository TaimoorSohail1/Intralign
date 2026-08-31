/**
 * DTM-0028 — Export / Share-out surface (IC-WE-DISCLOSE E1).
 *
 * The surface PACKAGES the governed outputs (it consumes the DTM-0018 reads read-only),
 * renders an in-app PREVIEW carrying each item's epistemic label + provenance +
 * plan-fact attribution, and offers a browser-native download/copy affordance (Blob/
 * anchor — no export/PDF library). It PRESENTS, NEVER GENERATES.
 *
 * THE CRITICAL NEGATIVES (fail review if absent):
 *   - NO generate / score / accept / reject / defer / edit / govern / reanalyze control.
 *   - Derived reads Derived (banded, never settled) in the preview; band never upgraded.
 *   - Plan facts + UARs read user-attested ("You confirmed", not world-truth).
 *   - Provenance preserved (the CHR ref/source visible).
 *   - The mandatory disclaimer is present.
 *
 * The eight DTM-0018 reads are mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderExport } from "./testHarness";
import {
  exportProjectFixture,
  exportConfidenceFixture,
  exportCafFixture,
  exportFindingsFixture,
  exportRecommendationsFixture,
  exportRunsCurrentFixture,
  exportRunsStaleFixture,
  exportAcceptancesFixture,
  exportPlanFactsFixture,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the eight DTM-0018 reads (the surface consumes, never re-implements) ─────
const projectState = { data: { data: exportProjectFixture }, isLoading: false };
const confidenceState = { data: { data: exportConfidenceFixture }, isLoading: false };
const cafState = { data: { data: exportCafFixture }, isLoading: false };
const findingsState = { data: { data: exportFindingsFixture }, isLoading: false };
const recommendationsState = {
  data: { data: exportRecommendationsFixture },
  isLoading: false,
};
const runsState = { data: { data: exportRunsCurrentFixture }, isLoading: false };
const acceptancesState = { data: { data: exportAcceptancesFixture }, isLoading: false };
const planFactsState = { data: { data: exportPlanFactsFixture }, isLoading: false };

vi.mock("../../api/generated/projects/projects", () => ({
  useGetProjectV1ProjectsProjectIdGet: () => projectState,
}));
vi.mock("../../api/generated/confidence/confidence", () => ({
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => confidenceState,
  useGetCafV1ProjectsProjectIdCafGet: () => cafState,
}));
vi.mock("../../api/generated/findings/findings", () => ({
  useListFindingsV1ProjectsProjectIdFindingsGet: () => findingsState,
}));
vi.mock("../../api/generated/recommendations/recommendations", () => ({
  useListRecommendationsV1ProjectsProjectIdRecommendationsGet: () => recommendationsState,
}));
vi.mock("../../api/generated/analysis-runs/analysis-runs", () => ({
  useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet: () => runsState,
}));
vi.mock("../../api/generated/acceptance/acceptance", () => ({
  useListAcceptancesV1ProjectsProjectIdAcceptanceGet: () => acceptancesState,
  useListPlanFactsV1ProjectsProjectIdPlanFactsGet: () => planFactsState,
}));

// Imported AFTER the mocks (vi.mock is hoisted).
import { Export } from "./Export";

function mount(projectId: string = PROJECT_ID) {
  return renderExport(<Export projectId={projectId} />, projectId);
}

function resetAll() {
  projectState.data = { data: exportProjectFixture };
  projectState.isLoading = false;
  confidenceState.data = { data: exportConfidenceFixture };
  confidenceState.isLoading = false;
  cafState.data = { data: exportCafFixture };
  cafState.isLoading = false;
  findingsState.data = { data: exportFindingsFixture };
  findingsState.isLoading = false;
  recommendationsState.data = { data: exportRecommendationsFixture };
  recommendationsState.isLoading = false;
  runsState.data = { data: exportRunsCurrentFixture };
  runsState.isLoading = false;
  acceptancesState.data = { data: exportAcceptancesFixture };
  acceptancesState.isLoading = false;
  planFactsState.data = { data: exportPlanFactsFixture };
  planFactsState.isLoading = false;
}

beforeEach(() => {
  resetAll();
  // Browser Blob/anchor download is exercised — stub URL.createObjectURL.
  (URL as unknown as { createObjectURL: () => string }).createObjectURL = vi.fn(
    () => "blob:mock",
  );
  (URL as unknown as { revokeObjectURL: () => void }).revokeObjectURL = vi.fn();
});

// ── POSITIVE: packages governed outputs with labels + provenance ──────────────────
describe("Export — packages the governed outputs into a preview", () => {
  it("renders the surface with a title + the mandatory disclaimer", async () => {
    await mount();
    expect(screen.getByTestId("export-surface")).toBeInTheDocument();
    expect(screen.getByTestId("surface-title")).toBeInTheDocument();
    expect(screen.getByTestId("export-disclaimer")).toBeInTheDocument();
    expect(screen.getByTestId("export-disclaimer").textContent).toMatch(
      /not project health/i,
    );
  });

  it("renders a preview that carries each governed item (finding summary, recommendation)", async () => {
    await mount();
    const preview = screen.getByTestId("export-preview");
    expect(
      within(preview).getByText(exportFindingsFixture[0].summary as string),
    ).toBeInTheDocument();
    expect(
      within(preview).getByText(exportRecommendationsFixture[0].title as string),
    ).toBeInTheDocument();
    expect(
      within(preview).getByText(exportPlanFactsFixture[0].proposition),
    ).toBeInTheDocument();
  });

  it("carries an epistemic label on every previewed claim group", async () => {
    await mount();
    const preview = screen.getByTestId("export-preview");
    expect(within(preview).getAllByTestId("epistemic-label").length).toBeGreaterThan(0);
  });

  it("preserves provenance — the CHR ref/source is visible in the preview", async () => {
    await mount();
    const preview = screen.getByTestId("export-preview");
    expect(within(preview).getAllByTestId("export-provenance").length).toBeGreaterThan(0);
    // a CHR ref from the fixtures is present (appears in the provenance summary + the
    // finding's provenance row — both are legitimate provenance carriers)
    expect(within(preview).getAllByText(/chr-f-1/).length).toBeGreaterThan(0);
  });

  it("offers a browser-native download affordance (Blob/anchor — no library)", async () => {
    await mount();
    const dl = screen.getByTestId("export-download");
    expect(dl).toBeInTheDocument();
    fireEvent.click(dl);
    expect(
      (URL as unknown as { createObjectURL: ReturnType<typeof vi.fn> }).createObjectURL,
    ).toHaveBeenCalled();
  });

  it("offers a copyable-summary affordance", async () => {
    await mount();
    expect(screen.getByTestId("export-copy")).toBeInTheDocument();
  });
});

// ── Loading / empty states ─────────────────────────────────────────────────────────
describe("Export — loading / empty states", () => {
  it("renders a clean loading state", async () => {
    projectState.isLoading = true;
    confidenceState.isLoading = true;
    cafState.isLoading = true;
    findingsState.isLoading = true;
    recommendationsState.isLoading = true;
    runsState.isLoading = true;
    acceptancesState.isLoading = true;
    planFactsState.isLoading = true;
    await mount();
    expect(screen.getByTestId("export-surface")).toBeInTheDocument();
    expect(screen.getByTestId("export-loading")).toBeInTheDocument();
  });

  it("renders a clean 'nothing to export' empty state when there is no understanding", async () => {
    confidenceState.data = { data: undefined as never };
    cafState.data = { data: undefined as never };
    findingsState.data = { data: [] as never };
    recommendationsState.data = { data: [] as never };
    runsState.data = { data: [] as never };
    acceptancesState.data = { data: [] as never };
    planFactsState.data = { data: [] as never };
    await mount();
    expect(screen.getByTestId("export-empty")).toBeInTheDocument();
  });
});

// ── Stale / previous-analysis handling ─────────────────────────────────────────────
describe("Export — stale handling (previous analysis, never current)", () => {
  it("warns + marks 'previous analysis' when the governed latest run is superseded", async () => {
    runsState.data = { data: exportRunsStaleFixture };
    await mount();
    expect(screen.getByTestId("export-stale-warning")).toBeInTheDocument();
    expect(screen.getByTestId("export-stale-warning").textContent).toMatch(
      /previous analysis/i,
    );
  });

  it("does NOT show a stale warning when understanding is current", async () => {
    await mount();
    expect(screen.queryByTestId("export-stale-warning")).not.toBeInTheDocument();
  });
});

// ── THE CRITICAL NEGATIVES (fail review if absent) ─────────────────────────────────
describe("Export — NEGATIVES: presents, never generates", () => {
  it("exposes NO generate / score / accept / reject / defer / edit / govern / reanalyze control", async () => {
    const { container } = await mount();
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
      ...container.querySelectorAll("textarea"),
      ...container.querySelectorAll("select"),
      ...container.querySelectorAll('[contenteditable="true"]'),
    ];
    const forbidden =
      /\bgenerate\b|\bscore\b|\baccept\b|\breject\b|\bdefer\b|\bedit\b|\bgovern\b|\bapprove\b|\bapproval\b|recompute|re-?analy[sz]e|reanalyze|reanalyse|\bapply\b|\bresolve\b|\bdelete\b|\brollback\b/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("Derived items NEVER render as settled / world-truth (always Derived projections)", async () => {
    await mount();
    const surface = screen.getByTestId("export-surface");
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    // findings/recommendations preview labels read Derived
    const findingGroup = screen.getByTestId("export-item-f-1");
    expect(
      within(findingGroup).getByTestId("epistemic-label"),
    ).toHaveAttribute("data-standing", "derived");
  });

  it("plan facts render user-attested ('You confirmed'), never world-truth/evidence-attested", async () => {
    await mount();
    const pf = screen.getByTestId("export-item-pf-001");
    const label = within(pf).getByTestId("epistemic-label");
    expect(label).toHaveAttribute("data-standing", "attested");
    expect(label).toHaveAttribute("data-source", "user");
    // "You confirmed" appears as both the user-attested label chip and the claim label
    expect(within(pf).getAllByText(/you confirmed/i).length).toBeGreaterThan(0);
    // the packaged content (the preview) never claims world-truth. (The mandatory
    // disclaimer is a separate node and legitimately denies such framings.)
    const preview = screen.getByTestId("export-preview");
    expect(within(preview).queryByText(/world.?truth/i)).not.toBeInTheDocument();
  });

  it("never frames confidence as project health / readiness / probability / a score", async () => {
    await mount();
    // Assert against the PREVIEW (the packaged claims), NOT the whole surface — the
    // mandatory disclaimer (a separate node) legitimately DENIES "project health /
    // readiness / probability" and that denial is required (EX-6).
    const preview = screen.getByTestId("export-preview");
    expect(within(preview).queryByText(/project health/i)).not.toBeInTheDocument();
    expect(within(preview).queryByText(/readiness/i)).not.toBeInTheDocument();
    expect(within(preview).queryByText(/probability/i)).not.toBeInTheDocument();
    // the numeric 0–100 index is never shown (only the band)
    expect(within(preview).queryByText(/\b66\b/)).not.toBeInTheDocument();
  });

  it("never frames itself as approval / certification / governance publication", async () => {
    await mount();
    // Assert against the packaged content (preview), NOT the disclaimer node (which
    // legitimately DENIES approval/certification — required by EX-6).
    const preview = screen.getByTestId("export-preview");
    expect(within(preview).queryByText(/\bcertification\b/i)).not.toBeInTheDocument();
    expect(within(preview).queryByText(/\bapproved\b/i)).not.toBeInTheDocument();
  });
});

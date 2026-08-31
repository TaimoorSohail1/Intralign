/**
 * DTM-0020 — the MRI umbrella surface (MRIWorkspace).
 *
 * It mounts the four DL-047 sub-components and presents Findings (grouped into the
 * MRI Experience categories Missing/Risky/Incomplete), CAF, and Outcome Confidence
 * — every governed Derived value carried through `EpistemicLabel`. It PRESENTS,
 * NEVER GENERATES: no compute/recompute/score/accept affordance exists.
 *
 * The DTM-0018 generated hooks are mocked with fixture DTOs.
 */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderMRI } from "./testHarness";
import {
  findingsFixture,
  cafFixture,
  confidenceFixture,
  analysisRunsFixture,
  PROJECT_ID,
} from "./fixtures";

// ── Mock the DTM-0018 Orval hooks (the surface consumes, never re-implements) ──
const findingsState = { data: { data: findingsFixture }, isLoading: false, isError: false };
const cafState = { data: { data: cafFixture }, isLoading: false, isError: false };
const confidenceState = { data: { data: confidenceFixture }, isLoading: false, isError: false };
const runsState = { data: { data: analysisRunsFixture }, isLoading: false, isError: false };

vi.mock("../../api/generated/findings/findings", () => ({
  useListFindingsV1ProjectsProjectIdFindingsGet: () => findingsState,
}));
vi.mock("../../api/generated/confidence/confidence", () => ({
  useGetCafV1ProjectsProjectIdCafGet: () => cafState,
  useGetConfidenceV1ProjectsProjectIdConfidenceGet: () => confidenceState,
}));
vi.mock("../../api/generated/analysis-runs/analysis-runs", () => ({
  useListAnalysisRunsV1ProjectsProjectIdAnalysisRunsGet: () => runsState,
}));

// Imported AFTER the mocks are declared (vi.mock is hoisted).
import { MRIWorkspace } from "./MRIWorkspace";

beforeEach(() => {
  findingsState.isLoading = false;
  findingsState.isError = false;
  findingsState.data = { data: findingsFixture };
});

describe("MRIWorkspace — governed objects each carry an epistemic label", () => {
  it("renders Findings, CAF and Confidence, each wrapped in EpistemicLabel", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    // the umbrella surface mounted
    expect(screen.getByTestId("mri-surface")).toBeInTheDocument();

    // Confidence is shown with its Derived label
    const confidence = screen.getByTestId("mri-confidence");
    expect(within(confidence).getByTestId("epistemic-label")).toHaveAttribute(
      "data-standing",
      "derived",
    );

    // CAF assessment carries its label (inside the triangle sub-component)
    const caf = screen.getByTestId("mri-caf-triangle");
    expect(within(caf).getAllByTestId("epistemic-label")[0]).toHaveAttribute(
      "data-standing",
      "derived",
    );

    // Findings list — each finding row carries its epistemic label
    const findings = screen.getByTestId("mri-findings");
    const rows = within(findings).getAllByTestId("finding-row");
    expect(rows.length).toBe(findingsFixture.length);
    for (const row of rows) {
      expect(within(row).getByTestId("epistemic-label")).toBeInTheDocument();
    }
  });

  it("groups findings into the MRI Experience categories Missing / Risky / Incomplete", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-category-missing")).toBeInTheDocument();
    expect(screen.getByTestId("mri-category-risky")).toBeInTheDocument();
    expect(screen.getByTestId("mri-category-incomplete")).toBeInTheDocument();
  });

  it("mounts all four DL-047 sub-components (MRI-04…07)", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-heatmap")).toBeInTheDocument();
    expect(screen.getByTestId("mri-caf-triangle")).toBeInTheDocument();
    expect(screen.getByTestId("mri-timeline")).toBeInTheDocument();
    expect(screen.getByTestId("mri-dependencies")).toBeInTheDocument();
  });

  it("surfaces the contested conflict marker on a conflicting finding (presents, not resolves)", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    expect(screen.getAllByTestId("conflict-marker").length).toBeGreaterThan(0);
  });
});

describe("MRIWorkspace — current + history both shown (Timeline)", () => {
  it("shows the current understanding prominently and the prior history trail", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    const timeline = screen.getByTestId("mri-timeline");
    expect(within(timeline).getByTestId("timeline-current")).toBeInTheDocument();
    expect(within(timeline).getAllByTestId("timeline-entry").length).toBe(
      analysisRunsFixture.length,
    );
  });
});

describe("MRIWorkspace — loading & empty states render cleanly", () => {
  it("renders a loading state without crashing", async () => {
    findingsState.isLoading = true;
    findingsState.data = undefined as never;
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-surface")).toBeInTheDocument();
    expect(screen.getByTestId("mri-loading")).toBeInTheDocument();
  });

  it("renders an empty findings state without crashing", async () => {
    findingsState.data = { data: [] };
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-surface")).toBeInTheDocument();
    expect(screen.getByTestId("mri-findings-empty")).toBeInTheDocument();
  });
});

// ── The epistemic-safety NEGATIVES (the spine of Disclose; fail review if absent) ──
describe("MRIWorkspace — NEGATIVES: presents, never generates", () => {
  it("exposes NO compute / recompute / score / accept / generate control", async () => {
    const { container } = await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    // No interactive control offers a forbidden Disclose action.
    const controls = [
      ...container.querySelectorAll("button"),
      ...container.querySelectorAll('[role="button"]'),
      ...container.querySelectorAll("input"),
    ];
    const forbidden =
      /recompute|re-analyze|reanalyze|compute|score|accept|reject|approve|generate|run analysis|apply|edit/i;
    for (const el of controls) {
      const text = `${el.textContent ?? ""} ${el.getAttribute("aria-label") ?? ""}`;
      expect(text).not.toMatch(forbidden);
    }
  });

  it("a Derived value never renders as settled / confirmed / attested-truth", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    const surface = screen.getByTestId("mri-surface");
    // No Derived item is dressed up as settled.
    expect(within(surface).queryByText(/\bsettled\b/i)).not.toBeInTheDocument();
    expect(within(surface).queryByText(/\bconfirmed by oslo\b/i)).not.toBeInTheDocument();
    // every epistemic label that is Derived stays Derived
    const labels = within(surface).getAllByTestId("epistemic-label");
    const derived = labels.filter(
      (l) => l.getAttribute("data-standing") === "derived",
    );
    expect(derived.length).toBeGreaterThan(0);
  });

  it("confidence label never reads as health / readiness / probability", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    const confidence = screen.getByTestId("mri-confidence");
    expect(confidence.textContent ?? "").not.toMatch(
      /health|ready|readiness|probability|on track|likelihood/i,
    );
  });

  it("shows no numeric score / percentage / rank anywhere on the surface (qualitative only)", async () => {
    await renderMRI(<MRIWorkspace projectId={PROJECT_ID} />);
    const surface = screen.getByTestId("mri-surface");
    expect(surface.textContent ?? "").not.toMatch(/\b\d{1,3}\s*%|\bscore\b|\brank(?:ed|ing)?\b|\b\d{2,3}\/100\b/i);
  });
});

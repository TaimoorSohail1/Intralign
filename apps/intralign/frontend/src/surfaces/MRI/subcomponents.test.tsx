/**
 * DTM-0020 — the four DL-047 MRI sub-components render from fixture DTOs, present
 * (never recompute), and carry epistemic labels where they show governed Derived
 * values. Components take their data as PROPS (the umbrella surface owns the hooks),
 * so these suites need no hook mocking.
 *
 * Sub-components:
 *   MRI-04 Artifact Understanding Heatmap   (UnderstandingHeatmap)
 *   MRI-05 CAF Triangle                     (CafTriangle)
 *   MRI-06 Understanding Timeline           (UnderstandingTimeline)
 *   MRI-07 Understanding Dependencies       (UnderstandingDependencies)
 */
import { describe, it, expect } from "vitest";
import { screen, within } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { renderMRI } from "./testHarness";
import { UnderstandingHeatmap } from "./UnderstandingHeatmap";
import { CafTriangle } from "./CafTriangle";
import { UnderstandingTimeline } from "./UnderstandingTimeline";
import { UnderstandingDependencies } from "./UnderstandingDependencies";
import {
  findingsFixture,
  cafFixture,
  analysisRunsFixture,
  PROJECT_ID,
} from "./fixtures";

const NUMERIC = /\b\d{1,3}\s*%|\bscore\b|\brank\b|\b\d{2,3}\/100\b/i;

describe("MRI-04 — Artifact Understanding Heatmap", () => {
  it("renders the heatmap discovery surface from findings (SVG)", async () => {
    await renderMRI(
      <UnderstandingHeatmap findings={findingsFixture} projectId={PROJECT_ID} />,
    );
    const heatmap = screen.getByTestId("mri-heatmap");
    expect(heatmap).toBeInTheDocument();
    // it is an SVG-based visualization (no charting library)
    expect(heatmap.querySelector("svg")).toBeTruthy();
    // at least one weakness cell is rendered
    expect(screen.getAllByTestId("heatmap-cell").length).toBeGreaterThan(0);
  });

  it("is qualitative only — shows no numeric score / percentage / rank (MRIW-C3)", async () => {
    await renderMRI(
      <UnderstandingHeatmap findings={findingsFixture} projectId={PROJECT_ID} />,
    );
    expect(screen.getByTestId("mri-heatmap").textContent ?? "").not.toMatch(NUMERIC);
  });

  it("renders a clean empty state when there are no findings", async () => {
    await renderMRI(<UnderstandingHeatmap findings={[]} projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-heatmap-empty")).toBeInTheDocument();
  });
});

describe("MRI-05 — CAF Triangle", () => {
  it("renders the three co-equal dimensions as an SVG triangle, each labelled", async () => {
    await renderMRI(<CafTriangle caf={cafFixture} />);
    const tri = screen.getByTestId("mri-caf-triangle");
    expect(tri.querySelector("svg")).toBeTruthy();
    expect(screen.getByTestId("caf-vertex-clarity")).toBeInTheDocument();
    expect(screen.getByTestId("caf-vertex-alignment")).toBeInTheDocument();
    expect(screen.getByTestId("caf-vertex-feasibility")).toBeInTheDocument();
  });

  it("wraps the CAF assessment in an EpistemicLabel (Derived + band)", async () => {
    await renderMRI(<CafTriangle caf={cafFixture} />);
    const tri = screen.getByTestId("mri-caf-triangle");
    const label = within(tri).getAllByTestId("epistemic-label")[0];
    expect(label).toHaveAttribute("data-standing", "derived");
    // NEGATIVE: a Derived CAF is never rendered as settled/confirmed.
    expect(within(tri).queryByText(/settled|confirmed/i)).not.toBeInTheDocument();
  });

  it("renders a clean empty state when CAF is absent", async () => {
    await renderMRI(<CafTriangle caf={undefined} />);
    expect(screen.getByTestId("mri-caf-triangle-empty")).toBeInTheDocument();
  });
});

describe("MRI-06 — Understanding Timeline (CHR history trail)", () => {
  it("shows the current understanding AND prior history entries (append-only)", async () => {
    await renderMRI(
      <UnderstandingTimeline runs={analysisRunsFixture} projectId={PROJECT_ID} />,
    );
    const timeline = screen.getByTestId("mri-timeline");
    expect(timeline).toBeInTheDocument();
    const entries = within(timeline).getAllByTestId("timeline-entry");
    // current + at least one past entry both shown
    expect(entries.length).toBe(analysisRunsFixture.length);
    // the newest entry is marked as the current understanding
    expect(within(timeline).getByTestId("timeline-current")).toBeInTheDocument();
    // a prior history entry is present too
    expect(within(timeline).getByText(/run-1/)).toBeInTheDocument();
  });

  it("renders a clean empty state when there is no history yet", async () => {
    await renderMRI(<UnderstandingTimeline runs={[]} projectId={PROJECT_ID} />);
    expect(screen.getByTestId("mri-timeline-empty")).toBeInTheDocument();
  });
});

describe("MRI-07 — Understanding Dependencies (blocked / awaiting review)", () => {
  it("lists findings that block understanding, awaiting review", async () => {
    await renderMRI(
      <UnderstandingDependencies
        findings={findingsFixture}
        projectId={PROJECT_ID}
      />,
    );
    const deps = screen.getByTestId("mri-dependencies");
    expect(deps).toBeInTheDocument();
    // open (not closed/superseded) findings are surfaced as blocking dependencies
    expect(within(deps).getAllByTestId("dependency-node").length).toBeGreaterThan(0);
    // each blocking item carries its epistemic label
    expect(within(deps).getAllByTestId("epistemic-label").length).toBeGreaterThan(0);
  });

  it("renders a clean empty state when nothing is blocked / awaiting review", async () => {
    const closed = findingsFixture.map((f) => ({ ...f, status: "closed" as const }));
    await renderMRI(
      <UnderstandingDependencies findings={closed} projectId={PROJECT_ID} />,
    );
    expect(screen.getByTestId("mri-dependencies-empty")).toBeInTheDocument();
  });
});

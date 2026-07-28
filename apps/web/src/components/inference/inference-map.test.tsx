import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { InferenceMap } from "./inference-map";

const snapshot: OverviewSnapshot = {
  snapshot_id: "snapshot-map",
  analysis_run_id: "run-map",
  project_id: "project-map",
  orientation_seen: true,
  state: "current",
  summary: "Project summary.",
  artifacts: [
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "Ownership is unclear.",
      reliability: "Moderate",
      evidence_refs: [],
      basis: "inferred",
      assumptions: [
        {
          id: "ASM-MAP",
          statement: "Nobody is accountable.",
          state: "inferred",
          load_bearing: true,
          evidence_refs: [],
        },
      ],
    },
  ],
  assessment: {
    confidence_index: 50,
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "Moderate",
    alignment: "Moderate",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: {
      coverage: "Moderate",
      evidence: "Moderate",
      assessability: "Low",
    },
    confidence_direction: "unchanged",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation: "Resources limit the read.",
    resolved_issue_count: 0,
    confirmed_dependency_count: 0,
    issues: [
      {
        id: "ISS-MAP",
        artifact_type: "resources",
        dimension: "Feasibility",
        severity: "Critical",
        title: "An owner is missing",
        why: "Nobody is accountable.",
        recommendation: "Name an owner.",
        evidence_refs: [],
        clarification: "Who owns delivery?",
        status: "open",
      },
    ],
  },
  published_at: new Date().toISOString(),
};

afterEach(cleanup);

describe("InferenceMap", () => {
  it("renders document provenance, assumptions, structure, and movement", () => {
    render(<InferenceMap snapshot={snapshot} />);

    expect(screen.getByRole("heading", { name: "Inference map" })).toBeInTheDocument();
    expect(screen.getByText("Where OSLO inferred")).toBeInTheDocument();
    expect(screen.getByLabelText("0 grounded and 1 inferred")).toBeInTheDocument();
    expect(screen.getByText("Nobody is accountable.")).toBeInTheDocument();
    expect(screen.getByText("Unowned parties")).toBeInTheDocument();
    expect(screen.getByText("OSLO inferred")).toBeInTheDocument();
  });

  it("opens the issue tied to an assumption", () => {
    const onOpenIssue = vi.fn();
    render(<InferenceMap onOpenIssue={onOpenIssue} snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("button", { name: /An owner is missing/ }));
    expect(onOpenIssue).toHaveBeenCalledWith(
      expect.objectContaining({ id: "ISS-MAP" }),
      expect.any(HTMLElement),
    );
  });
});

import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { IssueProposalSummary, OverviewSnapshot } from "@/lib/server/oslo-api";

import { FullPlanWorkspace } from "./full-plan-workspace";

const snapshot = {
  project_id: "project-full-plan",
  project_title: "Atlas launch",
  analysis_run_id: "run-full-plan",
  snapshot_id: "snapshot-full-plan",
  published_at: "2026-08-17T08:30:00Z",
  state: "current",
  freshness: { state: "current", pending_count: 0 },
  assessment: {
    integrity: { level: "Fragile", limiting_pillar: "Grounding" },
  },
  artifacts: [
    {
      artifact_type: "work_breakdown",
      title: "Work breakdown",
      summary: "Delivery hierarchy.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: [],
      content: {
        sections: [
          {
            heading: "Delivery",
            body: "",
            bullets: [],
            columns: ["WBS", "Item"],
            rows: [
              ["1.0", "Commerce platform"],
              ["1.1", "Checkout"],
              ["1.1.1", "Implement payment gateway"],
              ["1.1.2", "Test payment recovery"],
            ],
            row_ids: ["deliverable-1", "package-1", "task-1", "task-2"],
            row_states: ["confirmed", "confirmed", "confirmed", "inferred"],
            row_provenance: [
              "confirmed_by_user",
              "confirmed_by_user",
              "confirmed_by_user",
              "from_oslo",
            ],
          },
        ],
      },
    },
    {
      artifact_type: "schedule",
      title: "Schedule",
      summary: "Dates.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: [],
      content: {
        sections: [
          {
            heading: "Milestones",
            body: "",
            bullets: [],
            columns: ["Milestone", "Start", "End"],
            rows: [
              ["Implement payment gateway", "2026-09-01", "2026-09-12"],
              ["Test payment recovery", "", ""],
            ],
            row_ids: ["task-1", "task-2"],
          },
        ],
      },
    },
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "Owners.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: [],
      content: {
        sections: [
          {
            heading: "People",
            body: "",
            bullets: [],
            columns: ["Task", "Owner"],
            rows: [
              ["Implement payment gateway", "Dana"],
              ["Test payment recovery", ""],
            ],
            row_ids: ["task-1", "task-2"],
          },
        ],
      },
    },
  ],
} as unknown as OverviewSnapshot;

const proposal = {
  id: "proposal-task-3",
  issue_id: "issue-task-3",
  kind: "optional",
  resolver_key: "backup-provider",
  title: "Add backup payment provider",
  rationale: "Optional resilience task.",
  artifact_type: "work_breakdown",
  load_bearing: false,
  accepted: false,
  rejected: false,
  surface: "artifact",
} satisfies IssueProposalSummary;

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ entitled: false, configured: false, preview: [] }),
  }));
  Object.defineProperty(URL, "createObjectURL", {
    configurable: true,
    value: vi.fn(() => "blob:full-plan"),
  });
  Object.defineProperty(URL, "revokeObjectURL", {
    configurable: true,
    value: vi.fn(),
  });
  vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => undefined);
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("FullPlanWorkspace", () => {
  it("renders the prototype table with explicit incomplete and proposed states", () => {
    render(<FullPlanWorkspace proposals={[proposal]} snapshot={snapshot} />);

    expect(
      screen.getByRole("navigation", { name: "Full plan breadcrumb" }),
    ).toHaveTextContent("Outcome›Execution›Full plan · export");
    expect(
      screen.getByRole("note", { name: "Full plan status" }),
    ).toHaveTextContent("Grounding is the current gate");
    expect(screen.getByRole("heading", { name: "Full plan · export" })).toBeInTheDocument();
    const table = screen.getByRole("table", { name: "Full execution plan" });
    expect(within(table).getByText("Implement payment gateway")).toBeInTheDocument();
    expect(within(table).getAllByText("— unowned")).toHaveLength(2);
    expect(within(table).getAllByText("unscheduled")).toHaveLength(2);
    expect(within(table).getByText("Add backup payment provider")).toBeInTheDocument();
    expect(within(table).getAllByText("proposed")).toHaveLength(1);
  });

  it("downloads the selected real format and records the export without reanalysis", async () => {
    render(<FullPlanWorkspace proposals={[]} snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("button", { name: "Export plan" }));
    const dialog = screen.getByRole("dialog", { name: "Export your plan" });
    fireEvent.click(within(dialog).getByRole("button", { name: "CSV" }));
    fireEvent.click(within(dialog).getByRole("button", { name: "Download CSV" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "/api/projects/project-full-plan/report/exports",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ format: "csv", surface: "full_plan" }),
        }),
      );
    });
    expect(fetch).not.toHaveBeenCalledWith(
      expect.stringContaining("reanalysis"),
      expect.anything(),
    );
    expect(screen.getByRole("status")).toHaveTextContent("CSV export downloaded");
  });

  it("links an empty plan back to Work Breakdown", () => {
    render(
      <FullPlanWorkspace
        proposals={[]}
        snapshot={{ ...snapshot, artifacts: [] }}
      />,
    );

    expect(screen.getByRole("link", { name: "Open Work Breakdown" })).toHaveAttribute(
      "href",
      "/projects/project-full-plan/artifacts/work_breakdown",
    );
  });
});

import { describe, expect, it } from "vitest";

import type {
  ArtifactWorkspaceSummary,
  IssueProposalSummary,
  OverviewSnapshot,
} from "@/lib/server/oslo-api";

import {
  buildFullPlanProjection,
  withCurrentFullPlanArtifacts,
} from "./full-plan-projection";

const snapshot = {
  project_id: "project-full-plan",
  project_title: "Atlas launch",
  analysis_run_id: "run-full-plan",
  snapshot_id: "snapshot-full-plan",
  published_at: "2026-08-17T08:30:00Z",
  artifacts: [
    {
      artifact_type: "work_breakdown",
      title: "Work breakdown",
      summary: "The sequenced delivery hierarchy.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: ["document:plan:page:2"],
      content: {
        sections: [
          {
            heading: "Delivery hierarchy",
            body: "",
            bullets: [],
            columns: ["WBS", "Item", "Note"],
            rows: [
              ["1.0", "Commerce platform", ""],
              ["1.1", "Checkout", ""],
              ["1.1.1", "Implement payment gateway", "PCI boundary"],
              ["1.1.2", "Test payment recovery", "Failure paths"],
            ],
            row_ids: ["deliverable-1", "package-1", "task-1", "task-2"],
            row_states: ["confirmed", "confirmed", "confirmed", "inferred"],
            row_provenance: [
              "confirmed_by_user",
              "confirmed_by_user",
              "confirmed_by_user",
              "from_oslo",
            ],
            row_evidence_refs: [
              ["document:plan:page:2"],
              ["document:plan:page:2"],
              ["document:plan:page:3"],
              ["document:plan:page:4"],
            ],
          },
        ],
      },
    },
    {
      artifact_type: "schedule",
      title: "Schedule",
      summary: "Delivery dates.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: ["document:schedule:page:1"],
      content: {
        sections: [
          {
            heading: "Milestones",
            body: "",
            bullets: [],
            columns: ["Milestone", "Owner", "Start", "End", "Status"],
            rows: [
              ["Implement payment gateway", "Alex", "2026-09-01", "2026-09-12", "confirmed"],
              ["Test payment recovery", "", "", "", "planned"],
            ],
            row_ids: ["task-1", "task-2"],
            row_evidence_refs: [
              ["document:schedule:page:1"],
              ["document:schedule:page:2"],
            ],
          },
        ],
      },
    },
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "Delivery ownership.",
      reliability: "Moderate",
      basis: "Documented",
      evidence_refs: ["document:resources:page:1"],
      content: {
        sections: [
          {
            heading: "People",
            body: "",
            bullets: [],
            columns: ["Task", "Owner", "Status"],
            rows: [
              ["Implement payment gateway", "Dana", "confirmed"],
              ["Test payment recovery", "", "unowned"],
            ],
            row_ids: ["task-1", "task-2"],
            row_evidence_refs: [
              ["document:resources:page:1"],
              ["document:resources:page:2"],
            ],
          },
        ],
      },
    },
  ],
} as unknown as OverviewSnapshot;

const proposedTask = {
  id: "proposal-task-3",
  issue_id: "issue-task-3",
  kind: "optional",
  resolver_key: "add-backup-provider",
  title: "Add backup payment provider",
  rationale: "Reduces recovery risk without entering the plan until accepted.",
  artifact_type: "work_breakdown",
  load_bearing: false,
  accepted: false,
  rejected: false,
  surface: "artifact",
} satisfies IssueProposalSummary;

describe("buildFullPlanProjection", () => {
  it("projects the latest authored artifact versions instead of the older analysis snapshot", () => {
    const currentWorkBreakdown = {
      artifact_type: "work_breakdown",
      title: "Work breakdown",
      content: {
        sections: [
          {
            heading: "Current delivery hierarchy",
            body: "",
            bullets: [],
            columns: ["WBS", "Item"],
            rows: [["9.0", "Current authored task"]],
            row_ids: ["current-task"],
            row_states: ["confirmed"],
            row_provenance: ["confirmed_by_user"],
          },
        ],
      },
      version: 4,
      provenance: "confirmed_by_user",
      reliability: "High",
      basis: "Confirmed by the owner",
      evidence_refs: ["decision:current"],
      issues: [],
      updated_at: "2026-08-17T10:00:00Z",
    } as ArtifactWorkspaceSummary;

    const hydrated = withCurrentFullPlanArtifacts(snapshot, [currentWorkBreakdown]);
    const projection = buildFullPlanProjection(hydrated, []);

    expect(projection.rows).toHaveLength(1);
    expect(projection.rows[0]).toMatchObject({
      id: "current-task",
      task: "Current authored task",
      state: "yours",
    });
  });

  it("joins each WBS leaf to its schedule and resource facets by shared row ID", () => {
    const projection = buildFullPlanProjection(snapshot, []);

    expect(projection.rows).toHaveLength(2);
    expect(projection.rows[0]).toMatchObject({
      id: "task-1",
      task: "Implement payment gateway",
      workPackage: "Checkout",
      deliverable: "Commerce platform",
      owner: "Dana",
      start: "2026-09-01",
      due: "2026-09-12",
      schedule: "2026-09-01 – 2026-09-12",
      state: "yours",
      note: "PCI boundary",
    });
    expect(projection.rows[0].provenance).toEqual([
      "document:plan:page:3",
      "document:schedule:page:1",
      "document:resources:page:1",
    ]);
    expect(projection.rows[1]).toMatchObject({
      id: "task-2",
      owner: null,
      schedule: null,
      state: "inferred",
    });
  });

  it("keeps undecided OSLO task proposals visibly outside the governed plan", () => {
    const projection = buildFullPlanProjection(snapshot, [proposedTask]);

    expect(projection.rows.at(-1)).toMatchObject({
      id: "proposal-task-3",
      task: "Add backup payment provider",
      workPackage: "OSLO proposes",
      deliverable: "Optional addition",
      owner: null,
      schedule: null,
      state: "proposed",
    });
    expect(projection.confirmedCount).toBe(1);
    expect(projection.inferredCount).toBe(1);
    expect(projection.proposedCount).toBe(1);
  });

  it("keeps a terminal WBS work package when the source has no child task rows", () => {
    const packageOnly = {
      ...snapshot,
      artifacts: snapshot.artifacts.map((artifact) =>
        artifact.artifact_type === "work_breakdown"
          ? {
              ...artifact,
              content: {
                sections: [
                  {
                    heading: "Delivery hierarchy",
                    body: "",
                    bullets: [],
                    columns: ["WBS", "Work package evidence"],
                    rows: [["1.0", "Mobilization and governance"]],
                    row_ids: ["package-leaf-1"],
                    row_states: ["confirmed"],
                    row_provenance: ["confirmed_by_user"],
                    row_evidence_refs: [["document:plan:page:2"]],
                  },
                ],
              },
            }
          : artifact,
      ),
    } as OverviewSnapshot;

    const projection = buildFullPlanProjection(packageOnly, []);

    expect(projection.rows).toHaveLength(1);
    expect(projection.rows[0]).toMatchObject({
      id: "package-leaf-1",
      task: "Mobilization and governance",
      workPackage: "Mobilization and governance",
      deliverable: "Delivery hierarchy",
    });
  });

  it("returns an empty projection when no Work Breakdown exists", () => {
    const projection = buildFullPlanProjection(
      { ...snapshot, artifacts: snapshot.artifacts.filter((artifact) => artifact.artifact_type !== "work_breakdown") },
      [],
    );

    expect(projection.rows).toEqual([]);
    expect(projection.missingWorkBreakdown).toBe(true);
  });
});

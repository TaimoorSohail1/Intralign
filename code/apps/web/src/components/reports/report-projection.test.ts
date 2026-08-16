import { describe, expect, it } from "vitest";

import type { OverviewSnapshot, ProjectHistory } from "@/lib/server/oslo-api";

import { projectReportProjection } from "./report-projection";

const snapshot = {
  snapshot_id: "snapshot-slice-7",
  analysis_run_id: "run-slice-7",
  project_id: "project-slice-7",
  project_title: "Atlas launch",
  published_at: "2026-08-15T10:30:00Z",
  orientation_seen: true,
  state: "current",
  summary: "The launch is viable but rests on unconfirmed ownership.",
  artifacts: [],
  assessment: {
    confidence_index: 52,
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "Moderate",
    alignment: "High",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: { coverage: "Moderate", evidence: "Moderate", assessability: "Moderate" },
    confidence_direction: "unchanged",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation: "Ownership remains inferred.",
    resolved_issue_count: 1,
    confirmed_dependency_count: 1,
    integrity: {
      level: "Fragile",
      limiting_pillar: "Grounding",
      decomposition: [
        { key: "Viability", band: "Developing", basis: 2, why: ["The path is defined."] },
        { key: "Grounding", band: "Fragile", basis: 0, why: ["Ownership is inferred."] },
        { key: "Adaptability", band: "Weak", basis: 1, why: ["One checkpoint exists."] },
      ],
      posture: "moment-in-time",
      tracking: "pending-execution",
    },
    issues: [
      {
        id: "issue-low",
        artifact_type: "schedule",
        dimension: "Feasibility",
        severity: "Moderate",
        title: "Milestone sequence is unclear",
        why: "Dates conflict.",
        recommendation: "Reconcile the milestone sequence.",
        evidence_refs: [],
        status: "open",
        exposure_rank: 2,
      },
      {
        id: "issue-top",
        artifact_type: "resources",
        dimension: "Grounding",
        severity: "Critical",
        title: "Delivery owner is unconfirmed",
        why: "The named role has not accepted accountability.",
        recommendation: "Confirm the accountable delivery owner.",
        evidence_refs: [],
        status: "open",
        exposure_rank: 1,
      },
      {
        id: "issue-resolved",
        artifact_type: "requirements",
        dimension: "Grounding",
        severity: "Moderate",
        title: "Data steward is missing",
        why: "No owner was recorded.",
        recommendation: "Name the data steward.",
        evidence_refs: [],
        status: "resolved",
        selected_resolution: "Avery owns data stewardship.",
        attested_by: { id: "user-1", display_name: "Idris", role: "owner" },
      },
    ],
  },
  provenance: {
    schema_version: 1,
    artifacts: [],
    assumptions: [
      {
        id: "a1",
        artifact_type: "resources",
        text: "Avery owns delivery.",
        issue_id: "issue-top",
        issue_title: "Delivery owner is unconfirmed",
        load_bearing: true,
        state: "inferred",
      },
      {
        id: "a2",
        artifact_type: "requirements",
        text: "Avery owns data stewardship.",
        issue_id: "issue-resolved",
        issue_title: "Data steward is missing",
        load_bearing: true,
        state: "confirmed",
      },
      {
        id: "a3",
        artifact_type: "intent",
        text: "The launch targets enterprise buyers.",
        issue_id: null,
        issue_title: null,
        load_bearing: false,
        state: "inferred",
      },
    ],
    grounded_claims: 1,
    inferred_claims: 2,
    total_claims: 3,
    load_bearing_inferences: 1,
    structure: { unconfirmed_dependencies: 1, unowned_parties: 1, untraceable_numbers: 0 },
    this_week: { user_grounded: 1, oslo_inferred: 2 },
  },
} satisfies OverviewSnapshot;

const history = {
  project_id: snapshot.project_id,
  groups: [
    {
      run_id: snapshot.analysis_run_id,
      kind: "extended",
      status: "completed",
      current: true,
      occurred_at: snapshot.published_at,
      changes: [],
      events: [
        {
          id: 1,
          category: "decisions",
          event_type: "issue.resolved",
          summary: "Confirmed Avery as data steward",
          detail: "The requirement now rests on owner evidence.",
          actor_type: "user",
          artifact_type: "requirements",
          artifact_version: 2,
          issue_id: "issue-resolved",
          occurred_at: snapshot.published_at,
        },
      ],
    },
  ],
  trend: [],
  next_cursor: null,
} satisfies ProjectHistory;

describe("projectReportProjection", () => {
  it("projects one stable, explicitly-scoped read without mutating the source", () => {
    const before = JSON.stringify(snapshot);

    const projection = projectReportProjection(snapshot, history);

    expect(projection.analysisAt).toBe("2026-08-15T10:30:00Z");
    expect(projection.openIssues.map((issue) => issue.id)).toEqual(["issue-top", "issue-low"]);
    expect(projection.criticalGrounding).toEqual({ grounded: 1, total: 2 });
    expect(projection.evidenceRegister).toEqual({ grounded: 1, inferred: 2, total: 3 });
    expect(projection.decisions[0]).toMatchObject({
      title: "Confirmed Avery as data steward",
      actor: "You",
    });
    expect(projection.nextMove).toMatchObject({ id: "issue-top" });
    expect(JSON.stringify(snapshot)).toBe(before);
  });

  it("reconciles stale open-item counts in the retained analysis summary", () => {
    const staleSnapshot = {
      ...snapshot,
      summary: "The read is low confidence; 13 open findings identify the main uncertainty.",
    } satisfies OverviewSnapshot;

    const projection = projectReportProjection(staleSnapshot, history);

    expect(projection.summary).toContain("2 open findings");
    expect(projection.summary).not.toContain("13 open findings");
  });

  it("anchors a retained governed summary to the current project title", () => {
    const staleSnapshot = {
      ...snapshot,
      summary:
        "DevNorth 2026 is a developer conference. At the expanded stage, OSLO mapped the supplied evidence into 7 plan artifacts; 13 open findings identify the main uncertainty.",
    } satisfies OverviewSnapshot;

    const projection = projectReportProjection(staleSnapshot, history);

    expect(projection.summary).toMatch(/^Atlas launch\. At the expanded stage,/);
    expect(projection.summary).toContain("2 open findings");
    expect(projection.summary).not.toContain("DevNorth");
  });
});

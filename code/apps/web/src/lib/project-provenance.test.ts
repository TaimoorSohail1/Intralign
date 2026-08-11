import { describe, expect, it } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { buildProjectProvenance } from "./project-provenance";

const snapshot: OverviewSnapshot = {
  snapshot_id: "snapshot-provenance",
  analysis_run_id: "run-provenance",
  project_id: "project-provenance",
  orientation_seen: true,
  state: "current",
  summary: "A project read.",
  artifacts: [
    {
      artifact_type: "scope",
      title: "Scope",
      summary: "The scope is coherent but not fully confirmed.",
      reliability: "Moderate",
      evidence_refs: ["document:brief:page:1:fragment:1"],
      basis: "derived",
    },
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "Ownership is missing.",
      reliability: "Moderate",
      evidence_refs: [],
      basis: "inferred",
      assumptions: [
        {
          id: "ASM-OWNER",
          statement: "No accountable owner is named.",
          state: "inferred",
          load_bearing: true,
          evidence_refs: [],
        },
      ],
    },
  ],
  assessment: {
    confidence_index: 54,
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "High",
    alignment: "Moderate",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: {
      coverage: "Moderate",
      evidence: "Moderate",
      assessability: "Low",
    },
    confidence_direction: "strengthened",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation: "Resources constrain the read.",
    resolved_issue_count: 0,
    confirmed_dependency_count: 0,
    issues: [
      {
        id: "ISS-OWNER",
        artifact_type: "resources",
        dimension: "Feasibility",
        severity: "Critical",
        title: "Accountable delivery owner is missing",
        why: "No accountable owner is named.",
        recommendation: "Name an owner.",
        evidence_refs: [],
        clarification: "Who owns delivery?",
        status: "open",
      },
    ],
  },
  published_at: "2026-07-28T10:00:00Z",
};

describe("buildProjectProvenance", () => {
  it("derives one consistent provenance ledger from the published snapshot", () => {
    const result = buildProjectProvenance(snapshot);

    expect(result.groundedClaims).toBe(1);
    expect(result.inferredClaims).toBe(1);
    expect(result.totalClaims).toBe(2);
    expect(result.loadBearingInferences).toBe(1);
    expect(result.structure.unownedParties).toBe(1);
    expect(result.artifacts.find((artifact) => artifact.artifactType === "resources"))
      .toMatchObject({ grounded: 0, inferred: 1, verifyFirst: true });
  });

  it("puts load-bearing assumptions first and keeps their issue link", () => {
    const result = buildProjectProvenance(snapshot);

    expect(result.assumptions[0]).toMatchObject({
      issueId: "ISS-OWNER",
      loadBearing: true,
      text: "No accountable owner is named.",
    });
  });

  it("counts an evidence-backed source conflict as grounded disagreement", () => {
    const result = buildProjectProvenance({
      ...snapshot,
      artifacts: [
        {
          artifact_type: "schedule",
          title: "Schedule",
          summary: "Two documented options remain unresolved.",
          reliability: "High",
          evidence_refs: ["document:roadmap:page:2:fragment:0"],
          basis: "supported",
          content: {
            sections: [
              {
                heading: "Delivery options",
                body: "",
                bullets: [],
                columns: ["Option", "Duration"],
                rows: [["Baseline", "14 months"]],
                evidence_refs: ["document:roadmap:page:2:fragment:0"],
                row_evidence_refs: [["document:roadmap:page:2:fragment:0"]],
                row_states: ["conflicting"],
              },
            ],
          },
        },
      ],
    });

    expect(result.groundedClaims).toBe(1);
    expect(result.inferredClaims).toBe(0);
    expect(
      result.artifacts.find((artifact) => artifact.artifactType === "schedule"),
    ).toMatchObject({ grounded: 1, inferred: 0 });
  });

  it("does not count a confirmed assumption as an OSLO inference", () => {
    const result = buildProjectProvenance({
      ...snapshot,
      artifacts: [
        {
          ...snapshot.artifacts[1],
          assumptions: [
            {
              id: "ASM-CONFIRMED",
              statement: "The sponsor owns the decision.",
              state: "confirmed",
              load_bearing: true,
              evidence_refs: ["document:brief:page:2:fragment:0"],
            },
          ],
        },
      ],
    });

    expect(result.loadBearingInferences).toBe(0);
  });

  it("uses the server-owned provenance contract when it is present", () => {
    const result = buildProjectProvenance({
      ...snapshot,
      provenance: {
        schema_version: 1,
        artifacts: [
          {
            artifact_type: "scope",
            grounded: 9,
            inferred: 2,
            total: 11,
            verify_first: false,
          },
        ],
        assumptions: [
          {
            id: "ASM-SERVER",
            artifact_type: "scope",
            text: "A server-governed assumption.",
            issue_id: null,
            issue_title: null,
            load_bearing: false,
            state: "inferred",
          },
        ],
        grounded_claims: 9,
        inferred_claims: 2,
        total_claims: 11,
        load_bearing_inferences: 0,
        structure: {
          unconfirmed_dependencies: 1,
          unowned_parties: 2,
          untraceable_numbers: 3,
        },
        this_week: {
          user_grounded: 4,
          oslo_inferred: 2,
        },
      },
    });

    expect(result.groundedClaims).toBe(9);
    expect(result.inferredClaims).toBe(2);
    expect(result.structure.unownedParties).toBe(2);
    expect(result.assumptions[0]?.id).toBe("ASM-SERVER");
  });
});

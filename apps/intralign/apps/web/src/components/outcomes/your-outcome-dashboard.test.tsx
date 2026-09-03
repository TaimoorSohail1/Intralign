import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it } from "vitest";

import type {
  CollaborationRollUpProjection,
  OverviewSnapshot,
  ProjectOutcomeSummary,
} from "@/lib/server/oslo-api";

import { buildYourOutcomeProjection } from "./your-outcome-projection";
import { YourOutcomeDashboard } from "./your-outcome-dashboard";

afterEach(cleanup);

const snapshot: OverviewSnapshot = {
  snapshot_id: "snapshot-1",
  analysis_run_id: "run-2",
  project_id: "project-1",
  project_title: "Atlas launch",
  orientation_seen: true,
  state: "current",
  summary: "Launch Atlas for wholesale customers.",
  artifacts: [
    {
      artifact_type: "intent",
      title: "Intent",
      summary: "Launch Atlas for wholesale customers.",
      reliability: "High",
      basis: "supported",
      evidence_refs: ["source:1"],
      content: {
        sections: [
          {
            heading: "Outcomes",
            body: "",
            bullets: ["Launch Atlas", "Reduce handling time", "Grow adoption"],
            columns: [],
            rows: [],
          },
          {
            heading: "Goals",
            body: "",
            bullets: ["Launch safely", "Reach the target segment"],
            columns: [],
            rows: [],
          },
          {
            heading: "Success criteria",
            body: "",
            bullets: ["420 customers onboarded"],
            columns: [],
            rows: [],
          },
          {
            heading: "KPIs & metrics",
            body: "",
            bullets: ["Monthly active accounts", "Eligible orders through portal"],
            columns: [],
            rows: [],
          },
        ],
      },
    },
  ],
  assessment: {
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "Moderate",
    alignment: "Moderate",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: { coverage: "High", evidence: "Moderate", assessability: "Moderate" },
    confidence_direction: "strengthened",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation: "Grounding is the limiting pillar.",
    resolved_issue_count: 1,
    confirmed_dependency_count: 1,
    integrity: {
      level: "Fragile",
      limiting_pillar: "Grounding",
      decomposition: [
        { key: "Grounding", band: "Fragile", basis: 0.25, why: ["1 of 4 grounded"] },
        { key: "Adaptability", band: "Weak", basis: 0.5, why: ["1 of 2 checkpoints"] },
        { key: "Viability", band: "Developing", basis: 0.75, why: ["3 of 4 clear"] },
      ],
      posture: "moment-in-time",
      tracking: "pending-execution",
    },
    issues: [
      {
        id: "ISS-1",
        artifact_type: "intent",
        dimension: "feasibility",
        severity: "Critical",
        title: "Order-handling benefit is not measurable or owned",
        why: "Define the baseline and accountable owner.",
        recommendation: "Define the measure.",
        evidence_refs: [],
        status: "open",
      },
      {
        id: "ISS-2",
        artifact_type: "resources",
        dimension: "alignment",
        severity: "Moderate",
        title: "Fallback capacity is not confirmed",
        why: "The fallback owner is not named.",
        recommendation: "Name the fallback owner.",
        evidence_refs: [],
        status: "routed",
      },
    ],
  },
  first_run: {
    first_run: false,
    onboarded: true,
    grounding_act_count: 3,
    ever_unlocked: true,
    unlock_threshold: 2,
    freeze_on: false,
  },
  read_moved_notifications: [
    {
      id: "notification-1",
      analysis_run_id: "run-2",
      pillar_deltas: [{ pillar: "Grounding", from: "Weak", to: "Fragile" }],
      settled_causes: ["Sponsor commitments were confirmed"],
      previous_band: "Weak",
      current_band: "Fragile",
      delivery_kind: "durable",
      seen_at: null,
      expires_at: null,
      created_at: "2026-08-16T10:00:00Z",
    },
  ],
  provenance: {
    schema_version: 1,
    artifacts: [],
    assumptions: [],
    grounded_claims: 1,
    inferred_claims: 3,
    total_claims: 4,
    load_bearing_inferences: 2,
    grounding: {
      grounded: 0,
      addressed: 0,
      routed: 1,
      inferred: 1,
      total: 2,
      basis: 0,
      band: "Fragile",
    },
    structure: {
      unconfirmed_dependencies: 0,
      unowned_parties: 0,
      untraceable_numbers: 0,
    },
    this_week: { user_grounded: 0, oslo_inferred: 0 },
  },
  published_at: "2026-08-16T10:00:00Z",
};

const outcomes: ProjectOutcomeSummary[] = [
  {
    id: "outcome-1",
    workspace_id: "workspace-1",
    project_id: "project-1",
    title: "Launch Atlas for wholesale customers",
    status: "active",
    is_primary: true,
    provenance: "declared",
    created_at: "2026-08-15T10:00:00Z",
    archived_at: null,
  },
];

const rollUp: CollaborationRollUpProjection = {
  project_id: "project-1",
  actor_role: "owner",
  integrity: snapshot.assessment.integrity,
  trend: "strengthened",
  decision_queue: [
    {
      issue_id: "ISS-1",
      title: "Order-handling benefit is not measurable or owned",
      detail: "Define the baseline and accountable owner.",
      artifact_type: "intent",
      pillar: "Viability",
      state: "inferred",
      exposure_rank: 100,
      href: "/projects/project-1/issues?issue=ISS-1",
    },
    {
      issue_id: "ISS-2",
      title: "Fallback capacity is not confirmed",
      artifact_type: "resources",
      pillar: "Grounding",
      state: "routed",
      exposure_rank: 40,
      href: "/projects/project-1/issues?issue=ISS-2",
    },
  ],
  reviewers: [],
  who_is_grounding_what: [
    {
      reviewer_name: "Nora Evans",
      issue_id: "ISS-2",
      state: "awaiting",
      href: "/projects/project-1/issues?issue=ISS-2",
    },
  ],
  rests_on: { grounded: 1, addressed: 0, routed: 1, inferred: 2 },
};

describe("Your Outcome dashboard", () => {
  it("builds one read-only projection without leaking held outcome titles", () => {
    const projection = buildYourOutcomeProjection({ snapshot, outcomes, rollUp });

    expect(projection.primary_outcome?.title).toBe("Launch Atlas for wholesale customers");
    expect(projection.held_outcome_count).toBe(2);
    expect(projection.intent_counts).toEqual({ goals: 2, success_criteria: 1, kpis: 2 });
    expect(projection.needs_you.map((item) => item.issue_id)).toEqual(["ISS-1", "ISS-2"]);
    expect(projection.needs_you.map((item) => item.severity)).toEqual(["Critical", "Moderate"]);
    expect(projection.in_motion[0]).toMatchObject({
      issue_title: "Fallback capacity is not confirmed",
      reviewer_name: "Nora Evans",
    });
    expect(JSON.stringify(projection)).not.toContain("Reduce handling time");
    expect(JSON.stringify(projection)).not.toContain("Grow adoption");
    expect(projection.grounding).toEqual({ grounded: 0, total: 2 });
  });

  it("does not silently promote the first active outcome when no primary is declared", () => {
    const projection = buildYourOutcomeProjection({
      snapshot,
      outcomes: outcomes.map((outcome) => ({ ...outcome, is_primary: false })),
      rollUp,
    });

    expect(projection.primary_outcome).toBeNull();
    render(<YourOutcomeDashboard data={projection} />);
    expect(screen.getByText("No outcome is defined yet.")).toBeInTheDocument();
    expect(screen.queryByText("Primary")).not.toBeInTheDocument();
  });

  it("does not present an inferred missing-purpose statement as the primary outcome", () => {
    const projection = buildYourOutcomeProjection({
      snapshot,
      outcomes: outcomes.map((outcome, index) =>
        index === 0
          ? {
              ...outcome,
              title: "The conference purpose is not defined.",
              provenance: "inferred",
            }
          : outcome,
      ),
      rollUp,
    });

    expect(projection.primary_outcome).toBeNull();
    render(<YourOutcomeDashboard data={projection} />);
    expect(screen.getByText("No outcome is defined yet.")).toBeInTheDocument();
    expect(screen.queryByText("The conference purpose is not defined.")).not.toBeInTheDocument();
  });

  it("describes an unchanged integrity band without claiming it moved", () => {
    const unchangedSnapshot: OverviewSnapshot = {
      ...snapshot,
      read_moved_notifications: [
        {
          ...snapshot.read_moved_notifications![0],
          settled_causes: [],
          previous_band: "Fragile",
          current_band: "Fragile",
        },
      ],
    };

    const projection = buildYourOutcomeProjection({
      snapshot: unchangedSnapshot,
      outcomes,
      rollUp,
    });

    expect(projection.unseen_changes[0]?.summary).toBe(
      "Outcome Integrity remains Fragile",
    );
  });

  it("keeps every secondary outcome and disclosure nudge hidden during first-run freeze", () => {
    const frozenSnapshot: OverviewSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        ever_unlocked: false,
        unlock_threshold: 2,
        freeze_on: true,
      },
    };
    const secondaryOutcomes: ProjectOutcomeSummary[] = [
      ...outcomes,
      {
        ...outcomes[0],
        id: "outcome-2",
        title: "Reduce handling time",
        is_primary: false,
      },
    ];

    const projection = buildYourOutcomeProjection({
      snapshot: frozenSnapshot,
      outcomes: secondaryOutcomes,
      rollUp,
    });
    render(<YourOutcomeDashboard data={projection} />);

    expect(projection.visible_secondary_outcomes).toEqual([]);
    expect(projection.held_outcome_count).toBe(0);
    expect(screen.queryByText("Reduce handling time")).not.toBeInTheDocument();
    expect(screen.queryByText(/OSLO also read/i)).not.toBeInTheDocument();
  });

  it("keeps held-outcome disclosure neutral and free of tier or price copy", () => {
    const projection = buildYourOutcomeProjection({ snapshot, outcomes, rollUp });
    render(<YourOutcomeDashboard data={projection} />);

    const currentOutcome = screen.getByRole("region", { name: "Current outcome" });
    expect(within(currentOutcome).getByText(/OSLO also read 2 more outcomes/i)).toBeInTheDocument();
    expect(currentOutcome).not.toHaveTextContent(/Basic|Free|\$|month/i);
  });

  it("counts Intent groups with the same priority as the artifact workspace", () => {
    const groupedSnapshot: OverviewSnapshot = {
      ...snapshot,
      artifacts: [
        {
          ...snapshot.artifacts[0],
          content: {
            sections: [
              {
                heading: "Business outcomes and success measures",
                body: "",
                bullets: [],
                columns: ["Objective", "Measure", "Target"],
                rows: [
                  ["OBJ-01", "Eligible orders through portal", "80%"],
                  ["OBJ-02", "Monthly active accounts", "300"],
                  ["OBJ-03", "Orders needing correction", "2%"],
                  ["OBJ-04", "Severity 1 incidents", "0"],
                  ["OBJ-05", "Handling reduction", "30"],
                ],
              },
            ],
          },
        },
      ],
    };

    const projection = buildYourOutcomeProjection({
      snapshot: groupedSnapshot,
      outcomes,
      rollUp,
    });

    expect(projection.intent_counts).toEqual({ goals: 0, success_criteria: 0, kpis: 5 });
  });

  it("matches the prototype information hierarchy and routes every write to its governed home", () => {
    const projection = buildYourOutcomeProjection({ snapshot, outcomes, rollUp });
    render(<YourOutcomeDashboard data={projection} />);

    expect(screen.getByRole("heading", { name: "Your Outcome" })).toBeInTheDocument();
    expect(screen.getByText("Launch Atlas for wholesale customers")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Manage in Intent" })).toHaveAttribute(
      "href",
      "/projects/project-1/artifacts/intent?focus=primary-outcome&return=outcome",
    );
    expect(screen.getByRole("link", { name: /Review them now/i })).toHaveAttribute(
      "href",
      "/projects/project-1/artifacts/intent?review=held-outcomes&return=outcome",
    );
    expect(screen.getByRole("link", { name: /Declare an outcome/i })).toHaveAttribute(
      "href",
      "/projects/project-1/artifacts/intent?new=outcome&return=outcome",
    );

    const needsYou = screen.getByRole("region", { name: "Needs you" });
    expect(within(needsYou).getByRole("link", { name: /Order-handling benefit/i })).toHaveAttribute(
      "href",
      "/projects/project-1/issues?issue=ISS-1",
    );
    expect(screen.getByRole("link", { name: "Full history" })).toHaveAttribute(
      "href",
      "/projects/project-1/history?focus=since-last-looked",
    );
    expect(screen.getByText(/read-only/i)).toBeInTheDocument();
  });

  it("reveals lower-stakes calls with complete prototype rows and an honest keyboard disclosure", async () => {
    const projection = buildYourOutcomeProjection({ snapshot, outcomes, rollUp });
    const user = userEvent.setup();
    const rendered = render(<YourOutcomeDashboard data={projection} />);
    const dashboard = within(rendered.container);
    const needsYou = within(dashboard.getByRole("region", { name: "Needs you" }));

    expect(needsYou.queryByRole("link", { name: /Fallback capacity is not confirmed/i })).not.toBeInTheDocument();
    const showMore = needsYou.getByRole("button", {
      name: /Show 1 more, lower stakes — these can wait/i,
    });
    expect(showMore).toHaveAttribute("aria-expanded", "false");

    showMore.focus();
    await user.keyboard("{Enter}");

    const lowerStakeCall = needsYou
      .getByText("Fallback capacity is not confirmed")
      .closest("a");
    expect(lowerStakeCall).not.toBeNull();
    if (!lowerStakeCall) throw new Error("Expected a lower-stakes decision link");
    expect(within(lowerStakeCall).getByText("Moderate")).toBeInTheDocument();
    expect(within(lowerStakeCall).getByText("The fallback owner is not named.")).toBeInTheDocument();
    expect(within(lowerStakeCall).getByText("Decide in the read →")).toBeInTheDocument();
    const showFewer = needsYou.getByRole("button", { name: "Show fewer" });
    expect(showFewer).toHaveAttribute("aria-expanded", "true");

    showFewer.focus();
    await user.keyboard("{Enter}");
    expect(needsYou.queryByRole("link", { name: /Fallback capacity is not confirmed/i })).not.toBeInTheDocument();
  });
});

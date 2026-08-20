import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type {
  ArtifactWorkspaceSummary,
  IssueProposalSummary,
} from "@/lib/server/oslo-api";

import { ArtifactWorkspace } from "./artifact-workspace";

function artifactFor(
  artifactType: string,
  sections: ArtifactWorkspaceSummary["content"]["sections"],
  overrides: Partial<ArtifactWorkspaceSummary> = {},
): ArtifactWorkspaceSummary {
  return {
    artifact_type: artifactType,
    title: artifactType
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase()),
    content: { sections },
    version: 1,
    provenance: "from_oslo",
    reliability: "Moderate",
    basis: "derived",
    evidence_refs: [],
    issues: [],
    updated_at: "2026-08-14T10:00:00Z",
    ...overrides,
  };
}

const scheduleArtifact = artifactFor(
  "schedule",
  [
    {
      heading: "Milestones",
      body: "The delivery baseline is not approved.",
      bullets: [],
      columns: ["Milestone", "Owner", "Start", "End", "Status"],
      rows: [
        ["Launch", "Dana", "2026-09-01", "2026-09-12", "At risk"],
        ["Steering review", "", "2026-08-15", "", "Pending"],
      ],
      provenance: "from_oslo",
      row_evidence_refs: [[], []],
      row_states: ["confirmed", "inferred"],
      row_provenance: ["confirmed_by_user", "from_oslo"],
    },
  ],
  {
    title: "Schedule",
    issues: [
      {
        id: "ISS-SCHEDULE",
        artifact_type: "schedule",
        dimension: "Feasibility",
        severity: "Critical",
        title: "Delivery baseline is unresolved",
        why: "No approved milestone path exists.",
        recommendation: "Approve the baseline.",
        evidence_refs: [],
        clarification: "Which schedule is approved?",
        status: "open",
      },
    ],
  },
);

const proposal: IssueProposalSummary = {
  id: "proposal-schedule-1",
  issue_id: "ISS-SCHEDULE",
  kind: "build",
  resolver_key: "schedule:approved-baseline",
  title: "Add the approved delivery baseline",
  rationale: "The current schedule has no approved baseline.",
  artifact_type: "schedule",
  load_bearing: true,
  accepted: false,
  rejected: false,
  surface: null,
};

function renderArtifact({
  artifact = scheduleArtifact,
  artifactType = artifact.artifact_type,
  onAnalysisStarted = vi.fn(),
  onProposalDecision,
  proposalError,
  proposals = [],
}: {
  artifact?: ArtifactWorkspaceSummary;
  artifactType?: string;
  onAnalysisStarted?: (runId: string) => void;
  onProposalDecision?: (proposal: IssueProposalSummary, accepted: boolean) => void;
  proposalError?: string | null;
  proposals?: IssueProposalSummary[];
} = {}) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify(artifact), {
        status: 200,
        headers: { "content-type": "application/json" },
      }),
    ),
  );
  return render(
    <ArtifactWorkspace
      analysisRunning={false}
      artifactType={artifactType}
      onAnalysisStarted={onAnalysisStarted}
      onAskOslo={vi.fn()}
      onOpenIssue={vi.fn()}
      onProposalDecision={onProposalDecision}
      proposalError={proposalError}
      proposals={proposals}
      projectId="project-001"
    />,
  );
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("ArtifactWorkspace R2 plan artifacts", () => {
  it("renders the Schedule as dated task rows, a Gantt track, and one issue callout", async () => {
    renderArtifact();
    expect(await screen.findByRole("heading", { name: "Schedule" })).toBeInTheDocument();
    expect(screen.getByLabelText("Start date for Launch")).toHaveValue("2026-09-01");
    expect(screen.getByLabelText("End date for Launch")).toHaveValue("2026-09-12");
    expect(screen.getAllByText("Delivery baseline is unresolved")).toHaveLength(1);
    expect(document.querySelectorAll(".r2-schedule-track")).toHaveLength(2);
  });

  it("does not treat dependency evidence as an end-date field", async () => {
    const dependencies = artifactFor("schedule", [
      {
        heading: "Critical dependencies",
        body: "",
        bullets: [],
        columns: ["Dependency evidence", "RAG"],
        rows: [["Carrier-rate API access is required by 15 Jan 2027", "Amber"]],
        row_states: ["confirmed"],
        row_provenance: ["from_oslo"],
      },
    ]);

    renderArtifact({ artifact: dependencies, artifactType: "schedule" });
    await screen.findByRole("heading", { name: "Schedule" });

    expect(
      screen.getByLabelText("Start date for Carrier-rate API access is required by 15 Jan 2027"),
    ).toHaveValue("");
    expect(
      screen.getByLabelText("End date for Carrier-rate API access is required by 15 Jan 2027"),
    ).toHaveValue("");
    expect(screen.getByText("Amber")).toBeInTheDocument();
    expect(document.querySelector(".r2-schedule-row")).toHaveClass("is-yours");
  });

  it("keeps schedule edits local until Save changes and preserves real row data", async () => {
    const onAnalysisStarted = vi.fn();
    const saved = { ...scheduleArtifact, version: 2, analysis_run: { run_id: "run-edit-001" } };
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(Response.json(scheduleArtifact))
        .mockResolvedValueOnce(new Response(JSON.stringify(saved), { status: 202 })),
    );
    render(
      <ArtifactWorkspace
        analysisRunning={false}
        artifactType="schedule"
        onAnalysisStarted={onAnalysisStarted}
        onAskOslo={vi.fn()}
        onOpenIssue={vi.fn()}
        projectId="project-001"
      />,
    );
    const end = await screen.findByLabelText("End date for Steering review");
    fireEvent.change(end, { target: { value: "2026-08-22" } });
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2));
    const request = vi.mocked(fetch).mock.calls[1][1];
    const payload = JSON.parse(String(request?.body));
    expect(payload.content.sections[0].rows[1][3]).toBe("2026-08-22");
    expect(onAnalysisStarted).toHaveBeenCalledWith("run-edit-001");
  });

  it("cancels local artifact edits without saving or starting reanalysis", async () => {
    const fetcher = vi.fn().mockResolvedValueOnce(Response.json(scheduleArtifact));
    vi.stubGlobal("fetch", fetcher);
    render(
      <ArtifactWorkspace
        analysisRunning={false}
        artifactType="schedule"
        onAnalysisStarted={vi.fn()}
        onAskOslo={vi.fn()}
        onOpenIssue={vi.fn()}
        projectId="project-001"
      />,
    );
    const end = await screen.findByLabelText("End date for Steering review");
    expect(end).toHaveValue("");
    fireEvent.change(end, { target: { value: "2026-08-22" } });
    expect(end).toHaveValue("2026-08-22");

    fireEvent.click(screen.getByRole("button", { name: "Cancel changes" }));

    expect(screen.getByLabelText("End date for Steering review")).toHaveValue("");
    expect(screen.queryByText("Changes not applied")).not.toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledTimes(1);
  });

  it("shows a recoverable error when the artifact request fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(Response.json({ message: "Unavailable" }, { status: 503 }))
        .mockResolvedValueOnce(Response.json(scheduleArtifact)),
    );
    render(
      <ArtifactWorkspace
        analysisRunning={false}
        artifactType="schedule"
        onAnalysisStarted={vi.fn()}
        onAskOslo={vi.fn()}
        onOpenIssue={vi.fn()}
        projectId="project-001"
      />,
    );
    expect(await screen.findByRole("alert")).toHaveTextContent("Artifact could not be loaded");
    fireEvent.click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findByRole("heading", { name: "Schedule" })).toBeInTheDocument();
  });

  it("uses Add to plan and Dismiss for governed proposals", async () => {
    const onProposalDecision = vi.fn();
    renderArtifact({ onProposalDecision, proposals: [proposal] });
    const region = await screen.findByRole("region", { name: "OSLO proposes in this artifact" });
    expect(region).toHaveTextContent("nothing enters your plan until you accept");
    const addButton = within(region).getByRole("button", {
      name: "Add Add the approved delivery baseline to plan in Schedule",
    });
    const dismissButton = within(region).getByRole("button", {
      name: "Dismiss Add the approved delivery baseline in Schedule",
    });
    expect(addButton).toHaveClass("artifact-proposal-accept");
    expect(dismissButton).toHaveClass("artifact-proposal-reject");
    fireEvent.click(addButton);
    expect(onProposalDecision).toHaveBeenCalledWith(proposal, true);
    fireEvent.click(dismissButton);
    expect(onProposalDecision).toHaveBeenCalledWith(proposal, false);
  });

  it("uses the prototype inline Edit, Save, and Cancel controls for statements", async () => {
    const requirements = artifactFor("requirements", [
      {
        heading: "Requirements",
        body: "",
        bullets: ["Venue supports 450 attendees."],
        columns: [],
        rows: [],
        provenance: "confirmed_by_user",
      },
    ]);
    renderArtifact({ artifact: requirements, artifactType: "requirements" });
    await screen.findByRole("heading", { name: "Requirements" });

    const original = "Venue supports 450 attendees.";
    fireEvent.click(screen.getByRole("button", { name: `Edit ${original}` }));
    const editor = screen.getByRole("textbox", { name: `Edit ${original}` });
    expect(editor).toHaveValue(original);
    fireEvent.change(editor, { target: { value: "Venue supports 500 attendees." } });
    fireEvent.click(screen.getByRole("button", { name: "Cancel statement edit" }));
    expect(screen.getByText(original)).toBeInTheDocument();
    expect(screen.queryByText("Changes not applied")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: `Edit ${original}` }));
    fireEvent.change(
      screen.getByRole("textbox", { name: `Edit ${original}` }),
      { target: { value: "Venue supports 500 attendees." } },
    );
    fireEvent.click(screen.getByRole("button", { name: "Save statement edit" }));
    expect(screen.getByText("Venue supports 500 attendees.")).toBeInTheDocument();
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });

  it("renders Intent with the five prototype groups and confirms inferred rows", async () => {
    const intent = artifactFor("intent", [
      { heading: "Purpose", body: "Grow the developer community.", bullets: [], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Outcomes", body: "", bullets: ["Run a sold-out conference."], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Goals", body: "", bullets: ["Fill every seat."], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Success criteria", body: "", bullets: [], columns: ["Criterion"], rows: [["450 of 450 seats sold."]], row_states: ["inferred"], row_provenance: ["from_oslo"] },
      { heading: "KPIs & metrics", body: "", bullets: ["Tickets sold vs capacity."], columns: [], rows: [], provenance: "confirmed_by_user" },
    ]);
    renderArtifact({ artifact: intent, artifactType: "intent" });
    expect(await screen.findByRole("heading", { name: "Intent" })).toBeInTheDocument();
    for (const heading of ["Purpose", "Outcomes", "Goals", "Success criteria", "KPIs & metrics"]) {
      expect(screen.getByText(heading)).toBeInTheDocument();
    }
    const row = screen.getByText("450 of 450 seats sold.").closest(".r2-statement-row");
    expect(row).not.toBeNull();
    fireEvent.click(within(row as HTMLElement).getByRole("button", { name: /Confirm/ }));
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });

  it("styles source-grounded narrative evidence as the user's evidence", async () => {
    const intent = artifactFor("intent", [
      {
        heading: "Purpose",
        body: "Launch the customer portal.",
        bullets: [],
        columns: [],
        rows: [],
        provenance: "from_oslo",
        evidence_refs: ["document:charter:page:1:fragment:0"],
      },
    ]);

    renderArtifact({ artifact: intent, artifactType: "intent" });
    await screen.findByRole("heading", { name: "Intent" });

    expect(
      screen.getByText("Launch the customer portal.").closest(".r2-statement-row"),
    ).toHaveClass("is-yours");
  });

  it("renders structured understanding rows once instead of repeating body and bullet encodings", async () => {
    const intent = artifactFor("intent", [
      {
        heading: "Objectives and success measures",
        body: "ID Objective OBJ-01 Shift eligible orders online OBJ-02 Improve adoption",
        bullets: [
          "OBJ-01 | Shift eligible orders online",
          "OBJ-02 | Improve adoption",
        ],
        columns: ["ID", "Objective"],
        rows: [
          ["OBJ-01", "Shift eligible orders online"],
          ["OBJ-02", "Improve adoption"],
        ],
        row_states: ["confirmed", "confirmed"],
        row_provenance: ["confirmed_by_user", "confirmed_by_user"],
      },
    ]);

    renderArtifact({ artifact: intent, artifactType: "intent" });
    await screen.findByRole("heading", { name: "Intent" });

    expect(screen.getAllByText("Shift eligible orders online")).toHaveLength(1);
    expect(screen.getAllByText("Improve adoption")).toHaveLength(1);
    expect(screen.queryByText(/ID Objective OBJ-01/)).not.toBeInTheDocument();
    expect(screen.queryByText("OBJ-01 | Shift eligible orders online")).not.toBeInTheDocument();
    expect(screen.getByText("KPIs & metrics").closest("header")).toHaveTextContent("2");
  });

  it("shows one statement when identical content is retained across artifact sections", async () => {
    const constraints = artifactFor("constraints", [
      {
        heading: "Constraints",
        body: "The launch is capped at GBP 1,800,000.",
        bullets: [],
        columns: [],
        rows: [],
        provenance: "from_oslo",
      },
      {
        heading: "Confirmed constraints",
        body: "The launch is capped at GBP 1,800,000.",
        bullets: [],
        columns: [],
        rows: [],
        provenance: "confirmed_by_user",
      },
    ]);

    renderArtifact({ artifact: constraints, artifactType: "constraints" });
    await screen.findByRole("heading", { name: "Constraints" });

    const statements = screen.getAllByText("The launch is capped at GBP 1,800,000.");
    expect(statements).toHaveLength(1);
    expect(statements[0].closest(".r2-statement-row")).toHaveClass("is-yours");
  });

  it("renders a rewritten, read-only Intent narrative", async () => {
    const intent = artifactFor("intent", [
      { heading: "Purpose", body: "Deliver the agreed outcome.", bullets: [], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Goals", body: "", bullets: ["Measure the result."], columns: [], rows: [], provenance: "from_oslo" },
    ]);
    renderArtifact({ artifact: intent, artifactType: "intent" });
    await screen.findByRole("heading", { name: "Intent" });
    fireEvent.click(screen.getByRole("button", { name: "Narrative" }));
    const narrative = screen.getByLabelText("Intent narrative");
    expect(narrative).toHaveTextContent("Here is what this plan is setting out to achieve");
    expect(narrative).toHaveTextContent("Nothing enters your plan until you accept it");
    expect(narrative.querySelector("[contenteditable='true']")).toBeNull();
  });

  it("renders Scope as In scope, Out of scope, and Edge — undecided", async () => {
    const scope = artifactFor("scope", [
      { heading: "In scope", body: "Single-day conference.", bullets: [], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Out of scope", body: "Virtual attendance.", bullets: [], columns: [], rows: [], provenance: "confirmed_by_user" },
      { heading: "Edge — undecided", body: "Evening networking.", bullets: [], columns: [], rows: [], provenance: "from_oslo" },
    ]);
    renderArtifact({ artifact: scope, artifactType: "scope" });
    await screen.findByRole("heading", { name: "Scope" });
    expect(screen.getByText("✓ In scope")).toBeInTheDocument();
    expect(screen.getByText("× Out of scope")).toBeInTheDocument();
    expect(screen.getByText("Edge — undecided")).toBeInTheDocument();
  });

  it.each([
    ["requirements", "Add requirement", "Venue supports 450 attendees."],
    ["constraints", "Add constraint", "Total budget: $300,000 — hard cap."],
  ])("renders %s as readable statement rows with front-of-row actions", async (type, addLabel, text) => {
    const artifact = artifactFor(type, [
      { heading: type, body: "", bullets: [], columns: ["ID", "Statement"], rows: [["REQ-1", text]], row_states: ["inferred"], row_provenance: ["from_oslo"] },
    ]);
    renderArtifact({ artifact, artifactType: type });
    await screen.findByRole("heading", { name: type === "requirements" ? "Requirements" : "Constraints" });
    const row = screen.getByText(text).closest(".r2-statement-row");
    expect(within(row as HTMLElement).getByRole("button", { name: /Confirm/ })).toBeInTheDocument();
    expect(within(row as HTMLElement).getByRole("button", { name: /Edit/ })).toBeInTheDocument();
    expect(within(row as HTMLElement).getByRole("button", { name: /Delete/ })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: addLabel }));
    expect(screen.getByText("New statement")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Save changes" })).toBeEnabled();
  });

  it("shows an affected section issue once instead of under every requirement row", async () => {
    const requirements = artifactFor(
      "requirements",
      [
        {
          heading: "Functional requirements",
          body: "",
          bullets: [],
          columns: ["ID", "Requirement"],
          rows: [["REQ-1", "Create an order"], ["REQ-2", "Track an order"]],
          row_states: ["confirmed", "confirmed"],
          row_provenance: ["confirmed_by_user", "confirmed_by_user"],
        },
      ],
      {
        issues: [
          {
            id: "ISS-REQ",
            artifact_type: "requirements",
            dimension: "Clarity",
            severity: "Critical",
            title: "Payment security is unresolved",
            why: "No applicable control is named.",
            recommendation: "Name the approved control.",
            evidence_refs: [],
            clarification: "Which control applies?",
            status: "open",
          },
        ],
      },
    );

    renderArtifact({ artifact: requirements, artifactType: "requirements" });
    await screen.findByRole("heading", { name: "Requirements" });

    expect(screen.getAllByText("Payment security is unresolved")).toHaveLength(1);
    expect(document.querySelectorAll(".r2-row-warning")).toHaveLength(1);
  });

  it("renders Work breakdown hierarchy controls and adds work locally", async () => {
    const wbs = artifactFor("work_breakdown", [
      { heading: "Revenue & sponsorship", body: "", bullets: [], columns: ["WBS", "Item"], rows: [["1.0", "Sponsorship"], ["1.1", "Sponsor outreach"], ["1.1.1", "Send sponsor brief"]], row_states: ["confirmed", "confirmed", "inferred"], row_provenance: ["confirmed_by_user", "confirmed_by_user", "from_oslo"] },
    ]);
    renderArtifact({ artifact: wbs, artifactType: "work_breakdown" });
    await screen.findByRole("heading", { name: "Work Breakdown" });
    expect(screen.getByText("Revenue & sponsorship")).toBeInTheDocument();
    expect(screen.getByText("Sponsorship")).toBeInTheDocument();
    expect(screen.getByText("Sponsor outreach")).toBeInTheDocument();
    expect(screen.queryByText("1.1")).not.toBeInTheDocument();
    expect(screen.getByText("Deliverable")).toBeInTheDocument();
    expect(screen.getByText("Package")).toBeInTheDocument();
    expect(screen.queryByText("Task")).not.toBeInTheDocument();
    expect(
      screen.getByText(
        /Decomposes the outcome into deliverables, work packages, and tasks/,
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Click any name to rename; add or remove at every level/),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Add task to Sponsorship" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Backlog · agile" }));
    expect(screen.getByText(/Your plan as a backlog — epics and stories/)).toBeInTheDocument();
    expect(screen.getByText(/Same work items as the outline/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Add work package" }));
    expect(screen.getByText("New work package")).toBeInTheDocument();
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });

  it("upgrades a legacy flattened Work breakdown into the prototype hierarchy", async () => {
    const legacy = artifactFor("work_breakdown", [
      {
        heading: "Work breakdown",
        body: "Initial evidence-qualified work breakdown.",
        bullets: [
          "Plan a product or software launch: define users, scope, requirements, release plan, resources and adoption measures.",
          "Schedule artifact changes confirmed by the user: Section: Schedule Initial evidence-qualified schedule.",
          "Issue: Milestones are not fully reconciled Question: What evidence confirms this issue?",
        ],
        columns: [],
        rows: [],
        provenance: "from_oslo",
      },
    ]);

    renderArtifact({ artifact: legacy, artifactType: "work_breakdown" });

    expect(await screen.findByText("Product or software launch")).toBeInTheDocument();
    expect(screen.getByText("Plan a product or software launch")).toBeInTheDocument();
    expect(screen.getByText("Define users")).toBeInTheDocument();
    expect(screen.getByText("Define adoption measures")).toBeInTheDocument();
    expect(screen.queryByText(/Schedule artifact changes confirmed/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Milestones are not fully reconciled Question/)).not.toBeInTheDocument();
  });

  it("renders Resources summary cards and owner assignment controls", async () => {
    const resources = artifactFor("resources", [
      { heading: "People", body: "", bullets: [], columns: ["Task", "Owner", "Status"], rows: [["Sponsor outreach", "Dana", "confirmed"], ["Catering", "", "unowned"]], row_states: ["confirmed", "inferred"], row_provenance: ["confirmed_by_user", "from_oslo"] },
    ]);
    renderArtifact({ artifact: resources, artifactType: "resources" });
    await screen.findByRole("heading", { name: "Resources" });
    expect(screen.getByLabelText("Resource summary")).toBeInTheDocument();
    const cateringOwner = screen.getByLabelText("Owner for Catering");
    fireEvent.change(cateringOwner, { target: { value: "Dana" } });
    expect(cateringOwner).toHaveValue("Dana");
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });

  it("does not present risks, assumptions, or decisions as owner assignments", async () => {
    const resources = artifactFor("resources", [
      {
        heading: "Risks and issues",
        body: "",
        bullets: [],
        columns: ["ID", "Evidence-derived detail"],
        rows: [["R-01", "Pen-test supplier is not contracted"]],
        row_states: ["confirmed"],
        row_provenance: ["from_oslo"],
      },
      {
        heading: "Explicit assumptions",
        body: "",
        bullets: [],
        columns: ["ID", "Evidence-derived detail"],
        rows: [["A-01", "Production SSO is ready before testing"]],
        row_states: ["confirmed"],
        row_provenance: ["from_oslo"],
      },
      {
        heading: "Dependency and decision log",
        body: "",
        bullets: [],
        columns: ["ID", "Evidence-derived detail"],
        rows: [["DEC-01", "Steering Committee approval is pending"]],
        row_states: ["confirmed"],
        row_provenance: ["from_oslo"],
      },
    ]);

    renderArtifact({ artifact: resources, artifactType: "resources" });
    await screen.findByRole("heading", { name: "Resources" });

    expect(screen.getByRole("heading", { name: "Risks and issues" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Explicit assumptions" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Dependency and decision log" })).toBeInTheDocument();
    expect(screen.queryByLabelText(/Owner for Pen-test supplier/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/Owner for Production SSO/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/Owner for Steering Committee/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Add teammate" }));
    expect(screen.getByLabelText("Owner for New teammate")).toBeInTheDocument();
  });

  it("keeps Resources summary cards concise for large structured plans", async () => {
    const longFlattenedPlan = "Role Named resource Allocation Period Backup gap ".repeat(12);
    const resources = artifactFor("resources", [
      {
        heading: "Resource plan",
        body: longFlattenedPlan,
        bullets: [],
        columns: ["Role", "Named resource", "Allocation", "Period", "Backup / gap"],
        rows: [
          ["Programme Manager", "Priya Nair", "1.0 FTE", "Aug 2026-Jun 2027", "Owen Price"],
          ["Security Lead", "Rachel Cole", "0.3 FTE", "Aug 2026-May 2027", "Pen-test vendor not contracted"],
          ["Implementation partner", "TradeHub Ltd", "6.0 FTE", "Sep 2026-May 2027", "Contracted"],
        ],
        row_states: ["confirmed", "confirmed", "confirmed"],
        row_provenance: ["confirmed_by_user", "confirmed_by_user", "confirmed_by_user"],
      },
      {
        heading: "Risks and issues",
        body: "",
        bullets: [],
        columns: ["Type", "Detail"],
        rows: [["Risk", "Pen-test supplier is not contracted"]],
        row_states: ["confirmed"],
        row_provenance: ["confirmed_by_user"],
      },
    ]);

    renderArtifact({ artifact: resources, artifactType: "resources" });
    await screen.findByRole("heading", { name: "Resources" });

    const summary = screen.getByLabelText("Resource summary");
    expect(summary).toHaveTextContent("3 resource entries in Resource plan");
    expect(summary).toHaveTextContent("TradeHub Ltd \u00b7 Implementation partner");
    expect(summary).not.toHaveTextContent("Rachel Cole \u00b7 Security Lead");
    expect(summary).not.toHaveTextContent("Risk \u00b7 Pen-test supplier is not contracted");
    expect(summary).not.toHaveTextContent(longFlattenedPlan);
  });

  it("adds a proposed outcome checkpoint to the Schedule locally", async () => {
    const checkpointProposal = {
      ...proposal,
      id: "proposal-checkpoint",
      title: "Add checkpoint: read evidence that the stated outcome is materializing",
    };
    renderArtifact({ proposals: [checkpointProposal] });
    await screen.findByRole("heading", { name: "Schedule" });
    fireEvent.click(screen.getByRole("button", { name: "Add outcome checkpoint" }));
    expect(screen.getByText("Outcome checkpoint — read evidence that the stated outcome is materializing")).toBeInTheDocument();
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });

  it("shows proposal failures beside the proposal list", async () => {
    renderArtifact({
      onProposalDecision: vi.fn(),
      proposalError: "Proposal decision could not be saved",
      proposals: [proposal],
    });
    expect(await screen.findByRole("alert")).toHaveTextContent("Proposal decision could not be saved");
  });
});

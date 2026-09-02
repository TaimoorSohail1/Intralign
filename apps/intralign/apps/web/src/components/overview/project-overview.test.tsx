import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { ProjectOverview } from "./project-overview";

const push = vi.fn();
const replace = vi.fn();
const refresh = vi.fn();

vi.mock("next/navigation", () => ({
  usePathname: () => "/projects/project-001/issues",
  useRouter: () => ({ push, refresh, replace }),
}));

const snapshot: OverviewSnapshot = {
  snapshot_id: "snap-001",
  analysis_run_id: "run-001",
  project_id: "project-001",
  orientation_seen: true,
  state: "current",
  summary: "A project with an unresolved migration dependency.",
  artifacts: [
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "The accountable migration owner is not confirmed.",
      reliability: "Moderate",
      evidence_refs: ["document:plan:page:1:fragment:0"],
      basis: "supported",
    },
  ],
  assessment: {
    confidence_index: 52,
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "Moderate",
    alignment: "Moderate",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: {
      coverage: "High",
      evidence: "Moderate",
      assessability: "Moderate",
    },
    confidence_direction: "strengthened",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation:
      "The moderate confidence read is limited by feasibility.",
    resolved_issue_count: 0,
    confirmed_dependency_count: 0,
    integrity: {
      level: "Developing",
      limiting_pillar: "Grounding",
      decomposition: [
        { key: "Viability", band: "Solid", basis: 0.75, why: ["3 of 4 clear"] },
        { key: "Grounding", band: "Developing", basis: 0.5, why: ["2 of 4 grounded"] },
        { key: "Adaptability", band: "Solid", basis: 0.75, why: ["3 of 4 registered"] },
      ],
      posture: "moment-in-time",
      tracking: "pending-execution",
    },
    issues: [
      {
        id: "ISS-001",
        artifact_type: "resources",
        dimension: "Feasibility",
        severity: "Critical",
        title: "Migration ownership is unresolved",
        why: "No accountable owner is identified.",
        recommendation: "Confirm an accountable owner.",
        evidence_refs: ["document:plan:page:1:fragment:0"],
        evidence: [
          {
            source_name: "Migration plan.pdf",
            location: "Page 1",
            excerpt: "The accountable migration owner has not been confirmed.",
          },
        ],
        clarification: "Who owns migration?",
        status: "open",
      },
    ],
  },
  published_at: "2026-07-23T12:00:00Z",
};

const sliceFourSnapshot: OverviewSnapshot = {
  ...snapshot,
  assessment: {
    ...snapshot.assessment,
    issues: [
      {
        ...snapshot.assessment.issues[0],
        id: "ISS-REQ-CLARITY",
        artifact_type: "requirements",
        dimension: "Clarity",
        severity: "Moderate",
        title: "Success metric is not measurable",
        clarification: "Which approved target will measure success?",
      },
      {
        ...snapshot.assessment.issues[0],
        id: "ISS-RESOURCE-CRITICAL",
        title: "Migration ownership is unresolved",
      },
      {
        ...snapshot.assessment.issues[0],
        id: "ISS-RESOURCE-MODERATE",
        severity: "Moderate",
        status: "addressed",
        title: "Fallback capacity is not confirmed",
        clarification: "Which fallback team can absorb the work?",
      },
    ],
  },
};

beforeEach(() => {
  localStorage.setItem("oslo_orientation_seen", "true");
  sessionStorage.clear();
  push.mockReset();
  refresh.mockReset();
  replace.mockReset();
  Object.defineProperty(navigator, "clipboard", {
    configurable: true,
    value: { writeText: vi.fn().mockResolvedValue(undefined) },
  });
});

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("ProjectOverview", () => {
  it("renders the Slice 10 primary affordance from the derived finding model", () => {
    const classifiedSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        issues: [
          {
            ...snapshot.assessment.issues[0],
            finding_basis: "structural",
            structural_target: "achievability",
            primary_act: "build",
            also_offered: ["verify"],
            classification_state: "classified",
            sensitivity: 0.42,
            sensitivity_state: "shadow",
            sensitivity_trace: {
              paths: [["dependency", "outcome"]],
              span_true: 0.8,
              span_false: 0.4,
              span: 0.4,
              leverage: 0.7,
              uncertainty_factor: 1.25,
              runway_factor: 1.2,
              edge_key: null,
              outcome_reachability: ["outcome"],
            },
          },
        ],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={classifiedSnapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );

    expect(screen.getByRole("button", { name: "Apply this fix →" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Other options/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Write my own →" })).toBeInTheDocument();
    expect(screen.getByText("Verify with evidence")).toBeInTheDocument();
    expect(screen.getByText("Why this is load-bearing")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Verify with evidence"));
    expect(screen.getByRole("region", { name: "Ask for evidence" })).toBeInTheDocument();
  });

  it("renders the prototype trade-off actions for decision findings", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          assessment: {
            ...snapshot.assessment,
            issues: [{
              ...snapshot.assessment.issues[0],
              primary_act: "decide",
              also_offered: ["verify"],
              recommendation: "Bound the sponsor trade-off.",
            }],
          },
        }}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));

    expect(screen.getByRole("button", { name: "Draw the line →" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Accept on the record →" })).toBeInTheDocument();
  });

  it("does not claim the integrity band moved when a grounded update keeps the same band", () => {
    const unchangedBandSnapshot: OverviewSnapshot = {
      ...snapshot,
      read_moved_notifications: [
        {
          id: "notification-unchanged",
          analysis_run_id: snapshot.analysis_run_id,
          pillar_deltas: [],
          settled_causes: [],
          previous_band: "Developing",
          current_band: "Developing",
          delivery_kind: "durable",
          seen_at: null,
          expires_at: null,
          created_at: snapshot.published_at,
        },
      ],
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={unchangedBandSnapshot}
        initialView="overview"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("Your read was updated.")).toBeInTheDocument();
    expect(screen.getByText(/Outcome Integrity remains Developing/)).toBeInTheDocument();
    expect(screen.queryByText("Your read moved.")).not.toBeInTheDocument();
  });

  it("keeps the last good read visible while stale and offers an immediate reanalysis", async () => {
    const staleSnapshot: OverviewSnapshot = {
      ...snapshot,
      freshness: {
        state: "stale",
        pending_count: 2,
        based_on_run_id: "run-001",
        active_run_id: null,
        last_act_at: "2026-08-12T12:00:00Z",
        last_landed_at: "2026-08-12T11:59:00Z",
      },
    };
    const fetchMock = vi.fn().mockImplementation(async () =>
      Response.json({ run_id: "run-002", status: "queued" }, { status: 202 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={staleSnapshot}
        initialView="overview"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("Your read is safely out of date.")).toBeInTheDocument();
    expect(screen.getByText(/last completed read stays visible/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Reanalyze now" }));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/projects/project-001/reanalysis",
        expect.objectContaining({ method: "POST" }),
      ),
    );
    expect(await screen.findByText("Reanalysis queued")).toBeInTheDocument();
  });

  it("withdraws the latest pending change without hiding the last good read", async () => {
    const staleSnapshot: OverviewSnapshot = {
      ...snapshot,
      freshness: {
        state: "stale",
        pending_count: 1,
        based_on_run_id: "run-001",
        active_run_id: null,
        last_act_at: "2026-08-12T12:00:00Z",
        last_landed_at: "2026-08-12T11:59:00Z",
        latest_pending_event_id: "event-001",
      },
    };
    const fetchMock = vi.fn().mockImplementation(async () =>
      Response.json({
        event_id: "event-001",
        state: "withdrawn",
        pending_count: 0,
        grounding_act_count: 1,
        ever_unlocked: true,
        freeze_on: false,
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={staleSnapshot}
        initialView="overview"
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: "Undo last change" }));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/projects/project-001/acts/event-001",
        { method: "DELETE" },
      ),
    );
    expect(await screen.findByText("Pending change undone")).toBeInTheDocument();
    expect(screen.queryByText("Your read is safely out of date.")).not.toBeInTheDocument();
  });

  it("renders the prototype issue layer with exposure ranking and optional filters", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("heading", { name: "Issues" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "The issue layer" })).toBeInTheDocument();
    expect(screen.getByText(/one layer, exposure-ranked/i)).toBeInTheDocument();
    expect(screen.getByText("3 open")).toBeInTheDocument();
    expect(screen.getByText(/Grounding 0 · gating/i)).toBeInTheDocument();

    fireEvent.click(screen.getByText("Refine issue view"));
    expect(screen.getByRole("button", { name: "By dimension" })).toHaveAttribute(
      "aria-pressed",
      "false",
    );
    expect(screen.getByRole("button", { name: "Exposure ranked" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );

    fireEvent.click(screen.getByRole("button", { name: "By severity" }));
    expect(screen.getByRole("heading", { name: "Critical · 1" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Moderate · 2" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Resources 2" }));
    expect(screen.getByText("1 finding hidden by the current filters.")).toBeInTheDocument();
    expect(screen.queryByText("Success metric is not measurable")).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", {
        name: /Migration ownership is unresolved, critical, resources/i,
      }),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Clear filters" }));
    expect(screen.getByText("Success metric is not measurable")).toBeInTheDocument();
  });

  it("keeps resolved findings out of the default active filter counts", () => {
    const withResolved: OverviewSnapshot = {
      ...sliceFourSnapshot,
      assessment: {
        ...sliceFourSnapshot.assessment,
        issues: [
          ...sliceFourSnapshot.assessment.issues,
          {
            ...sliceFourSnapshot.assessment.issues[1],
            id: "ISS-RESOLVED",
            status: "resolved",
            title: "Old resolved resource issue",
          },
        ],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={withResolved}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("3 open")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Resolved · 1" })).toBeInTheDocument();
    fireEvent.click(screen.getByText("Refine issue view"));
    expect(screen.getByRole("button", { name: "Resources 2" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Critical 1" })).toBeInTheDocument();
    expect(screen.queryByText(/hidden by the current filters/i)).not.toBeInTheDocument();
    expect(screen.getByText("Old resolved resource issue")).toBeInTheDocument();
  });

  it("opens clarification only after the user explicitly asks OSLO", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Success metric is not measurable/i }),
    );

    const panel = screen.getByRole("dialog", { name: "Issue details" });
    expect(panel).toHaveTextContent("Success metric is not measurable");
    expect(panel).toHaveTextContent("Why it matters");
    expect(panel).not.toHaveTextContent("Clarification request");

    fireEvent.click(within(panel).getByRole("button", { name: "Let OSLO ask you a question" }));
    expect(panel).toHaveTextContent("Clarification request");
  });

  it("hydrates Issues filters from the URL contract and keeps filter changes shareable", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialIssueFilters={{
          artifact: "resources",
          dimension: "feasibility",
          severity: null,
          status: "active",
        }}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByText("Refine issue view"));
    expect(screen.getByRole("button", { name: "Resources 2" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByRole("button", { name: "Feasibility 2" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );

    fireEvent.click(screen.getByRole("button", { name: "Clear filters" }));
    expect(replace).toHaveBeenCalledWith("/projects/project-001/issues", {
      scroll: false,
    });
  });

  it("applies deep-link filters to the prototype-style Issues queue", () => {
    render(
      <ProjectOverview
        compactIssuesLanding
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialIssueFilters={{
          artifact: "requirements",
          dimension: "clarity",
          severity: null,
          status: "active",
        }}
        logoutAction={vi.fn()}
      />,
    );

    const queue = screen.getByRole("region", { name: "Exposure-ranked issue queue" });
    expect(within(queue).getByText("Success metric is not measurable")).toBeInTheDocument();
    expect(within(queue).queryByText("Migration ownership is unresolved")).not.toBeInTheDocument();
  });

  it("renders the golden Overview hierarchy and routes prototype entry points", () => {
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.queryByText("OSLO · AI-first R2 prototype")).not.toBeInTheDocument();
    expect(screen.queryByText("Sample")).not.toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Workspace open" })).toBeInTheDocument();
    const workspaceSlot = container.querySelector(".r2-workspace-open-slot");
    expect(workspaceSlot).toHaveAttribute("data-state", "open");
    fireEvent.click(screen.getByRole("button", { name: "Dismiss workspace open message" }));
    expect(screen.queryByRole("region", { name: "Workspace open" })).not.toBeInTheDocument();
    expect(container.querySelector(".r2-workspace-open-slot")).not.toBeInTheDocument();
    expect(screen.getAllByText(/Outcome integrity/i)).not.toHaveLength(0);
    expect(screen.queryByRole("link", { name: "Timeline" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Answer the first" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Project summary" })).toHaveAttribute(
      "aria-expanded",
      "false",
    );
    expect(screen.queryByText("Analysis status")).not.toBeInTheDocument();
  });

  it("keeps the sidebar utilities inside the scroll-safe sidebar layout", () => {
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const sidebar = screen.getByRole("complementary", { name: "Project navigation" });
    const content = container.querySelector(".workspace-sidebar-content");
    const footer = container.querySelector(".workspace-sidebar-footer");
    expect(content).toBeInTheDocument();
    expect(footer).toBeInTheDocument();
    expect(sidebar).toContainElement(content as HTMLElement);
    expect(sidebar).toContainElement(footer as HTMLElement);
    expect(footer?.querySelector(":scope > button:first-of-type")).toHaveTextContent("Take a quick tour");
    expect(within(footer as HTMLElement).getByRole("button", { name: "Feedback" })).toBeVisible();
  });

  it("waits for a server ticket before showing feedback as filed", async () => {
    const fetchMock = vi.fn().mockImplementation((input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              ticket_id: "ENH-0042",
              title: "The report audience control did not update.",
              status: "Filed",
              created_at: "2026-08-16T09:30:00Z",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      return Promise.resolve(
        new Response("[]", { status: 200, headers: { "content-type": "application/json" } }),
      );
    });
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="reports"
        logoutAction={vi.fn()}
      />,
    );

    const footer = container.querySelector(".workspace-sidebar-footer");
    fireEvent.click(within(footer as HTMLElement).getByRole("button", { name: "Feedback" }));

    const dialog = screen.getByRole("dialog", { name: "Feedback" });
    fireEvent.click(within(dialog).getByRole("button", { name: /Something’s missing/ }));
    fireEvent.change(within(dialog).getByPlaceholderText(/What happened/), {
      target: { value: "The report audience control did not update." },
    });
    fireEvent.click(within(dialog).getByRole("button", { name: /Request enhancement/ }));

    expect(within(dialog).getByRole("button", { name: "Filing feedback…" })).toBeDisabled();
    expect(within(dialog).queryByText(/your feedback is with the team/i)).not.toBeInTheDocument();

    expect(await within(dialog).findByText(/your feedback is with the team/i)).toBeInTheDocument();
    expect(within(dialog).getByText("ENH-0042")).toBeInTheDocument();
    expect(within(dialog).getByText(/project content were not changed/i)).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/feedback/tickets",
      expect.objectContaining({ method: "POST" }),
    );
    const postCall = fetchMock.mock.calls.find((call) => call[1]?.method === "POST");
    const request = JSON.parse(String(postCall?.[1]?.body));
    expect(request).toMatchObject({
      category: "enhancement",
      body: "The report audience control did not update.",
      expected: null,
      impact: null,
      context: {
        where: "Reports",
        view: "reports",
        first_run_flag: false,
      },
    });
    expect(request.context).not.toHaveProperty("project_id");
  });

  it("shows a retry path when feedback delivery fails and never claims it was filed", async () => {
    let postCount = 0;
    const fetchMock = vi.fn().mockImplementation((_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method !== "POST") {
        return Promise.resolve(
          new Response("[]", { status: 200, headers: { "content-type": "application/json" } }),
        );
      }
      postCount += 1;
      if (postCount === 1) {
        return Promise.resolve(
          new Response(JSON.stringify({ message: "Feedback could not be filed." }), {
            status: 503,
            headers: { "content-type": "application/json" },
          }),
        );
      }
      return Promise.resolve(
        new Response(
          JSON.stringify({
            ticket_id: "DEF-0043",
            title: "The report did not open.",
            status: "Filed",
            created_at: "2026-08-16T09:31:00Z",
          }),
          { status: 201, headers: { "content-type": "application/json" } },
        ),
      );
    });
    vi.stubGlobal("fetch", fetchMock);
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="reports"
        logoutAction={vi.fn()}
      />,
    );
    const footer = container.querySelector(".workspace-sidebar-footer");
    fireEvent.click(within(footer as HTMLElement).getByRole("button", { name: "Feedback" }));
    const dialog = screen.getByRole("dialog", { name: "Feedback" });
    fireEvent.change(within(dialog).getByPlaceholderText(/What happened/), {
      target: { value: "The report did not open." },
    });
    fireEvent.click(within(dialog).getByRole("button", { name: /File defect/ }));

    expect(await within(dialog).findByRole("alert")).toHaveTextContent("Feedback could not be filed");
    expect(within(dialog).queryByText(/your feedback is with the team/i)).not.toBeInTheDocument();
    fireEvent.click(within(dialog).getByRole("button", { name: "Try again" }));

    expect((await within(dialog).findAllByText("DEF-0043")).length).toBeGreaterThan(0);
    expect(postCount).toBe(2);
  });

  it("keeps the resolved lifecycle tray visible when no issue is settled yet", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("region", { name: "Resolved" })).toBeInTheDocument();
    expect(screen.getByText("0 of 1 settled")).toBeInTheDocument();
  });

  it("renders the R2 Slice 1 integrity masthead and the complete exposure-ranked queue", () => {
    const exposureSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        issues: [
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-LOW",
            title: "Lower exposure issue",
            exposure_rank: 1,
            severity: "Warning",
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-HIGH",
            title: "Highest exposure issue",
            exposure_rank: 5,
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-MID",
            title: "Middle exposure issue",
            exposure_rank: 3,
            severity: "Moderate",
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-SECOND",
            title: "Second exposure issue",
            exposure_rank: 4,
            severity: "Moderate",
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-FOURTH",
            title: "Fourth exposure issue",
            exposure_rank: 2,
            severity: "Warning",
          },
        ],
      },
    };

    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={exposureSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(container.querySelector("main")).toHaveClass("is-r2-slice-one");
    expect(
      screen.getByRole("region", { name: "Outcome Integrity summary" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Views")).toBeInTheDocument();
    expect(screen.getByText("Documents")).toBeInTheDocument();
    expect(
      Array.from(container.querySelectorAll(".workspace-artifact-group > a"))
        .slice(0, 4)
        .map((link) => link.textContent?.trim()),
    ).toEqual(["Intent", "Scope", "Requirements", "Constraints"]);
    expect(
      screen.getByRole("link", { name: "Constraints" }),
    ).toHaveAttribute(
      "href",
      `/projects/${snapshot.project_id}/artifacts/constraints`,
    );

    fireEvent.click(screen.getByText("Why a maturity read, not a probability?"));
    expect(screen.getByText(snapshot.assessment.confidence_explanation)).toBeVisible();

    const queue = screen.getByRole("region", {
      name: "Exposure-ranked issue queue",
    });
    const issueButtons = within(queue).getAllByRole("button");
    expect(issueButtons).toHaveLength(5);
    expect(issueButtons.map((button) => button.textContent)).toEqual([
      expect.stringContaining("Highest exposure issue"),
      expect.stringContaining("Second exposure issue"),
      expect.stringContaining("Middle exposure issue"),
      expect.stringContaining("Fourth exposure issue"),
      expect.stringContaining("Lower exposure issue"),
    ]);
    expect(within(queue).getAllByText("Holds up")).toHaveLength(5);
  });

  it("renders the Slice 2 prototype proposal and lifecycle trays without mixing acted items into the ranked queue", () => {
    const lifecycleSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        issues: [
          snapshot.assessment.issues[0],
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-FIX",
            title: "Delivery owner needs a fix",
            status: "needs_fix",
            basis: "answered",
            attested_by: { id: "reviewer-1", display_name: "Amina", role: "reviewer" },
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-GROUND",
            title: "Contingency fix needs evidence",
            status: "needs_grounding",
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-ROUTED",
            title: "Vendor capacity is awaiting evidence",
            status: "routed",
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-RESOLVED",
            title: "Sponsor commitment",
            status: "resolved",
            basis: "verified-directly",
            attested_by: { id: "user-1", display_name: "Alex", role: "owner" },
          },
        ],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={lifecycleSnapshot}
        initialProposals={[
          {
            id: "proposal-1",
            issue_id: "ISS-001",
            kind: "optional",
            resolver_key: "optional:owner",
            title: "Name a delivery fallback",
            rationale: "The current plan has no documented fallback.",
            artifact_type: "resources",
            load_bearing: false,
            accepted: false,
            rejected: false,
            surface: null,
          },
        ]}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("region", { name: "OSLO proposes" })).toBeInTheDocument();
    expect(screen.getByText("Name a delivery fallback")).toBeInTheDocument();
    expect(screen.queryByText("Optional")).not.toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Awaiting evidence" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Acted on, not yet closed" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Resolved" })).toBeInTheDocument();
    expect(screen.getByText("1 of 5 settled")).toBeInTheDocument();
    expect(screen.getByText("Answered · Flagged by Amina")).toBeInTheDocument();

    const queue = screen.getByRole("region", { name: "Exposure-ranked issue queue" });
    expect(within(queue).getAllByRole("button")).toHaveLength(1);
    expect(within(queue).getByText("Migration ownership is unresolved")).toBeInTheDocument();
    expect(within(queue).queryByText("Delivery owner needs a fix")).not.toBeInTheDocument();
    expect(
      within(screen.getByRole("region", { name: "Awaiting evidence" })).getByRole(
        "button",
        { name: "Withdraw" },
      ),
    ).toBeInTheDocument();
  });

  it("keeps proposal and lifecycle tray geometry reserved while collapsed", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialProposals={[
          {
            id: "proposal-1",
            issue_id: "ISS-001",
            kind: "optional",
            resolver_key: "optional:owner",
            title: "Name a delivery fallback",
            rationale: "The current plan has no documented fallback.",
            artifact_type: "resources",
            load_bearing: false,
            accepted: false,
            rejected: false,
            surface: null,
          },
        ]}
        logoutAction={vi.fn()}
      />,
    );

    const proposalRegion = screen.getAllByRole("region", { name: "OSLO proposes" }).at(-1)!;
    const proposalBody = proposalRegion.querySelector(".r2-proposal-body");
    fireEvent.click(within(proposalRegion).getByRole("button", { name: /OSLO proposes/i }));
    expect(proposalBody).toBeInTheDocument();
    expect(proposalBody).toHaveAttribute("aria-hidden", "true");

    const resolvedRegion = screen.getByRole("region", { name: "Resolved" });
    const resolvedBody = resolvedRegion.querySelector(".r2-tray-body");
    fireEvent.click(within(resolvedRegion).getByRole("button", { name: /Resolved/i }));
    expect(resolvedBody).toBeInTheDocument();
    expect(resolvedBody).toHaveAttribute("aria-hidden", "true");
    fireEvent.click(within(resolvedRegion).getByRole("button", { name: /Resolved/i }));
    expect(resolvedBody).toHaveAttribute("aria-hidden", "false");
  });

  it("keeps the inline clarification behind the prototype recommendation disclosure", () => {
    render(
      <ProjectOverview displayName="Alex" initial={snapshot} logoutAction={vi.fn()} />,
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );

    expect(screen.queryByLabelText("Clarification answer")).not.toBeInTheDocument();
    fireEvent.click(
      screen.getByRole("button", { name: "Let OSLO ask you a question" }),
    );
    expect(screen.getByLabelText("Clarification answer")).toBeVisible();
  });

  it("keeps a persistent Start here when the ranked worklist is clear", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          assessment: {
            ...snapshot.assessment,
            issues: snapshot.assessment.issues.map((issue) => ({
              ...issue,
              status: "needs_grounding" as const,
            })),
          },
        }}
        logoutAction={vi.fn()}
      />,
    );

    const start = screen.getByRole("status", { name: "Start here" });
    expect(start).toHaveTextContent("Finish the acted-on items below");
    expect(screen.getByRole("region", { name: "Exposure-ranked issue queue" })).toBeEmptyDOMElement();
  });

  it("routes a collaborator through authenticated issue acts without a bearer link", async () => {
    const fetcher = vi.fn().mockImplementation(async (request: RequestInfo | URL) => {
      const url = String(request);
      if (url.endsWith("/collaboration")) {
        return Response.json({ comments: [] });
      }
      if (url.endsWith("/acts")) {
        return Response.json({
          issue_id: "ISS-001",
          act: "route",
          status: "routed",
          attestation: null,
          analysis_run: null,
          first_run: {
            first_run: true,
            onboarded: false,
            grounding_act_count: 1,
            unlock_threshold: 2,
            ever_unlocked: false,
            freeze_on: true,
          },
        }, { status: 202 });
      }
      return Response.json({});
    });
    vi.stubGlobal("fetch", fetcher);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          first_run: {
            first_run: true,
            onboarded: false,
            grounding_act_count: 0,
            unlock_threshold: 2,
            ever_unlocked: false,
            freeze_on: true,
          },
        }}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));
    fireEvent.click(screen.getByRole("button", { name: /Ask for evidence/i }));
    fireEvent.click(screen.getByRole("button", { name: /Project collaborator/i }));

    await waitFor(() => expect(fetcher.mock.calls.some(
      ([url, init]) => String(url).endsWith("/acts") && init?.method === "POST",
    )).toBe(true));
    const actCall = fetcher.mock.calls.find(
      ([url, init]) => String(url).endsWith("/acts") && init?.method === "POST",
    );
    expect(JSON.parse(String(actCall?.[1]?.body))).toMatchObject({
      act: "route",
      reviewer: {
        display_name: "Project collaborator",
        role: "collaborator",
      },
    });
    expect(fetcher.mock.calls.some(
      ([url, init]) => String(url).endsWith("/collaboration") && init?.method === "POST",
    )).toBe(false);
    expect(screen.getByText("One call down - you confirmed your outcome.")).toBeInTheDocument();
  });

  it("creates an external review with exactly one question and cited source", async () => {
    const fetcher = vi.fn().mockImplementation(async (request: RequestInfo | URL, init?: RequestInit) => {
      const url = String(request);
      if (url.endsWith("/collaboration") && init?.method === "POST") {
        const body = JSON.parse(String(init.body));
        if (body.action === "review_delivered") {
          return Response.json({ delivery_state: "awaiting" });
        }
        return Response.json({
          id: "review-grant-1",
          url: "http://localhost:3002/review/token",
          expires_at: "2026-08-21T00:00:00Z",
          delivery_state: "draft",
        }, { status: 201 });
      }
      if (url.endsWith("/collaboration")) return Response.json({ comments: [] });
      if (url.endsWith("/acts")) {
        return Response.json({
          issue_id: "ISS-001",
          act: "route",
          status: "routed",
          attestation: null,
          analysis_run: null,
        }, { status: 202 });
      }
      return Response.json({});
    });
    vi.stubGlobal("fetch", fetcher);

    render(<ProjectOverview displayName="Alex" initial={snapshot} logoutAction={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));
    fireEvent.click(screen.getByRole("button", { name: /Ask for evidence/i }));
    fireEvent.click(screen.getByRole("button", { name: /External evidence holder/i }));

    expect(screen.getByLabelText("External reviewer scope preview")).toHaveTextContent("Who owns migration?");
    expect(screen.getByLabelText("External reviewer scope preview")).toHaveTextContent(
      "The accountable migration owner has not been confirmed.",
    );
    fireEvent.change(screen.getByLabelText("Reviewer name"), {
      target: { value: "Amina Khan" },
    });
    fireEvent.change(screen.getByLabelText(/Email/), {
      target: { value: "amina@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Create secure review link/i }));

    await waitFor(() => expect(fetcher.mock.calls.some(
      ([url, init]) => String(url).endsWith("/collaboration") && init?.method === "POST",
    )).toBe(true));
    const reviewCall = fetcher.mock.calls.find(
      ([url, init]) => String(url).endsWith("/collaboration") && init?.method === "POST",
    );
    expect(JSON.parse(String(reviewCall?.[1]?.body))).toEqual({
      action: "review",
      issueId: "ISS-001",
      reviewerName: "Amina Khan",
      reviewerEmail: "amina@example.com",
      question: "Who owns migration?",
      sourceRef: "document:plan:page:1:fragment:0",
      sourceExcerpt: "The accountable migration owner has not been confirmed.",
    });
    expect(fetcher.mock.calls.some(
      ([url, init]) => String(url).endsWith("/acts") && init?.method === "POST",
    )).toBe(false);

    fireEvent.click(await screen.findByRole("button", { name: "Copy link" }));

    await waitFor(() => expect(fetcher.mock.calls.some(([url, init]) => {
      if (!String(url).endsWith("/collaboration") || init?.method !== "POST") return false;
      return JSON.parse(String(init.body)).action === "review_delivered";
    })).toBe(true));
    expect(fetcher.mock.calls.some(
      ([url, init]) => String(url).endsWith("/acts") && init?.method === "POST",
    )).toBe(true);
  });

  it("records Slice 2 owner acts and proposal decisions from the same prototype surfaces", async () => {
    const fetcher = vi.fn().mockImplementation(async (request: RequestInfo | URL) => {
      const url = String(request);
      if (url.includes("/proposals/proposal-1/decisions")) {
        return Response.json({
          proposal: {
            id: "proposal-1",
            issue_id: "ISS-001",
            kind: "optional",
            resolver_key: "optional:owner",
            title: "Name a delivery fallback",
            rationale: "The current plan has no documented fallback.",
            artifact_type: "resources",
            load_bearing: false,
            accepted: true,
            rejected: false,
            surface: "folded_read",
          },
          analysis_run: null,
        });
      }
      return Response.json({
        issue_id: "ISS-001",
        act: "confirm",
        status: "addressed",
        attestation: {
          id: "attestation-1",
          act: "confirm",
          basis: "verified-directly",
          evidence_ref: "document:plan:page:1:fragment:0",
          attributed_to: { id: "user-1", display_name: "Alex", role: "owner" },
          supersedes: null,
        },
        analysis_run: {
          run_id: "run-confirm-1",
          consolidated_event_ids: ["event-confirm-1"],
        },
      }, { status: 202 });
    });
    vi.stubGlobal("fetch", fetcher);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialProposals={[
          {
            id: "proposal-1",
            issue_id: "ISS-001",
            kind: "optional",
            resolver_key: "optional:owner",
            title: "Name a delivery fallback",
            rationale: "The current plan has no documented fallback.",
            artifact_type: "resources",
            load_bearing: false,
            accepted: false,
            rejected: false,
            surface: null,
          },
        ]}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));
    fireEvent.click(screen.getByRole("button", { name: "Confirm — it holds" }));
    fireEvent.click(screen.getByRole("button", { name: "I have it documented in writing" }));

    await waitFor(() => expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/issues/ISS-001/acts",
      expect.objectContaining({ method: "POST" }),
    ));
    const actCall = fetcher.mock.calls.find(([url]) => String(url).endsWith("/acts"));
    expect(JSON.parse(String(actCall?.[1]?.body))).toMatchObject({
      act: "confirm",
      basis: "documented",
      evidenceRef: "document:plan:page:1:fragment:0",
    });

    await waitFor(() => {
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument();
      expect(screen.getByRole("status", { name: "Issue action recorded" })).toBeInTheDocument();
    });
    const foldedProposal = screen.getByRole("region", { name: "OSLO proposes" });
    fireEvent.click(within(foldedProposal).getByRole("button", { name: "Accept Name a delivery fallback" }));
    await waitFor(() => expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/proposals/proposal-1/decisions",
      expect.objectContaining({ method: "POST" }),
    ));
    const proposalCall = fetcher.mock.calls.find(([url]) => String(url).includes("/proposals/"));
    expect(JSON.parse(String(proposalCall?.[1]?.body))).toMatchObject({
      accepted: true,
      surface: "folded_read",
    });
  });

  it("starts with the full prototype read and collapses it on demand", () => {
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const shell = container.querySelector("main");
    expect(shell).toHaveClass("is-r2-slice-one");
    expect(shell).toHaveClass("r2-integrity-expanded");

    const toggle = screen.getByRole("button", {
      name: "Collapse Outcome Integrity",
    });
    expect(toggle).toHaveAttribute("aria-expanded", "true");

    fireEvent.click(toggle);

    expect(shell).not.toHaveClass("r2-integrity-expanded");
    expect(screen.getByRole("button", { name: "Expand Outcome Integrity" })).toHaveAttribute(
      "aria-expanded",
      "false",
    );
  });

  it("matches the R2 Slice 1 shell taxonomy and evidence-qualified advisor read", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          project_title: "Northstar migration",
          artifacts: [
            {
              artifact_type: "intent",
              title: "Intent",
              summary: "Move the Northstar platform without interrupting customers.",
              reliability: "High",
              evidence_refs: ["document:brief:page:1:fragment:0"],
              basis: "supported",
            },
            ...snapshot.artifacts,
          ],
        }}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("img", { name: "Intralign" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Outcome:/i })).not.toBeInTheDocument();

    const workspace = screen.getByRole("navigation", { name: "Workspace" });
    expect(within(workspace).getAllByRole("link").map((link) => link.textContent)).toEqual([
      expect.stringContaining("Issues"),
      expect.stringContaining("Your Outcome"),
      expect.stringContaining("Grounding map"),
      expect.stringContaining("Reports"),
      expect.stringContaining("History"),
    ]);
    expect(
      within(workspace).queryByRole("link", { name: "Attention map" }),
    ).not.toBeInTheDocument();
    expect(within(workspace).getByRole("link", { name: "Your Outcome" })).toHaveAttribute(
      "href",
      "/projects/project-001/outcome",
    );
    expect(
      screen.queryByRole("button", { name: "Manage Outcomes" }),
    ).not.toBeInTheDocument();

    const advisor = screen.getByRole("complementary", {
      name: "OSLO project advisor",
    });
    expect(within(advisor).getByText("On your read", { exact: false })).toBeInTheDocument();
    expect(within(advisor).getByText("Reasoning")).toBeInTheDocument();
    expect(within(advisor).getByText("Reliability basis")).toBeInTheDocument();
    expect(within(advisor).getByText("Reliability basis").closest("section")).toHaveTextContent(
      "0 load-bearing details grounded · 1 still OSLO's inference",
    );
    expect(within(advisor).getByText(/Your next move/)).toBeInTheDocument();
  });

  it("uses canonical provenance for the Overview load-bearing grounding count", () => {
    const canonicalSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        integrity: {
          ...snapshot.assessment.integrity,
          decomposition: snapshot.assessment.integrity.decomposition.map((pillar) =>
            pillar.key === "Grounding"
              ? { ...pillar, why: ["38 of 54 load-bearing items rest on evidence"] }
              : pillar,
          ),
        },
      },
      provenance: {
        schema_version: 1,
        artifacts: [],
        assumptions: [],
        grounded_claims: 47,
        inferred_claims: 45,
        total_claims: 92,
        load_bearing_inferences: 0,
        grounding: {
          grounded: 47,
          addressed: 0,
          routed: 0,
          inferred: 0,
          total: 47,
          basis: 1,
          band: "Sound",
        },
        structure: {
          unconfirmed_dependencies: 0,
          unowned_parties: 0,
          untraceable_numbers: 0,
        },
        this_week: {
          user_grounded: 0,
          oslo_inferred: 0,
        },
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={canonicalSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    const integritySummary = screen.getByRole("region", {
      name: "Outcome Integrity summary",
    });
    expect(
      within(integritySummary).getByText("Grounded 47 of 47 load-bearing"),
    ).toBeInTheDocument();
    expect(
      within(integritySummary).queryByText("38 of 54 load-bearing items rest on evidence"),
    ).not.toBeInTheDocument();
  });

  it("labels an inferred primary outcome honestly and uses its managed title", () => {
    render(
      <ProjectOverview
        displayName="Taimoor"
        initial={snapshot}
        initialOutcome={{
          id: "outcome-1",
          workspace_id: "workspace-1",
          project_id: snapshot.project_id,
          title: "Launch Atlas commerce for wholesale customers",
          status: "active",
          is_primary: true,
          provenance: "inferred",
          created_at: "2026-08-14T00:00:00Z",
          archived_at: null,
        }}
        logoutAction={vi.fn()}
      />,
    );

    const outcome = screen.getByRole("button", {
      name: /Outcome: Launch Atlas commerce for wholesale customers/i,
    });
    expect(within(outcome).getByText("OSLO inference")).toBeInTheDocument();
    expect(within(outcome).queryByText("✓ yours")).not.toBeInTheDocument();
  });

  it("restores the Overview scroll position after returning from Grounding map", () => {
    vi.useFakeTimers();
    const scrollTo = vi.fn();
    const originalScrollTo = Object.getOwnPropertyDescriptor(
      HTMLElement.prototype,
      "scrollTo",
    );
    Object.defineProperty(HTMLElement.prototype, "scrollTo", {
      configurable: true,
      value: scrollTo,
    });
    const requestAnimationFrame = vi
      .spyOn(window, "requestAnimationFrame")
      .mockImplementation((callback) => {
        callback(0);
        return 1;
      });
    const cancelAnimationFrame = vi
      .spyOn(window, "cancelAnimationFrame")
      .mockImplementation(() => undefined);
    const overview = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    const overviewScrollRegion = screen.getByRole("region", {
      name: "Project content",
    });
    Object.defineProperty(overviewScrollRegion, "scrollTop", {
      configurable: true,
      value: 640,
    });
    const workspace = screen.getByRole("navigation", { name: "Workspace" });
    fireEvent.click(
      within(workspace).getByRole("link", { name: "Grounding map" }),
    );

    expect(sessionStorage.getItem("oslo:overview-scroll:project-001")).toBe("640");

    overview.unmount();
    render(
      <StrictMode>
        <ProjectOverview
          displayName="Alex"
          initial={snapshot}
          logoutAction={vi.fn()}
        />
      </StrictMode>,
    );
    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(scrollTo).toHaveBeenCalledWith({ behavior: "auto", top: 640 });
    expect(scrollTo.mock.calls.length).toBeGreaterThanOrEqual(3);
    expect(sessionStorage.getItem("oslo:overview-scroll:project-001")).toBeNull();

    cancelAnimationFrame.mockRestore();
    requestAnimationFrame.mockRestore();
    if (originalScrollTo) {
      Object.defineProperty(
        HTMLElement.prototype,
        "scrollTo",
        originalScrollTo,
      );
    } else {
      delete (HTMLElement.prototype as { scrollTo?: unknown }).scrollTo;
    }
  });

  it("renders the Slice 1 outcome-integrity read and its three pillar drills", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const integrityTrigger = screen.getByRole("button", {
        name: /Outcome Integrity Developing, limited by Grounding/i,
      });
    expect(integrityTrigger).toBeInTheDocument();
    expect(within(integrityTrigger).getByText("Viability Solid")).toBeInTheDocument();
    expect(within(integrityTrigger).getByText("Grounding Developing")).toBeInTheDocument();
    expect(within(integrityTrigger).getByText("Adaptability Solid")).toBeInTheDocument();
    expect(screen.getAllByText("as of this analysis").length).toBeGreaterThan(0);
    expect(screen.getByText(/live tracking begins at execution/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Viability Solid/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Grounding Developing/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Adaptability Solid/i })).toBeInTheDocument();
    expect(screen.queryByText("52")).not.toBeInTheDocument();
  });

  it("renders the project shell and evidence-qualified integrity read", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("navigation", { name: "Workspace" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Issues 1" })).toHaveAttribute(
      "href",
      "/projects/project-001/issues",
    );
    expect(screen.getByRole("link", { name: "History" })).toHaveAttribute(
      "href",
      "/projects/project-001/history",
    );
    expect(screen.getAllByText("Developing").length).toBeGreaterThan(0);
    expect(screen.getByText("Why a maturity read, not a probability?")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Show Viability detail" })).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Timeline" })).not.toBeInTheDocument();
  });

  it("exposes navigation, project content, and advisor as independent regions", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(
      screen.getByRole("complementary", { name: "Project navigation" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("region", { name: "Project content" }),
    ).toBeInTheDocument();
    const advisor = screen.getByRole("complementary", {
      name: "OSLO project advisor",
    });
    expect(advisor).toBeInTheDocument();
    expect(advisor.parentElement).toHaveClass("project-sidepanel-slot");
    expect(
      screen.getByRole("region", { name: "OSLO conversation" }),
    ).toBeInTheDocument();
  });

  it("renders the five-step integrity ramp without exposing the numeric score", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          assessment: {
            ...snapshot.assessment,
            understanding_stage: "orientation",
          },
        }}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getAllByText("Fragile").length).toBeGreaterThan(0);
    expect(screen.getByText("Weak")).toBeInTheDocument();
    expect(screen.getAllByText("Developing").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Solid").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Sound").length).toBeGreaterThan(0);
    expect(screen.queryByText("/100")).not.toBeInTheDocument();
  });

  it("uses the membership orientation state instead of a stale browser-wide flag", async () => {
    vi.useFakeTimers();
    localStorage.setItem("oslo_orientation_seen", "true");

    render(
      <ProjectOverview
        displayName="New member"
        initial={{ ...snapshot, orientation_seen: false }}
        logoutAction={vi.fn()}
      />,
    );

    await act(async () => {
      await vi.runOnlyPendingTimersAsync();
    });

    expect(screen.getByRole("dialog", { name: "How OSLO works" })).toBeInTheDocument();
  });

  it("opens the searchable project command palette with routes and live issues", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Search project" }));

    expect(screen.getByRole("dialog", { name: "Search or jump to" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /Overview/i })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /^Intent$/i })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /^Resources$/i })).toBeInTheDocument();
    expect(
      screen.getByRole("option", { name: /Migration ownership is unresolved/i }),
    ).toBeInTheDocument();
  });

  it("opens the prototype settings modal from the account menu", async () => {
    vi.stubGlobal("matchMedia", vi.fn().mockReturnValue({
      matches: false,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));
    vi.stubGlobal("fetch", vi.fn().mockImplementation(async (input: string) => {
      if (input === "/api/workspace/preferences") {
        return Response.json({
          theme: "dark",
          analysis_notifications: true,
          failure_notifications: true,
          stale_notifications: true,
          display_name: "Alex Morgan",
          role_title: "I run the plan",
          workspace_name: "OSLO Alpha",
          actor_role: "owner",
          mentions_notifications: true,
          reply_notifications: true,
          shared_notifications: true,
        });
      }
      if (input === "/api/workspace") {
        return Response.json({
          id: "workspace-1",
          name: "OSLO Alpha",
          role: "owner",
          plan: "free",
          plan_label: "Free",
          price_usd_monthly: 0,
          document_limit: 20,
          word_limit: 50_000,
          collaborator_seat_limit: 3,
          monthly_analysis_limit: 8,
          monthly_analyses_used: 1,
          can_manage_plan: true,
          member_count: 1,
          projects: [],
          notifications: [],
        });
      }
      return Response.json({});
    }));
    render(
      <ProjectOverview
        displayName="Alex Morgan"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const navigation = screen.getByRole("complementary", {
      name: "Project navigation",
    });
    const account = within(navigation).getByRole("button", {
      name: "Open account menu for Alex Morgan",
    });
    expect(account).toHaveAttribute("title", "Account and settings");

    fireEvent.click(account);

    const menu = account.closest("details")?.querySelector(".project-account-menu");
    expect(menu).toBeInTheDocument();
    expect(within(menu as HTMLElement).getByRole("button", { name: "Settings" })).toBeInTheDocument();
    expect(within(menu as HTMLElement).getByRole("button", { name: "Take a quick tour" })).toBeInTheDocument();
    expect(within(menu as HTMLElement).getByRole("button", { name: "Replay walkthrough" })).toBeInTheDocument();
    expect(within(menu as HTMLElement).getByRole("button", { name: "Log out" })).toBeInTheDocument();
    expect(within(menu as HTMLElement).queryByText("Account & workspace")).not.toBeInTheDocument();
    fireEvent.click(within(menu as HTMLElement).getByRole("button", { name: "Settings" }));
    expect(await screen.findByRole("heading", { name: "Profile" })).toBeInTheDocument();
    expect(screen.getByRole("dialog", { name: "Settings" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Close settings" }));
    const footer = navigation.querySelector(".workspace-sidebar-footer");
    const planButton = await within(footer as HTMLElement).findByRole("button", { name: "Free" });
    fireEvent.click(planButton);
    expect(await screen.findByRole("heading", { name: "Plan & usage" })).toBeInTheDocument();
  });

  it("opens the integrity breakdown from the toolbar", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const trigger = screen.getByRole("button", {
      name: "Outcome Integrity Developing, limited by Grounding",
    });
    trigger.focus();
    fireEvent.click(trigger);

    expect(screen.getByRole("dialog", { name: "Integrity breakdown" })).toBeInTheDocument();
    expect(screen.getByText("The lowest pillar sets the overall integrity level.")).toBeInTheDocument();
    expect(screen.getAllByText("2 of 4 grounded").length).toBeGreaterThan(0);
    const close = screen.getByRole("button", { name: "Close integrity breakdown" });
    expect(close).toHaveFocus();

    fireEvent.keyDown(close, { key: "Escape" });

    expect(screen.queryByRole("dialog", { name: "Integrity breakdown" })).not.toBeInTheDocument();
    expect(trigger).toHaveFocus();
  });

  it("renders artifact pages in the prototype three-column workspace shell", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({
          artifact_type: "intent",
          title: "Intent",
          content: {
            sections: [
              {
                heading: "Purpose",
                body: "Deliver the agreed outcome.",
                bullets: [],
                columns: [],
                rows: [],
              },
            ],
          },
          version: 1,
          provenance: "from_oslo",
          reliability: "Moderate",
          basis: "derived",
          evidence_refs: [],
          issues: [],
          updated_at: "2026-08-14T00:00:00Z",
        }),
      ),
    );

    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="intent"
        logoutAction={vi.fn()}
      />,
    );

    expect(container.querySelector("main")).toHaveClass(
      "is-r2-artifact-workspace",
    );
    expect(screen.getByRole("region", { name: "Workspace open" })).toBeVisible();
    expect(screen.getByRole("complementary", { name: "Project navigation" })).toBeVisible();
    expect(screen.getByRole("complementary", { name: "OSLO project advisor" })).toBeVisible();

    const integrityToggle = screen.getByRole("button", {
      name: "Expand Outcome Integrity",
    });
    fireEvent.click(integrityToggle);

    const integritySummary = screen.getByRole("region", {
      name: "Outcome Integrity summary",
    });
    expect(integritySummary).toBeVisible();
    expect(within(integritySummary).getByRole("button", { name: /Viability/i })).toBeVisible();
    expect(within(integritySummary).getByRole("button", { name: /Grounding/i })).toBeVisible();
    expect(within(integritySummary).getByRole("button", { name: /Adaptability/i })).toBeVisible();
    expect(screen.queryByRole("dialog", { name: "Outcomes" })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Hide the OSLO panel" }));
    expect(container.querySelector(".project-grid")).toHaveClass("is-panel-closed");
    expect(screen.getByRole("button", { name: "Ask OSLO" })).toHaveClass(
      "advisor-floating",
    );
  });

  it("keeps OSLO collapsed when navigating between project sections", () => {
    const overview = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="overview"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Hide the OSLO panel" }));
    expect(sessionStorage.getItem("oslo:advisor-open:project-001")).toBe("false");
    overview.unmount();

    const history = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="history"
        logoutAction={vi.fn()}
      />,
    );

    expect(history.container.querySelector(".project-grid")).toHaveClass("is-panel-closed");
    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Ask OSLO" })).toHaveClass(
      "advisor-floating",
    );
  });

  it.each(["outcome", "inference", "rollup", "grounding", "history", "reports", "full_plan"] as const)(
    "keeps the Outcome Integrity expander available on the %s section",
    (initialView) => {
      const { container } = render(
        <ProjectOverview
          displayName="Alex"
          initial={snapshot}
          initialView={initialView}
          logoutAction={vi.fn()}
        />,
      );

      const integrityToggle = screen.getByRole("button", {
        name: "Expand Outcome Integrity",
      });
      expect(integrityToggle).toBeVisible();
      expect(
        screen.getByRole("link", { name: "Full plan · export" }),
      ).toHaveAttribute("href", "/projects/project-001/full-plan");

      if (initialView === "full_plan") {
        expect(container.querySelector("main")).toHaveClass(
          "is-r2-reports",
          "is-r2-full-plan",
        );
        expect(
          screen.queryByRole("button", { name: /^Outcome:/ }),
        ).not.toBeInTheDocument();
      }

      fireEvent.click(integrityToggle);

      expect(container.querySelector("main")).toHaveClass("r2-integrity-expanded");
      expect(
        screen.getByRole("region", { name: "Outcome Integrity summary" }),
      ).toBeVisible();
      expect(
        screen.getByRole("button", { name: "Collapse Outcome Integrity" }),
      ).toBeVisible();
    },
  );

  it("uses one aligned notice width contract across Overview status banners", () => {
    const noticeSnapshot: OverviewSnapshot = {
      ...snapshot,
      freshness: {
        state: "stale",
        pending_count: 1,
        latest_pending_event_id: null,
        active_run_id: null,
      },
      read_moved_notifications: [
        {
          id: "moved-001",
          previous_band: "Moderate",
          current_band: "Moderate",
          settled_causes: [],
        },
      ],
    };

    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={noticeSnapshot}
        initialView="overview"
        logoutAction={vi.fn()}
      />,
    );

    expect(container.querySelectorAll(".r2-overview-notice")).toHaveLength(3);
    expect(screen.getByRole("region", { name: "Workspace open" })).toHaveClass(
      "r2-overview-notice",
    );
  });

  it("does not count structured row body and bullet encodings as additional open inferences", () => {
    const structuredSnapshot: OverviewSnapshot = {
      ...snapshot,
      artifacts: [
        {
          artifact_type: "intent",
          title: "Intent",
          summary: "Measured launch outcomes.",
          reliability: "High",
          evidence_refs: ["document:brief:page:1:fragment:0"],
          basis: "supported",
          content: {
            sections: [
              {
                heading: "Objectives and success measures",
                body: "KPI Target Orders 99.7% successful",
                bullets: ["Orders | 99.7% successful"],
                columns: ["KPI", "Target"],
                rows: [["Orders", "99.7% successful"]],
                provenance: "from_oslo",
                row_states: ["confirmed"],
                row_provenance: ["confirmed_by_user"],
              },
            ],
          },
        },
      ],
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={structuredSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    const intentLink = screen.getByRole("link", { name: "Intent" });
    expect(intentLink.querySelector(".r2-artifact-indicators")).toHaveAttribute(
      "title",
      "0 proposals, 0 open",
    );
    expect(intentLink.querySelector(".is-open")).toBeNull();
  });

  it("explains the deterministic maturity basis without another advisor call", async () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const disclosureSummary = screen.getByText("Why a maturity read, not a probability?");
    const disclosure = disclosureSummary.closest("details");
    fireEvent.click(disclosureSummary);

    expect(screen.getByText(snapshot.assessment.confidence_explanation)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByRole("main")).toHaveClass("r2-integrity-detail-open");
    });
    expect(disclosure).toHaveAttribute("open");
    expect(within(disclosure as HTMLElement).queryByText("Clarity")).not.toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher).toHaveBeenCalledWith("/api/workspace", { cache: "no-store" });

    fireEvent.click(disclosureSummary);
    await waitFor(() => {
      expect(screen.getByRole("main")).not.toHaveClass("r2-integrity-detail-open");
    });
  });

  it("warns when a high confidence score rests on low-reliability evidence", () => {
    const highButWeak: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        confidence_index: 84,
        confidence_band: "High",
        reliability: "Low",
        false_confidence: true,
      },
    };
    render(
      <ProjectOverview
        displayName="Alex"
        initial={highButWeak}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("alert")).toHaveTextContent(
      /sits high on thin evidence/i,
    );
  });

  it("keeps the governed advisor beside R2 issue review and restores focus when it closes", async () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    const issueButton = screen.getByRole("button", { name: /Migration ownership is unresolved/i });
    issueButton.focus();
    fireEvent.click(issueButton);

    expect(screen.getByLabelText("OSLO project advisor")).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));

    await waitFor(() => {
      expect(screen.getByLabelText("OSLO project advisor")).toBeInTheDocument();
      expect(
        screen.getByRole("button", {
          name: /Migration ownership is unresolved/i,
        }),
      ).toHaveFocus();
    });
  });

  it("restores focus to the recreated issue row when Escape closes inline review", async () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    const issueButton = screen.getByRole("button", {
      name: /Migration ownership is unresolved/i,
    });
    issueButton.focus();
    fireEvent.click(issueButton);

    fireEvent.keyDown(window, { key: "Escape" });

    await waitFor(() => {
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument();
      expect(screen.getByRole("button", {
        name: /Migration ownership is unresolved/i,
      })).toHaveFocus();
    });
  });

  it("keeps the prototype advisor collapsed while an issue panel is open", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Hide the OSLO panel" }));
    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();

    fireEvent.click(
      screen.getByRole("button", {
        name: /Migration ownership is unresolved/i,
      }),
    );

    expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument();
    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Ask OSLO" })).toHaveClass(
      "advisor-floating",
    );
  });

  it("matches the first-run focus handoff after the outcome is confirmed", async () => {
    const firstRunSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        unlock_threshold: 2,
        ever_unlocked: false,
        freeze_on: true,
      },
    };
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={firstRunSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    await waitFor(() => {
      expect(container.querySelector(".project-shell")).toHaveClass(
        "is-first-run-frozen",
      );
      expect(screen.getByText("You confirmed your outcome")).toBeInTheDocument();
      expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument();
    });
    expect(screen.queryByText("Your workspace is open.")).not.toBeInTheDocument();
    expect(screen.getByText("One call down - you confirmed your outcome.")).toBeInTheDocument();
    expect(screen.getByText("One more decision completes your guided review.")).toBeInTheDocument();
    expect(screen.queryByText(/opens your full workspace/i)).not.toBeInTheDocument();
    const startHere = screen.getByRole("button", {
      name: /Start here: settle .*Migration ownership is unresolved/i,
    });
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));
    await waitFor(() =>
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument(),
    );
    fireEvent.click(startHere);
    await waitFor(() =>
      expect(screen.getByRole("region", { name: "Issue details" })).toHaveFocus(),
    );
    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^Ask OSLO$/i })).toHaveClass(
      "advisor-floating",
    );
  });

  it("opens the next actionable grounding issue when first-run onboarding has no untouched issue", async () => {
    const firstRunSnapshot: OverviewSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        unlock_threshold: 2,
        ever_unlocked: false,
        freeze_on: true,
      },
      assessment: {
        ...snapshot.assessment,
        issues: snapshot.assessment.issues.map((issue) => ({
          ...issue,
          status: "needs_grounding" as const,
          primary_act: "verify" as const,
        })),
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={firstRunSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    await waitFor(() => {
      expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument();
    });
    expect(screen.getByRole("button", { name: "Confirm — it holds" })).toBeVisible();
    expect(screen.getByRole("button", {
      name: /Start here: settle .*Migration ownership is unresolved/i,
    })).toBeEnabled();
  });

  it("foregrounds verification during frozen first-run onboarding when it is an allowed alternative", async () => {
    const firstRunSnapshot: OverviewSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        unlock_threshold: 2,
        ever_unlocked: false,
        freeze_on: true,
      },
      assessment: {
        ...snapshot.assessment,
        issues: snapshot.assessment.issues.map((issue) => ({
          ...issue,
          primary_act: "build" as const,
          also_offered: ["verify" as const],
          classification_state: "classified" as const,
        })),
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={firstRunSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    await waitFor(() => {
      expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument();
    });
    expect(screen.getByRole("button", { name: "Confirm — it holds" })).toBeVisible();
    expect(screen.queryByRole("button", { name: "Apply this fix →" })).not.toBeInTheDocument();
  });

  it("opens a verifiable issue for the second first-run confirmation", async () => {
    const firstRunSnapshot: OverviewSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        unlock_threshold: 2,
        ever_unlocked: false,
        freeze_on: true,
      },
      assessment: {
        ...snapshot.assessment,
        issues: [
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-BUILD-FIRST",
            title: "Delivery scope needs to be built",
            primary_act: "build" as const,
            also_offered: [],
            classification_state: "classified" as const,
          },
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-VERIFY-SECOND",
            severity: "Moderate" as const,
            title: "Owner evidence needs confirmation",
            primary_act: "verify" as const,
            also_offered: ["build" as const],
            classification_state: "classified" as const,
          },
        ],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={firstRunSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    const issuePanel = await screen.findByRole("region", { name: "Issue details" });
    expect(within(issuePanel).getByText("Owner evidence needs confirmation")).toBeVisible();
    expect(within(issuePanel).getByRole("button", { name: "Confirm — it holds" })).toBeVisible();
    expect(within(issuePanel).queryByRole("button", { name: "Apply this fix →" })).not.toBeInTheDocument();
  });

  it("treats the first-run outcome confirmation as transient feedback", async () => {
    vi.useFakeTimers();
    window.sessionStorage.removeItem("r2-first-run-recorded:project-001");
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          first_run: {
            first_run: true,
            onboarded: false,
            grounding_act_count: 1,
            unlock_threshold: 2,
            ever_unlocked: false,
            freeze_on: true,
          },
        }}
        logoutAction={vi.fn()}
      />,
    );

    await act(async () => Promise.resolve());
    expect(screen.getByText("You confirmed your outcome")).toBeInTheDocument();
    act(() => vi.advanceTimersByTime(2300));

    expect(screen.queryByText("You confirmed your outcome")).not.toBeInTheDocument();
    expect(screen.getByText("One call down - you confirmed your outcome.")).toBeInTheDocument();
  });

  it("moves focus to the next ranked issue after the opened issue is confirmed", async () => {
    const nextIssue = {
      ...snapshot.assessment.issues[0],
      id: "ISS-002",
      severity: "Moderate" as const,
      title: "Cutover fallback is unresolved",
    };
    const firstRunSnapshot: OverviewSnapshot = {
      ...snapshot,
      first_run: {
        first_run: true,
        onboarded: false,
        grounding_act_count: 1,
        unlock_threshold: 2,
        ever_unlocked: false,
        freeze_on: true,
      },
      assessment: {
        ...snapshot.assessment,
        issues: [...snapshot.assessment.issues, nextIssue],
      },
    };
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        Response.json({
          issue_id: "ISS-001",
          status: "addressed",
          analysis_run: null,
        }),
      ),
    );

    render(
      <ProjectOverview
        displayName="Alex"
        initial={firstRunSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    await waitFor(() =>
      expect(screen.getByRole("region", { name: "Issue details" })).toBeInTheDocument(),
    );
    fireEvent.click(screen.getByRole("button", { name: "Confirm — it holds" }));
    fireEvent.click(screen.getByRole("button", { name: "I’ve verified this directly" }));
    const queue = screen.getByRole("region", { name: "Exposure-ranked issue queue" });
    await waitFor(() =>
      expect(
        within(queue).getByRole("button", { name: /Cutover fallback is unresolved/i }),
      ).toBeInTheDocument(),
    );
    await waitFor(() =>
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument(),
    );
  });

  it("offers the prototype governed and wider advisor controls", () => {
    const { container } = render(
      <ProjectOverview displayName="Alex" initial={snapshot} logoutAction={vi.fn()} />,
    );

    expect(screen.getByText("Governed")).toBeInTheDocument();
    const widen = screen.getByRole("button", { name: "Widen OSLO panel" });
    fireEvent.click(widen);
    expect(container.querySelector(".project-grid")).toHaveClass("is-advisor-wide");
    expect(screen.getByRole("button", { name: "Narrow OSLO panel" })).toBeInTheDocument();
  });

  it("opens an Overview issue inline in the ranked queue without a popup", async () => {
    const scrollIntoView = vi.fn();
    const originalScrollIntoView = HTMLElement.prototype.scrollIntoView;
    HTMLElement.prototype.scrollIntoView = scrollIntoView;
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const queue = screen.getByRole("region", {
      name: "Exposure-ranked issue queue",
    });
    const issueButton = within(queue).getByRole("button", {
      name: /Migration ownership is unresolved/i,
    });

    fireEvent.click(issueButton);

    const detail = screen.getByRole("region", { name: "Issue details" });
    expect(detail.closest(".r2-issue-focus-layer")).toBeNull();
    expect(queue).toContainElement(detail);
    expect(detail).toHaveClass("is-inline");
    expect(detail).not.toHaveAttribute("aria-modal");
    expect(issueButton).not.toBeInTheDocument();
    expect(
      within(queue).queryByRole("button", {
        name: /Migration ownership is unresolved/i,
      }),
    ).not.toBeInTheDocument();
    expect(within(detail).getByText("Affects")).toBeInTheDocument();
    expect(within(detail).getByText("Holds up")).toBeInTheDocument();
    expect(
      within(detail).getByText("No downstream dependency path was published."),
    ).toBeInTheDocument();
    expect(
      within(detail).getAllByText("No accountable owner is identified."),
    ).toHaveLength(1);
    expect(screen.getByText("Your work — most important first")).toBeInTheDocument();
    await waitFor(() => expect(scrollIntoView).toHaveBeenCalledWith({
      behavior: "auto",
      block: "start",
    }));

    if (originalScrollIntoView) {
      HTMLElement.prototype.scrollIntoView = originalScrollIntoView;
    } else {
      delete (HTMLElement.prototype as { scrollIntoView?: unknown }).scrollIntoView;
    }
  });

  it("records a confirmation basis in the same tap instead of using a basis-free confirm", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ issue_id: "ISS-001", status: "resolved" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          assessment: {
            ...snapshot.assessment,
            issues: snapshot.assessment.issues.map((issue) => ({
              ...issue,
              primary_act: "verify" as const,
            })),
          },
        }}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));

    fireEvent.click(screen.getByRole("button", { name: "Confirm — it holds" }));
    expect(screen.getByRole("group", { name: "It holds because" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "I’ve verified this directly" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalled());
    const request = fetchMock.mock.calls.find(([url]) => String(url).endsWith("/acts"));
    expect(JSON.parse(String(request?.[1]?.body))).toMatchObject({
      act: "confirm",
      basis: "verified-directly",
    });
  });

  it("shows the actual downstream dependency path instead of repeating why the issue matters", () => {
    const tracedSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        issues: [{
          ...snapshot.assessment.issues[0],
          sensitivity_trace: {
            paths: [["migration-owner", "migration-ready", "safe-launch"]],
            dependency_paths: [["Migration owner", "Migration readiness", "Safe launch"]],
            outcome_dependencies: ["Safe launch"],
            span_true: 0.8,
            span_false: 0.2,
            span: 0.6,
            leverage: 0.8,
            uncertainty_factor: 1.2,
            runway_factor: 1,
            edge_key: null,
            outcome_reachability: ["safe-launch"],
          },
        }],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={tracedSnapshot}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );

    const detail = screen.getByRole("region", { name: "Issue details" });
    expect(
      within(detail).getByText("Migration readiness → Safe launch"),
    ).toBeInTheDocument();
  });

  it("reveals readable evidence through a keyboard-operable disclosure and hides locator ids", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );

    const evidenceDisclosure = screen.getByRole("button", {
      name: "Evidence · 1 source, traceable to inputs",
    });
    expect(evidenceDisclosure).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByText("Migration plan.pdf")).not.toBeInTheDocument();

    evidenceDisclosure.focus();
    fireEvent.keyDown(evidenceDisclosure, { key: "Enter" });
    fireEvent.click(evidenceDisclosure);

    expect(evidenceDisclosure).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("Migration plan.pdf")).toBeInTheDocument();
    expect(screen.getByText("Page 1")).toBeInTheDocument();
    expect(
      screen.getByText("The accountable migration owner has not been confirmed."),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("document:plan:page:1:fragment:0"),
    ).not.toBeInTheDocument();
  });

  it("selects a governed resolution path and shows it as confirmed by the user", async () => {
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        issue_id: "ISS-001",
        action: "select",
        status: "addressed",
        selected_resolution: "Confirm an accountable owner.",
        analysis_run: null,
      }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );
    fireEvent.click(screen.getByRole("button", { name: "Other ways to handle this" }));
    fireEvent.click(screen.getByRole("button", { name: "Select this path" }));

    const confirmation = await screen.findByRole("status", { name: "Issue action recorded" });
    expect(confirmation).toHaveTextContent("Migration ownership is unresolved");
    expect(confirmation).toHaveTextContent("Settling to resolved");
    expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/issues/ISS-001/actions",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("restores the persisted selected resolution after a browser refresh", () => {
    const refreshedSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        issues: snapshot.assessment.issues.map((issue) => ({
          ...issue,
          status: "addressed",
          selected_resolution: "Assign Priya as the accountable migration owner.",
        })),
      },
    };
    render(
      <ProjectOverview
        displayName="Alex"
        initial={refreshedSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );

    expect(screen.getByText("Confirmed by you")).toBeInTheDocument();
    expect(
      screen.getByText("Assign Priya as the accountable migration owner."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Issue status addressed")).toBeInTheDocument();
  });

  it("confirms a recommendation through the typed Slice 2 lifecycle", async () => {
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        issue_id: "ISS-001",
        act: "confirm",
        status: "addressed",
        attestation: {
          id: "attestation-confirm-1",
          act: "confirm",
          basis: "verified-directly",
          evidence_ref: "document:plan:page:1:fragment:0",
          attributed_to: { id: "user-1", display_name: "Alex", role: "owner" },
          supersedes: null,
        },
        analysis_run: {
          run_id: "run-apply-001",
          project_id: "project-001",
          kind: "extended",
          status: "queued",
          consolidated_event_ids: ["event-apply-001"],
        },
      }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );
    fireEvent.click(screen.getByRole("button", { name: "Confirm — it holds" }));
    fireEvent.click(screen.getByRole("button", { name: "I’ve verified this directly" }));

    await waitFor(() => {
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument();
      expect(screen.queryByText("Your read is safely out of date.")).not.toBeInTheDocument();
      expect(screen.getByRole("status", { name: "Issue action recorded" })).toHaveTextContent(
        "Migration ownership is unresolved",
      );
      expect(screen.getByRole("status", { name: "Issue action recorded" })).toHaveTextContent(
        "Settling to resolved",
      );
    });
  });

  it("saves a clarification once and marks the issue addressed until analysis completes", async () => {
    let releaseResponse: ((value: unknown) => void) | undefined;
    const fetcher = vi.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          releaseResponse = resolve;
        }),
    );
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );
    fireEvent.click(
      screen.getByRole("button", { name: "Let OSLO ask you a question" }),
    );
    fireEvent.change(screen.getByLabelText("Clarification answer"), {
      target: { value: "Priya owns migration; the legacy import is the fallback." },
    });
    const submit = screen.getByRole("button", { name: "Submit answer →" });
    fireEvent.click(submit);
    fireEvent.click(submit);

    expect(
      fetcher.mock.calls.filter(([url]) =>
        url === "/api/projects/project-001/issues/ISS-001/answers"
      ),
    ).toHaveLength(1);
    releaseResponse?.({
      ok: true,
      json: async () => ({
        run_id: "run-clarification-001",
        consolidated_event_ids: ["event-clarification-001"],
      }),
    });

    await waitFor(() => {
      expect(screen.queryByRole("region", { name: "Issue details" })).not.toBeInTheDocument();
      expect(screen.getByRole("status", { name: "Issue action recorded" })).toHaveTextContent(
        "Migration ownership is unresolved",
      );
      expect(screen.queryByText("Your read is safely out of date.")).not.toBeInTheDocument();
    });
  });

  it("reconnects to an active clarification run after a browser refresh", async () => {
    vi.useFakeTimers();
    const runningSnapshot: OverviewSnapshot = {
      ...snapshot,
      extended_analysis: {
        run_id: "run-clarification-refresh",
        project_id: "project-001",
        kind: "extended",
        status: "running",
        phase: "evaluate_advise",
        completed_phases: ["perceive", "retrieve_evidence", "construct_artifacts"],
        error_code: null,
      },
    };
    const completedSnapshot: OverviewSnapshot = {
      ...snapshot,
      snapshot_id: "snap-clarification-complete",
      summary: "The refreshed clarification is now part of the current read.",
    };
    const fetcher = vi.fn().mockImplementation((url: string) => {
      if (url === "/api/analysis-runs/run-clarification-refresh") {
        return Promise.resolve({
          ok: true,
          json: async () => ({ status: "completed" }),
        });
      }
      if (url === "/api/projects/project-001/overview") {
        return Promise.resolve({
          ok: true,
          json: async () => completedSnapshot,
        });
      }
      return Promise.resolve({ ok: false });
    });
    vi.stubGlobal("fetch", fetcher);

    render(
      <ProjectOverview
        displayName="Alex"
        initial={runningSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    await act(async () => {
      await vi.advanceTimersByTimeAsync(2500);
    });

    expect(fetcher).toHaveBeenCalledWith(
      "/api/analysis-runs/run-clarification-refresh",
      { cache: "no-store" },
    );
    expect(
      screen.getByText("The refreshed clarification is now part of the current read."),
    ).toBeInTheDocument();
    vi.useRealTimers();
  });

  it("renders the delivered Issues workspace while keeping History honest", () => {
    const { rerender } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("heading", { name: "Issues" })).toBeInTheDocument();
    expect(screen.getByText("1 active finding")).toBeInTheDocument();

    rerender(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="history"
        logoutAction={vi.fn()}
      />,
    );
    expect(screen.getByRole("heading", { name: "History" })).toBeInTheDocument();
    expect(screen.getByText(/full decision history arrives in Slice 7/i)).toBeInTheDocument();
  });

  it("replays and completes the prototype-aligned five-step orientation tour", async () => {
    const { container } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialOutcome={{
          id: "outcome-1",
          workspace_id: "workspace-1",
          project_id: snapshot.project_id,
          title: "Complete the migration safely",
          status: "active",
          is_primary: true,
          provenance: "declared",
          created_at: "2026-08-16T00:00:00Z",
          archived_at: null,
        }}
        logoutAction={vi.fn()}
      />,
    );

    const sidebar = screen.getByRole("complementary", { name: "Project navigation" });
    const footer = sidebar.querySelector(".workspace-sidebar-footer");
    fireEvent.click(footer?.querySelector(":scope > button:first-of-type") as HTMLButtonElement);

    expect(screen.getByText("Step 1 of 5")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Outcome Integrity" })).toBeInTheDocument();
    expect(screen.getByRole("button", {
      name: "Outcome Integrity Developing, limited by Grounding",
    })).toHaveClass("is-tour-target");
    expect(screen.queryByRole("button", { name: "Back" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    expect(screen.getByText("Step 2 of 5")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Outcome: Complete the migration safely/i })).toHaveClass("is-tour-target");

    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    expect(screen.getByText("Step 3 of 5")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Migration ownership is unresolved/i })).toHaveClass("is-tour-target");

    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    expect(screen.getByText("Step 4 of 5")).toBeInTheDocument();
    expect(container.querySelector(".workspace-artifact-group")).toHaveClass("is-tour-target");

    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    expect(screen.getByText("Step 5 of 5")).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: "Ask OSLO" }).closest("form")).toHaveClass("is-tour-target");
    expect(screen.getByRole("heading", { name: "OSLO — advisory" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Back" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Done" }));

    await waitFor(() => {
      expect(screen.queryByRole("dialog", { name: "How OSLO works" })).not.toBeInTheDocument();
      expect(localStorage.getItem("oslo_orientation_seen")).toBe("true");
    });
  });

  it("sends a quick question to the project advisor and renders its grounded reply", async () => {
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        answer: "Confirm the migration owner first because the dependency blocks delivery.",
        follow_up_questions: ["Who can approve the owner?"],
      }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "What should I do next?" }));

    expect(await screen.findByText(/Confirm the migration owner first/)).toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/advisor",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ question: "What should I do next?" }),
      }),
    );
    expect(screen.getByRole("button", { name: "Who can approve the owner?" })).toBeInTheDocument();
  });

  it("routes new-project creation through the workspace switcher", async () => {
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        id: "workspace-001",
        name: "OSLO Alpha",
        role: "owner",
        plan: "free",
        active_project_count: 1,
        can_create_project: false,
        projects: [{
          id: "project-001",
          name: "Migration plan",
          archived: false,
          analysis_status: "current",
          confidence_index: 52,
          confidence_band: "Moderate",
          open_issue_count: 1,
          updated_at: "2026-07-23T12:00:00Z",
          owner_id: "user-001",
        }],
        notifications: [],
      }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Project" }));

    const newProject = await screen.findByRole("menuitem", { name: /New project/i });
    expect(newProject).toHaveAttribute("href", "/workspace?new=1");
    expect(screen.queryByRole("button", { name: "New project" })).not.toBeInTheDocument();
  });

  it("shows a retryable message when the advisor is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.change(screen.getByLabelText("Ask OSLO"), {
      target: { value: "Explain the migration risk" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));

    expect(
      await screen.findByText("OSLO could not answer right now. Your project data is unchanged."),
    ).toBeInTheDocument();
  });

  it("shows a failed clarification re-analysis on a current snapshot and retries it", async () => {
    const failedSnapshot: OverviewSnapshot = {
      ...snapshot,
      state: "current",
      extended_analysis: {
        run_id: "run-extended-001",
        project_id: "project-001",
        kind: "extended",
        status: "failed",
        phase: "perceive",
        completed_phases: [],
        error_code: "OPENAI_QUOTA",
      },
    };
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        ...failedSnapshot.extended_analysis,
        status: "running",
      }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={failedSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("This read needs another attempt")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Your documents are safe. OSLO did not publish an incomplete read. Please retry the analysis. The last successful read is unchanged.",
      ),
    ).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Retry Extended Analysis" }));

    await waitFor(() => {
      expect(fetcher).toHaveBeenCalledWith(
        "/api/analysis-runs/run-extended-001/retry",
        { method: "POST" },
      );
      expect(screen.getByText("Extended Analysis is retrying")).toBeInTheDocument();
    });
  });

  it("reconnects a retried clarification run and publishes its completed read", async () => {
    const failedSnapshot: OverviewSnapshot = {
      ...snapshot,
      state: "current",
      extended_analysis: {
        run_id: "run-extended-retry",
        project_id: "project-001",
        kind: "extended",
        status: "failed",
        phase: "perceive",
        completed_phases: [],
        error_code: "OPENAI_QUOTA",
      },
    };
    const completedSnapshot: OverviewSnapshot = {
      ...failedSnapshot,
      extended_analysis: {
        ...failedSnapshot.extended_analysis!,
        status: "completed",
        phase: "extended_transition",
      },
    };
    const fetcher = vi.fn(async (input: string, init?: RequestInit) => {
      if (input === "/api/analysis-runs/run-extended-retry/retry" && init?.method === "POST") {
        return { ok: true, json: async () => ({ status: "running" }) };
      }
      if (input === "/api/analysis-runs/run-extended-retry") {
        return { ok: true, json: async () => ({ status: "completed" }) };
      }
      if (input === "/api/projects/project-001/overview") {
        return { ok: true, json: async () => completedSnapshot };
      }
      return { ok: false };
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={failedSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Retry Extended Analysis" }));

    await waitFor(
      () => {
        expect(fetcher).toHaveBeenCalledWith(
          "/api/analysis-runs/run-extended-retry",
          { cache: "no-store" },
        );
      },
      { timeout: 3500 },
    );
    await waitFor(() => {
      expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument();
    });
  });

  it("moves answered questions into the closed Progress readout", () => {
    const resolvedSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        resolved_issue_count: 1,
        confirmed_dependency_count: 1,
        issues: snapshot.assessment.issues.map((issue) => ({
          ...issue,
          status: "resolved",
        })),
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={resolvedSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("Questions answered")).toBeInTheDocument();
    expect(screen.getByText("Issues resolved")).toBeInTheDocument();
  });

  it("invalidates prefetched project routes after the orientation is dismissed", async () => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true }));
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{ ...snapshot, orientation_seen: false }}
        logoutAction={vi.fn()}
      />,
    );

    await act(async () => {
      await vi.runOnlyPendingTimersAsync();
    });
    vi.useRealTimers();
    fireEvent.click(screen.getByRole("button", { name: "Skip tour" }));

    await waitFor(() => {
      expect(refresh).toHaveBeenCalledTimes(1);
    });
  });

  it("clears recorded action feedback while reanalysis continues", async () => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        issue_id: "ISS-001",
        act: "confirm",
        status: "addressed",
        analysis_run: {
          run_id: "run-apply-001",
          project_id: "project-001",
          kind: "extended",
          status: "queued",
          consolidated_event_ids: ["event-apply-001"],
        },
      }),
    }));
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));
    fireEvent.click(screen.getByRole("button", { name: "Confirm — it holds" }));
    fireEvent.click(screen.getByRole("button", { name: "I’ve verified this directly" }));

    await act(async () => Promise.resolve());
    expect(screen.getByRole("status", { name: "Issue action recorded" })).toBeInTheDocument();
    act(() => vi.advanceTimersByTime(2700));

    expect(screen.queryByRole("status", { name: "Issue action recorded" })).not.toBeInTheDocument();
    expect(screen.getByText("Your read is safely out of date.")).toBeInTheDocument();
  });

  it("opens the tour on the read workspace when launched from another project view", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="history"
        logoutAction={vi.fn()}
      />,
    );

    const sidebar = screen.getByRole("complementary", { name: "Project navigation" });
    const footer = sidebar.querySelector(".workspace-sidebar-footer");
    fireEvent.click(footer?.querySelector(":scope > button:first-of-type") as HTMLButtonElement);

    expect(push).toHaveBeenCalledWith("/projects/project-001/overview?tour=1");
    expect(screen.queryByRole("dialog", { name: "How OSLO works" })).not.toBeInTheDocument();
  });

  it("resumes the requested tour after arriving on the read workspace", async () => {
    window.history.replaceState({}, "", "/projects/project-001/overview?tour=1");
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(await screen.findByText("Step 1 of 5")).toBeInTheDocument();
    expect(window.location.search).toBe("");
  });

  it("derives advisor settled counts from the live issue lifecycle", () => {
    const lifecycleSnapshot: OverviewSnapshot = {
      ...snapshot,
      assessment: {
        ...snapshot.assessment,
        resolved_issue_count: 0,
        issues: [
          snapshot.assessment.issues[0],
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-RESOLVED",
            status: "resolved",
            title: "Migration sponsor confirmed",
          },
        ],
      },
    };

    render(
      <ProjectOverview
        displayName="Alex"
        initial={lifecycleSnapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getAllByText("1 of 2")).not.toHaveLength(0);
  });
});

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

vi.mock("next/navigation", () => ({
  usePathname: () => "/projects/project-001/issues",
  useRouter: () => ({ push, replace }),
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
  replace.mockReset();
});

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("ProjectOverview", () => {
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

  it("renders the Slice 6 Issues workspace with live grouping and filters", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("heading", { name: "Issues" })).toBeInTheDocument();
    expect(screen.getByText("3 active findings")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "By dimension" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByRole("heading", { name: "Feasibility · 2" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Clarity · 1" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "By severity" }));
    expect(screen.getByRole("heading", { name: "Critical · 1" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Moderate · 2" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Resources 2" }));
    expect(screen.getByText("1 finding hidden by the current filters.")).toBeInTheDocument();
    expect(screen.queryByText("Success metric is not measurable")).not.toBeInTheDocument();
    expect(screen.getByText("Migration ownership is unresolved")).toBeInTheDocument();

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

    expect(screen.getByRole("button", { name: "Resources 2" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Critical 1" })).toBeInTheDocument();
    expect(screen.queryByText(/hidden by the current filters/i)).not.toBeInTheDocument();
    expect(screen.queryByText("Old resolved resource issue")).not.toBeInTheDocument();
  });

  it("opens the governed issue panel from an Issues workspace card", () => {
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
    expect(panel).toHaveTextContent("Clarification request");
  });

  it("renders the Slice 4 current-snapshot matrix without the superseded field toggle", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="attention"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("heading", { name: "Attention map" })).toBeInTheDocument();
    expect(
      screen.getByText(
        /Brighter = more attention — not a health score\. Click a cell to investigate\./,
      ),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Dimensions" })).not.toBeInTheDocument();
    expect(screen.getByRole("grid", { name: "Project attention map" })).toBeInTheDocument();
    expect(
      screen.getByRole("gridcell", {
        name: "Requirements Clarity: 1 issue, Moderate",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("gridcell", {
        name: "Resources Feasibility: 2 issues, Critical",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("gridcell", { name: "Intent Clarity: 0 issues" }),
    ).not.toHaveAttribute("tabindex");
  });

  it("opens one finding directly and routes multiple findings to a filtered Issues page", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="attention"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("gridcell", {
        name: "Requirements Clarity: 1 issue, Moderate",
      }),
    );
    expect(screen.getByRole("dialog", { name: "Issue details" })).toHaveTextContent(
      "Success metric is not measurable",
    );
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));

    fireEvent.click(
      screen.getByRole("gridcell", {
        name: "Resources Feasibility: 2 issues, Critical",
      }),
    );
    expect(push).toHaveBeenCalledWith(
      "/projects/project-001/issues?artifact=resources&dimension=feasibility",
    );
    expect(
      screen.queryByRole("dialog", { name: "Scoped attention findings" }),
    ).not.toBeInTheDocument();
  });

  it("routes an artifact row to Issues and keeps the natural all-clear state", () => {
    const { unmount } = render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="attention"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Open Resources findings" }));
    expect(push).toHaveBeenCalledWith(
      "/projects/project-001/issues?artifact=resources",
    );

    unmount();
    render(
      <ProjectOverview
        displayName="Alex"
        initial={{
          ...snapshot,
          assessment: {
            ...snapshot.assessment,
            issues: snapshot.assessment.issues.map((issue) => ({
              ...issue,
              status: "resolved",
            })),
          },
        }}
        initialView="attention"
        logoutAction={vi.fn()}
      />,
    );
    expect(screen.getByText("Nothing needs your attention right now.")).toBeInTheDocument();
    expect(screen.getByText("All seven plan artifacts are clear in the current read.")).toBeInTheDocument();
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
    expect(screen.getByRole("button", { name: "Take a quick tour" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Feedback" })).toBeVisible();
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

  it("creates a secure review route before moving an issue to Awaiting evidence", async () => {
    const fetcher = vi.fn().mockImplementation(async (request: RequestInfo | URL, init?: RequestInit) => {
      const url = String(request);
      if (url.endsWith("/collaboration") && init?.method === "POST") {
        return Response.json({ id: "review-grant-1", url: "http://localhost:3002/review/token" }, { status: 201 });
      }
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
        }, { status: 202 });
      }
      return Response.json({});
    });
    vi.stubGlobal("fetch", fetcher);

    render(
      <ProjectOverview displayName="Alex" initial={snapshot} logoutAction={vi.fn()} />,
    );
    fireEvent.click(screen.getByRole("button", { name: /Migration ownership is unresolved/i }));
    fireEvent.click(screen.getByRole("button", { name: /Ask for evidence/i }));
    fireEvent.click(screen.getByRole("button", { name: /Project collaborator/i }));

    await waitFor(() => expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/collaboration",
      expect.objectContaining({ method: "POST" }),
    ));
    const reviewCall = fetcher.mock.calls.find(
      ([url, init]) => String(url).endsWith("/collaboration") && init?.method === "POST",
    );
    expect(fetcher.mock.calls.some(([url, init]) => String(url).endsWith("/acts") && init?.method === "POST")).toBe(true);
    const reviewBody = JSON.parse(String(reviewCall?.[1]?.body));
    expect(reviewBody).toMatchObject({
      action: "review",
      issueId: "ISS-001",
      reviewerName: "Project collaborator",
    });
    expect(reviewCall).toBeDefined();
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

    await waitFor(() => expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/issues/ISS-001/acts",
      expect.objectContaining({ method: "POST" }),
    ));
    const actCall = fetcher.mock.calls.find(([url]) => String(url).endsWith("/acts"));
    expect(JSON.parse(String(actCall?.[1]?.body))).toMatchObject({
      act: "confirm",
      basis: "verified-directly",
      evidenceRef: "document:plan:page:1:fragment:0",
    });

    const issueDetail = screen.getByRole("region", { name: "Issue details" });
    const foldedProposal = screen
      .getAllByRole("region", { name: "OSLO proposes" })
      .find((region) => !issueDetail.contains(region))!;
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
    expect(screen.getByRole("button", { name: /Outcome: Move the Northstar platform/i })).toBeInTheDocument();

    const workspace = screen.getByRole("navigation", { name: "Workspace" });
    expect(within(workspace).getAllByRole("link").map((link) => link.textContent)).toEqual([
      expect.stringContaining("Issues"),
      expect.stringContaining("Your Outcome"),
      expect.stringContaining("Grounding map"),
      expect.stringContaining("Reports"),
      expect.stringContaining("History"),
    ]);

    const advisor = screen.getByRole("complementary", {
      name: "OSLO project advisor",
    });
    expect(within(advisor).getByText("On your read", { exact: false })).toBeInTheDocument();
    expect(within(advisor).getByText("Reasoning")).toBeInTheDocument();
    expect(within(advisor).getByText("Reliability basis")).toBeInTheDocument();
    expect(within(advisor).getByText(/Your next move/)).toBeInTheDocument();
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

  it("restores the Overview scroll position after returning from Attention Map", () => {
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
      "/projects/project-001/overview",
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

  it("exposes a clear account control and professional account navigation", () => {
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

    expect(within(navigation).getByText("Account & workspace")).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: "Settings" })).toHaveAttribute(
      "href",
      "/settings",
    );
    expect(within(navigation).getByRole("button", { name: "Log out" })).toBeInTheDocument();
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

  it("explains the deterministic maturity basis without another advisor call", () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByText("Why a maturity read, not a probability?"));

    expect(screen.getByText(snapshot.assessment.confidence_explanation)).toBeInTheDocument();
    expect(screen.getByText("Clarity")).toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher).toHaveBeenCalledWith("/api/workspace", { cache: "no-store" });
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

  it("restores the prototype advisor beside an inline issue when it was collapsed", () => {
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
    expect(screen.getByLabelText("OSLO project advisor")).toBeInTheDocument();
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
    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^Ask OSLO$/i })).toHaveClass(
      "advisor-floating",
    );
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
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /Cutover fallback is unresolved/i }),
      ).toBeInTheDocument(),
    );
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));

    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /Cutover fallback is unresolved/i }),
      ).toHaveFocus(),
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

    const confirmation = (await screen.findByText("Confirmed by you")).closest("section");
    expect(confirmation).not.toBeNull();
    expect(within(confirmation!).getByText("Confirm an accountable owner.")).toBeInTheDocument();
    expect(screen.getByLabelText("Issue status addressed")).toBeInTheDocument();
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

    await waitFor(() => {
      expect(screen.getByRole("region", { name: "Issue details" })).toHaveAttribute(
        "aria-describedby",
        "issue-analysis-pending-status",
      );
      expect(screen.getByLabelText("Issue status addressed")).toBeInTheDocument();
      expect(screen.getByText("Waiting for reanalysis")).toBeInTheDocument();
      expect(screen.getByText("Your read is safely out of date.")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Undo last change" })).toBeInTheDocument();
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
    const submit = screen.getByRole("button", { name: "Submit & re-analyze" });
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
      expect(screen.getByRole("region", { name: "Issue details" })).toHaveAttribute(
        "aria-describedby",
        "issue-analysis-pending-status",
      );
      expect(screen.getByText("Re-analyzing…")).toBeInTheDocument();
      expect(screen.getByText("Saved · Analysis pending")).toBeInTheDocument();
      expect(screen.getByLabelText("Issue status addressed")).toBeInTheDocument();
      expect(screen.getByText("Your read is safely out of date.")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Undo last change" })).toBeInTheDocument();
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

  it("replays and completes the six-step anchored orientation tour", async () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Take a quick tour" }));

    expect(screen.getByText("Step 1 of 6")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Your strategic read" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Back" })).not.toBeInTheDocument();
    for (let step = 1; step < 6; step += 1) {
      fireEvent.click(screen.getByRole("button", { name: "Next" }));
      expect(screen.getByText(`Step ${step + 1} of 6`)).toBeInTheDocument();
    }
    expect(screen.getByRole("heading", { name: "Ask OSLO anything" })).toBeInTheDocument();
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

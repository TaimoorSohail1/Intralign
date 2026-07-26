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

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
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
});

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("ProjectOverview", () => {
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

  it("opens a single-cell finding directly and a multi-cell scoped list before issue detail", () => {
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
    const scope = screen.getByRole("dialog", { name: "Scoped attention findings" });
    expect(scope).toHaveTextContent("Resources");
    expect(scope).toHaveTextContent("Feasibility");
    expect(scope).toHaveTextContent("Migration ownership is unresolved");
    expect(scope).toHaveTextContent("Fallback capacity is not confirmed");

    fireEvent.click(
      screen.getByRole("button", { name: /Migration ownership is unresolved/i }),
    );
    expect(screen.getByRole("dialog", { name: "Issue details" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));
    expect(
      screen.getByRole("dialog", { name: "Scoped attention findings" }),
    ).toBeInTheDocument();
  });

  it("supports row scoping, clearing one scope chip, and the natural all-clear state", () => {
    const { unmount } = render(
      <ProjectOverview
        displayName="Alex"
        initial={sliceFourSnapshot}
        initialView="attention"
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Open Resources findings" }));
    expect(
      screen.getByRole("dialog", { name: "Scoped attention findings" }),
    ).toHaveTextContent("2 findings");
    fireEvent.click(screen.getByRole("button", { name: "Clear Resources filter" }));
    expect(screen.queryByRole("dialog", { name: "Scoped attention findings" })).not.toBeInTheDocument();

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

  it("renders the golden Overview hierarchy and routes prototype entry points", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getAllByText("Confidence")).not.toHaveLength(0);
    expect(screen.getByRole("link", { name: "Timeline" })).toHaveAttribute(
      "href",
      "/projects/project-001/attention",
    );
    expect(screen.getByRole("button", { name: "Answer the first" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Project summary" })).toHaveAttribute(
      "aria-expanded",
      "false",
    );
    expect(screen.queryByText("Analysis status")).not.toBeInTheDocument();
  });

  it("restores the Overview scroll position after returning from Attention Map", () => {
    vi.useFakeTimers();
    const scrollTo = vi.spyOn(window, "scrollTo").mockImplementation(() => undefined);
    const requestAnimationFrame = vi
      .spyOn(window, "requestAnimationFrame")
      .mockImplementation((callback) => {
        callback(0);
        return 1;
      });
    const cancelAnimationFrame = vi
      .spyOn(window, "cancelAnimationFrame")
      .mockImplementation(() => undefined);
    Object.defineProperty(window, "scrollY", {
      configurable: true,
      value: 640,
    });

    const overview = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );
    const workspace = screen.getByRole("navigation", { name: "Workspace" });
    fireEvent.click(
      within(workspace).getByRole("link", { name: /Attention map/ }),
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
    scrollTo.mockRestore();
  });

  it("renders the Slice 3 project shell and evidence-qualified confidence read", () => {
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
    expect(screen.getByText("Expanded")).toBeInTheDocument();
    expect(screen.getByText("Strengthened")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "How confidence is calculated" })).toBeInTheDocument();
  });

  it("renders each understanding stage once when the current stage is orientation", () => {
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

    expect(screen.getAllByText("Orientation")).toHaveLength(1);
    expect(screen.getAllByText("Expanded")).toHaveLength(1);
    expect(screen.getAllByText("Validated")).toHaveLength(1);
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

  it("opens the prototype confidence breakdown from the toolbar", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", {
        name: "Confidence 52, Moderate, Moderate reliability",
      }),
    );

    expect(screen.getByRole("dialog", { name: "Confidence breakdown" })).toBeInTheDocument();
    expect(screen.getByText("Reliability basis")).toBeInTheDocument();
    expect(screen.getByText("Assessability")).toBeInTheDocument();
  });

  it("explains the deterministic confidence basis without another advisor call", () => {
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Why this confidence read" }));

    expect(screen.getByRole("region", { name: "Confidence calculation" })).toBeInTheDocument();
    expect(screen.getByText(snapshot.assessment.confidence_explanation)).toBeInTheDocument();
    expect(screen.getByText("Coverage")).toBeInTheDocument();
    expect(fetcher).not.toHaveBeenCalled();
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
      /supporting evidence is not yet reliable enough/i,
    );
  });

  it("closes the advisor for issue review and restores focus when the drawer closes", async () => {
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

    expect(screen.queryByLabelText("OSLO project advisor")).not.toBeInTheDocument();
    expect(screen.getByRole("dialog", { name: "Issue details" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Close issue" }));

    await waitFor(() => {
      expect(screen.getByLabelText("OSLO project advisor")).toBeInTheDocument();
      expect(issueButton).toHaveFocus();
    });
  });

  it("shows readable evidence in issue review and hides internal locator ids", () => {
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

    expect(screen.getByText("Migration plan.pdf")).toBeInTheDocument();
    expect(screen.getByText("Page 1")).toBeInTheDocument();
    expect(
      screen.getByText("The accountable migration owner has not been confirmed."),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("document:plan:page:1:fragment:0"),
    ).not.toBeInTheDocument();
  });

  it("saves a clarification once and immediately shows the addressed reanalysis state", async () => {
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
    fireEvent.change(screen.getByLabelText("Clarification answer"), {
      target: { value: "Priya owns migration; the legacy import is the fallback." },
    });
    const submit = screen.getByRole("button", { name: "Submit & re-analyze" });
    fireEvent.click(submit);
    fireEvent.click(submit);

    expect(fetcher).toHaveBeenCalledTimes(1);
    releaseResponse?.({
      ok: true,
      json: async () => ({ run_id: "run-clarification-001" }),
    });

    await waitFor(() => {
      expect(screen.getByRole("dialog", { name: "Issue details" })).toHaveAttribute(
        "aria-describedby",
        "issue-addressed-status",
      );
      expect(screen.getByText("Re-analyzing…")).toBeInTheDocument();
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

  it("keeps later-slice Issues and History destinations honest", () => {
    const { rerender } = render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        initialView="issues"
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByRole("heading", { name: "Issues" })).toBeInTheDocument();
    expect(screen.getByText(/full issues workspace arrives in Slice 6/i)).toBeInTheDocument();

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

  it("replays and completes the five-step orientation tour", async () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Take a quick tour" }));
    fireEvent.click(screen.getByRole("button", { name: "Get started" }));

    expect(screen.getByText("1 of 5")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Your confidence read" })).toBeInTheDocument();
    for (let step = 1; step < 5; step += 1) {
      fireEvent.click(screen.getByRole("button", { name: "Next" }));
      expect(screen.getByText(`${step + 1} of 5`)).toBeInTheDocument();
    }
    fireEvent.click(screen.getByRole("button", { name: "Finish tour" }));

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

    fireEvent.click(screen.getByRole("button", { name: "What should I address first?" }));

    expect(await screen.findByText(/Confirm the migration owner first/)).toBeInTheDocument();
    expect(fetcher).toHaveBeenCalledWith(
      "/api/projects/project-001/advisor",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ question: "What should I address first?" }),
      }),
    );
    expect(screen.getByRole("button", { name: "Who can approve the owner?" })).toBeInTheDocument();
  });

  it("creates one fresh project and navigates to its Intake page", async () => {
    const fetcher = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: "project-002" }),
    });
    vi.stubGlobal("fetch", fetcher);
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    const button = screen.getByRole("button", { name: "New project" });
    fireEvent.click(button);
    fireEvent.click(button);

    await waitFor(() => {
      expect(fetcher).toHaveBeenCalledTimes(1);
      expect(push).toHaveBeenCalledWith("/intake?project=project-002");
    });
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

    expect(screen.getByText("Extended Analysis paused safely")).toBeInTheDocument();
    expect(
      screen.getByText("The deeper read stopped before it could safely publish."),
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

  it("keeps the confirmed-dependency denominator stable after resolution", () => {
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

    expect(screen.getByText("Dependencies confirmed")).toBeInTheDocument();
    expect(screen.getByText("1 / 1")).toBeInTheDocument();
  });
});

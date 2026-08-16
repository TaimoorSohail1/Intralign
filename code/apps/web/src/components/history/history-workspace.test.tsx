import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ProjectHistory } from "@/lib/server/oslo-api";

import { HistoryWorkspace } from "./history-workspace";

const history: ProjectHistory = {
  project_id: "project-001",
  groups: [
    {
      run_id: "run-extended",
      kind: "extended",
      status: "completed",
      current: true,
      occurred_at: "2026-07-26T12:00:00Z",
      confidence_index: 62,
      confidence_band: "Moderate",
      confidence_direction: "strengthened",
      understanding_stage: "expanded",
      changes: [
        { label: "6 opened", tone: "neutral" },
        { label: "Feasibility Very Low → Low", tone: "positive" },
      ],
      events: [
        {
          id: 3,
          category: "collaboration",
          event_type: "collaboration.review_invited",
          summary: "Reviewer invited",
          detail: "Alex Morgan was invited to review a project issue.",
          actor_type: "user",
          artifact_type: null,
          artifact_version: null,
          issue_id: "issue-001",
          occurred_at: "2026-07-26T12:01:00Z",
        },
        {
          id: 2,
          category: "issues",
          event_type: "issues.reconciled",
          summary: "6 issues detected",
          detail: "6 opened and 0 resolved in this read.",
          actor_type: "system",
          artifact_type: null,
          artifact_version: null,
          issue_id: null,
          occurred_at: "2026-07-26T12:00:00Z",
        },
        {
          id: 1,
          category: "versions",
          event_type: "artifacts.versions_retained",
          summary: "7 plan-artifact versions retained (v1)",
          detail: "Intent · Context · Scope · Requirements · Work breakdown · Schedule · Resources",
          actor_type: "system",
          artifact_type: null,
          artifact_version: 1,
          issue_id: null,
          occurred_at: "2026-07-26T12:00:00Z",
        },
      ],
    },
    {
      run_id: "run-initial",
      kind: "initial",
      status: "completed",
      current: false,
      occurred_at: "2026-07-26T11:58:00Z",
      confidence_index: 58,
      confidence_band: "Moderate",
      confidence_direction: "unchanged",
      understanding_stage: "orientation",
      changes: [{ label: "First evidence-qualified read", tone: "neutral" }],
      events: [
        {
          id: 0,
          category: "analysis",
          event_type: "analysis.initial_completed",
          summary: "Initial Analysis complete",
          detail: "The first evidence-qualified read is available.",
          actor_type: "oslo",
          artifact_type: null,
          artifact_version: null,
          issue_id: null,
          occurred_at: "2026-07-26T11:58:00Z",
        },
      ],
    },
  ],
  trend: [
    {
      run_id: "run-initial",
      confidence_index: 58,
      confidence_band: "Moderate",
      direction: "unchanged",
      cause: "First evidence-qualified read",
      occurred_at: "2026-07-26T11:58:00Z",
      current: false,
    },
    {
      run_id: "run-extended",
      confidence_index: 62,
      confidence_band: "Moderate",
      direction: "strengthened",
      cause: "Feasibility Very Low → Low",
      occurred_at: "2026-07-26T12:00:00Z",
      current: true,
    },
  ],
  next_cursor: null,
};

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("HistoryWorkspace", () => {
  it("refreshes the visible timeline in place when a newer analysis version arrives", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: false })
      .mockResolvedValue({ ok: true, json: async () => history });
    vi.stubGlobal("fetch", fetchMock);
    const initialOnly: ProjectHistory = {
      ...history,
      groups: history.groups.filter((group) => group.kind === "initial"),
      trend: history.trend.filter((item) => item.run_id === "run-initial"),
    };
    const view = render(
      <HistoryWorkspace
        analysisRunId="run-initial"
        history={initialOnly}
        projectId="project-001"
      />,
    );

    expect(screen.queryByText("Extended Analysis complete")).not.toBeInTheDocument();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));

    view.rerender(
      <HistoryWorkspace
        analysisRunId="run-extended"
        history={history}
        projectId="project-001"
      />,
    );

    await waitFor(() =>
      expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument(),
    );
    view.unmount();
  });

  it("renders the append-only timeline, filters events, and opens a retained snapshot", async () => {
    const onAskOslo = vi.fn();
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          assessment: { confidence_index: 62, confidence_band: "Moderate" },
          artifacts: [{ artifact_type: "intent", title: "Intent", summary: "Run the event." }],
          summary: "A retained historical project read.",
        }),
      }),
    );

    render(
      <HistoryWorkspace
        history={history}
        onAskOslo={onAskOslo}
        projectId="project-001"
      />,
    );

    expect(screen.getByRole("heading", { name: "History" })).toBeInTheDocument();
    expect(screen.getByText("append-only — how the read moved")).toBeInTheDocument();
    expect(screen.getByText("Your read over this session")).toBeInTheDocument();
    expect(screen.getByText("Extended Analysis complete")).toBeInTheDocument();
    expect(screen.getAllByText("Initial Analysis complete")).not.toHaveLength(0);
    expect(screen.queryByRole("button", { name: /collapse extended/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Analysis" }));
    expect(screen.getByText(/7 plan-artifact versions retained/)).toBeInTheDocument();
    expect(screen.queryByText("6 issues detected")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Your decisions" }));
    expect(screen.getByText("Reviewer invited")).toBeInTheDocument();
    expect(screen.queryByText(/7 plan-artifact versions retained/)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Analysis" }));
    fireEvent.click(screen.getByRole("button", { name: /view snapshot/i }));
    await waitFor(() =>
      expect(screen.getByRole("dialog", { name: /historical snapshot/i })).toBeInTheDocument(),
    );
    expect(screen.getByText("A retained historical project read.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /close historical snapshot/i })).toHaveFocus();
    fireEvent.keyDown(document, { key: "Escape" });
    await waitFor(() =>
      expect(
        screen.queryByRole("dialog", { name: /historical snapshot/i }),
      ).not.toBeInTheDocument(),
    );

    expect(onAskOslo).not.toHaveBeenCalled();
  });
});

import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { ArtifactWorkspaceSummary } from "@/lib/server/oslo-api";

import { ArtifactWorkspace } from "./artifact-workspace";

const artifact: ArtifactWorkspaceSummary = {
  artifact_type: "schedule",
  title: "Schedule",
  content: {
    sections: [
      {
        heading: "Milestones",
        body: "The delivery baseline is not approved.",
        bullets: [],
        columns: ["Milestone", "Date", "Status"],
        rows: [
          ["Launch", "1 September", "At risk"],
          ["Steering review", "15 August", "Pending"],
        ],
      },
    ],
  },
  version: 1,
  provenance: "from_oslo",
  reliability: "Moderate",
  basis: "derived",
  evidence_refs: [],
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
  updated_at: "2026-07-25T10:00:00Z",
};

describe("ArtifactWorkspace", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(
          new Response(JSON.stringify(artifact), {
            status: 200,
            headers: { "content-type": "application/json" },
          }),
        )
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({
              ...artifact,
              version: 2,
              provenance: "confirmed_by_user",
              analysis_run: {
                run_id: "run-edit-001",
                project_id: "project-001",
                kind: "extended",
                status: "queued",
              },
            }),
            { status: 202, headers: { "content-type": "application/json" } },
          ),
        ),
    );
  });

  afterEach(() => {
    cleanup();
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("keeps edits local until the user explicitly applies them", async () => {
    const onAnalysisStarted = vi.fn();
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

    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });
    expect(screen.getByRole("heading", { name: "Schedule" })).toBeInTheDocument();
    expect(screen.getByText("Delivery baseline is unresolved")).toBeInTheDocument();
    expect(fetch).toHaveBeenNthCalledWith(
      1,
      "/api/projects/project-001/artifacts/schedule",
      { cache: "no-store" },
    );

    const paragraph = screen.getByText("The delivery baseline is not approved.");
    paragraph.textContent = "The schedule is approved by the steering committee.";
    fireEvent.input(paragraph);
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(1600);
      await Promise.resolve();
      await Promise.resolve();
    });
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(onAnalysisStarted).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole("button", { name: "Apply changes" }));
    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    expect(onAnalysisStarted).toHaveBeenCalledWith("run-edit-001");
    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it("supports keyboard row reordering", async () => {
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

    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    const rowGrips = screen.getAllByRole("button", {
      name: "Reorder row — use Up and Down arrow keys to move",
    });
    fireEvent.keyDown(rowGrips[0], { key: "ArrowDown" });

    const rows = screen.getAllByRole("row");
    expect(rows[1]).toHaveTextContent("Steering review");
    expect(rows[2]).toHaveTextContent("Launch");
  });

  it("does not save or start analysis when a delayed edit is undone back to the loaded content", async () => {
    const onAnalysisStarted = vi.fn();
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

    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    fireEvent.click(screen.getByRole("button", { name: "Add section" }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(5000);
      await Promise.resolve();
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(onAnalysisStarted).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Apply changes" })).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Undo" }));

    expect(screen.queryByRole("button", { name: "Apply changes" })).not.toBeInTheDocument();
    expect(screen.getByText("Up to date")).toBeInTheDocument();
  });

  it("keeps a heading-only section local until the user adds material content", async () => {
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

    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    fireEvent.click(screen.getByRole("button", { name: "Add section" }));
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1600);
      await Promise.resolve();
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(screen.getByText("Changes not applied")).toBeInTheDocument();
  });
});

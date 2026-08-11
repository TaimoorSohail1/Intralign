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
        provenance: "from_oslo",
        row_evidence_refs: [[], []],
        row_states: ["confirmed", "inferred"],
        row_provenance: ["from_oslo", "from_oslo"],
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
    expect(
      screen.getByLabelText("Provenance: Confirmed by you"),
    ).toHaveClass("artifact-block-provenance");

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

  it("shows an artifact issue callout once instead of repeating it in every section", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            ...artifact,
            content: {
              sections: [
                artifact.content.sections[0],
                {
                  ...artifact.content.sections[0],
                  heading: "Dependencies",
                  body: "The launch depends on supplier readiness.",
                },
              ],
            },
          }),
          { status: 200, headers: { "content-type": "application/json" } },
        ),
      ),
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

    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    expect(screen.getAllByText("Delivery baseline is unresolved")).toHaveLength(1);
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

  it("tracks exact row provenance through edit, undo, redo, and save", async () => {
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

    const rows = screen.getAllByRole("row");
    expect(
      rows[1].querySelector('[aria-label="Provenance: From OSLO"]'),
    ).toBeInTheDocument();
    expect(
      rows[2].querySelector('[aria-label="Provenance: From OSLO"]'),
    ).toBeInTheDocument();
    expect(
      rows[2].querySelector('[aria-label^="Inferred by OSLO"]'),
    ).toBeInTheDocument();

    const editedCell = screen.getByText("Pending");
    editedCell.textContent = "Approved";
    fireEvent.input(editedCell);

    expect(
      screen.getAllByRole("row")[1].querySelector(
        '[aria-label="Provenance: From OSLO"]',
      ),
    ).toBeInTheDocument();
    expect(
      screen.getAllByRole("row")[2].querySelector(
        '[aria-label="Provenance: Confirmed by you"]',
      ),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Undo" }));
    expect(
      screen.getAllByRole("row")[2].querySelector(
        '[aria-label="Provenance: From OSLO"]',
      ),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Redo" }));
    fireEvent.click(screen.getByRole("button", { name: "Apply changes" }));
    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });

    const saveCall = vi.mocked(fetch).mock.calls[1];
    const payload = JSON.parse(String(saveCall[1]?.body));
    expect(payload.content.sections[0].row_provenance).toEqual([
      "from_oslo",
      "confirmed_by_user",
    ]);
    expect(payload.content.sections[0].row_states).toEqual([
      "confirmed",
      "inferred",
    ]);
  });

  it("keeps the same editable cell focused across consecutive keystrokes", async () => {
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

    const cell = screen.getByText("Pending");
    cell.focus();
    cell.textContent = "Pending1";
    fireEvent.input(cell);

    expect(cell.isConnected).toBe(true);
    expect(cell).toHaveFocus();

    cell.textContent = "Pending12";
    fireEvent.input(cell);

    expect(cell.isConnected).toBe(true);
    expect(cell).toHaveFocus();
    expect(cell).toHaveTextContent("Pending12");
  });

  it("keeps the caret at the edit point after deleting the last character", async () => {
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

    const cell = screen.getByText("Pending");
    const textNode = cell.firstChild;
    expect(textNode).toBeInstanceOf(Text);

    const selection = window.getSelection();
    const range = document.createRange();
    range.setStart(textNode as Text, textNode?.textContent?.length ?? 0);
    range.collapse(true);
    selection?.removeAllRanges();
    selection?.addRange(range);

    (textNode as Text).deleteData(6, 1);
    range.setStart(textNode as Text, 6);
    range.collapse(true);
    fireEvent.input(cell, { inputType: "deleteContentBackward" });

    expect(cell).toHaveTextContent("Pendin");
    expect(selection?.anchorNode).toBe(textNode);
    expect(selection?.anchorOffset).toBe(6);
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

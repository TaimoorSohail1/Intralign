import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
        clarification: "Who owns migration?",
        status: "open",
      },
    ],
  },
  published_at: "2026-07-23T12:00:00Z",
};

beforeEach(() => {
  localStorage.setItem("oslo_orientation_seen", "true");
  push.mockReset();
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("ProjectOverview", () => {
  it("renders the golden Overview hierarchy and routes prototype entry points", () => {
    render(
      <ProjectOverview
        displayName="Alex"
        initial={snapshot}
        logoutAction={vi.fn()}
      />,
    );

    expect(screen.getByText("Confidence")).toBeInTheDocument();
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

  it("shows the real Extended failure and retries the failed run", async () => {
    const failedSnapshot: OverviewSnapshot = {
      ...snapshot,
      state: "provisional",
      extended_analysis: {
        run_id: "run-extended-001",
        project_id: "project-001",
        kind: "extended",
        status: "failed",
        phase: "perceive",
        completed_phases: [],
        error_code: "EVIDENCE_REFERENCE_CONTRACT_FAILED",
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
      screen.getByText("An evidence reference did not match the source document."),
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
});

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { OverviewSnapshot } from "@/lib/server/oslo-api";

import { ReportWorkspace } from "./report-workspace";

const snapshot: OverviewSnapshot = {
  snapshot_id: "snapshot-report",
  analysis_run_id: "run-report",
  project_id: "project-report",
  orientation_seen: true,
  state: "current",
  summary: "The launch plan has a clear goal but an unresolved delivery owner.",
  artifacts: [
    {
      artifact_type: "resources",
      title: "Resources",
      summary: "The delivery owner is not confirmed.",
      reliability: "Moderate",
      evidence_refs: ["document:plan:page:2:fragment:4"],
      basis: "The source lists responsibilities without naming an accountable owner.",
      assumptions: [
        {
          id: "ASM-OWNER",
          statement: "The delivery lead can approve the cutover.",
          state: "inferred",
          load_bearing: true,
          evidence_refs: ["document:plan:page:2:fragment:4"],
        },
      ],
    },
  ],
  assessment: {
    confidence_index: 58,
    confidence_band: "Moderate",
    reliability: "Moderate",
    clarity: "Moderate",
    alignment: "High",
    feasibility: "Low",
    understanding_stage: "expanded",
    reliability_basis: {
      coverage: "Moderate",
      evidence: "Moderate",
      assessability: "Moderate",
    },
    confidence_direction: "strengthened",
    limiting_dimension: "feasibility",
    false_confidence: false,
    confidence_explanation: "Feasibility is limited by missing ownership.",
    resolved_issue_count: 0,
    confirmed_dependency_count: 0,
    issues: [
      {
        id: "ISS-REPORT",
        artifact_type: "resources",
        dimension: "Feasibility",
        severity: "Critical",
        title: "Delivery ownership is unresolved",
        why: "No accountable owner is named.",
        recommendation: "Name an accountable owner and approval date.",
        evidence_refs: ["document:plan:page:2:fragment:4"],
        evidence: [],
        clarification: "Who owns delivery?",
        status: "open",
      },
    ],
  },
  published_at: "2026-07-27T12:00:00Z",
  source_document_count: 10,
};

beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((_url: string, init?: RequestInit) => {
      if (init?.method === "POST") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "delivery-1",
              status: "sent",
              scheduled_for: "2026-07-27T12:00:00Z",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (!init?.method || init.method === "GET") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              snapshot_id: snapshot.snapshot_id,
              content: null,
              deliveries: [],
            }),
            { status: 200, headers: { "content-type": "application/json" } },
          ),
        );
      }
      return Promise.resolve(
        new Response(JSON.stringify({ updated_at: "2026-07-27T12:01:00Z" }), {
          status: 200,
          headers: { "content-type": "application/json" },
        }),
      );
    }),
  );
});

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("ReportWorkspace", () => {
  it("renders all seven report sections in one continuous editable document", () => {
    render(<ReportWorkspace snapshot={snapshot} />);

    expect(screen.getByRole("heading", { name: "Project understanding" })).toBeInTheDocument();
    expect(screen.getAllByRole("textbox")).toHaveLength(1);
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "The launch plan has a clear goal",
    );
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "Delivery ownership is unresolved",
    );
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "10 source documents",
    );
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "The delivery lead can approve the cutover",
    );
    expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(7);
  });

  it("supports section navigation, audience-specific asks, and real send feedback", async () => {
    render(<ReportWorkspace snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("button", { name: /Sections/i }));
    expect(screen.getByRole("menuitem", { name: /Decisions needed/i })).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Report recipient"), {
      target: { value: "Steering group" },
    });
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "Please resolve the highest-impact open decision",
    );
    fireEvent.click(screen.getByRole("button", { name: /Send/i }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "sponsor@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send now" }));
    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent(
        "Report emailed to sponsor@example.com.",
      );
    });
    expect(fetch).toHaveBeenCalledWith(
      `/api/projects/${snapshot.project_id}/report`,
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("autosaves sanitized document edits without running analysis", () => {
    vi.useFakeTimers();
    render(<ReportWorkspace snapshot={snapshot} />);

    const editor = screen.getByRole("textbox", { name: "Edit readout" });
    editor.innerHTML = `${editor.innerHTML}<script>alert('no')</script><p onclick="bad()">Owner confirmed.</p>`;
    fireEvent.input(editor);
    vi.advanceTimersByTime(500);

    const saved = localStorage.getItem(
      `oslo:readout:${snapshot.project_id}:${snapshot.snapshot_id}`,
    );
    expect(saved).toContain("Owner confirmed.");
    expect(saved).not.toContain("<script");
    expect(saved).not.toContain("onclick");
    expect(fetch).toHaveBeenCalledWith(
      `/api/projects/${snapshot.project_id}/report`,
      expect.objectContaining({ method: "PUT" }),
    );
    expect(fetch).not.toHaveBeenCalledWith(
      expect.stringContaining("analysis-runs"),
      expect.anything(),
    );
  });

  it("hydrates device drafts after mount without changing the server render", async () => {
    localStorage.setItem(
      `oslo:readout:${snapshot.project_id}:${snapshot.snapshot_id}`,
      '<section class="report-editable-section" data-section="summary">' +
        '<h2>Summary</h2><div class="report-section-body">' +
        "<p>Device draft restored safely.</p></div></section>",
    );

    render(<ReportWorkspace snapshot={snapshot} />);

    expect(
      await screen.findByText("Device draft restored safely."),
    ).toBeInTheDocument();
  });

  it("accepts a native date-time input and schedules durable delivery", async () => {
    render(<ReportWorkspace snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("button", { name: "Schedule" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "scheduled@example.com" },
    });
    fireEvent.input(screen.getByLabelText("Delivery time"), {
      target: { value: "2026-07-28T13:00" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Schedule delivery" }));

    await waitFor(() => {
      const scheduledFor = new Date("2026-07-28T13:00").toISOString();
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report`,
        expect.objectContaining({
          method: "POST",
          body: expect.stringContaining(`"scheduled_for":"${scheduledFor}"`),
        }),
      );
    });
  });

  it("does not claim an email was sent when the mail service failed", async () => {
    vi.mocked(fetch).mockImplementation(
      (_url: string | URL | Request, init?: RequestInit) => {
      if (init?.method === "POST") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "delivery-failed",
              status: "failed",
              scheduled_for: "2026-07-27T12:00:00Z",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      return Promise.resolve(
        new Response(
          JSON.stringify({
            snapshot_id: snapshot.snapshot_id,
            content: null,
            deliveries: [],
          }),
          { status: 200, headers: { "content-type": "application/json" } },
        ),
      );
      },
    );
    render(<ReportWorkspace snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("button", { name: /Send/i }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "sponsor@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send now" }));

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("email delivery failed");
    });
    expect(screen.getByRole("status")).not.toHaveTextContent("Report emailed");
  });
});

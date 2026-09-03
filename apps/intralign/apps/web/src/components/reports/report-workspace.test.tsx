import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { OverviewSnapshot, ProjectHistory } from "@/lib/server/oslo-api";

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
    integrity: {
      level: "Fragile",
      limiting_pillar: "Viability",
      decomposition: [
        { key: "Viability", band: "Fragile", basis: 0, why: [] },
        { key: "Grounding", band: "Fragile", basis: 0, why: [] },
        { key: "Adaptability", band: "Fragile", basis: 0, why: [] },
      ],
      posture: "moment-in-time",
      tracking: "pending-execution",
    },
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
      const url = String(_url);
      if (url.endsWith("/report/asana") && init?.method === "POST") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "handoff-1",
              state: "completed",
              total_count: 1,
              completed_count: 1,
              safe_error_code: null,
              destination_gid: "asana-project-1",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/asana") && (!init?.method || init.method === "GET")) {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              configured: false,
              entitled: false,
              destination_gid: null,
              snapshot_id: snapshot.snapshot_id,
              preview: [],
              latest: null,
            }),
            { status: 200, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/schedules") && init?.method === "POST") {
        const body = JSON.parse(String(init.body));
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "schedule-1",
              recipient_email: body.recipient_email,
              recipient_class: body.recipient_class,
              weekday: body.weekday,
              local_time: body.local_time,
              timezone: body.timezone,
              state: "enabled",
              next_run_at: "2026-07-28T13:00:00Z",
              last_run_at: null,
              last_delivery_id: null,
              created_at: "2026-07-27T12:00:00Z",
              updated_at: "2026-07-27T12:00:00Z",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/schedules") && (!init?.method || init.method === "GET")) {
        return Promise.resolve(
          new Response(JSON.stringify([]), {
            status: 200,
            headers: { "content-type": "application/json" },
          }),
        );
      }
      if (url.includes("/report/schedules/") && init?.method === "PATCH") {
        const state = JSON.parse(String(init.body)).state;
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "schedule-1",
              recipient_email: "scheduled@example.com",
              recipient_class: "exec-sponsor",
              weekday: 4,
              local_time: "13:00:00",
              timezone: "Asia/Karachi",
              state,
              next_run_at: "2026-07-28T13:00:00Z",
              last_run_at: null,
              last_delivery_id: null,
              created_at: "2026-07-27T12:00:00Z",
              updated_at: "2026-07-27T12:01:00Z",
            }),
            { status: 200, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.includes("/report/schedules/") && init?.method === "DELETE") {
        return Promise.resolve(new Response(null, { status: 204 }));
      }
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
  Reflect.deleteProperty(navigator, "clipboard");
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

function renderAuthored(snapshotValue: OverviewSnapshot = snapshot) {
  const result = render(<ReportWorkspace snapshot={snapshotValue} />);
  fireEvent.click(screen.getByRole("button", { name: /Generate a draft/i }));
  return result;
}

describe("ReportWorkspace", () => {
  it("matches the prototype report entry hierarchy and keeps dismissal durable", async () => {
    const first = render(<ReportWorkspace snapshot={snapshot} />);
    expect(screen.getByLabelText("Reports location")).toHaveTextContent("OutcomeReports");
    expect(screen.getByRole("region", { name: "Reports welcome" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Reports" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Take a 30-second tour →" }));
    expect(screen.getByRole("status")).toHaveTextContent("Start with Executive Briefing");

    fireEvent.click(screen.getByRole("button", { name: "Dismiss reports welcome" }));
    expect(screen.queryByRole("region", { name: "Reports welcome" })).not.toBeInTheDocument();
    first.unmount();
    render(<ReportWorkspace snapshot={snapshot} />);
    await waitFor(() => {
      expect(screen.queryByRole("region", { name: "Reports welcome" })).not.toBeInTheDocument();
    });
  });

  it("persists a newly generated draft with its audience, depth and sections", async () => {
    render(<ReportWorkspace snapshot={snapshot} />);
    fireEvent.click(screen.getByRole("button", { name: "Team" }));
    fireEvent.click(screen.getByRole("button", { name: "Summary" }));
    fireEvent.click(screen.getByRole("button", { name: "Top risks" }));
    fireEvent.click(screen.getByRole("button", { name: /Generate a draft/i }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report`,
        expect.objectContaining({
          method: "PUT",
          body: expect.stringContaining('"recipient_class":"team"'),
        }),
      );
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report`,
        expect.objectContaining({
          body: expect.stringContaining('"composition_depth":"summary"'),
        }),
      );
    });
  });

  it("presents the four Slice 7 authored and generated reports", () => {
    renderAuthored();

    expect(screen.getByRole("tablist", { name: "Reports" })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /Authored Executive Briefing/i })).toHaveAttribute(
      "aria-selected",
      "true",
    );
    expect(screen.getByRole("tab", { name: /Generated Outcome Readiness/i })).toBeInTheDocument();
    expect(
      screen.getByRole("tab", { name: /Generated Assumptions & Evidence/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: /Generated Decision Record/i })).toBeInTheDocument();
  });

  it("keeps the prototype memo, copy and regenerate actions at the end of the authored report", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Copy" }));
    await waitFor(() => expect(writeText).toHaveBeenCalled());
    expect(screen.getByRole("status")).toHaveTextContent("Report copied to the clipboard");

    fireEvent.click(screen.getByRole("button", { name: "Regenerate from the read" }));
    expect(screen.getByRole("status")).toHaveTextContent(/Draft (generated|regenerated)/);

    fireEvent.click(screen.getByRole("button", { name: "Send as a memo" }));
    expect(screen.getByRole("dialog", { name: "Send readout" })).toBeInTheDocument();
  });

  it("renders Outcome Readiness from the retained analysis without an editor", () => {
    render(<ReportWorkspace snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("tab", { name: /Generated Outcome Readiness/i }));

    expect(
      screen.getByRole("heading", { name: /Outcome Readiness · read-only snapshot/i }),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Fragile", { selector: "strong" })).not.toHaveLength(0);
    expect(screen.getByText(/0 of 1 critical details grounded/i)).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Delivery ownership is unresolved", level: 2 }),
    ).toBeInTheDocument();
    expect(screen.getByText(/27 Jul 2026/i)).toBeInTheDocument();
    expect(screen.queryByRole("textbox", { name: "Edit readout" })).not.toBeInTheDocument();
  });

  it("supports Summary and Full depth in the generated evidence register", () => {
    const withEvidence: OverviewSnapshot = {
      ...snapshot,
      provenance: {
        schema_version: 1,
        artifacts: [],
        assumptions: Array.from({ length: 6 }, (_, index) => ({
          id: `ASM-${index + 1}`,
          artifact_type: "resources",
          text: `Evidence detail ${index + 1}`,
          issue_id: null,
          issue_title: null,
          load_bearing: index < 2,
          state: index === 0 ? "confirmed" : "inferred",
        })),
        grounded_claims: 1,
        inferred_claims: 5,
        total_claims: 6,
        load_bearing_inferences: 1,
        grounding: {
          grounded: 1,
          addressed: 1,
          routed: 0,
          inferred: 2,
          total: 4,
          basis: 0.25,
          band: "Weak",
        },
        structure: {
          unconfirmed_dependencies: 0,
          unowned_parties: 1,
          untraceable_numbers: 0,
        },
        this_week: { user_grounded: 1, oslo_inferred: 5 },
      },
    };
    render(<ReportWorkspace snapshot={withEvidence} />);

    fireEvent.click(screen.getByRole("tab", { name: /Generated Assumptions & Evidence/i }));

    expect(
      screen.getByRole("heading", { name: /Assumptions & Evidence · read-only snapshot/i }),
    ).toBeInTheDocument();
    const groundingSummary = screen.getByText(
      (_content, element) => element?.classList.contains("generated-report-intro") ?? false,
    );
    expect(groundingSummary).toHaveTextContent(/1 of 4 load-bearing details rest on your evidence/i);
    expect(groundingSummary).toHaveTextContent(/3 remain ungrounded/i);
    expect(screen.getByRole("button", { name: "Summary" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.queryByText("Evidence detail 6")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Full" }));

    expect(screen.getByText("Evidence detail 6")).toBeInTheDocument();
    expect(screen.queryByRole("textbox", { name: "Edit readout" })).not.toBeInTheDocument();
  });

  it("shows visible feedback when a generated report is exported", () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:generated-report"),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => undefined);
    renderAuthored();
    fireEvent.click(screen.getByRole("tab", { name: /Generated Outcome Readiness/i }));

    expect(screen.getAllByText("Fragile", { selector: "strong" })).not.toHaveLength(0);
    expect(screen.getByText(/firms as you confirm more/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Export this report" }));

    expect(screen.getByRole("status")).toHaveTextContent("TEXT export downloaded");
  });

  it("attributes retained decisions and keeps open decisions separate", () => {
    const history: ProjectHistory = {
      project_id: snapshot.project_id,
      next_cursor: null,
      trend: [],
      groups: [
        {
          run_id: snapshot.analysis_run_id,
          kind: "extended",
          status: "completed",
          current: true,
          occurred_at: snapshot.published_at,
          confidence_index: 58,
          confidence_band: "Moderate",
          confidence_direction: "strengthened",
          understanding_stage: "expanded",
          changes: [],
          events: [
            {
              id: 17,
              category: "decisions",
              event_type: "issue_resolution_confirmed",
              summary: "Delivery lead appointed",
              detail: "The project owner confirmed the accountable lead.",
              actor_type: "user",
              artifact_type: "resources",
              artifact_version: 3,
              issue_id: "ISS-OLD",
              occurred_at: "2026-07-26T10:00:00Z",
            },
          ],
        },
      ],
    };
    render(<ReportWorkspace history={history} snapshot={snapshot} />);

    fireEvent.click(screen.getByRole("tab", { name: /Generated Decision Record/i }));

    expect(
      screen.getByRole("heading", { name: /Decision Record · read-only snapshot/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Delivery lead appointed" })).toBeInTheDocument();
    expect(screen.getByText(/You · 26 Jul 2026/i)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Who owns delivery?" })).toBeInTheDocument();
  });

  it("starts Executive Briefing in the prototype compose state and generates an authored draft", () => {
    render(<ReportWorkspace snapshot={snapshot} />);

    expect(screen.getByText(/the note that goes out/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /1 Generate/i })).toHaveAttribute(
      "aria-current",
      "step",
    );
    expect(screen.getByRole("button", { name: "Exec sponsor" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByRole("button", { name: "Full" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: "Integrity" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.queryByRole("textbox", { name: "Edit readout" })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /Generate a draft/i }));

    expect(screen.getByRole("textbox", { name: "Edit readout" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /2 Author/i })).toHaveAttribute(
      "aria-current",
      "step",
    );
  });

  it("renders all seven report sections in one continuous editable document", () => {
    renderAuthored();

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

  it("does not repeat equivalent assumptions or recommendations", () => {
    const repeated: OverviewSnapshot = {
      ...snapshot,
      artifacts: [
        snapshot.artifacts[0],
        {
          ...snapshot.artifacts[0],
          artifact_type: "schedule",
        },
      ],
      assessment: {
        ...snapshot.assessment,
        issues: [
          snapshot.assessment.issues[0],
          {
            ...snapshot.assessment.issues[0],
            id: "ISS-REPORT-DUPLICATE",
            artifact_type: "schedule",
          },
        ],
      },
    };

    renderAuthored(repeated);

    const report = screen.getByRole("textbox", { name: "Edit readout" }).textContent ?? "";
    expect(report.match(/The delivery lead can approve the cutover/g)).toHaveLength(1);
    expect(report.match(/Recommended: Name an accountable owner and approval date/g)).toHaveLength(1);
  });

  it("inserts a paragraph without creating an extra report heading", () => {
    const { container } = renderAuthored();
    const editor = screen.getByRole("textbox", { name: "Edit readout" });
    const summaryBody = editor.querySelector(
      '[data-section="summary"] .report-section-body',
    );
    const paragraphsBefore = summaryBody?.querySelectorAll(":scope > p").length;

    fireEvent.click(screen.getByRole("button", { name: "Insert paragraph" }));

    expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(7);
    expect(summaryBody?.querySelectorAll(":scope > p")).toHaveLength(
      (paragraphsBefore ?? 0) + 1,
    );
    expect(
      container.querySelector('[data-section="summary"] .report-section-body > p:last-child br'),
    ).toBeInTheDocument();
  });

  it("supports section navigation, audience-specific asks, and real send feedback", async () => {
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: /Sections/i }));
    expect(screen.getByRole("menuitem", { name: /Decisions needed/i })).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Report recipient"), {
      target: { value: "Board" },
    });
    expect(screen.getByRole("textbox", { name: "Edit readout" })).toHaveTextContent(
      "Please resolve the highest-impact open decision",
    );
    fireEvent.click(screen.getByRole("button", { name: /^Send$/i }));
    expect(screen.getByRole("dialog", { name: "Send readout" })).toHaveTextContent(
      "Goes to Board as a read-only copy",
    );
    fireEvent.click(screen.getByRole("button", { name: "Change recipient" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "sponsor@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send to the board" }));
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

  it("requires an explicit delivery address instead of pre-filling a plausible recipient", () => {
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: /^Send$/i }));

    expect(screen.getByRole("textbox", { name: "Recipient email" })).toHaveValue("");
    expect(
      screen.getByRole("button", { name: "Send to the exec sponsor" }),
    ).toBeDisabled();
  });

  it("shows friendly validation and does not call delivery for an invalid email", () => {
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: /^Send$/i }));
    fireEvent.click(screen.getByRole("button", { name: "Change recipient" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "not-an-email" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send to the exec sponsor" }));

    expect(screen.getByRole("status")).toHaveTextContent(
      "Enter a valid recipient email address.",
    );
    expect(fetch).not.toHaveBeenCalledWith(
      `/api/projects/${snapshot.project_id}/report`,
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("autosaves sanitized document edits without running analysis", () => {
    vi.useFakeTimers();
    renderAuthored();

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

  it("persists the current document before starting a PDF export", async () => {
    const click = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => undefined);
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Export" }));
    expect(screen.getByRole("dialog", { name: "Export your plan" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Export as PDF" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report`,
        expect.objectContaining({ method: "PUT", keepalive: true }),
      );
      expect(click).toHaveBeenCalledOnce();
    });
  });

  it("offers the real Slice 7 export formats and the Asana Basic fallback", () => {
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Export" }));

    const dialog = screen.getByRole("dialog", { name: "Export your plan" });
    expect(dialog).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Excel" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "CSV" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Text" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "PDF package" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Copy summary" })).toBeInTheDocument();
    expect(screen.getByText(/Asana/i)).toBeInTheDocument();
    expect(screen.getByText(/Basic/i)).toBeInTheDocument();
  });

  it("labels the export with executable plan tasks instead of open issues", async () => {
    vi.mocked(fetch).mockImplementation((_url: string | URL | Request) => {
      const url = String(_url);
      if (url.endsWith("/report/asana")) {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              configured: false,
              entitled: false,
              destination_gid: null,
              snapshot_id: snapshot.snapshot_id,
              preview: [
                { item_key: "task-1", task: "Confirm launch", owner: null, start_on: null, due_on: null, source_date: null, provenance: "document:plan:page:3" },
                { item_key: "task-2", task: "Publish launch", owner: null, start_on: null, due_on: null, source_date: null, provenance: "document:plan:page:4" },
              ],
              latest: null,
            }),
            { status: 200, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/schedules")) {
        return Promise.resolve(new Response(JSON.stringify([]), { status: 200 }));
      }
      return Promise.resolve(new Response(JSON.stringify({ content: null }), { status: 200 }));
    });
    renderAuthored();

    await waitFor(() => expect(fetch).toHaveBeenCalledWith(
      `/api/projects/${snapshot.project_id}/report/asana`,
      expect.objectContaining({ cache: "no-store" }),
    ));
    fireEvent.click(screen.getByRole("button", { name: "Export" }));

    const dialog = screen.getByRole("dialog", { name: "Export your plan" });
    expect(within(dialog).getByText(/2 tasks/)).toBeInTheDocument();
    expect(within(dialog).queryByText(/open tasks/)).not.toBeInTheDocument();
  });

  it("portals the export dialog to the viewport and closes it with Escape", () => {
    renderAuthored();
    fireEvent.click(screen.getByRole("button", { name: "Export" }));
    const dialog = screen.getByRole("dialog", { name: "Export your plan" });
    expect(dialog.parentElement?.parentElement).toBe(document.body);

    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog", { name: "Export your plan" })).not.toBeInTheDocument();
  });

  it("copies the current summary and records the export", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Export" }));
    fireEvent.click(screen.getByRole("button", { name: "Copy summary" }));

    await waitFor(() => {
      expect(writeText).toHaveBeenCalledWith(snapshot.summary);
      expect(screen.getByRole("status")).toHaveTextContent("Summary copied");
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report/exports`,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ format: "copy-summary" }),
        }),
      );
    });
  });

  it("imports the executable preview through a configured Basic Asana hand-off", async () => {
    vi.mocked(fetch).mockImplementation((_url: string | URL | Request, init?: RequestInit) => {
      const url = String(_url);
      if (url.endsWith("/report/asana") && init?.method === "POST") {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: "handoff-1",
              state: "completed",
              total_count: 1,
              completed_count: 1,
              safe_error_code: null,
              destination_gid: "asana-project-1",
            }),
            { status: 201, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/asana")) {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              configured: true,
              entitled: true,
              destination_gid: "asana-project-1",
              snapshot_id: snapshot.snapshot_id,
              preview: [
                {
                  item_key: "item-1",
                  task: "Confirm launch",
                  owner: "Maya",
                  start_on: null,
                  due_on: null,
                  source_date: null,
                  provenance: "document:plan:page:3",
                },
              ],
              latest: null,
            }),
            { status: 200, headers: { "content-type": "application/json" } },
          ),
        );
      }
      if (url.endsWith("/report/schedules")) {
        return Promise.resolve(new Response(JSON.stringify([]), { status: 200 }));
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
      return Promise.resolve(new Response("{}", { status: 200 }));
    });
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Export" }));
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Import 1 tasks →" })).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole("button", { name: "Import 1 tasks →" }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report/asana`,
        { method: "POST" },
      );
      expect(screen.getByRole("status")).toHaveTextContent(
        "1 executable plan items imported to Asana",
      );
    });
  });

  it("downloads a real CSV payload from the retained plan", () => {
    let downloadedAs = "";
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:plan-export"),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(function () {
      downloadedAs = this.download;
    });
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Export" }));
    fireEvent.click(screen.getByRole("button", { name: "CSV" }));
    fireEvent.click(screen.getByRole("button", { name: "Download the CSV" }));

    expect(URL.createObjectURL).toHaveBeenCalledOnce();
    expect(downloadedAs).toMatch(/Atlas launch-plan\.csv$|Project understanding-plan\.csv$/);
    expect(screen.getByRole("status")).toHaveTextContent("CSV export downloaded");
  });

  it("hydrates device drafts after mount without changing the server render", async () => {
    localStorage.setItem(
      `oslo:readout:${snapshot.project_id}:${snapshot.snapshot_id}`,
      '<section class="report-editable-section" data-section="summary">' +
        '<h2>Summary</h2><div class="report-section-body">' +
        "<p>Device draft restored safely.</p></div></section>",
    );

    render(<ReportWorkspace snapshot={snapshot} />);

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /2 Author/i })).toHaveAttribute(
        "aria-current",
        "step",
      );
      expect(screen.getByText("Device draft restored safely.")).toBeInTheDocument();
    });
  });

  it("creates a timezone-aware weekly schedule through the Basic contract", async () => {
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: "Schedule" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "scheduled@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Day"), {
      target: { value: "4" },
    });
    fireEvent.change(screen.getByLabelText("Local time"), {
      target: { value: "13:00" },
    });
    fireEvent.change(screen.getByLabelText("Timezone"), {
      target: { value: "Asia/Karachi" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Schedule weekly · Basic/i }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `/api/projects/${snapshot.project_id}/report/schedules`,
        expect.objectContaining({
          method: "POST",
          body: expect.stringContaining('"timezone":"Asia/Karachi"'),
        }),
      );
      expect(screen.getByRole("status")).toHaveTextContent("Weekly delivery scheduled");
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Pause weekly schedule for scheduled@example.com",
      }),
    );
    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("Weekly delivery paused");
      expect(
        screen.getByRole("button", {
          name: "Resume weekly schedule for scheduled@example.com",
        }),
      ).toBeInTheDocument();
    });

    fireEvent.click(
      screen.getByRole("button", {
        name: "Remove weekly schedule for scheduled@example.com",
      }),
    );
    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("Weekly delivery removed");
      expect(
        screen.queryByRole("button", {
          name: "Pause weekly schedule for scheduled@example.com",
        }),
      ).not.toBeInTheDocument();
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
    renderAuthored();

    fireEvent.click(screen.getByRole("button", { name: /^Send$/i }));
    fireEvent.click(screen.getByRole("button", { name: "Change recipient" }));
    fireEvent.change(screen.getByRole("textbox", { name: "Recipient email" }), {
      target: { value: "sponsor@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send to the exec sponsor" }));

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("email delivery failed");
    });
    expect(screen.getByRole("status")).not.toHaveTextContent("Report emailed");
  });

  it("labels a previous-analysis report and blocks external sending until refresh", async () => {
    vi.mocked(fetch).mockImplementation(
      (_url: string | URL | Request, init?: RequestInit) => {
        if (init?.method === "POST") {
          return Promise.resolve(
            new Response(
              JSON.stringify({
                id: "delivery-previous",
                status: "sent",
                currency_state: "previous_analysis",
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
                snapshot_id: "snapshot-newer",
                content: null,
                deliveries: [],
              }),
              { status: 200, headers: { "content-type": "application/json" } },
            ),
          );
        }
        return Promise.resolve(
          new Response(JSON.stringify({ message: "The report is from a previous analysis." }), {
            status: 409,
            headers: { "content-type": "application/json" },
          }),
        );
      },
    );
    renderAuthored();

    expect(await screen.findByText("Previous analysis")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /^Send$/i }));
    expect(screen.getByRole("status")).toHaveTextContent(
      "Refresh the report from the current analysis before sending or scheduling it.",
    );
    expect(fetch).not.toHaveBeenCalledWith(
      `/api/projects/${snapshot.project_id}/report`,
      expect.objectContaining({ method: "POST" }),
    );

    expect(
      screen.queryByRole("checkbox", {
        name: "I understand this report is based on a previous analysis",
      }),
    ).not.toBeInTheDocument();
  });
});

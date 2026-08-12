import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { AnalysisProgress } from "./analysis-progress";

const replace = vi.fn();
const router = { replace };

vi.mock("next/navigation", () => ({
  useRouter: () => router,
}));

class FakeEventSource {
  static current: FakeEventSource | null = null;
  private listeners = new Map<string, Array<(event: MessageEvent) => void>>();

  constructor() {
    FakeEventSource.current = this;
  }

  addEventListener(type: string, listener: (event: MessageEvent) => void) {
    this.listeners.set(type, [...(this.listeners.get(type) ?? []), listener]);
  }

  emit(type: string, payload: object) {
    const event = new MessageEvent(type, { data: JSON.stringify(payload) });
    this.listeners.get(type)?.forEach((listener) => listener(event));
  }

  close() {}
}

function frame() {
  return screen.getByTitle("OSLO analysis and outcome confirmation") as HTMLIFrameElement;
}

function emitArcMessage(data: object, options?: { origin?: string; source?: MessageEventSource | null }) {
  window.dispatchEvent(
    new MessageEvent("message", {
      data,
      origin: options?.origin ?? window.location.origin,
      source: options?.source === undefined ? frame().contentWindow : options.source,
    }),
  );
}

function completedOverview() {
  return {
    project_title: "Migration",
    summary: "Ship the migration without customer interruption.",
    artifacts: [
      {
        artifact_type: "intent",
        summary: "Ship the migration without customer interruption.",
        content: { sections: [] },
      },
    ],
    assessment: { integrity: { decomposition: [] } },
  };
}

describe("AnalysisProgress", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource);
    replace.mockReset();
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("reconnects to the running analysis without reloading the failed page", async () => {
    let statusRequest = 0;
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") return new Response("{}", { status: 202 });
      statusRequest += 1;
      return Response.json(
        statusRequest === 1
          ? {
              status: "failed",
              phase: "construct_artifacts",
              completed_phases: ["perceive"],
              error_code: "OPENAI_TIMEOUT",
            }
          : {
              status: "running",
              phase: "construct_artifacts",
              completed_phases: ["perceive"],
            },
      );
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    await screen.findByRole("button", { name: "Retry analysis" });

    fireEvent.click(screen.getByRole("button", { name: "Retry analysis" }));

    await waitFor(() => expect(statusRequest).toBe(2));
    expect(screen.getByRole("status")).toHaveTextContent("Drafting your plan documents…");
    expect(frame()).toHaveAttribute("src", "/r2/onboarding-arc.html?embed=1&live=1&mode=guided");
  });

  it("uses the exact prototype arc and sends truthful live analysis progress into it", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({
          status: "running",
          phase: "construct_artifacts",
          completed_phases: ["ingest_parse", "retrieve_evidence"],
        }),
      ),
    );

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    const arc = frame();
    const postMessage = vi.spyOn(arc.contentWindow!, "postMessage");
    emitArcMessage({ oarc: "ready" });

    await waitFor(() => expect(postMessage).toHaveBeenCalled());
    expect(arc).toHaveAttribute("data-oarc-complete", "false");
    expect(postMessage).toHaveBeenCalledWith(
      expect.objectContaining({
        oarc: "sync",
        events: expect.arrayContaining(["plan-structure", "inference"]),
        complete: false,
      }),
      window.location.origin,
    );
    expect(screen.getByRole("status")).toHaveTextContent(
      "Drafting your plan documents… Stage 5 of 8. 2 analysis steps complete.",
    );

    FakeEventSource.current?.emit("analysis.artifact_completed", { artifact_type: "intent" });
    expect(screen.getByRole("status")).toHaveTextContent("2 analysis steps complete");
  });

  it("mirrors completed live state onto the same-origin frame for race-free synchronization", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) =>
        String(input).includes("/overview")
          ? Response.json(completedOverview())
          : Response.json({
              status: "completed",
              phase: "publish",
              completed_phases: ["publish"],
            }),
      ),
    );

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);

    await waitFor(() => expect(frame()).toHaveAttribute("data-oarc-complete", "true"));
    expect(frame()).toHaveAttribute(
      "data-oarc-outcome",
      "Ship the migration without customer interruption.",
    );
    expect(frame()).toHaveAttribute("data-oarc-events", expect.stringContaining("outcome"));
  });

  it("synchronizes after the embedded document loads even if its ready handshake raced", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) =>
        String(input).includes("/overview")
          ? Response.json(completedOverview())
          : Response.json({
              status: "completed",
              phase: "publish",
              completed_phases: ["publish"],
            }),
      ),
    );

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    const arc = frame();
    const postMessage = vi.spyOn(arc.contentWindow!, "postMessage");

    fireEvent.load(arc);
    await waitFor(() => expect(postMessage).toHaveBeenCalled());
  });

  it.each([
    ["confirm", null, "Ship the migration without customer interruption."],
    ["refine", "Ship safely in my words", "Ship safely in my words"],
    ["defer", null, "Ship the migration without customer interruption."],
  ] as const)("persists the prototype %s outcome decision before navigating", async (action, text, expectedOutcome) => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/outcome-actions") && init?.method === "POST") {
        return Response.json({ action, outcome: expectedOutcome, analysis_run: null });
      }
      if (url.includes("/overview")) return Response.json(completedOverview());
      return Response.json({
        status: "completed",
        phase: "publish",
        completed_phases: ["publish"],
        pass_kind: "fast",
      });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    expect(await screen.findByRole("status")).toHaveTextContent("Analysis complete");
    expect(replace).not.toHaveBeenCalled();
    const postMessage = vi.spyOn(frame().contentWindow!, "postMessage");

    emitArcMessage({ oarc: "decision", action, text });

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/projects/project-1/outcome-actions",
        expect.objectContaining({
          method: "POST",
          body: expect.stringContaining(`\"outcome\":\"${expectedOutcome}\"`),
        }),
      ),
    );
    expect(postMessage).toHaveBeenCalledWith(
      { oarc: "decision-result", ok: true },
      window.location.origin,
    );
    await waitFor(() => expect(replace).toHaveBeenCalledWith("/projects/project-1/overview"), {
      timeout: 1_500,
    });
  });

  it("keeps the outcome decision available when persistence fails", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/outcome-actions") && init?.method === "POST") {
        return new Response("no", { status: 503 });
      }
      if (url.includes("/overview")) return Response.json(completedOverview());
      return Response.json({ status: "completed", phase: "publish", completed_phases: ["publish"] });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    await screen.findByText(/Analysis complete/);
    const postMessage = vi.spyOn(frame().contentWindow!, "postMessage");

    emitArcMessage({ oarc: "decision", action: "confirm", text: null });

    await waitFor(() =>
      expect(postMessage).toHaveBeenCalledWith(
        { oarc: "decision-result", ok: false },
        window.location.origin,
      ),
    );
    expect(replace).not.toHaveBeenCalled();
  });

  it("ignores forged outcome messages from another origin or window", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ status: "running", phase: "perceive", completed_phases: [] }),
      ),
    );
    render(<AnalysisProgress mode="guided" projectId="project-1" runId="run-1" />);
    await screen.findByRole("status");
    const fetchMock = vi.mocked(fetch);

    emitArcMessage(
      { oarc: "decision", action: "confirm", text: null },
      { origin: "https://example.invalid" },
    );
    emitArcMessage(
      { oarc: "decision", action: "confirm", text: null },
      { source: window },
    );

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(replace).not.toHaveBeenCalled();
  });

  it("uses the returning watch-it-work mode without replaying the guided arc", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        Response.json({ status: "running", phase: "perceive", completed_phases: [] }),
      ),
    );

    render(<AnalysisProgress mode="watch" projectId="project-1" runId="run-1" />);

    expect(frame()).toHaveAttribute("src", "/r2/onboarding-arc.html?embed=1&live=1&mode=watch");
  });

  it("hands a completed returning-client read back to Overview without waiting for a first-time decision", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/outcome-actions") && init?.method === "POST") {
        return Response.json({ action: "confirm", outcome: completedOverview().summary });
      }
      if (url.includes("/overview")) return Response.json(completedOverview());
      return Response.json({ status: "completed", phase: "publish", completed_phases: ["publish"] });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AnalysisProgress mode="watch" projectId="project-1" runId="run-1" />);

    await waitFor(() => expect(replace).toHaveBeenCalledWith("/projects/project-1/overview"), {
      timeout: 2_000,
    });
  });
});

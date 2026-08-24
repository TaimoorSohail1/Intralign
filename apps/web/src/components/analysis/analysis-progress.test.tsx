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

describe("AnalysisProgress", () => {
  beforeEach(() => {
    vi.stubGlobal("EventSource", FakeEventSource);
    replace.mockReset();
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("reconnects to the running analysis without reloading the failed page", async () => {
    let statusRequest = 0;
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        return new Response("{}", { status: 202 });
      }
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

    render(<AnalysisProgress projectId="project-1" runId="run-1" />);
    await screen.findByRole("button", { name: "Retry analysis" });

    fireEvent.click(screen.getByRole("button", { name: "Retry analysis" }));

    await waitFor(() => expect(statusRequest).toBe(2));
    expect(screen.getByText("Analyzing…")).toBeInTheDocument();
  });

  it("matches the prototype language while constructing seven documents", async () => {
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

    render(<AnalysisProgress projectId="project-1" runId="run-1" />);

    expect(
      await screen.findByRole("heading", { name: "Constructing your seven documents…" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Flagging thin evidence as clarifications, not certainty…"),
    ).toBeInTheDocument();

    FakeEventSource.current?.emit("analysis.artifact_completed", {
      artifact_type: "intent",
    });

    expect(await screen.findByText("constructed documents")).toBeInTheDocument();
    expect(screen.getByText("· 1 document")).toBeInTheDocument();
    expect(screen.queryByText(/plan artifacts/i)).not.toBeInTheDocument();
  });
});

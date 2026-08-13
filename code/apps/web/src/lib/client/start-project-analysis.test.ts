import { describe, expect, it, vi } from "vitest";

import {
  startProjectAnalysis,
  startProjectAnalysisWithRecovery,
} from "./start-project-analysis";

const projectId = "018f9f7e-8de2-7000-8000-000000000020";
const runId = "018f9f7e-8de2-7000-8000-000000000088";
const documentId = "018f9f7e-8de2-7000-8000-000000000099";

describe("startProjectAnalysis", () => {
  it("uploads document bytes before starting an evidence-linked run", async () => {
    const requests: Array<{ input: RequestInfo | URL; init?: RequestInit }> = [];
    const fetcher = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      requests.push({ input, init });
      if (String(input).endsWith("/documents")) {
        return new Response(
          JSON.stringify({
            document_id: documentId,
            file_name: "plan.pdf",
            status: "parsed",
            fragment_count: 3,
          }),
          { status: 201 },
        );
      }
      return new Response(
        JSON.stringify({
          run_id: runId,
          project_id: projectId,
          kind: "initial",
          status: "queued",
        }),
        { status: 202 },
      );
    });

    const result = await startProjectAnalysis({
      projectId,
      description: "",
      files: [new File(["pdf bytes"], "plan.pdf", { type: "application/pdf" })],
      fetcher,
    });

    expect(result.run_id).toBe(runId);
    expect(requests).toHaveLength(2);
    expect(requests[0].input).toBe(`/api/projects/${projectId}/documents`);
    expect(requests[0].init?.body).toBeInstanceOf(FormData);
    expect(JSON.parse(String(requests[1].init?.body))).toMatchObject({
      sourceNames: ["plan.pdf"],
      sourceDocumentIds: [documentId],
    });
  });

  it("reports every failed document and does not start a partially grounded run", async () => {
    const fetcher = vi.fn(async (input: RequestInfo | URL) => {
      if (!String(input).endsWith("/documents")) {
        throw new Error("Analysis must not start after a partial upload failure");
      }
      if (fetcher.mock.calls.length === 1) {
        return new Response(
          JSON.stringify({
            document_id: documentId,
            file_name: "valid.docx",
            status: "parsed",
            fragment_count: 2,
          }),
          { status: 201 },
        );
      }
      return new Response(
        JSON.stringify({ message: "DOCUMENT_PASSWORD_PROTECTED" }),
        { status: 422 },
      );
    });

    await expect(
      startProjectAnalysis({
        projectId,
        description: "",
        files: [
          new File(["docx"], "valid.docx"),
          new File(["pptx"], "locked.pptx"),
        ],
        fetcher,
      }),
    ).rejects.toThrow("locked.pptx: The document is password-protected.");
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it("creates one replacement project when a stale intake project is unavailable", async () => {
    const replacementId = "018f9f7e-8de2-7000-8000-000000000021";
    const fetcher = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url === `/api/projects/${projectId}/documents`) {
        return new Response(
          JSON.stringify({ code: "PROJECT_NOT_FOUND", message: "Project unavailable" }),
          { status: 404 },
        );
      }
      if (url === "/api/projects/new") {
        return new Response(JSON.stringify({ id: replacementId }), { status: 201 });
      }
      if (url === `/api/projects/${replacementId}/documents`) {
        return new Response(
          JSON.stringify({ document_id: documentId, file_name: "plan.pdf" }),
          { status: 201 },
        );
      }
      return new Response(
        JSON.stringify({
          run_id: runId,
          project_id: replacementId,
          kind: "initial",
          status: "queued",
        }),
        { status: 202 },
      );
    });

    const result = await startProjectAnalysisWithRecovery({
      projectId,
      description: "",
      files: [new File(["pdf"], "plan.pdf")],
      fetcher,
    });

    expect(result.projectId).toBe(replacementId);
    expect(result.run.run_id).toBe(runId);
    expect(fetcher).toHaveBeenCalledTimes(4);
  });

  it("surfaces a friendly replacement-project creation failure", async () => {
    const fetcher = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input) === "/api/projects/new") {
        return new Response(
          JSON.stringify({ message: "A replacement project could not be created." }),
          { status: 503 },
        );
      }
      return new Response(JSON.stringify({ code: "PROJECT_NOT_FOUND" }), {
        status: 404,
      });
    });

    await expect(
      startProjectAnalysisWithRecovery({
        projectId,
        description: "",
        files: [new File(["pdf"], "plan.pdf")],
        fetcher,
      }),
    ).rejects.toThrow(/replacement project could not be created/i);
  });

  it("explains how to recover when a stale project cannot be replaced at the plan limit", async () => {
    const fetcher = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input) === "/api/projects/new") {
        return new Response(JSON.stringify({ message: "OSLO API request failed" }), {
          status: 422,
        });
      }
      return new Response(JSON.stringify({ code: "PROJECT_NOT_FOUND" }), {
        status: 404,
      });
    });

    await expect(
      startProjectAnalysisWithRecovery({
        projectId,
        description: "",
        files: [new File(["pdf"], "plan.pdf")],
        fetcher,
      }),
    ).rejects.toThrow(/Return to Plans.*archive an active plan/i);
  });
});

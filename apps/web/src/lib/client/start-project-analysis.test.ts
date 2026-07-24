import { describe, expect, it, vi } from "vitest";

import { startProjectAnalysis } from "./start-project-analysis";

describe("startProjectAnalysis", () => {
  it("uploads document bytes before starting an evidence-linked run", async () => {
    const requests: Array<{ input: RequestInfo | URL; init?: RequestInit }> = [];
    const fetcher = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      requests.push({ input, init });
      if (String(input).endsWith("/documents")) {
        return new Response(
          JSON.stringify({
            document_id: "018f9f7e-8de2-7000-8000-000000000099",
            file_name: "plan.pdf",
            status: "parsed",
            fragment_count: 3,
          }),
          { status: 201 },
        );
      }
      return new Response(
        JSON.stringify({
          run_id: "018f9f7e-8de2-7000-8000-000000000088",
          project_id: "018f9f7e-8de2-7000-8000-000000000020",
          kind: "initial",
          status: "queued",
        }),
        { status: 202 },
      );
    });

    const result = await startProjectAnalysis({
      projectId: "018f9f7e-8de2-7000-8000-000000000020",
      description: "",
      files: [new File(["pdf bytes"], "plan.pdf", { type: "application/pdf" })],
      fetcher,
    });

    expect(result.run_id).toBe("018f9f7e-8de2-7000-8000-000000000088");
    expect(requests).toHaveLength(2);
    expect(requests[0].input).toBe(
      "/api/projects/018f9f7e-8de2-7000-8000-000000000020/documents",
    );
    expect(requests[0].init?.body).toBeInstanceOf(FormData);
    expect(JSON.parse(String(requests[1].init?.body))).toMatchObject({
      sourceNames: ["plan.pdf"],
      sourceDocumentIds: ["018f9f7e-8de2-7000-8000-000000000099"],
    });
  });

  it("reports every failed document and does not start a partially grounded run", async () => {
    const fetcher = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/documents")) {
        const callNumber = fetcher.mock.calls.length;
        if (callNumber === 1) {
          return new Response(
            JSON.stringify({
              document_id: "018f9f7e-8de2-7000-8000-000000000099",
              file_name: "valid.docx",
              status: "parsed",
              fragment_count: 2,
            }),
            { status: 201 },
          );
        }
        return new Response(
          JSON.stringify({ message: "The presentation is password-protected." }),
          { status: 422 },
        );
      }
      throw new Error("Analysis must not start after a partial upload failure");
    });

    await expect(
      startProjectAnalysis({
        projectId: "018f9f7e-8de2-7000-8000-000000000020",
        description: "",
        files: [
          new File(["docx"], "valid.docx"),
          new File(["pptx"], "locked.pptx"),
        ],
        fetcher,
      }),
    ).rejects.toThrow(
      "locked.pptx: The presentation is password-protected.",
    );
    expect(fetcher).toHaveBeenCalledTimes(2);
  });
});

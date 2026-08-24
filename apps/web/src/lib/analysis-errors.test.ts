import { describe, expect, it } from "vitest";

import { analysisFailureCopy } from "./analysis-errors";

describe("analysisFailureCopy", () => {
  it("keeps provider and validation details out of client-facing copy", () => {
    expect(analysisFailureCopy("OPENAI_QUOTA")).toEqual({
      title: "This read needs another attempt",
      detail:
        "Your documents are safe. OSLO did not publish an incomplete read. Please retry the analysis.",
    });
    expect(analysisFailureCopy("OPENAI_AUTHENTICATION")).toEqual(
      analysisFailureCopy("OPENAI_TIMEOUT"),
    );
    expect(analysisFailureCopy("EVIDENCE_REFERENCE_CONTRACT_FAILED")).toEqual(
      analysisFailureCopy("OPENAI_TIMEOUT"),
    );
  });

  it("keeps unknown internal errors safe and truthful", () => {
    expect(analysisFailureCopy("UNEXPECTED_INTERNAL_ERROR")).toEqual({
      title: "This read needs another attempt",
      detail:
        "Your documents are safe. OSLO did not publish an incomplete read. Please retry the analysis.",
    });
  });
});

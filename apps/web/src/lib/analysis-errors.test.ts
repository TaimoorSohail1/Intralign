import { describe, expect, it } from "vitest";

import { analysisFailureCopy } from "./analysis-errors";

describe("analysisFailureCopy", () => {
  it("explains exhausted OpenAI quota without masking it as a safe pause", () => {
    expect(analysisFailureCopy("OPENAI_QUOTA")).toEqual({
      title: "OpenAI API quota exhausted",
      detail:
        "The configured OpenAI project has no available API quota. Restore API credits or increase its spending limit, then retry.",
    });
  });

  it("distinguishes authentication, rate limits, and timeouts", () => {
    expect(analysisFailureCopy("OPENAI_AUTHENTICATION").title).toBe(
      "OpenAI API key was rejected",
    );
    expect(analysisFailureCopy("OPENAI_RATE_LIMIT").title).toBe(
      "OpenAI rate limit reached",
    );
    expect(analysisFailureCopy("OPENAI_TIMEOUT").title).toBe(
      "OpenAI request timed out",
    );
  });

  it("keeps unknown internal errors safe and truthful", () => {
    expect(analysisFailureCopy("UNEXPECTED_INTERNAL_ERROR")).toEqual({
      title: "Analysis failed",
      detail:
        "OSLO could not complete this analysis. No incomplete result was published.",
    });
  });
});

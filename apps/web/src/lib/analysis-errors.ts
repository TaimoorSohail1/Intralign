export interface AnalysisFailureCopy {
  title: string;
  detail: string;
}

const providerFailures: Record<string, AnalysisFailureCopy> = {
  OPENAI_AUTHENTICATION: {
    title: "OpenAI API key was rejected",
    detail:
      "The configured OpenAI API key could not authenticate. Update the key, then retry.",
  },
  OPENAI_PERMISSION: {
    title: "OpenAI project access was denied",
    detail:
      "The configured API key cannot access the selected OpenAI project or model. Correct its permissions, then retry.",
  },
  OPENAI_QUOTA: {
    title: "OpenAI API quota exhausted",
    detail:
      "The configured OpenAI project has no available API quota. Restore API credits or increase its spending limit, then retry.",
  },
  OPENAI_RATE_LIMIT: {
    title: "OpenAI rate limit reached",
    detail:
      "OpenAI temporarily limited this request. Wait briefly, then retry the analysis.",
  },
  OPENAI_TIMEOUT: {
    title: "OpenAI request timed out",
    detail:
      "OpenAI did not complete the request within the allowed time. No incomplete result was published.",
  },
  OPENAI_UNAVAILABLE: {
    title: "OpenAI service unavailable",
    detail:
      "OSLO reached OpenAI, but the service could not complete the request. No incomplete result was published.",
  },
  OPENAI_OUTPUT_LIMIT: {
    title: "OpenAI response was incomplete",
    detail:
      "The model response ended before the required analysis contract was complete. No incomplete result was published.",
  },
  EVIDENCE_REFERENCE_CONTRACT_FAILED: {
    title: "Evidence validation failed",
    detail:
      "An analysis reference did not match the source evidence. No incomplete result was published.",
  },
};

export function analysisFailureCopy(
  errorCode: string | null | undefined,
): AnalysisFailureCopy {
  return (
    (errorCode ? providerFailures[errorCode] : undefined) ?? {
      title: "Analysis failed",
      detail:
        "OSLO could not complete this analysis. No incomplete result was published.",
    }
  );
}

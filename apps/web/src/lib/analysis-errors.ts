export interface AnalysisFailureCopy {
  title: string;
  detail: string;
}

const clientSafeFailure: AnalysisFailureCopy = {
  title: "This read needs another attempt",
  detail:
    "Your documents are safe. OSLO did not publish an incomplete read. Please retry the analysis.",
};

export function analysisFailureCopy(
  errorCode: string | null | undefined,
): AnalysisFailureCopy {
  void errorCode;
  return clientSafeFailure;
}

interface StartProjectAnalysisInput {
  projectId: string;
  description: string;
  files: File[];
  fetcher?: typeof fetch;
}

interface AnalysisRun {
  run_id: string;
  project_id: string;
  kind: "initial" | "extended";
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
}

async function responseJson(response: Response) {
  return response.json().catch(() => ({}));
}

const documentErrors: Record<string, string> = {
  DOCUMENT_EMPTY: "The document is empty.",
  DOCUMENT_TOO_LARGE: "The document is larger than the 10 MB limit.",
  DOCUMENT_TYPE_UNSUPPORTED: "This file type is not supported.",
  DOCUMENT_TYPE_MISMATCH: "The file contents do not match its extension.",
  DOCUMENT_PASSWORD_PROTECTED: "The document is password-protected.",
  DOCUMENT_TEXT_NOT_EXTRACTABLE: "No readable text was found in the document.",
  DOCUMENT_PDF_INVALID: "The PDF is corrupted or invalid.",
  DOCUMENT_DOCX_INVALID: "The Word document is corrupted or invalid.",
  DOCUMENT_PPTX_INVALID: "The PowerPoint is corrupted or invalid.",
  DOCUMENT_XLSX_INVALID: "The spreadsheet is corrupted or invalid.",
  DOCUMENT_OCR_FAILED: "The scanned PDF could not be read after retrying.",
  DOCUMENT_PARSING_FAILED: "The document could not be processed after retrying.",
};

function documentError(message: unknown) {
  const code = typeof message === "string" ? message : "";
  return documentErrors[code] ?? (code || "Document could not be processed");
}

export async function startProjectAnalysis({
  projectId,
  description,
  files,
  fetcher = fetch,
}: StartProjectAnalysisInput): Promise<AnalysisRun> {
  const uploadResults = await Promise.allSettled(
    files.map(async (file) => {
      const form = new FormData();
      form.append("file", file);
      const response = await fetcher(`/api/projects/${projectId}/documents`, {
        method: "POST",
        body: form,
      });
      const payload = await responseJson(response);
      if (!response.ok) {
        throw new Error(
          `${file.name}: ${documentError(payload.message)}`,
        );
      }
      return payload as {
        document_id: string;
        file_name: string;
      };
    }),
  );
  const uploadFailures = uploadResults.filter(
    (result): result is PromiseRejectedResult => result.status === "rejected",
  );
  if (uploadFailures.length > 0) {
    throw new Error(
      uploadFailures
        .map((failure) =>
          failure.reason instanceof Error
            ? failure.reason.message
            : "A document could not be processed",
        )
        .join("\n"),
    );
  }
  const uploaded = uploadResults.map(
    (result) => (result as PromiseFulfilledResult<{
      document_id: string;
      file_name: string;
    }>).value,
  );

  const response = await fetcher(`/api/projects/${projectId}/analysis-runs`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      description,
      sourceNames: uploaded.map((document) => document.file_name),
      sourceDocumentIds: uploaded.map((document) => document.document_id),
      idempotencyKey: crypto.randomUUID(),
    }),
  });
  const payload = await responseJson(response);
  if (!response.ok) {
    throw new Error(payload.message ?? "Analysis could not start");
  }
  return payload as AnalysisRun;
}

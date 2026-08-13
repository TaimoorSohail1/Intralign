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

interface StartProjectAnalysisResult {
  projectId: string;
  run: AnalysisRun;
}

interface ProjectResponse {
  id?: string;
  project_id?: string;
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

export class ProjectUnavailableError extends Error {
  constructor(message = "This project is no longer available.") {
    super(message);
    this.name = "ProjectUnavailableError";
  }
}

function isProjectUnavailable(response: Response, payload: Record<string, unknown>) {
  return response.status === 404 || payload.code === "PROJECT_NOT_FOUND";
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
      const payload = (await responseJson(response)) as Record<string, unknown>;
      if (!response.ok) {
        if (isProjectUnavailable(response, payload)) {
          throw new ProjectUnavailableError(
            typeof payload.message === "string" ? payload.message : undefined,
          );
        }
        throw new Error(`${file.name}: ${documentError(payload.message)}`);
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
  const unavailableFailure = uploadFailures.find(
    (failure) => failure.reason instanceof ProjectUnavailableError,
  );
  if (unavailableFailure) {
    throw unavailableFailure.reason;
  }
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
    (result) =>
      (
        result as PromiseFulfilledResult<{
          document_id: string;
          file_name: string;
        }>
      ).value,
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
  const payload = (await responseJson(response)) as Record<string, unknown>;
  if (!response.ok) {
    if (isProjectUnavailable(response, payload)) {
      throw new ProjectUnavailableError(
        typeof payload.message === "string" ? payload.message : undefined,
      );
    }
    throw new Error(
      typeof payload.message === "string"
        ? payload.message
        : "Analysis could not start",
    );
  }
  return payload as unknown as AnalysisRun;
}

export async function startProjectAnalysisWithRecovery(
  input: StartProjectAnalysisInput,
): Promise<StartProjectAnalysisResult> {
  const fetcher = input.fetcher ?? fetch;
  try {
    const run = await startProjectAnalysis({ ...input, fetcher });
    return { projectId: input.projectId, run };
  } catch (error) {
    if (!(error instanceof ProjectUnavailableError)) {
      throw error;
    }
  }

  const projectResponse = await fetcher("/api/projects/new", { method: "POST" });
  const projectPayload = (await responseJson(projectResponse)) as Record<
    string,
    unknown
  >;
  if (!projectResponse.ok) {
    if (projectResponse.status === 422) {
      throw new Error(
        "This plan is no longer available. Return to Plans and start a new plan; archive an active plan first if you are at your plan limit.",
      );
    }
    throw new Error(
      typeof projectPayload.message === "string"
        ? projectPayload.message
        : "A replacement project could not be created.",
    );
  }

  const project = projectPayload as ProjectResponse;
  const replacementProjectId = project.id ?? project.project_id;
  if (!replacementProjectId) {
    throw new Error("A replacement project could not be created.");
  }

  const run = await startProjectAnalysis({
    ...input,
    projectId: replacementProjectId,
    fetcher,
  });
  return { projectId: replacementProjectId, run };
}

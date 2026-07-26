import "server-only";

const apiUrl = process.env.OSLO_API_URL ?? "http://127.0.0.1:8000";

export interface InvitationDetails {
  email: string;
  workspace_name: string;
  role: "owner" | "collaborator" | "viewer";
  expires_at: string;
  account_exists: boolean;
}

export interface SessionPayload {
  user_id: string;
  email: string;
  workspace_id: string;
  access_token: string;
  refresh_token: string;
  expires_in: number;
  welcome_required: boolean;
}

export interface InvitationSummary {
  id: string;
  email: string;
  role: "owner" | "collaborator" | "viewer";
  status: "pending" | "accepted" | "revoked" | "expired";
  expires_at: string;
}

export async function apiRequest<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, {
    ...init,
    cache: "no-store",
    headers: { "content-type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail?.message ?? body?.detail ?? "OSLO API request failed");
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const osloApiUrl = apiUrl;

export interface AnalysisRunSummary {
  run_id: string;
  project_id: string;
  kind: "initial" | "extended";
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  phase?: string | null;
  completed_phases?: string[];
  error_code?: string | null;
}

export interface UploadedDocumentSummary {
  document_id: string;
  file_name: string;
  status: "parsed";
  fragment_count: number;
}

export interface OverviewSnapshot {
  snapshot_id: string;
  analysis_run_id: string;
  project_id: string;
  orientation_seen: boolean;
  state: "provisional" | "current" | "last_good";
  summary: string;
  artifacts: Array<{
    artifact_type: string;
    title: string;
    summary: string;
    reliability: string;
    evidence_refs: string[];
    basis: string;
  }>;
  assessment: {
    confidence_index: number;
    confidence_band: string;
    reliability: string;
    clarity: string;
    alignment: string;
    feasibility: string;
    understanding_stage: "orientation" | "expanded" | "validated";
    reliability_basis: {
      coverage: string;
      evidence: string;
      assessability: string;
    };
    confidence_direction: "strengthened" | "weakened" | "unchanged";
    limiting_dimension: "clarity" | "alignment" | "feasibility";
    false_confidence: boolean;
    confidence_explanation: string;
    resolved_issue_count: number;
    confirmed_dependency_count: number;
    issues: Array<{
      id: string;
      artifact_type: string;
      dimension: string;
      severity: string;
      title: string;
      why: string;
      recommendation: string;
      evidence_refs: string[];
      evidence?: Array<{
        source_name: string;
        location: string;
        excerpt: string;
      }>;
      clarification?: string | null;
      status: string;
    }>;
  };
  published_at: string;
  extended_analysis?: AnalysisRunSummary | null;
}

export interface AdvisorReplySummary {
  answer: string;
  follow_up_questions: string[];
}

export interface ArtifactSection {
  heading: string;
  body: string;
  bullets: string[];
  columns: string[];
  rows: string[][];
}

export interface ArtifactWorkspaceSummary {
  artifact_type: string;
  title: string;
  content: { sections: ArtifactSection[] };
  version: number;
  provenance: "from_oslo" | "confirmed_by_user";
  reliability: string;
  basis: string;
  evidence_refs: string[];
  issues: OverviewSnapshot["assessment"]["issues"];
  updated_at: string;
  analysis_run?: AnalysisRunSummary | null;
}

export function startAnalysis(input: {
  accessToken: string;
  projectId: string;
  description: string;
  sourceNames: string[];
  sourceDocumentIds: string[];
  idempotencyKey: string;
}): Promise<AnalysisRunSummary> {
  return apiRequest(`/v1/projects/${input.projectId}/analysis-runs`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${input.accessToken}`,
      "Idempotency-Key": input.idempotencyKey,
    },
    body: JSON.stringify({
      kind: "initial",
      description: input.description,
      source_names: input.sourceNames,
      source_document_ids: input.sourceDocumentIds,
    }),
  });
}

export async function uploadDocument(input: {
  accessToken: string;
  projectId: string;
  file: File;
}): Promise<UploadedDocumentSummary> {
  const form = new FormData();
  form.append("file", input.file);
  const response = await fetch(`${apiUrl}/v1/projects/${input.projectId}/documents`, {
    method: "POST",
    cache: "no-store",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: form,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Document could not be processed");
  }
  return response.json() as Promise<UploadedDocumentSummary>;
}

export function getAnalysisRun(
  accessToken: string,
  runId: string,
): Promise<AnalysisRunSummary> {
  return apiRequest(`/v1/analysis-runs/${runId}`, {
    method: "GET",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function retryAnalysis(
  accessToken: string,
  runId: string,
): Promise<AnalysisRunSummary> {
  return apiRequest(`/v1/analysis-runs/${runId}/retry`, {
    method: "POST",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function getOverview(
  accessToken: string,
  projectId: string,
): Promise<OverviewSnapshot> {
  return apiRequest(`/v1/projects/${projectId}/overview`, {
    method: "GET",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function askAdvisor(input: {
  accessToken: string;
  projectId: string;
  question: string;
}): Promise<AdvisorReplySummary> {
  return apiRequest(`/v1/projects/${input.projectId}/advisor/messages`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ question: input.question }),
  });
}

export function answerProjectIssue(input: {
  accessToken: string;
  projectId: string;
  issueId: string;
  answer: string;
  idempotencyKey: string;
}): Promise<AnalysisRunSummary> {
  return apiRequest(
    `/v1/projects/${input.projectId}/issues/${encodeURIComponent(input.issueId)}/answers`,
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${input.accessToken}`,
        "Idempotency-Key": input.idempotencyKey,
      },
      body: JSON.stringify({ answer: input.answer }),
    },
  );
}

export function getProjectArtifact(
  accessToken: string,
  projectId: string,
  artifactType: string,
): Promise<ArtifactWorkspaceSummary> {
  return apiRequest(
    `/v1/projects/${projectId}/artifacts/${encodeURIComponent(artifactType)}`,
    {
      method: "GET",
      headers: { authorization: `Bearer ${accessToken}` },
    },
  );
}

export function updateProjectArtifact(input: {
  accessToken: string;
  projectId: string;
  artifactType: string;
  content: ArtifactWorkspaceSummary["content"];
  expectedVersion: number;
  idempotencyKey: string;
}): Promise<ArtifactWorkspaceSummary> {
  return apiRequest(
    `/v1/projects/${input.projectId}/artifacts/${encodeURIComponent(input.artifactType)}`,
    {
      method: "PATCH",
      headers: {
        authorization: `Bearer ${input.accessToken}`,
        "Idempotency-Key": input.idempotencyKey,
      },
      body: JSON.stringify({
        content: input.content,
        expected_version: input.expectedVersion,
      }),
    },
  );
}

export function resolveInvitation(token: string): Promise<InvitationDetails> {
  return apiRequest("/v1/invitations/resolve", {
    method: "POST",
    body: JSON.stringify({ token }),
  });
}

export function activateInvitation(input: {
  token: string;
  display_name: string;
  password: string;
}): Promise<SessionPayload> {
  return apiRequest("/v1/invitations/activate", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function acceptExistingInvitation(input: {
  token: string;
  email: string;
  password: string;
}): Promise<SessionPayload> {
  return apiRequest("/v1/invitations/accept-existing", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function sendInvitation(input: {
  accessToken: string;
  workspaceId: string;
  email: string;
  role: string;
}): Promise<{ id: string; email: string }> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/invitations`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ email: input.email, role: input.role }),
  });
}

export function listInvitations(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<InvitationSummary[]> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/invitations`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function resendInvitation(input: {
  accessToken: string;
  workspaceId: string;
  invitationId: string;
}): Promise<InvitationSummary> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/invitations/${input.invitationId}/resend`,
    { method: "POST", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function revokeInvitation(input: {
  accessToken: string;
  workspaceId: string;
  invitationId: string;
}): Promise<void> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/invitations/${input.invitationId}`,
    { method: "DELETE", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function startProject(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<{ id: string; workspace_id: string; name: string; status: string }> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/projects`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

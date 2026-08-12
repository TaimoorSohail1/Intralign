import "server-only";

const apiUrl = process.env.OSLO_API_URL ?? "http://127.0.0.1:8000";

export interface InvitationDetails {
  email: string;
  workspace_name: string;
  role: "owner";
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
  account_role?: "admin" | "owner";
}

export interface SessionContext {
  user_id: string;
  email: string;
  workspace_id: string;
  display_name: string;
  account_role: "admin" | "owner";
  welcome_required: boolean;
}

export interface InvitationSummary {
  id: string;
  email: string;
  role: "owner";
  status: "pending" | "accepted" | "revoked" | "expired";
  expires_at: string;
}

export class OsloApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly detail: unknown,
  ) {
    super(message);
  }
}

export async function apiRequest<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, {
    ...init,
    cache: "no-store",
    headers: { "content-type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const message =
      body?.detail?.message ??
      (typeof body?.detail === "string" ? body.detail : null) ??
      "OSLO API request failed";
    throw new OsloApiError(message, response.status, body?.detail);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const osloApiUrl = apiUrl;

export interface AnalysisRunSummary {
  run_id: string;
  project_id: string;
  kind: "initial" | "extended" | "review";
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  phase?: string | null;
  completed_phases?: string[];
  error_code?: string | null;
  pass_kind?: "fast" | "deep";
  trigger?: "intake" | "batch" | "explicit" | "deep_supersede";
  consolidated_event_ids?: string[];
  provisional?: boolean;
  auto_retry_count?: number;
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
    content?: { sections: ArtifactSection[] };
    assumptions?: ArtifactAssumption[];
    conflicts?: ArtifactConflict[];
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
    integrity: {
      level: "Fragile" | "Weak" | "Developing" | "Solid" | "Sound";
      limiting_pillar: "Viability" | "Grounding" | "Adaptability";
      decomposition: Array<{
        key: "Viability" | "Grounding" | "Adaptability";
        band: "Fragile" | "Weak" | "Developing" | "Solid" | "Sound";
        basis: number;
        why: string[];
      }>;
      posture: "moment-in-time";
      tracking: "pending-execution";
    };
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
      selected_resolution?: string | null;
      pillar?: "Viability" | "Grounding" | "Adaptability";
      dimensions?: string[];
      finding_type?: string;
      section?: string;
      recommendation_from_oslo?: boolean;
      exposure_rank?: number;
    }>;
  };
  provenance?: {
    schema_version: number;
    artifacts: Array<{
      artifact_type: string;
      grounded: number;
      inferred: number;
      total: number;
      verify_first: boolean;
    }>;
    assumptions: Array<{
      id: string;
      artifact_type: string;
      text: string;
      issue_id: string | null;
      issue_title: string | null;
      load_bearing: boolean;
      state: "confirmed" | "inferred" | "conflicting";
    }>;
    grounded_claims: number;
    inferred_claims: number;
    total_claims: number;
    load_bearing_inferences: number;
    structure: {
      unconfirmed_dependencies: number;
      unowned_parties: number;
      untraceable_numbers: number;
    };
    this_week: {
      user_grounded: number;
      oslo_inferred: number;
    };
  };
  published_at: string;
  project_title?: string | null;
  source_document_count?: number;
  extended_analysis?: AnalysisRunSummary | null;
  freshness?: {
    state: "fresh" | "stale" | "reanalyzing";
    pending_count: number;
    based_on_run_id: string | null;
    active_run_id: string | null;
    last_act_at: string | null;
    last_landed_at: string | null;
    latest_pending_event_id?: string | null;
  };
  first_run?: {
    first_run: boolean;
    onboarded: boolean;
    grounding_act_count: number;
    ever_unlocked: boolean;
    unlock_threshold: number;
    freeze_on: boolean;
  };
  read_moved_notifications?: Array<{
    id: string;
    analysis_run_id: string;
    pillar_deltas: Array<{ pillar: string; from: string | null; to: string }>;
    settled_causes: string[];
    previous_band: string | null;
    current_band: string | null;
    delivery_kind: "transient" | "durable";
    seen_at: string | null;
    expires_at: string | null;
    created_at: string;
  }>;
}

export interface AdvisorReplySummary {
  answer: string;
  follow_up_questions: string[];
}

export type HistoryCategory =
  | "analysis"
  | "issues"
  | "versions"
  | "decisions"
  | "collaboration";

export interface HistoryChange {
  label: string;
  tone: "positive" | "neutral" | "warning";
}

export interface HistoryEvent {
  id: number;
  category: HistoryCategory;
  event_type: string;
  summary: string;
  detail: string | null;
  actor_type: "user" | "oslo" | "system";
  artifact_type: string | null;
  artifact_version: number | null;
  issue_id: string | null;
  occurred_at: string;
}

export interface HistoryGroup {
  run_id: string;
  kind: "initial" | "extended";
  status: string;
  current: boolean;
  occurred_at: string;
  confidence_index: number | null;
  confidence_band: string | null;
  confidence_direction: string | null;
  understanding_stage: string | null;
  changes: HistoryChange[];
  events: HistoryEvent[];
}

export interface HistoryTrendPoint {
  run_id: string;
  confidence_index: number;
  confidence_band: string;
  direction: string;
  cause: string;
  occurred_at: string;
  current: boolean;
}

export interface ProjectHistory {
  project_id: string;
  groups: HistoryGroup[];
  trend: HistoryTrendPoint[];
  next_cursor: string | null;
}

export interface IssueActionSummary {
  issue_id: string;
  action: "select" | "apply" | "custom";
  status: "addressed";
  selected_resolution: string;
  analysis_run?: AnalysisRunSummary | null;
}

export interface ArtifactSection {
  id?: string;
  heading: string;
  body: string;
  bullets: string[];
  columns: string[];
  rows: string[][];
  provenance?: "from_oslo" | "confirmed_by_user";
  evidence_refs?: string[];
  row_evidence_refs?: string[][];
  row_states?: Array<"confirmed" | "inferred" | "conflicting" | "unknown">;
  row_provenance?: Array<"from_oslo" | "confirmed_by_user">;
  row_ids?: string[];
}

export interface ArtifactAssumption {
  id: string;
  statement: string;
  state: "confirmed" | "inferred" | "conflicting";
  load_bearing: boolean;
  evidence_refs: string[];
}

export interface ArtifactConflict {
  id: string;
  field: string;
  values: string[];
  evidence_refs: string[];
}

export interface ArtifactWorkspaceSummary {
  artifact_type: string;
  title: string;
  content: { sections: ArtifactSection[] };
  version: number;
  provenance: "from_oslo" | "confirmed_by_user" | "mixed";
  reliability: string;
  basis: string;
  evidence_refs: string[];
  assumptions?: ArtifactAssumption[];
  conflicts?: ArtifactConflict[];
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

export function runProjectReanalysis(input: {
  accessToken: string;
  projectId: string;
  deep?: boolean;
  idempotencyKey: string;
}): Promise<AnalysisRunSummary> {
  return apiRequest(`/v1/projects/${input.projectId}/reanalysis:run`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${input.accessToken}`,
      "Idempotency-Key": input.idempotencyKey,
    },
    body: JSON.stringify({ deep: input.deep ?? false }),
  });
}

export function undoPendingAct(input: {
  accessToken: string;
  projectId: string;
  eventId: string;
}): Promise<{
  event_id: string;
  state: "withdrawn";
  pending_count: number;
  grounding_act_count: number;
  ever_unlocked: boolean;
  freeze_on: boolean;
}> {
  return apiRequest(`/v1/projects/${input.projectId}/acts/${input.eventId}`, {
    method: "DELETE",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function actOnPrimaryOutcome(input: {
  accessToken: string;
  projectId: string;
  action: "confirm" | "refine" | "defer";
  outcome?: string;
  idempotencyKey: string;
}): Promise<{
  action: "confirm" | "refine" | "defer";
  outcome: string;
  analysis_run: AnalysisRunSummary | null;
}> {
  return apiRequest(`/v1/projects/${input.projectId}/outcome-actions`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${input.accessToken}`,
      "Idempotency-Key": input.idempotencyKey,
    },
    body: JSON.stringify({ action: input.action, outcome: input.outcome }),
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
  historyRunId?: string | null;
}): Promise<AdvisorReplySummary> {
  return apiRequest(`/v1/projects/${input.projectId}/advisor/messages`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      question: input.question,
      history_run_id: input.historyRunId ?? null,
    }),
  });
}

export function getProjectHistory(input: {
  accessToken: string;
  projectId: string;
  category?: "all" | HistoryCategory;
  cursor?: string | null;
  limit?: number;
}): Promise<ProjectHistory> {
  const query = new URLSearchParams({
    category: input.category ?? "all",
    limit: String(input.limit ?? 40),
  });
  if (input.cursor) query.set("cursor", input.cursor);
  return apiRequest(`/v1/projects/${input.projectId}/history?${query}`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function getProjectHistorySnapshot(input: {
  accessToken: string;
  projectId: string;
  runId: string;
}): Promise<OverviewSnapshot> {
  return apiRequest(
    `/v1/projects/${input.projectId}/history/runs/${input.runId}`,
    {
      method: "GET",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
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

export function actOnProjectIssue(input: {
  accessToken: string;
  projectId: string;
  issueId: string;
  action: "select" | "apply" | "custom";
  resolution: string;
  idempotencyKey: string;
}): Promise<IssueActionSummary> {
  return apiRequest(
    `/v1/projects/${input.projectId}/issues/${encodeURIComponent(input.issueId)}/actions`,
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${input.accessToken}`,
        "Idempotency-Key": input.idempotencyKey,
      },
      body: JSON.stringify({
        action: input.action,
        resolution: input.resolution,
      }),
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

export function getSessionContext(input: {
  accessToken: string;
}): Promise<SessionContext> {
  return apiRequest("/v1/session", {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function sendInvitation(input: {
  accessToken: string;
  workspaceId: string;
  email: string;
}): Promise<{ id: string; email: string }> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/invitations`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ email: input.email }),
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

export function completeWelcome(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<void> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/welcome`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export interface WorkspaceProjectSummary {
  id: string;
  name: string;
  status: string;
  archived: boolean;
  updated_at: string;
  analysis_status: string;
  confidence_index: number | null;
  confidence_band: string | null;
  reliability: string | null;
  open_issues: number;
  artifact_count: number;
}

export interface WorkspaceNotificationSummary {
  key: string;
  project_id: string;
  project_name: string;
  kind: "initial" | "extended";
  status: "completed" | "failed";
  title: string;
  created_at: string;
  read: boolean;
}

export interface WorkspaceSummary {
  id: string;
  name: string;
  role: "owner";
  plan: "free" | "basic";
  plan_label: string;
  price_usd_monthly: number;
  document_limit: number;
  word_limit: number;
  collaborator_seat_limit: number;
  monthly_analysis_limit: number | null;
  monthly_analyses_used: number;
  can_manage_plan: boolean;
  member_count?: number;
  collaborator_seats_used?: number;
  active_project_limit?: number;
  can_create_project?: boolean;
  projects: WorkspaceProjectSummary[];
  notifications: WorkspaceNotificationSummary[];
}

export interface WorkspacePreferences {
  theme: "dark" | "light" | "system";
  analysis_notifications: boolean;
  failure_notifications: boolean;
  stale_notifications: boolean;
  display_name: string;
  role_title: string;
  workspace_name: string;
  actor_role: "owner";
  mentions_notifications: boolean;
  reply_notifications: boolean;
  shared_notifications: boolean;
}

export interface CollaborationState {
  actor_role: "owner";
  plan: {
    name: string;
    collaborator_seats: number;
    collaborator_seats_used: number;
    monthly_invites: number;
    monthly_invites_used?: number;
    viewers_unlimited: boolean;
    reviewers_unmetered: boolean;
    export_formats: string[];
  };
  participants: Array<{ id: string; display_name: string; role: "owner" }>;
  invitations?: InvitationSummary[];
  comments: Array<{
    id: string;
    issue_id: string;
    body: string;
    mentions: string[];
    author_name: string;
    created_at: string;
  }>;
  reviews: Array<{
    id: string;
    issue_id?: string | null;
    reviewer_name: string;
    reviewer_email?: string | null;
    expires_at: string;
    resolved_at?: string | null;
    revoked_at?: string | null;
    response_id?: string | null;
    response_kind?: string | null;
    response_body?: string | null;
    responded_at?: string | null;
    analysis_run_id?: string | null;
  }>;
  share_links: Array<{
    id: string;
    expires_at: string;
    revoked_at?: string | null;
    created_at: string;
  }>;
}

export function getCollaboration(accessToken: string, projectId: string) {
  return apiRequest<CollaborationState>(`/v1/projects/${projectId}/collaboration`, {
    method: "GET",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function createShareLink(accessToken: string, projectId: string) {
  return apiRequest<{ id: string; url: string; expires_at: string }>(
    `/v1/projects/${projectId}/share-links`,
    { method: "POST", headers: { authorization: `Bearer ${accessToken}` } },
  );
}

export function createReviewGrant(input: {
  accessToken: string;
  projectId: string;
  issueId?: string | null;
  reviewerName: string;
  reviewerEmail?: string | null;
}) {
  return apiRequest<{ id: string; url: string; expires_at: string }>(
    `/v1/projects/${input.projectId}/review-grants`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({
        issue_id: input.issueId ?? null,
        reviewer_name: input.reviewerName,
        reviewer_email: input.reviewerEmail || null,
      }),
    },
  );
}

export function revokeShareLink(input: {
  accessToken: string;
  projectId: string;
  linkId: string;
}): Promise<void> {
  return apiRequest(
    `/v1/projects/${input.projectId}/share-links/${input.linkId}`,
    { method: "DELETE", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function revokeReviewGrant(input: {
  accessToken: string;
  projectId: string;
  grantId: string;
}): Promise<void> {
  return apiRequest(
    `/v1/projects/${input.projectId}/review-grants/${input.grantId}`,
    { method: "DELETE", headers: { authorization: `Bearer ${input.accessToken}` } },
  );
}

export function addProjectComment(input: {
  accessToken: string;
  projectId: string;
  issueId: string;
  body: string;
  mentions: string[];
}) {
  return apiRequest(
    `/v1/projects/${input.projectId}/issues/${encodeURIComponent(input.issueId)}/comments`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({ body: input.body, mentions: input.mentions }),
    },
  );
}

export function getWorkspace(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<WorkspaceSummary> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function promoteReviewResponse(input: {
  accessToken: string;
  projectId: string;
  responseId: string;
}) {
  return apiRequest<{
    response_id: string;
    analysis_run_id: string;
    status: string;
  }>(
    `/v1/projects/${input.projectId}/review-responses/${input.responseId}/evidence`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

export type ReportContent = {
  sections: Array<{ id: string; title: string; body: string[] }>;
};

export function getProjectReport(accessToken: string, projectId: string) {
  return apiRequest<{
    project_id: string;
    project_name: string;
    snapshot_id: string;
    content: ReportContent | null;
    updated_at: string | null;
    deliveries: Array<{
      id: string;
      recipient_email: string;
      recipient_label: string;
      status: "scheduled" | "sending" | "sent" | "failed";
      scheduled_for: string;
      sent_at: string | null;
      error_code: string | null;
      currency_state: "current" | "previous_analysis";
      previous_analysis_confirmed: boolean;
    }>;
  }>(`/v1/projects/${projectId}/report`, {
    method: "GET",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function saveProjectReport(input: {
  accessToken: string;
  projectId: string;
  snapshotId: string;
  content: ReportContent;
}) {
  return apiRequest(`/v1/projects/${input.projectId}/report`, {
    method: "PUT",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      snapshot_id: input.snapshotId,
      content: input.content,
    }),
  });
}

export function deliverProjectReport(input: {
  accessToken: string;
  projectId: string;
  snapshotId: string;
  recipientEmail: string;
  recipientLabel: string;
  subject: string;
  content: ReportContent;
  scheduledFor?: string | null;
  confirmPreviousAnalysis?: boolean;
}) {
  return apiRequest<{
    id: string;
    status: "scheduled" | "sending" | "sent" | "failed";
    scheduled_for: string;
    sent_at: string | null;
    error_code: string | null;
    currency_state: "current" | "previous_analysis";
    previous_analysis_confirmed: boolean;
  }>(`/v1/projects/${input.projectId}/report/deliveries`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      snapshot_id: input.snapshotId,
      recipient_email: input.recipientEmail,
      recipient_label: input.recipientLabel,
      subject: input.subject,
      content: input.content,
      scheduled_for: input.scheduledFor || null,
      confirm_previous_analysis: input.confirmPreviousAnalysis ?? false,
    }),
  });
}

export function setWorkspacePlan(input: {
  accessToken: string;
  workspaceId: string;
  plan: WorkspaceSummary["plan"];
}): Promise<WorkspaceSummary> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/plan`, {
    method: "PUT",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ plan: input.plan }),
  });
}

export function setProjectArchived(input: {
  accessToken: string;
  workspaceId: string;
  projectId: string;
  archived: boolean;
}): Promise<void> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/projects/${input.projectId}/${
      input.archived ? "archive" : "restore"
    }`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

export function markWorkspaceNotificationsRead(input: {
  accessToken: string;
  workspaceId: string;
  keys: string[];
}): Promise<void> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/notifications/read`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ keys: input.keys }),
  });
}

export function getWorkspacePreferences(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<WorkspacePreferences> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/preferences`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function updateWorkspacePreferences(input: {
  accessToken: string;
  workspaceId: string;
  preferences: WorkspacePreferences;
}): Promise<WorkspacePreferences> {
  const preferences = {
    theme: input.preferences.theme,
    analysis_notifications: input.preferences.analysis_notifications,
    failure_notifications: input.preferences.failure_notifications,
    stale_notifications: input.preferences.stale_notifications,
    display_name: input.preferences.display_name,
    role_title: input.preferences.role_title,
    workspace_name: input.preferences.workspace_name,
    mentions_notifications: input.preferences.mentions_notifications,
    reply_notifications: input.preferences.reply_notifications,
    shared_notifications: input.preferences.shared_notifications,
  };
  return apiRequest(`/v1/workspaces/${input.workspaceId}/preferences`, {
    method: "PUT",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify(preferences),
  });
}

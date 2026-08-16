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
    const validationIssue = Array.isArray(body?.detail) ? body.detail[0] : null;
    const validationField = Array.isArray(validationIssue?.loc)
      ? validationIssue.loc.at(-1)
      : null;
    const validationMessage = validationIssue?.msg
      ? `${validationField ? `${String(validationField).replaceAll("_", " ")}: ` : ""}${validationIssue.msg}`
      : null;
    const message =
      body?.detail?.message ??
      (typeof body?.detail === "string" ? body.detail : null) ??
      validationMessage ??
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
      complete?: boolean;
      sound_claim_blocked?: boolean;
      under_review_regions?: string[];
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
      basis?: "documented" | "vendor-or-owner-verified" | "verified-directly" | "answered" | null;
      evidence_ref?: string | null;
      attested_by?: { id: string; display_name: string; role: string } | null;
      routed_to?: { id: string; display_name: string; role: string } | null;
      pillar?: "Viability" | "Grounding" | "Adaptability";
      dimensions?: string[];
      finding_type?: string;
      section?: string;
      recommendation_from_oslo?: boolean;
      exposure_rank?: number;
      finding_basis?: "inference" | "structural" | "decision" | "model_gap" | "";
      structural_target?: "definition" | "edge" | "achievability" | "truth" | "coverage" | "";
      primary_act?: "verify" | "build" | "decide" | "";
      also_offered?: Array<"verify" | "build" | "decide">;
      classification_state?: "classified" | "escalated" | "unclassified";
      sensitivity?: number | null;
      sensitivity_trace?: {
        paths: string[][];
        span_true: number;
        span_false: number;
        span: number;
        leverage: number;
        uncertainty_factor: number;
        runway_factor: number;
        edge_key?: [string, string] | null;
        outcome_reachability: string[];
      } | null;
      sensitivity_state?: "calibrated" | "shadow" | "unavailable";
      unassessed?: boolean;
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
  kind: "initial" | "extended";
  provisional: boolean;
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
      kind: input.kind,
      provisional: input.provisional,
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
    const message =
      (typeof body?.detail === "string" ? body.detail : body?.detail?.message) ??
      "Document could not be processed";
    throw new OsloApiError(message, response.status, body?.detail);
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

export type IssueLifecycleAct = "confirm" | "flag" | "fix" | "ground" | "route" | "withdraw";
export type IssueBasis = "documented" | "vendor-or-owner-verified" | "verified-directly" | "answered";

export interface IssueLifecycleActSummary {
  issue_id: string;
  act: IssueLifecycleAct;
  status: "open" | "addressed" | "routed" | "needs_fix" | "needs_grounding" | "resolved";
  attestation: {
    id: string;
    act: IssueLifecycleAct;
    basis: IssueBasis | null;
    evidence_ref: string | null;
    attributed_to: { id: string; display_name: string; role: string };
    supersedes: string | null;
  };
  analysis_run?: AnalysisRunSummary | null;
}

export interface IssueProposalSummary {
  id: string;
  issue_id: string;
  kind: "build" | "inference" | "optional";
  resolver_key: string;
  title: string;
  rationale: string;
  artifact_type: string | null;
  load_bearing: boolean;
  accepted: boolean;
  rejected: boolean;
  surface: "issue_card" | "artifact" | "folded_read" | null;
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

export async function getOrientationSeen(
  accessToken: string,
  projectId: string,
): Promise<boolean> {
  const result = await apiRequest<{ seen: boolean }>(
    `/v1/projects/${projectId}/orientation-seen`,
    {
      method: "GET",
      headers: { authorization: `Bearer ${accessToken}` },
    },
  );
  return result.seen;
}

export function actOnProjectIssueLifecycle(input: {
  accessToken: string;
  projectId: string;
  issueId: string;
  act: IssueLifecycleAct;
  basis?: IssueBasis | null;
  evidenceRef?: string | null;
  resolution?: string | null;
  reviewer?: { id: string; display_name: string; role: string } | null;
  idempotencyKey: string;
}): Promise<IssueLifecycleActSummary> {
  return apiRequest(
    `/v1/projects/${input.projectId}/issues/${encodeURIComponent(input.issueId)}/acts`,
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${input.accessToken}`,
        "Idempotency-Key": input.idempotencyKey,
      },
      body: JSON.stringify({
        act: input.act,
        basis: input.basis ?? null,
        evidence_ref: input.evidenceRef ?? null,
        resolution: input.resolution ?? null,
        reviewer: input.reviewer ?? null,
      }),
    },
  );
}

export function getProjectIssueProposals(input: {
  accessToken: string;
  projectId: string;
}): Promise<IssueProposalSummary[]> {
  return apiRequest(`/v1/projects/${input.projectId}/proposals`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function decideProjectIssueProposal(input: {
  accessToken: string;
  projectId: string;
  proposalId: string;
  accepted: boolean;
  surface: "issue_card" | "artifact" | "folded_read";
  idempotencyKey: string;
}): Promise<{ proposal: IssueProposalSummary; analysis_run?: AnalysisRunSummary | null }> {
  return apiRequest(
    `/v1/projects/${input.projectId}/proposals/${input.proposalId}/decisions`,
    {
      method: "POST",
      headers: {
        authorization: `Bearer ${input.accessToken}`,
        "Idempotency-Key": input.idempotencyKey,
      },
      body: JSON.stringify({
        accepted: input.accepted,
        surface: input.surface,
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
  weakest_pillar?: string | null;
}

export interface WorkspaceNotificationSummary {
  key: string;
  project_id: string;
  project_name: string;
  kind: "initial" | "extended" | "review" | "mention";
  status: "completed" | "failed";
  title: string;
  created_at: string;
  read: boolean;
  href?: string | null;
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
  collaborator_seat_limit: number | null;
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
  actor_role: "owner" | "collaborator" | "viewer";
  plan: {
    name: string;
    collaborators_unmetered: boolean;
    invitations_unmetered: boolean;
    viewers_unlimited: boolean;
    reviewers_unmetered: boolean;
    export_formats: string[];
  };
  participants: Array<{
    id: string;
    display_name: string;
    role: "owner" | "collaborator" | "viewer";
  }>;
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
    delivery_state: "draft" | "sending" | "delivered" | "failed" | "awaiting" | "answered" | "withdrawn";
    delivery_attempts: number;
    delivered_at?: string | null;
    withdrawn_at?: string | null;
    question?: string | null;
    source_ref?: string | null;
    source_excerpt?: string | null;
  }>;
  share_links: Array<{
    id: string;
    expires_at: string;
    revoked_at?: string | null;
    created_at: string;
    recipient_name: string;
    recipient_email?: string | null;
    first_viewed_at?: string | null;
    last_viewed_at?: string | null;
  }>;
}

export type GroundingNodeState = "grounded" | "addressed" | "routed" | "inferred";

export interface GroundingMapProjection {
  project_id: string;
  actor_role: string;
  counts: Record<GroundingNodeState, number>;
  nodes: Array<{
    issue_id: string;
    title: string;
    detail?: string;
    artifact_type: string;
    pillar: string;
    state: GroundingNodeState;
    exposure_rank: number;
    href: string;
  }>;
}

export interface CollaborationRollUpProjection {
  project_id: string;
  actor_role: string;
  integrity: OverviewSnapshot["assessment"]["integrity"];
  trend: "strengthened" | "weakened" | "unchanged";
  decision_queue: GroundingMapProjection["nodes"];
  reviewers: Array<{
    id: string;
    issue_id?: string | null;
    reviewer_name: string;
    delivery_state: string;
    expires_at: string;
    responded_at?: string | null;
    response_kind?: string | null;
    analysis_run_id?: string | null;
  }>;
  who_is_grounding_what: Array<{
    reviewer_name: string;
    issue_id: string;
    state: string;
    href: string;
  }>;
  rests_on: Record<GroundingNodeState, number>;
}

export function getCollaborationRollUp(accessToken: string, projectId: string) {
  return apiRequest<CollaborationRollUpProjection>(
    `/v1/projects/${projectId}/collaboration/roll-up`,
    { method: "GET", headers: { authorization: `Bearer ${accessToken}` } },
  );
}

export function getCollaborationGroundingMap(accessToken: string, projectId: string) {
  return apiRequest<GroundingMapProjection>(
    `/v1/projects/${projectId}/collaboration/grounding-map`,
    { method: "GET", headers: { authorization: `Bearer ${accessToken}` } },
  );
}

export function getCollaboration(accessToken: string, projectId: string) {
  return apiRequest<CollaborationState>(`/v1/projects/${projectId}/collaboration`, {
    method: "GET",
    headers: { authorization: `Bearer ${accessToken}` },
  });
}

export function createShareLink(input: {
  accessToken: string;
  projectId: string;
  recipientName: string;
  recipientEmail?: string | null;
}) {
  return apiRequest<{ id: string; url: string; expires_at: string }>(
    `/v1/projects/${input.projectId}/share-links`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({
        recipient_name: input.recipientName,
        recipient_email: input.recipientEmail || null,
      }),
    },
  );
}

export function createReviewGrant(input: {
  accessToken: string;
  projectId: string;
  issueId: string;
  reviewerName: string;
  reviewerEmail?: string | null;
  question: string;
  sourceRef: string;
  sourceExcerpt: string;
}) {
  return apiRequest<{
    id: string;
    url: string;
    expires_at: string;
    delivery_state: "draft" | "awaiting" | "failed";
    delivery_attempts: number;
    delivered_at?: string | null;
  }>(
    `/v1/projects/${input.projectId}/review-grants`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({
        issue_id: input.issueId,
        reviewer_name: input.reviewerName,
        reviewer_email: input.reviewerEmail || null,
        question: input.question,
        source_ref: input.sourceRef,
        source_excerpt: input.sourceExcerpt,
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

export type ReportSchedule = {
  id: string;
  recipient_email: string;
  recipient_class: "exec-sponsor" | "team" | "board";
  weekday: number;
  local_time: string;
  timezone: string;
  state: "enabled" | "paused";
  next_run_at: string;
  last_run_at: string | null;
  last_delivery_id: string | null;
  created_at: string;
  updated_at: string;
};

export type AsanaHandoffState = {
  configured: boolean;
  entitled: boolean;
  destination_gid: string | null;
  snapshot_id: string;
  preview: Array<{
    item_key: string;
    task: string;
    owner: string | null;
    start_on: string | null;
    due_on: string | null;
    source_date: string | null;
    provenance: string;
  }>;
  latest: null | {
    id: string;
    state: "running" | "partial" | "completed" | "failed";
    total_count: number;
    completed_count: number;
    safe_error_code: string | null;
    destination_gid: string;
    created_at: string;
    updated_at: string;
  };
};

export function getProjectReport(accessToken: string, projectId: string) {
  return apiRequest<{
    project_id: string;
    project_name: string;
    snapshot_id: string;
    content: ReportContent | null;
    updated_at: string | null;
    recipient_class: "exec-sponsor" | "team" | "board";
    composition_depth: "summary" | "full";
    included: Record<string, boolean>;
    revision: number;
    source_analysis_run_id: string | null;
    read_signature: string | null;
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
      report_version: number;
      source_analysis_run_id: string;
      analysis_completed_at: string;
      read_signature: string;
      content_checksum: string;
      disclaimer_version: string;
      content?: ReportContent;
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
  recipientClass?: "exec-sponsor" | "team" | "board";
  compositionDepth?: "summary" | "full";
  included?: Record<string, boolean>;
  revision?: number;
}) {
  return apiRequest(`/v1/projects/${input.projectId}/report`, {
    method: "PUT",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      snapshot_id: input.snapshotId,
      content: input.content,
      recipient_class: input.recipientClass ?? "exec-sponsor",
      composition_depth: input.compositionDepth ?? "full",
      included: input.included ?? {},
      revision: input.revision ?? 1,
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

export interface HostedBillingSession {
  id: string;
  url: string;
}

export function getProjectReportSchedules(input: {
  accessToken: string;
  projectId: string;
}): Promise<ReportSchedule[]> {
  return apiRequest(`/v1/projects/${input.projectId}/report/schedules`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function createProjectReportSchedule(input: {
  accessToken: string;
  projectId: string;
  recipientEmail: string;
  recipientClass: "exec-sponsor" | "team" | "board";
  weekday: number;
  localTime: string;
  timezone: string;
}): Promise<ReportSchedule> {
  return apiRequest(`/v1/projects/${input.projectId}/report/schedules`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      recipient_email: input.recipientEmail,
      recipient_class: input.recipientClass,
      weekday: input.weekday,
      local_time: input.localTime,
      timezone: input.timezone,
    }),
  });
}

export function updateProjectReportSchedule(input: {
  accessToken: string;
  projectId: string;
  scheduleId: string;
  state: "enabled" | "paused";
}): Promise<ReportSchedule> {
  return apiRequest(
    `/v1/projects/${input.projectId}/report/schedules/${input.scheduleId}`,
    {
      method: "PATCH",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({ state: input.state }),
    },
  );
}

export function deleteProjectReportSchedule(input: {
  accessToken: string;
  projectId: string;
  scheduleId: string;
}): Promise<void> {
  return apiRequest(
    `/v1/projects/${input.projectId}/report/schedules/${input.scheduleId}`,
    {
      method: "DELETE",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

export function recordProjectReportExport(input: {
  accessToken: string;
  projectId: string;
  format: "pdf" | "excel" | "csv" | "text" | "copy-summary" | "asana";
  contentChecksum?: string | null;
}) {
  return apiRequest(`/v1/projects/${input.projectId}/report/exports`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      format: input.format,
      content_checksum: input.contentChecksum ?? null,
    }),
  });
}

export function getProjectAsanaHandoff(input: {
  accessToken: string;
  projectId: string;
}): Promise<AsanaHandoffState> {
  return apiRequest(`/v1/projects/${input.projectId}/report/asana`, {
    method: "GET",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function importProjectToAsana(input: {
  accessToken: string;
  projectId: string;
}) {
  return apiRequest<NonNullable<AsanaHandoffState["latest"]>>(
    `/v1/projects/${input.projectId}/report/asana`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

export function markReviewDelivered(input: {
  accessToken: string;
  projectId: string;
  grantId: string;
}) {
  return apiRequest<{
    id: string;
    delivery_state: "awaiting" | "answered" | "withdrawn";
    delivery_attempts: number;
    delivered_at: string;
  }>(`/v1/projects/${input.projectId}/review-grants/${input.grantId}/deliveries/manual`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export interface ProjectOutcomeSummary {
  id: string;
  workspace_id: string;
  project_id: string;
  title: string;
  status: "active" | "archived";
  is_primary: boolean;
  provenance: "declared" | "inferred";
  created_at: string;
  archived_at: string | null;
}

export function createBasicCheckout(input: {
  accessToken: string;
  workspaceId: string;
  interval: "monthly" | "annual";
  wallKey: "multiOutcome" | "multiPlan" | "envelope" | "schedule";
}): Promise<HostedBillingSession> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/billing/checkout-sessions`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({ interval: input.interval, wall_key: input.wallKey }),
  });
}

export function createBillingPortal(input: {
  accessToken: string;
  workspaceId: string;
}): Promise<HostedBillingSession> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/billing/portal-sessions`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
  });
}

export function recordCapacityIntent(input: {
  accessToken: string;
  workspaceId: string;
  wallKey: "multiOutcome" | "multiPlan" | "envelope" | "schedule";
  chosenPath: "committed" | "free_path" | "declined" | "keep_both";
  fullOptionSet: string[];
  context: Record<string, unknown>;
}): Promise<void> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/intent-signals`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify({
      wall_key: input.wallKey,
      chosen_path: input.chosenPath,
      full_option_set: input.fullOptionSet,
      context: input.context,
    }),
  });
}

export function listProjectOutcomes(input: {
  accessToken: string;
  workspaceId: string;
  projectId: string;
}): Promise<ProjectOutcomeSummary[]> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/projects/${input.projectId}/outcomes`,
    {
      method: "GET",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

export function createProjectOutcome(input: {
  accessToken: string;
  workspaceId: string;
  projectId: string;
  title: string;
}): Promise<ProjectOutcomeSummary> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/projects/${input.projectId}/outcomes`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
      body: JSON.stringify({ title: input.title, provenance: "declared" }),
    },
  );
}

export function setOutcomeArchived(input: {
  accessToken: string;
  workspaceId: string;
  outcomeId: string;
  archived: boolean;
}): Promise<ProjectOutcomeSummary> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/outcomes/${input.outcomeId}:${
      input.archived ? "archive" : "reactivate"
    }`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
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

export interface FeedbackTicketSummary {
  ticket_id: string;
  title: string;
  status: string;
  created_at: string;
}

export interface FeedbackTicketInput {
  session_id: string;
  category: "defect" | "enhancement" | "other";
  body: string;
  expected: string | null;
  impact: "blocking" | "slowing" | "minor" | null;
  context: {
    where: string;
    view: string;
    role: string;
    grounded_x: number;
    total_y: number;
    first_run_flag: boolean;
    ts: string;
  };
}

export function fileFeedbackTicket(input: {
  accessToken: string;
  workspaceId: string;
  ticket: FeedbackTicketInput;
}): Promise<FeedbackTicketSummary> {
  return apiRequest(`/v1/workspaces/${input.workspaceId}/feedback/tickets`, {
    method: "POST",
    headers: { authorization: `Bearer ${input.accessToken}` },
    body: JSON.stringify(input.ticket),
  });
}

export function listFeedbackTickets(input: {
  accessToken: string;
  workspaceId: string;
  sessionId: string;
}): Promise<FeedbackTicketSummary[]> {
  return apiRequest(
    `/v1/workspaces/${input.workspaceId}/feedback/tickets?session_id=${encodeURIComponent(input.sessionId)}`,
    {
      method: "GET",
      headers: { authorization: `Bearer ${input.accessToken}` },
    },
  );
}

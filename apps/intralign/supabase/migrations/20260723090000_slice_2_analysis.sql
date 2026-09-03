create type public.analysis_run_kind as enum ('initial', 'extended');
create type public.analysis_run_status as enum (
  'queued', 'running', 'completed', 'failed', 'cancelled'
);
create type public.analysis_phase as enum (
  'submit_intake',
  'validate_scope',
  'ingest_parse',
  'perceive',
  'retrieve_evidence',
  'construct_artifacts',
  'checkpoint',
  'evaluate_advise',
  'validate_result',
  'publish',
  'project_browser',
  'extended_transition'
);
create type public.plan_artifact_type as enum (
  'intent',
  'context',
  'scope',
  'requirements',
  'work_breakdown',
  'schedule',
  'resources'
);

alter table public.memberships
  add column orientation_seen_at timestamptz;

create table public.intake_submissions (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  submitted_by uuid not null references public.profiles (id),
  start_method text not null default 'description'
    check (start_method in ('description', 'documents', 'template', 'sample')),
  description text not null default ''
    check (char_length(description) <= 100000),
  submitted_at timestamptz not null default now()
);

create table public.source_documents (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  intake_submission_id uuid not null
    references public.intake_submissions (id) on delete cascade,
  file_name text not null,
  object_key text not null,
  detected_mime_type text,
  byte_size bigint not null check (byte_size between 0 and 10485760),
  checksum text not null,
  status text not null default 'uploaded'
    check (status in ('uploaded', 'parsing', 'parsed', 'failed', 'rejected')),
  parser_version text,
  failure_code text,
  created_at timestamptz not null default now(),
  unique (workspace_id, project_id, checksum)
);

create table public.source_fragments (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  source_document_id uuid not null
    references public.source_documents (id) on delete cascade,
  ordinal integer not null check (ordinal >= 0),
  content text not null,
  locator jsonb not null default '{}'::jsonb,
  checksum text not null,
  embedding extensions.vector(1536),
  embedding_model text,
  created_at timestamptz not null default now(),
  unique (source_document_id, ordinal)
);

create table public.analysis_runs (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  intake_submission_id uuid references public.intake_submissions (id) on delete set null,
  requested_by uuid not null references public.profiles (id),
  kind public.analysis_run_kind not null,
  status public.analysis_run_status not null default 'queued',
  description text not null default '',
  source_names jsonb not null default '[]'::jsonb,
  idempotency_key text not null,
  parent_run_id uuid references public.analysis_runs (id),
  current_phase public.analysis_phase,
  error_code text,
  graph_version text not null default 'slice2-graph-v1',
  harness_version text not null default 'oslo-harness-v1',
  prompt_versions jsonb not null default '{}'::jsonb,
  model_versions jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz,
  updated_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

create index analysis_runs_project_created_idx
  on public.analysis_runs (workspace_id, project_id, created_at desc);
create index analysis_runs_active_idx
  on public.analysis_runs (workspace_id, status, created_at)
  where status in ('queued', 'running');

create table public.analysis_node_attempts (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  phase public.analysis_phase not null,
  attempt_no integer not null default 1 check (attempt_no > 0),
  status text not null check (status in ('running', 'completed', 'failed')),
  safe_error_code text,
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  unique (analysis_run_id, phase, attempt_no)
);

create table public.analysis_checkpoints (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  checkpoint_key text not null,
  completed_phases jsonb not null default '[]'::jsonb,
  state_json jsonb not null default '{}'::jsonb,
  state_hash text not null,
  graph_version text not null,
  created_at timestamptz not null default now(),
  unique (analysis_run_id, checkpoint_key)
);

create table public.analysis_run_events (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  sequence_no integer not null check (sequence_no > 0),
  event_type text not null,
  phase public.analysis_phase,
  status public.analysis_run_status not null,
  payload jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now(),
  unique (analysis_run_id, sequence_no)
);

create index analysis_run_events_replay_idx
  on public.analysis_run_events (workspace_id, analysis_run_id, sequence_no);

create table public.assessment_snapshots (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null unique
    references public.analysis_runs (id) on delete cascade,
  snapshot_state text not null check (snapshot_state in ('provisional', 'current')),
  snapshot_json jsonb not null,
  published_at timestamptz not null default now()
);

create index assessment_snapshots_project_published_idx
  on public.assessment_snapshots (workspace_id, project_id, published_at desc);

create table public.artifact_versions (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  artifact_type public.plan_artifact_type not null,
  title text not null,
  summary text not null,
  reliability text not null,
  basis text not null,
  evidence_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  unique (analysis_run_id, artifact_type)
);

create table public.issues (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  stable_key text not null,
  current_status text not null default 'open'
    check (current_status in ('open', 'addressed', 'resolved')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project_id, stable_key)
);

create table public.issue_observations (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_id uuid not null references public.issues (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  artifact_type public.plan_artifact_type not null,
  dimension text not null check (dimension in ('Clarity', 'Alignment', 'Feasibility')),
  severity text not null check (severity in ('Warning', 'Moderate', 'Critical')),
  status text not null check (status in ('open', 'addressed', 'resolved')),
  observation_json jsonb not null,
  observed_at timestamptz not null default now(),
  unique (issue_id, analysis_run_id)
);

create table public.idempotency_keys (
  key text not null,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  operation text not null,
  request_hash text not null,
  response_ref text,
  status text not null check (status in ('started', 'completed', 'failed')),
  expires_at timestamptz not null,
  created_at timestamptz not null default now(),
  primary key (workspace_id, operation, key)
);

create table public.outbox_events (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  aggregate_type text not null,
  aggregate_id uuid not null,
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now(),
  published_at timestamptz,
  attempt_count integer not null default 0 check (attempt_count >= 0)
);

create index outbox_events_unpublished_idx
  on public.outbox_events (occurred_at)
  where published_at is null;

alter table public.projects
  add column current_analysis_run_id uuid references public.analysis_runs (id);

alter table public.intake_submissions enable row level security;
alter table public.source_documents enable row level security;
alter table public.source_fragments enable row level security;
alter table public.analysis_runs enable row level security;
alter table public.analysis_node_attempts enable row level security;
alter table public.analysis_checkpoints enable row level security;
alter table public.analysis_run_events enable row level security;
alter table public.assessment_snapshots enable row level security;
alter table public.artifact_versions enable row level security;
alter table public.issues enable row level security;
alter table public.issue_observations enable row level security;
alter table public.idempotency_keys enable row level security;
alter table public.outbox_events enable row level security;

create policy "members can view intake submissions"
  on public.intake_submissions for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view source documents"
  on public.source_documents for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view source fragments"
  on public.source_fragments for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view analysis runs"
  on public.analysis_runs for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view analysis attempts"
  on public.analysis_node_attempts for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view analysis checkpoints"
  on public.analysis_checkpoints for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view analysis events"
  on public.analysis_run_events for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view assessment snapshots"
  on public.assessment_snapshots for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view artifact versions"
  on public.artifact_versions for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view issues"
  on public.issues for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can view issue observations"
  on public.issue_observations for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select on public.intake_submissions, public.source_documents,
  public.source_fragments, public.analysis_runs, public.analysis_node_attempts,
  public.analysis_checkpoints, public.analysis_run_events,
  public.assessment_snapshots, public.artifact_versions, public.issues,
  public.issue_observations to authenticated;

comment on table public.analysis_checkpoints is
  'Restartable graph state. Checkpoints are never user-visible assessment truth.';
comment on table public.analysis_run_events is
  'Safe ordered SSE projection. Raw prompts, source content and hidden reasoning are forbidden.';
comment on table public.outbox_events is
  'Transactional delivery mechanism. PostgreSQL domain state remains canonical truth.';

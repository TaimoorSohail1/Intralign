create table public.analysis_artifact_jobs (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  artifact_type public.plan_artifact_type not null,
  status text not null
    check (status in ('pending', 'running', 'completed', 'failed')),
  attempt_count integer not null default 0 check (attempt_count >= 0),
  output_json jsonb,
  safe_error_code text,
  retryable boolean,
  lease_owner text,
  lease_expires_at timestamptz,
  heartbeat_at timestamptz,
  provider text,
  model_id text,
  prompt_version text,
  provider_response_id text,
  input_tokens integer check (input_tokens >= 0),
  output_tokens integer check (output_tokens >= 0),
  duration_ms integer check (duration_ms >= 0),
  execution_mode text check (execution_mode in ('primary', 'fallback')),
  fallback_reason text,
  created_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz,
  updated_at timestamptz not null default now(),
  unique (analysis_run_id, artifact_type)
);

create index analysis_artifact_jobs_claim_idx
  on public.analysis_artifact_jobs (status, lease_expires_at, updated_at)
  where status in ('pending', 'running', 'failed');

alter table public.analysis_artifact_jobs enable row level security;

create policy "members can view analysis artifact jobs"
  on public.analysis_artifact_jobs for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select on public.analysis_artifact_jobs to authenticated;

comment on table public.analysis_artifact_jobs is
  'Durable per-artifact construction state. Completed outputs survive sibling failures and are reused by retry.';
comment on column public.analysis_artifact_jobs.lease_owner is
  'Opaque worker identifier used with lease_expires_at to make future queue workers safe.';

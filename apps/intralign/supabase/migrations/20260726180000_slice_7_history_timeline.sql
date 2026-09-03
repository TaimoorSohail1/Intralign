create type public.project_history_category as enum (
  'analysis',
  'issues',
  'versions',
  'decisions'
);

create table public.project_history_events (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  actor_id uuid references public.profiles (id) on delete set null,
  actor_type text not null check (actor_type in ('user', 'oslo', 'system')),
  category public.project_history_category not null,
  event_type text not null check (char_length(event_type) between 1 and 120),
  summary text not null check (char_length(summary) between 1 and 300),
  detail text check (detail is null or char_length(detail) <= 2000),
  artifact_type public.plan_artifact_type,
  artifact_version integer check (artifact_version is null or artifact_version > 0),
  issue_stable_key text,
  payload jsonb not null default '{}'::jsonb,
  schema_version integer not null default 1 check (schema_version > 0),
  idempotency_key text not null,
  occurred_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

create index project_history_events_project_cursor_idx
  on public.project_history_events (workspace_id, project_id, occurred_at desc, id desc);

create index project_history_events_run_idx
  on public.project_history_events (analysis_run_id, occurred_at, id);

create index project_history_events_category_idx
  on public.project_history_events (
    workspace_id,
    project_id,
    category,
    occurred_at desc,
    id desc
  );

alter table public.project_history_events enable row level security;

create policy "members can view project history"
  on public.project_history_events for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select on public.project_history_events to authenticated;
grant usage, select on sequence public.project_history_events_id_seq to authenticated;

comment on table public.project_history_events is
  'Append-only, user-facing Slice 7 history ledger. Stores safe summaries and references; canonical project truth remains in snapshots, artifacts, issues, and decisions.';

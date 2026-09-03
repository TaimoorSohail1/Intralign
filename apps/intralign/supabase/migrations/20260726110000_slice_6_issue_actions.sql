create table public.issue_actions (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_stable_key text not null,
  acted_by uuid not null references public.profiles (id),
  action_type text not null
    check (action_type in ('select', 'apply', 'custom')),
  resolution_text text not null
    check (char_length(resolution_text) between 1 and 5000),
  artifact_type public.plan_artifact_type,
  artifact_version integer check (artifact_version is null or artifact_version > 0),
  analysis_run_id uuid references public.analysis_runs (id) on delete set null,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

create index issue_actions_project_created_idx
  on public.issue_actions (workspace_id, project_id, created_at desc);

create index issue_actions_issue_created_idx
  on public.issue_actions (
    workspace_id,
    project_id,
    issue_stable_key,
    created_at desc
  );

alter table public.issue_actions enable row level security;

create policy "members can view issue actions"
  on public.issue_actions for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "members can create issue actions"
  on public.issue_actions for insert to authenticated
  with check (
    public.is_workspace_member(workspace_id)
    and acted_by = (select auth.uid())
  );

grant select, insert on public.issue_actions to authenticated;

comment on table public.issue_actions is
  'Durable Slice 6 resolution selections and governed artifact changes. Applying a resolution starts evidence-qualified re-analysis.';

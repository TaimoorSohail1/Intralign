create table public.artifact_drafts (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  artifact_type public.plan_artifact_type not null,
  source_snapshot_id uuid not null
    references public.assessment_snapshots (id) on delete cascade,
  content_json jsonb not null,
  version integer not null default 1 check (version > 0),
  provenance text not null default 'from_oslo'
    check (provenance in ('from_oslo', 'confirmed_by_user')),
  updated_by uuid not null references public.profiles (id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project_id, artifact_type)
);

create table public.artifact_draft_versions (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  artifact_type public.plan_artifact_type not null,
  artifact_draft_id uuid not null
    references public.artifact_drafts (id) on delete cascade,
  version integer not null check (version > 0),
  content_json jsonb not null,
  provenance text not null
    check (provenance in ('from_oslo', 'confirmed_by_user')),
  changed_by uuid not null references public.profiles (id),
  analysis_run_id uuid references public.analysis_runs (id) on delete set null,
  created_at timestamptz not null default now(),
  unique (artifact_draft_id, version)
);

create index artifact_drafts_workspace_project_idx
  on public.artifact_drafts (workspace_id, project_id);

create index artifact_draft_versions_project_created_idx
  on public.artifact_draft_versions (workspace_id, project_id, created_at desc);

alter table public.artifact_drafts enable row level security;
alter table public.artifact_draft_versions enable row level security;

create policy "members can view artifact drafts"
  on public.artifact_drafts for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "members can view artifact draft versions"
  on public.artifact_draft_versions for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "members can edit artifact drafts"
  on public.artifact_drafts for all to authenticated
  using (public.is_workspace_member(workspace_id))
  with check (public.is_workspace_member(workspace_id));

create policy "members can append artifact draft versions"
  on public.artifact_draft_versions for insert to authenticated
  with check (public.is_workspace_member(workspace_id));

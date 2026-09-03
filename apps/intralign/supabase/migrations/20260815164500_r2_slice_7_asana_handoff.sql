create table if not exists public.project_asana_handoffs (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  snapshot_id uuid not null references public.assessment_snapshots (id) on delete cascade,
  requested_by uuid not null references public.profiles (id),
  destination_gid text not null,
  state text not null default 'running' check (state in ('running', 'partial', 'completed', 'failed')),
  total_count integer not null default 0 check (total_count >= 0),
  completed_count integer not null default 0 check (completed_count >= 0),
  safe_error_code text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project_id, snapshot_id, destination_gid)
);

create table if not exists public.project_asana_handoff_items (
  id uuid primary key default gen_random_uuid(),
  handoff_id uuid not null references public.project_asana_handoffs (id) on delete cascade,
  item_key text not null,
  task_name text not null,
  external_task_gid text,
  external_permalink text,
  state text not null default 'pending' check (state in ('pending', 'completed', 'failed')),
  safe_error_code text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (handoff_id, item_key)
);

alter table public.project_asana_handoffs enable row level security;
alter table public.project_asana_handoff_items enable row level security;

create policy "members can view Asana handoffs"
  on public.project_asana_handoffs for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "editors can create Asana handoffs"
  on public.project_asana_handoffs for insert to authenticated
  with check (
    private.is_workspace_member(workspace_id)
    and requested_by = (select auth.uid())
  );
create policy "editors can update Asana handoffs"
  on public.project_asana_handoffs for update to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "members can view Asana handoff items"
  on public.project_asana_handoff_items for select to authenticated
  using (
    exists (
      select 1 from public.project_asana_handoffs handoff
      where handoff.id = handoff_id
        and private.is_workspace_member(handoff.workspace_id)
    )
  );
create policy "editors can manage Asana handoff items"
  on public.project_asana_handoff_items for all to authenticated
  using (
    exists (
      select 1 from public.project_asana_handoffs handoff
      where handoff.id = handoff_id
        and private.is_workspace_member(handoff.workspace_id)
    )
  )
  with check (
    exists (
      select 1 from public.project_asana_handoffs handoff
      where handoff.id = handoff_id
        and private.is_workspace_member(handoff.workspace_id)
    )
  );

grant select, insert, update on public.project_asana_handoffs to authenticated;
grant select, insert, update on public.project_asana_handoff_items to authenticated;

comment on table public.project_asana_handoffs is
  'Idempotent one-way Slice 7 imports of executable-plan fields into a configured Asana project.';
comment on table public.project_asana_handoff_items is
  'Per-item checkpoint records; no OAuth/PAT secret or OSLO assessment content is retained.';

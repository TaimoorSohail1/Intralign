alter table public.projects
  add column archived_at timestamptz,
  add column archived_by uuid references public.profiles (id) on delete set null;

create index projects_workspace_active_idx
  on public.projects (workspace_id, updated_at desc)
  where archived_at is null;

create index projects_archived_by_idx
  on public.projects (archived_by)
  where archived_by is not null;

create table public.workspace_member_preferences (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  theme text not null default 'system' check (theme in ('dark', 'light', 'system')),
  analysis_notifications boolean not null default true,
  failure_notifications boolean not null default true,
  stale_notifications boolean not null default true,
  updated_at timestamptz not null default now(),
  primary key (workspace_id, user_id)
);

create index workspace_member_preferences_user_idx
  on public.workspace_member_preferences (user_id);

create table public.workspace_notification_reads (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  notification_key text not null,
  read_at timestamptz not null default now(),
  primary key (workspace_id, user_id, notification_key)
);

create index workspace_notification_reads_user_idx
  on public.workspace_notification_reads (user_id);

alter table public.workspace_member_preferences enable row level security;
alter table public.workspace_notification_reads enable row level security;

create policy "members manage their workspace preferences"
  on public.workspace_member_preferences for all to authenticated
  using (
    user_id = (select auth.uid())
    and public.is_workspace_member(workspace_id)
  )
  with check (
    user_id = (select auth.uid())
    and public.is_workspace_member(workspace_id)
  );

create policy "members manage their notification reads"
  on public.workspace_notification_reads for all to authenticated
  using (
    user_id = (select auth.uid())
    and public.is_workspace_member(workspace_id)
  )
  with check (
    user_id = (select auth.uid())
    and public.is_workspace_member(workspace_id)
  );

grant select, insert, update on public.workspace_member_preferences to authenticated;
grant select, insert, update, delete on public.workspace_notification_reads to authenticated;

comment on column public.projects.archived_at is
  'Slice 8 non-destructive project archive marker. Archived projects retain all evidence, analysis, issues and history.';

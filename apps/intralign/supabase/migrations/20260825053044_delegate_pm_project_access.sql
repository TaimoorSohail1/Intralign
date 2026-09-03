begin;

lock table public.memberships in share row exclusive mode;
lock table public.invitations in share row exclusive mode;

alter table public.memberships alter column role drop default;
alter table public.invitations alter column role drop default;

alter type public.membership_role rename to membership_role_owner_only;
create type public.membership_role as enum ('owner', 'delegate_pm');

alter table public.memberships
  alter column role type public.membership_role
  using role::text::public.membership_role;
alter table public.invitations
  alter column role type public.membership_role
  using role::text::public.membership_role;

alter table public.memberships alter column role set default 'owner';
alter table public.invitations alter column role set default 'owner';

drop type public.membership_role_owner_only;

alter table public.memberships
  add constraint memberships_are_workspace_owners
  check (role = 'owner');

create unique index projects_workspace_id_id_idx
  on public.projects (workspace_id, id);

alter table public.invitations
  add column project_id uuid;

alter table public.invitations
  add constraint invitations_project_belongs_to_workspace
  foreign key (workspace_id, project_id)
  references public.projects (workspace_id, id)
  on delete cascade;

alter table public.invitations
  add constraint invitations_role_scope_consistent
  check (
    (role = 'owner' and project_id is null)
    or (role = 'delegate_pm' and project_id is not null)
  );

create table public.project_memberships (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null,
  user_id uuid not null references public.profiles (id) on delete cascade,
  role public.membership_role not null default 'delegate_pm',
  assigned_by uuid not null references public.profiles (id),
  orientation_seen_at timestamptz,
  created_at timestamptz not null default now(),
  primary key (project_id, user_id),
  constraint project_memberships_project_belongs_to_workspace
    foreign key (workspace_id, project_id)
    references public.projects (workspace_id, id)
    on delete cascade,
  constraint project_memberships_are_delegate_pm
    check (role = 'delegate_pm')
);

create index project_memberships_user_project_idx
  on public.project_memberships (user_id, project_id);
create index project_memberships_workspace_user_idx
  on public.project_memberships (workspace_id, user_id);

create or replace function private.is_project_member(target_project_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.projects project
    where project.id = target_project_id
      and (
        private.is_workspace_owner(project.workspace_id)
        or exists (
          select 1
          from public.project_memberships membership
          where membership.project_id = project.id
            and membership.user_id = (select auth.uid())
            and membership.role = 'delegate_pm'
        )
      )
  );
$$;

create or replace function private.can_edit_project(target_project_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select private.is_project_member(target_project_id);
$$;

revoke all on function private.is_project_member(uuid) from public, anon;
revoke all on function private.can_edit_project(uuid) from public, anon;
grant execute on function private.is_project_member(uuid) to authenticated;
grant execute on function private.can_edit_project(uuid) to authenticated;

alter table public.project_memberships enable row level security;

create policy "owners can view project memberships"
  on public.project_memberships for select to authenticated
  using (private.is_workspace_owner(workspace_id));

create policy "delegates can view their project memberships"
  on public.project_memberships for select to authenticated
  using (user_id = (select auth.uid()));

create policy "owners can manage project memberships"
  on public.project_memberships for all to authenticated
  using (private.is_workspace_owner(workspace_id))
  with check (private.is_workspace_owner(workspace_id));

create policy "delegates can view assigned workspaces"
  on public.workspaces for select to authenticated
  using (
    exists (
      select 1
      from public.project_memberships membership
      where membership.workspace_id = id
        and membership.user_id = (select auth.uid())
    )
  );

create policy "delegates can view assigned projects"
  on public.projects for select to authenticated
  using (private.is_project_member(id));

do $delegate_policies$
declare
  table_name text;
begin
  foreach table_name in array array[
    'intake_submissions',
    'source_documents',
    'source_fragments',
    'analysis_runs',
    'analysis_run_events',
    'assessment_snapshots',
    'artifact_versions',
    'issues',
    'issue_observations',
    'issue_answers',
    'document_parse_attempts',
    'artifact_drafts',
    'artifact_draft_versions',
    'issue_actions',
    'project_history_events',
    'project_comments',
    'project_share_links',
    'project_review_grants',
    'project_review_responses',
    'project_exports',
    'workspace_analysis_usage',
    'analysis_artifact_jobs',
    'project_report_drafts',
    'project_report_deliveries',
    'reanalysis_change_events',
    'project_read_freshness',
    'project_first_run_states',
    'read_moved_notifications',
    'issue_attestations',
    'issue_proposals',
    'issue_proposal_decisions',
    'project_outcomes',
    'project_snapshot_views',
    'project_report_schedules',
    'project_export_records',
    'project_asana_handoffs'
  ] loop
    if to_regclass(format('public.%I', table_name)) is not null then
      execute format(
        'create policy %I on public.%I for select to authenticated using (private.is_project_member(project_id))',
        'delegates can view assigned project rows',
        table_name
      );
    end if;
  end loop;
end;
$delegate_policies$;

create policy "delegates can edit assigned artifact drafts"
  on public.artifact_drafts for all to authenticated
  using (private.can_edit_project(project_id))
  with check (private.can_edit_project(project_id));

create policy "delegates can append assigned artifact versions"
  on public.artifact_draft_versions for insert to authenticated
  with check (private.can_edit_project(project_id));

create policy "delegates can add assigned issue answers"
  on public.issue_answers for insert to authenticated
  with check (private.can_edit_project(project_id));

create policy "delegates can add assigned issue actions"
  on public.issue_actions for insert to authenticated
  with check (private.can_edit_project(project_id));

create policy "delegates can add assigned project comments"
  on public.project_comments for insert to authenticated
  with check (
    private.can_edit_project(project_id)
    and author_id = (select auth.uid())
  );

create policy "delegates can manage assigned outcomes"
  on public.project_outcomes for all to authenticated
  using (private.can_edit_project(project_id))
  with check (private.can_edit_project(project_id));

create policy "delegates manage their assigned workspace preferences"
  on public.workspace_member_preferences for all to authenticated
  using (
    user_id = (select auth.uid())
    and exists (
      select 1
      from public.project_memberships membership
      where membership.workspace_id = workspace_member_preferences.workspace_id
        and membership.user_id = (select auth.uid())
    )
  )
  with check (
    user_id = (select auth.uid())
    and exists (
      select 1
      from public.project_memberships membership
      where membership.workspace_id = workspace_member_preferences.workspace_id
        and membership.user_id = (select auth.uid())
    )
  );

create policy "delegates manage their assigned notification reads"
  on public.workspace_notification_reads for all to authenticated
  using (
    user_id = (select auth.uid())
    and exists (
      select 1
      from public.project_memberships membership
      where membership.workspace_id = workspace_notification_reads.workspace_id
        and membership.user_id = (select auth.uid())
    )
  )
  with check (
    user_id = (select auth.uid())
    and exists (
      select 1
      from public.project_memberships membership
      where membership.workspace_id = workspace_notification_reads.workspace_id
        and membership.user_id = (select auth.uid())
    )
  );

grant select on public.project_memberships to authenticated;

comment on type public.membership_role is
  'Workspace owners and project-scoped Delegate-PMs. Delegate-PMs are assigned through project_memberships.';
comment on table public.project_memberships is
  'Project-scoped Delegate-PM assignments. Rows never grant access to other projects in the workspace.';
comment on column public.invitations.project_id is
  'Required for Delegate-PM invitations and null for workspace-owner invitations.';

commit;

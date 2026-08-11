create table public.project_report_drafts (
  project_id uuid primary key references public.projects (id) on delete cascade,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  snapshot_id uuid not null references public.assessment_snapshots (id) on delete cascade,
  content_json jsonb not null,
  updated_by uuid not null references public.profiles (id),
  updated_at timestamptz not null default now()
);

create table public.project_report_deliveries (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  snapshot_id uuid not null references public.assessment_snapshots (id) on delete cascade,
  requested_by uuid not null references public.profiles (id),
  recipient_email extensions.citext not null,
  recipient_label text not null check (char_length(trim(recipient_label)) between 1 and 120),
  subject text not null check (char_length(trim(subject)) between 1 and 200),
  content_json jsonb not null,
  status text not null check (status in ('scheduled', 'sending', 'sent', 'failed')),
  scheduled_for timestamptz not null,
  sent_at timestamptz,
  error_code text,
  created_at timestamptz not null default now()
);

create index project_report_deliveries_due_idx
  on public.project_report_deliveries (status, scheduled_for);

alter table public.project_report_drafts enable row level security;
alter table public.project_report_deliveries enable row level security;

create policy "members can view project report drafts"
  on public.project_report_drafts for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "editors can write project report drafts"
  on public.project_report_drafts for all to authenticated
  using (public.is_workspace_member(workspace_id))
  with check (
    public.is_workspace_member(workspace_id)
    and updated_by = (select auth.uid())
  );

create policy "members can view project report deliveries"
  on public.project_report_deliveries for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "editors can create project report deliveries"
  on public.project_report_deliveries for insert to authenticated
  with check (
    public.is_workspace_member(workspace_id)
    and requested_by = (select auth.uid())
  );

grant select, insert, update on public.project_report_drafts to authenticated;
grant select, insert on public.project_report_deliveries to authenticated;

comment on table public.project_report_drafts is
  'The shared, structured seven-section readout for the current retained project snapshot.';
comment on table public.project_report_deliveries is
  'Durable immediate and scheduled report email delivery records.';

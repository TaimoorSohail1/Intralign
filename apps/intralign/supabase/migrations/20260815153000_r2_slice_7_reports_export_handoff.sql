alter table public.project_report_drafts
  add column if not exists report_key text not null default 'executive-briefing'
    check (report_key = 'executive-briefing'),
  add column if not exists stage text not null default 'authored'
    check (stage in ('compose', 'authored')),
  add column if not exists recipient_class text not null default 'exec-sponsor'
    check (recipient_class in ('exec-sponsor', 'team', 'board')),
  add column if not exists composition_depth text not null default 'full'
    check (composition_depth in ('summary', 'full')),
  add column if not exists included_json jsonb not null default
    '{"integrity":true,"risks":true,"grounding":true,"moves":true}'::jsonb,
  add column if not exists source_analysis_run_id uuid references public.analysis_runs (id),
  add column if not exists read_signature text,
  add column if not exists revision integer not null default 1 check (revision > 0);

update public.project_report_drafts draft
set source_analysis_run_id = snapshot.analysis_run_id,
    read_signature = snapshot.analysis_run_id::text || ':' || draft.snapshot_id::text
from public.assessment_snapshots snapshot
where snapshot.id = draft.snapshot_id
  and (draft.source_analysis_run_id is null or draft.read_signature is null);

alter table public.project_report_deliveries
  add column if not exists report_key text not null default 'executive-briefing'
    check (report_key = 'executive-briefing'),
  add column if not exists report_version integer,
  add column if not exists source_analysis_run_id uuid references public.analysis_runs (id),
  add column if not exists analysis_completed_at timestamptz,
  add column if not exists read_signature text,
  add column if not exists content_checksum text,
  add column if not exists disclaimer_version text not null default 'r2-v1';

with versions as (
  select id, row_number() over (partition by project_id order by created_at, id)::integer as version
  from public.project_report_deliveries
)
update public.project_report_deliveries delivery
set report_version = versions.version
from versions
where versions.id = delivery.id and delivery.report_version is null;

update public.project_report_deliveries delivery
set source_analysis_run_id = snapshot.analysis_run_id,
    analysis_completed_at = snapshot.published_at,
    read_signature = snapshot.analysis_run_id::text || ':' || delivery.snapshot_id::text,
    content_checksum = encode(extensions.digest(delivery.content_json::text, 'sha256'), 'hex')
from public.assessment_snapshots snapshot
where snapshot.id = delivery.snapshot_id
  and (
    delivery.source_analysis_run_id is null
    or delivery.analysis_completed_at is null
    or delivery.read_signature is null
    or delivery.content_checksum is null
  );

alter table public.project_report_deliveries
  alter column report_version set not null,
  alter column source_analysis_run_id set not null,
  alter column analysis_completed_at set not null,
  alter column read_signature set not null,
  alter column content_checksum set not null;

create unique index if not exists project_report_deliveries_project_version_uidx
  on public.project_report_deliveries (project_id, report_version);

create or replace function public.protect_immutable_report_memo()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if new.project_id is distinct from old.project_id
     or new.workspace_id is distinct from old.workspace_id
     or new.snapshot_id is distinct from old.snapshot_id
     or new.source_analysis_run_id is distinct from old.source_analysis_run_id
     or new.analysis_completed_at is distinct from old.analysis_completed_at
     or new.read_signature is distinct from old.read_signature
     or new.report_version is distinct from old.report_version
     or new.recipient_email is distinct from old.recipient_email
     or new.recipient_label is distinct from old.recipient_label
     or new.subject is distinct from old.subject
     or new.content_json is distinct from old.content_json
     or new.content_checksum is distinct from old.content_checksum
     or new.disclaimer_version is distinct from old.disclaimer_version
  then
    raise exception 'A sent or scheduled report memo is immutable';
  end if;
  return new;
end;
$$;

drop trigger if exists protect_immutable_report_memo on public.project_report_deliveries;
create trigger protect_immutable_report_memo
before update on public.project_report_deliveries
for each row execute function public.protect_immutable_report_memo();

create table if not exists public.project_report_schedules (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  created_by uuid not null references public.profiles (id),
  recipient_email extensions.citext not null,
  recipient_class text not null check (recipient_class in ('exec-sponsor', 'team', 'board')),
  weekday smallint not null check (weekday between 0 and 6),
  local_time time not null,
  timezone text not null check (char_length(trim(timezone)) between 1 and 80),
  state text not null default 'enabled' check (state in ('enabled', 'paused')),
  next_run_at timestamptz not null,
  last_run_at timestamptz,
  last_delivery_id uuid references public.project_report_deliveries (id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists project_report_schedules_due_idx
  on public.project_report_schedules (state, next_run_at);

create table if not exists public.project_export_records (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  requested_by uuid not null references public.profiles (id),
  snapshot_id uuid not null references public.assessment_snapshots (id) on delete cascade,
  source_analysis_run_id uuid not null references public.analysis_runs (id),
  read_signature text not null,
  format text not null check (format in ('pdf', 'excel', 'csv', 'text', 'copy-summary', 'asana')),
  status text not null check (status in ('requested', 'completed', 'failed')),
  optimized_for text,
  content_checksum text,
  safe_error_code text,
  created_at timestamptz not null default now(),
  completed_at timestamptz
);

alter table public.project_report_schedules enable row level security;
alter table public.project_export_records enable row level security;

create policy "members can view report schedules"
  on public.project_report_schedules for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "editors can manage report schedules"
  on public.project_report_schedules for all to authenticated
  using (private.is_workspace_member(workspace_id))
  with check (
    private.is_workspace_member(workspace_id)
    and created_by = (select auth.uid())
  );
create policy "members can view project export records"
  on public.project_export_records for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "editors can create project export records"
  on public.project_export_records for insert to authenticated
  with check (
    private.is_workspace_member(workspace_id)
    and requested_by = (select auth.uid())
  );

grant select, insert, update, delete on public.project_report_schedules to authenticated;
grant select, insert on public.project_export_records to authenticated;

comment on column public.project_report_deliveries.content_checksum is
  'SHA-256 of the immutable structured memo body frozen for this version.';
comment on table public.project_report_schedules is
  'Basic-tier weekly Executive Briefing schedules; each run establishes current truth before freezing a memo.';
comment on table public.project_export_records is
  'Audit-only records for report and executable-plan exports; no raw file or connector token is stored.';

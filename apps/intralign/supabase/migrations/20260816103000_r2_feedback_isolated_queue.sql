-- Canonical R2 Slice 8 / Product feedback specification v1:
-- Alpha/Beta uses an in-house durable queue. The dedicated role is deliberately
-- denied canonical write grants; tracker routing and retention remain owner-TBD.

do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'feedback_service') then
    create role feedback_service nologin noinherit;
  end if;
end
$$;

do $$
begin
  grant feedback_service to postgres;
  if exists (select 1 from pg_roles where rolname = 'service_role') then
    grant feedback_service to service_role;
  end if;
end
$$;

create schema if not exists feedback_svc authorization postgres;
revoke all on schema feedback_svc from public;
revoke all on schema public from feedback_service;
revoke all on all tables in schema public from feedback_service;
revoke all on all sequences in schema public from feedback_service;

create sequence if not exists feedback_svc.defect_ticket_seq start with 1001;
create sequence if not exists feedback_svc.enhancement_ticket_seq start with 1001;
create sequence if not exists feedback_svc.note_ticket_seq start with 1001;

create table if not exists feedback_svc.tickets (
  id uuid primary key,
  ticket_id text not null unique,
  actor_user_id uuid not null,
  workspace_id uuid not null,
  session_id text not null check (session_id ~ '^[A-Za-z0-9_-]{8,128}$'),
  category text not null check (category in ('defect', 'enhancement', 'other')),
  title text not null check (char_length(title) between 1 and 80),
  body text not null check (char_length(body) between 1 and 4000),
  expected text check (expected is null or char_length(expected) <= 4000),
  impact text check (impact is null or impact in ('blocking', 'slowing', 'minor')),
  repro_context jsonb not null,
  status text not null default 'Filed' check (
    status in ('Filed', 'Triaged', 'Accepted', 'Duplicate', 'Won''t-fix', 'In-progress', 'Resolved', 'Closed')
  ),
  priority text,
  component text,
  tracker_ref text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (
    repro_context ?& array[
      'where', 'view', 'role', 'grounded_x', 'total_y', 'first_run_flag', 'ts'
    ]
    and not (repro_context ?| array['project_id', 'artifact', 'statement', 'figure', 'plan'])
  )
);

create index if not exists feedback_tickets_session_idx
  on feedback_svc.tickets (workspace_id, actor_user_id, session_id, created_at desc);

create table if not exists feedback_svc.events (
  id uuid primary key,
  workspace_id uuid not null,
  actor_user_id uuid not null,
  session_id text not null,
  event_name text not null check (event_name in ('feedback_filed')),
  ticket_id text not null,
  payload jsonb not null,
  occurred_at timestamptz not null default now(),
  check (not (payload ?| array['body', 'expected', 'free_text', 'plan_content']))
);

revoke all on all tables in schema feedback_svc from public;
revoke all on all sequences in schema feedback_svc from public;
grant usage on schema feedback_svc to feedback_service;
grant select, insert, update on feedback_svc.tickets to feedback_service;
grant select, insert on feedback_svc.events to feedback_service;
grant usage, select on sequence feedback_svc.defect_ticket_seq to feedback_service;
grant usage, select on sequence feedback_svc.enhancement_ticket_seq to feedback_service;
grant usage, select on sequence feedback_svc.note_ticket_seq to feedback_service;

comment on schema feedback_svc is
  'Isolated product-feedback queue. No grants to canonical plan, finding, attestation, or History tables.';
comment on table feedback_svc.tickets is
  'Sanitized Alpha/Beta feedback tickets; tracker delivery and retention are owner-TBD.';

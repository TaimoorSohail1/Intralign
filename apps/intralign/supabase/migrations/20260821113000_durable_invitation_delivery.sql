-- Durable invitation delivery outbox. The one-time activation URL is kept only
-- in the private schema while delivery is pending and is erased after the mail
-- provider accepts the message.

create schema if not exists private authorization postgres;

create table if not exists private.invitation_delivery_jobs (
  invitation_id uuid primary key references public.invitations(id) on delete cascade,
  workspace_id uuid not null references public.workspaces(id) on delete cascade,
  requested_by uuid not null,
  recipient_email text not null,
  workspace_name text not null,
  role_label text not null,
  activation_url text,
  expires_at timestamptz not null,
  status text not null default 'queued'
    check (status in ('queued', 'running', 'delivered', 'failed', 'cancelled')),
  attempts integer not null default 0 check (attempts >= 0),
  max_attempts integer not null default 5 check (max_attempts between 1 and 20),
  available_at timestamptz not null default now(),
  locked_at timestamptz,
  locked_by text,
  last_error text,
  provider_accepted_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (status not in ('delivered', 'cancelled') or activation_url is null)
);

create index if not exists invitation_delivery_jobs_ready_idx
  on private.invitation_delivery_jobs (available_at, created_at)
  where status in ('queued', 'running');

revoke all on table private.invitation_delivery_jobs from public;
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'anon') then
    revoke all on table private.invitation_delivery_jobs from anon;
  end if;
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    revoke all on table private.invitation_delivery_jobs from authenticated;
  end if;
end
$$;

comment on table private.invitation_delivery_jobs is
  'Private invitation-email outbox with leases, bounded retry and post-acceptance token erasure.';

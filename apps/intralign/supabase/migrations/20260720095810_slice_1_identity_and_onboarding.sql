create extension if not exists citext with schema extensions;
create extension if not exists pgcrypto with schema extensions;

create type public.membership_role as enum ('owner', 'collaborator', 'viewer');
create type public.invitation_status as enum ('pending', 'accepted', 'revoked');
create type public.project_status as enum ('draft', 'active', 'archived');

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text not null check (char_length(trim(display_name)) between 1 and 120),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.workspaces (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(trim(name)) between 1 and 120),
  created_by uuid not null references public.profiles (id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.memberships (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  role public.membership_role not null default 'collaborator',
  welcome_seen_at timestamptz,
  created_at timestamptz not null default now(),
  primary key (workspace_id, user_id)
);

create table public.invitations (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  email extensions.citext not null,
  role public.membership_role not null default 'collaborator',
  token_hash bytea not null unique,
  status public.invitation_status not null default 'pending',
  invited_by uuid not null references public.profiles (id),
  accepted_by uuid references public.profiles (id),
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  accepted_at timestamptz,
  revoked_at timestamptz,
  constraint invitations_expire_after_creation check (expires_at > created_at),
  constraint invitations_acceptance_consistent check (
    (status = 'accepted' and accepted_by is not null and accepted_at is not null)
    or (status <> 'accepted' and accepted_by is null and accepted_at is null)
  ),
  constraint invitations_revocation_consistent check (
    (status = 'revoked' and revoked_at is not null)
    or (status <> 'revoked' and revoked_at is null)
  )
);

create unique index one_pending_invitation_per_workspace_email
  on public.invitations (workspace_id, email)
  where status = 'pending';
create index invitations_workspace_created_idx
  on public.invitations (workspace_id, created_at desc);

create table public.projects (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  name text not null check (char_length(trim(name)) between 1 and 160),
  status public.project_status not null default 'draft',
  created_by uuid not null references public.profiles (id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index projects_workspace_created_idx
  on public.projects (workspace_id, created_at desc);

create table public.audit_events (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  actor_user_id uuid references public.profiles (id),
  action text not null check (char_length(action) between 1 and 100),
  subject_type text not null check (char_length(subject_type) between 1 and 100),
  subject_id text not null,
  metadata jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);

create index audit_events_workspace_occurred_idx
  on public.audit_events (workspace_id, occurred_at desc);

create or replace function public.is_workspace_member(target_workspace_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.memberships membership
    where membership.workspace_id = target_workspace_id
      and membership.user_id = (select auth.uid())
  );
$$;

create or replace function public.is_workspace_owner(target_workspace_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.memberships membership
    where membership.workspace_id = target_workspace_id
      and membership.user_id = (select auth.uid())
      and membership.role = 'owner'
  );
$$;

revoke all on function public.is_workspace_member(uuid) from public;
revoke all on function public.is_workspace_owner(uuid) from public;
grant execute on function public.is_workspace_member(uuid) to authenticated;
grant execute on function public.is_workspace_owner(uuid) to authenticated;

alter table public.profiles enable row level security;
alter table public.workspaces enable row level security;
alter table public.memberships enable row level security;
alter table public.invitations enable row level security;
alter table public.projects enable row level security;
alter table public.audit_events enable row level security;

create policy "profiles are visible to their owner"
  on public.profiles for select to authenticated
  using (id = (select auth.uid()));

create policy "members can view their workspaces"
  on public.workspaces for select to authenticated
  using (public.is_workspace_member(id));

create policy "members can view workspace memberships"
  on public.memberships for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "owners can view workspace invitations"
  on public.invitations for select to authenticated
  using (public.is_workspace_owner(workspace_id));

create policy "members can view workspace projects"
  on public.projects for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "owners can view workspace audit events"
  on public.audit_events for select to authenticated
  using (public.is_workspace_owner(workspace_id));

grant usage on schema public to authenticated;
grant select on public.profiles, public.workspaces, public.memberships,
  public.invitations, public.projects, public.audit_events to authenticated;

comment on column public.invitations.token_hash is
  'SHA-256 digest only. Raw bearer invitation tokens must never be persisted.';

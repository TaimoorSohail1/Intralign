create table public.workspace_subscriptions (
  workspace_id uuid primary key references public.workspaces (id) on delete cascade,
  plan_code text not null default 'free' check (plan_code in ('free', 'basic')),
  status text not null default 'active' check (status in ('active', 'cancelled')),
  changed_by uuid references public.profiles (id) on delete set null,
  started_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.workspace_analysis_usage (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  usage_kind text not null default 'user_requested_analysis'
    check (usage_kind in ('user_requested_analysis')),
  period_start date not null default date_trunc('month', now())::date,
  occurred_at timestamptz not null default now(),
  unique (analysis_run_id)
);

create index workspace_analysis_usage_period_idx
  on public.workspace_analysis_usage (workspace_id, period_start, occurred_at);

create table public.workspace_limit_events (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  actor_user_id uuid references public.profiles (id) on delete set null,
  project_id uuid references public.projects (id) on delete set null,
  limit_kind text not null check (
    limit_kind in (
      'active_projects',
      'documents',
      'words',
      'collaborator_seats',
      'monthly_invitations',
      'monthly_analyses'
    )
  ),
  outcome text not null check (outcome in ('allowed', 'partial', 'blocked')),
  details jsonb not null default '{}'::jsonb,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

create index workspace_limit_events_created_idx
  on public.workspace_limit_events (workspace_id, created_at desc);

alter table public.analysis_runs
  add column consumes_analysis_allowance boolean not null default false;

alter table public.workspace_subscriptions enable row level security;
alter table public.workspace_analysis_usage enable row level security;
alter table public.workspace_limit_events enable row level security;

create policy "members can view workspace subscription"
  on public.workspace_subscriptions for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "owners can manage workspace subscription"
  on public.workspace_subscriptions for all to authenticated
  using (public.is_workspace_owner(workspace_id))
  with check (public.is_workspace_owner(workspace_id));

create policy "members can view analysis usage"
  on public.workspace_analysis_usage for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "members can view workspace limit events"
  on public.workspace_limit_events for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select, insert, update on public.workspace_subscriptions to authenticated;
grant select on public.workspace_analysis_usage to authenticated;
grant select on public.workspace_limit_events to authenticated;

comment on table public.workspace_subscriptions is
  'Slice 10 workspace plan state. Plan changes are simulated in Alpha and never collect payment.';
comment on table public.workspace_analysis_usage is
  'Successful user-requested analysis runs only. Failed and automatic runs do not consume allowance.';
comment on table public.workspace_limit_events is
  'Idempotent audit evidence for every server-side plan capacity decision.';
comment on column public.analysis_runs.consumes_analysis_allowance is
  'True only for a user-requested run that should consume allowance after successful publication.';

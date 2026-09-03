alter table public.workspace_subscriptions
  drop constraint if exists workspace_subscriptions_status_check;

alter table public.workspace_subscriptions
  add column if not exists provider_customer_id text,
  add column if not exists provider_subscription_id text,
  add column if not exists cancel_at_period_end boolean not null default false,
  add column if not exists current_period_end timestamptz,
  add column if not exists grace_ends_at timestamptz,
  add constraint workspace_subscriptions_status_check
    check (status in ('active', 'past_due', 'cancelled'));

create unique index if not exists workspace_subscriptions_customer_idx
  on public.workspace_subscriptions (provider_customer_id)
  where provider_customer_id is not null;

create unique index if not exists workspace_subscriptions_provider_subscription_idx
  on public.workspace_subscriptions (provider_subscription_id)
  where provider_subscription_id is not null;

create table public.project_outcomes (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  title text not null check (char_length(btrim(title)) between 1 and 240),
  status text not null default 'active' check (status in ('active', 'archived')),
  is_primary boolean not null default false,
  provenance text not null check (provenance in ('declared', 'inferred')),
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  archived_at timestamptz,
  unique (workspace_id, project_id, id)
);

create unique index project_outcomes_one_primary_idx
  on public.project_outcomes (project_id)
  where is_primary;

create index project_outcomes_active_workspace_idx
  on public.project_outcomes (workspace_id, status, created_at);

create table public.billing_checkout_sessions (
  id text primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  actor_user_id uuid references public.profiles (id) on delete set null,
  plan_code text not null default 'basic' check (plan_code in ('basic')),
  billing_interval text not null check (billing_interval in ('monthly', 'annual')),
  price_usd integer not null check (price_usd > 0),
  status text not null default 'pending'
    check (status in ('pending', 'committed', 'expired')),
  created_at timestamptz not null default now(),
  committed_at timestamptz
);

create index billing_checkout_sessions_workspace_idx
  on public.billing_checkout_sessions (workspace_id, created_at desc);

create table public.billing_webhook_events (
  event_id text primary key,
  event_type text not null,
  received_at timestamptz not null default now()
);

create table public.commitment_logs (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  checkout_session_id text not null references public.billing_checkout_sessions (id),
  provider_event_id text not null references public.billing_webhook_events (event_id),
  plan_code text not null check (plan_code in ('basic')),
  billing_interval text not null check (billing_interval in ('monthly', 'annual')),
  price_usd integer not null check (price_usd > 0),
  committed_at timestamptz not null default now(),
  unique (checkout_session_id),
  unique (provider_event_id)
);

create table public.intent_signals (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  actor_user_id uuid references public.profiles (id) on delete set null,
  wall_key text not null
    check (wall_key in ('multiOutcome', 'multiPlan', 'envelope', 'schedule')),
  tier_mapped text not null default 'basic' check (tier_mapped in ('basic')),
  chosen_path text not null
    check (chosen_path in ('committed', 'free_path', 'declined', 'keep_both')),
  full_option_set jsonb not null default '[]'::jsonb,
  context jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);

create index intent_signals_workspace_idx
  on public.intent_signals (workspace_id, occurred_at desc);

alter table public.workspace_limit_events
  drop constraint if exists workspace_limit_events_limit_kind_check;

alter table public.workspace_limit_events
  add constraint workspace_limit_events_limit_kind_check check (
    limit_kind in (
      'active_projects',
      'active_outcomes',
      'documents',
      'words',
      'intake_words',
      'collaborator_seats',
      'monthly_invitations',
      'monthly_analyses'
    )
  );

alter table public.project_outcomes enable row level security;
alter table public.billing_checkout_sessions enable row level security;
alter table public.billing_webhook_events enable row level security;
alter table public.commitment_logs enable row level security;
alter table public.intent_signals enable row level security;

create policy "members can view project outcomes"
  on public.project_outcomes for select to authenticated
  using (private.is_workspace_member(workspace_id));

create policy "members can manage project outcomes"
  on public.project_outcomes for all to authenticated
  using (private.is_workspace_member(workspace_id))
  with check (private.is_workspace_member(workspace_id));

create policy "owners can view checkout sessions"
  on public.billing_checkout_sessions for select to authenticated
  using (private.is_workspace_owner(workspace_id));

create policy "owners can view commitment logs"
  on public.commitment_logs for select to authenticated
  using (private.is_workspace_owner(workspace_id));

create policy "members can view intent signals"
  on public.intent_signals for select to authenticated
  using (private.is_workspace_member(workspace_id));

grant select, insert, update on public.project_outcomes to authenticated;
grant select on public.billing_checkout_sessions to authenticated;
grant select on public.commitment_logs to authenticated;
grant select on public.intent_signals to authenticated;

comment on table public.project_outcomes is
  'R2 Slice 4 first-class Outcome records. Archive is reversible and never deletes the record.';
comment on table public.billing_checkout_sessions is
  'Server-created hosted Checkout attempts. Pending rows never grant an entitlement.';
comment on table public.billing_webhook_events is
  'Idempotency ledger for signature-verified billing-provider events.';
comment on table public.commitment_logs is
  'Durable proof of a real paid commitment preceding a Basic entitlement grant.';
comment on table public.intent_signals is
  'Durable branch-level demand signals for every Slice 4 capacity wall path.';
comment on table public.workspace_subscriptions is
  'Workspace entitlement state granted only through verified billing events or explicit owner operations.';

create type public.analysis_pass_kind as enum ('fast', 'deep');
create type public.reanalysis_trigger as enum (
  'intake', 'batch', 'explicit', 'deep_supersede'
);
create type public.read_freshness_state as enum (
  'fresh', 'stale', 'reanalyzing'
);

alter table public.analysis_runs
  add column pass_kind public.analysis_pass_kind not null default 'fast',
  add column reanalysis_trigger public.reanalysis_trigger not null default 'intake',
  add column consolidated_event_ids jsonb not null default '[]'::jsonb,
  add column provisional boolean not null default false,
  add column auto_retry_count integer not null default 0
    check (auto_retry_count between 0 and 1);

update public.analysis_runs
set reanalysis_trigger = case
  when kind = 'initial' then 'intake'::public.reanalysis_trigger
  else 'batch'::public.reanalysis_trigger
end;

create table public.reanalysis_change_events (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  actor_user_id uuid not null references public.profiles (id),
  event_key text not null,
  change_kind text not null check (change_kind in (
    'confirm', 'flag', 'route', 'apply_fix', 'answer_clarify',
    'edit', 'add_checkpoint', 'explicit'
  )),
  scope text not null,
  evidence_json jsonb not null default '{}'::jsonb,
  requires_deep_pass boolean not null default false,
  state text not null default 'pending'
    check (state in ('pending', 'consumed', 'withdrawn')),
  analysis_run_id uuid references public.analysis_runs (id) on delete set null,
  grounding_counted_at timestamptz,
  created_at timestamptz not null default now(),
  consumed_at timestamptz,
  withdrawn_at timestamptz,
  unique (workspace_id, event_key)
);

create index reanalysis_change_events_pending_idx
  on public.reanalysis_change_events (project_id, created_at)
  where state = 'pending';

create table public.project_read_freshness (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid primary key references public.projects (id) on delete cascade,
  state public.read_freshness_state not null default 'fresh',
  pending_count integer not null default 0 check (pending_count >= 0),
  based_on_run_id uuid references public.analysis_runs (id) on delete set null,
  active_run_id uuid references public.analysis_runs (id) on delete set null,
  last_act_at timestamptz,
  last_landed_at timestamptz,
  updated_at timestamptz not null default now()
);

insert into public.project_read_freshness (
  workspace_id, project_id, state, pending_count, based_on_run_id,
  last_landed_at
)
select project.workspace_id, project.id, 'fresh', 0,
       project.current_analysis_run_id, now()
from public.projects project
on conflict (project_id) do nothing;

create table public.project_first_run_states (
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  first_run boolean not null default true,
  onboarded boolean not null default false,
  grounding_act_count integer not null default 0 check (grounding_act_count >= 0),
  ever_unlocked boolean not null default false,
  unlock_threshold integer not null default 2 check (unlock_threshold between 1 and 10),
  activation_event_id uuid,
  updated_at timestamptz not null default now(),
  primary key (project_id, user_id)
);

-- Existing R1 projects must not replay the R2 first-run gate.
insert into public.project_first_run_states (
  workspace_id, project_id, user_id, first_run, onboarded,
  grounding_act_count, ever_unlocked, unlock_threshold
)
select project.workspace_id, project.id, membership.user_id,
       false, true, 2, true, 2
from public.projects project
join public.memberships membership
  on membership.workspace_id = project.workspace_id
on conflict (project_id, user_id) do nothing;

create table public.read_moved_notifications (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  analysis_run_id uuid not null references public.analysis_runs (id) on delete cascade,
  pillar_deltas jsonb not null default '[]'::jsonb,
  settled_causes jsonb not null default '[]'::jsonb,
  previous_band text,
  current_band text,
  delivery_kind text not null check (delivery_kind in ('transient', 'durable')),
  seen_at timestamptz,
  expires_at timestamptz,
  created_at timestamptz not null default now()
);

create index read_moved_notifications_unseen_idx
  on public.read_moved_notifications (user_id, project_id, created_at desc)
  where seen_at is null and delivery_kind = 'durable';

alter table public.reanalysis_change_events enable row level security;
alter table public.project_read_freshness enable row level security;
alter table public.project_first_run_states enable row level security;
alter table public.read_moved_notifications enable row level security;

create policy "members can view reanalysis changes"
  on public.reanalysis_change_events for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "members can view read freshness"
  on public.project_read_freshness for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "users can view their first-run state"
  on public.project_first_run_states for select to authenticated
  using (user_id = auth.uid() and private.is_workspace_member(workspace_id));
create policy "users can view their read-moved notifications"
  on public.read_moved_notifications for select to authenticated
  using (user_id = auth.uid() and private.is_workspace_member(workspace_id));

grant select on public.reanalysis_change_events, public.project_read_freshness,
  public.project_first_run_states, public.read_moved_notifications to authenticated;

comment on table public.reanalysis_change_events is
  'Append-only plan-affecting changes. Acts address items; only a landed analysis pass resolves the read.';
comment on table public.project_read_freshness is
  'Honest project-level FRESH/STALE/REANALYZING projection retaining the last-good run.';
comment on table public.project_first_run_states is
  'Per-user, per-project presentation gate. ever_unlocked is monotonic and never withholds the read API.';
comment on table public.read_moved_notifications is
  'Causal notification projection created from a landed pass, never from a manual act.';

create type public.issue_attestation_act as enum (
  'confirm', 'answer', 'flag', 'fix', 'ground', 'route', 'withdraw'
);

create type public.issue_attestation_basis as enum (
  'documented', 'vendor-or-owner-verified', 'verified-directly', 'answered'
);

alter table public.issues drop constraint issues_current_status_check;
alter table public.issues
  add constraint issues_current_status_check check (current_status in (
    'open', 'addressed', 'routed', 'needs_fix', 'needs_grounding', 'resolved'
  ));

alter table public.issue_observations drop constraint issue_observations_status_check;
alter table public.issue_observations
  add constraint issue_observations_status_check check (status in (
    'open', 'addressed', 'routed', 'needs_fix', 'needs_grounding', 'resolved'
  ));

alter table public.reanalysis_change_events
  drop constraint reanalysis_change_events_change_kind_check;
alter table public.reanalysis_change_events
  add constraint reanalysis_change_events_change_kind_check check (change_kind in (
    'confirm', 'flag', 'route', 'apply_fix', 'answer_clarify',
    'edit', 'add_checkpoint', 'explicit', 'ground', 'withdraw', 'proposal'
  ));

create table public.issue_attestations (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null,
  project_id uuid not null,
  issue_stable_key text not null,
  act public.issue_attestation_act not null,
  actor_user_id uuid not null,
  attributed_to jsonb not null,
  basis public.issue_attestation_basis,
  evidence_ref text,
  plan_change_ref text,
  routed_to jsonb,
  supersedes uuid references public.issue_attestations (id),
  analysis_run_id uuid,
  idempotency_key text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key),
  check (
    act not in ('confirm', 'answer', 'ground')
    or basis is not null
  ),
  check (act <> 'fix' or plan_change_ref is not null),
  check (act <> 'route' or routed_to is not null),
  check (act <> 'withdraw' or supersedes is not null)
);

create index issue_attestations_issue_created_idx
  on public.issue_attestations (
    workspace_id, project_id, issue_stable_key, created_at desc
  );
create index issue_attestations_run_idx
  on public.issue_attestations (analysis_run_id)
  where analysis_run_id is not null;

create trigger issue_attestations_append_only
  before update or delete on public.issue_attestations
  for each statement execute function public.enforce_append_only();

create type public.issue_proposal_kind as enum ('build', 'inference', 'optional');
create type public.issue_proposal_surface as enum (
  'issue_card', 'artifact', 'folded_read'
);

create table public.issue_proposals (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_stable_key text not null,
  stable_key text not null,
  kind public.issue_proposal_kind not null,
  resolver_key text not null,
  title text not null,
  rationale text not null,
  artifact_type public.plan_artifact_type,
  load_bearing boolean not null default false,
  created_by_run_id uuid references public.analysis_runs (id) on delete set null,
  created_at timestamptz not null default now(),
  unique (project_id, stable_key)
);

create table public.issue_proposal_decisions (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null,
  project_id uuid not null,
  proposal_id uuid not null,
  accepted boolean not null,
  actor_user_id uuid not null,
  surface public.issue_proposal_surface not null,
  analysis_run_id uuid,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

insert into public.issue_proposals (
  workspace_id, project_id, issue_stable_key, stable_key, kind,
  resolver_key, title, rationale, artifact_type, load_bearing,
  created_by_run_id
)
select observation.workspace_id, observation.project_id,
       issue.stable_key, 'build:' || issue.stable_key || ':primary', 'build',
       observation.artifact_type::text || ':primary',
       coalesce(nullif(observation.observation_json ->> 'recommendation', ''),
                'Address ' || (observation.observation_json ->> 'title')),
       coalesce(nullif(observation.observation_json ->> 'why', ''),
                'This finding needs a governed structural change.'),
       observation.artifact_type,
       observation.severity in ('Critical', 'Moderate'),
       observation.analysis_run_id
from public.issues issue
join lateral (
  select candidate.*
  from public.issue_observations candidate
  where candidate.issue_id = issue.id
  order by candidate.observed_at desc
  limit 1
) observation on true
on conflict (project_id, stable_key) do nothing;

create index issue_proposals_finding_idx
  on public.issue_proposals (workspace_id, project_id, issue_stable_key, created_at);
create index issue_proposal_decisions_proposal_idx
  on public.issue_proposal_decisions (proposal_id, created_at desc);

create trigger issue_proposal_decisions_append_only
  before update or delete on public.issue_proposal_decisions
  for each statement execute function public.enforce_append_only();

alter table public.issue_attestations enable row level security;
alter table public.issue_proposals enable row level security;
alter table public.issue_proposal_decisions enable row level security;

create policy "members can view issue attestations"
  on public.issue_attestations for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "members can view issue proposals"
  on public.issue_proposals for select to authenticated
  using (private.is_workspace_member(workspace_id));
create policy "members can view issue proposal decisions"
  on public.issue_proposal_decisions for select to authenticated
  using (private.is_workspace_member(workspace_id));

grant select on public.issue_attestations, public.issue_proposals,
  public.issue_proposal_decisions to authenticated;

comment on table public.issue_attestations is
  'R2 Slice 2 append-only issue-act ledger. A manual act enqueues; only landed reanalysis changes a resolution state.';
comment on table public.issue_proposals is
  'DL-211 itemized proposal resolvers shared across issue-card, artifact, and folded-read surfaces.';
comment on table public.issue_proposal_decisions is
  'Append-only cross-surface proposal decisions. Inference and optional decisions never ground a finding.';

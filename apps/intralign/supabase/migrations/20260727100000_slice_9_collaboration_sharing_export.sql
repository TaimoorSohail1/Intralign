create type public.review_response_kind as enum (
  'comment',
  'approve',
  'reject',
  'suggest_alternative'
);

create table public.project_comments (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_stable_key text not null check (char_length(issue_stable_key) between 1 and 240),
  author_id uuid not null references public.profiles (id),
  body text not null check (char_length(trim(body)) between 1 and 5000),
  mentions jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create index project_comments_issue_created_idx
  on public.project_comments (project_id, issue_stable_key, created_at);

create table public.project_share_links (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  snapshot_id uuid references public.assessment_snapshots (id) on delete cascade,
  token_hash bytea not null unique,
  created_by uuid not null references public.profiles (id),
  expires_at timestamptz not null,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check (expires_at > created_at)
);

create index project_share_links_project_created_idx
  on public.project_share_links (project_id, created_at desc);

create table public.project_review_grants (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_stable_key text,
  reviewer_name text not null check (char_length(trim(reviewer_name)) between 1 and 120),
  reviewer_email extensions.citext,
  token_hash bytea not null unique,
  created_by uuid not null references public.profiles (id),
  expires_at timestamptz not null,
  resolved_at timestamptz,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check (expires_at > created_at)
);

create index project_review_grants_project_created_idx
  on public.project_review_grants (project_id, created_at desc);

create table public.project_review_responses (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  review_grant_id uuid not null references public.project_review_grants (id) on delete cascade,
  issue_stable_key text,
  response_kind public.review_response_kind not null,
  body text not null check (char_length(trim(body)) between 1 and 5000),
  analysis_run_id uuid references public.analysis_runs (id) on delete set null,
  created_at timestamptz not null default now(),
  unique (review_grant_id)
);

create index project_review_responses_project_created_idx
  on public.project_review_responses (project_id, created_at desc);

create table public.project_exports (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  snapshot_id uuid references public.assessment_snapshots (id) on delete set null,
  exported_by uuid not null references public.profiles (id),
  format text not null check (format in ('pdf')),
  created_at timestamptz not null default now()
);

alter table public.project_comments enable row level security;
alter table public.project_share_links enable row level security;
alter table public.project_review_grants enable row level security;
alter table public.project_review_responses enable row level security;
alter table public.project_exports enable row level security;

create policy "members can view project comments"
  on public.project_comments for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can add project comments"
  on public.project_comments for insert to authenticated
  with check (
    public.is_workspace_member(workspace_id)
    and author_id = (select auth.uid())
  );

create policy "members can view project share links"
  on public.project_share_links for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can manage project share links"
  on public.project_share_links for all to authenticated
  using (public.is_workspace_member(workspace_id))
  with check (
    public.is_workspace_member(workspace_id)
    and created_by = (select auth.uid())
  );

create policy "members can view project review grants"
  on public.project_review_grants for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can manage project review grants"
  on public.project_review_grants for all to authenticated
  using (public.is_workspace_member(workspace_id))
  with check (
    public.is_workspace_member(workspace_id)
    and created_by = (select auth.uid())
  );

create policy "members can view project review responses"
  on public.project_review_responses for select to authenticated
  using (public.is_workspace_member(workspace_id));

create policy "members can view project exports"
  on public.project_exports for select to authenticated
  using (public.is_workspace_member(workspace_id));
create policy "members can add project exports"
  on public.project_exports for insert to authenticated
  with check (
    public.is_workspace_member(workspace_id)
    and exported_by = (select auth.uid())
  );

grant select, insert on public.project_comments to authenticated;
grant select, insert, update, delete on public.project_share_links to authenticated;
grant select, insert, update, delete on public.project_review_grants to authenticated;
grant select on public.project_review_responses to authenticated;
grant select, insert on public.project_exports to authenticated;

comment on column public.project_share_links.token_hash is
  'SHA-256 digest only. Raw snapshot bearer tokens must never be persisted.';
comment on column public.project_review_grants.token_hash is
  'SHA-256 digest only. Raw reviewer bearer tokens must never be persisted.';

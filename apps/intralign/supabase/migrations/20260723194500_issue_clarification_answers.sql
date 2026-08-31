create table public.issue_answers (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  issue_stable_key text not null,
  answered_by uuid not null references public.profiles (id),
  answer text not null check (char_length(answer) between 1 and 5000),
  idempotency_key text not null,
  analysis_run_id uuid references public.analysis_runs (id) on delete set null,
  created_at timestamptz not null default now(),
  unique (workspace_id, idempotency_key)
);

create index issue_answers_project_created_idx
  on public.issue_answers (workspace_id, project_id, created_at desc);

alter table public.issue_answers enable row level security;

create policy "members can view issue answers"
  on public.issue_answers for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select on public.issue_answers to authenticated;

comment on table public.issue_answers is
  'Durable user clarifications. Each answer starts an evidence-qualified re-analysis run.';

create table if not exists public.analysis_jobs (
  analysis_run_id uuid primary key references public.analysis_runs(id) on delete cascade,
  status text not null default 'queued'
    check (status in ('queued', 'running', 'completed')),
  attempts integer not null default 0 check (attempts >= 0),
  available_at timestamptz not null default now(),
  locked_at timestamptz,
  locked_by text,
  last_error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists analysis_jobs_claim_idx
  on public.analysis_jobs (status, available_at, updated_at);

alter table public.analysis_jobs enable row level security;

comment on table public.analysis_jobs is
  'Internal durable queue for analysis-run workers. Server database roles only; no Data API policies.';

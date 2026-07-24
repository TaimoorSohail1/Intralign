alter table public.source_documents
  add column parse_attempt_count integer not null default 0
    check (parse_attempt_count >= 0),
  add column last_attempt_at timestamptz,
  add column parsed_at timestamptz,
  add column ocr_used boolean not null default false,
  add column locator_schema_version text not null default 'source-locator-v2';

create table public.document_parse_attempts (
  id bigint generated always as identity primary key,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  source_document_id uuid not null
    references public.source_documents (id) on delete cascade,
  attempt_no integer not null check (attempt_no > 0),
  status text not null check (status in ('running', 'completed', 'failed')),
  error_code text,
  retryable boolean not null default false,
  parser_version text not null,
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  unique (source_document_id, attempt_no)
);

create index document_parse_attempts_document_idx
  on public.document_parse_attempts (source_document_id, attempt_no);

alter table public.document_parse_attempts enable row level security;

create policy "members can view document parse attempts"
  on public.document_parse_attempts for select to authenticated
  using (public.is_workspace_member(workspace_id));

grant select on public.document_parse_attempts to authenticated;

comment on table public.document_parse_attempts is
  'Durable document parsing history. Error codes are safe; raw source content is excluded.';

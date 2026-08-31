alter table public.analysis_runs
  add column source_document_ids jsonb not null default '[]'::jsonb;

comment on column public.analysis_runs.source_document_ids is
  'Immutable source document identifiers selected for this analysis run.';

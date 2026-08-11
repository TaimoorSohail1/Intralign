alter table public.analysis_runs
  add column if not exists user_evidence jsonb not null default '[]'::jsonb;

alter table public.artifact_drafts
  drop constraint if exists artifact_drafts_provenance_check;

alter table public.artifact_drafts
  add constraint artifact_drafts_provenance_check
  check (provenance in ('from_oslo', 'confirmed_by_user', 'mixed'));

alter table public.artifact_draft_versions
  drop constraint if exists artifact_draft_versions_provenance_check;

alter table public.artifact_draft_versions
  add constraint artifact_draft_versions_provenance_check
  check (provenance in ('from_oslo', 'confirmed_by_user', 'mixed'));

comment on column public.analysis_runs.user_evidence is
  'Structured user-confirmed evidence supplied separately from prompt-control text.';

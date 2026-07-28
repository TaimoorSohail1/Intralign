alter table public.artifact_versions
  add column if not exists content_json jsonb not null
    default '{"sections":[]}'::jsonb,
  add column if not exists assumptions_json jsonb not null default '[]'::jsonb,
  add column if not exists conflicts_json jsonb not null default '[]'::jsonb,
  add column if not exists revision integer;

with ranked as (
  select
    id,
    row_number() over (
      partition by project_id, artifact_type
      order by created_at, id
    ) as revision
  from public.artifact_versions
)
update public.artifact_versions as versions
set revision = ranked.revision
from ranked
where versions.id = ranked.id
  and versions.revision is null;

alter table public.artifact_versions
  alter column revision set not null;

create unique index if not exists artifact_versions_project_type_revision_idx
  on public.artifact_versions (project_id, artifact_type, revision);

create index if not exists artifact_versions_current_run_idx
  on public.artifact_versions (project_id, analysis_run_id, artifact_type);

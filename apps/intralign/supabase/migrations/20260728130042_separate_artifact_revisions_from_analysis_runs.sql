-- A material artifact revision can be observed by more than one analysis run.
-- Keep the run/type uniqueness while allowing the same revision number to be
-- retained across those observations.
drop index if exists public.artifact_versions_project_type_revision_idx;

create index if not exists artifact_versions_project_type_revision_idx
  on public.artifact_versions (project_id, artifact_type, revision);

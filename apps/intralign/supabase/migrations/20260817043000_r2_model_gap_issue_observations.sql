-- DL-210: model-gap findings are explicitly unassessed. They have no CAF
-- dimension tag and must not be default-classified merely to fit storage.

alter table public.issue_observations
  alter column dimension drop not null;

comment on column public.issue_observations.dimension is
  'Derived CAF/pillar dimension; null only for an unassessed model-gap escalation.';

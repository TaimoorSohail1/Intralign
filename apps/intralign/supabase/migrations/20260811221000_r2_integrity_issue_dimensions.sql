-- R2 Slice 1: Grounding and Adaptability are peer integrity pillars.
-- Their computed issues share the governed issue-observation ledger with CAF.

alter table public.issue_observations
  drop constraint if exists issue_observations_dimension_check;

alter table public.issue_observations
  add constraint issue_observations_dimension_check
  check (
    dimension in (
      'Clarity',
      'Alignment',
      'Feasibility',
      'Grounding',
      'Adaptability'
    )
  );

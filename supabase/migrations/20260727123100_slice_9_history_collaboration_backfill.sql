insert into public.project_history_events (
  workspace_id,
  project_id,
  analysis_run_id,
  actor_id,
  actor_type,
  category,
  event_type,
  summary,
  detail,
  issue_stable_key,
  payload,
  idempotency_key,
  occurred_at
)
select
  grant_record.workspace_id,
  grant_record.project_id,
  project.current_analysis_run_id,
  grant_record.created_by,
  'user',
  'collaboration',
  'collaboration.review_invited',
  'Reviewer invited',
  grant_record.reviewer_name || ' was invited to review a project issue.',
  grant_record.issue_stable_key,
  jsonb_build_object(
    'review_grant_id', grant_record.id::text,
    'reviewer_name', grant_record.reviewer_name
  ),
  'collaboration:review:' || grant_record.id::text || ':created',
  grant_record.created_at
from public.project_review_grants as grant_record
join public.projects as project
  on project.id = grant_record.project_id
where project.current_analysis_run_id is not null
on conflict (workspace_id, idempotency_key) do nothing;

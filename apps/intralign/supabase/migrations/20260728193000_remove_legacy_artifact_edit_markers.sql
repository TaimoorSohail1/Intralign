update public.assessment_snapshots
set snapshot_json = jsonb_set(
  snapshot_json,
  '{summary}',
  to_jsonb(
    coalesce(
      substring(
        snapshot_json->>'summary'
        from '(At the (orientation|expanded|validated) stage,.*)$'
      ),
      'The retained project read was refreshed from governed evidence.'
    )
  )
)
where snapshot_json->>'summary' like 'USER_ARTIFACT_EDIT%';

update public.project_report_drafts draft
set content_json = jsonb_set(
  draft.content_json,
  '{sections,0,body,0}',
  snapshot.snapshot_json->'summary'
),
updated_at = now()
from public.assessment_snapshots snapshot
where snapshot.id = draft.snapshot_id
  and draft.content_json::text like '%USER_ARTIFACT_EDIT%';

comment on table public.assessment_snapshots is
  'Immutable governed project reads. Public summaries exclude internal workflow envelopes.';

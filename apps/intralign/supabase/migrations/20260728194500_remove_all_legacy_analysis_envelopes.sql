-- Remove transport envelopes created by pre-structured user/reviewer evidence.
-- New runs persist these inputs in analysis_runs.user_evidence instead.

update public.analysis_runs
set description = regexp_replace(
  description,
  E'\\n\\n(USER_CLARIFICATION|REVIEWER_ATTESTATION|USER_ARTIFACT_EDIT)[\\s\\S]*$',
  ''
)
where description ~ '(USER_CLARIFICATION|REVIEWER_ATTESTATION|USER_ARTIFACT_EDIT)';

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
where snapshot_json->>'summary'
  ~ '^(USER_CLARIFICATION|REVIEWER_ATTESTATION|USER_ARTIFACT_EDIT)';

update public.project_report_drafts draft
set content_json = jsonb_set(
  draft.content_json,
  '{sections,0,body,0}',
  snapshot.snapshot_json->'summary'
),
updated_at = now()
from public.assessment_snapshots snapshot
where snapshot.id = draft.snapshot_id
  and draft.content_json::text
    ~ '(USER_CLARIFICATION|REVIEWER_ATTESTATION|USER_ARTIFACT_EDIT)';

comment on column public.analysis_runs.user_evidence is
  'Typed user, reviewer, and artifact evidence. Transport envelopes must not be stored in description.';

-- R2 Slice 6: freeze the lifecycle projection shown by recipient snapshots.
-- The source assessment remains immutable; this copy captures user-visible issue state
-- at the moment the share link is created.

alter table public.project_share_links
  add column frozen_snapshot_json jsonb;

comment on column public.project_share_links.frozen_snapshot_json is
  'Frozen recipient projection, including issue lifecycle status at share-link creation.';

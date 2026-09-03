-- R2 Slice 6: scoped ReviewRequest round-trip and recipient-bound snapshots.
-- Contracts: R2 S6 L1-L9 / INV-1..INV-8; DL-049; DL-166.

create type public.review_scope_kind as enum ('scoped', 'collaborator');
create type public.review_delivery_state as enum (
  'draft',
  'sending',
  'delivered',
  'failed',
  'awaiting',
  'answered',
  'withdrawn'
);

alter table public.project_review_grants
  add column scope_kind public.review_scope_kind not null default 'scoped',
  add column question_text text,
  add column source_ref text,
  add column source_excerpt text,
  add column delivery_state public.review_delivery_state not null default 'draft',
  add column delivery_attempts integer not null default 0 check (delivery_attempts between 0 and 3),
  add column delivered_at timestamptz,
  add column responded_at timestamptz,
  add column withdrawn_at timestamptz,
  add column token_version integer not null default 1 check (token_version > 0);

alter table public.project_review_grants
  add constraint project_review_grants_scoped_payload_check check (
    scope_kind <> 'scoped'
    or (
      issue_stable_key is not null
      and char_length(trim(question_text)) between 1 and 1000
      and char_length(trim(source_ref)) between 1 and 1000
      and char_length(trim(source_excerpt)) between 1 and 5000
    )
  ) not valid;

alter table public.project_review_responses
  add column basis text check (basis is null or basis = 'answered'),
  add column evidence_ref text,
  add column attributed_to jsonb,
  add column idempotency_key text;

create unique index project_review_responses_idempotency_idx
  on public.project_review_responses (workspace_id, idempotency_key)
  where idempotency_key is not null;

create index project_review_grants_active_issue_idx
  on public.project_review_grants (project_id, issue_stable_key, created_at desc)
  where revoked_at is null and withdrawn_at is null;

alter table public.project_share_links
  add column recipient_name text,
  add column recipient_email extensions.citext;

create table public.project_snapshot_views (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  project_id uuid not null references public.projects (id) on delete cascade,
  share_link_id uuid not null references public.project_share_links (id) on delete cascade,
  recipient_label text not null,
  first_viewed_at timestamptz not null default now(),
  last_viewed_at timestamptz not null default now(),
  retention_until timestamptz not null default (now() + interval '90 days'),
  unique (share_link_id)
);

alter table public.project_snapshot_views enable row level security;

create policy "members can view snapshot audit"
  on public.project_snapshot_views for select to authenticated
  using (private.is_workspace_member(workspace_id));

grant select on public.project_snapshot_views to authenticated;

comment on table public.project_snapshot_views is
  'Minimal disclosed Viewer audit. No raw token, IP address, user agent, or behavioral trail.';

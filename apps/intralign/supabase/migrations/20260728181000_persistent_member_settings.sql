alter table public.workspace_member_preferences
  add column if not exists display_name text not null default '',
  add column if not exists role_title text not null default '',
  add column if not exists mentions_notifications boolean not null default true,
  add column if not exists reply_notifications boolean not null default true,
  add column if not exists shared_notifications boolean not null default true;

alter table public.workspace_member_preferences
  add constraint workspace_member_preferences_display_name_length
  check (char_length(display_name) <= 120),
  add constraint workspace_member_preferences_role_title_length
  check (char_length(role_title) <= 120);

comment on column public.workspace_member_preferences.display_name is
  'Workspace-facing display name selected by this member.';

comment on column public.workspace_member_preferences.role_title is
  'Optional workspace-facing role or job title selected by this member.';

begin;

create table if not exists private.platform_admins (
  singleton boolean primary key default true check (singleton),
  user_id uuid not null unique references public.profiles (id) on delete cascade,
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  created_at timestamptz not null default now()
);

revoke all on private.platform_admins from public, anon, authenticated;
alter table private.platform_admins enable row level security;

comment on table private.platform_admins is
  'Single platform administrator. This identity is not a workspace Owner and uses no seat.';

insert into private.platform_admins (singleton, user_id, workspace_id)
select true, auth_user.id, target_workspace.workspace_id
from auth.users auth_user
cross join lateral (
  select coalesce(
    (
      select membership.workspace_id
      from public.memberships membership
      where membership.user_id = auth_user.id
      order by membership.created_at, membership.workspace_id
      limit 1
    ),
    (
      select workspace.id
      from public.workspaces workspace
      order by workspace.created_at, workspace.id
      limit 1
    )
  ) as workspace_id
) target_workspace
where lower(auth_user.email) = 'admin@oslo.local'
  and target_workspace.workspace_id is not null
limit 1
on conflict (singleton) do update set
  user_id = excluded.user_id,
  workspace_id = excluded.workspace_id;

delete from public.memberships membership
using private.platform_admins admin
where membership.user_id = admin.user_id;

commit;

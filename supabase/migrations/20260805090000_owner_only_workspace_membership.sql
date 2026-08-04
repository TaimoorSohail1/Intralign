begin;

lock table public.memberships in share row exclusive mode;
lock table public.invitations in share row exclusive mode;

update public.memberships set role = 'owner' where role <> 'owner';
update public.invitations set role = 'owner' where role <> 'owner';

alter table public.memberships alter column role drop default;
alter table public.invitations alter column role drop default;

alter type public.membership_role rename to membership_role_legacy;
create type public.membership_role as enum ('owner');

alter table public.memberships
  alter column role type public.membership_role
  using role::text::public.membership_role;
alter table public.invitations
  alter column role type public.membership_role
  using role::text::public.membership_role;

alter table public.memberships alter column role set default 'owner';
alter table public.invitations alter column role set default 'owner';

drop type public.membership_role_legacy;

comment on type public.membership_role is
  'Owner-only workspace membership. External review access is modelled separately.';

commit;

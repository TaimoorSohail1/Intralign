begin;

alter table public.invitations
  add column accepted_workspace_id uuid
  references public.workspaces (id) on delete cascade;

update public.invitations
set accepted_workspace_id = workspace_id
where status = 'accepted'
  and accepted_workspace_id is null;

comment on column public.invitations.accepted_workspace_id is
  'Workspace joined or provisioned when the invitation was accepted.';

commit;

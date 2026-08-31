create schema if not exists private;

revoke all on schema private from public, anon;
grant usage on schema private to authenticated;

alter function public.is_workspace_member(uuid) set schema private;
alter function public.is_workspace_owner(uuid) set schema private;

revoke all on function private.is_workspace_member(uuid) from public, anon;
revoke all on function private.is_workspace_owner(uuid) from public, anon;
grant execute on function private.is_workspace_member(uuid) to authenticated;
grant execute on function private.is_workspace_owner(uuid) to authenticated;

do $$
begin
  if to_regprocedure('public.rls_auto_enable()') is not null then
    execute 'alter function public.rls_auto_enable() set schema private';
    execute 'revoke all on function private.rls_auto_enable() from public, anon, authenticated';
  end if;
end;
$$;

comment on schema private is
  'Internal helper functions that must not be exposed through the Data API.';

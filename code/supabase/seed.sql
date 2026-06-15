-- =============================================================================
-- LOCAL-ONLY seed (applied by `supabase db reset`; never a schema migration).
--
-- DTM-0002 test support: the canonical tables revoke UPDATE/DELETE from every
-- API role, so PostgREST clients hit "permission denied" BEFORE the append-only
-- trigger can fire. This SECURITY DEFINER probe runs as the table owner
-- (postgres), which holds owner privileges — the only thing left to stop the
-- mutation is the BEFORE UPDATE OR DELETE trigger itself. The probe attempts
-- the mutation (against zero rows) and returns the raised error message, so
-- tests can assert the trigger fires even for owner-privileged connections.
-- =============================================================================

create or replace function public.test_probe_append_only(p_table text, p_op text)
returns text
language plpgsql
security definer
set search_path = public
as $probe$
declare
    msg text;
begin
    if p_table not in ('attested_assertion', 'cognition_history_record',
                       'user_acceptance_record', 'history_record') then
        raise exception 'test_probe_append_only: not a canonical table: %', p_table;
    end if;
    begin
        if p_op = 'update' then
            execute format('update public.%I set version = version where false', p_table);
        elsif p_op = 'delete' then
            execute format('delete from public.%I where false', p_table);
        else
            raise exception 'test_probe_append_only: unknown op: %', p_op;
        end if;
    exception when others then
        get stacked diagnostics msg = MESSAGE_TEXT;
        return msg;
    end;
    return 'NO ERROR RAISED';
end;
$probe$;

grant execute on function public.test_probe_append_only(text, text)
    to anon, authenticated, service_role;

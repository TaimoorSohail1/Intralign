-- The feedback repository uses SET LOCAL ROLE feedback_service. Grant that
-- isolated role to the migration/runtime database principal as well as the
-- conventional Supabase principals so feedback filing cannot fail merely
-- because a deployment uses a non-default Postgres login.

do $$
begin
  execute format('grant feedback_service to %I', current_user);

  if exists (select 1 from pg_roles where rolname = 'postgres') then
    grant feedback_service to postgres;
  end if;

  if exists (select 1 from pg_roles where rolname = 'service_role') then
    grant feedback_service to service_role;
  end if;
end
$$;

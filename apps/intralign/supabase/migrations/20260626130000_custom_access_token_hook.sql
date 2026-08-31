-- =============================================================================
-- DTM-0041 — Supabase custom-access-token hook (DTM-0036 deployment requirement).
--
-- OWNER-APPROVED additive deploy-binding artifact (deep-task-0041; staging deploy
-- prep). Mints the two project-issued custom claims the backend auth verifier
-- (backend/platform/auth.py) reads out of ``app_metadata``:
--     * workspace_id  — the caller's single R1 workspace scope.
--     * role          — the RBAC role (owner | admin | member).
-- GoTrue copies ``app_metadata`` into the access-token claims, and auth.py reads
-- ``role`` with ``prefer_metadata=True`` (Supabase reserves the top-level ``role``
-- claim for the Postgres role ``authenticated``), so minting them into
-- ``app_metadata`` is exactly the shape the verifier expects.
--
-- NO SECRET (Deployment Governance §7): this is SQL/config only. The hook reads a
-- mapping table; the JWT signing secret (SUPABASE_JWT_SECRET) is never referenced
-- here — GoTrue signs the token after the hook returns.
--
-- EPISTEMIC CLASS — PLATFORM, NOT CANONICAL: ``workspace_membership`` is a mutable
-- commodity auth-scoping table (who belongs to which workspace, in what role). It
-- touches NO canonical table (no ALTER/UPDATE/DELETE/DROP on any of them), so the
-- gate-4 migration linter (ci/gate_invariants.py) passes — this migration only
-- CREATEs new relations/functions and GRANTs.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Source-of-truth mapping: GoTrue user -> (workspace_id, role). R1 is single
-- workspace per user, so (user_id) is unique; the table shape allows a future
-- multi-workspace evolution without a destructive change. Seeded out-of-band
-- (owner/admin provisioning) or by the platform onboarding flow — NOT here.
-- -----------------------------------------------------------------------------
create table if not exists public.workspace_membership (
    user_id      uuid primary key,
    workspace_id uuid not null,
    role         text not null default 'member'
        check (role in ('owner', 'admin', 'member')),
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now()
);

comment on table public.workspace_membership is
    'Auth-scoping map (platform, mutable): GoTrue user -> workspace_id + RBAC role. '
    'Read by the custom-access-token hook to mint app_metadata claims (DTM-0036/DTM-0041).';

create index if not exists workspace_membership_workspace_idx
    on public.workspace_membership (workspace_id);

-- -----------------------------------------------------------------------------
-- The hook. GoTrue calls it with a JSONB ``event`` carrying ``user_id`` and the
-- in-flight ``claims`` (incl. ``app_metadata``); it returns the same event with
-- ``app_metadata.workspace_id`` + ``app_metadata.role`` merged in. If the user
-- has no membership row, the claims pass through unchanged — the backend verifier
-- then fails closed (AuthError: missing required claim) rather than minting a
-- default scope. SECURITY DEFINER so the hook can read the mapping regardless of
-- the caller; search_path pinned to '' to avoid search-path hijack.
-- -----------------------------------------------------------------------------
create or replace function public.custom_access_token_hook(event jsonb)
returns jsonb
language plpgsql
stable
security definer
set search_path = ''
as $$
declare
    claims        jsonb;
    v_workspace   uuid;
    v_role        text;
begin
    select m.workspace_id, m.role
      into v_workspace, v_role
      from public.workspace_membership m
     where m.user_id = (event ->> 'user_id')::uuid;

    claims := coalesce(event -> 'claims', '{}'::jsonb);

    if v_workspace is not null then
        -- Ensure app_metadata exists, then merge the two custom claims into it.
        if jsonb_typeof(claims -> 'app_metadata') is distinct from 'object' then
            claims := jsonb_set(claims, '{app_metadata}', '{}'::jsonb);
        end if;
        claims := jsonb_set(claims, '{app_metadata, workspace_id}', to_jsonb(v_workspace::text), true);
        claims := jsonb_set(claims, '{app_metadata, role}',         to_jsonb(v_role),            true);
        event  := jsonb_set(event,  '{claims}', claims, true);
    end if;

    return event;
end;
$$;

comment on function public.custom_access_token_hook(jsonb) is
    'Supabase access-token hook: mints app_metadata.workspace_id + app_metadata.role '
    'from public.workspace_membership (DTM-0036/DTM-0041). No secret; SQL/config only.';

-- -----------------------------------------------------------------------------
-- Grants required by the Supabase auth hook contract. GoTrue executes hooks as
-- the ``supabase_auth_admin`` role; it must be able to EXECUTE the function and
-- SELECT the mapping. Revoke EXECUTE from the public/API roles (the hook is not
-- an application endpoint). These grants target ONLY the new objects.
-- -----------------------------------------------------------------------------
grant usage on schema public to supabase_auth_admin;

grant execute on function public.custom_access_token_hook(jsonb) to supabase_auth_admin;
revoke execute on function public.custom_access_token_hook(jsonb) from authenticated, anon, public;

grant select on public.workspace_membership to supabase_auth_admin;

-- The mapping is owner/admin-provisioned, not client-writable: enable RLS and add
-- NO permissive policy for anon/authenticated (default-deny). service_role (the
-- backend) bypasses RLS by Postgres rule for any provisioning the app performs.
alter table public.workspace_membership enable row level security;

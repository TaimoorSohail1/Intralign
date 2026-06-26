-- =============================================================================
-- DTM-0031 — Platform persistence: project / analysis_run / notification.
--
-- OWNER-APPROVED additive migration (recorded 2026-06-26, deep-task-decisions.md
-- "Owner authorization"). Creates the three PLATFORM tables the DTM-0018 read
-- seam (backend/services/render/read_seam.py SupabaseProjectionReader) already
-- SELECTs, plus the columns the shared.entities DTOs (Data Model v1.2 §7/§10/§13)
-- bind verbatim. This makes the read seam hit real tables and unblocks the
-- project/analysis/notification command slices (DTM-0032/0034/0035).
--
-- Source of fields (VERBATIM, snake_case):
--   project       — RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2 §7  (+ LDM §6 physical
--                   binding: Supabase Postgres holds Projects/Users/Orgs).
--   analysis_run  — Data Model v1.2 §10; lifecycle/status enums per the State
--                   Model Specification (run_type / run_status).
--   notification  — Data Model v1.2 §13 (R-4); state enum per the State Model.
-- The exact column set is the INTERSECTION-superset of (a) the read seam's
-- SELECT * + its ORDER-BY columns (created_at / started_at) and (b) the DTO
-- field sets — no column is invented, none the read/DTO needs is omitted.
--
-- EPISTEMIC CLASS — PLATFORM, NOT CANONICAL (locked decision; LDM §2 vs §6):
--   These are mutable commodity tables (project lifecycle transitions,
--   analysis_run status transitions, notification view/dismiss state). The
--   append-only discipline applies to the CANONICAL epistemic store ONLY
--   (attested_assertion / cognition_history_record / user_acceptance_record /
--   history_record). Therefore — by design, and per the gate-4 migration linter
--   (ci/gate_invariants.py) — this migration:
--     * CREATEs three brand-new relations and touches NO canonical table
--       (no ALTER / UPDATE / DELETE / DROP TABLE / REVOKE on any of them);
--     * adds NO append-only trigger and NO mutation REVOKE to the platform
--       tables (they are meant to be UPDATE-able — that is correct here).
--
-- WORKSPACE SCOPING / RLS (API Contract §3; single workspace per user in R1):
--   RLS is enabled on every table; reads/writes are scoped by workspace_id
--   (project / notification carry it directly; analysis_run inherits it through
--   its parent project). The service_role (the backend app role) bypasses RLS
--   by Postgres rule, so the repos' explicit ``.eq(workspace_id, …)`` /
--   ``.eq(project_id, …)`` filters are the scoping the backend relies on; the
--   policies bind direct anon/authenticated access (defence in depth).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- §7 Project — the planning workspace's unit of work. lifecycle_state is the
-- mutable Project lifecycle (created -> orienting -> oriented -> deep_analyzing
-- -> analyzed -> archived; State Model §"60-Second Orientation"/"Deep Analysis").
-- current_confidence_state_id references the live MRI confidence projection.
-- -----------------------------------------------------------------------------
create table public.project (
    project_id                  uuid primary key default gen_random_uuid(),
    workspace_id                uuid not null,
    created_by_user_id          uuid,
    title                       text,
    description                 text,
    lifecycle_state             text not null default 'created'
        check (lifecycle_state in ('created', 'orienting', 'oriented',
                                   'deep_analyzing', 'analyzed', 'archived')),
    current_confidence_state_id uuid,
    created_at                  timestamptz not null default now(),
    updated_at                  timestamptz not null default now()
);

comment on table public.project is
    'Data Model v1.2 §7 — Project (platform, mutable lifecycle; workspace-scoped); LDM §6; DTM-0031.';

create index project_workspace_idx on public.project (workspace_id, created_at desc);

-- -----------------------------------------------------------------------------
-- §10 AnalysisRun — one fast/deep analysis pass over a project. run_status is
-- the mutable run lifecycle (queued -> running -> completed|failed|cancelled,
-- and superseded on re-run; State Model §"AnalysisRun"). previous_run_id chains
-- successive runs. started_at is the read seam's ORDER-BY column.
-- -----------------------------------------------------------------------------
create table public.analysis_run (
    analysis_run_id uuid primary key default gen_random_uuid(),
    project_id      uuid not null references public.project (project_id),
    run_type        text not null
        check (run_type in ('fast_analysis_pass', 'deep_analysis_pass')),
    run_status      text not null default 'queued'
        check (run_status in ('queued', 'running', 'completed', 'failed',
                              'cancelled', 'superseded')),
    previous_run_id uuid references public.analysis_run (analysis_run_id),
    started_at      timestamptz,
    completed_at    timestamptz,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

comment on table public.analysis_run is
    'Data Model v1.2 §10 — AnalysisRun (platform, mutable status; project-scoped); State Model; DTM-0031.';

create index analysis_run_project_idx on public.analysis_run (project_id, started_at desc);

-- -----------------------------------------------------------------------------
-- §13 Notification (R-4) — platform awareness state (non-canonical; never drives
-- analysis). state is the mutable awareness lifecycle (created -> viewed ->
-- dismissed; expired terminal; State Model §"notifications"). It references a
-- source object (finding|recommendation|analysis_run|comment|shared_artifact)
-- but carries no epistemic cognition label (it is not a Derived projection).
-- -----------------------------------------------------------------------------
create table public.notification (
    notification_id    uuid primary key default gen_random_uuid(),
    workspace_id       uuid not null,
    project_id         uuid references public.project (project_id),
    source_object_type text not null
        check (source_object_type in ('finding', 'recommendation', 'analysis_run',
                                      'comment', 'shared_artifact')),
    source_object_id   uuid not null,
    event_type         text not null,
    target_user_id     uuid,
    state              text not null default 'created'
        check (state in ('created', 'viewed', 'dismissed', 'expired')),
    created_at         timestamptz not null default now(),
    viewed_at          timestamptz,
    dismissed_at       timestamptz,
    expired_at         timestamptz
);

comment on table public.notification is
    'Data Model v1.2 §13 — Notification (platform awareness, mutable state; workspace-scoped); State Model; DTM-0031.';

create index notification_workspace_idx on public.notification (workspace_id, created_at desc);

-- =============================================================================
-- Grants — platform tables ARE mutable (non-canonical): the app/API roles get
-- full access (mirroring the DERIVED grant style of migration
-- 20260612090100, NOT the canonical REVOKE). No append-only trigger, no REVOKE.
-- =============================================================================
grant all on public.project       to anon, authenticated, service_role;
grant all on public.analysis_run  to anon, authenticated, service_role;
grant all on public.notification  to anon, authenticated, service_role;

-- =============================================================================
-- Row-Level Security — workspace-scoped (API Contract §3). RLS is enabled on
-- every table; the service_role (backend) bypasses RLS by Postgres rule, so the
-- backend scoping is the repos' explicit workspace/project filters. The policies
-- bind direct anon/authenticated access to the caller's workspace (R1: one
-- workspace per user). app.workspace_id is the request-scoped GUC the API sets.
-- =============================================================================
alter table public.project      enable row level security;
alter table public.analysis_run enable row level security;
alter table public.notification enable row level security;

create policy project_workspace_isolation on public.project
    for all to anon, authenticated
    using (workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid)
    with check (workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid);

create policy analysis_run_workspace_isolation on public.analysis_run
    for all to anon, authenticated
    using (
        project_id in (
            select p.project_id from public.project p
            where p.workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid
        )
    )
    with check (
        project_id in (
            select p.project_id from public.project p
            where p.workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid
        )
    );

create policy notification_workspace_isolation on public.notification
    for all to anon, authenticated
    using (workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid)
    with check (workspace_id = nullif(current_setting('app.workspace_id', true), '')::uuid);

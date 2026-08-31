-- =============================================================================
-- DTM-0002 — Canonical (Attested) schema: append-only enforced in Postgres.
--
-- Source of fields (VERBATIM, snake_case): RELEASE_1_LOGICAL_DATA_MODEL_V1.md
--   §1  universal fields  ·  §2.1 attested_assertion  ·  §2.2 cognition_history_record
--   §2.4 user_acceptance_record (+ Plan Fact rule)  ·  §2.5 history_record
-- Binding: DL-054 (Supabase Postgres; snapshots/refs -> jsonb), DL-043,
--          code/CLAUDE.md hard rules #2 (canonical/derived separation) and
--          #3 (recompute appends, never overwrites).
--
-- Canonical tables are APPEND-ONLY (LDM §5.1). Enforcement is belt-and-braces:
--   belt   — REVOKE UPDATE, DELETE (and TRUNCATE, which bypasses row triggers)
--            from anon, authenticated, service_role;
--   braces — BEFORE UPDATE OR DELETE statement-level trigger raising an
--            exception, so even owner-privileged connections fail.
--
-- NOTE for the gate-4 migration linter (ci/gate_invariants.py): every canonical
-- table below is created COMPLETE in a single CREATE TABLE statement with all
-- constraints inline — no post-hoc ALTER TABLE on canonical tables.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- §2.1 Attested Assertion — the canonical unit (single table; sub-classes by
-- attesting_source discriminator). Plan Fact (§2.4) = a row in THIS table with
-- attesting_source = 'user' (user-attested confirmed content).
-- An inferred assumption/constraint/dependency is Derived (§3), never stored here.
-- -----------------------------------------------------------------------------
create table public.attested_assertion (
    -- LDM §2.1 fields
    assertion_id     uuid primary key default gen_random_uuid(),
    content_type     text not null
        check (content_type in ('fact', 'assumption', 'constraint', 'dependency', 'goal')),
    proposition      text not null,
    attesting_source text not null,  -- evidence-source-id | oslo | user-id (discriminator; open identifier set -> no CHECK)
    source_ref       jsonb not null, -- artifact + locus, or emission ref, or acceptance ref
    re_derivable     boolean not null default true,
    version          integer not null default 1,
    supersedes_id    uuid references public.attested_assertion (assertion_id),
    created_at       timestamptz not null default now(),
    -- LDM §1 universal fields not already named by §2.1
    project_id       uuid not null,
    created_by       text not null,  -- user | OSLO | source-system
    epistemic_state  text not null
        check (epistemic_state in ('attested-evidence', 'attested-oslo', 'attested-user')),
    provenance_ref   jsonb not null
);

comment on table public.attested_assertion is
    'LDM §2.1 — canonical append-only Attested Assertion (system of record); Plan Fact = attesting_source = user (LDM §2.4); DL-043.';

-- -----------------------------------------------------------------------------
-- §2.2 Cognition History Record — OSLO-self-attested emission receipt.
-- A recompute APPENDS a new CHR; it never overwrites (hard rule #3).
-- -----------------------------------------------------------------------------
create table public.cognition_history_record (
    -- LDM §2.2 fields
    chr_id                    uuid primary key default gen_random_uuid(),
    output_kind               text not null
        check (output_kind in ('finding', 'issue', 'confidence', 'reliability', 'caf',
                               'outcome_confidence', 'recommendation', 'clarification',
                               'acceptance_impact', 'alignment', 'feasibility', 'risk')),
    output_payload            jsonb not null,  -- emitted value/content snapshot (DL-054: snapshots -> jsonb)
    emitted_at                timestamptz not null default now(),
    input_attestation_version text not null,   -- which Attested set it was computed over
    model_or_rule_version     jsonb not null,  -- incl. provider+model identity (structured -> jsonb)
    upstream_lineage          jsonb not null,  -- refs to the CHRs/assertions it derived from
    recompute_trigger         text not null
        check (recompute_trigger in ('promotion', 'knowledge-change', 'clarification',
                                     'user-action', 'reanalysis')),
    supersedes_chr_id         uuid references public.cognition_history_record (chr_id),
    -- LDM §1 universal fields not already named by §2.2
    project_id                uuid not null,
    created_at                timestamptz not null default now(),
    created_by                text not null default 'OSLO',
    epistemic_state           text not null default 'attested-oslo'
        check (epistemic_state = 'attested-oslo'),  -- §2.2: OSLO-self-attested
    provenance_ref            jsonb not null,
    version                   integer not null default 1
);

comment on table public.cognition_history_record is
    'LDM §2.2 — canonical append-only Cognition History Record (emission receipt); recompute appends, never overwrites; DL-043.';

-- -----------------------------------------------------------------------------
-- §2.4 User Acceptance Record — user-attested. NOT a Governance Decision.
-- version_pin = CHR id for Derived targets, or assertion id for Attested
-- (polymorphic -> no single-table FK; integrity is a logical invariant §5.4).
-- -----------------------------------------------------------------------------
create table public.user_acceptance_record (
    -- LDM §2.4 fields
    uar_id          uuid primary key default gen_random_uuid(),
    user_id         uuid not null,
    confirmed_at    timestamptz not null default now(),
    action          text not null
        check (action in ('accept', 'reject', 'defer', 'direct_edit')),
    target_kind     text not null,  -- recommendation | finding | assumption | plan_item | … (LDM list open-ended -> no CHECK)
    version_pin     uuid not null,
    rationale       text,           -- optional
    -- LDM §1 universal fields not already named by §2.4
    project_id      uuid not null,
    created_at      timestamptz not null default now(),
    created_by      text not null,
    epistemic_state text not null default 'attested-user'
        check (epistemic_state = 'attested-user'),  -- §2.4: user-attested
    provenance_ref  jsonb not null,
    version         integer not null default 1,
    supersedes_id   uuid references public.user_acceptance_record (uar_id)
);

comment on table public.user_acceptance_record is
    'LDM §2.4 — canonical append-only User Acceptance Record (user-attested; version-pinned; not a Governance Decision); DL-043.';

-- -----------------------------------------------------------------------------
-- §2.5 History Record — generic append-only audit entry (integrity/audit trail).
-- -----------------------------------------------------------------------------
create table public.history_record (
    -- LDM §2.5 fields
    history_id      uuid primary key default gen_random_uuid(),
    event_type      text not null
        check (event_type in ('integrity-clearance', 'knowledge-versioned', 'superseded',
                              'archived', 'emission-appended', 'acceptance-recorded', 'recompute')),
    subject_ref     jsonb not null,
    at              timestamptz not null default now(),
    actor           text not null,
    -- LDM §1 universal fields not already named by §2.5
    project_id      uuid not null,
    created_at      timestamptz not null default now(),
    created_by      text not null,
    epistemic_state text not null
        check (epistemic_state in ('attested-evidence', 'attested-oslo', 'attested-user')),
    provenance_ref  jsonb not null,
    version         integer not null default 1,
    supersedes_id   uuid references public.history_record (history_id)
);

comment on table public.history_record is
    'LDM §2.5 — canonical append-only History Record (generic audit entry; R3/R5 event mapping); DL-043.';

-- =============================================================================
-- Append-only enforcement (LDM §5.1; DL-043; hard rule #3) — belt and braces.
-- =============================================================================

-- Braces: one shared trigger function; raises on any UPDATE/DELETE attempt.
create function public.enforce_append_only() returns trigger
language plpgsql
as $append_only$
begin
    raise exception
        '% on canonical table "%" is forbidden: canonical stores are append-only (LDM v1 §5.1; DL-043; recompute appends, never overwrites)',
        TG_OP, TG_TABLE_NAME;
end;
$append_only$;

comment on function public.enforce_append_only() is
    'Shared append-only guard for canonical tables (LDM §5.1; DL-043): BEFORE UPDATE OR DELETE -> exception.';

-- Statement-level so the guard fires even for zero-row UPDATE/DELETE attempts.
create trigger attested_assertion_append_only
    before update or delete on public.attested_assertion
    for each statement execute function public.enforce_append_only();

create trigger cognition_history_record_append_only
    before update or delete on public.cognition_history_record
    for each statement execute function public.enforce_append_only();

create trigger user_acceptance_record_append_only
    before update or delete on public.user_acceptance_record
    for each statement execute function public.enforce_append_only();

create trigger history_record_append_only
    before update or delete on public.history_record
    for each statement execute function public.enforce_append_only();

-- Belt: revoke mutation privileges from every API/app role (service_role is the
-- distinct app/backend role in Supabase). TRUNCATE included — it would bypass
-- row/statement UPDATE/DELETE triggers.
revoke update, delete, truncate on public.attested_assertion        from anon, authenticated, service_role;
revoke update, delete, truncate on public.cognition_history_record  from anon, authenticated, service_role;
revoke update, delete, truncate on public.user_acceptance_record    from anon, authenticated, service_role;
revoke update, delete, truncate on public.history_record            from anon, authenticated, service_role;

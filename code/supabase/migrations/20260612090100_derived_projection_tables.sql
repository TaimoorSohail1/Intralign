-- =============================================================================
-- DTM-0002 — Derived representation: live cognition projections (current-view).
--
-- Source of fields (VERBATIM, snake_case): RELEASE_1_LOGICAL_DATA_MODEL_V1.md §3.1
-- (Live Cognition Projection) — instances: Findings / Issues / Recommendations /
-- Clarifications / Confidence / CAF / Outcome-Confidence / Acceptance-Impact.
-- Locked decision #5: derived projections live in separate tables in schema
-- `derived`, rebuildable, with FK lineage columns referencing CHR ids.
--
-- These tables are NON-canonical and UPDATABLE: a recompute appends a new
-- cognition_history_record (canonical) and REPLACES the projection row here.
-- Derived carries no authority (LDM §5.6) — if lost, recompute restores it.
-- Confidence bands per RELEASE_1_CALIBRATION_DEFAULTS_V1.md §2: low/medium/high.
-- =============================================================================

create schema derived;

-- One table per §3.1 projection instance; identical shape (the §3.1 field set).
-- output_kind values use the LDM §2.2 output_kind vocabulary.

create table derived.finding_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'finding' check (output_kind = 'finding'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.issue_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'issue' check (output_kind = 'issue'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.confidence_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'confidence' check (output_kind = 'confidence'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.caf_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'caf' check (output_kind = 'caf'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.recommendation_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'recommendation' check (output_kind = 'recommendation'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.clarification_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'clarification' check (output_kind = 'clarification'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.outcome_confidence_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'outcome_confidence' check (output_kind = 'outcome_confidence'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

create table derived.acceptance_impact_current (
    projection_id    uuid primary key default gen_random_uuid(),
    project_id       uuid not null,
    output_kind      text not null default 'acceptance_impact' check (output_kind = 'acceptance_impact'),
    current_payload  jsonb not null,
    current_chr_ref  uuid not null references public.cognition_history_record (chr_id),
    epistemic_label  text not null default 'derived' check (epistemic_label = 'derived'),
    confidence_value numeric check (confidence_value between 0 and 100),
    confidence_band  text check (confidence_band in ('low', 'medium', 'high')),
    conflict_state   text not null default 'none' check (conflict_state in ('none', 'contested')),
    recomputed_at    timestamptz not null default now()
);

-- API/app access: derived tables ARE updatable (non-canonical, rebuildable).
grant usage on schema derived to anon, authenticated, service_role;
grant all on all tables in schema derived to anon, authenticated, service_role;
alter default privileges in schema derived
    grant all on tables to anon, authenticated, service_role;

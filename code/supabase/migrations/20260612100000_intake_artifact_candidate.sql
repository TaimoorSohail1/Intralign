-- =============================================================================
-- DTM-0007 — IC-WA-001 Artifact Intake: evidence anchor + promotion candidate.
--
-- Source of fields: RELEASE_1_LOGICAL_DATA_MODEL_V1.md §2.3 (Evidence & Intake)
--   + §1 universal fields, per the DTM-0002 precedent. Binding: DL-054
--   (artifact BODIES live in Supabase Storage bucket 'artifacts'; Postgres
--   holds body_ref + normalized_form), DL-053 (idempotency key is named
--   dedup_key), IC-WA-001 A3.1/A3.3/A3.8.
--
-- artifact            — APPEND-ONLY canonical evidentiary anchor (LDM §2.3
--                       "Append-only/versioned"); same belt-and-braces
--                       enforcement as the DTM-0002 canonical tables, reusing
--                       the existing public.enforce_append_only() trigger
--                       function. Added to the gate-4 linter CANONICAL_TABLES.
-- promotion_candidate — transient-but-audited, MUTABLE (readiness_state moves
--                       pending -> ready|failed; LDM §2.3 "transient, not
--                       long-term canonical") — deliberately NO append-only lock.
--
-- NOTE for the gate-4 migration linter (ci/gate_invariants.py): the canonical
-- table below is created COMPLETE in a single CREATE TABLE statement with all
-- constraints inline — no post-hoc ALTER TABLE on canonical tables.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- §2.3 Artifact — raw intake evidence anchor. The unstructured body lives in
-- Supabase Storage (bucket 'artifacts'); body_ref is the Storage object path.
-- dedup_key = sha256(project_id + source + content) — UNIQUE makes
-- double-admission impossible at the store level (A3.3/A3.8; QA B2.4/B3.6).
-- -----------------------------------------------------------------------------
create table public.artifact (
    -- LDM §2.3 fields (content_ref bound to Storage as body_ref per DL-054)
    artifact_id     uuid primary key default gen_random_uuid(),
    project_id      uuid not null,
    body_ref        text not null,   -- Supabase Storage path of the raw body
    normalized_form jsonb not null,  -- consistent internal form, meaning-preserving
    provenance      jsonb not null,  -- who / when / from-where (A3.1)
    dedup_key       text not null unique,  -- DL-053 name; idempotent intake (A3.3)
    submitted_by    text not null,
    created_at      timestamptz not null default now(),
    -- LDM §1 universal fields not already named above
    epistemic_state text not null default 'attested-evidence'
        check (epistemic_state = 'attested-evidence'),  -- evidence-attested anchor
    provenance_ref  jsonb not null,
    version         integer not null default 1,
    supersedes_id   uuid references public.artifact (artifact_id),
    created_by      text not null    -- user | source-system
);

comment on table public.artifact is
    'LDM §2.3 — canonical append-only Artifact (evidence anchor); body in Supabase Storage (DL-054); dedup_key idempotency (DL-053); IC-WA-001.';

-- -----------------------------------------------------------------------------
-- §2.3 Promotion Candidate — transient pre-admission object, audited but
-- MUTABLE (no append-only lock): readiness_state is its lifecycle field.
-- integrity_clearance records the attribution + idempotency + evidence-chain
-- results (OBS-WA-001 C3 integrity-clearance reference).
-- -----------------------------------------------------------------------------
create table public.promotion_candidate (
    candidate_id        uuid primary key default gen_random_uuid(),
    artifact_ref        uuid not null references public.artifact (artifact_id),
    normalized_form     jsonb not null,
    readiness_state     text not null default 'pending'
        check (readiness_state in ('pending', 'ready', 'failed')),
    integrity_clearance jsonb,       -- attribution + idempotency + evidence-chain results
    project_id          uuid not null,
    created_at          timestamptz not null default now(),
    updated_at          timestamptz not null default now()
);

comment on table public.promotion_candidate is
    'LDM §2.3 — transient-but-audited Promotion Candidate (pending|ready|failed); resolves into Attested Assertions on Retain admission; IC-WA-001.';

-- =============================================================================
-- Append-only enforcement for artifact (LDM §5.1) — belt and braces, reusing
-- the shared guard from migration 20260612090000.
-- =============================================================================

-- Braces: statement-level trigger so the guard fires even for zero-row attempts.
create trigger artifact_append_only
    before update or delete on public.artifact
    for each statement execute function public.enforce_append_only();

-- Belt: revoke mutation privileges from every API/app role. TRUNCATE included —
-- it would bypass row/statement UPDATE/DELETE triggers.
revoke update, delete, truncate on public.artifact from anon, authenticated, service_role;

-- =============================================================================
-- DTM-0009 — Widen the Cognition History Record output_kind CHECK by EXACTLY
-- the two Wave-S Derived kinds: 'synthesized_planning_model', 'planning_artifact'.
--
-- OWNER-APPROVED 2026-06-17 (deep-task-decisions.md "Schema for Derived types"
-- — RESOLVED for Wave S; deep-task-0009.md persistence line). The Wave-S
-- Derived outputs (SynthesizedPlanningModel + the seven PlanningArtifact types)
-- persist via the GENERIC CHR output_kind/output_payload (no typed tables).
-- migration 20260612090000 created the CHR table before these two kinds existed
-- (it admits only the 12 Wave-A/B kinds); this migration adds the two — and
-- ONLY the two — owner-approved values. Anything further => STOP (decisions).
--
-- Binding: DL-047 (object additions), DL-054 (Supabase Postgres), code/CLAUDE.md
-- hard rule #3 (recompute appends, never overwrites) — UNCHANGED here.
--
-- APPEND-ONLY PRESERVED: this migration touches ONLY the output_kind CHECK
-- constraint (drop + recreate, widened by two values). It does NOT touch the
-- append-only enforcement — the BEFORE UPDATE/DELETE trigger and the
-- REVOKE UPDATE/DELETE/TRUNCATE grants from migration 20260612090000 are left
-- exactly as they are. No row is mutated; no column is altered; no data moves.
-- The table stays append-only; only the set of permitted output_kind values grows.
--
-- NOTE for the gate-4 migration linter (ci/gate_invariants.py): this is the sole
-- ALTER TABLE on a canonical table in the repo. It is an owner-approved,
-- append-only-preserving CHECK widening, recorded in the gate-4 ALTER allowlist
-- (ci/invariant_allowlist.txt) under gate-7 human review — NOT a data mutation.
-- =============================================================================

alter table public.cognition_history_record
    drop constraint if exists cognition_history_record_output_kind_check;

alter table public.cognition_history_record
    add constraint cognition_history_record_output_kind_check
    check (output_kind in ('finding', 'issue', 'confidence', 'reliability', 'caf',
                           'outcome_confidence', 'recommendation', 'clarification',
                           'acceptance_impact', 'alignment', 'feasibility', 'risk',
                           -- DTM-0009 / Wave S (DL-047) — owner-approved 2026-06-17:
                           'synthesized_planning_model', 'planning_artifact'));

comment on constraint cognition_history_record_output_kind_check
    on public.cognition_history_record is
    'LDM §2.2 output_kind value list — 12 Wave-A/B kinds + 2 Wave-S kinds (DL-047, owner-approved 2026-06-17, DTM-0009).';

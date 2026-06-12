# DTM-0002 — Canonical schema: append-only enforced in Postgres

**Status:** Not started · **Module:** DTM-0002 · **Phase:** I · **Contract:** none (Phase-I infra; label `phase-1-infra`)

## Goal / observable behavior

Supabase migrations create the canonical (Attested) stores as **database-enforced
append-only** tables and the derived projections as separate, rebuildable tables.
`UPDATE`/`DELETE` against a canonical table **fails at the database**, proven by tests.

## Source docs / constraints

- Field-level model: `30_engineering/runtime_models/RELEASE_1_LOGICAL_DATA_MODEL_V1.md` §2 (canonical) + §3 (derived) — bind fields **verbatim**, invent nothing (ANTI_ASSUMPTION).
- Entity reference: `30_engineering/data/RELEASE_1_DATA_MODEL_SPECIFICATION_V1.2.md`.
- Binding: DL-054 (Supabase Postgres; snapshots `jsonb`; large blobs → Storage).
- Hard rules #2/#3 (`code/CLAUDE.md`): canonical/derived separation; recompute appends.

## Locked decisions

- Tables: `attested_assertion` (single table, `attesting_source` discriminator; Plan Fact = user-attested row per LDM §2.4) · `cognition_history_record` (CHR §2.2 incl. `model_or_rule_version` with provider+model identity, `upstream_lineage`, `supersedes_chr_id`) · `user_acceptance_record` (§2.4) · `history_record` (§2.5).
- Enforcement: `REVOKE UPDATE, DELETE` from app role + `BEFORE UPDATE OR DELETE` trigger raising exception, per canonical table.
- Derived projections in Postgres schema `derived`; FK lineage columns referencing CHR ids; rebuildable (no canonical data lives only there).
- Migrations under `code/supabase/migrations/` (Supabase CLI layout).

## Owned files

- `code/supabase/**` (new), `code/tests/{positive,negative}/persistence/**` (new).
- Read-only: `shared/`, `backend/` (no repository code yet — that's DTM-0004).

## Packages / refactors

- None new (supabase CLI is environment tooling, not a Python dep). No refactors.

## Implementation instructions

1. Author migration SQL for the four canonical tables, bound field-by-field to LDM §2.
2. Add the append-only enforcement (revoke + trigger) in the same migration.
3. Create `derived` schema + the live-projection tables LDM §3.1 names, lineage FKs to CHR.
4. Tests (against local Supabase): insert OK; `UPDATE`→error; `DELETE`→error; `supersedes_chr_id` chain insert OK; derived rows updatable (they're non-canonical).

## Data contract

LDM §2.1/§2.2/§2.4/§2.5 column sets, names verbatim (snake_case). Enum-ish fields as
`text` + `CHECK` constraints using LDM's exact value lists (e.g. `recompute_trigger`).

## Test plan

- Positive: inserts + supersession chains on all four tables; derived projection update succeeds.
- Negative: UPDATE/DELETE on each canonical table rejected by PG (both via revoked role and trigger); migration linter (DTM-0001 gate 4) passes on these migrations.

## Done criteria

- `supabase db reset` applies clean; all tests green locally; gate-4 linter passes; no field invented beyond LDM/Data-Model v1.2.

## Worker report

_(pending)_

## Engineering-manager review notes

_(pending)_

## Approved by engineering manager

_(pending)_

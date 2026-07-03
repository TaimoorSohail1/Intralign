# DTM-0002 — Canonical schema: append-only enforced in Postgres

**Status:** Approved · **Module:** DTM-0002 · **Phase:** I · **Contract:** none (Phase-I infra; label `phase-1-infra`)

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

**Worker:** DTM-0002 worker · **Date:** 2026-06-12 · **Result:** complete; all done-criteria met locally.

### Built

- `code/supabase/` (new, via `supabase init`): `config.toml` (edited — see deviations), `.gitignore`, `.temp/` (CLI cache, gitignored), `migrations/`, `seed.sql`.
- `code/supabase/migrations/20260612090000_canonical_append_only_tables.sql` — the four canonical tables in `public`, each created **complete in a single `CREATE TABLE`** (all constraints inline; no `ALTER TABLE` on canonical tables, per the gate-4 linter):
  - `attested_assertion` (LDM §2.1, single table, `attesting_source` discriminator; Plan Fact = `attesting_source = 'user'` per §2.4); `content_type` CHECK with §2.1's exact list.
  - `cognition_history_record` (LDM §2.2) incl. `model_or_rule_version` (jsonb, provider+model identity), `input_attestation_version`, `upstream_lineage` (jsonb), `recompute_trigger` CHECK with §2.2's exact list (`promotion | knowledge-change | clarification | user-action | reanalysis`), `supersedes_chr_id` self-FK.
  - `user_acceptance_record` (LDM §2.4): `action` CHECK (`accept|reject|defer|direct_edit`), `version_pin`, `target_kind` (no CHECK — LDM list is explicitly open-ended: "… ").
  - `history_record` (LDM §2.5): `history_id`, `event_type` CHECK with §2.5's exact list, `subject_ref`, `at`, `actor`.
  - All four also carry the LDM §1 **universal fields** not already named per-section: `project_id`, `created_at`, `created_by`, `epistemic_state` (CHECK restricted to `attested-*`), `provenance_ref`, `version`, `supersedes_id` (self-FK).
  - **Append-only enforcement, belt and braces:** (1) `REVOKE UPDATE, DELETE, TRUNCATE … FROM anon, authenticated, service_role` per table; (2) one shared plpgsql function `public.enforce_append_only()` raising an exception citing append-only/LDM §5.1/DL-043, wired as a `BEFORE UPDATE OR DELETE … FOR EACH STATEMENT` trigger on each table (statement-level so it fires even on zero-row attempts).
- `code/supabase/migrations/20260612090100_derived_projection_tables.sql` — schema `derived` with eight projection tables (LDM §3.1 instance list): `finding_current`, `issue_current`, `confidence_current`, `caf_current`, `recommendation_current`, `clarification_current`, `outcome_confidence_current`, `acceptance_impact_current`. Each binds §3.1's field set verbatim (`projection_id`, `output_kind`, `current_payload`, `current_chr_ref`, `epistemic_label`, `confidence_value`, `confidence_band`, `conflict_state`, `recomputed_at`) + `project_id`; `current_chr_ref` is a **FK to `cognition_history_record(chr_id)`**; tables are updatable; grants for `anon/authenticated/service_role`.
- `code/supabase/seed.sql` — **local-only test probe** `public.test_probe_append_only(p_table, p_op)` (SECURITY DEFINER, runs as table owner, attempts UPDATE/DELETE against zero rows and returns the raised message). Needed because the REVOKE belt blocks API roles with "permission denied" *before* the trigger can fire — the probe is the only way to prove the trigger itself fires for owner-privileged connections. Seed ≠ migration; ships no schema.
- `code/tests/positive/persistence/test_canonical_persistence.py` — INSERT into each canonical table (incl. Plan Fact row); CHR supersedes chain (A → B with `supersedes_chr_id = A`); UAR version-pinned to a CHR; derived `finding_current` INSERT **and UPDATE** succeed.
- `code/tests/negative/persistence/test_append_only_enforcement.py` — UPDATE and DELETE on **each** canonical table rejected via revoked privileges (service_role gets `permission denied`); trigger verified to fire past privileges via the probe (asserts the message contains `append-only` and `DL-043`), for update+delete on all four tables; invalid `recompute_trigger` rejected (CHECK); invalid UAR `action` rejected (CHECK).
- Both test modules **skip gracefully** (`pytest.mark.skipif`) when `supabase-py` is not importable or `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` are unset — Phase I CI has no Supabase, so these run locally only (documented in module docstrings). Transport is **supabase-py** (already in `pyproject.toml`); `psycopg` is NOT transitively available (verified), so PostgREST is the test path.

### Commands + real results

| Command | Result |
|---|---|
| `cd code && printf 'n\nn\n' \| supabase init` | "Finished supabase init." Declined VS Code/IntelliJ Deno settings. Created `config.toml`, `.gitignore`, `.temp/` only. |
| `supabase start` | Started clean; both migrations applied on first start; seed applied. |
| `supabase db reset` | Re-applied clean: both migrations + seed, "Finished supabase db reset on branch feat/phase1-wavea-00r." |
| `/tmp/oslo-ci-venv/bin/python -m ci.gate_invariants --code-root .` | **PASS** — "no forbidden tokens, no authority module, no canonical-table mutations in migrations." |
| Live persistence suites (`/tmp/oslo-dbtest-venv`, env set) | **24 passed** (6 positive, 18 negative). |
| `/tmp/oslo-ci-venv/bin/python -m pytest tests/positive tests/negative` (no Supabase env) | **57 passed, 24 skipped** — persistence suites skip gracefully; all ci/health suites green. |
| Same, with `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` set | **81 passed** — full local green incl. live persistence. |

`supabase status` (stack left RUNNING for DTM-0003): API `http://127.0.0.1:54331` · DB `postgresql://postgres:postgres@127.0.0.1:54332/postgres` · Studio `http://127.0.0.1:54333` · Inbucket `http://127.0.0.1:54334` · demo JWT keys (standard local `supabase-demo` anon/service_role keys, retrievable any time via `supabase status`).

### LDM-gap flags (owner confirmation needed)

1. **§2.5 history_record — universal-field overlay duplication.** §2.5 *does* give an explicit list (`history_id · event_type · subject_ref · at · actor`); I bound it verbatim AND applied the §1 universal fields ("every entity") consistently with the other tables. Result: `at`/`created_at` and `actor`/`created_by` semantically overlap. Kept both (verbatim binding); owner may wish to collapse.
2. **`id` vs entity-specific ids.** §1 universal `id` is realized as each section's named id (`assertion_id`, `chr_id`, `uar_id`, `history_id`) — no separate `id` column added.
3. **`epistemic_state` CHECK restricted to the three `attested-*` values on canonical tables** (full LDM list includes `derived`, but a `derived` row in the canonical store would violate §1 two-storage-classes / hard rule #2). CHR pinned to `attested-oslo`, UAR to `attested-user` (their §2.2/§2.4 sub-class labels).
4. **Physical types are environment-layer choices** (LDM is explicitly logical, §6): uuid ids (`gen_random_uuid()` defaults), `timestamptz`, `integer version default 1`, and **jsonb** for `source_ref`/`provenance_ref`/`output_payload`/`model_or_rule_version`/`upstream_lineage`/`subject_ref`/`current_payload` (DL-054 snapshots→jsonb). `model_or_rule_version` made jsonb specifically to carry provider+model identity structurally.
5. **No CHECK on `attesting_source`, `created_by`, `target_kind`** — LDM gives identifier-ish or explicitly open ("…") value sets, not closed enums.
6. **No `projects` table exists yet** → `project_id` is uuid NOT NULL without FK. Same for `user_id` (Supabase Auth wiring is not in this task). `version_pin` is uuid without FK (LDM §2.4: polymorphic — CHR id *or* assertion id; §5.4 integrity stays logical).
7. **Derived tables: §3.1 field set + `project_id` only** — universal overlay NOT applied to derived (rebuildable current-views; `current_chr_ref` carries lineage; `supersedes` history lives in CHR). Eight tables, including `outcome_confidence_current` (the task summary's seven-name list omitted it, but LDM §3.1's instance list names Outcome-Confidence — LDM is THE source). Table names `<kind>_current` are mine (LDM names no tables); `confidence_band` CHECK uses `low|medium|high` per Calibration Defaults §2.

### Deviations / environment notes

- **Ports shifted** in `config.toml` (`54331/54332/54333/54334/54337/54339`; shadow `54330`): an unrelated leftover Supabase stack (`intralign-oslo-local-e2e`, config no longer on disk) already holds the 54321–54327 defaults on this machine. Did not stop it (not mine to kill). `project_id = "oslo"`.
- `config.toml`: added `"derived"` to `api.schemas` so tests can exercise the derived tables through PostgREST.
- **TRUNCATE added to the REVOKE list** (task said UPDATE, DELETE): TRUNCATE empties a table while bypassing UPDATE/DELETE triggers — leaving it granted would be an append-only hole.
- **Triggers are statement-level** (`FOR EACH STATEMENT`), not row-level: row triggers don't fire on zero-row UPDATE/DELETE; statement-level blocks even those.
- `/tmp/oslo-ci-venv` lacked the project install (pre-existing: even `tests/positive/test_health.py` failed collection on missing `fastapi`). Ran `pip install -e ".[dev]"` into it — exactly what app-ci gate 1 does — no packages beyond the locked `pyproject.toml`. Also created throwaway `/tmp/oslo-dbtest-venv` (pytest + supabase-py, both already project/dev deps) for the first live run.
- No new project dependencies; no refactors; nothing committed (working tree only). Files touched: `code/supabase/**`, `code/tests/{positive,negative}/persistence/**`, this report.

## Engineering-manager review notes

**Review 1 (2026-06-12):** Migration SQL reviewed line-by-line — LDM-verbatim fields,
inline constraints (linter-compatible), single CREATE per canonical table, shared
trigger function, belt (REVOKE incl. TRUNCATE — partially closes the DTM-0001 TRUNCATE
linter residual) + braces (statement-level trigger). Derived schema correct: per-instance
tables, `epistemic_label='derived'` CHECK, CHR lineage FK, calibration-aligned band CHECK.
Worker's 7 LDM-gap flags reviewed — all defensible verbatim-binding choices; forwarded to
owner list. Scope clean.

**EM independent verification:** 81/81 tests (full suite, live Supabase); gate-4 linter
PASS; direct superuser psql in the db container: INSERT ok, UPDATE/DELETE both rejected
by `enforce_append_only()` — the strongest possible proof (trigger holds even above
role grants).

**Accepted follow-ups:** (1) RLS not yet enabled on these tables — local-dev acceptable;
RLS + workspace scoping is Phase II platform work (api/deps.py seam), must land before
Staging. (2) `seed.sql` SECURITY DEFINER probe is local-only test tooling — must NOT
ship beyond local (seeds don't run in deploys; noted). (3) `config.toml` exposes
`derived` schema to the API for test transport — re-examine posture before Staging.
(4) Owner items: §2.5 universal-overlay duplication; TRUNCATE linting addition.

## Approved by engineering manager

Status: Approved

Executive summary:
- Canonical append-only layer is real and database-enforced: four LDM §2 tables
  (single-statement CREATEs, CHECK-constrained enums, supersession self-FKs) guarded by
  REVOKE (belt) + a shared BEFORE UPDATE/DELETE exception trigger (braces); eight
  derived §3.1 projection tables in schema `derived`, CHR-lineaged, updatable.
  Phase I exit-gate item 4 (canonical append-only; derived separate) is demonstrated.

Verification:
- EM-run: `pytest tests/positive tests/negative` (live env) → **81 passed**.
- EM-run: `ci.gate_invariants --code-root .` → PASS.
- EM-run, superuser psql in supabase_db container: INSERT returns id; `UPDATE
  history_record` → ERROR enforce_append_only; `DELETE cognition_history_record` →
  ERROR enforce_append_only.
- Worker-run: `supabase db reset` applies clean; 24 live persistence tests green;
  57 passed/24 skipped without env (graceful skip verified).

Manual test plan:
- `cd code && supabase start && supabase db reset`; then in Studio (http://127.0.0.1:54333)
  try editing any row of `attested_assertion` → rejected with the append-only error.

Remaining risks:
- RLS/workspace scoping not yet on (Phase II; before Staging).
- Plpgsql-internal mutations + CTE forms evade the static linter; the DB trigger now
  backstops this at runtime (defense in depth achieved).
- LDM-gap flags 1–7 forwarded for owner confirmation (none block Phase II).

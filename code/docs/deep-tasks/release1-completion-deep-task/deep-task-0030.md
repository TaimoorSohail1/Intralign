# DTM-0030 — Projection materializer (`derived.*_current` upsert; live read model)

**Status:** In progress — owner authorized full completion plan 2026-06-26 · **Module:** DTM-0030 ·
**Phase:** Completion · **Contract:** LDM §3.1 (Live Cognition Projection) + Event Model §8 ·
**Depends:** the existing orchestration (`deep_pass.py`, `runner.py`) + CHR repo. · **Branch:**
`feat/release1-completion`.

## Goal / observable behavior

After a wave run appends its CHRs, the **`derived.*_current` projection rows are written** so the
Disclose read surface (DTM-0018 `ProjectionReader`) returns LIVE data. A `mark_current`-style step
in the orchestration reads each governed output's latest CHR and **upserts** the matching
`derived.<kind>_current` row: `current_payload` (the CHR's output snapshot), `current_chr_ref` (the
CHR id), `epistemic_label='derived'`, `confidence_value`/`confidence_band`/`conflict_state` (from
the evaluate output), `recomputed_at`. Recompute **supersedes** the projection (new
`current_chr_ref`) while the CHR log stays append-only. The projection is **rebuildable from the
latest CHR** (LDM §3.1) — losing it loses nothing canonical.

## Source docs / constraints

- **LDM §3.1** — the Live Cognition Projection row shape + "recompute appends CHR; the live
  projection is updated/replaced in sync; rebuildable from latest CHR per (project, output_kind,
  subject); carries no authority." Event Model §8 (`*_analysis_completed` → projection updates).
- `code/CONTEXT.md` (Derived vs Canonical; recompute appends never overwrites). `deep-task-
  decisions.md` #2, #4 (invariants). The 8 `derived.*_current` tables already exist
  (`code/supabase/migrations/20260612090100_derived_projection_tables.sql`).
- The read shape the materializer must satisfy = exactly what `backend/services/render/read_seam.py`
  `SupabaseProjectionReader.list_projection/get_projection` SELECTs (and the DTM-0018 render mappers
  consume): `projection_id, project_id, output_kind, current_payload, current_chr_ref,
  epistemic_label, confidence_value, confidence_band, conflict_state, recomputed_at`.

## Locked decisions (do not re-derive)

- **Materializer writes the DERIVED projection ONLY** — never a canonical row, never mutates/
  overwrites a CHR or attested assertion, never promotes Derived→Attested (Critical invariant,
  gate-4). It's a recomputable cache write (LDM §3.1).
- **Additive to the frozen topology** — add a materialize step at/after the existing `mark_current`
  node in `deep_pass.py` (or a thin `services` materializer the node calls); compose by calling
  existing builders. Do NOT change the cognition stages or the chain order.
- **Upsert keyed** on (project_id, output_kind, subject/projection_id) — recompute updates the
  current row to the new CHR; the projection is replaced, the CHR history grows. For list-kinds
  (finding/recommendation/issue/clarification) the subject is the per-item id; for singletons
  (outcome_confidence/caf) one row per project.
- **A rebuild path** — a function that rebuilds `derived.*_current` for a project from the latest
  CHRs (so a lost/empty projection store can be repopulated; supports the "rebuildable" clause + a
  one-shot backfill).
- No new dependency. No new migration (tables exist).

## Owned files / boundaries

- **OWN:** a materializer in `backend/services/render/` or `backend/responsibilities/disclose/`
  (e.g. `projection_writer.py`) + the upsert seam in `backend/services/persistence/` (a
  `ProjectionStore` with `upsert_projection`/`rebuild_for_project`) + the wiring in
  `backend/orchestration/deep_pass.py` (the materialize step) + `tests/{positive,negative}/disclose/`
  (or `/render/`). 
- **READ-ONLY:** the cognition stages (infer/evaluate/advise), the CHR repo (read its appended
  records), the render read seam (consume its row shape — match it), ALL existing migrations, the
  canonical stores. **No cognition change. No canonical write.**

## Packages / refactors — none new. No migration.

## Implementation instructions (TDD)

1. Red (pytest): after a run appends CHRs, the materializer upserts each `derived.*_current` row
   with the CHR payload + envelope, matching the read-seam shape; a re-run supersedes the projection
   (new `current_chr_ref`) — the read returns the latest; `rebuild_for_project` repopulates from
   CHRs. **Negatives:** materializer writes NO canonical/attested row, mutates NO CHR (append-only
   intact), never sets `epistemic_label` to attested / never promotes Derived→Attested; a failed
   materialize leaves the last-known-good projection (no partial corruption).
2. Build the `ProjectionStore.upsert_projection` + the materializer that maps appended CHRs →
   projection rows; wire the materialize step into `deep_pass.py` after `mark_current`. Provide
   `rebuild_for_project`.
3. Live e2e (if the runtime is available): trigger a run → the read endpoint returns the
   materialized finding/confidence/CAF (no seed harness needed).

## API / data / schema contracts

- Writes the existing `derived.*_current` tables (LDM §3.1 shape). Reads the CHR log. No schema
  change. The projection row must satisfy the DTM-0018 render mappers verbatim.

## Test plan

- **Positive:** materialize per output_kind (finding/issue/recommendation/clarification/confidence/
  caf/outcome_confidence/acceptance_impact); supersession on re-run; `rebuild_for_project`.
- **Negative (Critical):** no canonical/CHR mutation; no Derived→Attested; append-only preserved;
  last-known-good on failure.
- `pytest tests/positive tests/negative` (no regression) + ruff + gate-4 + gate-5 green.

## Manual checks (EM)

- Trigger a real run (or the orchestration test path) → query `derived.finding_current` etc. →
  rows present with the latest `current_chr_ref`; the DTM-0018 `GET …/findings` returns them; a
  re-run updates the row, CHR count grows.

## Done criteria

- The materializer upserts `derived.*_current` from appended CHRs (wired in orchestration), the
  read surfaces show live data, supersession + rebuild work, no canonical write / no CHR mutation
  (negative-proven), no new dep/migration, gates green. PR cites LDM §3.1. Ready for the command
  slices (DTM-0031+).

## Worker report

**Status: Ready for review.** Cites LDM §3.1 (Live Cognition Projection). No new
migration, no new dependency (`pyproject.toml` unchanged), no canonical-store
write in the materializer.

### Files added

- `backend/services/persistence/projection_store.py` — `SupabaseProjectionStore`:
  the Derived-only write seam over the eight `derived.*_current` tables (the same
  set the read seam SELECTs). Public surface = `supports` / `upsert_projection`
  (PostgREST `upsert(..., on_conflict="projection_id")`) / `list_for_project`
  (SELECT, used by rebuild). NO canonical-table surface by construction.
- `backend/responsibilities/disclose/projection_writer.py` — the materializer:
  `chr_to_projection_row` (pure CHR→row map), `ProjectionMaterializer`
  (`materialize_chr_ids` + `rebuild_for_project`), and the keying helpers
  `projection_subject` / `projection_id_for`.
- `backend/responsibilities/disclose/__init__.py`,
  `backend/services/persistence/__init__.py` — exports.
- `tests/positive/disclose/test_projection_materializer.py` (8 tests),
  `tests/negative/disclose/test_projection_materializer_negative.py` (7 tests).

### Files modified (additive wiring only)

- `backend/orchestration/graphs/deep_pass.py` — added an OPTIONAL `materializer`
  param + a thin `materialize_projection` node on the SUCCESS path only:
  `mark_current -> materialize_projection -> END`. When no materializer is
  injected it is a pass-through, so the frozen backbone behavior (incl.
  durable-resume / failure-edge tests) is unchanged. The cognition stages and the
  chain order (`append_chrs -> stage_infer -> stage_evaluate -> stage_advise`) are
  untouched.
- `backend/orchestration/runner.py` — threaded the optional `materializer` through
  `run` / `submit_trigger` to the graph factory (default `None`; every existing
  caller/test is unaffected).

### How upsert + supersession + rebuild work

- **Upsert keyed.** Each row's `projection_id` is a deterministic
  `uuid5(project_id, output_kind, subject)`. List-kinds key on the per-item
  subject (`finding_id` / `issue_id` / `recommendation_id` / `clarification_id`);
  singletons (`confidence` / `caf` / `outcome_confidence`) key on one row per
  project; `acceptance_impact` keys per `uar_ref`. Same triple → same id → the
  store `upsert` REPLACES the current row.
- **Supersession.** A recompute appends a NEW CHR for the same subject (canonical,
  via the frozen retain stage) and the materialize step upserts the matching live
  row to the new `current_chr_ref`/payload. The CHR log grows append-only; the
  projection is replaced in sync (proven: `test_rerun_supersedes_projection_same_row_new_chr`).
- **Envelope.** `epistemic_label` is PINNED `'derived'`; `confidence_value`/`band`
  come from the CHR payload (`index`/`band`, else the EVALUATE-owned `band_for`
  — no invented band); `conflict_state` is `contested` iff the snapshot marks a
  conflict, else `none`. Output matches the read-seam shape verbatim and is fed
  through the DTM-0018 render mappers in the tests (`finding`/`confidence`/`caf`/
  `recommendation`).
- **Rebuild.** `rebuild_for_project(project_id)` reads the append-only CHR log
  (via `chrs_for_project` when available, else `latest_for_output` per kind),
  reduces to the latest CHR per (output_kind, subject), and upserts each — so a
  lost/empty projection store is restored from CHRs alone (LDM §3.1 "rebuildable";
  supports a backfill replacing the seeded dev harness). Proven:
  `test_rebuild_for_project_repopulates_from_latest_chrs`.

### Negatives proven (Critical, gate-4 aligned)

- **No canonical write.** AST scan over both DTM-0030 modules: no `.table(...)`
  names any canonical table; the store targets only `derived.*_current` tables;
  `SupabaseProjectionStore` has no `insert_assertion`/`insert_acceptance`/
  `insert_history`/`append` surface.
- **No CHR mutation / append-only intact.** The materializer uses the CHR repo
  READ-only (`get`/lister); an exploding-`append` fake proves `append` is never
  invoked.
- **No Derived→Attested.** Every materialized row carries `epistemic_label='derived'`
  for all eight kinds, even when the CHR payload carries a stray
  `epistemic_state="attested-oslo"` (it does not leak).
- **Last-known-good on failure.** A store that raises mid-batch leaves the prior
  good row byte-identical and the CHR log unmutated (no partial corruption).
- Unmaterializable kinds (`reliability` etc.) are skipped — no row written.

### Verify (exact commands + results)

- `cd code && .venv/bin/pytest tests/positive/disclose tests/negative/disclose -q`
  → **15 passed**.
- `.venv/bin/pytest tests/positive tests/negative -q` → **589 passed, 65 skipped**
  (the skips are the live-Supabase suites; no local stack), **0 failed** — no
  regression.
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS**.
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS** (the materializer
  is correctly NOT seen as a CHR-append site — it only `get`s CHRs).
- `git status` confirms: no new migration under `supabase/migrations/`,
  `pyproject.toml` unchanged. Unrelated working-tree changes (`vite.config.ts`,
  `scripts/`) preserved, untouched.

### Flags

- The live end-to-end leg (run → `derived.finding_current` populated → DTM-0018
  `GET …/findings` returns it) is NOT exercised here because no local Supabase
  stack is configured (the live deep_pass suite skips for the same reason). The
  in-memory positive suite proves the CHR→row mapping and supersession against the
  real render mappers; the wiring point (`materialize_projection` after
  `mark_current`, with `materializer` threaded through the runner) is in place for
  the live run once a stack + an injected `ProjectionMaterializer` are available.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Projection materializer built: `SupabaseProjectionStore` (Derived-only upsert over the 8 existing
  `derived.*_current` tables) + `ProjectionMaterializer` (`materialize_chr_ids` + `rebuild_for_project`)
  wired as an OPTIONAL pass-through `materialize_projection` node after `mark_current` in deep_pass.
  Read surfaces now show live materialized data from appended CHRs. LDM §3.1.

Verification (EM re-ran):
- `.venv/bin/pytest tests/positive tests/negative -q` → **589 passed, 65 skipped** (15 new; no
  regression). ruff clean; gate-4 PASS; gate-5 PASS.
- No new migration (8 derived tables already exist); `pyproject.toml` unchanged (no dep).
- Derived-only confirmed: the store/materializer reference canonical tables only in docstrings (what
  they must NOT touch); no canonical/CHR write surface. Negatives: AST scan (no canonical write),
  exploding-append fake (no CHR mutation), all 8 kinds stay `derived` (no Derived→Attested),
  last-known-good on mid-batch failure.
- Additive topology: `materialize_projection` is pass-through when no materializer injected — frozen
  backbone (durable-resume / failure-edge) unchanged.

Manual test plan:
- Inject a `ProjectionMaterializer` at a configured run → trigger → `derived.finding_current` holds
  rows with the latest `current_chr_ref`; `GET …/findings` returns them; re-run supersedes the row,
  CHR log grows.

Remaining risks / flagged:
- Live e2e (real Supabase run → query → GET) not exercised locally (no Supabase stack; same skip as
  the existing live deep_pass suite). Wiring is in place + unit-proven; the runner now threads the
  optional materializer. Will be exercised once DTM-0041 stands up the backing services.

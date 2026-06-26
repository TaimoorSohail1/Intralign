# DTM-0030 — Projection materializer (`derived.*_current` upsert; live read model)

**Status:** Planned (ungated — can start on user authorization) · **Module:** DTM-0030 · **Phase:**
Completion · **Contract:** LDM §3.1 (Live Cognition Projection) + Event Model §8 · **Depends:** the
existing orchestration (`deep_pass.py`, `runner.py`) + CHR repo.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

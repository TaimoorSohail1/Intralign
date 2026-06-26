# DTM-0031 — Platform persistence (project / analysis_run / notification tables + repos)

**Status:** In progress — OWNER-APPROVED migration (2026-06-26) · **Module:** DTM-0031 · **Phase:**
Completion · **Contract:** LDM §6 (physical binding) + API Contract §5 + Data Model v1.2 ·
**Depends:** the existing Supabase migrations + persistence service. · **Branch:**
`feat/release1-completion`.

## Goal / observable behavior

The platform tables the read seam already expects exist, with repos to read+write them. A new
**additive** migration creates `project`, `analysis_run`, `notification` (workspace-scoped, RLS),
and `backend/platform/` gains repos. The DTM-0018 read seam (`SupabaseProjectionReader.list_projects
/get_project/list_analysis_runs/list_notifications`) — which already queries these tables — now hits
real tables. This unblocks the project/analysis/notification command slices (DTM-0032/0034/0035).

## Source docs / constraints

- **OWNER GATE CLEARED:** the owner authorized this migration (decisions file "Owner authorization").
  Still obey Deployment Governance §5 (migrations additive + forward-only; **canonical tables stay
  append-only and UNTOUCHED**) + gate-4 (the migration linter rejects canonical-table mutations).
- **LDM §6** (Supabase Postgres holds Projects/Users/Orgs/Artifacts-meta) + **§2.4/§5** (lifecycle).
  **API Contract §5** + **Data Model v1.2** (`shared/entities.py` Project/AnalysisRun/Notification
  DTO fields — the table columns must back these). The **State Model** spec for the lifecycle enums
  (project lifecycle, AnalysisRun status, notification state).
- The **read seam is the source of the expected shape** — `backend/services/render/read_seam.py`
  `SupabaseProjectionReader` SELECTs specific columns from `project`/`analysis_run`/`notification`;
  the migration columns MUST match those + the `shared/entities.py` DTOs. Reconcile any mismatch by
  the Data Model / read-seam; if genuinely ambiguous ⇒ STOP/escalate (ANTI_ASSUMPTION).

## Locked decisions (do not re-derive)

- **Platform tables are NOT canonical** — they may be UPDATE-able (project lifecycle, AnalysisRun
  status transitions, notification view/dismiss state). The append-only discipline applies to the
  canonical epistemic store ONLY (attested/CHR/UAR/history) — **do not touch those tables**.
- **Migration:** one new file `code/supabase/migrations/<TS>_platform_tables.sql` with a timestamp
  **strictly after** the latest existing migration (currently `20260617120000`). Additive: CREATE
  the 3 tables + indexes + RLS (workspace-scoped, mirroring the canonical tables' grant style). No
  ALTER/REVOKE on canonical tables.
- **Repos** in `backend/platform/` (e.g. `project_repo.py`, `analysis_run_repo.py`,
  `notification_repo.py`) — read + write seams over the Supabase client (mirror
  `services/persistence` style). The write methods are used by DTM-0032/0034/0035; this slice
  provides them + read.
- Workspace scoping + RLS per API Contract §3 (single workspace per user in R1). No new dependency
  (Supabase client already present).

## Owned files / boundaries

- **OWN:** `code/supabase/migrations/<TS>_platform_tables.sql` (NEW) · `backend/platform/**` (repos
  + `__init__`) · wiring the read seam to the real tables IF a column mismatch needs reconciling
  (minimal, in `read_seam.py`) · `shared/entities.py` only if a DTO field must align to the Data
  Model (additive) · `tests/{positive,negative}/platform/**`.
- **READ-ONLY:** canonical migrations + tables (NEVER touch), cognition/orchestration, the render
  mappers, the frontend.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest): the repos create/read/update a project (lifecycle), an analysis_run (status
   transition), a notification (view/dismiss state); workspace scoping filters correctly; the read
   seam returns rows matching the DTM-0018 DTO shape. **Negatives:** the migration touches NO
   canonical table (assert via the migration linter / a test that canonical tables are unaltered);
   cross-workspace read returns nothing; platform writes never write a canonical/CHR row.
2. Author the migration (additive, RLS); build the repos; reconcile the read-seam columns if needed.
3. Run the migration linter / gate-4 to confirm no canonical-table mutation.

## API / data / schema contracts

- Tables back the `shared/entities.py` Project/AnalysisRun/Notification DTOs (Data Model v1.2) +
  the read-seam SELECT columns. Lifecycle/status/state enums per the State Model spec. No canonical
  schema change.

## Test plan

- **Positive:** project create/get/update-lifecycle; analysis_run insert/get/status; notification
  insert/get/view/dismiss; workspace scoping; read-seam shape matches DTOs.
- **Negative (Critical):** migration alters no canonical table (gate-4 / linter); cross-workspace
  isolation; platform write never writes canonical/CHR.
- `.venv/bin/pytest tests/positive tests/negative` (no regression) + ruff + gate-4 (incl. migration
  linter) + gate-5 green.

## Manual checks (EM)

- Apply the migration to a local Supabase (or inspect the SQL) → 3 tables + RLS, canonical tables
  untouched; the repos round-trip a project/run/notification; the read seam returns them.

## Done criteria

- Platform tables migrated (additive, canonical untouched), repos read+write, read seam on real
  tables, workspace-scoped, gate-4 (migration linter) green, no canonical mutation (negative-proven),
  no new dep. PR cites LDM §6 / API §5. Unblocks DTM-0032/0034/0035.

## Worker report

**Status: Ready for review.** Additive platform persistence built TDD-first; all gates green;
canonical store UNTOUCHED (gate-4 negative-proven); no new dependency. read_seam.py + entities.py
needed NO reconciliation — the table columns matched the read-seam SELECTs and the DTOs exactly.

### Migration — `code/supabase/migrations/20260626120000_platform_tables.sql` (NEW; one file)

Timestamp `20260626120000` is strictly after the latest existing migration (`20260617120000`).
**Additive only** — three brand-new `public` relations; no ALTER/UPDATE/DELETE/DROP/REVOKE on any
canonical table. Follows the DERIVED/updatable grant style (migration `20260612090100`), NOT the
canonical append-only pattern: **no append-only trigger, no mutation REVOKE** on the platform tables
(they are meant to be mutable — project lifecycle, run status, notification view/dismiss).

| Table | Columns | Mutable lifecycle | RLS / scoping |
|---|---|---|---|
| `project` | `project_id` pk · `workspace_id` · `created_by_user_id` · `title` · `description` · `lifecycle_state` (CHECK created/orienting/oriented/deep_analyzing/analyzed/archived) · `current_confidence_state_id` · `created_at` · `updated_at` | `lifecycle_state` | RLS on; policy isolates by `workspace_id`; index `(workspace_id, created_at desc)` |
| `analysis_run` | `analysis_run_id` pk · `project_id` (FK project) · `run_type` (CHECK fast/deep_analysis_pass) · `run_status` (CHECK queued/running/completed/failed/cancelled/superseded) · `previous_run_id` (self-FK) · `started_at` · `completed_at` · `created_at` · `updated_at` | `run_status` | RLS on; policy isolates via parent project's workspace; index `(project_id, started_at desc)` |
| `notification` | `notification_id` pk · `workspace_id` · `project_id` (FK project) · `source_object_type` (CHECK finding/recommendation/analysis_run/comment/shared_artifact) · `source_object_id` · `event_type` · `target_user_id` · `state` (CHECK created/viewed/dismissed/expired) · `created_at` · `viewed_at` · `dismissed_at` · `expired_at` | `state` | RLS on; policy isolates by `workspace_id`; index `(workspace_id, created_at desc)` |

Enum CHECK lists are the verbatim Data Model v1.2 / State Model values (`shared/entities.py`
`ProjectLifecycle` / `AnalysisRunType` / `AnalysisRunStatus` / `NotificationSourceType` /
`NotificationState`). Grants: `grant all … to anon, authenticated, service_role` (mutable). RLS
policies bind direct anon/authenticated access to the request `app.workspace_id` GUC; the backend
`service_role` bypasses RLS by Postgres rule, so the repos' explicit `.eq(workspace_id|project_id,…)`
filters are the backend's scoping (policies = defence in depth).

### Repos — `backend/platform/` (NEW; mirror `services/persistence` Supabase-client style)

- `project_repo.py` `SupabaseProjectRepository`: **write** `create`, `update_lifecycle`, `update`;
  **read** `get`, `list_for_workspace`.
- `analysis_run_repo.py` `SupabaseAnalysisRunRepository`: **write** `create`, `update_status`
  (+optional `completed_at` etc.); **read** `get`, `list_for_project`.
- `notification_repo.py` `SupabaseNotificationRepository`: **write** `create`, `mark_viewed`,
  `mark_dismissed`; **read** `get`, `list_for_workspace`.
- `__init__.py` exports all three. Each repo writes its ONE platform table only — no canonical-table
  surface, never appends a CHR (AST-scanned + behaviourally proven in the negative suite). Write
  methods are for DTM-0032/0034/0035; read methods + read-seam are exercised now.

### Column → read-seam + DTO mapping (no reconciliation required)

Every column the read seam SELECTs and orders by is present, and every DTO field is backed:

- `list_projects(workspace_id)` filters `workspace_id`, orders `created_at` ✓; `get_project` by
  `project_id` ✓ → backs `Project` DTO (project_id/workspace_id/created_by_user_id/title/description/
  lifecycle_state/current_confidence_state_id/created_at/updated_at).
- `list_analysis_runs(project_id)` filters `project_id`, orders `started_at` ✓; `get_analysis_run`
  by `analysis_run_id` ✓ → backs `AnalysisRun` DTO (analysis_run_id/project_id/run_type/run_status/
  previous_run_id/started_at/completed_at).
- `list_notifications(workspace_id)` filters `workspace_id`, orders `created_at` ✓ → backs
  `Notification` DTO (notification_id/workspace_id/project_id/source_object_type/source_object_id/
  event_type/target_user_id/state/created_at/viewed_at/dismissed_at/expired_at).

Round-trip proven end-to-end: rows written via the repos are read back through the real
`SupabaseProjectionReader` over a shared in-memory PostgREST fake
(`tests/support/fake_supabase.py`, the house "fake the transport, exercise the real seam" style).
**No ambiguity flagged** — the read seam and the Data Model agreed; nothing was guessed.

### Tests (TDD red→green)

- `tests/positive/platform/test_platform_repos.py` — project create/get/lifecycle-update;
  analysis_run insert/get/status-transition + project scoping; notification insert/view/dismiss +
  workspace scoping; read-seam lists the repo-written rows in DTO shape; project workspace scoping.
- `tests/negative/platform/test_platform_repos_negative.py` (Critical) — **migration touches no
  canonical table** (asserted via the gate-4 linter `lint_migration_sql` on the new file, plus a
  whole-identifier executable-SQL scan); repos name no canonical table (AST) and expose no canonical
  write method; a full round-trip leaves the canonical/CHR buckets empty (only project/analysis_run/
  notification exist); cross-workspace project + notification reads return empty.
- `tests/support/fake_supabase.py` (NEW) — minimal in-memory PostgREST-shaped client fake (the
  operators the repos + read seam use); platform-only, simulates no canonical semantics.

### Verify — exact commands + results

```
$ cd code && .venv/bin/pytest tests/positive tests/negative -q
604 passed, 65 skipped, 1 warning in 3.62s          # 65 skips = live-Supabase suites (CI has none)

$ .venv/bin/pytest tests/positive/platform tests/negative/platform -q
15 passed in 0.04s

$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/python ci/gate_invariants.py
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.

$ .venv/bin/python ci/gate_observability.py
[gate-5 observability] PASS: every CHR-append call-site emits 'cognition_history_record_appended', …
```

Confirmed: **exactly one** new migration file (`20260626120000_platform_tables.sql`); **no canonical
table touched** (gate-4 green; `git status` shows only the new platform migration + `backend/platform`
+ `tests/{positive,negative}/platform` + `tests/support`); **no new dependency** (`pyproject.toml`
unchanged; Supabase client already present); `read_seam.py` and `shared/entities.py` UNTOUCHED (no
reconciliation needed). Working tree otherwise preserved (the unrelated `vite.config.ts` /
`code/scripts/` changes left intact). Staged the green change; did NOT commit.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Owner-approved additive migration `20260626120000_platform_tables.sql` creates `project`,
  `analysis_run`, `notification` (mutable, RLS workspace-scoped, derived/updatable grant style — NOT
  canonical append-only). `backend/platform/{project,analysis_run,notification}_repo.py` provide
  read+write. read_seam.py + entities.py needed NO reconciliation (columns matched exactly).

Verification (EM re-ran):
- `.venv/bin/pytest tests/positive tests/negative -q` → **604 passed, 65 skipped** (15 new; no
  regression). ruff clean.
- **gate-4 PASS** — migration linter confirms NO canonical-table mutation; grep confirms no
  ALTER/DROP/REVOKE on attested_assertion/cognition_history_record/user_acceptance_record/history_record.
- Migration CREATEs only the 3 platform tables; exactly one new migration file. No new dependency.
- Negatives: platform repos write no canonical/CHR row; cross-workspace reads empty; round-trip
  leaves canonical buckets empty.

Manual test plan:
- Apply the migration to a local Supabase → 3 tables + RLS, canonical untouched; repos round-trip a
  project/run/notification; the read seam returns them.

Remaining risks:
- Migration not yet applied to a live Supabase (DTM-0041 stands up the stack); SQL inspected +
  linter-clean. RLS relies on service_role bypass + backend `.eq(workspace_id)` scoping (the house
  pattern) — re-verify once auth (DTM-0036) lands the real Principal.

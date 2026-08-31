# DTM-0032 — REST: analysis triggers (:fast / :deep / :cancel) → submit_trigger + materialize

**Status:** In progress · **Module:** DTM-0032 · **Phase:** Completion · **Contract:** API §5
(122–124) + Event Model §8.8 · **Depends:** DTM-0030 (materializer), DTM-0031 (analysis_run table).
**Branch:** `feat/release1-completion`.

## Goal / observable behavior

A user can start an analysis from REST and see live results. New command router:
- `POST /v1/projects/{pid}/analysis-runs:fast` → AnalysisRun(`queued`) + `fast_analysis_requested`.
- `POST /v1/projects/{pid}/analysis-runs:deep` (`{trigger_source}`) → `deep_analysis_requested`.
- `POST /v1/analysis-runs/{rid}:cancel` → AnalysisRun(`cancelled`).
Each wires the EXISTING `backend/orchestration/runner.py` `submit_trigger("deep_pass", …)` and
persists the run via the DTM-0031 `analysis_run_repo`. The run is launched with the DTM-0030
`ProjectionMaterializer` injected so `derived.*_current` is populated → the read surfaces show the
results. Returns the affected `AnalysisRun` DTO + emits the §8.8 event. `Idempotency-Key` honored;
workspace-scoped.

## Source docs / constraints

- API §5 (122–124) — the three endpoints (path/method/request/response/idempotency/events). Event
  Model §8.8 — `fast/deep_analysis_requested/started/completed`, AnalysisRun + Project transitions.
  `code/CONTEXT.md` (Fast/Deep Pass, mode + confidence_stage attrs). decisions #4, #5.
- Code: `backend/orchestration/runner.py` (`submit_trigger` signature, the materializer param added
  in DTM-0030), `backend/platform/analysis_run_repo.py` (DTM-0031 write), `backend/api/v1/routers/
  analysis_runs.py` (the existing GET router — ADD the command router beside it, don't break reads),
  `backend/api/deps.py` (Principal + workspace scoping + idempotency), `backend/responsibilities/
  disclose/projection_writer.py` (inject the materializer).

## Locked decisions (do not re-derive)

- **Wire the existing seam — invent no orchestration.** The command builds a `TriggerClaim` and
  calls `submit_trigger`; it does not re-implement the run. Inject the `ProjectionMaterializer` so
  results materialize (DTM-0030).
- **Command router is separate/additive** — a new `analysis_commands` router (or POST methods on a
  command router); the DTM-0018 GET read router + its read-mostly negatives stay green.
- **Async semantics:** the run is durable/async (returns `queued`); the UI polls the GET endpoint.
  Coalescing/cancel per the runner's existing behavior.
- Emit the §8.8 event names verbatim (gate-5 vocab). `Idempotency-Key` → same run on retry (API
  §10). Workspace-scoped (404 cross-workspace). No new dependency.

## Owned files / boundaries

- **OWN:** `backend/api/v1/routers/analysis_commands.py` (NEW, or POST on a command router) +
  include in `v1/__init__.py` · `backend/api/v1/schemas/` (request bodies if any) · minimal glue in
  `backend/platform/analysis_run_repo.py` only if a status-transition helper is missing ·
  `tests/{positive,negative}/api/**`.
- **READ-ONLY:** the runner/orchestration internals (call, don't change), the materializer, the read
  router + read seam, migrations, cognition.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest, mirror `tests/positive/api/conftest.py` TestClient + override pattern): each command
   creates/persists an AnalysisRun, calls `submit_trigger` (assert via a fake runner), returns the
   DTO, emits the §8.8 event; idempotency-key returns the same run; cancel transitions status.
   **Negatives:** unauth 401; cross-workspace 404; the read surface stays GET-only (no regression);
   the command emits no canonical write itself (the run does, via the frozen retain path); invalid
   transition 409.
2. Build the command router wiring `submit_trigger` (materializer injected) + the analysis_run repo
   persistence; include in `v1/__init__.py`; regenerate OpenAPI is a frontend concern (note it).

## API / data / schema contracts

- Returns the `AnalysisRun` DTO (Data Model v1.2). Emits `fast/deep_analysis_requested`,
  `analysis_cancelled`. No schema change.

## Test plan

- **Positive:** :fast/:deep create a queued run + event + submit_trigger called (materializer
  injected); :cancel; idempotency; workspace scoping.
- **Negative:** 401/404/409; read router unchanged (read-mostly negatives green); no direct
  canonical write from the command.
- `.venv/bin/pytest tests/positive tests/negative` + ruff + gate-4 + gate-5 (new event vocab) green.

## Manual checks (EM)

- With backing services (or a fake runner): POST :fast → run queued + event; the run materializes
  `derived.*_current`; GET …/findings then returns live data.

## Done criteria

- The 3 analysis command endpoints wire `submit_trigger` (materializer injected) + persist via the
  repo + emit §8.8 events, idempotent + workspace-scoped, read router unchanged, gates green, no new
  dep. PR cites API §5 / Event §8.8. Ready for DTM-0033.

## Worker report

**Status: Ready for review.**

### What shipped — 3 command endpoints (new additive router, GET reads untouched)

New `backend/api/v1/routers/analysis_commands.py` (tag `analysis_commands`),
included in `v1/__init__.py` AFTER the read routers. The DTM-0018 GET router
(`analysis_runs.py`) is byte-for-byte unchanged.

| Endpoint | Persist (DTM-0031 repo) | `submit_trigger` wiring | Event (EM §8.8) | Status |
|---|---|---|---|---|
| `POST /v1/projects/{pid}/analysis-runs:fast` | `repo.create({…, run_type=fast_analysis_pass, run_status=queued})` | `submit_trigger("deep_pass", TriggerClaim(reanalysis, info_changed=True), materializer=<injected>)` | `fast_analysis_requested` | `201` AnalysisRun(queued) |
| `POST /v1/projects/{pid}/analysis-runs:deep` body `{trigger_source}` | `repo.create({…, run_type=deep_analysis_pass, run_status=queued})` | same seam; `trigger_source` → `claim.source` | `deep_analysis_requested` | `201` AnalysisRun(queued) |
| `POST /v1/analysis-runs/{rid}:cancel` | `repo.update_status(rid, "cancelled")` | — (cancel transitions the persisted run; no new run) | `analysis_cancelled` | `200` AnalysisRun(cancelled) |

Each `:fast`/`:deep` returns `analysis_run_to_dto(row)` (the Data Model v1.2
`AnalysisRun` DTO via the existing render mapper). The materializer is injected
into `submit_trigger` so a successful deep pass upserts `derived.*_current`
(DTM-0030, LDM §3.1) → the read surfaces show live results.

**Wiring is via DI providers in `backend/api/deps.py`** (all overridable in
tests, wired to the real Supabase/runner seams in prod): `get_analysis_run_repo`
(SupabaseAnalysisRunRepository), `get_trigger_submitter` (runner.submit_trigger),
`get_materializer` (ProjectionMaterializer(SupabaseProjectionStore, ChrRepository)),
`get_event_emitter` (ObservedEventEmitter-wrapped collector), plus the
`Idempotency-Key` header dep + an in-process idempotency store.

### TriggerClaim shape (flagged for review)

The runner's `submit_trigger` takes a `TriggerClaim`. The command builds:
`TriggerClaim(trigger_type=REANALYSIS, project_id=pid, information_changed=True,
source=<trigger_source>)`. **Rationale:** the five valid triggers
(`adapt/triggers.py`) are `promotion / knowledge-change / clarification /
user-action / reanalysis`; a user-initiated analysis request is an explicit
**reanalysis** (TriggerType.REANALYSIS), and it carries an information-change
claim (`information_changed=True`) so it passes the A4.6 gate (intake/acceptance
ALONE is not a trigger). The API §5 `fast`/`deep` distinction is carried on the
persisted `run_type`, not on the trigger vocabulary — R1 registers exactly one
durable graph (`deep_pass`), so both passes route through it. **Open for EM
confirmation:** whether `user-action` would be preferred over `reanalysis` for
the manual `:fast`/`:deep` source — both are valid five-vocabulary triggers with
`information_changed=True`; I chose `reanalysis` per the trigger enum's
"explicit/auto reanalysis" semantics.

### Events added + gate-5 update

New `EVENT_NAMES_ANALYSIS = ("fast_analysis_requested", "deep_analysis_requested",
"analysis_cancelled")` (EM §8.8 order, verbatim) in
`backend/services/observability/events.py`, appended to the `EVENT_NAMES` union.
The run-lifecycle names (`*_analysis_started/completed`) are engine-produced via
the recompute backbone (WA00R) — deliberately NOT pinned as command events.
Gate-5 (`ci/gate_observability.py`) updated in lockstep: `EXPECTED_EVENT_NAMES_ANALYSIS`
+ entries in `_CONTRACT_VOCABULARIES` and `_UNION_NAME_ORDER` + the expected
union. Both gate-5 test fixtures updated:
`tests/positive/observability/test_gate_observability.py` (new verbatim test +
11-way union assertion) and `tests/negative/observability/test_gate_observability_negative.py`
(the synthetic `GOOD_EVENTS_PY` grew the ANALYSIS leg; the missing-assignment
count 11→12 and the union-drop tamper string updated).

### Idempotency / scoping

- **`Idempotency-Key`** → keyed by `(key, route)` in an in-process store
  (`reset_idempotency_store()` test seam). A retry returns the SAME run with NO
  second `repo.create` and NO second `submit_trigger` (proven). R1 single-dyno;
  the cross-dyno Redis store is the flagged follow-up (matches the runner's own
  in-memory coalescing-guard scope).
- **Workspace-scoped:** every command resolves the project via
  `reader.get_project` and 404s when absent or in another workspace (existence
  not leaked, §12). `:cancel` resolves the run's parent project the same way.
- **401** when unauthenticated (the `current_principal` bearer contract).
- **409** when cancelling a run not in `queued`/`running` (illegal transition, §9).

### Epistemic-boundary purity (proven)

The command persists the PLATFORM `analysis_run` row ONLY — it imports/uses no
CHR repo and touches no canonical store (negative test greps the router source
for `chr_repo`/`ChrRepository`/`AttestedAssertion`/`cognition_history_record`).
The canonical CHR append happens inside the durable run via the frozen retain
path, not the transport.

### Read-surface guard kept green

`tests/negative/api/test_read_surface_negatives.py` `_dtm0018_routes()` was
narrowed to the read routers BY TAG (the command router lives under the same
`/v1` prefix but is a separate concern, decision #3/#4). The guard still proves
the DTM-0018 read routers are GET-only; a new negative
(`test_read_routers_stay_get_only_after_commands_added`) re-asserts this after
the command router is added.

### Verify (exact commands + results)

```
$ cd code && .venv/bin/pytest tests/positive tests/negative -q
619 passed, 65 skipped, 1 warning in 3.76s
  (65 skips = pre-existing live-Supabase/LLM tests; OTel trace-export errors are
   the disabled exporter, not test failures)

$ .venv/bin/ruff check .
All checks passed!

$ .venv/bin/python ci/gate_invariants.py        # gate-4
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module,
no canonical-table mutations in migrations.

$ .venv/bin/python ci/gate_observability.py      # gate-5 (WITH the new events)
[gate-5 observability] PASS: every CHR-append call-site emits
'cognition_history_record_appended', the per-contract A6 vocabularies are pinned
verbatim (union consistent), and the replay harness is present.
```

App composition verified: all three POST routes register, the GET routes
coexist, `app.openapi()` builds with the three `:fast`/`:deep`/`:cancel` paths in
the spec.

**Confirmed:** no new dependency (no requirements/pyproject change), no migration
(no `supabase/migrations/` change), GET read router untouched. Unrelated
working-tree changes (`frontend/vite.config.ts`, `scripts/`) preserved.

OpenAPI/Orval regeneration is a frontend concern (DTM-0039) — noted, not done here.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- New additive `analysis_commands` router: `:fast`/`:deep` create+persist a queued AnalysisRun (via
  the DTM-0031 repo), call `submit_trigger("deep_pass", TriggerClaim, materializer=<injected>)` so
  results materialize (DTM-0030), and emit `fast/deep_analysis_requested`; `:cancel` transitions
  status + emits `analysis_cancelled`. DI providers in deps.py (all test-overridable). API §5/Event §8.8.

Verification (EM re-ran): `.venv/bin/pytest tests/positive tests/negative -q` → **619 passed, 65
skipped** (15 new; no regression). ruff clean; gate-4 PASS; gate-5 PASS (new event names pinned in
vocab + both fixtures). No new dep, no migration. GET read router `analysis_runs.py` unchanged.

Negatives proven: 401 unauth; 404 cross-workspace (project + run); 409 invalid cancel transition;
Idempotency-Key returns the same run (no second persist/trigger); command writes no canonical row
(the durable run does, via frozen retain); read-surface guard re-asserted (narrowed to read-router
tags — correct now that command routers exist).

Remaining risks / accepted: TriggerClaim uses `REANALYSIS` + `information_changed=True` (passes the
A4.6 gate; reasonable for a user-initiated analysis — `user-action` was the alternative). R1
idempotency store is single-dyno (Redis cross-dyno = a later ops follow-up, matches the runner's
coalescing scope).

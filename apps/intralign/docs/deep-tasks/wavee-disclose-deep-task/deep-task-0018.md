# DTM-0018 — REST exposure: api/v1 read routers + render DTOs (the layer the UI consumes)

**Status:** Ready for review — owner authorized Wave E start 2026-06-25 · **Module:** DTM-0018 ·
**Phase:** VI (Wave E) · **Contract:** **IC-WE-DISCLOSE** (presentation transport) + **ADR-0003**
(REST `/v1`) · **Depends:** Waves A–U (present in this branch via the stack), Data Model v1.2. ·
**Note:** Wave U (#69) not yet merged to `main`; its code is in this branch; owner directed start.

## Goal / observable behavior

The frontend can fetch the governed objects over REST. `backend/api/v1/` exposes **read-mostly**
GET endpoints that present what Waves A–U produced — Projects, Findings, Issues, Recommendations,
Confidence/CAF/Outcome Confidence, the Cognition-History trail, User Acceptance Records + Plan
Facts, Acceptance-Impact, Notifications — each mapped by `services/render` into **Data Model v1.2
DTOs** (`shared/entities.py`), exposed verbatim. The OpenAPI grows from `/health` to the domain
surface; `npm run api:gen` regenerates the Orval client and the drift gate (`tsc`) stays green.
**The API presents; it never computes, mutates cognition, or accepts** (writes stay on the
existing capture/acceptance seams).

## Source docs / constraints

- IC-WE-DISCLOSE E0/E1 (Disclose presents; epistemic labels travel with every object); ADR-0003
  (REST `/v1`, DTOs = Data Model v1.2 verbatim, the Orval drift gate); the **API Contract Spec**
  (`20_handoff/interfaces/`) + **UI_SCREEN_INVENTORY** (which operations each screen needs);
  `deep-task-decisions.md` #3–#5, #9, #11; ANTI_ASSUMPTION.

## Locked decisions (from decisions file — do not re-derive)

- **Read-mostly:** the present endpoints are GET (list/detail) over governed objects. **No new
  write/mutation path** — acceptance/capture stay on the existing Wave-A/U seams (the
  Recommendation accept affordance, DTM-0021+, routes to the existing capture).
- **Render maps cognition → DTO:** `services/render` converts internal `epistemic.py` types
  (Finding/Issue/Confidence/CAF/…/CHR/UAR/PlanFact/AcceptanceImpact) into the external
  `shared/entities.py` DTOs. **Internal types are never serialized verbatim** (negative-proven).
  The DTO carries the **epistemic label** (Attested/Derived + confidence band + conflict) so the
  UI can render it without re-deriving.
- **Endpoints** bind to the API Contract Spec + the screen inventory's operation list (e.g.
  `GET /projects`, `GET /projects/{id}`, `…/findings`, `…/recommendations`, `…/issues`,
  `…/confidence`, `…/history`, `…/acceptance`, `…/notifications`). Pull each path/DTO from the
  spec — **do not invent** an endpoint a screen doesn't need or a DTO field not in Data Model v1.2
  (⇒ STOP/escalate on a gap).
- **Auth/scoping:** reuse `api/deps.py` (Supabase-JWT + workspace scoping + idempotency). **No
  migration.**
- Routers live under `api/v1/routers/` (the catalog already names them); `v1/__init__.py`
  includes them; `app.py` keeps serving `/openapi.json`.

## Owned files / boundaries

- **OWN (additive):** `backend/api/v1/routers/**` (the GET routers) · `backend/api/v1/__init__.py`
  (include them) · `backend/api/v1/schemas/**` (request inputs if any) · `backend/services/render/**`
  (the cognition→DTO mappers) · `shared/entities.py` (fill the DTO fields from Data Model v1.2 —
  additive) · `code/frontend/src/api/generated/**` (regenerate via `npm run api:gen`) ·
  `tests/{positive,negative}/api/**` + `tests/{positive,negative}/render/**`.
- **READ-ONLY:** all cognition/orchestration (`responsibilities/**`, `orchestration/**`,
  `retain/**` write paths), ALL migrations, the gates, `app.py` core. **No cognition change, no
  new write surface.**

## Packages / refactors

- None new (backend). No migration. Additive routers + render mappers only.

## Implementation instructions (TDD)

1. Red: pytest — `services/render` maps each governed object → its Data Model v1.2 DTO with the
   epistemic label intact; each GET endpoint returns the DTO (list + detail); auth/scoping
   enforced; **negatives:** no internal `epistemic.py` type serialized verbatim; the read surface
   exposes no mutation/accept/compute path; a DTO carries no field absent from Data Model v1.2.
2. `services/render` mappers → `api/v1/routers` GET endpoints → include in `v1/__init__.py`.
3. Regenerate the Orval client (`cd frontend && npm run api:gen`); run the drift gate
   (`bash scripts/check-openapi-drift.sh` / `tsc --noEmit`).

## API / data / schema contracts

- DTOs = `shared/entities.py` (Data Model v1.2), verbatim over REST (ADR-0003). Each carries
  `epistemic_label` (attested-*/derived) + confidence band + conflict where applicable. **No
  schema/DB change.**

## Test plan

- **Positive:** render maps cognition→DTO (labels intact); GET list/detail per resource; auth +
  workspace scoping; OpenAPI regen + drift gate green.
- **Negative:** internal cognition type leaked verbatim *(Critical)*; a write/mutation/accept/
  compute reachable from the read surface *(Critical)*; DTO field not in Data Model v1.2; missing
  epistemic label on a Derived object.
- ruff + gate-4 + gate-5 green; full backend suite no regression; frontend `tsc` green.

## Manual checks (EM)

- Backend up → `GET /v1/projects/{id}/findings` returns DTOs with labels; no endpoint mutates a
  canonical row; `frontend npm run api:gen` produces hooks for the new resources.

## Done criteria

- The domain REST surface exists + render mappers; Orval client regenerated; drift gate green; the
  read-mostly + no-verbatim-leak negatives pass; no migration/package; PR cites IC-WE-DISCLOSE /
  ADR-0003. Ready for DTM-0019.

## Worker report

**Status: Ready for review.** Cites IC-WE-DISCLOSE (E0/E1) + ADR-0003.

### What was built (additive only — no migration, no new dependency)

**DTOs — `shared/entities.py` (Data Model v1.2 verbatim; the response models, ADR-0003).**
Filled the skeleton entities and added the full Disclose read-surface DTO set, fields
bound to Data Model v1.2 (§7 Project, §10 AnalysisRun/CAFState/ConfidenceState, §11
Finding, §12 Recommendation incl. RS-R3 `deferred` + RS-R7 card fields, §13
Notification) and the Wave U receipts (UserAcceptanceRecord, PlanFact,
AcceptanceImpactAssessment). Each **Derived** DTO carries a `DerivedEnvelope`
(`label`) holding the epistemic-safety triple — `epistemic_label` (always `derived`)
+ `confidence_band` (LDM §3.1 / Calibration §2, the user-facing value) +
`conflict_state` + `current_chr_ref` lineage — so the UI renders without re-deriving
(decision #5). UAR/PlanFact carry `epistemic_label="attested-user"`. New enums
(ProjectLifecycle, AnalysisRunType/Status, FindingType/Status, Severity, Dimension,
RecommendationType/Status, EffortLevel, ConfidenceBand, ConflictState, Notification*)
are transcribed verbatim from Data Model v1.2 §7/§10/§11/§12/§13.

**Render layer — `backend/services/render/` (cognition → DTO mappers; replaces the stub).**
- `read_seam.py` — the **SELECT-only** `ProjectionReader` Protocol + `SupabaseProjectionReader`.
  Reads the **existing** persistence: the `derived.*_current` live-projection tables
  (LDM §3.1; migration 20260612090100 — each row already carries `current_payload` +
  the epistemic envelope) for derived cognition, and the append-only
  `user_acceptance_record` / `attested_assertion` retention tables for the canonical
  receipts. No insert/update/delete/upsert/append method exists on the reader (read-mostly
  by construction; a negative test asserts this).
- `mappers.py` — `finding_to_dto` / `recommendation_to_dto` / `confidence_to_dto` /
  `caf_to_dto` / `acceptance_impact_to_dto` / `uar_to_dto` / `plan_fact_to_dto` /
  `project_to_dto` / `analysis_run_to_dto` / `notification_to_dto`. Each reads the governed
  **source row** and emits the external DTO with the epistemic label intact. **The internal
  `shared.epistemic` types are never serialized verbatim** (decision #4; negative-proven).
  Internal vocab is translated to the Data-Model enums (Advise `recommendation_type`
  `candidate_improvement/suggested_action → improvement`; Infer `finding_type`
  `gap+gap_kind/conflict/risk →` the §11 flat taxonomy).

**Read routers — `backend/api/v1/routers/**` (GET only) + `v1/__init__.py` (includes them).**
GET endpoints (the operations the screens in `UI_SCREEN_INVENTORY` actually consume):
- `GET /v1/projects`, `GET /v1/projects/{project_id}` (Dashboard, Project Workspace)
- `GET /v1/projects/{project_id}/analysis-runs`, `GET /v1/analysis-runs/{analysis_run_id}` (Analysis Progress poll §11, Deep Results)
- `GET /v1/projects/{project_id}/findings`, `GET /v1/findings/{finding_id}` (Findings Workspace, Orientation)
- `GET /v1/projects/{project_id}/recommendations`, `GET /v1/findings/{finding_id}/recommendations` (RP-C1 Finding-context list), `GET /v1/recommendations/{recommendation_id}`
- `GET /v1/projects/{project_id}/confidence`, `GET /v1/projects/{project_id}/caf` (Dashboard, Confidence Experience, Orientation)
- `GET /v1/projects/{project_id}/acceptance`, `…/plan-facts`, `…/acceptance-impact` (History/Timeline, Awareness)
- `GET /v1/notifications` (Dashboard, Notification Center)

Routers are thin: auth/scoping via `api/deps.py` (`require_principal` → bearer-required
Principal; `get_projection_reader` → the SELECT-only seam), delegate to render mappers.
`app.py` still serves `/openapi.json`. `api/deps.py` was upgraded from a `NotImplementedError`
stub to a working contract surface (bearer → Principal, 401 on absent token; reader dependency
overridable in tests) — additive, read-only.

### Hard-constraint confirmation
- **Read-mostly:** every DTM-0018 `/v1` route is GET (negative test enumerates the routes and
  asserts no POST/PUT/PATCH/DELETE and no `:verb` path is reachable). No accept/capture/compute
  path added; acceptance stays on the existing Wave U seam.
- **No verbatim leak:** OpenAPI exposes only `shared.entities` DTOs; negatives assert the internal
  cognition fields (`model_or_rule_version`/`understanding_state`/`confidence_stage`) never appear
  and `shared.entities` never imports `shared.epistemic`.
- **Every Derived object carries its epistemic label** (positive + negative tests).
- **No migration, no new dependency** (`pyproject.toml` / `package.json` runtime unchanged; only
  the approved test-tooling line stays). **No cognition/orchestration touched**; render appends no
  CHR (gate-5 stays green — no CHR-append call-site added).

### Tests (TDD — red first, then green)
- `tests/positive/render/test_mappers.py` — mapper-per-object, labels intact.
- `tests/negative/render/test_no_verbatim_leak.py` — DTO ≠ internal type; no internal fields;
  Derived must carry a label; entities ≠ epistemic.
- `tests/positive/api/` (conftest fake reader + dependency overrides) + `test_read_endpoints.py`
  — GET list/detail per resource, labels in the JSON.
- `tests/negative/api/test_read_surface_negatives.py` — 401 unauth; 404 out-of-workspace (§12);
  **no mutating method / no :verb on the read surface (Critical)**; OpenAPI exposes no internal
  cognition schema (Critical); reader has no write method.

### Exact verification commands + results
- `cd code && .venv/bin/python -m pytest tests/positive tests/negative -q` →
  **574 passed, 65 skipped** (the 65 skips are pre-existing live/network-gated tests, unchanged;
  my 40 new tests pass; no regression). The `StatusCode.UNAVAILABLE` lines are the offline
  trace-export harness, not test failures.
- `cd code && .venv/bin/ruff check .` → **All checks passed!**
- `cd code && .venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS**.
- `cd code && .venv/bin/python ci/gate_observability.py` (gate-5) → **PASS**.
- Backend up (`uvicorn backend.api.app:app --port 8000`), then
  `cd code/frontend && npm run api:gen` → Orval generated hooks for projects, analysis-runs,
  findings, recommendations, confidence, acceptance, notifications (+ schemas).
  `bash scripts/check-openapi-drift.sh` → **"Frontend is in sync with the backend OpenAPI
  contract."** (`npx tsc --noEmit` exit 0). `npm run build` (tsc -b + vite) → **built in 408ms**.
- OpenAPI surface grew from `/health` to 16 paths (all GET); component schemas are the external
  DTOs only.
- `git status` — no change under `code/supabase/migrations/`; `git diff` empty for
  `pyproject.toml` and `frontend/package.json` deps. Generated Orval client stays gitignored
  (ADR-0003).

### Spec gaps hit + how resolved/escalated (ANTI_ASSUMPTION)

1. **Project / AnalysisRun / Notification have no built persistence/read seam (ESCALATE).**
   `backend/platform/__init__.py` is a one-line stub and **no migration creates a `project`,
   `analysis_run`, or `notification` table** in this branch (the built waves persist cognition
   as CHRs + `derived.*_current`, and Wave U writes `user_acceptance_record`/`attested_assertion`).
   `UI_SCREEN_INVENTORY` requires `GET /projects`, `GET /projects/{pid}`,
   `GET /projects/{pid}/analysis-runs`, `GET /analysis-runs/{rid}`, `GET /notifications`.
   **Resolution (no invention):** I exposed exactly those GET endpoints (so the OpenAPI/Orval
   contract the UI binds to is complete) and defined the SELECT-only reads against the
   Data-Model-named tables (`project`/`analysis_run`/`notification`, §7/§10/§13) on the reader.
   I did **NOT** author any migration or invent table columns. The reads work the moment the
   platform-persistence slice lands; tests exercise them via the in-memory fake. **This is a
   genuine upstream gap: the Project/AnalysisRun/Notification persistence (platform module) is
   unbuilt.** Flagging for the owner/EM — DTM-0018 cannot create canonical platform tables
   (human approval required for schema/persistence; CLAUDE.md), and the screens need them. Likely
   a platform-persistence task before/with DTM-0019+.

2. **Derived-cognition LIST reads use `derived.*_current`, not the CHR repo.** The existing
   `ChrRepository` read methods (`latest_for_output`/`get`/`lineage_chain`) return a single
   stream's latest/detail/history, not "all findings/recs for a project" — and `repository.py` is
   READ-ONLY in my boundary. The `derived.*_current` live-projection tables (LDM §3.1, already
   migrated) ARE the designed presentation read model and carry the epistemic envelope, so render
   reads them via a SELECT-only reader in `services/render` (which I own). **Caveat for the EM:**
   no built wave currently *populates* `derived.*_current` (the stages emit CHRs; the
   projection-write step isn't implemented yet), so these lists return rows only once that
   projection-write exists. The READ contract + mappers are correct and tested against the real
   row shape; the projection-WRITE is upstream (not DTM-0018's scope — read-only).

3. **Confidence `?history=true` chain (spec §6) not built here.** The current-confidence GET is
   provided; the supersession-chain variant depends on the CHR `lineage_chain` walk over a
   populated projection — deferred to the surface slice that needs it (no screen in scope strictly
   requires the chain for DTM-0018; added if DTM-0019+ binds it). Not invented.

No OBS-WE event tuples were added to `events.py` (gate-5 pins the per-wave A6 vocabularies exactly;
the `Disclosure Rendered`/`Notification Raised` OBS-WE events are surface-emitted in DTM-0019+, not
by this read-transport slice — adding them now would fail gate-5 and isn't this contract's surface).

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

Status: Approved

Executive summary:
- REST read surface built additively: `services/render` (read_seam SELECT-only + cognition→DTO
  mappers) + 7 GET routers (projects, analysis_runs, findings, recommendations, confidence,
  acceptance, notifications) included in `v1/__init__.py`; `shared/entities.py` filled with the
  Data Model v1.2 DTOs, every Derived DTO carrying a `DerivedEnvelope` (epistemic_label + band +
  conflict + CHR lineage). OpenAPI grew `/health` → 16 GET paths. Satisfies IC-WE-DISCLOSE
  (presents, never generates) + ADR-0003 (DTOs verbatim).

Verification (EM re-ran, all green):
- `.venv/bin/pytest tests/positive tests/negative -q` → **574 passed, 65 skipped** (40 new; no
  regression).
- `.venv/bin/ruff check .` → All checks passed. gate-4 → PASS. gate-5 → PASS.
- Hard constraints test-enforced + spot-checked: `grep` confirms **GET-only** (no
  post/put/patch/delete in routers); negatives bite — no-mutating-method, GET-only, no `:verb`
  command path, 401 unauthenticated, 404 out-of-workspace, OpenAPI exposes no internal cognition
  schema, `entities.py` has no `from shared.epistemic import`, `read_seam` SELECT-only.
- No migration file added; no runtime dependency added (pyproject/package.json unchanged).

Manual test plan:
- Start backend on :8000 → `GET /v1/projects/{id}/findings` returns DTOs with labels; no endpoint
  mutates a canonical row. `cd frontend && npm run api:gen` regenerates the client; drift gate green.

Remaining risks / accepted follow-ups (both correctly escalated, NOT guessed):
- **Platform persistence unbuilt** (projects/analysis_runs/notifications tables) — endpoints exist
  but lists are empty until a platform-persistence task authors the schema (**owner approval
  required** — CLAUDE.md migration rule). Tracked for a follow-up slice.
- **No wave writes `derived.*_current` yet** — the read contract + mappers are correct/tested
  against the real row shape; the projection-WRITE step is upstream (out of this read-only scope).
- Neither blocks DTM-0019 (the shell consumes the generated client; empty lists render fine).

# DTM-0033 — REST: acceptance commands (recommendations :accept/:reject/:defer/:implement)

**Status:** Ready for review · **Module:** DTM-0033 · **Phase:** Completion · **Contract:** API §5
(140–143) + DL-055 + Event Model §8 · **Depends:** the existing `record_acceptance` seam (UAR table
exists). **Branch:** `feat/release1-completion`.

## Goal / observable behavior

The Recommendation Panel's accept/reject/defer affordance (DTM-0022) now persists. New command
endpoints:
- `POST /v1/recommendations/{rid}:accept` → records a UAR + plan fact (accept), emits
  `recommendation_accepted`.
- `:reject` → UAR (no plan fact), `recommendation_rejected`.
- `:defer` → UAR (no plan fact), `recommendation_deferred`.
- `:implement` → UAR + (per DL-055) triggers a Deep recompute, `recommendation_implemented`.
Each resolves the recommendation's **current CHR as the mandatory `version_pin`**, builds an
`AcceptanceCapture`, and calls the EXISTING `backend/responsibilities/retain/acceptance.py`
`record_acceptance` (which writes UAR + plan fact, version-pinned, user-attested). The **user is the
actor** (from the Principal) — OSLO never self-accepts. Returns the affected `Recommendation` DTO;
`Idempotency-Key`; workspace-scoped.

## Source docs / constraints

- API §5 (140–143) — the 4 endpoints (path/method/response/idempotency/events). DL-055 (rec state
  lifecycle: Generated→{Accepted|Rejected|Deferred}→Implemented; accept/defer/reject are USER
  actions recorded by Wave U). `code/CONTEXT.md` (UAR version-pin mandatory; plan fact on
  accept/direct_edit only; never self-accept). Event Model §8 (`recommendation_accepted/…`).
- Code: `backend/responsibilities/retain/acceptance.py` (`record_acceptance` signature — the
  `AcceptanceCapture`/`store`/`emitter`/`chr_reader` params; what it writes), the retention store
  (`backend/services/persistence/retention_store.py` `insert_acceptance/insert_assertion`), the CHR
  reader (`backend/responsibilities/retain/repository.py` `latest_for_output` — to resolve the
  recommendation's current CHR = version_pin), `backend/api/v1/routers/recommendations.py` (existing
  GET — ADD a command router beside it), `backend/api/deps.py` (Principal + idempotency).

## Locked decisions (do not re-derive)

- **Wire `record_acceptance` — invent no acceptance logic.** The command resolves version_pin (the
  recommendation's current CHR via the chr_reader), builds the `AcceptanceCapture` (action + target
  + user_id from Principal + version_pin), calls `record_acceptance`. version_pin MANDATORY (no UAR
  without it — the existing `AcceptanceRecordingError` path).
- **OSLO never self-accepts (Critical):** the actor is the authenticated user (Principal.user_id);
  the command never auto-accepts, never marks the rec "true". Plan fact written only on accept (and
  direct_edit) — reject/defer write UAR only (the existing `record_acceptance` behavior).
- **:implement** records the UAR + (DL-055) triggers a Deep recompute via `submit_trigger`
  (materializer injected, like DTM-0032) — the implementation is new evidence → recompute.
- Additive command router; the GET read router + its negatives stay green. Emit the §8 event names
  (gate-5 vocab). `Idempotency-Key`; workspace-scoped (404). No new dep/migration.

## Owned files / boundaries

- **OWN:** `backend/api/v1/routers/acceptance_commands.py` (NEW) + include · `backend/api/v1/schemas/`
  · DI providers in `deps.py` (store/chr_reader/emitter — overridable) · `tests/{positive,negative}/
  api/**`. Event vocab + gate-5 fixtures if new names.
- **READ-ONLY:** `record_acceptance` + retain internals (call, don't change), the read router/seam,
  migrations, cognition.

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. Red (pytest, TestClient + overrides): each command resolves version_pin + calls
   `record_acceptance` with the right capture (assert via a fake store/recorder), returns the DTO,
   emits the §8 event; accept writes a plan fact, reject/defer do not; :implement also triggers a
   recompute. **Negatives (Critical):** version_pin missing → rejected (never an unpinned UAR);
   OSLO-self-accept impossible (actor = Principal, no server-initiated accept); 401 unauth; 404
   cross-workspace; reject/defer write NO plan fact; idempotency returns the same UAR.
2. Build the command router wiring `record_acceptance`; include in `v1/__init__.py`.

## API / data / schema contracts

- Returns the `Recommendation` DTO (state per DL-055). Writes UAR (+ plan fact on accept) via the
  existing append-only retention store. Emits `recommendation_accepted/rejected/deferred/implemented`.
  No schema change.

## Test plan

- **Positive:** accept (UAR + plan fact + event), reject/defer (UAR only + event), implement (UAR +
  recompute + event); version_pin resolved; idempotency; scoping.
- **Negative (Critical):** unpinned UAR rejected; no self-accept; reject/defer no plan fact; 401/404;
  read router unchanged.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 (new vocab) green.

## Manual checks (EM)

- POST :accept on a recommendation → a UAR + plan fact persisted (version-pinned to its CHR); the
  History surface shows it; GET acceptance/plan-facts returns it. reject/defer → UAR only.

## Done criteria

- The 4 acceptance command endpoints wire `record_acceptance` (version-pinned, user-actor, plan fact
  on accept only), :implement recomputes, idempotent + scoped, read router unchanged, never-self-
  accept + mandatory-version-pin negative-proven, gates green, no new dep. PR cites API §5 / DL-055.
  Ready for DTM-0034.

## Worker report

**Status: Ready for review.**

### What shipped

New additive command router `backend/api/v1/routers/acceptance_commands.py` (tag
`acceptance_commands`), included in `backend/api/v1/__init__.py` beside (not inside)
the GET recommendations read router. Four endpoints, all `response_model=Recommendation`,
workspace-scoped, `Idempotency-Key`-aware:

| Endpoint | record_acceptance action | Writes | Recompute | Event (EM §8.11) |
|---|---|---|---|---|
| `POST /v1/recommendations/{rid}:accept` | `accept` | UAR **+ plan fact** | no | `recommendation_accepted` |
| `POST .../{rid}:reject` | `reject` | UAR only | no | `recommendation_rejected` |
| `POST .../{rid}:defer` | `defer` | UAR only | no | `recommendation_deferred` |
| `POST .../{rid}:implement` | `implement` | UAR only | **yes (Deep)** | `recommendation_implemented` |

### How each wires `record_acceptance` (no acceptance logic invented)

1. **version_pin resolution (mandatory):** `_resolve_recommendation` reads the
   recommendation projection via the existing `ProjectionReader.get_projection("recommendation", rid)`;
   its `current_chr_ref` IS the recommendation's CURRENT CHR = the `version_pin`.
   404 if the projection is missing OR its project's `workspace_id` ≠
   `Principal.workspace_id` (existence not leaked, §12).
2. **Capture shape:** `{user_id=Principal.user_id, target_kind="recommendation",
   version_pin=current_chr_ref, action, project_id, captured_at}`. For
   accept/reject/defer this is built as an `AcceptanceCapture` (valid capture
   actions); `implement` is a DL-055 user action that is NOT in the
   `AcceptanceCapture` Literal, so it is passed to `record_acceptance` as a
   Mapping (the seam accepts either) — recorded as a UAR, no plan fact.
3. **Call:** `record_acceptance(capture, project_id=…, store=…, emitter=…, chr_reader=…)`.
   The existing seam writes the UAR ALWAYS and the plan fact ONLY for
   `accept`/`direct_edit` (its `_PLAN_FACT_ACTIONS`) — so reject/defer/implement
   write NO plan fact, unchanged. `record_acceptance`, the retention store, and
   the read router are byte-unchanged.
4. **Plan-fact-on-accept-only:** confirmed structurally — only `accept` is in the
   seam's `_PLAN_FACT_ACTIONS`; the router adds nothing.
5. **`:implement` recompute (DL-055):** after the UAR, builds a `TriggerClaim`
   (`REANALYSIS`, `information_changed=True`, `source="recommendation_implemented"`)
   and calls the EXISTING `submit_trigger("deep_pass", claim, materializer=…)` —
   the DTM-0032 DI providers (`get_trigger_submitter`/`get_materializer`) reused.
   Implementation = new evidence → recompute.
6. **DTO:** returns `recommendation_to_dto(row)` with the user-action `status`
   overlaid (DL-055 state) via `model_copy` — the Derived projection is NOT
   mutated (the rec stays recomputable; OSLO never promotes it).

### DI providers added (`backend/api/deps.py`, overridable in tests)

- `get_retention_store` → `SupabaseRetentionStore` (UAR/plan-fact INSERT).
- `get_acceptance_chr_reader` → `ChrRepository` (satisfies the `ChrReader`
  protocol — the accept plan-fact reads the pinned CHR's `output_payload`, a data
  read, no LLM). `submit_trigger`/`materializer` reused from DTM-0032.

### Events + gate-5

New §8.11 vocabulary `EVENT_NAMES_RECOMMENDATION` (the four
`recommendation_accepted/rejected/deferred/implemented` names, verbatim, in
contract order) added to `events.py` and appended to the `EVENT_NAMES` union after
`EVENT_NAMES_ANALYSIS`. Gate-5 (`ci/gate_observability.py`) updated: expected tuple
+ `_CONTRACT_VOCABULARIES` entry + `_UNION_NAME_ORDER`. Both gate-5 fixtures updated
(positive `test_gate_observability.py` synthetic union + a new §8.11 isolation
test; negative `test_gate_observability_negative.py` `GOOD_EVENTS_PY` + the
"all-missing" count 12→13 + the union-drop fixture). `recommendation_generated`
(the engine emission) stays in `WC_ADVISE`, never duplicated here.

### Negatives proven (Critical)

- **Mandatory version_pin** — a recommendation with `current_chr_ref=None` →
  `AcceptanceRecordingError` → **422**; assert **no UAR and no plan fact written**
  (no unpinned acceptance ever exists).
- **OSLO never self-accepts** — actor is always `Principal.user_id`
  (`test_actor_is_always_the_principal_user`: user "alice" recorded as
  `user_id`/`created_by`/plan-fact `attesting_source`); no bearer → **401** with
  nothing recorded (no server-initiated/auto accept path);
  `test_command_never_marks_recommendation_world_true` asserts no
  approved/true/world_truth/canonical/governed field on the UAR and the plan fact
  stays `attested-user`.
- **reject/defer write NO plan fact** — both write exactly one UAR, zero assertions.
- **401** unauth · **404** cross-workspace + missing rec (nothing persisted).
- **Idempotency** — same `Idempotency-Key` replays the same DTO; no second UAR /
  plan fact.
- **Read router unchanged** — `test_read_routers_stay_get_only_after_acceptance_commands_added`
  proves the `recommendations` GET router exposes no POST/PUT/PATCH/DELETE.
- **Purity** — router source asserted to call `record_acceptance` and NOT
  `insert_acceptance`/`insert_assertion` (it reimplements no UAR/plan-fact write).

### Verify (exact commands + results)

- `cd code && .venv/bin/pytest tests/positive tests/negative -q` →
  **642 passed, 65 skipped** (skips are live-Supabase/LLM axes; pre-existing). No
  regression. (Trailing OTel `StatusCode.UNAVAILABLE` trace-export lines are the
  exporter with no local collector — pre-existing, unrelated to this slice.)
- New-slice subset (`tests/positive/api/test_acceptance_commands.py`,
  `tests/negative/api/test_acceptance_command_negatives.py`, both gate-5 fixtures)
  → **66 passed**.
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS**.
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS** (new §8.11
  names pinned; union consistent).

### Confirmed

No new dependency (only existing/stdlib imports). No migration (`supabase/` and
canonical tables untouched; append-only honored — writes go through the existing
append-only retention store). `record_acceptance` (`responsibilities/retain/
acceptance.py`) and the GET read router (`routers/recommendations.py`) byte-
unchanged. Unrelated working-tree changes (`frontend/vite.config.ts`, `scripts/`)
preserved.

### Flagged

- Response `status` is overlaid on the DTO from the user action just recorded
  (the UAR is the source of truth for the DL-055 user-action lifecycle); the
  Derived projection is intentionally NOT mutated (OSLO never promotes a rec). If
  the owner later wants the lifecycle state to round-trip on a subsequent GET, a
  read-side overlay (GET joins the latest UAR per rec) would be the follow-up —
  out of this slice's scope (the read router stays untouched here).
- `implement` is recorded as a UAR with `action="implement"` (a DL-055 user
  action) via the Mapping form, since the `AcceptanceCapture` Literal admits only
  `accept|reject|defer|direct_edit`. No capture-vocabulary change was made (per
  READ-ONLY boundary); flag for the owner if a first-class `implement` capture
  action is wanted later.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- New additive `acceptance_commands` router: `:accept`→UAR+plan fact, `:reject`/`:defer`→UAR only,
  `:implement`→UAR + Deep recompute. Each resolves the recommendation's `current_chr_ref` as the
  mandatory version_pin, builds the capture (actor = Principal.user_id), and calls the EXISTING
  `record_acceptance`. API §5/DL-055. `record_acceptance` + GET read router byte-unchanged.

Verification (EM re-ran): `.venv/bin/pytest` → **642 passed, 65 skipped** (23 new; no regression).
ruff clean; gate-4 PASS; gate-5 PASS (new `recommendation_*` vocab pinned + fixtures). No new
dep/migration.

Negatives proven (Critical): missing version_pin → 422 (no unpinned UAR); OSLO never self-accepts
(actor = Principal; 401 records nothing); reject/defer write NO plan fact; 401/404; idempotency
replays the same UAR; read router GET-only.

Remaining risks / accepted follow-ups:
- DL-055 lifecycle state is overlaid on the response DTO, not round-tripped on a later GET — a
  read-side UAR-join is the follow-up if persistence-on-read is wanted.
- `:implement` uses the Mapping form (the `AcceptanceCapture` Literal vocabulary stayed READ-ONLY) —
  a first-class `implement` capture action is a Wave-U follow-up if desired.

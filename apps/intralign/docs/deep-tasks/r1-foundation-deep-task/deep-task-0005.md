# DTM-0005 — Recompute & stale backbone (the 00R spine)

**Status:** Approved · **Module:** DTM-0005 · **Phase:** II (Wave A) · **Contract:** **IC-WA-00R** · **Depends:** DTM-0004

## Goal / observable behavior

A valid trigger (promotion · knowledge-changing modification · clarification answered ·
information-changing user action · explicit/auto reanalysis) moves a project's cognition
state `Current → Stale → Reanalyzing → Current'`, re-runs the registered chain
`Retain → Infer → Evaluate → Advise` as a **durable LangGraph run**, replaces the live
Derived projection, and appends one CHR per emission via DTM-0004. On chain failure:
state → `Failed`, **last-known-good live projection retained**, history uncorrupted.

## Source docs / constraints

- The whole of `WAVE_A_CONTRACT_PACKAGE_00R_RECOMPUTE_STALE_BACKBONE.md` — IC A3 (required), **A4 (forbidden — enforce in tests)**, A7 states, A10 invariants; QA B2/B3/B4.
- DL-046: 00R is the **Deep Pass** engine — async, coalesced, must not block Fast Pass.
- ADR-0002: ALL graph wiring in `backend/orchestration/` (registry/runner/checkpointer); domain logic in responsibilities. A node is thin.
- Trigger detection belongs to Perceive; orchestration coordination to Act/Adapt (contract A1).

## Locked decisions

- Chain stages are **injected via a stage registry**: Phase II-A registers explicit no-op placeholders for Infer/Evaluate/Advise (each returns input unchanged, marked `WAVE_B_PLACEHOLDER`/`WAVE_C_PLACEHOLDER`). Backbone produces no cognition itself (A4.3).
- State machine + trigger types in `responsibilities/adapt/` (recompute discipline) + stale detection in `responsibilities/perceive/`; graph topology `orchestration/graphs/deep_pass.py`; durable checkpointer wired (Supabase Postgres) per `orchestration/checkpointer.py` stub.
- Coalescing: triggers arriving while `Reanalyzing` mark the run stale-again; one queued follow-up max (no unbounded queue) — exact semantics from contract A3/§0 (coalesced).
- States as enum: `analyzing | current | stale | reanalyzing | failed` (contract A3.6).
- Events emitted to an internal dispatcher seam only (transport TBD — open NFR); full observability contract is DTM-0006.

## Owned files

- `backend/orchestration/**` (implement stubs: checkpointer, runner, registry, state, graphs/deep_pass.py), `backend/responsibilities/{adapt,perceive}/**`, `tests/{positive,negative}/{orchestration,adapt,perceive}/**`.
- Read-only: `retain/` (consume DTM-0004 repo as-is), migrations, api/.

## Packages / refactors

- `langgraph-checkpoint-postgres` approved if the pinned langgraph version needs it (stop-and-ask otherwise). No refactors.

## Implementation instructions (TDD)

1. Red first against QA-WA-00R: B2.1–B2.5 positives; B3.1–B3.5 negatives (assessment-without-recompute impossible; CHR overwrite rejected; intake alone changes nothing; backbone emits no cognition of its own; no Derived→Attested write path).
2. Green: state machine → trigger validation → graph topology → durable run via checkpointer → last-known-good handling.
3. Replace each `NotImplementedError` stub in `orchestration/` — do not change its public seam without EM approval.

## Test plan

- Positive: each valid trigger → full transition cycle; CHR appended per emission; resume-after-interrupt (kill mid-run, resume from checkpoint); coalescing under burst triggers.
- Negative: B3 set, invalid trigger rejected, failure path retains last-known-good and appends nothing partial.
- Failure classification awareness: any Critical-class behavior (B4) = test must exist proving impossibility.

## Done criteria

- All QA-WA-00R B2+B3 mapped to named tests (traceability list in worker report); durable resume demonstrated; PR cites `IC-WA-00R`; gates green.

## Worker report

**Status: Ready for review** (worker, 2026-06-12). TDD: QA-mapped tests written first (8 collection
errors red), then implemented to green. Cites **IC-WA-00R**.

### Built

| Piece | File | What |
|---|---|---|
| Stale detection (A3.1) | `backend/responsibilities/perceive/staleness.py` | Pure `detect_staleness`/`is_stale` over `StalenessDescriptor` markers (last-analyzed vs current attested/evidence). No DB polling — descriptors come from the trigger payload. |
| Triggers (A3.2/A4.6) | `backend/responsibilities/adapt/triggers.py` | `TriggerType` enum — EXACTLY the 5 CHR `recompute_trigger` CHECK values; `validate_trigger` with dedicated `NoInformationChangeError` path (`information_changed: bool` required True — intake/acceptance-capture alone rejected) and `InvalidTriggerTypeError` for everything else. `TriggerClaim.emissions` makes emission flow explicit. |
| State machine (A3.6/A7) | `backend/responsibilities/adapt/states.py` | `CognitionState` exactly `analyzing\|current\|stale\|reanalyzing\|failed`; `CognitionStateMachine.transition` — A7 table only, illegal → `IllegalStateTransitionError`, every legal move returns a `StateTransitionEvent` record and emits `state_transition_occurred` through the seam (no printing). |
| Event seam (A6) | `backend/services/observability/events.py` | `EventEmitter` protocol + `CollectingEventEmitter` default; the 7 A6 names EXACTLY; unknown names rejected. Transport NOT wired (DTM-0006). |
| Graph state | `backend/orchestration/state.py` | `GraphState` extended ADDITIVELY: `trigger`, `emissions`, `appended_chr_ids`, `cognition_state`, `live_projection_ref` (last-known-good carrier), `failure`. Existing fields untouched. |
| Stage registry (locked #6) | `backend/orchestration/stages.py` | Injected chain `retain → infer → evaluate → advise`. `retain_stage` REAL: one `ChrRepository.append` per emission + `cognition_history_record_appended` each. `wave_b_placeholder_infer`/`wave_b_placeholder_evaluate`/`wave_c_placeholder_advise`: no-op pass-throughs, marked in name+docstring, produce NO cognition (A4.3). `default_stages()` copy + `register_stage` for Wave B/C injection. |
| Checkpointer | `backend/orchestration/checkpointer.py` | `build_checkpointer()` → `PostgresSaver` on `SUPABASE_DB_URL` (psycopg conn, `setup()` idempotent); `in_memory=True` fallback ONLY for tests that ask. Docstring records: LangGraph owns its checkpoint tables — workflow metadata per DL-054, NOT canonical. |
| Registry | `backend/orchestration/registry.py` | `register`/`get` (factories take wiring kwargs); `"deep_pass"` registered by `graphs/deep_pass.py`; lazy default-graph load in `get` (avoids circular import). |
| Deep Pass graph | `backend/orchestration/graphs/deep_pass.py` | `validate_trigger → mark_reanalyzing → append_chrs(retain, REAL) → stage_infer → stage_evaluate → stage_advise → mark_current`; failure edge → `mark_failed` (live ref NOT touched, `recompute_failed` emitted). Nodes THIN — delegate to adapt/perceive/retain/injected stages. |
| Runner | `backend/orchestration/runner.py` | `run()` durable execute/resume (thread_id = run id; re-invoke same thread_id with `state=None` resumes); `submit_trigger()` validate → mark stale (evented) → durable run → drain ONE coalesced follow-up. `CoalescingGuard` in-memory keyed by project_id. `RunOutcome{completed\|failed\|queued}`. |
| Dependency | `pyproject.toml` | `langgraph-checkpoint-postgres>=2` added — the ONE approved package (resolved 3.1.0; brings psycopg 3.3.4). Nothing else added. |

### QA traceability (QA-WA-00R → tests)

| QA | Test(s) | File |
|---|---|---|
| B2.1 valid trigger → recompute, chain re-run, live replaced | `test_b2_1_valid_trigger_full_cycle[promotion\|knowledge-change\|clarification\|user-action\|reanalysis]` (live, full cycle + A6 event order); `test_b2_1_each_valid_trigger_validates` (pure) | `tests/positive/orchestration/test_deep_pass_backbone.py`; `tests/positive/adapt/test_triggers.py` |
| B2.1 durable resume | `test_b2_1_run_resumes_with_same_thread_id` (interrupt before `stage_infer`, re-invoke same thread_id → completes; no double append) | `tests/positive/orchestration/test_deep_pass_backbone.py` |
| B2.1 coalescing | `test_b2_1_burst_of_three_triggers_coalesces_to_one_followup` (3 triggers while Reanalyzing → 3×queued, exactly 1 follow-up run) | `tests/positive/orchestration/test_runner_coalescing.py` |
| B2.2 each emission appends NEW CHR, priors intact | `test_b2_2_each_emission_appends_new_chr_priors_intact` (live DB counts + prior row byte-identical) | `tests/positive/orchestration/test_deep_pass_backbone.py` |
| B2.3 state transitions emitted | `test_b2_3_state_transitions_emitted_across_success_and_failure` (live, all 4 run transitions); `test_b2_3_full_success_cycle_emits_each_transition`, `test_b2_3_failure_branch_reanalyzing_to_failed` (pure); `test_b2_3_illegal_transition_rejected` (negative leg) | `tests/positive/orchestration/test_deep_pass_backbone.py`; `tests/positive/adapt/test_states.py`; `tests/negative/adapt/test_states_negative.py` |
| B2.4 failure → last-known-good, history uncorrupted | `test_b2_4_failure_retains_last_known_good_history_uncorrupted` (live: Failed state, `live_projection_ref` unchanged, CHR count unchanged, `recompute_failed` with `last_known_good_retained: True`) | `tests/positive/orchestration/test_deep_pass_backbone.py` |
| B2.5 stale on attested/evidence change | `test_b2_5_stale_detected_on_attested_knowledge_change`, `test_b2_5_stale_detected_on_evidence_change`, `test_b2_5_both_changes_reported_together` | `tests/positive/perceive/test_staleness.py` |
| B3.1 assessment-without-recompute impossible | `test_b3_1_no_assessment_mutation_api_exists` (introspection: adapt/perceive/orchestration export surfaces — no set/update/overwrite/mutate/delete/patch/edit mutators) | `tests/negative/orchestration/test_backbone_negative.py` |
| B3.2 CHR overwrite impossible | `test_b3_2_chr_overwrite_surface_absent_at_backbone_level` (re-asserted at backbone level; DB REVOKE+trigger proven live in DTM-0002/0004 suites) | `tests/negative/orchestration/test_backbone_negative.py` |
| B3.3 intake/acceptance alone rejected | `test_b3_3_trigger_without_information_change_rejected` (×5 types, dedicated error), `test_b3_3_invalid_trigger_name_rejected` (incl. literal `intake`, `acceptance-capture`), `test_b3_3_intake_alone_trigger_rejected_before_any_run` (submit-level: zero events) | `tests/negative/adapt/test_triggers_negative.py`; `tests/negative/orchestration/test_backbone_negative.py` |
| B3.4 backbone produces no cognition | `test_b3_4_placeholder_stages_produce_no_cognition` (output==input, exploding repo proves no append, zero events, WAVE_B/WAVE_C marks asserted), `test_b3_4_retain_stage_is_the_only_real_chain_stage` | `tests/negative/orchestration/test_backbone_negative.py` |
| B3.5 no Derived→Attested path | `test_b3_5_no_derived_to_attested_write_path_static_scan` (AST scan of orchestration+adapt+perceive: no `.table/.insert/.update/.upsert/.delete` calls, no raw client acquisition — canonical writes only via `retain.ChrRepository.append`) | `tests/negative/orchestration/test_backbone_negative.py` |
| invalid trigger / illegal transition / event vocabulary | `test_invalid_trigger_name_rejected_before_any_run`, `test_b2_3_illegal_transition_rejected`, `test_unknown_state_value_rejected`, `test_event_seam_rejects_unknown_event_names` | `tests/negative/{orchestration,adapt}/` |

B4 Critical classes each have an impossibility test: assessment-without-recompute → B3.1; history
overwrite/deletion → B3.2 (+ live DB suites); Derived→Attested / canonical mutation → B3.5 AST scan +
append-only repo surface.

### Commands run (real results)

Env: `SUPABASE_URL=http://127.0.0.1:54331`, `SUPABASE_SERVICE_ROLE_KEY=<service_role from supabase status>`,
`SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54332/postgres`; venv `/tmp/oslo-ci-venv`.

| Command | Result |
|---|---|
| `pytest tests/positive tests/negative -q` (baseline, before changes) | **96 passed** |
| `pytest tests/positive/{adapt,perceive,orchestration} tests/negative/{adapt,orchestration} -q` (red, pre-implementation) | 8 collection errors (modules absent) — red confirmed |
| `pip install "langgraph-checkpoint-postgres>=2"` | 3.1.0 installed (psycopg 3.3.4, psycopg-pool, langgraph-checkpoint 4.x) |
| same new-suite command after implementation | **66 passed** (0 skipped — live env present) |
| `pytest tests/positive tests/negative -q` (full, live env) | **162 passed** (96 baseline + 66 new; no regression) |
| `pytest tests/positive tests/negative -q` (env UNSET — CI shape) | **122 passed, 40 skipped, 0 failed** (live suites skip cleanly) |
| `ruff check .` | All checks passed |
| `python -m ci.gate_invariants --code-root .` | gate-4 PASS (no forbidden tokens / authority dir / canonical-table mutations) |
| PG inspection | LangGraph tables `checkpoint_blobs, checkpoint_migrations, checkpoint_writes, checkpoints` created by `setup()`; 22 checkpointed threads after suite |

### Flags (seam / signature / decisions for EM)

1. **Stub signature changes** (all were `NotImplementedError` stubs):
   - `checkpointer.build_checkpointer()` → `build_checkpointer(*, in_memory: bool = False)`.
   - `runner.run(graph_name, state)` → `run(graph_name, state | None, *, thread_id, checkpointer, emitter, chr_repo, stages, interrupt_before)` — `state=None` + same `thread_id` = resume. Positional compatibility kept.
   - `runner` gained `submit_trigger(...) -> RunOutcome` (backbone entry), `CoalescingGuard`, `reset_coalescing_guard()`.
   - `registry.GRAPHS` value type widened `Callable[[], object]` → `Callable[..., object]` (factories take wiring kwargs); `get()` lazily imports default graph modules and raises a descriptive `KeyError`.
   - `runner.py` stub's import `from orchestration.state import ...` was broken (package roots are `backend`/`shared`); fixed to `backend.orchestration.state`.
2. **events.py placement:** `backend/services/observability/events.py` (the allowed services/observability option — one new file) rather than orchestration, so responsibilities (adapt) import the seam without a responsibilities→orchestration dependency. DTM-0006 binds transport here.
3. **Coalescing guard is in-memory** (per-process dict keyed by `project_id`) — acceptable for this increment per task; **Redis-backed guard is the Phase-II-A follow-up** (multi-dyno correctness on Heroku).
4. **`append_chrs` node position:** placed at the chain HEAD (executing the injected REAL `retain` stage), i.e. `… → append_chrs → stage_infer → stage_evaluate → stage_advise → …`, honoring the A3.3 chain order Retain→Infer→Evaluate→Advise. The task text sketched `chain stages → append_chrs`; with Wave-A placeholders the two are behaviorally identical (placeholders emit nothing). Flagged for EM; Wave B may move the append point when real stages produce emissions.
5. **`failed → stale` transition added** to the A7 table (a NEW information-changing trigger re-marks a failed project stale; last-known-good retained meanwhile). A7 names no exit from Failed — without one, a failed project could never recover. Flagged as interpretation; tested both ways (`failed→stale` legal, `failed→current/reanalyzing` illegal).
6. **Local-machine env note (NOT a project dependency):** the approved package depends on plain `psycopg`, whose pure-Python impl needs system `libpq`; this Mac has none, so `psycopg-binary==3.3.4` (same driver's official binary wheel, bundled libpq) was installed **into `/tmp/oslo-ci-venv` only** — `pyproject.toml` carries exactly the one approved package. CI ubuntu runners ship libpq, so plain `psycopg` works there. If the EM prefers it declared, the line would be `psycopg[binary]` — owner/EM call.
7. **LangGraph checkpoint tables** (`checkpoints`, `checkpoint_blobs`, `checkpoint_writes`, `checkpoint_migrations`) are created by `PostgresSaver.setup()` in the public schema — workflow metadata per DL-054, NOT canonical, owned by LangGraph; outside the canonical-migration linter by design (documented in `checkpointer.py`).
8. **No cognition produced anywhere** in this increment (A4.3): the only real stage appends receipts for emissions DECLARED in the trigger payload; placeholders are inert. Stale detection consumes descriptors from the trigger payload (intake doesn't exist yet — DTM-0001..4 scope).
9. Not committed/pushed (per task rules). `git status`: modified `orchestration/{state,checkpointer,registry,runner}.py`, `responsibilities/{adapt,perceive}/__init__.py`, `pyproject.toml`; new `orchestration/{stages.py,graphs/deep_pass.py}`, `responsibilities/adapt/{triggers,states}.py`, `responsibilities/perceive/staleness.py`, `services/observability/events.py`, `tests/{positive,negative}/{orchestration,adapt,perceive}/`.

## Engineering-manager review notes

**Review 1 (2026-06-12):** `stages.py` + `deep_pass.py` + `runner.py` + adapt/perceive
modules reviewed. Wiring-vs-work discipline held throughout: every graph node thin,
cognition logic absent, placeholders provably no-op (exploding-repo negative test).
Failure edge captures (never swallows) and `mark_failed` provably leaves
`live_projection_ref` untouched. A6 names exact; A7 table enforced with exceptions.
QA traceability table complete (B2.1–B2.5, B3.1–B3.5 → named tests).

**Flag rulings:** (1) stub signature changes — accepted, all were `NotImplementedError`
seams. (2) `events.py` in `services/observability/` — accepted; DTM-0006 wires transport
there. (3) in-memory CoalescingGuard — accepted for this increment; **Redis guard is a
recorded Phase II-A follow-up** (multi-dyno). (4) `append_chrs` at chain head — matches
A3.3 chain order Retain→Infer→Evaluate→Advise; Wave B may move the append point when
real stages produce emissions. (5) `failed→stale` recovery transition — contract
interpretation (A7 names no exit from Failed; a valid new trigger must recover) —
**added to owner items**. (6) psycopg-binary local-venv-only — fine. (7) LangGraph
checkpoint tables = workflow metadata (DL-054), documented — fine.

## Approved by engineering manager

Status: Approved

Executive summary:
- The 00R recompute backbone is live: validated triggers (5 exact types,
  information-change required) drive a durable LangGraph Deep Pass
  (Supabase-Postgres checkpointer, resume-by-thread-id proven) through the injected
  Retain→Infer→Evaluate→Advise chain; the real retain stage appends CHRs; success
  replaces the live projection; failure retains last-known-good with history
  uncorrupted; bursts coalesce to at most one follow-up. Only-recompute-changes-
  assessment is enforced by construction and by negative tests.

Verification (EM-run, independent):
- `pytest tests/positive tests/negative` (live env incl. SUPABASE_DB_URL) → **162 passed**.
- `ruff check .` → clean; `ci.gate_invariants` → PASS.
- Code review: A4 forbidden behaviors each have a proving negative test; no
  cognition production anywhere in backbone code.
- Worker TDD evidence: 8 collection errors red → green; durable resume +
  3-trigger coalescing demonstrated live.

Manual test plan:
- From `code/` with env set: submit a `promotion` trigger with one declared emission
  via `runner.submit_trigger("deep_pass", {...})`; watch `stale_detected →
  reanalysis_triggered → recompute_started → cognition_history_record_appended →
  state transitions → recompute_completed` in the collecting emitter; verify the CHR
  row in Studio.

Remaining risks:
- Coalescing guard is per-process — Redis follow-up before multi-dyno Staging.
- `failed→stale` recovery is a contract interpretation pending owner nod.
- Emission flow currently trigger-declared (placeholders produce none) — Wave B
  replaces this when Infer/Evaluate emit for real.

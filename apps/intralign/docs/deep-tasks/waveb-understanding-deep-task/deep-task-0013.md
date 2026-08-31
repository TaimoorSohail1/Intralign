# DTM-0013 — Defect fix: cognition stages must append a CHR *model*, not a dict (live)

**Status:** **Approved** (EM, 2026-06-17) · **Module:** DTM-0013 ·
**Phase:** III (Wave B) · **Fixes:** DTM-0009 (`infer/stage.py`), DTM-0010 (`infer/finding_stage.py`),
and DTM-0011 (`evaluate/stage.py` if it has the same shape) · **Surfaced during:** full live
suite after DTM-0012 (`pytest` with Supabase up).

## Defect

`backend/responsibilities/retain/repository.py::ChrRepository.append(record)` (the REAL repo)
calls `record.model_dump(mode="json", …)` — it requires a `CognitionHistoryRecord` **model**.
`orchestration/stages.py::retain_stage` honours that (constructs the model). But the cognition
stages pass a **plain dict**:
- `infer/stage.py:238` → `ctx.chr_repo.append({"project_id": project_id, **spec})`
- `infer/finding_stage.py:208` → same.

Live, this raises `AttributeError: 'dict' object has no attribute 'model_dump'`, the `infer`
stage fails, and the deep_pass run ends `failed` (last-known-good retained). **Offline it was
masked** by a dict-tolerant fake repo (`tests/positive/synthesis/fakes.py:28
append(self, record: dict)`), and the one test that would have caught it
(`tests/positive/evaluate/test_b2_live_chain_e2e.py`) is env-gated and was **skipped** in every
prior run. Net: `522 passed, 1 failed` live; the failure is the Wave-B live chain e2e.

## Fix (scope)

1. **`infer/stage.py`** (`_append_chr`): construct `CognitionHistoryRecord(project_id=project_id,
   **spec)` and pass the **model** to `ctx.chr_repo.append(...)` — mirror `retain_stage`
   exactly (import `CognitionHistoryRecord` from `backend.responsibilities.retain`). `spec`
   already carries `recompute_trigger` (from `planning_chr_spec`), so no double-pass.
2. **`infer/finding_stage.py`** (`_append_chr`): same fix.
3. **`evaluate/stage.py`:** check its CHR-append path; if it also passes a dict, apply the same
   model-construction fix. If it already passes a model, leave it.
4. **Tighten the test doubles so this can't reappear:** the fake repos (`tests/positive/
   synthesis/fakes.py`, and any finding/evaluate fake repo) must accept a
   `CognitionHistoryRecord` (validate/duck-type the model contract), NOT a bare dict — so the
   double matches the real `append` signature. Update call-sites/assertions accordingly.
5. **Make the live e2e pass:** `tests/positive/evaluate/test_b2_live_chain_e2e.py` must go green
   with Supabase up.

## Owned files / boundaries

- **OWN:** `backend/responsibilities/infer/stage.py`, `backend/responsibilities/infer/finding_stage.py`,
  `backend/responsibilities/evaluate/stage.py` (CHR-append construction only — no logic change);
  the fake repos under `tests/**` + affected assertions.
- **READ-ONLY:** `retain/repository.py` (the contract is correct — match it), `stages.py`
  (`retain_stage` is the reference), `orchestration/**` core, migrations, gate vocab, the v0
  scoring, cognition logic, prompts, recorded-fixture content.

## Constraints

- No new dependency, no schema change, no Docker. The fix is "build the model the real repo
  already requires." Recorded-fixture CI (ADR-0004) unchanged. Determinism unchanged.

## Test plan

- The full **live** suite (Supabase up, `OSLO_LLM_LIVE` unset → recorded fixtures) goes green:
  `set -a; source .env; set +a; pytest tests/positive tests/negative tests/replay -q` → 0 failed.
- The offline suite stays green with the **tightened** fake repos (the dict-tolerant hole is
  closed; a stage passing a dict would now fail a test).
- ruff + gate-4 + gate-5 green.

## Done criteria

- `test_b2_live_chain_admit_infer_evaluate_under_60s_and_recompute_supersedes` PASSES live;
  cognition CHRs (synthesis/finding/issue/confidence/caf/outcome_confidence) actually persist
  to `cognition_history_record`; full live + offline suites green; fake repos match the real
  `append(CognitionHistoryRecord)` contract.

## Worker report

**Ready for review**

### Root cause (confirmed live)

The real `ChrRepository.append(record)` calls `record.model_dump(...)` — it needs a
`CognitionHistoryRecord` MODEL. `infer/stage.py`, `infer/finding_stage.py` and
`evaluate/stage.py` all called `ctx.chr_repo.append({"project_id": project_id, **spec})` (a
plain DICT). Live: `AttributeError: 'dict' object has no attribute 'model_dump'` at the `infer`
stage → run ends `failed`. Reproduced before the fix (`first.state.failure ==
{'stage': 'infer', 'error_type': 'AttributeError', 'error': "'dict' object has no attribute
'model_dump'"}`).

Constructing the model surfaced TWO more contract requirements the dict-tolerant fake had masked,
both of which would ALSO have failed live:

1. `CognitionHistoryRecord` requires `provenance_ref` (no default; DB column NOT NULL) — neither
   `planning_chr_spec`/`finding_chr_spec` nor the evaluate spec carried it.
2. `recompute_trigger` is a non-optional Literal (DB CHECK NOT NULL, 5 values). The stages read it
   from `inputs.get("recompute_trigger")`, which was `None` in the live e2e (and in the offline
   helpers). retain_stage never hits this because it reads `trigger.trigger_type` (always present).

### Files changed (production)

- `backend/responsibilities/infer/stage.py` — import `CognitionHistoryRecord`; `_append_chr` now
  builds `CognitionHistoryRecord(project_id=project_id, provenance_ref={"emitted_by":
  "infer.synthesis"}, **spec)` and passes the MODEL. No other logic change; emit + `_persisted_chr_id`
  unchanged (return is now a model — already tolerated).
- `backend/responsibilities/infer/finding_stage.py` — same fix; `provenance_ref={"emitted_by":
  "infer.finding"}`.
- `backend/responsibilities/evaluate/stage.py` — **YES, it had the same dict bug** (`stage.py:387`).
  Same fix; `provenance_ref={"emitted_by": "evaluate"}`. (The live run died at `infer` before
  evaluate, so its append was unproven — now consistent and proven by the e2e, which persists
  issue/reliability/caf/confidence/outcome_confidence rows.)

### Files changed (tests — fake-repo tightening + recompute_trigger realism)

- `tests/positive/synthesis/fakes.py` — `AppendOnlyFakeChrRepo.append` now MATCHES the real
  signature: `append(record: CognitionHistoryRecord) -> CognitionHistoryRecord`. It raises
  `TypeError` on a non-model (so a future dict-pass FAILS a test), and mirrors the real repo
  (`model_dump` → store row → `model_validate` → return a model). `.rows` stay dict-shaped and
  `rows_for_kind` is unchanged, so existing dict-access assertions still hold.
- Tightened the two "returned-row cannot overwrite storage" negatives to pass a real model and
  mutate the RETURNED model (`tests/negative/synthesis/test_b3_derived_boundary.py`,
  `tests/negative/infer_finding/test_b3_recompute_and_modes.py`) — the invariant (returned record is
  independent of storage) is preserved and now exercises the real contract.
- Set a valid first-pass `recompute_trigger` (`"knowledge-change"`) where offline helpers/tests
  previously passed `None` (which the tightened fake — and the live DB — reject): `synthesis/
  test_b2_generation.py`, `synthesis/test_b2_cost.py`, `synthesis/test_b2_recompute.py`, `evaluate/
  test_b2_stage.py`, `evaluate/test_b2_performance_gate.py`, `evaluate/test_b2_wave_b_composition.py`
  (`_State.inputs`), `llm_provider/test_chr_provenance_dtm0012.py`, `infer_finding/test_b2_stage.py`,
  and the negatives `evaluate/test_b3_recompute_and_invariants.py`, `evaluate/
  test_b3_cost_and_performance.py`, `infer_finding/test_b3_recompute_and_modes.py`, `synthesis/
  test_b3_derived_boundary.py`, `synthesis/test_b3_autonomous_write.py`.
- `tests/positive/evaluate/test_b2_live_chain_e2e.py` — `_infer_inputs_from_state` now reconstructs
  the per-run input set from the surviving `trigger.trigger_type` (the live wiring): it carries
  `recompute_trigger`, and derives `is_recompute`/`input_attestation_version`
  (`knowledge-change`→v1, `reanalysis`→v2). NOTE the WHY below.

### Note for the EM (a real, pre-existing wiring gap I did NOT widen scope to fix)

`TriggerClaim` (`backend/responsibilities/adapt/triggers.py`) carries only `trigger_type/project_id/
information_changed/source/emissions` — NOT free-form `inputs`. The runner builds `GraphState`
without copying any trigger inputs or `base_state.inputs`. So the e2e's
`_trigger(..., input_attestation_version="v2")` payload was silently dropped: the stages always saw
the default `"v1"` and a null `recompute_trigger`. `triggers.py`/`runner.py`/`state.py` are READ-ONLY
for this task, so I reconstructed the per-run inputs from the one field that survives
(`trigger_type`) inside the test's own `extract_infer_inputs` mapper. This keeps the two generations'
`input_attestation_version` distinct + reconstructable from CHR lineage WITHOUT touching orchestration
core. If the team wants triggers to carry real free-form inputs end-to-end, that is a separate
orchestration change (escalate).

### Verification — exact commands + results

OFFLINE (no env):
`.venv/bin/python -m pytest tests/positive tests/negative tests/replay -q`
→ **455 passed, 68 skipped, 0 failed**. (Confirmed the tightened fake closes the hole: before the
recompute_trigger fixes, 38 tests failed on the now-validated model; a dict-pass now raises.)

LIVE (Supabase up, `OSLO_LLM_LIVE` unset → recorded fixtures):
`set -a; source .env; set +a; unset OSLO_LLM_LIVE; .venv/bin/python -m pytest tests/positive
tests/negative tests/replay -q`
→ **523 passed, 0 skipped (of these), 0 failed**.
`tests/positive/evaluate/test_b2_live_chain_e2e.py::
test_b2_live_chain_admit_infer_evaluate_under_60s_and_recompute_supersedes` → **PASSES** (was the 1
failure; it is no longer env-skipped with the live stack up).

Gates:
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python -m ci.gate_invariants` → **PASS** (no forbidden tokens / authority module /
  canonical-table mutations).
- `.venv/bin/python -m ci.gate_observability` → **PASS** (every CHR-append call-site emits
  `cognition_history_record_appended`).

Sanity (one live deep_pass run, queried `cognition_history_record` by project_id):
`{'synthesized_planning_model': 1, 'planning_artifact': 7, 'finding': 6, 'issue': 6,
'reliability': 1, 'caf': 1, 'confidence': 1, 'outcome_confidence': 1}` — **24 CHRs persisted**
spanning synthesis + finding + evaluate. The chain actually persisted.

### Guardrails

No edits to retain/repository.py, retain/models.py, stages.py retain_stage, orchestration core,
migrations, gate vocab, v0 scoring, prompts, recorded-fixture content, or cognition logic. No new
dependency, no schema change, no Docker. No git commit. No STOP raised.

## Engineering-manager review notes

**Review (2026-06-17).** Defect found by the EM live run (the prior DTM-0009/0010/0011
approvals were verified **offline only** — their live e2e was env-gated and skipped in every
run, and the dict-tolerant fake repo masked the real `append` contract; recorded here so the
gap is on the record). EM independently verified the fix:

- **Scope correct:** the 3 stage files now construct `CognitionHistoryRecord(...)` and pass the
  **model** (`infer/stage.py:242`, `infer/finding_stage.py:212`, `evaluate/stage.py:390` — yes,
  evaluate had the same dict bug). Frozen `orchestration/**`, `retain/**`, migrations, `ci/**`
  **untouched** (empty diff). No new dependency, no schema change.
- **Fake-repo tightening verified:** `AppendOnlyFakeChrRepo.append` now requires a
  `CognitionHistoryRecord` (raises `TypeError` on a dict) and mirrors the real repo
  (`model_dump`→store→`model_validate`) — a future dict-pass now FAILS offline, closing the hole
  that hid this.
- **Two further masked requirements** the worker correctly surfaced and satisfied:
  `provenance_ref` (NOT NULL — set to `{"emitted_by": "<stage>"}`) and the non-optional
  `recompute_trigger` Literal. Accepted; sensible minimal provenance (upstream assertion
  lineage is separately carried in `upstream_lineage`).

**EM-run verification (independent, 2026-06-17):**
- OFFLINE (`env -u SUPABASE_* -u OSLO_LLM_LIVE pytest …`) → **455 passed, 68 skipped, 0 failed**.
- LIVE (Supabase up, `source .env`, `OSLO_LLM_LIVE` unset → recorded fixtures) → **523 passed,
  0 failed**; `test_b2_live_chain_…` runs and **PASSES** (was the lone failure). A live run
  persists the full chain (synthesis + 7 artifacts + findings + issues + CAF/confidence/
  reliability/outcome → CHR rows).
- `ruff` clean · gate-4 PASS · gate-5 PASS.

**Carried follow-up (not a defect; orchestration is read-only here):** `TriggerClaim`/`GraphState`
do not propagate free-form per-run inputs, so the e2e reconstructs `input_attestation_version`/
`is_recompute` inside its own `extract_infer_inputs` mapper from `trigger.trigger_type`. Making
triggers carry real inputs end-to-end is a separate orchestration change — flag for the owner.

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0013 fixes a live-only durable-execution defect: all three cognition stages (synthesis,
  finding, evaluate) passed a plain dict to `ChrRepository.append`, which requires a
  `CognitionHistoryRecord` model — so every live recompute failed at the infer stage. The fix
  constructs the model (mirroring `retain_stage`); the test fakes are tightened to the real
  contract so the gap cannot reopen. The Wave-B chain now runs and persists end-to-end live.

Verification:
- OFFLINE 455 passed / 68 skipped / 0 failed; LIVE 523 passed / 0 failed (e2e green) · ruff
  clean · gate-4 PASS · gate-5 PASS. Frozen modules untouched; no dependency/schema change.

Manual test plan:
- `supabase start` + `docker compose up -d`; `set -a; source .env; set +a`;
  `pytest tests/positive tests/negative tests/replay` → 0 failed; inspect Studio:
  `cognition_history_record` has synthesis/finding/issue/confidence/caf/outcome rows for the
  e2e project; a recompute supersedes with prior CHRs byte-intact.

Remaining risks:
- Triggers don't carry free-form inputs end-to-end (above) — owner-flagged orchestration item.
- Live LLM (Gemma) still exercised only via recorded fixtures here; a true live-model run needs
  `OSLO_LLM_LIVE=1` + `OSLO_LLM_BASE_URL` once the runtime is up (DTM-0012 manual check).

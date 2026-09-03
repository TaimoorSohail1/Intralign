# DTM-0040 — DL-048 token-budget enforcement (spend-gate + graceful degradation)

**Status:** In progress · **Module:** DTM-0040 · **Phase:** Completion · **Contract:** DL-048 +
Calibration §4c + OPEN_TBD A6 · **Depends:** the LLM seam + the existing budget machinery (Wave B).
**Branch:** `feat/release1-completion`.

## Goal / observable behavior

The DL-048 freemium cost-governance is **enforced end-to-end**: a run that would exceed its
per-tier token/cost budget is **gracefully degraded** (partial orientation, not a hard crash), the
`AI Spend Recorded` telemetry is emitted, and the **honest-limit signal** (the truthful
partial-analysis disclosure the DTM-0029 frontend renders) is produced. First **audit** what Wave B
already built (`budget_for_tier`, `ai_spend_recorded`, the synthesis cost tests, the routing/tier
config) and implement only the **missing enforcement** — the spend-check seam + the degradation +
the honest-limit signal — using the DL-048 numbers (NOT invented).

## Source docs / constraints

- DL-048 (per-tier budget gating; graceful degradation; `AI Spend Recorded` telemetry; the QA gate;
  Upgrade-Prompt UP-4 + the **honest-limit disclosure** = the contracted part). Calibration §4c +
  OPEN_TBD A6 (the owner-confirmed budget numbers: Fast 150k/run, Deep 600k/run, daily 500k, monthly
  4M, ~$3 Tier-1 ceiling — **use these, invent none**). `code/CONTEXT.md` (Fast/Deep, honest-limit).
- Code: `backend/services/llm_provider/config.py` (`budget_for_tier`/`TierBudget`/routing — what
  exists), the `ai_spend_recorded` event + the Wave B synthesis cost tests (the spend-recording that
  already works), the cognition stages that call the LLM (`perceive/extraction`, `infer/synthesis`,
  `infer/finding`) — where the spend-check seam attaches, the orchestration (degradation = partial
  result + the honest-limit signal on the run/projection). events + gate-5.

## Locked decisions (do not re-derive)

- **Audit first, then close the gap** — report what enforcement already exists vs is missing; build
  ONLY the missing spend-gate + degradation + honest-limit signal. Do not duplicate working
  spend-recording.
- **Graceful degradation, not failure** (DL-048): exceeding the budget yields a **partial** result
  with the honest-limit signal (reduced coverage + reason), never a hard error or a silently-complete
  result. The honest-limit signal is what the DTM-0029 `HonestLimitDisclosure` renders (a
  presentation flag on the run/projection — confirm the shape the frontend expects).
- **Numbers from DL-048/Calibration §4c** — Fast/Deep/daily/monthly budgets + the Tier-1 ceiling;
  routing per the existing tier config. Invent no number (A3/A4 latency stays owner-TBD).
- **`AI Spend Recorded`** emitted with model + est_cost + tokens (the existing event — ensure the
  enforcement path emits it). Gate-5 vocab if a new event. No new dependency.

## Owned files / boundaries

- **OWN:** the spend-gate seam (`backend/services/llm_provider/` budget enforcement or a small
  `backend/responsibilities/.../budget.py`) + the degradation/honest-limit signal wiring (orchestration
  state / the projection envelope) + `tests/{positive,negative}/...`. Event vocab + gate-5 if new.
- **READ-ONLY:** the cognition stages' logic (attach the gate, don't change the cognition), the LLM
  adapter, migrations, the frontend (it already renders the honest-limit — match its expected shape).

## Packages / refactors — none new.

## Implementation instructions (TDD)

1. **Audit** (write findings in the report): what budget/spend code exists (`budget_for_tier`,
   `ai_spend_recorded`, cost tests) and what enforcement is missing.
2. Red (pytest): a run projected to exceed the per-tier budget → degraded partial result + the
   honest-limit signal + `AI Spend Recorded`; a within-budget run → full result, no honest-limit.
   **Negatives:** a budget-exceeded run is NEVER presented as complete (the honest-limit signal is
   set); the upgrade prompt is alongside, never instead of (the signal carries the truthful
   disclosure); spend is recorded even on degradation; no invented budget number.
3. Implement the spend-gate + degradation + honest-limit signal using the DL-048 numbers.

## API / data / schema contracts

- The honest-limit signal travels on the run/projection (the shape the DTM-0029 frontend reads).
  `AI Spend Recorded` telemetry. No schema change (flag if the signal needs a projection field).

## Test plan

- **Positive:** within-budget → full; over-budget → degraded + honest-limit + spend recorded;
  per-tier numbers (DL-048).
- **Negative:** over-budget never shown complete; disclosure alongside not instead; spend recorded
  on degradation; no invented number.
- `.venv/bin/pytest` + ruff + gate-4 + gate-5 green.

## Manual checks (EM)

- Force a small budget → a run degrades to partial + the honest-limit signal (the frontend shows the
  truthful disclosure); `AI Spend Recorded` emitted; within budget → full, no disclosure.

## Done criteria

- DL-048 budget enforcement complete: spend-gate + graceful degradation + honest-limit signal +
  `AI Spend Recorded`, DL-048 numbers (none invented), over-budget-never-complete negative-proven,
  gates green, no new dep/migration. PR cites DL-048. Ready for DTM-0041.

## Worker report

**Status: Ready for review.**

### AUDIT — what Wave B already built (DO NOT duplicate) vs what was MISSING

The DL-048 spend-gate, graceful degradation, and `AI Spend Recorded` telemetry
already exist and are tested. Only the **honest-limit signal** was missing.

**ALREADY BUILT (enforced + tested — left untouched):**

- **Budget config (numbers, §4c / A6).** `backend/services/llm_provider/config.py`
  — `TierBudget` (Fast 150k/run, Deep 600k/run, daily 500k, monthly 4M), `budget_for_tier`,
  `routing_for_tier`, `COST_PER_MILLION` (the June-2026 cost basis), `estimate_cost_usd`.
  All numbers are config transcribed from Calibration §4c — **I invented none.**
- **The spend-gate (accountant).** `backend/services/llm_provider/budget.py` — `RunBudget`
  with `can_afford(estimated_tokens)` (the pre-call gate), `record(...)` (post-call usage),
  `over_budget` (the degrade trigger = spend ≥ §4c per-run cap), `est_cost_usd()`, and
  `spend_event_payload(...)` (the shared `ai_spend_recorded` shape: tokens_in/out, est_cost,
  tier, user, mode, model + degraded/over_budget trust signal).
- **Graceful degradation.** `backend/responsibilities/infer/synthesis.py` —
  `synthesize_and_generate` prioritizes evidence (constraint→dependency→fact→assumption),
  synthesizes a partial model within budget, and **defers** any artifact that would exceed
  the cap (`can_afford` False) instead of overspending. `SynthesisResult` carries
  `degraded` + `deferred_artifact_types` + `spend_payload`.
- **`AI Spend Recorded` emit.** `backend/responsibilities/infer/stage.py::run_synthesis_stage`
  emits exactly one `ai_spend_recorded` per run (including degraded runs). Event vocab pinned
  in `events.py` `EVENT_NAMES_COST` + gate-5.
- **Existing tests.** `tests/positive/synthesis/test_b2_cost.py` (within-budget no-defer;
  over-budget degrade + spend) and `tests/negative/synthesis/test_b3_cost_governance.py`
  (no silent overspend / no runaway / wrong-tier routing / over-budget can't hide).

**MISSING (the DTM-0040 gap I built):** the **honest-limit signal** — the truthful
partial-analysis disclosure the DTM-0029 `HonestLimitDisclosure` frontend renders. A grep
for `honest`/`limited`/`coverage_note` across `backend/`+`shared/` returned **nothing**:
the degraded run produced `degraded`/`deferred_artifact_types` internally, but **no
`HonestLimit`-shaped signal was ever produced on the run/projection envelope** for Disclose
to render. The frontend (`HonestLimitDisclosure.tsx` + `honestLimit.fixtures.ts`) already
FLAGGED this as a backend dependency ("DL-048 limit signals are not yet exposed").

### What I built (the missing enforcement only)

1. **`backend/responsibilities/infer/honest_limit.py`** — a PURE builder
   `honest_limit_for_result(result, *, upgrade=None)` mapping the already-computed
   `SynthesisResult` → the non-canonical `HonestLimit` presentation shape. Complete run →
   `{"limited": False}` (frontend renders nothing); degraded run → `{"limited": True,
   "reason": <truthful>, "coverage_note": "<generated> of <total> planning artifacts were
   generated; <deferred> were deferred…"}`, with the optional commodity `upgrade`
   **alongside, never instead-of**. It produces no cognition, calls no provider, appends no
   CHR, and embeds **no §4c number** (coverage comes from the run's own counts; the cap that
   triggered the degrade lives only in `config.py`).
2. **Wired onto the run outputs envelope** — `infer/stage.py::build_infer_stage`'s stage fn
   now adds `outputs["honest_limit"] = honest_limit_for_result(result)`. This is the existing
   **non-canonical run/projection envelope** (`GraphState.outputs`) — **no schema change, no
   migration, no new projection field.** The cognition body (`synthesize_and_generate` /
   `run_synthesis_stage`) is **unchanged** (one-producer discipline preserved).

### Where the numbers come from

All from **config (Calibration §4c / A6)**, never invented: Fast 150k/run, Deep 600k/run,
daily 500k, monthly 4M, ~$3 Tier-1 — in `config.py` `_FREE_BUDGET` + `COST_PER_MILLION`.
The honest-limit code embeds **no** budget number (negative-asserted, see below). A3/A4
latency stays owner-TBD and was not touched.

### Honest-limit signal shape (matches the frontend)

Matches `frontend/src/components/HonestLimitDisclosure.tsx` `HonestLimit` interface verbatim:
`{ limited: bool, reason?: str, coverage_note?: str, upgrade?: { message, cta_label } }`.
Tests assert `{"limited","reason","coverage_note"} ⊆ signal` for a degraded run.

### Tests (TDD: red → green)

- **Positive** `tests/positive/synthesis/test_b2_honest_limit.py` (5): within-budget →
  `limited False`, no disclosure; over-budget → signal in the frontend shape; signal rides
  the run `outputs` envelope; coverage note reports the run's real generated/total counts;
  cap is the §4c config value (150k).
- **Negative** `tests/negative/synthesis/test_b3_honest_limit.py` (4): a degraded run is
  **never** presented as complete (`limited` can't be False); the disclosure is carried
  **alongside, never instead of** the upgrade (reason+coverage present even WITH an upgrade);
  **spend is still recorded on degradation** (one `ai_spend_recorded`, `degraded`+`over_budget`
  True); the honest-limit module embeds **no invented §4c number** (source-asserted).

### Verify — exact commands + results (`.venv/bin/`)

- `cd code && .venv/bin/pytest tests/positive tests/negative -q` → **746 passed, 65 skipped**
  (no regression). New honest-limit suites: **9 passed**. (A harmless OTel "Failed to export
  traces to 127.0.0.1" line appears — no local collector; not a test failure.)
- `.venv/bin/ruff check .` → **All checks passed!**
- `.venv/bin/python ci/gate_invariants.py` (gate-4) → **PASS**.
- `.venv/bin/python ci/gate_observability.py` (gate-5) → **PASS**.

### Constraints confirmed

- **No new dependency** (only `shared.epistemic.PLANNING_ARTIFACT_TYPES`, already in use).
- **No migration** (`git status` on persistence/migrations is clean; signal rides the
  existing `GraphState.outputs` envelope).
- **Cognition logic unchanged** — `synthesis.py` + `llm_provider/` have a zero diff; only
  `infer/stage.py` gained the presentation import + one `outputs` key.
- **Numbers from config/DL-048** — honest-limit code asserts no §4c literal; the cap is
  `budget_for_tier("free").per_run_cap("fast") == 150_000` (config).
- Working-tree changes unrelated to this task (`frontend/vite.config.ts`, `scripts/`) were
  preserved. Changes staged (not committed).

### Open note for review

The signal currently surfaces on the run `outputs` envelope (the in-process projection). It
is **not yet exposed over the DTM-0018 REST surface** — exactly the dependency the frontend
`honestLimit.fixtures.ts` flagged. Exposing it as a DTO is a REST-surface change beyond this
task's owned boundary (the task said "prefer the existing run/projection envelope; flag if a
projection field is needed"). No new field was needed on the envelope; a future REST slice can
read `outputs["honest_limit"]` without a schema change here.

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

## Approved by engineering manager

Status: Approved

Executive summary:
- Audit confirmed the DL-048 spend-gate (`RunBudget.can_afford/over_budget`), graceful degradation
  (synthesis defers over-budget artifacts), and `AI Spend Recorded` telemetry were already built +
  tested in Wave B. The only gap — the **honest-limit signal** — is now built: `infer/honest_limit.py`
  maps `SynthesisResult` → the frontend `HonestLimit` shape (`limited`/`reason`/`coverage_note`/
  `upgrade`), wired onto the run `outputs["honest_limit"]` envelope. Numbers from config (§4c/A6),
  none invented.

Verification (EM re-ran): `.venv/bin/pytest` → **746 passed, 65 skipped** (9 new; no regression).
ruff clean; gate-4 PASS; gate-5 PASS. No new dep, no migration; `synthesis.py`/`llm_provider/`
zero diff (already complete — not duplicated).

Negatives proven: degraded run never `limited:False`; disclosure alongside never instead-of the
upgrade; `ai_spend_recorded` still emitted on degradation (degraded+over_budget True); the
honest-limit module embeds zero §4c literals (numbers come from config).

Remaining risks / flagged follow-up: the honest-limit signal rides the in-process run envelope but
is not yet exposed over the DTM-0018 REST surface as a DTO field — the DTM-0029 frontend already
renders from its `limited` seam, so this is a small read-shape follow-up (expose `honest_limit` on
the analysis-run/projection DTO), not a functional gap.

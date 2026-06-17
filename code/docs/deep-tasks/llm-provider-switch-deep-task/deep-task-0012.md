# DTM-0012 — Internal Gemma (local Llama) as the primary LLM at the seam

**Status:** **Approved** (EM, 2026-06-17) · **Module:** DTM-0012 · **Contract / governing
decision:** **DL-059** (amends DL-054 §5) + **ADR-0007** · **Depends:** DL-059 ✓; ADR-0004
unchanged. · **Ops:** `base_url` is env config (placeholder in `.env.example`; owner sets the
live value); OpenAI-compatibility confirmed at the pydantic-ai layer.

## Goal / observable behavior

The PRIMARY LLM for OSLO is the internal `gemma4` model on a local Llama runtime
(OpenAI-compatible endpoint), reached behind the existing `/services/llm_provider` seam, run
natively (no Docker). The three cognition call sites now resolve to gemma; a live run needs no
OpenAI/Anthropic key. OpenAI/Anthropic remain a disabled fallback (config flip to re-enable).
Each cognition CHR records the **actual** provider/model used (`internal` / gemma id), not a
hardcoded "openai". Recorded-fixture CI (ADR-0004) is unchanged — zero provider calls in PR CI.

## Source docs / constraints

- DL-059 (`00_owner/decisions/decision_log.md`) cond. 1–5 — seam-only, Profile §5 controls +
  auditability preserved, ADR-0004 intact, no new dependency, no Docker, OpenAI-compatible
  assumed (else STOP).
- ADR-0007 (`code/docs/adr/0007-…`) — the engineering approach; ADR-0004 (recorded fixtures);
  `deep-task-decisions.md` (locked decisions #1–#5, Open items); ANTI_ASSUMPTION protocol.

## Locked decisions (from decisions file — do not re-derive)

- **config.py:** add an `internal` `TierRouting` (all stages → `ModelRef("internal", <gemma id
  from config>)`) and make internal the **primary/default** routing the engines resolve; keep
  OpenAI/Anthropic `ModelRef`s defined but non-primary. Add an internal/gemma row to
  `COST_PER_MILLION` = `(0.0, 0.0)`. `internal` budget reuses the Free `TierBudget` (no invented
  numbers).
- **adapter.py:** add `provider == "internal"` to `_build_live_model` →
  `OpenAIChatModel(model_ref.model, …)` against the **env `base_url`** (e.g. `OSLO_LLM_BASE_URL`),
  reusing the lazy import + `OSLO_LLM_LIVE` gate. No new dependency. The offline guard still
  raises `LiveCallsDisabledError` when no fixture + flag unset.
- **Provenance fix (the only edit to the frozen DTM-0009/0010 files):** in `infer/stage.py` and
  `infer/finding_stage.py`, replace the hardcoded `{"provider": "openai", "model_version": …}`
  CHR `model_or_rule_version` with the **resolved** identity from
  `provider.resolve(tier, stage)` (provider + model) merged with the existing prompt/rule
  version. Justified by DL-054 cond. 3 / DL-059 cond. 2 (model-consumption auditability).
- **Concrete `base_url` + model id = config, never hardcoded** (ANTI_ASSUMPTION). Wire the env
  var; put a commented placeholder (`gemma4`, a localhost `/v1` base_url) in `.env.example`. If
  the runtime is **not** OpenAI-compatible ⇒ **STOP and escalate** (native model class = new
  dependency decision).
- **CI stays recorded-fixture** — do not make any test call a network.

## Owned files / boundaries

- **OWN:** `backend/services/llm_provider/config.py`, `backend/services/llm_provider/adapter.py`,
  `.env.example`; the **provenance lines only** in `backend/responsibilities/infer/stage.py` +
  `backend/responsibilities/infer/finding_stage.py`; routing-assertion **tests** under
  `tests/{positive,negative}/**` that pin the primary provider (update in place) + any new
  adapter/routing/provenance unit tests.
- **READ-ONLY:** everything else — the 3 call sites' logic, `evaluate/**`, `orchestration/**`,
  `retain/**`, `perceive/**` (except none here), migrations, `events.py`/gate vocab, the
  recorded-fixture harness, ci gates. No behavior change to cognition; **seam + provenance +
  config only.**

## Packages / refactors

- None new. No refactor beyond the scoped provenance lines.

## Implementation instructions (TDD)

1. Red: update/author tests — primary routing resolves `internal`/gemma for all stages; adapter
   builds an `OpenAIChatModel` against the env base_url for `provider=="internal"` (no network);
   CHR provenance carries `provider=="internal"` + gemma id; `estimate_cost_usd(gemma)==0.0`;
   offline guard still raises with no fixture + flag unset; OpenAI/Anthropic fallback branch
   still constructs.
2. Green: `config.py` internal routing (primary) + cost row + budget mapping; `adapter.py`
   internal branch (env base_url); provenance fix in the 2 stage files; `.env.example` vars
   (`OSLO_LLM_BASE_URL`, model id, keep `OSLO_LLM_LIVE`; mark OpenAI/Anthropic optional).
3. Update the DL-048 routing negatives to the new primary (external full model still refused).
4. Do NOT change cognition logic, prompts, or the recorded fixtures' content.

## Test plan

- **Positive:** internal primary routing (3 stages); adapter internal-branch construction
  (env base_url, no network); CHR provenance accurate (synthesis + finding); gemma cost 0.0;
  fallback branch intact.
- **Negative/guard:** offline guard raises `LiveCallsDisabledError` (no fixture + flag unset)
  for internal too; external full model still refused for Free (updated wrong-tier negative);
  no test performs a real network call.
- ruff + gate-4 + gate-5 green; full suite no regression vs the Wave-B head (444/68 offline).

## Manual checks (EM / owner)

- Local Llama up + `OSLO_LLM_LIVE=1` + `OSLO_LLM_BASE_URL` set: one dev synthesis reaches gemma
  with no OpenAI/Anthropic key; `ai_spend_recorded.model` = gemma id, `est_cost` 0.
- `pytest` (flag unset) → zero network calls.

## Done criteria

- Internal gemma is the resolved primary at the seam; CHR provenance accurate; OpenAI/Anthropic
  a disabled fallback; recorded-fixture CI intact; no new dependency/Docker; `.env.example`
  documents the vars (placeholder; real values owner-set); PR cites DL-059 / ADR-0007.

## Worker report

**Ready for review.**

### Summary

Internal `gemma4` on a local Llama runtime (OpenAI-compatible endpoint) is now the resolved
PRIMARY behind the `/services/llm_provider` seam. Seam + provenance + config only — no cognition
logic, prompts, recorded-fixture content, gates, or events vocab changed. No new dependency
(reused pydantic-ai `OpenAIChatModel` + `OpenAIProvider(base_url=…)`), no Docker, no migration.
OpenAI-compatible assumption **held** (verified construction against a localhost `/v1` base_url
with zero network) → no STOP. CHR provenance now records the actual provider/model. Recorded-
fixture CI (ADR-0004) intact: zero provider calls offline.

### Files changed

| File | Change |
|---|---|
| `backend/services/llm_provider/config.py` | Added `internal_model_id()` (env `OSLO_LLM_MODEL`, default `gemma4`) + `INTERNAL_MODEL_ENV`/`DEFAULT_INTERNAL_MODEL`. Added `_internal_routing()` (all stages → `ModelRef("internal", gemma)`, OpenAI fallback ModelRef kept) as PRIMARY; demoted ex-Free OpenAI/Anthropic routing to `_OPENAI_FALLBACK_ROUTING` (defined, non-primary). `routing_for_tier` now returns the internal routing for every tier (free/internal/unknown). Added gemma row `(0.0,0.0)` to `COST_PER_MILLION`. `internal` tier reuses the Free `TierBudget` (no invented numbers). |
| `backend/services/llm_provider/adapter.py` | Added `provider == "internal"` branch to `_build_live_model`: lazily imports `OpenAIChatModel` + `OpenAIProvider`, builds against env `OSLO_LLM_BASE_URL` (+ optional `OSLO_LLM_API_KEY`, dummy if unset). Refuses with `LiveCallsDisabledError` if base_url env unset (no guessed URL). Added `INTERNAL_BASE_URL_ENV`/`INTERNAL_API_KEY_ENV`. `OSLO_LLM_LIVE` gate + recorded-fixture offline path UNCHANGED. Updated module docstring + the unknown-provider error text. |
| `backend/services/llm_provider/__init__.py` | Exported `internal_model_id`, `DEFAULT_INTERNAL_MODEL`, `INTERNAL_MODEL_ENV`, `INTERNAL_BASE_URL_ENV`; docstring updated. |
| `backend/responsibilities/infer/stage.py` | **Provenance only:** `planning_chr_spec` takes `model_identity`; `model_or_rule_version` now `{**resolved_identity, "model_version": SYNTHESIS_VERSION}`. `run_synthesis_stage` resolves the synthesis/generation identity via `engine.provider.resolve(...).model_ref.as_dict()` and passes it. No other logic touched. |
| `backend/responsibilities/infer/finding_stage.py` | **Provenance only:** `finding_chr_spec` takes `model_identity`; `model_or_rule_version` now `{**resolved_identity, "model_version": FINDING_VERSION}`. `run_finding_stage` resolves the synthesis-stage identity and passes it. No other logic touched. |
| `.env.example` | LLM section rewritten: primary = internal; added `OSLO_LLM_BASE_URL=` (commented placeholder `http://localhost:11434/v1`), `OSLO_LLM_MODEL=gemma4`, `OSLO_LLM_API_KEY=`, kept `OSLO_LLM_LIVE=`; `LLM_PRIMARY_PROVIDER=internal`; OpenAI/Anthropic keys marked optional disabled fallback. No active live URL. |

### Test updates (edit-in-place — DL-048 routing negatives repointed to the new primary)

| File / test | Change |
|---|---|
| `tests/negative/synthesis/test_b3_cost_governance.py` | `…routes_synthesis_to_mini…` → `…_to_internal…`: asserts internal/gemma primary for all stages + external full model (`gpt-4.1`, `openai`) still refused. |
| `tests/negative/evaluate/test_b3_cost_and_performance.py` | `…records_the_configured_free_tier_model…` → `…_primary_model…`: spend payload `model == internal_model_id()`, `!= gpt-4.1`, `est_cost == 0.0`. |
| `tests/positive/infer_finding/test_b2_cost_modes.py` | `…routes_finding_passes_to_the_cheap_model` → `…_to_the_internal_primary`: provider `internal`, model gemma, `!= gpt-4.1`. |
| `tests/replay/test_recorded_fixture_harness.py` | `test_no_provider_sdk_imported_by_importing_llm_provider` hardened to a **fresh-interpreter subprocess** check (the new live-branch tests legitimately import the SDK in-session, polluting global `sys.modules`; the guarded invariant — *importing the seam* pulls no SDK — is only meaningful in a clean interpreter). Same invariant, order-independent. |

### New tests

| File | Coverage |
|---|---|
| `tests/positive/llm_provider/test_internal_primary_dtm0012.py` | (a) primary routing resolves `internal`+gemma for all 3 stages + `internal` tier; model id is env config; (b) `_build_live_model("internal")` builds an `OpenAIChatModel` on the env base_url with NO network (asserts type + `client.base_url`); (d) `estimate_cost_usd(gemma)==0.0`; (e) OpenAI + Anthropic fallback branches still construct; `OSLO_LLM_LIVE` constant preserved. |
| `tests/positive/llm_provider/test_chr_provenance_dtm0012.py` | (c) synthesis + planning-artifact CHRs and Finding CHRs carry `model_or_rule_version.provider=="internal"` + gemma id (no `"openai"`), via the real stage runners over recorded fixtures. |
| `tests/negative/llm_provider/test_internal_guards_dtm0012.py` | offline guard raises `LiveCallsDisabledError` for internal with flag unset; internal branch refuses when `OSLO_LLM_BASE_URL` env unset (no guessed URL); external full model still wrong-tier for Free. |

### Exact commands + results

```
$ python -m pytest tests/positive tests/negative tests/replay -q
455 passed, 68 skipped, 1 warning   (baseline 444/68 + 11 new; ZERO regressions; zero provider calls)

$ ruff check .
All checks passed!

$ python -m ci.gate_invariants
[gate-4 epistemic-invariant] PASS: no forbidden tokens, no authority module, no canonical-table mutations in migrations.

$ python -m ci.gate_observability
[gate-5 observability] PASS: every CHR-append call-site emits 'cognition_history_record_appended', the per-contract A6 vocabularies are pinned verbatim (union consistent), and the replay harness is present.
```

(Interpreter: repo `.venv` / Python 3.12.11. OTEL "Failed to export traces" lines in test output are a pre-existing local-collector artifact, not provider calls.)

### Flags for review

- **Env base_url placeholder (ops, non-blocking):** `OSLO_LLM_BASE_URL` is a commented placeholder
  (`http://localhost:11434/v1`) — the owner sets the live value. The active value is empty; the
  adapter refuses a live call if it's unset (`LiveCallsDisabledError`).
- **OpenAI-compatible assumption — CONFIRMED (no STOP):** pydantic-ai `1.107.0`'s `OpenAIChatModel`
  + `OpenAIProvider(base_url=…, api_key=…)` constructs against a local `/v1` endpoint with no
  network and no new dependency. If a deploy target's runtime is NOT OpenAI-compatible, that is a
  separate native-SDK dependency decision (DL-059 cond. 4) — escalate then.
- **Provenance edit to the 2 frozen DTM-0009/0010 files:** the ONLY change is the
  `model_or_rule_version` dict (now resolved identity, was hardcoded `"openai"`) + threading
  `model_identity` from `provider.resolve(...)`. Justified by DL-054 cond. 3 / DL-059 cond. 2
  (model-consumption auditability). No cognition logic, payloads, events, or topology touched.
- **Pre-existing test hardening:** the one non-routing test edit (`test_recorded_fixture_harness.py`)
  was forced by the new live-branch construction tests; it preserves the exact same invariant via a
  subprocess. Called out explicitly since it's outside the "routing-assertion" set.
- **Budgets:** `internal` reuses the Free `TierBudget` (ANTI_ASSUMPTION — no invented numbers).

## Engineering-manager review notes

**Review (2026-06-17).** Single worker, no STOP. EM independently verified:

- **Scope correct:** `config.py`, `adapter.py`, `__init__.py`, `.env.example`; the **provenance
  edit only** in `infer/stage.py` + `infer/finding_stage.py` (added an optional `model_identity`
  param threaded from `provider.resolve(...).model_ref.as_dict()`; CHR `model_or_rule_version`
  now records the resolved provider/model, not hardcoded "openai" — no cognition-logic change);
  3 DL-048 routing negatives edited in place; 2 new `tests/{positive,negative}/llm_provider/`
  suites; 1 guard-test rewrite (below). **`pyproject.toml` untouched — no new dependency.**
- **Adapter (read):** `provider == "internal"` lazily builds `OpenAIChatModel` +
  `OpenAIProvider(base_url=os.environ[INTERNAL_BASE_URL_ENV])`; **refuses with
  `LiveCallsDisabledError` if the base_url env is unset — no guessed URL** (ANTI_ASSUMPTION
  held). `OSLO_LLM_LIVE` gate + recorded-fixture offline path unchanged; OpenAI/Anthropic
  branches retained as the disabled fallback.
- **Config (read):** internal routing (all stages → `ModelRef("internal", internal_model_id())`,
  env `OSLO_LLM_MODEL` default `gemma4`) is the primary `routing_for_tier` returns; ex-Free
  OpenAI/Anthropic kept as a defined-but-non-primary fallback; gemma cost row `(0.0,0.0)`;
  `internal` budget reuses Free (no invented numbers).
- **Guard-test rewrite (the flagged out-of-routing edit) — accepted:**
  `test_no_provider_sdk_imported_by_importing_llm_provider` now runs in a fresh-interpreter
  subprocess. Justified: the new live-branch construction tests legitimately import the SDK
  in-session, so the "bare import pulls no provider SDK" invariant is only meaningful in a clean
  process. The rewrite preserves — and strengthens (order-independent) — the invariant. Verified
  the subprocess asserts both `pydantic_ai.models.openai`/`.anthropic` absent after importing the
  seam.
- **CI premise intact (ADR-0004):** zero provider calls offline; the live `internal` path is
  flag+base_url gated.

**EM-run verification (independent, 2026-06-17, offline):**
- `ruff check .` → clean · `ci.gate_invariants` → PASS · `ci.gate_observability` → PASS ·
  `pytest tests/positive tests/negative tests/replay` → **455 passed, 68 skipped, 0 failed**
  (branch head 444 → +11; no regression).

## Approved by engineering manager

Status: Approved

Executive summary:
- DTM-0012 enacts DL-059 / ADR-0007: the internal `gemma4` model on a local Llama runtime
  (OpenAI-compatible endpoint) is the resolved PRIMARY LLM behind the existing
  `/services/llm_provider` seam — config + adapter only, plus a provenance fix so each cognition
  CHR records the actual provider/model (Profile §5 auditability). No new dependency, no Docker,
  no schema change; OpenAI/Anthropic remain a disabled fallback (config flip to re-enable);
  recorded-fixture CI is untouched. The concrete `base_url` is env config (placeholder in
  `.env.example`; the adapter refuses rather than guess).

Verification:
- ruff clean · gate-4 PASS · gate-5 PASS · pytest 455 passed / 68 skipped / 0 failed offline
  (+11). Scope-checked: pyproject untouched (no new dep); frozen stage files changed only for
  provenance; cognition logic unchanged.

Manual test plan:
- Start the local Llama runtime serving `gemma4`; set `OSLO_LLM_LIVE=1` + `OSLO_LLM_BASE_URL=<the
  /v1 endpoint>` (+ `OSLO_LLM_MODEL` if not `gemma4`). Run one dev synthesis → it reaches gemma
  with no OpenAI/Anthropic key; `ai_spend_recorded.model` = the gemma id, `est_cost` 0; the
  synthesis/finding CHRs show `model_or_rule_version.provider == "internal"`.
- `pytest` with the flag unset → zero network calls.

Remaining risks:
- The OpenAI-compatibility of the specific runtime is confirmed at the pydantic-ai layer
  (constructs against a localhost `/v1` base_url); a true end-to-end live call is the owner's
  manual check above once the runtime + base_url are provided.
- Paid/internal-tier budget numbers remain owner-deferred (internal reuses Free as a
  soft/observability bound).

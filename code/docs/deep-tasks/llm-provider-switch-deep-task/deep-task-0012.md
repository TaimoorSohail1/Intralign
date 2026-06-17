# DTM-0012 — Internal Gemma (local Llama) as the primary LLM at the seam

**Status:** Planned — BLOCKED on owner go-ahead + the base_url/model-id ops item · **Module:**
DTM-0012 · **Contract / governing decision:** **DL-059** (amends DL-054 §5) + **ADR-0007** ·
**Depends:** DL-059 ratified ✓; ADR-0004 (test premise) unchanged.

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

_(worker fills)_

## Engineering-manager review notes

_(EM fills)_

## Approved by engineering manager

_(added only after verification passes)_

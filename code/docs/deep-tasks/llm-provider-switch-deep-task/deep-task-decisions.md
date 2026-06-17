# Deep-task decisions — Internal Gemma as primary LLM (DL-059 / ADR-0007)

Implementation-control record for the LLM provider switch. Cites source-of-truth; does not
restate it. Single slice (DTM-0012). **Branch:** `feat/phase3-waveb-understanding` (the DL-059 /
ADR-0007 doc edits already live in this working tree).

## Source-of-truth docs (binding; read, do not edit from deep-task)

- **DL-059** — `00_owner/decisions/decision_log.md` (amends DL-054 §5): internal `gemma4` on a
  local Llama runtime is the PRIMARY LLM, native/no-docker, behind `/services/llm_provider`;
  OpenAI/Anthropic → optional disabled fallback. Conditions 1–5 govern this task.
- **ADR-0007** — `code/docs/adr/0007-internal-gemma-primary-llm.md` (the engineering "how").
- **ADR-0004** — recorded-fixture test strategy (UNCHANGED — CI stays offline/fixtures).
- DL-054 §5 + cond. 3 (Profile §5 controls: routing/quota/**auditability**); DL-048 §4c
  (routing/budget); `00_owner/ANTI_ASSUMPTION_BUILD_PROTOCOL.md`; `code/CLAUDE.md` (stack line,
  STOP rules); `code/CONTEXT.md`.

## Repo facts (current seam)

- `backend/services/llm_provider/config.py`: `Tier = Literal["free","paid","internal"]`
  (the `internal` tier literal **already exists** but has no routing). `_FREE_ROUTING` →
  OpenAI nano/mini + Anthropic haiku fallback. `routing_for_tier`/`budget_for_tier` fall back
  to Free for unknown tiers. `COST_PER_MILLION` has no gemma row. `estimate_cost_usd` →
  0.0 for unknown models (ANTI_ASSUMPTION).
- `backend/services/llm_provider/adapter.py`: `LLMProvider._build_live_model` branches on
  `provider == "openai" | "anthropic"` and lazily imports the SDK. The `OSLO_LLM_LIVE` gate +
  the recorded-fixture path (`recorded_model`) are the offline discipline.
- `.env.example`: `LLM_PRIMARY_PROVIDER=openai`, `LLM_FALLBACK_PROVIDER=anthropic`,
  `OPENAI_API_KEY=`, `ANTHROPIC_API_KEY=` — no base_url / internal-model vars yet.
- **Provenance hardcode (wrinkle):** `infer/stage.py:80` and `infer/finding_stage.py:73`
  hardcode `model_or_rule_version = {"provider": "openai", "model_version": …}` in the CHR
  spec. After the switch this records the WRONG provider → breaks Profile §5
  "model-consumption auditability" (DL-054 cond. 3 / DL-059 cond. 2).
- Call sites reach the model ONLY via `LLMProvider` (`perceive/extraction.py`,
  `infer/synthesis.py`, `infer/finding.py`); Evaluate uses no LLM.

## Locked decisions

1. **Seam-only + provenance (DL-059 cond. 1, plus the auditability fix):**
   - `config.py`: add an `internal` `TierRouting` whose stages all resolve to
     `ModelRef("internal", <model-id-from-env>)`, and make **internal the primary** (the
     active/default routing the engines resolve). Keep OpenAI/Anthropic `ModelRef`s present
     but non-primary (disabled fallback). Add a `gemma`/internal row to `COST_PER_MILLION` as
     `(0.0, 0.0)` (local inference is un-metered → `est_cost` 0; tokens still recorded).
   - `adapter.py`: add a `provider == "internal"` branch in `_build_live_model` →
     `OpenAIChatModel(model_ref.model, …)` pointed at the local **`base_url` read from env**
     (OpenAI-compatible). Reuse the existing lazy-import + `OSLO_LLM_LIVE` gate; no new import.
   - **Provenance fix (minimal, touches the 2 frozen stage files):** replace the hardcoded
     `{"provider": "openai", …}` in `infer/stage.py` and `infer/finding_stage.py` with the
     **resolved** model identity (`provider.resolve(...).model_ref.as_dict()` merged with the
     prompt/rule version), so the CHR records the actual provider/model. This is the only edit
     to the frozen DTM-0009/0010 files and is justified by the auditability condition.
2. **Concrete values are config, NOT code (ANTI_ASSUMPTION):** the `base_url` and exact model
   id are **owner/ops-confirmed** and live in `.env` / config — the worker wires the env var
   and puts a clearly-commented placeholder in `.env.example`; it does **NOT** hardcode or
   invent a URL. Owner-given model id is `gemma4` (used as the documented default placeholder).
3. **Recorded-fixture CI unchanged (ADR-0004):** PR CI makes zero provider calls; the
   `internal` provider is exercised live only under `OSLO_LLM_LIVE=1` (dev/nightly) + as the
   fixture source. No test should newly call a network.
4. **No new dependency, no Docker** (DL-059 cond. 4/5): reuse `OpenAIChatModel(base_url=…)`. If
   the runtime turns out **non-OpenAI-compatible**, a native model class is a separate
   dependency decision ⇒ **STOP and escalate** (do not add an SDK).
5. **Budgets:** `internal` tier reuses the Free `TierBudget` as a soft/observability bound
   (local is un-metered) — do **not** invent new numbers.

## Packages / refactors

- **No new package** (`pydantic-ai` `OpenAIChatModel` already used). No refactor beyond the
  scoped provenance fix in the 2 stage files.

## Open items

- **OPEN (ops config, non-blocking for code structure):** concrete `base_url` + exact model id
  + confirmation the runtime is **OpenAI-compatible** (grill Q2, unanswered). The worker can
  wire `OSLO_LLM_BASE_URL` (read from env) and leave `.env.example` with a commented
  placeholder; the live value is set at deploy. **If non-OpenAI-compatible ⇒ STOP.**
- **Test updates expected:** routing-assertion tests that pin OpenAI as Free's primary (the
  DL-048 "wrong-tier routing" negatives, e.g. `…spend_records_the_configured_free_tier_model…`)
  must be updated to assert **internal gemma is primary** and an external full model is still
  refused. These are additive/edit-in-place, not new contracts.
- **Branch:** kept on `feat/phase3-waveb-understanding` (the DL-059/ADR-0007 doc edits are
  already here). Owner may prefer a dedicated branch — confirm.
- **GATE — owner says do not start coding until confirmed** (+ resolve the base_url/model-id
  ops item). This file + the plan + DTM-0012 are planning only.

## Slice index

| Task | Scope | File |
|---|---|---|
| DTM-0012 | Internal-Gemma primary at the seam + provenance fix + env + test updates | `deep-task-0012.md` |

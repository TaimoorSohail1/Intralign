# Deep-task plan — Internal Gemma as primary LLM (DL-069 / ADR-0007)

Single vertical slice on `feat/phase3-waveb-understanding`. One fresh worker, EM
review → fix → verify → approve. **Coding gated on owner confirm + the base_url/model-id
ops item (decisions, Open items).**

## Slice

| # | Module | Slice (vertical outcome) | Source | Depends on |
|---|---|---|---|---|
| 1 | DTM-0012 | Internal `gemma4` (local Llama, OpenAI-compatible) is the primary LLM behind the existing seam: `config.py` internal routing (primary) + `adapter.py` internal branch (`base_url` from env) + CHR provenance reflects the resolved provider/model + `.env.example` vars; recorded-fixture CI unchanged; routing-assertion tests updated. | DL-069, ADR-0007, ADR-0004 | DL-069 ratified ✓; ops base_url/model-id ⏳ |

## Test strategy

- **Recorded-fixture CI stays green offline (ADR-0004):** zero provider calls in `pytest`; the
  adapter's offline guard (`LiveCallsDisabledError` when no fixture + flag unset) still holds
  for the `internal` provider too.
- **Routing:** a positive test asserts the primary routing now resolves `provider == "internal"`,
  model == the configured gemma id, for extraction/synthesis/generation; the DL-048
  "wrong-tier / external-full-model" negatives are updated to the new primary (an external full
  model is still refused for Free).
- **Adapter:** unit-test that `_build_live_model` for `provider == "internal"` builds an
  `OpenAIChatModel` against the env `base_url` **without** importing/calling a network — assert
  on construction/config, not a live call (or monkeypatch). The OpenAI/Anthropic branches still
  work (fallback retained).
- **Provenance:** a test asserts a synthesis CHR and a finding CHR carry
  `model_or_rule_version.provider == "internal"` and the gemma model id (no hardcoded "openai").
- **Cost:** `estimate_cost_usd(<gemma id>, …) == 0.0` (local/free) and `ai_spend_recorded` still
  records real token counts.
- Full suite + ruff + gate-4 + gate-5 green; baseline (444 passed / 68 skipped offline at the
  Wave-B head) must not regress.

## Manual checks (EM / owner)

- With the local Llama runtime up + `OSLO_LLM_LIVE=1` + `OSLO_LLM_BASE_URL` set: run one live
  synthesis (dev) → confirm it reaches gemma (no OpenAI/Anthropic key needed) and emits
  `ai_spend_recorded` with `model` = the gemma id, `est_cost` 0.
- Confirm `pytest` with the flag unset makes zero network calls (offline guard).

## Done = provider switched

Primary LLM is internal gemma at the seam; CHR provenance is accurate; OpenAI/Anthropic remain
a disabled fallback (config flip to re-enable); recorded-fixture CI intact; no new
dependency/Docker; PR cites DL-069 / ADR-0007. `.env.example` documents the env vars with a
placeholder (concrete values owner-set).

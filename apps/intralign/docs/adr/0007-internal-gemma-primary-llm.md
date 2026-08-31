# Internal Gemma (local Llama runtime) is the primary LLM, behind the existing seam

DL-054 §5 bound the LLM to "Pydantic AI + adapter, OpenAI primary / Anthropic fallback."
**DL-069 (owner-directed, 2026-06-17) amends that:** the primary LLM — for the application
runtime and as the live/baseline test runtime — is an internal, already-installed `gemma4`
model served by a **local Llama runtime** (llama.cpp/Ollama-style), run **natively, not
dockerised**. OpenAI/Anthropic drop to an optional, disabled-by-default fallback. This ADR
records how that lands in `code/`; DL-069 is the governing decision.

The change is deliberately confined to the **provider seam**. The local Llama runtime exposes
an **OpenAI-compatible `/v1` endpoint**, so the seam keeps using Pydantic AI's
`OpenAIChatModel` pointed at a local `base_url` with the `gemma4` model id — **no new
dependency, no new model class**. The three cognition call sites
([`perceive/extraction.py`](../../backend/responsibilities/perceive/extraction.py),
[`infer/synthesis.py`](../../backend/responsibilities/infer/synthesis.py),
[`infer/finding.py`](../../backend/responsibilities/infer/finding.py)) reach the model only
through [`LLMProvider`](../../backend/services/llm_provider/adapter.py) and do **not** change.
Evaluate stays rule-arithmetic (no LLM).

Concretely, the code change (follow-up, docs-first per owner) is:
- [`config.py`](../../backend/services/llm_provider/config.py): add an `internal` tier routing
  (and/or repoint `_FREE_ROUTING`) whose stages resolve to `ModelRef("internal", "gemma4")`;
  keep OpenAI/Anthropic refs present but non-primary.
- [`adapter.py`](../../backend/services/llm_provider/adapter.py) `_build_live_model`: for the
  `internal` provider, construct `OpenAIChatModel(model_ref.model, base_url=<local>, …)`
  against the local endpoint. The `OSLO_LLM_LIVE` gate and the recorded-fixture path are
  unchanged.
- `.env.example`: the local `base_url` + model id (ops-confirmed values).

## Status

accepted — governed by DL-069 (owner-directed, 2026-06-17). Docs updated first; the
seam code change follows.

## Considered Options

- **Native model class for Ollama/Gemma** — rejected for now: a new provider SDK/class is a
  new dependency (STOP / separate approval). Only taken if the runtime is **not**
  OpenAI-compatible (DL-069 cond. 4).
- **OpenAI-compatible local endpoint via `OpenAIChatModel(base_url=…)` (chosen)** — zero new
  dependency, smallest seam change, reuses all routing/budget/audit plumbing.
- **Keep OpenAI/Anthropic primary** — rejected by owner (external token cost + data egress;
  an internal model is installed and free).

## Consequences

- **Determinism (ADR-0004) is unchanged and still correct:** a local model is still
  nondeterministic, so PR CI stays on recorded model-response fixtures (offline, deterministic,
  free). `gemma4` becomes the model that **records/refreshes** those fixtures and drives
  dev/nightly + live integration tests — not a per-PR live call. A `gemma4` version bump is a
  **new baseline (DT-6)**, not a regression.
- **Cost governance (DL-048) still applies as observability:** `AI Spend Recorded` keeps
  emitting token counts even though local inference is un-metered — the per-tier budget becomes
  a soft/observability bound rather than a billing cap. Routing/quota/audit (Profile §5) are
  preserved.
- **No Docker for the LLM:** the runtime is a native sidecar (Profile §6 — only backing
  services are containerised). `docker-compose.yml` is not touched for the model.
- **Reversible:** OpenAI/Anthropic refs remain in the routing table behind the seam; re-enabling
  them is a config flip (and an owner decision), not a rewrite.
- **One open variable:** the concrete local `base_url` + exact `gemma4` model id are
  ops-confirmed in `.env.example`; if the runtime turns out non-OpenAI-compatible, the native
  model class is a separate dependency decision (DL-069 cond. 4).

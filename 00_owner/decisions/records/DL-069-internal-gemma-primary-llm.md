# DL-069 — Internal Gemma (local Llama runtime) as the primary LLM (amends DL-054 §5)

- **Date:** 2026-06-18 · **Status:** Ratified · **Decided by:** Idris (Founder Console)
- **Class:** A

- **Source:** Owner direction (2026-06-17, this session), confirmed ratified by the owner via the Founder Console. Recorded by AI contributor as scribe (non-ratifying — the owner ratifies, per `CLAUDE.md` Authority Constraint).
- **Layer:** Implementation / environment binding (`30_engineering/environment`). Amends **DL-054 §5 (LLM strategy)** and `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` §5. **DL-043 platform architecture and every epistemic invariant unchanged** — this binds the LLM provider/runtime only.
- **Numbering note:** Originally scribed as "DL-059" on branch `feat/phase3-waveb-understanding` (pre-DL-065 monolith style, reserving a number against the in-flight unarchive branch). Re-recorded here as **DL-069** under the DL-065 number-at-merge records discipline (one file per decision; numbers assigned at merge, not reserved). Code/docs that reference "DL-059" should be updated to **DL-069**.

## Decision
The **primary LLM** for OSLO Release 1 — for **application runtime** and as the **live/baseline test runtime** — is an **internal, already-installed `gemma4` model served by a local Llama runtime** (llama.cpp / Ollama-style), reached behind the canon-mandated `/services/llm_provider` seam. It runs **natively as a local sidecar — NOT dockerised** (consistent with Profile §6: only backing services are Dockerized). OpenAI/Anthropic are **demoted from primary**: retained only as an optional, disabled-by-default fallback behind the same seam (not used unless the owner re-enables).

## Rationale
An internal model removes external-provider token cost and data-egress, and the local Llama runtime exposes an OpenAI-compatible endpoint so the existing Pydantic AI seam is reused with no new dependency. The change is confined to the provider seam; the cognition call sites and epistemic discipline are untouched.

## Conditions
1. **Seam-only change.** Only `code/backend/services/llm_provider/{config.py,adapter.py}` change; the three call sites (Perceive extraction, Infer synthesis/generation, Infer findings) reach the model **only** through `LLMProvider` — unchanged. Evaluate remains rule-arithmetic (no LLM).
2. **Profile §5 controls preserved (DL-054 cond. 3):** workload-based routing, usage quotas, and model-consumption auditability stay; cost-governance still emits `AI Spend Recorded` (token accounting/observability applies even though local inference is un-metered).
3. **Determinism unchanged (ADR-0004 intact):** PR CI stays on **recorded model-response fixtures** (a local model is still nondeterministic); `gemma4` is the live model **and** the source that records/refreshes those fixtures (dev + nightly), not a per-PR live call. A model-version change is a **new baseline (DT-6)**, never a regression.
4. **Integration mechanism (assumed; confirm before code):** the Llama runtime exposes an **OpenAI-compatible** `/v1` endpoint, so the seam reuses Pydantic AI's `OpenAIChatModel` with a local `base_url` + the `gemma4` model id — **no new dependency**. The concrete `base_url` and exact model id are ops-confirmed (recorded in `code/.env.example`). If the model is served via a **non-OpenAI-compatible** API, adding a native model class is a **separate dependency decision** (STOP / new approval).
5. **No new dependency / no Docker for the LLM.** Adding a provider SDK or containerising the model would exceed this decision.

## Supersedes / Amends
**Amends DL-054 §5** (primary provider OpenAI → internal Gemma; Anthropic fallback → optional/disabled) and `RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1` §5. Preserves DL-054 cond. 1–3 (observability additive; audit-retention owner-pending; §5 controls). No other DL-054 content changed. DL-043 platform architecture and all epistemic invariants unchanged.

## Affected artifacts (each via branch → PR → green gate → owner merge)
`30_engineering/environment/RUNTIME_ENVIRONMENT_CONSTRAINT_PROFILE_V1.md` §5; `code/CLAUDE.md` (stack line); `code/docs/adr/0007-internal-gemma-primary-llm.md` (new) + `code/docs/adr/0004-…` (test-premise note); `code/backend/services/llm_provider/{config.py,adapter.py}` + `code/.env.example`. Most of these ride in PR #39 (Wave B); this record supplies the governance basis they cite (replacing the branch's "DL-059" monolith entry).

## Provenance
Owner-ratified 2026-06-17 (Founder Console). Realizes the governance basis for PR #39's DTM-0012 (internal Gemma at the seam). Landed via the DL-065 number-at-merge records discipline.

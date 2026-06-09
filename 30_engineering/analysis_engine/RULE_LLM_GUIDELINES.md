# Rule vs LLM Guidelines

**Status:** Active Architecture V1 · **Date:** 2026-05-31
**Grounded in:** Analysis Engine (determinism §15, replay §16) · Planning Intelligence · CAF/Reliability/Confidence models (formula-free) · Event Model (idempotency §17). Tags: `canonical` / `derived` / `proposal` / `TBD`.

> Principle: maximize the deterministic surface; reserve the LLM for genuinely semantic work. Every stage pulled out of the LLM is faster, cheaper, and fully deterministic — which shrinks the bounded-equivalence band that must be defended for the LLM parts.

## 1. What MUST be deterministic (rule) `derived`/`proposal`

- Intake validation, envelope/type checks, provenance capture, run enqueue (`canonical` plumbing).
- Normalization: parsing, segmentation, span tagging.
- Entity/term indexing, cross-reference linking (candidate generation).
- Intrinsic **Clarity** detection: vagueness lexicon, missing-units, internal inconsistency.
- Absence/coverage checks against the index (missing information, coverage gap, unsupported-assertion graph check).
- Constraint extraction (dates, budgets, counts) via NER/regex.
- Finding object **emission** (type, dimension, basis links assembly).
- Recommendation **type selection** (finding-type → recommendation-type mapping).
- Confidence/CAF **state assembly**, supersession-pointer maintenance, reliability-qualifier attachment.
- `canonical_key`/hash for dedup and determinism.
- MRI render, atomic persistence, event emission, state transitions.

## 2. What MAY use the LLM `canonical`/`derived`

- Intent restatement and relationship-skeleton semantics (global map).
- Claim identification incl. paraphrased/implicit claims; `normalized_text`.
- Relational **Alignment/Feasibility** judgment.
- **Conflict discovery** (logical incompatibility, intent drift).
- Deeper assumption/claim discovery (Deep).
- Recommendation **rationale** phrasing.

## 3. What the LLM is FORBIDDEN to do `canonical`

- Introduce any **formula, weight, percentage, or threshold** for CAF, Reliability, or Confidence.
- Produce a confidence value not derived from CAF + Reliability, or a **bare** (unqualified) confidence value.
- Emit **prescriptive** content inside a Finding (findings are descriptive).
- **Apply** a recommendation, decide, accept, or govern (advisory only; user decides).
- Invent entities, states, or events outside the Data/State/Event models.
- Perform governance, accepted-understanding, agent-governance, autonomous execution, actuation, or outcome orchestration.
- Treat Fast output as final understanding.
- Emit any output without a resolvable source span / basis.

## 4. Schema validation requirements `proposal`

- Every LLM output is parsed against a **fixed schema** (see `analysis_contracts.py`); non-conforming output is rejected and retried (§6).
- Enum-valued fields validated against `analysis_enums.py`; unknown values rejected.
- Structured claim/finding/recommendation records must populate all required fields or be discarded.
- No free-form field may carry a state, score, or event name not defined in the models.

## 5. Source-span requirements `canonical`

- Every claim, finding, and relationship must carry a **resolvable source span** (`evidence_id` + offsets) — explainability to basis is mandatory (Engine §21; Reliability/CAF explanation models).
- Items lacking attribution are invalid and dropped.
- Spans must survive normalization (Stage 1) so reconstruction is exact.

## 6. Retry / fallback behavior `derived`/`proposal`

- **LLM call retry:** schema-invalid or failed output retried up to a bounded count (**`TBD – Owner Decision Required`**), same inputs.
- **Stage fallback:** if the global skeleton (Fast S2) fails, degrade to isolation-only with **reduced reliability** (Coverage ↓) rather than failing the run.
- **Run failure:** a failed analysis is **not** restarted in place — a **new** `AnalysisRun` is queued (`previous_run_id`); prior run retained (Engine §20).
- **Idempotency:** events deduped on `event_id`; transitions are set-to-state; identical-input re-runs do not fabricate new states (no-change → no-recompute).

## 7. Token / output budget guidance `proposal`/`TBD`

- Bottleneck is **output decode**, not input prefill (≤ envelope fits one context).
- Keep the global map **output-light** (compact index/skeleton).
- Bound Fast claim extraction to the salient subset (~50–100 claims — **proposal/TBD**) to protect the 60s budget.
- Per-claim structured output budget ≈ proposal; exact per-call output limits **`TBD – Owner Decision Required`**.
- Prefer terse structured schemas over verbose prose to reduce decode time.

## 8. Parallelism guidance `proposal`

- **Fast:** parallelize claim extraction across chunks, but every chunk **carries the Stage-2 global map** as shared context (preserves global semantics; prevents chunk-boundary determinism hazards).
- **Deep:** parallelize extraction/expansion across the corpus; merge/dedup by `canonical_key`; single active deep run per project with event coalescing.
- Run fan-out ordering (`confidence → finding → recommendation → notification`) must be preserved under one `correlation_id` regardless of parallelism (Event Model §16).

## 9. Determinism contract reference `canonical`

- Same inputs + same pinned model configuration ⇒ **bounded-equivalent** governable outputs (finding-type set, recommendation set, confidence band, reliability qualifier). Exact tolerance **`TBD – Owner Decision Required`** (Engine §15).
- Replay reconstructs persisted state from the event log exactly; external side effects suppressed (Engine §16).
- Configuration (model version + settings) recorded per run.
